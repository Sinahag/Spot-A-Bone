#include "includes/nfcReader.h"

tagWithUID tagDatabase[] = {
    {1, {0x04, 0x86, 0x6a, 0xb1, 0x70, 0x00, 0x00}},
    {2, {0x04, 0x87, 0x6a, 0xb1, 0x70, 0x00, 0x00}}
};

int numTags = 2;
int maxTagTens = 2;

char *queueFileName = "/mnt/remote/myApps/NFC.txt";

void NFC_initialize(NFC_descriptor* desc){
	NFC_runCommand("config-pin P9_18 i2c");
	NFC_runCommand("config-pin P9_17 i2c");

	// Initialize libnfc and set the nfc_context
	nfc_init(&(desc->cont));
	if (desc->cont == NULL)
	{
		printf("Unable to init libnfc (malloc)\n");
		exit(EXIT_FAILURE);
	}

	// Open, using the first available NFC device which can be in order of selection:
	//   - default device specified using environment variable or
	//   - first specified device in libnfc.conf (/etc/nfc) or
	//   - first specified device in device-configuration directory (/etc/nfc/devices.d) or
	//   - first auto-detected (if feature is not disabled in libnfc.conf) device
	desc->dev = nfc_open(desc->cont, NULL);

	if (desc->dev == NULL)
	{
		printf("ERROR: %s\n", "Unable to open NFC device.");
		exit(EXIT_FAILURE);
	}
	// Set opened NFC device to initiator mode
	if (nfc_initiator_init(desc->dev) < 0)
	{
		nfc_perror(desc->dev, "nfc_initiator_init");
		exit(EXIT_FAILURE);
	}

	printf("NFC reader: %s initialized.\n", nfc_device_get_name(desc->dev));
	return;
}

int NFC_poll(NFC_descriptor* desc){
	// Poll for a ISO14443A (MIFARE) tag
	const nfc_modulation nmMifare = {
		.nmt = NMT_ISO14443A,
		.nbr = NBR_106,
	};

	int tagNumber = 0;

	if (nfc_initiator_select_passive_target(desc->dev, nmMifare, NULL, 0, &(desc->targ)) > 0){
		tagNumber = NFC_findOutWhichTag((desc->targ).nti.nai.abtUid, (desc->targ).nti.nai.szUidLen);
	}
	return tagNumber;
}

void NFC_end(NFC_descriptor* desc){
	// Close NFC device
	nfc_close(desc->dev);
	// Release the context
	nfc_exit(desc->cont);
}


int NFC_findOutWhichTag(const uint8_t *pbtData, const size_t szBytes){
	size_t szPos;
	bool equal = true;
	for (int i = 0; i < numTags; i++){
		equal = true;
		for (szPos = 0; szPos < szBytes; szPos++)
		{
			if (pbtData[szPos] != tagDatabase[i].UID[szPos]){
				equal = false;
				break;
			}
		}
		if (equal){
			return i+1;
		}
	}
	return 0;
}

void NFC_queueUp(int tagNum){
	FILE *pFile;
	while((pFile = fopen(queueFileName, "ab")) == NULL); // Wait if cannot open... (somewhat like a mutex)
	
	char toWrite[maxTagTens];
	sprintf(toWrite, "%d\n", tagNum);
    fprintf(pFile, toWrite);

    fclose(pFile);
}


void NFC_runCommand(char *command)
{
	// Execute the shell command (output into pipe)
	FILE *pipe = popen(command, "r");
	// Ignore output of the command; but consume it
	// so we don't get an error when closing the pipe.
	char buffer[1024];
	while (!feof(pipe) && !ferror(pipe))
	{
		if (fgets(buffer, sizeof(buffer), pipe) == NULL)
			break;
		// printf("--> %s", buffer); // Uncomment for debugging
	}
	// Get the exit code from the pipe; non-zero is an error:
	int exitCode = WEXITSTATUS(pclose(pipe));
	if (exitCode != 0)
	{
		perror("Unable to execute command:");
		printf(" command: %s\n", command);
		printf(" exit code: %d\n", exitCode);
	}
}
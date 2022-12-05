#include "includes/button.h"
#include <stdio.h>

void button_initiate(){
    button_runCommand("config-pin p8.43 gpio"); //force the button's pin to be treated as GPIO
    writeToFile(BUTTON_pathDirection, "in");
    writeToFile(BUTTON_pathactiveLow, "1");
}

// Implementation wholely inspired from assignment document (Brian Fraser)
void writeToFile(char *fileName, char *toWrite){
    FILE *pFile = fopen(fileName, "w");
    if (pFile == NULL) {
        printf("ERROR: Unable to open export file.\n");
        exit(1);
    }

    fprintf(pFile, toWrite);

    fclose(pFile);
}

// Implementation partially inspired from assignment document (Brian Fraser)
int readButton(char *fileName){
    FILE *pFile = fopen(fileName, "r");
    if (pFile == NULL) {
        printf("ERROR: Unable to open file (%s) for read\n", fileName);
        exit(-1);
    }
    // Read string (line)
    char result[MAX_LENGTH];
    fgets(result, MAX_LENGTH, pFile);
    // Close
    fclose(pFile);
    if (result[0] == '1')
        return 1;
    else   
        return 0;
}

void button_runCommand(char *command)
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
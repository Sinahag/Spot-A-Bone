#ifndef NFCREADER_H_
#define NFCREADER_H_

#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/ioctl.h>
#include <linux/i2c.h>
#include <linux/i2c-dev.h>
#include <nfc/nfc.h>

#define UID_len 7

typedef struct{
    int tagNumber;
    uint8_t UID[7];
} tagWithUID;


typedef struct{
    nfc_device *dev;
    nfc_target targ;
	nfc_context *cont;
} NFC_descriptor;

void NFC_initialize(NFC_descriptor* desc);
int NFC_poll(NFC_descriptor* desc);
int NFC_findOutWhichTag(const uint8_t *pbtData, const size_t szBytes);
void NFC_end(NFC_descriptor* desc);
void NFC_queueUp(int tagNum);
void NFC_runCommand(char* command);

#endif
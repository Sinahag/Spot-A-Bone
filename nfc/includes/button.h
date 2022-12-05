#ifndef BUTTON_H_
#define BUTTON_H_
// Needed for exit() and etc.
#include <stdlib.h>

// Paths of button characteristics that need to be set
#define BUTTON_pathValue "/sys/class/gpio/gpio72/value"
#define BUTTON_pathactiveLow "/sys/class/gpio/gpio72/active_low"
#define BUTTON_pathDirection "/sys/class/gpio/gpio72/direction"

static const int MAX_LENGTH = 1024;

void button_initiate();
// Will write the string toWrite into the file designated in fileName
void writeToFile(char *fileName, char *toWrite);

// Will return the integer form of the reading from fileName
int readButton(char *fileName);

void button_runCommand(char *command);

#endif
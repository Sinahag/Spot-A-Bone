CC_C = arm-linux-gnueabihf-gcc
CFLAGS = -Wall -g -std=c99 -D _POSIX_C_SOURCE=200809L -Werror
OUTDIR = $(HOME)/cmpt433/public/myApps
SOURCES = main.c nfcReader.c myThreads.c button.c
TARGET = main

all: clean main

# nfcReader: nfcReader.o nfc-utils.o
# 	$(CC_C) $(CFLAGS) -o nfcReader nfcReader.o nfc-utils.o -lm -lnfc

main:
	$(CC_C) $(CFLAGS) $(SOURCES) -o $(OUTDIR)/$(TARGET) -lpthread -lnfc

# nfc-utils.o:
# 	$(CC_C) $(CFLAGS) -c utils/nfc-utils.c

# nfcReader.o:
# 	$(CC_C) $(CFLAGS) -c nfcReader.c

# deploy:
# 	cp nfcReader $(HOME)/cmpt433/public/myApps/

clean:
	rm -rf nfcReader *.o *~

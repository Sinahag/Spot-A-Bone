#include "includes/myThreads.h"

void *threadNFC(void *arg){
    NFC_descriptor *descPtr = (NFC_descriptor *) arg;
    int tagNum = 0, prevTagNum = 0;
    NFC_initialize(descPtr);
    while(1){
        if ((tagNum = NFC_poll(descPtr)) != prevTagNum && tagNum != 0){
            printf("Found tag #%d\n", tagNum);
            if (tagNum != 0)
                prevTagNum = tagNum;
            NFC_queueUp(tagNum);
        }
    }
    return NULL;
}
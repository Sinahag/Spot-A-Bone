import pipes
import time
import threading

# this implementation only recognizes only the input to NFC.txt
class nfc_pipe:
    def __init__(self,):
        print ("Creating pipe and thread...")
        self.p = pipes.Template()
        self.nfctags = "spotabone/NFC.txt"
        self.read_tags = list()
        self.read_tags_mutex = True # set true if you can read from tag, false if we're emptying buffer
        self.x = threading.Thread(target=self.readNFC, args=(0.5,))
        self.event = threading.Event()
        self.x.start()

    def readNFC(self,delay):
        while(1):
            time.sleep(delay)
            f = self.p.open(self.nfctags,'r')

            try:
                algo = f.read()
                if (algo):
                    print (f"Tag #{algo} found!\n")
            finally:
                f.close()
            open("NFC.txt", "w").close()

            while (not self.read_tags_mutex):
                time.sleep(delay)

            if (algo):
                self.read_tags.append(algo)

            if self.event.is_set():
                break

    def get_and_clear_readtags(self):
        self.read_tags_mutex=False

        to_return = self.read_tags
        self.read_tags=list()

        self.read_tags_mutex=True

        return to_return

    def close_pipe(self):
        self.x.join()

    def stop_thread(self):
        self.event.set()

    
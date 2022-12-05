import pipes
import time
import threading
# possible improvement is to get all the keys from the database at the beginning
# and store them in dictionaries in here just so if we add more playlists etc, its fine

class nfc_pipe:
    def __init__(self):
        self.commands = ['skip','track','pause','play','close']
        self.users = ['sina','justin','avash','raymond']
        self.playlists = ['p1','p2','p3','p4','p5','p6','p7','p8','p9','p10']
        self.songs = ['s1','s2','s3','s4','s5','s6','s7','s8','s9','s10']

        print ("Creating pipe and thread...")
        self.p = pipes.Template()
        self.nfctags = "spotabone/NFC.txt"
        
        self.songQueue = list()
        self.playlistQueue = list()
        self.commandQueue = list()
        self.userQueue = list()
        self.searchSongQueue =  list()

        self.read_tags_mutex = True # set true if you can read from tag, false if we're emptying buffer
        self.x = threading.Thread(target=self.readNFC, args=(0.5,))
        self.event = threading.Event()
        self.x.start()

    def readNFC(self,delay):
        while(1):
            f = self.p.open(self.nfctags,'r')
            try:
                algo = f.readline()
                while(algo):
                    if(algo):
                        algo = str(algo.strip())
                        print (f"Tag {algo} found!\n")
                        if (algo in self.commands):
                            self.commandQueue.append(algo)
                        elif (algo in self.users):
                            self.userQueue.append(algo)
                        elif (algo in self.playlists):
                            algo = list(algo)
                            algo = algo[1] # gets the playlist number
                            self.playlistQueue.append(algo)
                        elif (algo in self.songs):
                            algo = list(algo)
                            algo = algo[1] # gets the song number
                            self.songQueue.append(algo)
                        else:
                            self.searchSongQueue.append(algo)
                    algo = f.readline()
            finally:
                f.close()
            open("spotabone/NFC.txt", "w").close()
            while(not self.read_tags_mutex):
                time.sleep(delay)

            if self.event.is_set():
                break

    def get_and_clear_commandBuffer(self):
        if self.commandQueue:
            return self.commandQueue.pop(0)

        return None

    def get_and_clear_userBuffer(self):
        if self.userQueue:
            return self.userQueue.pop(0)

        return None

    def get_and_clear_playlistBuffer(self):
        if self.playlistQueue:
            return self.playlistQueue.pop(0)

        return None

    def get_and_clear_songBuffer(self):
        if self.songQueue:
            return self.songQueue.pop(0)

        return None

    def get_and_clear_searchSongBuffer(self):
        if self.searchSongQueue:
            return self.searchSongQueue.pop(0)

        return None

    def close_pipe(self):
        self.x.join()

    def stop_thread(self):
        self.event.set()
    

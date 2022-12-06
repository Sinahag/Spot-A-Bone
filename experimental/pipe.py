import pipes
import time
import threading
from connect_db import database
import getpass
# possible improvement is to get all the keys from the database at the beginning
# and store them in dictionaries in here just so if we add more playlists etc, its fine

class nfc_pipe:
    def __init__(self):
        print ("Creating pipe and thread...")

        db = database(None)
        self.commands = ['skip','track','pause','play','close']
        self.users =db.get_users()
        self.playlists = db.get_playlists()
        self.songs = db.get_songs()
        db.cleanup()

        self.p = pipes.Template()
        username = getpass.getuser()        
        username = "/home/"+username
        self.nfctags = username+ "/cmpt433/public/myApps/spotabone/comms/NFC.txt"
        self.songNames = username+"/cmpt433/public/myApps/spotabone/comms/song.txt"

        self.songQueue = list()
        self.playlistQueue = list()
        self.commandQueue = list()
        self.userQueue = list()
        self.searchSongQueue =  list()

        self.read_tags_mutex = True # set true if you can read from tag, false if we're emptying buffer
        self.nfcThread = threading.Thread(target=self.readNFC, args=(0.5,))
        self.event = threading.Event()
        self.nfcThread.start()

    def getSongDirectory(self):
        return self.songNames

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
            open(self.nfctags, "w").close()
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
        self.nfcThread.join()

    def stop_thread(self):
        self.event.set()
    

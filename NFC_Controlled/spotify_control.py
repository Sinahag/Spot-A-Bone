import spotipy
from connect_db import database
import time
from pprint import pprint
import sys

class control:
    def __init__(self,username):
        self.db = database(username)
        token = self.db.get_token()
        self.sp = spotipy.Spotify(auth=token)
        self.username = username
        #self.current_user = self.get_current_user()
        self.current_playback = self.get_current_playback()
        self.deviceID = str()

    def get_song_uri(self, song_name):
        results = self.sp.search(song_name, 1, 0, "track")
        song_items = results['tracks']['items']
        song_name = song_items[0]['name']
        song_artist = song_items[0]['artists'][0]['name']
        song_id = song_items[0]['id']
        song_uri = song_items[0]['uri']
        return [song_uri,song_id,song_name,song_artist]

    def change_user(self,username):
        self.db = database(username)
        token = self.db.get_token()
        self.username=username
        self.sp = spotipy.Spotify(auth=token)
        #self.current_user = self.get_current_user()
        self.current_playback = self.get_current_playback()
        self.deviceID = str()

    def get_current_user(self):
        return self.username

    def get_current_playback(self):
        return self.sp.current_playback()

    def start_playback(self, uris:list()):
        try:
            self.sp.start_playback(uris=uris)
        except:
            print("No active device!")
            return;
        time.sleep(0.5)
        control.print_playback()
        self.deviceID = self.get_current_playback()['device']['id']

    def print_playback(self):
        print(f"Playing {self.sp.current_playback()['item']['name']} by {self.sp.current_playback()['item']['artists'][0]['name']} on {self.username} {self.sp.current_playback()['device']['name']}")

    def print_queued(self,song_name, song_artist):
        print(f"Queued {song_name} by {song_artist} on {self.username} {self.sp.current_playback()['device']['name']}")

    def play_NFC_piped(self):
        uris=self.pipe.get_and_clear_readtags()
        if len(uris) > 0:
            self.sp.start_playback(uris=uris)

    def play_song_by_number(self, songNum):
        uri = self.db.get_tag_uri(songNum)
        if uri:
            try:
                self.sp.start_playback(uris=[uri])
            except:
                print("No Active Device")
                

    def shuffle_playlist_by_id(self,playlistNum):
        playlistID = self.db.get_playlist_id(playlistNum)
        try:
            self.sp.user_playlist_tracks(playlist_id=playlistID)
        except:
            print("Current User doesn't have this playlist")
            return;
        results = self.sp.user_playlist_tracks(playlist_id=playlistID)
        uris=list()
        for track in results['tracks']['items']:
            uris.append(track['track']['uri'])
        if (len(uris)==0):
            print(f"Couldn't find playlist, please add it to your profile")
        else:
            try:
                self.sp.start_playback(uris=uris)
            except:
                print("No active device!")
                return;
            self.sp.shuffle(True)       
            print(f"Now Shuffling")
        self.deviceID = self.get_current_playback()['device']['id']
        time.sleep(0.5)
        self.print_playback()


    def shuffle_playlist(self,requested_playlist):
        results = self.sp.current_user_playlists()
        uris=list()
        for i in results['items']:
            if(i['name']==requested_playlist):
                for track in self.sp.playlist_tracks(i['id'])['items']:
                    uris.append(track['track']['uri'])
                try:
                    self.sp.start_playback(uris=uris)
                except:
                    print("No active device!")
                    return;
                self.sp.shuffle(True)
                break
        if (len(uris)==0):
            print(f"Couldn't find {requested_playlist}, please add it to your profile")
        else:
            print(f"Now Shuffling {requested_playlist}")

    def playback_handler(self, command):
        if(command == "skip"):
            try:
                self.sp.next_track()
            except:
                print("Nothing Next")
                return
            print("Skipping...")
            self.print_playback()
        elif(command == "track"):
            try:
                self.sp.previous_track()
            except:
                print("No Previous Track")
                return
            print("Tracking...")
            self.print_playback()
        elif(command == "play"):
            try:
                self.sp.start_playback(device_id = self.deviceID)
            except:
                print("No active device to play")
                return
            self.print_playback()

        elif(command == "pause"):
            try:
                self.deviceID = self.get_current_playback()['device']['id']
                self.sp.pause_playback()
            except:
                print("Cannot pause, nothing playing")
                return
            print("Paused")
        elif(command == 'close'):
            self.cleanup()
            sys.exit()

    # song info is a list of value: [song_uri,song_id,song_artist,song_name]
    def play_or_queue(self, PorQ, song_info):
        if PorQ=="1":
            try:
                self.sp.start_playback(uris = [song_info[0]])
            except:
                print("No active device!")
                return;
            time.sleep(0.5)
            self.print_playback()
        else:
            self.sp.add_to_queue(song_info[1],song_info[3])
            time.sleep(0.5)
            self.print_queued(song_info[3],song_info[2])

    def cleanup(self):
        print("Closing Database...")
        self.db.cleanup()

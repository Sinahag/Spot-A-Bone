import spotipy
from connect_db import database
from nfc_pipe import nfc_pipe
import time

class control:
    def __init__(self,username):
        self.db = database(username)
        token = self.db.get_token()
        self.sp = spotipy.Spotify(auth=token)
        self.pipe = nfc_pipe()
        self.current_user = self.get_current_user()
        self.current_playback = self.get_current_playback()

    def get_song_uri(self, song_name):
        results = self.sp.search(song_name, 1, 0, "track")
        song_items = results['tracks']['items']
        song_name = song_items[0]['name']
        song_artist = song_items[0]['artists'][0]['name']
        song_id = song_items[0]['id']
        song_uri = song_items[0]['uri']
        return [song_uri,song_id,song_name,song_artist]
    
    def get_current_user(self):
        return self.sp.current_user()['id']

    def get_current_playback(self):
        return self.sp.current_playback()

    def start_playback(self, uris:list()):
        self.sp.start_playback(uris=uris)

    def print_playback(self):
        print(f"Playing {self.sp.current_playback()['item']['name']} by {self.sp.current_playback()['item']['artists'][0]['name']} on {self.sp.current_user()['id']} {self.sp.current_playback()['device']['name']}")

    def print_queued(self,song_name, song_artist):
        print(f"Queued {song_name} by {song_artist} on {self.sp.current_user()['id']} {self.sp.current_playback()['device']['name']}")

    def play_from_NFC(self):
        uris=list()
        with open('spotabone/NFC.txt') as f:
            for line in f:
                uris.append(self.db.get_tag_uri(str(line.strip())))
        if len(uris) > 0:
            self.sp.start_playback(uris=uris)
        open("NFC.txt", "w").close()

    def play_NFC_piped(self):
        uris=self.pipe.get_and_clear_readtags()
        if len(uris) > 0:
            self.sp.start_playback(uris=uris)

    def shuffle_playlist(self,requested_playlist):
        results = self.sp.current_user_playlists()
        uris=list()
        for i in results['items']:
            if(i['name']==requested_playlist):
                for track in self.sp.playlist_tracks(i['id'])['items']:
                    uris.append(track['track']['uri'])
                self.sp.start_playback(uris=uris)
                self.sp.shuffle(True)
                break
        if (len(uris)==0):
            print(f"Couldn't find {requested_playlist}, please add it to your profile")
        else:
            print(f"Now Shuffling {requested_playlist}")

    # song info is a list of value: [song_uri,song_id,song_artist,song_name]
    def play_or_queue(self, PorQ, song_info):
        if PorQ=="1":
            self.sp.start_playback(uris = [song_info[0]])
            time.sleep(0.5)
            self.print_playback()
        else:
            self.sp.add_to_queue(song_info[1],song_info[3])
            time.sleep(0.5)
            self.print_queued(song_info[3],song_info[2])

    def cleanup(self):
        print("Closing Database...")
        self.db.cleanup()

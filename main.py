import webbrowser
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import spotipy.util as util

from pprint import pprint
import sys
scope = 'user-library-read user-library-modify user-read-private playlist-modify-public user-modify-playback-state user-read-playback-state user-read-currently-playing'
username = 'justinmateo'

# client_credentials_manager = SpotifyClientCredentials()
# sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

token = util.prompt_for_user_token(username, scope)

if token:
    sp = spotipy.Spotify(auth=token)

# if sys.argv[1]:
#     results = sp.search(sys.argv[1], limit=1)

print(f"Current User: {sp.current_user()['id']}")
# sp.start_playback()

print(f"Currently Playing: {sp.current_playback()['item']['album']['name']}");

while True:
    print("Welcome to the project, " + sp.current_user()['display_name'])
    print("0 - Exit the console")
    print("1 - Search for a Song")
    user_input = int(input("Enter Your Choice: "))
    if user_input == 1:
        search_song = input("Enter the song name: ")
        results = sp.search(search_song, 1, 0, "track")
        songs_dict = results['tracks']
        song_items = songs_dict['items']
        song_name = song_items[0]['name']
        song_artist = song_items[0]['artists'][0]['name']
        song_id = song_items[0]['id']
        song_uri = song_items[0]['uri']
        # sp.add_to_queue(song_id)
        uris = list()
        uris.append(song_uri)
        sp.start_playback(uris=uris)
        # sp.add_to_queue(song_id) # if you want to add
        print(f"Playing {song_name} by {song_artist} on {sp.current_user()['id']} {sp.current_playback()['device']['name']}")
    elif user_input == 0:
        print("Good Bye, Have a great day!")
        break
    else:
        print("Please enter valid user-input.")

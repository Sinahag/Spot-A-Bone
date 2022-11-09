import webbrowser
import spotipy
import spotipy.util as util
from NFCTAGURIMAPPING import getURI
from userinfo import device_id, username

from pprint import pprint
import sys

scope = 'user-top-read user-library-read user-library-modify user-read-private playlist-modify-public user-modify-playback-state user-read-playback-state user-read-currently-playing'

token = util.prompt_for_user_token(username, scope)

if token:
    sp = spotipy.Spotify(auth=token)

if (sp.current_user()):
    print(f"Current User: {sp.current_user()['id']}")
    # sp.transfer_playback(device_id=device_id, force_play=True) # tries playing on iphone if it's available
else:
    print("Need an active session")
    sys.exit()

print(f"Currently Playing: {sp.current_playback()['item']['name']}")

while True:
    print("SPOT-A-BONE running on:" + sp.current_user()['display_name'])
    print("0 - Exit")
    print("1 - Search for a Song")
    print("2 - Read From NFC")
    choice = int(input("choice: "))
    if choice == 1:
        search_song = input("Enter the song name: ")
        results = sp.search(search_song, 1, 0, "track")
        song_items = results['tracks']['items']
        song_name = song_items[0]['name']
        song_artist = song_items[0]['artists'][0]['name']
        song_id = song_items[0]['id']
        song_uri = song_items[0]['uri']
        play_or_queue = str(input("Play Now (1) or Queue (any other key): "))
        if play_or_queue=="1":
            sp.start_playback(uris=[song_uri])
            print(f"Playing {song_name} by {song_artist} on {sp.current_user()['id']} {sp.current_playback()['device']['name']}")
        else:
            sp.add_to_queue(song_id)
            print(f"Queued {song_name} by {song_artist} on {sp.current_user()['id']} {sp.current_playback()['device']['name']}")
    elif choice == 2:
        uris=list()
        with open('NFC.txt') as f:
            for line in f:
                uris.append(getURI(str(line.strip())))
        if len(uris) > 0:
            sp.start_playback(uris=uris)
        open("NFC.txt", "w").close()
        print(f"""Playing {sp.current_playback()['item']['name']} by {sp.current_playback()['item']['artists'][0]['name']} on {sp.current_user()['id']} {sp.current_playback()['device']['name']}""")
    elif choice == 0:
        break
    else:
        print("Invalid Input")

import webbrowser
from spotify_control import control
import sys

username = str(input("Please enter your username: "))
control = control(username)

if (control.get_current_user()):
    print(f"Current User: {control.get_current_user()}")
    # sp.transfer_playback(device_id=device_id, force_play=True) # tries playing on iphone if it's available
else:
    print("Unauthorized user")
    sys.exit()

if control.get_current_playback():
    print(f"Currently Playing: {control.get_current_playback()['item']['name']}")
else:
    print("Need to have an active device")
    control.cleanup()
    sys.exit()

while True:
    print("SPOT-A-BONE running on: " + control.get_current_playback()['device']['name'])
    print("0 - Exit")
    print("1 - Search for a Song")
    print("2 - Read From NFC")
    print("3 - Get User Playlist's")
    print("4 - Read From NFC Pipe")
    choice = int(input("choice: "))
    if choice == 1:
        search_song = input("Enter the song name: ")
        song_info = control.get_song_uri(search_song)
        play_or_queue = str(input("Play Now (1) or Queue (any other key): "))
        control.play_or_queue(play_or_queue,song_info)
    elif choice == 2:
        control.play_from_NFC()
        control.print_playback()
    elif choice == 3:
        requested_playlist = str(input("Playlist: "))
        control.shuffle_playlist(requested_playlist)
    elif choice == 4:
        control.play_NFC_piped()
        control.print_playback()
    elif choice == 0:
        control.cleanup()
        print("Thank you for using Spot-A-Bone!")
        break
    else:
        print("Invalid Input")

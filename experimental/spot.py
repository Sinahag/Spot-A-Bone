import sys
sys.dont_write_bytecode=True # stops creating pycache file
# the pycache would disrupt the change user functionality
import webbrowser
from spotify_control import control
from pipe import nfc_pipe
import time


def wait():
    while(isServicingRequest):
        time.wait(0.1)

pipe = nfc_pipe()
songFileDirectory = pipe.getSongDirectory()
isServicingRequest=False
control = control("sina",songFileDirectory)

print("Please Scan User to Begin")

while(1): 
    username = pipe.get_and_clear_userBuffer()
    if username:
        control.change_user(username)
        break

if (control.get_current_user()):
    print(f"Current User: {control.get_current_user()}")
else:
    print("Unauthorized user")
    sys.exit()

while(1):
    wait()
    username = pipe.get_and_clear_userBuffer()
    if username:
        isServicingRequest=True
        control.change_user(username)
        isServicingRequest=False
        print(f"Successfully Changed User to {control.get_current_user()}")
    wait()
    song = pipe.get_and_clear_songBuffer()
    if song:
        isServicingRequest=True
        control.play_song_by_number(song)
        isServicingRequest=False
    wait()
    playlist = pipe.get_and_clear_playlistBuffer()
    if playlist:
        isServicingRequest=True
        control.shuffle_playlist_by_id(playlist)
        isServicingRequest=False
    wait()
    command = pipe.get_and_clear_commandBuffer()
    if command:
        isServicingRequest=True
        if command == 'close':
            pipe.stop_thread()
            print("Closing Pipe...")
            pipe.close_pipe()
            time.sleep(3)
            print("Thanks for using spot-a-bone")
        control.playback_handler(command)
        isServicingRequest=False
    wait()
    search_song = pipe.get_and_clear_searchSongBuffer()
    if search_song:
        isServicingRequest=True
        song_info = control.get_song_uri(search_song)
        control.play_or_queue('1',song_info)
        isServicingRequest=False

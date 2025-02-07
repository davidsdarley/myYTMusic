'''
Client Goals:

    1. Play music
        - recieve info from server and play it

    2. Send messages to Server
        POST messages:
        - add songs

        PUT messages:
        - Skip
        - go back
        - pause/play

        DELETE messages:
        - remove song

        GET messages:
        - see list

    3. Keep minimal amount of data here
        - Current song
'''

import requests
import vlc
from pynput import keyboard
import threading

SERVER_URL = "http://127.0.0.1:5000"
BOOMBOX = None
STATE = True


def press(key):
    pass
def release(key):
    global STATE
    """Called when a key is released"""
    if key == keyboard.Key.right:
        # If the right arrow key is released, call the skip function
        STATE = skip()
def skip():
    global BOOMBOX
    if BOOMBOX != None:
        BOOMBOX.stop()
        BOOMBOX = None
        print("Skipped!")
        return False
    return True

def controls():
    """Listen for keyboard events in a separate thread"""
    with keyboard.Listener(on_press = press, on_release = release) as listener:
        listener.join()

# Start the listener in a separate thread
keyboardControls = threading.Thread(target = controls)
keyboardControls.daemon = True  # Makes the thread exit when the main program exits. VERY IMPORTANT
keyboardControls.start()
def getPlaylist():
    response = requests.get("http://127.0.0.1:5000/playlist")
    if response.status_code == 200:
        playlist = response.json()
        print(playlist)
    else:
        print(f"Error: {response.status_code}")

def getNextSong():
    response = requests.get("http://127.0.0.1:5000/next")
    if response.status_code == 200:
        song = response.json()
        return song

def playAudio(url):
    global BOOMBOX, STATE
    print(url)
    #download the audio, then play it
    BOOMBOX = vlc.MediaPlayer(url)  # make an audioplayer object
    BOOMBOX.play()                  # start the tunes
    while True:
        if BOOMBOX.get_state() in [vlc.State.Ended, vlc.State.Stopped]:
            return
        elif STATE == False:
            return



def controls():
    #skip
    pass


def main():
    global STATE
    while True:
        STATE = True
        songinfo = getNextSong()
        if not songinfo:
            print("No more songs")
            break
        print(songinfo[0])
        playAudio(songinfo[1])
        print("DEBUG")


if __name__ == '__main__':
    main()
    pass

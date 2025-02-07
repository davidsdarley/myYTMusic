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
import time
import yt_dlp
import os

SERVER_URL = "http://127.0.0.1:5000"

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
    print(url)
    #download the audio, then play it
    boombox = vlc.MediaPlayer(url)  # make an audioplayer object
    boombox.play()                  # start the tunes
    state = boombox.get_state()
    print()
    while state not in [vlc.State.Ended, vlc.State.Stopped]:
        state = boombox.get_state()

def controls():
    pass


def main():
    running = True
    while running == True:
        songinfo = getNextSong()
        if not songinfo:
            print("No more songs")
            break
        print(songinfo[0])
        playAudio(songinfo[1])


if __name__ == '__main__':
    main()
    pass

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
from pytube import YouTube

SERVER_URL = "http://127.0.0.1:5000"

def getPlaylist():
    response = requests.get("http://127.0.0.1:5000/playlist")
    if response.status_code == 200:
        playlist = response.json()
        print(playlist)
    else:
        print(f"Error: {response.status_code}")

def getNextSong():
    response = requests.get("http://127.0.0.1:5000/next")   #response holds a dictionary. The
    if response.status_code == 200:
        url = response.json()
        return url


def playAudio(filename):
    #download the audio, then play it
    pass

def main():
    running = True
    while running == True:
        songUrl = getNextSong()
        if not songUrl:
            print("No more songs")
            break
        print(songUrl)



if __name__ == '__main__':
    main()
    pass

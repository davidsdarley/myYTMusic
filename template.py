import requests
import vlc
import time
from pytube import YouTube

SERVER_URL = "http://127.0.0.1:5000"

def get_next_song():
    """Ask the server for the next YouTube song URL"""
    response = requests.get(f"{SERVER_URL}/next")
    if response.status_code == 200:
        return response.json()["url"]
    else:
        print("Error fetching next song")
        return None

def download_audio(youtube_url):
    """Download the YouTube audio stream and return the file path"""
    yt = YouTube(youtube_url)
    stream = yt.streams.filter(only_audio=True).first()
    file_path = stream.download(filename="current_song.mp4")  # Save as MP4
    return file_path

def play_audio(file_path):
    """Play the downloaded audio file using VLC"""
    player = vlc.MediaPlayer(file_path)
    player.play()

    # Wait until the song finishes playing
    while player.get_state() not in [vlc.State.Ended, vlc.State.Stopped]:
        time.sleep(1)

def main():
    while True:
        song_url = get_next_song()
        if not song_url:
            print("No more songs in the playlist.")
            break

        print(f"Playing: {song_url}")
        audio_file = download_audio(song_url)
        play_audio(audio_file)

if __name__ == "__main__":
    main()
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



CODE FROM GAMES THAT MIGHT BE HELPFUL

pygame.display.set_mode((1296, 750))


running = True
    while running == True:
        screen.fill((0, 0, 0))
        mouseUp = (None, None)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #close the game when X is clicked
                running = False
            if event.type == pygame.MOUSEBUTTONUP: #click, return mouse position
                mouseUp = pygame.mouse.get_pos()
                game.click(mouseUp)
'''

import requests
import vlc
import pygame

class MusicApp:

    def __init__(self, url = "http://127.0.0.1:5000"):
        self.SERVER_URL = url
        self.boombox = None
        self.state = True


    def press(self, key):
        pass
    def release(self, key):
        """Called when a key is released"""
        if key == "rarrow":
            # If the right arrow key is released, call the skip function
            self.state = self.skip()
        elif key == "larrow":
            pass
    def skip(self):
        global BOOMBOX
        if self.boombox != None:
            self.boombox.stop()
            BOOMBOX = None
            print("Skipped!")
            return False
        return True

    def controls(self):
        pass
        #call the appropriate method for the appropriate event





    def getPlaylist(self):
        response = requests.get("http://127.0.0.1:5000/playlist")
        if response.status_code == 200:
            playlist = response.json()
            print(playlist)
        else:
            print(f"Error: {response.status_code}")

    def getNextSong(self):
        response = requests.get("http://127.0.0.1:5000/next")
        if response.status_code == 200:
            song = response.json()
            return song

    def playAudio(self, url):
        print(url)
        #download the audio, then play it
        self.boombox = vlc.MediaPlayer(url)  # make an audioplayer object
        self.boombox.play()                  # start the tunes
        while (self.boombox.get_state() not in [vlc.State.Ended, vlc.State.Stopped]) and self.state:




    def controls(self):
        #skip
        pass


    def main(self):
        while True:
            self.state = True
            songinfo = self.getNextSong()
            if not songinfo:
                print("No more songs")
                break
            print(songinfo[0])
            self.playAudio(songinfo[1])
            print("DEBUG")


if __name__ == '__main__':
    app = MusicApp()
    app.main()




    pass

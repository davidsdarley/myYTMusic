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
pygame.init()
class MusicApp:

    def __init__(self, url = "http://127.0.0.1:5000"):
        self.SERVER_URL = url
        self.running = True
        self.boombox = None
        self.state = True
        self.paused = False
        #pygame interface stuff
        self.screen = pygame.display.set_mode((1296, 750))
        self.clock = pygame.time.Clock()

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

    def goBack(self):
        response = requests.get("http://127.0.0.1:5000/previous")
        if response.status_code == 200:
            self.boombox.stop()
            self.state = False
    def setPlaylist(self):
        response = requests.get("http://127.0.0.1:5000/allPlaylists")
        if response.status_code == 200:
            for playlist in response.json():
                print(playlist)
            choice = input("\nselection: ")
            while True:
                if choice in response.json():
                    response = requests.post("http://127.0.0.1:5000/selectPlaylist", json = choice)
                    if response.status_code == 201:
                        self.skip(f"Playlist {choice}:\n{response.json()}")
                        return
                elif choice == "":
                    return
                else:
                    choice = input("Invalid selection.\nselection: ")
        else:
            print("Didn't work")

    def skip(self, message = "Skipped!"):
        if self.boombox != None:
            self.boombox.stop()
            self.state = False
            print(message)
    def restart(self):
        self.boombox.stop()
        self.boombox.play()
    def playPause(self):
        if self.paused:
            self.boombox.play()
            print("resume")
            self.paused = False
        else:
            self.boombox.pause()
            print("pause")
            self.paused = True

    def controls(self):
        for event in pygame.event.get():
            if event == pygame.QUIT:  # close the game when X is clicked
                self.running = False
                self.boombox.stop()
                self.state = False
            elif event.type == pygame.KEYUP:        #right: skip    left: restart.  down: previous song     up: print playlist
                if event.key == pygame.K_RIGHT:
                    self.skip()
                elif event.key == pygame.K_SPACE:
                    self.playPause()
                elif event.key == pygame.K_LEFT:
                    self.restart()
                elif event.key == pygame.K_DOWN:
                    self.goBack()
                elif event.key == pygame.K_UP:
                    self.getPlaylist()
                elif event.key == pygame.K_q:
                    print("shutting down")
                    self.state = False
                    self.running = False
                elif event.key == pygame.K_p:
                    self.setPlaylist()
                else:
                    print(event.key)
        return

    def playAudio(self, url):
        print(url)
        #download the audio, then play it
        if self.boombox != None:
            self.boombox.release()
        self.boombox = vlc.MediaPlayer(url)  # make an audioplayer object
        self.boombox.play()                  # start the tunes
        while (self.boombox.get_state() not in [vlc.State.Ended]) and self.state:
            self.controls()

    def main(self):
        screen = pygame.display.set_mode((250, 140))                  #for later
        buttons = pygame.image.load("musicAppButtons.png")

        while self.running:
            screen.fill((0, 0, 0))
            screen.blit(buttons, (0,0))                            #also for later
            self.state = True
            songinfo = self.getNextSong()
            if not songinfo:
                print("No more songs")
                break
            print(songinfo[0])
            self.playAudio(songinfo[1])
            app.clock.tick(10)
            pygame.display.update()
        if app.boombox != None:
            app.boombox.release()




if __name__ == '__main__':
    app = MusicApp()
    app.main()




    pass

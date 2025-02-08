#PLANNING
'''
OK, what are the goals of this project?
    1. Learn servers
    2. make the server keep track of playqueue information
        - maintain list of songs to be played, and which index is the active one
        - Play the active song
            * ON THE CLIENT'S DEVICE specifically
        - When active song ends, the next song becomes the active song
        - remember previous songs played
        - capable of adding and removing songs from list
        - capable of changing order, of songs, including randomizing the order, or randomizing just the ones that haven't played yet

    3. Send data to server as needed
        - Json format, so need to get that capability ready

    4. if it recieves a request from a client, carry it out
        - Skip song
        - replay
        - add song to queue
            * end of queue or specific position
        - remove songs from queue
            * clear queue


Implementation:
    based on my understanding, since all the messages that I can send need to be in the form of JSONs, I need to
    build everything in a format that can be easily converted
        JSON data types:
            String
            Number
            Boolean
            Array
            Object      (dictionary with String keys and any other datatype values)
            Null

    All messages sent will be HTTP requests
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
        - see available songs

    Start by getting the playqueue set up. library jsonify turns dictionaries into JSONs, so use them
    as much as possible.

'''

from flask import Flask, jsonify, request
import yt_dlp


app = Flask(__name__)

musicLibrary = {
    "Never the Hero": "https://www.youtube.com/watch?v=8WSZRUEi7Eo&list=PLP-hm-yIkc9k9C2VLviglOYIH_MvGxmBU",
    "Soldier and Thief": "https://www.youtube.com/watch?v=_Gn9EsU_-eg",
    "Grace in the Glow": "https://www.youtube.com/watch?v=22l1xIrq4Do&list=PLP-hm-yIkc9k9C2VLviglOYIH_MvGxmBU&index=2",
    "Don't Forget Your Past": "https://www.youtube.com/watch?v=cCG9vm0Rv8o&list=PLP-hm-yIkc9k9C2VLviglOYIH_MvGxmBU&index=3",
    "Star Wars | EPIC SAMURAI VERSION" : "https://www.youtube.com/watch?v=V8XPbvDdIP0&list=PLP-hm-yIkc9mHXLhN7GxeEqvsh0OF_6Mr",
    "The Clones Theme | EPIC SAMURAI VERSION" : "https://www.youtube.com/watch?v=4B9mgvv82C4&list=PLP-hm-yIkc9mHXLhN7GxeEqvsh0OF_6Mr&index=2",
    "Rise to Victory" : "https://www.youtube.com/watch?v=GORfswQLHEE"
}

playlists = {
    "test" : ["Don't Forget Your Past", "Grace in the Glow","Never the Hero", "Soldier and Thief"],
    "dnd" : [],
    "Samuel Kim": ["Star Wars | EPIC SAMURAI VERSION", "The Clones Theme | EPIC SAMURAI VERSION"],
    "Clamavi de Profundis" : ["Rise to Victory"]
}


playqueue = {
    "songs": playlists["test"],
    "currentIndex": 0
}

print(playqueue)
@app.route("/playlist", methods = ["GET"])
def getPlayqueue():
    return jsonify(playqueue), 200

@app.route("/allPlaylists", methods = ["GET"])
def getPlaylists():
    lsts = list(playlists.keys())
    return jsonify(lsts), 200
@app.route("/selectPlaylist", methods = ["POST"])
def setPlaylist():
    print("Changing playlist")
    name = request.get_json()
    print(f"to {name}!")
    if name not in playlists.keys():
        return jsonify({"error": "requested playlist does not exist"}), 404
    playqueue["songs"] = playlists[name]
    playqueue["currentIndex"] = 0
    lsts = playqueue["songs"]
    print(lsts)
    return jsonify(lsts), 201

@app.route("/next", methods = ["GET"])
def nextSong():
    index = playqueue["currentIndex"]
    song = playqueue["songs"][index]
    url = getSongUrl(name = song)
    playqueue["currentIndex"] += 1
    if playqueue["currentIndex"] >= len(playqueue["songs"]):
        playqueue["currentIndex"] = 0
    print(f'Sending "{song}" now!')
    return jsonify([song, url]), 200

@app.route("/previous", methods = ["GET"])
def previous():
    print("Bring back index")
    print(playqueue["currentIndex"])
    playqueue["currentIndex"] -= 2
    return jsonify({"message": "Replaying!"}), 200

def getSongUrl(index = None, name = None):
    if index != None:
        url =  musicLibrary[playqueue["songs"][index]]
    elif name != None:
        url = musicLibrary[name]
    else:
        return "error"
    ydl_opts = {
        # I don't entirely understand what these are but the internet says that they are good default settings!
        "format": "bestaudio/best",
        "quiet": True,
        "noplaylist": True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        file = ydl.extract_info(url, download=False)  # don't download, just url
        return file["url"]

if __name__ == '__main__':
    app.run()

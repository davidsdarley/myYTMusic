#PLANNING
'''
OK, what are the goals of this project?
    1. Learn servers
    2. make the server keep track of playlist information
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

    Start by getting the playlist set up. library jsonify turns dictionaries into JSONs, so use them
    as much as possible.

'''

from flask import Flask, jsonify, request

app = Flask(__name__)

musicLibrary = {
    "Never the Hero": "https://www.youtube.com/watch?v=8WSZRUEi7Eo&list=PLP-hm-yIkc9k9C2VLviglOYIH_MvGxmBU",
    "Soldier and Thief": "https://www.youtube.com/watch?v=_Gn9EsU_-eg"
}

playlist = {
    "songs": ["Soldier and Thief", "Never the Hero"],
    "currentIndex": 0
}

@app.route("/playlist", methods = ["GET"])
def getPlaylist():
    return jsonify(playlist), 200

@app.route("/next", methods = ["GET"])
def nextSong():
    if len(playlist["songs"]) > playlist["currentIndex"]:
        song = getSongUrl(playlist["currentIndex"])
        playlist["currentIndex"] +=1
        return jsonify({"song url": song}), 200
    else:
        return jsonify({"message": "No more songs"}), 404

def getSongUrl(index = None, name = None):
    #           dict of urls  access the playlist     at active index
    if index != None:
        return musicLibrary[playlist["songs"][index]]
    elif name != None:
        return musicLibrary[name]
    else:
        return "error"



if __name__ == '__main__':
    app.run(debug=True)

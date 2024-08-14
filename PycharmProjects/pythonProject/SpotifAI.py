import os
import time
import requests
import sqlite3
import CredentialManager
import logging
import logging.handlers
import threading
from urllib.parse import urlencode
from webLord import web

dataInterval = 15

logfile = 'LOG'

"""
import sqlite3

def create_tables():
    conn = sqlite3.connect('chat.db')
    c = conn.cursor()

    # Create USERS table
    c.execute('''CREATE TABLE IF NOT EXISTS USERS (
                    id INTEGER PRIMARY KEY,
                    username TEXT NOT NULL,
                    email TEXT NOT NULL,
                    password_hash TEXT NOT NULL
                 )''')

    # Create CONVERSATIONS table
    c.execute('''CREATE TABLE IF NOT EXISTS CONVERSATIONS (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL
                 )''')

    # Create MESSAGES table
    c.execute('''CREATE TABLE IF NOT EXISTS MESSAGES (
                    id INTEGER PRIMARY KEY,
                    conversation_id INTEGER NOT NULL,
                    sender_user_id INTEGER NOT NULL,
                    content TEXT NOT NULL,
                    sent_at INTEGER NOT NULL,
                    FOREIGN KEY (conversation_id) REFERENCES CONVERSATIONS(id),
                    FOREIGN KEY (sender_user_id) REFERENCES USERS(id)
                 )''')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_tables()
"""


logger = logging.getLogger("SpotifAI")
logConsole = logging.StreamHandler()
logFile = logging.FileHandler("LOG")
systemdHandler = logging.handlers.SysLogHandler(address="/dev/log")
formatter = logging.Formatter('| %(asctime)s |0| %(levelname)s |0| %(module)s |0| %(lineno)d |0| %(message)s |')
logger.setLevel(logging.DEBUG)
logFile.setFormatter(formatter)
logConsole.setFormatter(formatter)
systemdHandler.setFormatter(formatter)

if __name__ == "__main__":
    logger.addHandler(logConsole)
    logger.addHandler(logFile)
    logger.addHandler(systemdHandler)


tokefile = 'token.txt'
my_access_token = None

# Set up the OAuth2 credentials
scopes = 'user-read-playback-state'

# Check if a token file exists. If not, prompt the user for authorization
if not os.path.exists(tokefile):
    logger.debug("Token file doesn't exist")
    my_access_token = CredentialManager.get_authorization(scopes)
    logger.debug(my_access_token)
    CredentialManager.token_to_file(my_access_token, tokefile)
else:
    # If a token file exists, verify the expiration time of the token
    my_access_token = CredentialManager.token_from_file(tokefile, 180)
    logger.debug(my_access_token)

# Set up the SQLite database
conn = sqlite3.connect('playback_data.db')
cursor = conn.cursor()

cursor.execute('PRAGMA foreign_keys = ON;')

# Create a table to store the data

cursor.execute('''
CREATE TABLE IF NOT EXISTS genre_data (
    artist TEXT PRIMARY KEY,
    genre TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS playback_data (
    timestamp INTEGER DEFAULT (strftime('%s', 'now', 'localtime')),
    is_playing INTEGER,
    track TEXT,
    album TEXT,
    artist TEXT,
    repeat_state INTEGER,
    play_progress INTEGER,
    FOREIGN KEY (artist) REFERENCES genre_data(artist)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS gpt_messages (
    id INTEGER,
    timestamp INTEGER DEFAULT (strftime('%s', 'now', 'localtime')),
    user TEXT,
    content TEXT,
    FOREIGN KEY (id) REFERENCES gpt_ids(id)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS gpt_ids (
    id INTEGER PRIMARY KEY,
    label TEXT
)
''')

conn.commit()


def ping_data():
    global my_access_token
    with sqlite3.connect('playback_data.db') as testConn:
        testCur = testConn.cursor()
        while True:
            # Get the current timestamp in unix time
            timestamp = int(time.time())

            # Set the API endpoint and headers
            playbackAPI = 'https://api.spotify.com/v1/me/player'
            artistAPI = 'https://api.spotify.com/v1/artists'

            headers = {
                'Authorization': f'Bearer {my_access_token["access_token"]}',
                'Content-Type': 'application/json'
            }
            # Make the request to the API and get the response
            response = requests.get(playbackAPI, headers=headers)
            # If the response is successful, return the data
            if not response.ok:
                logger.debug(response.json())

            if response.status_code == 200:
                playback_state = response.json()

                # Check if Spotify is currently playing
                if playback_state['is_playing'] and playback_state['currently_playing_type'] != 'episode':  # Ignore audiobooks. Maybe track them in the future?
                    # If Spotify is playing, get the details of the track that is playing
                    track = playback_state['item']['name']
                    album = playback_state['item']['album']['name']
                    artist = playback_state['item']['artists'][0]['name']
                    repeat_state = playback_state['repeat_state']
                    play_progress = playback_state['progress_ms']

                    testCur.execute('''
                    INSERT INTO playback_data (
                        timestamp,
                        is_playing,
                        track,
                        album,
                        artist,
                        repeat_state,
                        play_progress
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                    ''', (timestamp, True, track, album, artist, repeat_state, play_progress))

                    # Obtain genre data
                    genresToGet = []
                    for artist in playback_state['item']['artists']:
                        artistInDB = testCur.execute("SELECT * FROM genre_data WHERE artist = ?", (artist['name'],)).fetchone()
                        if artistInDB is None:
                            genresToGet.append(artist)
                            # testCur.execute("INSERT INTO genre_data (artist, genre) VALUES (?, ?)", (artistName, artistGenreData))
                    if len(genresToGet) == 1:
                        response = requests.get(artistAPI + f'/{artist["id"]}', headers=headers)
                        jsonData = response.json()
                        genreData = jsonData['genres'] if 'genres' in jsonData else None
                        if genreData is not None:
                            testCur.execute("INSERT INTO genre_data (artist, genre) VALUES (?, ?)", (artist['name'], ','.join(genreData)))
                    elif len(genresToGet) > 1:
                        genreData = {}
                        requestPayload = urlencode({'ids': ','.join([artist['id'] for artist in genresToGet])})
                        response = requests.get(artistAPI + f'/?{requestPayload}', headers=headers)
                        jsonData = response.json()
                        for artist in jsonData['artists']:
                            if 'genres' in artist:
                                genreData[artist['name']] = artist['genres']
                        logger.debug(genreData)
                        if len(genreData) != 0:
                            dbData = [(artistName, ','.join(genre)) for artistName, genre in genreData.items()]
                            logger.debug(dbData)
                            testCur.executemany("INSERT INTO genre_data (artist, genre) VALUES (?, ?)", dbData)


                    testConn.commit()
                    # Save the playback state data to the database
                    #save_data(timestamp, 1, track, album, artist, repeat_state, play_progress, genreData)
                else:
                    # If Spotify is not playing, save a record with empty values
                    pass
                    #save_data(timestamp, 0, '', '', '', 0, 0)
            elif response.status_code == 204:
                pass
                #save_data(timestamp, 0, '', '', '', 0, 0)
            else:
                logger.debug(playback_state)

            time.sleep(dataInterval)
            my_access_token = CredentialManager.token_from_file(tokefile, 180)
            logger.info('Datapulse')


if __name__ == "__main__":
    dataPulse = threading.Thread(target=ping_data)
    dataPulse.daemon = True
    dataPulse.start()
    web.run(host='127.0.0.1', port=10188)

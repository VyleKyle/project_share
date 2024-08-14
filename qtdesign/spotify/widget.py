# This Python file uses the following encoding: utf-8

#  UI IMPORTS

import sys
from PySide6.QtWidgets import QApplication, QDialog, QMainWindow
from PySide6.QtCore import QTimer, Signal, QStringListModel
from mainWindow import Ui_MainWindow
from newTagPop import Ui_Dialog as Ui_newTagDialog
from modifyTagsPop import Ui_Dialog as Ui_modifyTagsPop

#  LOGIC/MISC IMPORTS

import sqlite3
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
import credentials
import logging
import atexit
from collections import Counter
import json


logging.basicConfig(
    level=logging.INFO,  # Log messages of level INFO and above
    format='%(name)s |-| %(funcName)s |-| %(levelname)s |-| %(lineno)d |-| %(message)s',  # Log message format
    handlers=[
        logging.StreamHandler(),  # Console output
        logging.FileHandler("app.log")  # Write to app.log file
    ]
)


logger = logging.getLogger(__name__)


sp = Spotify(auth_manager=SpotifyOAuth(
    client_id=credentials.spotifyID,
    client_secret=credentials.spotifySecret,
    redirect_uri=credentials.spotifyRedir,
    scope="user-library-read app-remote-control user-modify-playback-state playlist-modify-private playlist-read-private"  # Add other scopes as needed
))


dbcon = sqlite3.connect('spotify_tracks.db')
dbcurs = dbcon.cursor()

atexit.register(dbcon.close)


class NewTagPopup(QDialog):

    dataEntered = Signal()

    def __init__(self, parent=None):
        super(NewTagPopup, self).__init__(parent)
        self.ui = Ui_newTagDialog()
        self.ui.setupUi(self)

        self.ui.lineEdit.returnPressed.connect(self.ui.applyTag.click)

        self.ui.applyTag.clicked.connect(self.insert_tag_to_db)
        self.ui.cancelButton.clicked.connect(self.reject)

    def insert_tag_to_db(self):
        text = self.ui.lineEdit.text()
        if not len(text) >= 3:
            logger.error("Tag too short!")
        else:
            playlist = sp.user_playlist_create(sp.me()['id'], f"{text}", public=False, description=f"{text} playlist")
            try:
                dbcurs.execute("INSERT INTO genres (name, spotify_playlist_id) VALUES (?, ?)", (text, playlist['id']))

                dbcon.commit()

                self.dataEntered.emit()
                self.close()
            except sqlite3.IntegrityError as e:
                if "UNIQUE" in e.__str__():
                    logger.error(f"Entry ('{text}') already exists in the database!")
                else:
                    raise(e)



class Widget(QMainWindow):
    def __init__(self):
        super(Widget, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        #  Make connections here
        #  self.ui.{ITEM}.{CONNECTION_LOGIC}
        #  IGNORE HIERARCHY, REFERENCE DIRECTLY

        #  Menu bar actions
        self.ui.actionUpdate_DB_Spot.triggered.connect(self.liked_to_db)
        self.ui.actionRefresh_Lists.triggered.connect(self.populate_unlabelled_list)


        #  Buttons
        self.ui.selectButton.clicked.connect(self.play_track)
        self.ui.randomButton.clicked.connect(self.play_random)
        #self.ui.applyTagsToSelectedButton.clicked.connect() TODO
        self.ui.applyTagsToPlayingButton.clicked.connect(self.applyToPlaying)
        self.ui.removeTagsButton.clicked.connect(self.remove_tags)
        self.ui.newTagButton.clicked.connect(self.open_new_tag_window)

        #  MAKE LOGIC HERE

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_playing)
        self.timer.start(2500)

        self.model = QStringListModel()
        self.ui.gridListView.setModel(self.model)

        self.updateGenres()

        # Pop-ups
        self.removeTags = None
        self.newTagWindow = None

        self.populate_unlabelled_list()
        self.update_playing()

    def liked_to_db(self):
        songs = fetch_liked_songs_spotipy()
        save_songs_to_db(songs)

    def populate_unlabelled_list(self):
        logging.info("Populating unlabelled song list")

        #conn = sqlite3.connect('spotify_tracks.db')
        #cursor = conn.cursor()

        dbcurs.execute("SELECT * FROM tracks WHERE labelled=0")
        tracks = dbcurs.fetchall()
        #conn.close()
        for track in tracks:
            self.ui.listWidget.addItem(f"{track[1]} || {track[2]}")

    def play_random(self):

        #conn = sqlite3.connect('spotify_tracks.db')
        #cursor = conn.cursor()

        dbcurs.execute("SELECT * FROM tracks WHERE labelled=0 ORDER BY RANDOM() LIMIT 1")
        tracks = dbcurs.fetchone()
        #conn.close()

        sp.start_playback(uris=[f"spotify:track:{tracks[0]}"])
        logger.info(f"Selected random song for play ({tracks[1]})")

    def play_track(self):
        logger.info("Selected song")
        selected = self.ui.listWidget.currentItem()
        if selected is None:
            logger.error("No track selected")
            return
        item_text = selected.text()
        title, artist = item_text.split(" || ")

        #conn = sqlite3.connect('spotify_tracks.db')
        #cursor = conn.cursor()

        dbcurs.execute("SELECT * FROM tracks WHERE artist=? AND name=? AND labelled=0", (artist, title))
        tracks = dbcurs.fetchall()
        if len(tracks) > 1:
            logger.critical("More than one track returned")
            return
        elif len(tracks) == 0:
            logger.error("...?")
        #conn.close()

        sp.start_playback(uris=[f"spotify:track:{tracks[0][0]}"])


    def remove_tags(self):
        model = self.ui.gridListView.model()
        selected_indexes = self.ui.gridListView.selectionModel().selectedIndexes()
        selected_texts = [model.data(index) for index in selected_indexes]

        for selection in selected_texts:

            dbcurs.execute("SELECT spotify_playlist_id FROM genres WHERE name = ?", (selection,))
            playlist_id = dbcurs.fetchone()

            dbcurs.execute("""
                DELETE FROM track_genres 
                WHERE genre_id = (SELECT genre_id FROM genres WHERE name = ?)
            """, (selection,))

            dbcurs.execute("DELETE FROM genres WHERE name=?", (selection,))

            sp.current_user_unfollow_playlist(playlist_id)

        dbcon.commit()
        self.updateGenres()


    def update_playing(self):
        playback = sp.current_playback()
        if playback and playback["item"]:
            if playback["item"]["type"] == "track":
                track_name = playback["item"]["name"]
                artist_name = playback["item"]["artists"][0]["name"]
                self.ui.label.setText(f"Now Playing: {track_name} by {artist_name}")
            elif playback["item"]["type"] == "episode":
                self.ui.label.setText("Now Playing: An audiobook")
            else:
                self.ui.label.setText("Now Playing: ???")
        else:
            self.ui.label.setText("Now Playing: Nothing.")


    def updateGenres(self):
        logger.info("Loading tag pool")
        dbcurs.execute("SELECT * FROM genres")
        data = dbcurs.fetchall()
        self.model.setStringList([x[1] for x in data])
    
    def open_new_tag_window(self):
        if self.newTagWindow is None:
            self.newTagWindow = NewTagPopup(self)
            self.newTagWindow.dataEntered.connect(self.updateGenres)
            self.newTagWindow.show()
        elif self.newTagWindow.isVisible() is False:
            self.newTagWindow.show()

    def applyToSelection(self):
        pass

    def applyToPlaying(self):
        playback = sp.current_playback()
        if playback and playback["item"]:
            if playback["item"]["type"] == "track":
                track_id = playback["item"]["id"]
                track_name = playback['item']['name']

                model = self.ui.gridListView.model()
                selected_indexes = self.ui.gridListView.selectionModel().selectedIndexes()
                selected_genres = [model.data(index) for index in selected_indexes]

                for selection in selected_genres:
                    try:

                        dbcurs.execute("SELECT genre_id, spotify_playlist_id FROM genres WHERE name = ?", (selection,))
                        genre_id, playlist_id = dbcurs.fetchone()

                        sp.playlist_add_items(playlist_id,[track_id])

                        dbcurs.execute("INSERT INTO track_genres (track_id, genre_id, track_name) VALUES (?, ?, ?)", (track_id, genre_id, track_name))

                    except sqlite3.IntegrityError:
                        logger.error(f"Track is already associated with genre({playback['item']['name']} -> {selection})")
                        sp.playlist_remove_all_occurrences_of_items(playlist_id,[track_id])

                # self.ui.label.setText(f"Now Playing: {track_name} by {artist_name}")
            elif playback["item"]["type"] == "episode":
                logger.error("Genres are only applicable to music")
            else:
                logger.error("Unknown playback")
        else:
            logger.error("Can't apply genre information to nothingness")



#  AI GENERATED UTILITY FUNCS

def setup_database():
    #conn = sqlite3.connect('spotify_tracks.db')
    #cursor = conn.cursor()

    # Create a table to store the tracks if it doesn't exist
    dbcurs.execute("""
        CREATE TABLE IF NOT EXISTS tracks (
            track_id TEXT PRIMARY KEY,
            name TEXT,
            artist TEXT,
            labelled INTEGER DEFAULT 0,
            genre_label TEXT DEFAULT NULL
        )
    """)

    dbcurs.execute("""
        CREATE TABLE IF NOT EXISTS genres (
            genre_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            spotify_playlist_id TEXT DEFAULT NULL
        )
    """)

    dbcurs.execute("""
        CREATE TABLE IF NOT EXISTS track_genres (
            track_id TEXT,
            genre_id INTEGER,
            track_name TEXT,
            PRIMARY KEY(track_id, genre_id),
            FOREIGN KEY(track_id) REFERENCES tracks(track_id),
            FOREIGN KEY(genre_id) REFERENCES genres(genre_id)
            )
        """)

    #conn.commit()
    #conn.close()
    return


def fetch_liked_songs_spotipy():
    songs = []
    offset = 0
    limit = 50  # Max allowed by Spotify

    logger.info("Requesting liked song data...")

    while True:
        results = sp.current_user_saved_tracks(limit=limit, offset=offset)
        songs.extend(results['items'])

        logger.info(f"Retrieving song data, index: {offset}")

        if len(results['items']) < limit:
            break

        offset += limit

    logger.info(f"Returning {len(songs)} songs")

    return songs


def save_songs_to_db(songs):  # 'songs' being Spotify song objects

    for song in songs:
        track_id = song["track"]["id"]
        name = song["track"]["name"]
        artist = song["track"]["artists"][0]["name"]
        dbcurs.execute("INSERT OR IGNORE INTO tracks (track_id, name, artist) VALUES (?, ?, ?)", (track_id, name, artist))

    dbcon.commit()

    logger.info("Stored liked songs, beginning genre fetching")

    unique_artist_ids = list({song["track"]["artists"][0]["id"] for song in songs})

    # Batch artists to sets of 50 (Spotify's limit for a single call)
    for i in range(0, len(unique_artist_ids), 50):
        logger.info(f"Starting genre data batch from {i}")
        batched_artist_ids = unique_artist_ids[i:i+50]
        artists_info = sp.artists(batched_artist_ids)["artists"]

        for artist_info in artists_info:
            artist_id = artist_info["id"]
            artist_genres = artist_info["genres"]

            for genre in artist_genres:
                # Insert the genre into the 'genres' table if it doesn't already exist
                dbcurs.execute("INSERT OR IGNORE INTO genres (name) VALUES (?)", (genre,))

                # Fetch the genre_id of the genre we just inserted (or the existing one)
                dbcurs.execute("SELECT genre_id FROM genres WHERE name = ?", (genre,))
                genre_id = dbcurs.fetchone()[0]

                # Find all tracks associated with this artist in our songs list and link them to the genre
                associated_tracks = [song for song in songs if song["track"]["artists"][0]["id"] == artist_id]
                for track in associated_tracks:
                    track_id = track["track"]["id"]
                    track_name = track['track']['name']
                    # Link track to genre in 'track_genres' table
                    dbcurs.execute("INSERT OR IGNORE INTO track_genres (track_id, genre_id, track_name) VALUES (?, ?, ?)", (track_id, genre_id, track_name))

            dbcon.commit()  # Commit changes to the database after each artist. You can adjust this if needed.

    threshold = 25

    logger.info(f"Beginning trimming. Threshold = {threshold}")

    # 1. Query the database to gather all genre IDs associated with tracks
    dbcurs.execute("SELECT genre_id FROM track_genres")
    all_genre_ids = [row[0] for row in dbcurs.fetchall()]

    # 2. Calculate the frequency of each genre ID
    genre_counts = Counter(all_genre_ids)

    dbcurs.execute("SELECT genre_id, name FROM genres")
    id_to_name = {genre_id: name for genre_id, name in dbcurs.fetchall()}
    genre_name_counts = {id_to_name[genre_id]: count for genre_id, count in genre_counts.items()}

    sorted_genre_counts = dict(sorted(genre_name_counts.items(), key=lambda item: item[1], reverse=True))
    with open('weirdo_genre_data.json', 'w') as json_file:
        json.dump(sorted_genre_counts, json_file, indent=4)

    # 3. Identify genre IDs that are below the threshold
    low_freq_genre_ids = [genre_id for genre_id, count in genre_counts.items() if count < threshold]

    # 4. Convert the low-frequency genre IDs to genre names (optional)
    dbcurs.execute(
        "SELECT genre_id, name FROM genres WHERE genre_id IN ({})".format(', '.join(['?'] * len(low_freq_genre_ids))),
        tuple(low_freq_genre_ids))
    low_freq_genres = dbcurs.fetchall()  # This gives pairs of (genre_id, genre_name)

    # 5. Update the database to reflect changes
    # Here, I'm removing tracks associated with low-frequency genres.
    for genre_id, genre_name in low_freq_genres:
        # Delete associations from track_genres table
        dbcurs.execute("DELETE FROM track_genres WHERE genre_id=?", (genre_id,))

        # Delete the low-frequency genre from genres table (optional step)
        dbcurs.execute("DELETE FROM genres WHERE genre_id=?", (genre_id,))
    dbcon.commit()
    logger.info("Data downloaded and trimmed!")


if __name__ == "__main__":
    app = QApplication([])
    setup_database()
    window = Widget()
    window.show()

    sys.exit(app.exec())

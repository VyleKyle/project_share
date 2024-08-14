import json
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from tkinter import *
from tkinter import messagebox

class SpotifyGenreLabeler:
    def __init__(self):
        self.data_file = 'labelled_data.json'
        self.auth_data = self.load_auth()
        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=self.auth_data['client_id'],
                                                            client_secret=self.auth_data['client_secret'],
                                                            redirect_uri=self.auth_data['redirect_uri'],
                                                            scope=self.auth_data['scope']))
        self.user_id = self.sp.current_user()['id']
        self.liked_songs = self.get_liked_songs()

    def load_auth(self):
        with open('auth.json') as json_file:
            return json.load(json_file)

    def get_liked_songs(self):
        results = self.sp.current_user_saved_tracks()
        return results['items']

    def save_data(self, data):
        with open(self.data_file, 'w') as json_file:
            json.dump(data, json_file)

    def load_data(self):
        if os.path.exists(self.data_file):
            with open(self.data_file) as json_file:
                return json.load(json_file)
        else:
            return {}

    def add_song_to_playlist(self, song_id, genre):
        playlist_name = f"LikedLabelled/{genre}"
        playlists = self.sp.user_playlists(self.user_id)
        playlist_id = None
        for playlist in playlists['items']:
            if playlist['name'] == playlist_name:
                playlist_id = playlist['id']
                break

        if playlist_id is None:
            playlist = self.sp.user_playlist_create(self.user_id, playlist_name)
            playlist_id = playlist['id']

        self.sp.playlist_add_items(playlist_id, [song_id])

    def label_song(self, song_id, genre):
        data = self.load_data()
        data[song_id] = genre
        self.save_data(data)
        self.add_song_to_playlist(song_id, genre)


class GenreLabelerGUI:
    def __init__(self, root, labeler):
        self.root = root
        self.labeler = labeler
        self.root.title("Spotify Genre Labeler")
        self.label_var = StringVar()
        self.label_entry = Entry(root, textvariable=self.label_var)
        self.label_entry.pack()
        self.next_button = Button(root, text="Next Song", command=self.next_song)
        self.next_button.pack()

    def next_song(self):
        if len(self.labeler.liked_songs) == 0:
            messagebox.showinfo("Done", "All songs have been labeled.")
            return

        song = self.labeler.liked_songs.pop(0)
        genre = self.label_var.get()
        if genre:
            self.labeler.label_song(song['track']['id'], genre)

        self.root.title(song['track']['name'])
        self.label_var.set("")


root = Tk()
labeler = SpotifyGenreLabeler()
gui = GenreLabelerGUI(root, labeler)
root.mainloop()


# Goals:
# Authorize
# Get saved songs
# tracks.txt > list of track - artist
# artists.json > list of artist - genre, genre, genre
# output.json > list of track - genre, genre, genre
#
# Known issues:
# Some artists aren't returning genre data. This is used in output, so tracks lack it as well.
# Note from the future: They didn't return because spotify didn't have or offer it.

import credentials
import requests
import json
from time import sleep

# Set limit and offset for pagination of large data
limit = 50
offset = 0

# Set batch size
batch_size = 10

# Initialize empty lists for tracks and artists
tracks = []
artists = []

# Set request delay to avoid rate limit
delay = 60 / 75

# Implement OAuth2 authorization with Spotify
auth_url = "https://accounts.spotify.com/authorize"
auth_params = {
    "client_id": secrets.client_id,
    "response_type": "code",
    "redirect_uri": secrets.redirect_uri,
    "scope": "user-library-read"
}

# Prompt user to open authorization link
auth_link = f"{auth_url}?{'&'.join([f'{key}={value}' for key, value in auth_params.items()])}"
print("Please open the following link in your web browser and return with the authorization code:")
print(auth_link)
auth_code = input("Enter authorization code: ")

# Use authorization code to get access token
token_url = "https://accounts.spotify.com/api/token"
token_data = {
    "grant_type": "authorization_code",
    "code": auth_code,
    "redirect_uri": secrets.redirect_uri,
    "client_id": secrets.client_id,
    "client_secret": secrets.client_secret
}

# Request access token
token_response = requests.post(token_url, data=token_data)
access_token = token_response.json()["access_token"]

# Use access token to request saved tracks
track_url = "https://api.spotify.com/v1/me/tracks"
track_params = {
    "limit": limit,
    "offset": offset
}
track_headers = {
    "Authorization": f"Bearer {access_token}"
}
print("Entering loop")
# Request saved tracks and loop through pages
while True:
    track_response = requests.get(track_url, params=track_params, headers=track_headers)
    print(track_response.status_code)
    track_data = track_response.json()

    # Add saved tracks and artist names to lists
    for item in track_data["items"]:
        track = item["track"]
        tracks.append(track)
        for artist in track["artists"]:
            if not artist in artists:
                artists.append(artist)

    # Check for next page of results
    if track_data["next"] is not None:
        offset += limit
        track_params["offset"] = offset
    else:
        break

    # Implement request delay
    sleep(delay)

# Generate "tracks.txt" with saved tracks and artist names
with open("tracks.txt", "w") as file:
    for track in tracks:
        file.write(f"{track['name']}, {', '.join( [artist['name'] for artist in track['artists']] )}\n")

# Generate "artists.json" with artists and their affiliated genres
artist_url = "https://api.spotify.com/v1/artists"
artist_headers = {
    "Authorization": f"Bearer {access_token}"
}

# Initialize empty list for artist names and genres
artist_genres = {}

print("Entering artist loop")
# Loop through artists in batches
for i in range(0, len(artists), batch_size):
    # Set artist ids for current batch
    print(artists[i:i+batch_size])
    artist_ids = ",".join([artist['id'] for artist in artists[i:i+batch_size]])

    # Request artist data
    artist_params = {
        "ids": artist_ids
    }
    print(artist_ids)
    artist_response = requests.get(artist_url, params=artist_params, headers=artist_headers)
    artist_data = artist_response.json()

    # Add artist names and genres to list
    for artist in artist_data["artists"]:
        artist_genres[artist['name']] = artist['genres']
    sleep(delay)

# Write artist data to "artists.json"
with open("artists.json", "w") as file:
    json.dump(artist_genres, file, indent=4)

# Generate "output.json" with tracks and affiliated genres
output_data = {}

# Add track names and genres to list
for track in tracks:
    output_data[track["name"]] = [artist_genres[artist['name']] for artist in track['artists'] if artist['name']]

# Write output data to "output.json"
with open("output.json", "w") as file:
    json.dump(output_data, file, indent=4)

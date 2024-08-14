# This was originally a prompt for guiding ChatGPT to do what I wanted.

Write a python script to accomplish the following goals:
- Authorize with spotify using OAuth2 authorization flow.
- Get the user's saved tracks from spotify with pagination using limit and offset.
- Generate "tracks.txt" with every line corresponding to a saved track, followed by its contributing artists, comma separated.
- Generate "artists.json" containing a json list of artists and their affiliated genres from the saved tracks. (example: ["artist": ["grunge", "rock"]] )
- Generate "output.json" containing json data of tracks and their affiliated genres.

Additional information and rules:
- You may not use Spotipy.
- The user will have many saved tracks, you must use pagination.
- Spotify maintains a variable request rate limit, you will be denied if you make too many requests in a minute.
- The script is nearly complete and will be provided to you. Currently, Spotify denies the request made at `artist_response = requests.get(artist_url, params=artist_params, headers=artist_headers)` with HTTP response code 413. Because we do not know the size limit, please implement a `batch_size` variable and complete the operation in batches.

```
-SNIP- I copy/pasted the whole script here at some point -SNIP-
```

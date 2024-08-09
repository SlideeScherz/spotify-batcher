import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Spotify API credentials
SPOTIPY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
SPOTIPY_REDIRECT_URI = os.getenv('SPOTIPY_REDIRECT_URI')
SCOPE = 'playlist-modify-private'

# Authenticate with Spotify
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIPY_CLIENT_ID,
    client_secret=SPOTIPY_CLIENT_SECRET,
    redirect_uri=SPOTIPY_REDIRECT_URI,
    scope=SCOPE
))

# Function to add songs to a playlist
def add_songs_to_playlist(playlist_id, song_list_file):
    with open(song_list_file, 'r') as file:
        songs = file.readlines()

    track_uris = []
    for song in songs:
        song = song.strip()
        if not song:
            continue
        results = sp.search(q=song, type='track', limit=1)
        if results['tracks']['items']:
            track_uri = results['tracks']['items'][0]['uri']
            track_uris.append(track_uri)
        else:
            print(f"Song '{song}' not found on Spotify.")

    if track_uris:
        sp.playlist_add_items(playlist_id, track_uris)
        print(f"Added {len(track_uris)} songs to the playlist.")
    else:
        print("No songs were added to the playlist.")

if __name__ == "__main__":
    # Set your Spotify playlist ID here
    playlist_id = 'your_playlist_id_here'
    
    # Set the path to your input file
    song_list_file = 'songs.txt'

    # Add songs to the playlist
    add_songs_to_playlist(playlist_id, song_list_file)

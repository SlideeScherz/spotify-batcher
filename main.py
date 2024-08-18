import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv
import logging

load_dotenv()

logging.basicConfig(filename='app.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# credentials
SPOTIPY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
SPOTIPY_REDIRECT_URI = os.getenv('SPOTIPY_REDIRECT_URI')
SCOPE = 'user-library-read playlist-modify-public user-library-modify'

# other config
song_list_file_path = 'songs.txt'

# verify config
if not SPOTIPY_CLIENT_ID or not SPOTIPY_CLIENT_SECRET or not SPOTIPY_REDIRECT_URI or not SCOPE or not song_list_file_path:
    raise ValueError("Please set SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, and SPOTIPY_REDIRECT_URI in your .env file.")
else:
    logging.info("Config verified.")

# create authorized Spotify client
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIPY_CLIENT_ID,
    client_secret=SPOTIPY_CLIENT_SECRET,
    redirect_uri=SPOTIPY_REDIRECT_URI,
    scope=SCOPE
))

def get_song_ids_from_file(file_path):
    with open(file_path, 'r') as file:
        song_names = file.readlines()
    return [song.strip() for song in song_names]

def search_song(song_name):
    result = sp.search(q=song_name, limit=1, type='track')
    if result['tracks']['items']:
        return result['tracks']['items'][0]['id']
    return None

def check_song_in_library(song_id):
    return sp.current_user_saved_tracks_contains([song_id])[0]

def add_song_to_library(song_id):
    sp.current_user_saved_tracks_add([song_id])

def process_songs(file_path):
    song_names = get_song_ids_from_file(file_path)
    
    for song_name in song_names:
        song_id = search_song(song_name)
        if not song_id:
            logging.info(f"Song not found: {song_name}. Skipping.")
            continue
        
        if check_song_in_library(song_id):
            logging.info(f"Song '{song_name}' already in library. Skipping.")
        else:
            add_song_to_library(song_id)
            logging.info(f"Song '{song_name}' added to library successfully.")

if __name__ == "__main__":
    process_songs("songs.txt")
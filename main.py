import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv
import logging

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(filename='app.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

logging.info(f"Running script: {os.path.basename(__file__)}")

# Spotify API credentials
SPOTIPY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
SPOTIPY_REDIRECT_URI = os.getenv('SPOTIPY_REDIRECT_URI')
SCOPE = 'user-library-read playlist-modify-public user-library-modify'

if not SPOTIPY_CLIENT_ID or not SPOTIPY_CLIENT_SECRET or not SPOTIPY_REDIRECT_URI:
    raise ValueError("Please set SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, and SPOTIPY_REDIRECT_URI in your .env file.")
else:
    logging.info("Spotify API credentials loaded successfully.")

# Authenticate with Spotify
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIPY_CLIENT_ID,
    client_secret=SPOTIPY_CLIENT_SECRET,
    redirect_uri=SPOTIPY_REDIRECT_URI,
    scope=SCOPE
))

# Get the user's saved tracks
track_search_results = sp.current_user_saved_tracks()
for idx, item in enumerate(track_search_results['items']):
    track = item['track']
    print(idx, track['artists'][0]['name'], " – ", track['name'])

# Function to create a playlist
def create_playlist(name, description, public=True):
    user_id = sp.current_user()['id']
    playlist = sp.user_playlist_create(user=user_id, name=name, description=description, public=public)
    logging.info(f"Created playlist '{name}' with ID {playlist['id']}")
    return playlist['id']

# Function to add songs to a playlist
def add_songs_to_playlist(song_list_file):
    with open(song_list_file, 'r') as file:
        songs = file.readlines()

    if not songs:
        logging.warn(f"No songs found in the input file: {song_list_file}")
        return
    
    logging.info(f"Parsed {len(songs)} songs from input file: {song_list_file}")

    track_uris = []
    for song in songs:
        song = song.strip()
        
        if not song:
            logging.warn("No songs found in the input file.")
            continue
        
        results = sp.search(q=song, type='track', limit=1)
        logging.debug(f"Search results for '{song}': {results}")

        if results['tracks']['items']:
            track_uri = results['tracks']['items'][0]['uri']
            track_uris.append(track_uri)
        else:
            logging.info(f"Song '{song}' not found on Spotify.")

    if track_uris:
        playlist_id = create_playlist(name='My Playlist', description='My playlist description')
        sp.playlist_add_items(playlist_id=playlist_id, items=track_uris)
        # sp.current_user_saved_tracks_add(tracks=track_uris)
        logging.info(f"Adding {len(track_uris)} songs to the playlist.")
        logging.debug(f"Track URIs: {track_uris}")
    else:
        logging.info("No songs were added to the playlist.")

if __name__ == "__main__":
    # Set your Spotify playlist ID here
    # playlist_id = 'your_playlist_id_here'
    
    # Set the path to your input file
    song_list_file = 'pauls-awesome-songs.txt'

    # Add songs to the playlist
    add_songs_to_playlist(song_list_file)

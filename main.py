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

# track_search_results = sp.current_user_saved_tracks()
# for idx, item in enumerate(track_search_results['items']):
#     track = item['track']
#     print(idx, track['artists'][0]['name'], " – ", track['name'])

# create playlist, and return the playlist.id
def create_playlist(name, description, public=True):
    user_id = sp.current_user()['id']
    playlist = sp.user_playlist_create(user=user_id, name=name, description=description, public=public)
    logging.info(f"Created playlist '{name}' with ID {playlist['id']}")
    return playlist['id']

def parse_songs(file_path):
    """
    Reads the content of a file and returns a list of lines.

    :param file_path: Path to the input file
    :return: List of lines from the file
    """
    with open(file_path, 'r') as file:
        lines = file.readlines()

    logging.info(f"Parsed {len(lines)} songs from input file: {file_path}")
    return lines

def add_songs_to_playlist(tracks):
    """
    Searches for songs on Spotify and adds them to a new playlist.

    todo: change argument to list of songs rather than file path
    
    :param song_list_file: Path to the file containing the list of songs
    """

    if not tracks:
        raise ValueError("No songs found in the input file.")

    # search for each song on Spotify
    track_uris = []
    for song in tracks:
        song = song.strip()
        
        if not song:
            logging.warn("No songs found in the input file.")
            continue
        
        results = sp.search(q=song, type='track', limit=1)
        logging.info(f"Search results for '{song}': {results}")

        if results['tracks']['items']:
            track_uri = results['tracks']['items'][0]['uri']
            track_uris.append(track_uri)
        else:
            logging.info(f"Song '{song}' not found on Spotify.")

    if len(track_uris) < len(tracks):
        logging.warn(f"Could not find {len(tracks) - len(track_uris)} songs on Spotify.")

    if track_uris:
        playlist_id = create_playlist(name='My Playlist', description='My playlist description')
        sp.playlist_add_items(playlist_id=playlist_id, items=track_uris)
        # sp.current_user_saved_tracks_add(tracks=track_uris)
        logging.info(f"Adding {len(track_uris)} songs to the playlist.")
        logging.debug(f"Track URIs: {track_uris}")
    else:
        logging.info("No songs were added to the playlist.")

if __name__ == "__main__":
    logging.info(f"Running script: {os.path.basename(__file__)}")
    tracks = parse_songs(song_list_file_path)
    add_songs_to_playlist(tracks)
    logging.info("-----------------\n\n")

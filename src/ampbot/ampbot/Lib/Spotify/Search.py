from Lib.Config import Parser
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

def getResults(query, config):
    client_credentials_manager = SpotifyClientCredentials(client_id=config.production.spotify.clientId, client_secret=config.production.spotify.clientSecret)
    return spotipy.Spotify(client_credentials_manager=client_credentials_manager).search(q=query, limit=4, offset=0, type='track,album,artist,playlist')
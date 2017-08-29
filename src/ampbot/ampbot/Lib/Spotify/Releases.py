from Lib.Config import Parser
import spotipy
import spotipy.util as util

def newReleases(config, country = None, limit = 20, offset = 0):
    token = util.prompt_for_user_token(config.production.spotify.username, scope=config.production.spotify.scopes, client_id=config.production.spotify.clientId, client_secret=config.production.spotify.clientSecret, redirect_uri=config.production.spotify.redirectUri)
    sp = spotipy.Spotify(auth=token)
    return sp.new_releases(country, limit, offset)

from Lib.Config import Parser
import spotipy
import spotipy.util as util
import arrow
import logging

from Lib.ampbot import Logger
logger = Logger.ConfigureLogger(__name__)

def getTrackById(id, config):
    token = util.prompt_for_user_token(config.production.spotify.username, scope=config.production.spotify.scopes, client_id=config.production.spotify.clientId, client_secret=config.production.spotify.clientSecret, redirect_uri=config.production.spotify.redirectUri)
    sp = spotipy.Spotify(auth=token)
    return sp.track(id)

def getTrackAnalysis(id, config):
    token = util.prompt_for_user_token(config.production.spotify.username, scope=config.production.spotify.scopes, client_id=config.production.spotify.clientId, client_secret=config.production.spotify.clientSecret, redirect_uri=config.production.spotify.redirectUri)
    sp = spotipy.Spotify(auth=token)
    return sp.audio_features([id])
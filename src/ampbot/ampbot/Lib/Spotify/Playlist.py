from Lib.Config import Parser
from Lib.ampbot import Logger
import spotipy
import spotipy.util as util
import arrow
import logging

logger = Logger.ConfigureLogging()

def addTrack(id, config):
    if 'spotify:track:' in id:
        if checkIfTrackAlreadyInPlaylist(id.replace('spotify:track:', ''), config) == False:
            token = util.prompt_for_user_token(config.production.spotify.username, scope=config.production.spotify.scopes, client_id=config.production.spotify.clientId, client_secret=config.production.spotify.clientSecret, redirect_uri=config.production.spotify.redirectUri)
            sp = spotipy.Spotify(auth=token)
            temp = []
            temp.append(id)
            sp.user_playlist_add_tracks(config.production.spotify.username, config.production.spotify.playlistId, temp)
            logger.info('add track {0} to community playlist'.format(id))
            return True
        else:
            logger.info('track {0} already in community playlist'.format(id))
            return False
    else:
        pass

def updatePlaylistName(firstName, config):
    local = arrow.utcnow().to('Europe/Berlin')
    newName = 'ampbot [last update {0} by {1}]'.format(local.format('YYYY-MM-DD'), firstName)
    token = util.prompt_for_user_token(config.production.spotify.username, scope=config.production.spotify.scopes, client_id=config.production.spotify.clientId, client_secret=config.production.spotify.clientSecret, redirect_uri=config.production.spotify.redirectUri)
    sp = spotipy.Spotify(auth=token)
    sp.user_playlist_change_details(
        config.production.spotify.username,
        config.production.spotify.playlistId,
        name=newName)
    logger.info('changed playlist name to "{0}"'.format(newName))

def checkIfTrackAlreadyInPlaylist(id, config):
    token = util.prompt_for_user_token(config.production.spotify.username, scope=config.production.spotify.scopes, client_id=config.production.spotify.clientId, client_secret=config.production.spotify.clientSecret, redirect_uri=config.production.spotify.redirectUri)
    sp = spotipy.Spotify(auth=token)
    limit = 100
    offset = 0
    weiter = True
    tracks = []
    while weiter:
        results = sp.user_playlist_tracks(config.production.spotify.username,
                    config.production.spotify.playlistId,
                    limit=limit,
                    offset=offset)
        if results['total'] == results['offset']:
            weiter = False
    
        for track in results['items']:
            if track['track']['id'] == id:
                return True
        offset = offset + limit
    return False
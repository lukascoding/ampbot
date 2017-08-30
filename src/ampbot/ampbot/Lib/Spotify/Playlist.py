from Lib.Config import Parser
import spotipy
import spotipy.util as util
import arrow

def addTrack(id, config):
    if 'spotify:track:' in id:
        token = util.prompt_for_user_token(config.production.spotify.username, scope=config.production.spotify.scopes, client_id=config.production.spotify.clientId, client_secret=config.production.spotify.clientSecret, redirect_uri=config.production.spotify.redirectUri)
        sp = spotipy.Spotify(auth=token)
        temp = []
        temp.append(id)
        sp.user_playlist_add_tracks(config.production.spotify.username, config.production.spotify.playlistId, temp)
    else:
        pass

def updatePlaylistName(firstName, config):
    local = arrow.utcnow().to('Europe/Berlin')
    token = util.prompt_for_user_token(config.production.spotify.username, scope=config.production.spotify.scopes, client_id=config.production.spotify.clientId, client_secret=config.production.spotify.clientSecret, redirect_uri=config.production.spotify.redirectUri)
    sp = spotipy.Spotify(auth=token)
    sp.user_playlist_change_details(
        config.production.spotify.username,
        config.production.spotify.playlistId,
        name='ampbot [last update {0} by {1}]'.format(local.format('YYYY-MM-DD'), firstName))

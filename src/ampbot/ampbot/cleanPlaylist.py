from Lib.Config import Parser
import spotipy
import spotipy.util as util

config = Parser.parse_ini('ampbot.ini')

token = util.prompt_for_user_token(config.production.spotify.username, scope=config.production.spotify.scopes, client_id=config.production.spotify.clientId, client_secret=config.production.spotify.clientSecret, redirect_uri=config.production.spotify.redirectUri)
sp = spotipy.Spotify(auth=token)
sp.trace = False

limit = 100
offset = 0
weiter = True
tracks = []
tracksToRemove = list()


while weiter:
     results = sp.user_playlist_tracks(config.production.spotify.username,
                    config.production.spotify.playlistId,
                    limit=limit,
                    offset=offset)
     if results['total'] == results['offset']:
         weiter = False
    
     for track in results['items']:
         if track['track']['id'] in tracks:
             print(track['track']['id'] + '   ' + track['track']['name'] + ' - ' + track['track']['artists'][0]['name'] + ' - ' + track['track']['album']['name'])
             tracksToRemove.append({"uri": "{0}".format(track['track']['id']), "positions":[offset+results['items'].index(track)]})
         else:
             tracks.append(track['track']['id'])
     offset = offset + limit

sp.user_playlist_remove_specific_occurrences_of_tracks(config.production.spotify.username,
            config.production.spotify.playlistId,
            tracksToRemove)

print(offset)
print(len(tracks))

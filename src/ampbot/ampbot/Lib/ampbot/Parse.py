#Url

def TrackUrl(track):
    url = None
    if track['external_urls']['spotify']:
        url = track['external_urls']['spotify']
    return url

def AlbumUrl(album):
    url = None
    if album['external_urls']['spotify']:
        url = album['external_urls']['spotify']
    return url

def ArtistUrl(artist):
    url = None
    if artist['external_urls']['spotify']:
        url = artist['external_urls']['spotify']
    return url

def PlaylistUrl(playlist):
    url = None
    if playlist['external_urls']['spotify']:
        url = playlist['external_urls']['spotify']
    return url


#PreviewUrl

def TrackPreviewUrl(track):
    url = None
    if track['preview_url']:
        url = track['preview_url']
    return url

#ThumbUrl

def TrackThumbUrl(track):
    thumb = None
    if len(track['album']['images']) > 0:
        thumb = track['album']['images'][0]['url']
    return thumb

def AlbumThumbUrl(album):
    thumb = None
    if len(album['images']) > 0:
        thumb = album['images'][0]['url']
    return thumb

def ArtistThumbUrl(artist):
    thumb = None
    if len(artist['images']) > 0:
        thumb = artist['images'][0]['url']
    return thumb

def PlaylistThumbUrl(playlist):
    thumb = None
    if len(playlist['images']) > 0:
        thumb = playlist['images'][0]['url']
    return thumb


#Album

def TrackAlbumName(track):
    album = ''
    if len(track['album']['name']) > 0:
        album = track['album']['name']
    return album


#Name

def TrackName(track):
    name = None
    if track['name']:
        name = track['name']
    else:
        name = ""
    return '{0}'.format(name)

def ArtistName(artist):
    name = None
    if artist['name']:
        name = artist['name']
    else:
        name = ""
    return '{0}'.format(name)

def AlbumName(album):
    name = None
    if album['name']:
        name = album['name']
    else:
        name = ""
    return '{0}'.format(name)

def PlaylistName(playlist):
    name = None
    if playlist['name']:
        name = playlist['name']
    else:
        name = ""
    return '{0}'.format(name)

#Follower

def ArtistFollower(artist):
    follower = 0
    if artist['followers']['total']:
        follower = artist['followers']['total']
    return follower


#Artist

def TrackFirstArtist(track):
    if len(track['artists']) > 0:
        return track['artists'][0]['name']
    else:
        return ''

def TrackArtists(track):
    artists = ''
    if len(track['artists']) > 0:
        if len(track['artists']) == 1:
            artists += track['artists'][0]['name']
        else:
            count = 1
            for artist in track['artists']:
                artists += '{0} '.format(artist['name'])
                if len(track['artists']) > count:
                    artists += '& '
                count += 1
    return artists

def AlbumArtists(album):
    artists = ''
    if len(album['artists']) > 0:
        if len(album['artists']) == 1:
            artists += album['artists'][0]['name']
        else:
            count = 1
            for artist in album['artists']:
                artists += '{0} '.format(artist['name'])
                if len(album['artists']) > count:
                    artists += '& '
                count += 1
    return artists

#Messages

def TrackInlineTitle(track):
    return TrackName(track)

def TrackInlineTitleWithOutPreview(track):
    return 'Track: {0}'.format(TrackName(track))

def TrackInlineDescription(track):
    return TrackArtists(track)

def TrackInlineDescriptionWithOutPreview(track):
    return '{0} by {1} from {2}'.format(TrackName(track), TrackArtists(track), TrackAlbumName(track))

def TrackAddedSuccessDescription(track):
    return 'successfully added {0} by {1}'.format(TrackName(track), TrackArtists(track))

def TrackAddedFailedDescription(track):
    return '{0} by {1} already in playlist'.format(TrackName(track), TrackArtists(track))

def ArtistInlineTitle(artist):
    return 'Artist: {0}'.format(ArtistName(artist))

def ArtistInlineDescription(artist):
    return '{0} with {1} Followers'.format(ArtistName(artist), ArtistFollower(artist))

def AlbumInlineTitle(album):
    return 'Album: {0}'.format(AlbumName(album))

def AlbumInlineDescription(album):
    return '{0} by {1}'.format(AlbumName(album), AlbumArtists(album))

def PlaylistInlineTitle(playlist):
    return 'Playlist: {0}'.format(PlaylistName(playlist))

def PlaylistInlineDescription(playlist):
    return '{0}'.format(PlaylistName(playlist))

def TrackInlineInputMessage(track):
    return '[{0}]({1}) by {2} from {3}'.format(TrackName(track), TrackUrl(track), TrackArtists(track), TrackAlbumName(track))

def AlbumInlineInputMessage(album):
    return '[{0}]({1}) by {2}'.format(AlbumName(album), AlbumUrl(album), AlbumArtists(album))

def ArtistInlineInputMessage(artist):
    return '[{0}]({1}) with {2} Followers'.format(ArtistName(artist), ArtistUrl(artist), ArtistFollower(artist))

def PlaylistInlineInputMessage(playlist):
    return '[{0}]({1})'.format(PlaylistName(playlist), PlaylistUrl(playlist))

def AlbumReleaseInlineTitle(count, album):
    return '{0}. {1}'.format(count, AlbumName(album))

def AlbumReleaseInlineInputMessage(album):
    return 'NEW RELEASE\n\n[{0}]({1}) by {2}'.format(AlbumName(album), AlbumUrl(album), AlbumArtists(album))
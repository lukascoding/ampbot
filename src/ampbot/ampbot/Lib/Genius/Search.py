from Lib.ampbot import Logger
from rauth import OAuth2Service
import json

logger = Logger.ConfigureLogger(__name__)

def getTrack(query, config):
    logger.info('get lyrics for query: {0}'.format(query))
    api = OAuth2Service(
        config.production.genius.clientId,
        config.production.genius.clientSecret,
        name='GeniusApi',
        access_token_url = config.production.genius.accessTokenUri,
        authorize_url = config.production.genius.authorizeUri,
        base_url = config.production.genius.baseUri)

    session = api.get_session(config.production.genius.token)
    
    response = session.get('/search?q={0}'.format(query))
    data = json.loads(response.text)
    if CheckIfThereIsASong(data):
        track = data["response"]["hits"][0]["result"]
        session.close()
        return track

def CheckIfThereIsASong(data):
    try:
        song_api_path = data["response"]["hits"][0]["result"]["api_path"]
    except:
        return False
    return True

from Lib.ampbot import Logger
import requests
from bs4 import BeautifulSoup
from rauth import OAuth2Service
import json

logger = Logger.ConfigureLogger(__name__)

def getLyrics(query, config):
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
        song_api_path = data["response"]["hits"][0]["result"]["api_path"]
        song_url = config.production.genius.baseUri + song_api_path
        response = session.get(song_url)
        song = json.loads(response.text)
        path = song["response"]["song"]["path"]
        page_url = "http://genius.com" + path

        page = requests.get(page_url)
        session.close()
        return GetLyricsFromHtmlString(page.text)

def CheckIfThereIsASong(data):
    try:
        song_api_path = data["response"]["hits"][0]["result"]["api_path"]
    except:
        return False
    return True

def GetLyricsFromHtmlString(html):
    soup = BeautifulSoup(html, "html.parser")
    div = soup.find('div',{'class': 'song_body-lyrics'})
    lyrics = div.find('p').getText()
    if lyrics == '' or lyrics == None:
        lyrics = 'no lyrics found'    
    return lyrics
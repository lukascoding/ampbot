from Lib.Config import Parser

config = Parser.parse_ini('ampbot.ini')

def Start():
    return config.answers.start

def Settings():
    return config.answers.settings

def Help():
    return config.answers.help

def Test():
    return config.answers.test

def Rate(ratelink):
    return config.answers.rate.format(ratelink)

def Group(grouplink):
    return config.answers.group.format(grouplink)

def Issue():
    return config.answers.issue

def SendToAdmin():
    return config.answers.sendtoadmin

def Channel():
    return config.answers.channel

def Playlist(playlistUri, playlistId):
    return config.answers.playlist.format(playlistUri, playlistId)

def Default():
    return config.answers.default
    
from Lib.Config import Parser

config = Parser.parse_ini('ampbot.ini')

def Start():
    return config.answers.start

def Settings():
    return config.answers.settings

def Help():
    return config.answers.help

def Test():
    return config.answers.Test

def Issue():
    return config.answers.issue

def SendToAdmin():
    return config.answers.sendtoadmin

def Channel():
    return config.answers.channel

def Playlist():
    return config.answers.playlist

def Default():
    return config.answers.default
    
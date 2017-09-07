#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Bot.py"""
#own
from Lib.ampbot import Parse, Answers, Logger, Database, Filter
from Lib.ampbot.Functions import NormalCommand, ConversationCommand, CostlyCommand
from Lib.Config import Parser

#packages
from telegram.ext import *
from telegram.error import Unauthorized, NetworkError
from telegram.ext.dispatcher import run_async
from telegram import InlineQueryResultArticle, InlineQueryResultAudio, InputTextMessageContent, ParseMode, InlineKeyboardMarkup, InlineKeyboardButton, MessageEntity, Bot
from uuid import uuid4

import re
from pprint import pprint
from emoji import emojize
import arrow
import logging
import timeit

#from apscheduler.schedulers.background import BackgroundScheduler
#import requests
#from tld import get_tld
#import configparser
#import datetime
#import pytz
#import time
#import re
#import math
#import validators
#import threading
#import ftfy
#from tabulate import tabulate
ISSUES = range(1)
lastUpdate = None
scheduler = None
config = None
tgBot = None
clientId = None
clientSecret = None

logger = Logger.ConfigureLogger(__name__)

#NormalCommands
def start(bot, update):
    NormalCommand.Start(bot, update)

def settings(bot, update):
    NormalCommand.Settings(bot, update)

def help(bot, update):
    NormalCommand.Help(bot, update)

def test(bot, update):
    NormalCommand.Test(bot, update)

def rate(bot, update):
    NormalCommand.Rate(bot, update)

def group(bot, update):
    NormalCommand.Group(bot, update)

def channel(bot, update):
    NormalCommand.Channel(bot, update)

def playlist(bot, update):
    NormalCommand.Playlist(bot, update)

def answerIssues(bot, update):
    NormalCommand.AnswerIssues(bot, update)

def default(bot, update):
    NormalCommand.Default(bot, update)

#ConversationCommands
def issues(bot, update):
    return ConversationCommand.Issues(bot, update)

def sendToAdmin(bot, update):
    return ConversationCommand.SendToAdmin(bot, update)

def cancel(bot, update):
    return ConversationCommand.Cancel(bot, update)

#CostlyCommands
def inline(bot, update):
    CostlyCommand.ProcessInlineQuery(bot, update)
    
def chosen(bot, update):
    CostlyCommand.ProcessChosenInlineResult(bot, update)

def callback(bot, update):
    CostlyCommand.ProcessCallbackQuery(bot, update)

def new(bot, update):
    CostlyCommand.ProcessNewAlbumReleases(bot, update)    

def add(bot, update, args, user_data, chat_data):
    CostlyCommand.ProcessAddTrackToPlaylist(bot, update, args, user_data, chat_data)
        
@run_async
def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))   

def main():
    global config
    global tgBot
    global scheduler
    global lastUpdate
    withoutErrors = True
    config = Parser.parse_ini('ampbot.ini')

    logger.info('@ampbot started')
    
    updater = Updater(config.production.bot.token, workers=10)
    tgBot = updater.bot

    while withoutErrors:
        try:
            dp = updater.dispatcher

            dp.add_handler(CommandHandler("new", new))
            dp.add_handler(CommandHandler("add", add, pass_user_data=True, pass_chat_data=True, pass_args=True))
            dp.add_handler(CallbackQueryHandler(callback))
            dp.add_handler(InlineQueryHandler(inline))
            dp.add_handler(ChosenInlineResultHandler(chosen))

            dp.add_handler(CommandHandler("start", start))
            dp.add_handler(CommandHandler("settings", settings))
            dp.add_handler(CommandHandler("help", help))
            dp.add_handler(CommandHandler("rate", rate))
            dp.add_handler(CommandHandler("test", test))
            dp.add_handler(CommandHandler("group", group))
            dp.add_handler(CommandHandler("channel", channel))
            dp.add_handler(CommandHandler("playlist", playlist))

            filterIsAdminInPrivate = Filter.FilterIsAdminInPrivate()
            dp.add_handler(MessageHandler(filterIsAdminInPrivate, answerIssues))
            
            conversation = ConversationHandler(entry_points=[CommandHandler('issues', issues)],
                states={
                    ISSUES: [MessageHandler(Filters.text, sendToAdmin)]
                },
                fallbacks=[CommandHandler('cancel', cancel)])
            dp.add_handler(conversation)

            dp.add_handler(MessageHandler(None, default))

            dp.add_error_handler(error)
        
            updater.start_polling()
            updater.idle()
        except NetworkError:
            time.sleep(5)
        except Unauthorized:
            updater.last_update_id = updater.last_update_id + 1
        except:
            withoutErrors = False 

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(sys.stderr + '\nExiting by user request.\n')
        sys.exit(0)
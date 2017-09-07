"""NormalCommand.py"""
from Lib.ampbot import Answers, Logger
from Lib.Config import Parser
from telegram.ext.dispatcher import run_async
from telegram import ParseMode, InlineKeyboardMarkup, InlineKeyboardButton, Bot

config = Parser.parse_ini('ampbot.ini')
logger = Logger.ConfigureLogger(__name__)

@run_async
def Start(bot, update):
    bot.sendMessage(update.message.chat_id, Answers.Start(), parse_mode=ParseMode.MARKDOWN)
    logger.info('START: @{0}({1})'.format(update.message.from_user.username, update.message.from_user.id))

@run_async
def Settings(bot, update):
    bot.sendMessage(update.message.chat_id, Answers.Settings())
    logger.info('SETTINGS: @{0}({1})'.format(update.message.from_user.username, update.message.from_user.id))

@run_async
def Help(bot, update):
    bot.sendMessage(update.message.chat_id, Answers.Help())
    logger.info('HELP: @{0}({1})'.format(update.message.from_user.username, update.message.from_user.id))

@run_async
def Rate(bot, update):
    bot.sendMessage(update.message.chat_id,
        Answers.Rate('{0}={1}'.format(config.production.bot.rateLink, config.production.bot.username)),
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('Rate now', url='{0}={1}'.format(config.production.bot.rateLink, config.production.bot.username))]]),
        parse_mode=ParseMode.MARKDOWN)
    logger.info('RATE: @{0}({1})'.format(update.message.from_user.username, update.message.from_user.id))

@run_async
def Test(bot, update):
    print(str(update))
    bot.sendMessage(update.message.chat_id, Answers.Test())
    logger.info('TEST: @{0}({1})'.format(update.message.from_user.username, update.message.from_user.id))

@run_async
def Group(bot, update):
    bot.sendMessage(update.message.chat_id,
        Answers.Group(config.production.bot.groupLink),
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('Join now', url=config.production.bot.groupLink)]]),
        parse_mode=ParseMode.MARKDOWN)
    logger.info('GROUP: @{0}({1})'.format(update.message.from_user.username, update.message.from_user.id))

@run_async
def Channel(bot, update):
    bot.sendMessage(update.message.chat_id, Answers.Channel())
    logger.info('CHANNEL: @{0}({1})'.format(update.message.from_user.username, update.message.from_user.id))

@run_async
def Playlist(bot, update):
    bot.sendMessage(update.message.chat_id,
        Answers.Playlist(config.production.spotify.playlistUri, config.production.spotify.playlistFullId),
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('Join now', url=config.production.spotify.playlistUri)]]),
        parse_mode=ParseMode.MARKDOWN)
    logger.info('PLAYLIST: @{0}({1})'.format(update.message.from_user.username, update.message.from_user.id))

@run_async
def AnswerIssues(bot, update):
    logger.info('AnswerIssues: @{0}({1}): {2}'.format(update.message.from_user.username, update.message.from_user.id, update.message.text))
    if update.message.from_user.id == 8139296 and update.message.chat.type == 'private':
        if update.message.reply_to_message:
            bot.sendMessage(update.message.reply_to_message.forward_from.id, update.message.text, reply_to_message_id=update.message.reply_to_message.message_id - 1)
    else:
        pass

@run_async
def Default(bot, update):
    logger.info('DEFAULT: @{0}({1}): {2}'.format(update.message.from_user.username, update.message.from_user.id, update))
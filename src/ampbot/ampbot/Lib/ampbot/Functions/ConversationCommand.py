"""ConversationCommand.py"""
from Lib.ampbot import Answers, Logger
from Lib.Config import Parser
from telegram.ext.dispatcher import run_async
from telegram import ParseMode, Bot
from telegram.ext import *

config = Parser.parse_ini('ampbot.ini')
logger = Logger.ConfigureLogger(__name__)
ISSUES = range(1)

@run_async
def Issues(bot, update):
    bot.sendMessage(update.message.chat_id, Answers.Issue())
    logger.info('ISSUES: @{0}({1}): {2}'.format(update.message.from_user.username, update.message.from_user.id, update.message.text))
    return ISSUES

@run_async
def SendToAdmin(bot, update):
    bot.forwardMessage(8139296, update.message.chat_id, update.message.message_id)
    bot.sendMessage(update.message.chat_id, Answers.SendToAdmin())
    logger.info('sendToAdmin: @{0}({1}): {2}'.format(update.message.from_user.username, update.message.from_user.id, update.message.text))
    return ConversationHandler.END

@run_async
def Cancel(bot, update):
    update.message.reply_text('action canceled')
    logger.info('CANCEL: @{0}({1})'.format(update.message.from_user.username, update.message.from_user.id))
    return ConversationHandler.END
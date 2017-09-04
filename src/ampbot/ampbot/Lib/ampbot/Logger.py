# Logger.py
import logging
from Lib.Config import Parser
from telegram import Bot, ParseMode

def ConfigureLogging():
    global logger
    config = Parser.parse_ini('ampbot.ini')
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    tgChannelHandler = TgChannelHandler(config.production.logger.token, config.production.logger.channel)
    
    hdlr = logging.FileHandler('bot.log')
    hdlr.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    logger = logging.getLogger(__name__)
    logger.addHandler(hdlr)
    logger.addHandler(tgChannelHandler)
    return logger


class TgChannelHandler(logging.Handler): # Inherit from logging.Handler
        def __init__(self, botToken, channelName):
                # run the regular Handler __init__
                logging.Handler.__init__(self)
                # Our custom argument
                self.botToken = botToken
                self.channelName = channelName
                self.bot = Bot(botToken)
        def emit(self, record):
                # record.message is the log message
                self.bot.send_message(
                    self.channelName,
                    record.message,
                    parse_mode = ParseMode.MARKDOWN,
                    disable_web_page_preview = True)
                    #disable_notification = True)


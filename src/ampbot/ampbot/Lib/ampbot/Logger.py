# Logger.py
import os
import codecs
import arrow
import logging
import logging.config
from logging.handlers import *
from Lib.Config import Parser
from telegram import Bot, ParseMode, Document

config = Parser.parse_ini('ampbot.ini')
logFormat = logging.Formatter(fmt='%(asctime)s [%(levelname)s] %(filename)s (%(module)s) %(funcName)s - %(name)s => %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

def ConfigureLogger(name):
    logging.basicConfig(format='%(asctime)s [%(levelname)s] %(filename)s (%(module)s) %(funcName)s - %(name)s => %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=logging.INFO)
    logger = ConfigureHandler(logging.getLogger(name))
    return logger

def ConfigureHandler(logger):
    channel = TgChannelHandler(config.production.logger.token, config.production.logger.channel)
    channel.setLevel(logging.INFO)
    channel.setFormatter(logFormat)
    
    #timed = TgTimedRotatingFileHandler('logs/ampbot', config.production.logger.token, config.production.logger.channel, when='D', backupCount=10)
    #timed.setLevel(logging.INFO)
    #timed.setFormatter(logFormat)

    file = logging.FileHandler('ampbot.log')
    file.setLevel(logging.INFO)
    file.setFormatter(logFormat)
    
    #logger.addHandler(timed)
    logger.addHandler(file)
    logger.addHandler(channel)
    return logger
    

class TgChannelHandler(logging.Handler):
        def __init__(self, botToken, channelName):
                logging.Handler.__init__(self)
                self.botToken = botToken
                self.channelName = channelName
                self.bot = Bot(botToken)
                self.messageTemplate = '{0} - <strong>[{1}]</strong>\nFileName: {2} (Module: {3})\nFuncName: {4}\nLogger: {5}\n\nMessage:\n<pre>{6}</pre>'
        def emit(self, record):
            self.bot.send_message(chat_id=self.channelName,
                    text=str(self.messageTemplate.format(record.asctime, record.levelname, record.filename, record.module, record.funcName, record.name, record.message)),
                    parse_mode = ParseMode.HTML,
                    disable_web_page_preview = True,
                    disable_notification = True)

class TgTimedRotatingFileHandler(TimedRotatingFileHandler):
    def __init__(self, filename, botToken, channelName, fileEnding='log', when='h', interval=1, backupCount=0, encoding=None, delay=False, utc=False, atTime=None):
        TimedRotatingFileHandler.__init__(self, filename, when, interval, backupCount, encoding, delay, utc, atTime)
        self.botToken = botToken
        self.fileName = filename
        self.channelName = channelName
        self.fileEnding = fileEnding
        self.bot = Bot(botToken)

    def doRollover(self):
        local = arrow.utcnow().to('Europe/Berlin')
        self.stream.close()
        t = self.rolloverAt - self.interval
        oldFilename = self.baseFilename
        self.baseFilename = self.fileName + "_{0}.{1}".format(local.format('YYYY-MM-DD'), self.fileEnding)
        if self.encoding:
            self.stream = codecs.open(self.baseFilename, 'w', self.encoding)
        else:
            self.stream = open(self.baseFilename, 'w')
        self.rolloverAt = self.rolloverAt + self.interval
        if os.path.isfile(oldFilename):
            if os.stat(oldFilename).st_size > 0:
                with open(oldFilename, 'rb') as f:
                    self.bot.send_document(
                        chat_id=self.channelName,
                        document=f,
                        caption=oldFilename,
                        disable_notification = True)


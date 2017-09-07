"""Filter.py"""
from telegram.ext import BaseFilter
from telegram import Message

class FilterIsAdminInPrivate(BaseFilter):
    def filter(self, message):
        return message.chat.type == 'private' and message.from_user.id == 8139296 and message.reply_to_message != None

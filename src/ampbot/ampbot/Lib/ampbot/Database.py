from peewee import *
from playhouse.sqlite_ext import SqliteExtDatabase
import datetime

db = SqliteExtDatabase('ampbot.db')

class BaseModel(Model):
    class Meta:
        database = db

class User(BaseModel):
    id = BigIntegerField(unique=True)
    username = CharField()
    fistname = CharField()
    lastname = CharField()

class Tracks(BaseModel):
    user = ForeignKeyField(User, related_name='tracks')
    id = TextField()
    created_date = DateTimeField(default=datetime.datetime.now)

def before_request_handler():
    database.connect()

def after_request_handler():
    database.close()

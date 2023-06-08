from peewee import *
import datetime
from flask_login import UserMixin

DATABASE = SqliteDatabase('test.sqlite')

class User(UserMixin, Model):
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField()

    class Meta:
        database = DATABASE

class Character(Model):
    name = CharField()
    user = ForeignKeyField(User, backref='characters')

    class Meta:
        database = DATABASE

def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Character], safe=True)
    print("Connected to DB and create tables IF they don't exist")
    DATABASE.close()

from peewee import *
import os
from playhouse.db_url import connect
import datetime
# test
# test test test test
# Local 
# DATABASE = SqliteDatabase('test.sqlite')

# Added the Database URL env
DATABASE = connect(os.environ.get('DATABASE_URL') or 'sqlite:///test.sqlite')
# Connect to the database URL defined in the environment, falling
# back to a local Sqlite database if no database URL is specified.



class User( Model):
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField()

    class Meta:
        database = DATABASE

class Character(Model):
    name = CharField()
    owner = ForeignKeyField(User, backref='characters')

    class Meta:
        database = DATABASE

def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Character], safe=True)
    print("Connected to DB and create tables IF they don't exist")
    DATABASE.close()

from peewee import *
import datetime

DATABASE = SqliteDatabase('dogs.sqlite')

class User(Model):
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField()

    class Meta:
        database = DATABASE

def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User], safe=True)
    print("Connected to DB and create tables IF they don't exist")
    DATABASE.close()

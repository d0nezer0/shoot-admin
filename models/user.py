from playhouse.sqlite_ext import Model
from peewee import SQL, SmallIntegerField, DateTimeField, IntegerField, CharField, FloatField
from utils.db_util import ds_db


class User(Model):
    user_name = CharField(unique=True)

    class Meta:
        table_name = "user"
        database = ds_db

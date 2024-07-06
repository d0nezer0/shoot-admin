from playhouse.sqlite_ext import Model
from peewee import AutoField, DateTimeField, IntegerField, CharField
from utils.db_util import ds_db


class TerminalInformation(Model):
    device_code = CharField(unique=True, null=False, max_length=64)
    device_number = IntegerField(index=True)

    class Meta:
        table_name = "terminal_information"
        database = ds_db

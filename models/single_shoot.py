from playhouse.sqlite_ext import Model
from peewee import TextField, SQL, ForeignKeyField, BigIntegerField, SmallIntegerField, DateTimeField, IntegerField, CharField, FloatField
from utils.db_util import ds_db
from models.single_round import SingleRound
import json


class JSONField(TextField):
    def db_value(self, value):
        """Convert the python value for storage in the database."""
        return value if value is None else json.dumps(value)

    def python_value(self, value):
        """Convert the database value to a pythonic value."""
        return value if value is None else json.loads(value)


class SingleShoot(Model):
    single_round = ForeignKeyField(SingleRound, backref='shoot_list')
    shoot_preface = IntegerField(verbose_name="发序", default=0)
    ring = FloatField(verbose_name="环数", default=0)
    # direction = SmallIntegerField(verbose_name="方向 todo 上下左右 左上 右上... 1 2 3 4 ...", default=0)
    direction = CharField(verbose_name="方向 todo 上下左右 左上 右上...", default="1")
    time_second = IntegerField(verbose_name="用时 todo 秒", default=0)
    time_mill = IntegerField(verbose_name="时间", default=0)
    grade = IntegerField(verbose_name="成绩", default=0)
    shoot = IntegerField(verbose_name="据枪", default=0)
    collimation = IntegerField(verbose_name="瞄准", default=0)
    send = IntegerField(verbose_name="击发", default=0)
    allGrade = IntegerField(verbose_name="总体", default=0)

    class Meta:
        table_name = "single_shoot"
        database = ds_db
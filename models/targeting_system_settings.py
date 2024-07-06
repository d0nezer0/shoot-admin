from playhouse.sqlite_ext import Model
from enum import Enum
from peewee import AutoField, DateTimeField, IntegerField, TextField, CharField, SQL
from utils.db_util import ds_db


class Mode(Enum):
    FreeTraining = 0
    UnifiedTraining = 1


class UnifiedTrainStatus(Enum):
    Inited = 0
    Started = 1
    Finished = 2


class TrainSettingRecord(Model):
    code = CharField(unique=True, null=False, max_length=64)
    train_mode = IntegerField(default=0)   # 训练模式：0：自由训练；1：统一训练
    round_count = IntegerField(default=0)  # 一共几轮
    bullet_count = IntegerField(default=0)  # 子弹数量
    file_path = CharField(null=False, max_length=255)
    status = IntegerField(default=0)
    created_at = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP ")])

    class Meta:
        table_name = "train_record"
        database = ds_db

    @property
    def train_mode_desc(self):
        if self.train_mode == Mode.FreeTraining.value:
            return "自由训练"
        if self.train_mode == Mode.UnifiedTraining.value:
            return "统一训练"


# class TrainerInfo(Model):
#     train_setting_code = CharField(null=True, max_length=64)
#     trainer_name = CharField(null=False, max_length=32)
#     device_number = IntegerField()
#     current_round = IntegerField(default=0)  # 当前局id（当前轮次）
#     bullet_count = IntegerField(default=0)  # 当前子弹数量
#     status = IntegerField(default=0)  # 是否开始
#
#     class Meta:
#         table_name = "trainer_info"
#         database = ds_db
#
#     @property
#     def status_desc(self):
#         if self.status == UnifiedTrainStatus.Inited.value:
#             return "未开始"
#         if self.status == UnifiedTrainStatus.Started.value:
#             return "进行中"
#         if self.status == UnifiedTrainStatus.Finished.value:
#             return "已结束"


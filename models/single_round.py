import datetime
import sys
sys.path.append("/Users/huomeimei/zhoudong/daba")
from playhouse.sqlite_ext import Model
from peewee import SQL, SmallIntegerField, DateTimeField, IntegerField, CharField, FloatField, BooleanField, DateField
from utils.db_util import ds_db


class SingleRound(Model):
    train_record_code = CharField(null=False, max_length=64)
    bullet_count = IntegerField(default=0)  # 子弹数量
    shoot_num = IntegerField(verbose_name="人形靶左上角靶号, 对应设备号：device_number")
    shoot_mile_type = IntegerField(verbose_name="100m->1 50m->2 25m->3 距离靶", default=1)
    bout_num = IntegerField(verbose_name="局ID")
    current_seq = IntegerField(verbose_name="当前发序 todo 暂不存储 非必需", default=0, null=True)
    current_ring = FloatField(verbose_name="当前环数 todo 暂不存储 非必需", default=0, null=True)
    total_ring = FloatField(verbose_name="总环数 全部结束后统计", default=0, null=True)
    total_grade = IntegerField(verbose_name="总成绩", default=0, null=True)
    total_shoot = IntegerField(verbose_name="总据枪", default=0, null=True)
    total_collimation = IntegerField(verbose_name="总瞄准", default=0, null=True)
    total_all = IntegerField(verbose_name="总体", default=0, null=True)
    user_id = IntegerField()
    user_name = CharField(null=False, max_length=64)
    started = BooleanField(verbose_name="是否启动", default=False)
    created_at = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP ")])
    updated_date = DateField(index=True, null=True)
    updated_at = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    is_deleted = SmallIntegerField(default=0)

    class Meta:
        table_name = "single_round"
        database = ds_db

    @classmethod
    def getTrainTop10(cls, train_record_code):
        return [(round_info.user_name, round(round_info.total_ring, 1)) for round_info in SingleRound.select().where(cls.train_record_code==train_record_code).order_by(cls.total_ring.desc()).limit(10)]

    @classmethod
    def getTop10ByDate(cls, start_date, is_dict=True):
        rank_list = []
        rank_num = 0
        if is_dict:
            for round_info in SingleRound.select().where(cls.updated_date >= start_date).order_by(cls.total_ring.desc()).limit(10):
                rank_num += 1
                rank_list.append({"rank_num": rank_num, "user_name": round_info.user_name, "grade": round(round_info.total_ring, 1)})
            return rank_list
        else:
            return [(round_info.user_name, round(round_info.total_ring, 1)) for round_info in SingleRound.select().where(cls.updated_date >= start_date).order_by(cls.total_ring.desc()).limit(10)]

    @classmethod
    def get_currentDay_top10(cls, is_dict=True):
        start = datetime.date.today()
        return cls.getTop10ByDate(start, is_dict)

    @classmethod
    def get_crrentWeek_top10(cls, is_dict=True):
        start = datetime.date.today() - datetime.timedelta(days=datetime.date.today().weekday())
        return cls.getTop10ByDate(start, is_dict)

    @classmethod
    def get_currentMonth_top10(cls, is_dict=True):
        start = datetime.date(year=datetime.date.today().year, month=datetime.date.today().month, day=1)
        return cls.getTop10ByDate(start, is_dict)

    @classmethod
    def get_currentYEAR_top10(cls, is_dict=True):
        start = datetime.date(year=datetime.date.today().year, month=1, day=1)
        return cls.getTop10ByDate(start, is_dict)



if __name__ == "__main__":
    from models.single_shoot import SingleShoot
    singleRound = SingleRound.select().where(SingleRound.train_record_code == "TR_20230826111735",
                                             SingleRound.shoot_num == 1).first()

    shoot_list = SingleShoot.select().where(SingleShoot.single_round == singleRound)
    print(shoot_list.count())
    # for ss in SingleShoot.select().where(SingleShoot.single_round==singleRound):
    #     print(ss)
    # for shoot_info in singleRound.shoot_list:


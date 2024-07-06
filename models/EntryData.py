from playhouse.sqlite_ext import Model
from peewee import TextField, SQL, BigIntegerField, SmallIntegerField, BooleanField, IntegerField, CharField, \
    FloatField, ForeignKeyField
from utils.db_util import ds_db
from models.single_shoot import SingleShoot


class Entry(Model):
    single_shot = ForeignKeyField(SingleShoot, backref='entry_list')
    head = IntegerField(verbose_name="帧头", default=0)
    len = IntegerField(verbose_name="全部数据的字节长度 06->6个byte为开枪数据->没有坐标 0A->10个byte为瞄准数据->有坐标", default=0)
    t_type = IntegerField(verbose_name="根据硬件来确定，目前测试数据是7E=126 代表胸环靶", default=0)
    device_id = IntegerField(verbose_name="设备编号 第几把枪 0-255", default=0)
    cmd = IntegerField(verbose_name="命令 01->发送坐标", default=0)
    d_time = IntegerField(verbose_name="这个不是时间戳 而是-> 距离0点的毫秒数  一天有24小时==1440分钟==86400000豪秒", default=0)
    x = FloatField(verbose_name="x坐标 ", default=0)
    y = FloatField(verbose_name="y坐标", default=0)
    ring = FloatField(verbose_name="环数 有x,y 勾股定理计算所得 采取四舍五入", default=0)
    check_verify = BooleanField(verbose_name="校验 A5+0A+7E+03+01+FF+83+00+64)%FF=17", default=0)
    single_round_id = IntegerField(verbose_name="局ID", default=0)
    user_status = IntegerField(verbose_name="参考 #UserModel.userStatus", default=0)
    delete_status = BooleanField(verbose_name="note 删除状态 false 默认不删除  true删除，与历史记录查询时、排名比较时有关联", default=0)

    class Meta:
        table_name = "entry"
        database = ds_db
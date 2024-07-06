import csv
import os
from datetime import datetime
from models.terminal_information_table import TerminalInformation
from models.targeting_system_settings import TrainSettingRecord, UnifiedTrainStatus, Mode
from utils.db_util import ds_db
from models.single_round import SingleRound
from models.user import User
from admin.views import add_device


def import_device_infos(device_info_path):
    if TerminalInformation.select().count() > 0:
        return
    if not os.path.exists(device_info_path):
        raise Exception(f"{device_info_path} 不存在！")
    line_num = 0
    with open(device_info_path, "r") as f:
        with ds_db:
            csv_reader = csv.reader(f)
            for row in csv_reader:
                if line_num == 0:
                    print(row)
                else:
                    add_device(row[0], row[1])
                line_num += 1


def import_train_settings(settings_path):
    headers = ["user_name", "bullet_count", "round_count", "device_number"]
    line_num = 0
    code = f'TR_{datetime.strftime(datetime.now(), "%Y%m%d%H%M%S")}'
    round_count = 0
    bullet_count = 0
    with open(settings_path, "r") as f:
        with ds_db:
            csv_reader = csv.reader(f)
            for row in csv_reader:
                if line_num == 0:
                    print(row)
                else:
                    user_name = row[0]  # 用户名
                    if bullet_count == 0:
                        bullet_count = int(row[1])  # 子弹数量
                    elif bullet_count != int(row[1]):
                        raise Exception("每个人配置的子弹数量不一致！")

                    if round_count == 0:
                        round_count = int(row[2])  # 局数
                    elif round_count != int(row[2]):
                        raise Exception("每个人配置的局数不一致！")

                    device_number = row[3]  # 靶号
                    print(row)
                    this_user, is_new = User.get_or_create(user_name=user_name)
                    for i in range(round_count):
                        SingleRound.create(
                            train_record_code=code,
                            shoot_num=device_number,
                            bout_num=i+1,  # 局id
                            bullet_count=bullet_count,
                            user_name=this_user.user_name,
                            user_id=this_user.id
                        )
                line_num += 1
            TrainSettingRecord.create(
                code=code,
                train_mode=Mode.UnifiedTraining.value,
                round_count=round_count,
                bullet_count=bullet_count,
                file_path=settings_path,
                status=UnifiedTrainStatus.Inited.value
            )

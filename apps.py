import datetime

from flask import Flask, request, jsonify
from utils.util import http_interface_waper
from models.terminal_information_table import TerminalInformation
from models.targeting_system_settings import TrainSettingRecord
from models.single_round import SingleRound
from models.single_shoot import SingleShoot
from models.EntryData import Entry
from models.targeting_system_settings import Mode, UnifiedTrainStatus
from train_setting_manager import ts_manager


app = Flask(__name__)


@app.route("/api/fetch_ranks", methods=["GET"])
def fetch_ranks():
    return {"day":SingleRound.get_currentDay_top10(),
            "week": SingleRound.get_crrentWeek_top10(),
            "month": SingleRound.get_currentMonth_top10(),
            "year": SingleRound.get_currentYEAR_top10()}


@app.route("/api/fetch_shot_cfg/<device_code>", methods=["GET"])
def fetch_shot_config(device_code):
    """
    return 局id、用户id、用户名
    管理员不点击"开始训练" 不返回
    """
    train_record_code = ts_manager.current_train_record_code
    terminal_info = TerminalInformation.select().where(TerminalInformation.device_code == device_code)
    # print(terminal_info)
    # for t_info  in terminal_info:
    #     print(t_info)
    terminal_info = terminal_info.first()
    single_rounds = []
    if terminal_info:
        if ts_manager.mode == Mode.UnifiedTraining.value and train_record_code:
            for singleRound in SingleRound.select().where(SingleRound.train_record_code == train_record_code,
                                                          SingleRound.shoot_num==terminal_info.device_number):
                single_rounds.append({"bout_id": singleRound.id, "shoot_num": singleRound.shoot_num,
                                      "user_name": singleRound.user_name, "user_id": singleRound.user_id,
                                      "bout_num": singleRound.bout_num, "bullet_count": singleRound.bullet_count})

        ts_manager.add_connect_info(terminal_info.device_number)
    return jsonify({"single_rounds": single_rounds, "mode": ts_manager.mode,
                    "status": ts_manager.status})


def update_shot_info(data):
    single_round_id = data.get("boutId")
    # shoot_mile_type = data.get("shootMileType")
    # current_seq = data.get("currentSeq")
    # current_ring = data.get("currentRing")
    # total_ring = data.get("totalRing")
    # total_grade = data.get("totalGrade")
    # total_shoot = data.get("totalShoot")
    # total_collimation = data.get("totalCollimation")
    # total_all = data.get("totalAll")
    single_round = SingleRound.get_or_none(SingleRound.id==single_round_id)

    if single_round:
        shoot_preface = data.get("shootPreface")
        ring = data.get("ring")
        direction = data.get("direction")
        time_second = data.get("timeSecond")
        time_mill = data.get("timeMill")
        grade = data.get("grade")
        shoot = data.get("shoot")
        collimation = data.get("collimation")
        send = data.get("send")
        allGrade = data.get("allGrade")
        SingleRound.update(started=1,
                           total_grade=SingleRound.total_grade + grade,
                           total_ring=SingleRound.total_ring + ring,
                           current_seq=shoot_preface,
                           current_ring=ring,
                           updated_date=datetime.datetime.now()
                           ).where(SingleRound.id == single_round.id).execute()

        single_shot = SingleShoot.create(
            single_round=single_round,
            shoot_preface=shoot_preface,
            ring=ring,
            direction=direction,
            time_second=time_second,
            time_mill=time_mill,
            grade=grade,
            shoot=shoot,
            collimation=collimation,
            send=send,
            allGrade=allGrade
        )
        check = data.get("check", [])
        check_data = []

        for ck in check:
            check_data.append((single_shot, ck.get("head", 0), ck.get("len", 0), ck.get("type", 0),
                               ck.get("deviceID"), ck.get("cmd"), ck.get("time"), ck.get("x"), ck.get("y"),
                               ck.get("ring"), ck.get("checkVerify")))

        print(check_data)

        Entry.insert_many(check_data, fields=[Entry.single_shot, Entry.head, Entry.len,
                                              Entry.t_type, Entry.device_id,
                                              Entry.cmd, Entry.d_time, Entry.x, Entry.y,
                                              Entry.ring, Entry.check_verify]).execute()
        ts_manager.add_connect_info(single_round.shoot_num)


@app.route("/api/shot_info", methods=["POST"])
def shoot_info():
    request_data = request.json
    print(f"---------request_data:{request_data}--------------------")
    if ts_manager.mode == Mode.UnifiedTraining.value and ts_manager.status == UnifiedTrainStatus.Started.value:
        update_shot_info(request_data)
    return "success"



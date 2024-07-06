import time

import requests
from models.single_shoot import SingleShoot
from models.single_round import SingleRound
from models.EntryData import Entry
from concurrent.futures import ThreadPoolExecutor, as_completed

"""
{
    "mode": 1,
    "single_rounds": [
        {
            "bout_id": 421,
            "bout_num": 1,
            "bullet_count": 10,
            "shoot_num": 1,
            "user_id": 1,
            "user_name": "张三"
        },
        {
            "bout_id": 422,
            "bout_num": 2,
            "bullet_count": 10,
            "shoot_num": 1,
            "user_id": 1,
            "user_name": "张三"
        }
    ],
    "status": 0
}
"""
def get_current_config(device_code):
    res = requests.get(f"http://127.0.0.1:9999/api/fetch_shot_cfg/{device_code}")
    return res.json()




def sendShoots(device_code):
    round_list = None
    while True:
        res = get_current_config(device_code)
        if res.get("status") == 1:
            round_list = res.get("single_rounds")
            break

    one_single_round = SingleRound.get(SingleRound.id == 44)
    for round_cfg_info in round_list:
        for shoot_info in one_single_round.shoot_list:
            shoot_info_dict = {}
            shoot_info_dict["boutId"] = round_cfg_info["bout_id"]
            shoot_info_dict["shootPreface"] = shoot_info.shoot_preface
            shoot_info_dict["ring"] = shoot_info.ring
            shoot_info_dict["direction"] = shoot_info.direction
            shoot_info_dict["timeSecond"] = shoot_info.time_second
            shoot_info_dict["timeMill"] = shoot_info.time_mill
            shoot_info_dict["grade"] = shoot_info.grade
            shoot_info_dict["shoot"] = shoot_info.shoot
            shoot_info_dict["collimation"] = shoot_info.collimation
            shoot_info_dict["send"] = shoot_info.send
            shoot_info_dict["allGrade"] = shoot_info.allGrade
            entry_list = []
            shoot_info_dict["check"] = entry_list
            entry_obj_list = Entry.select().where(Entry.single_shot == shoot_info)
            for entry_obj in entry_obj_list:
                entry_list.append({
                    "head": entry_obj.head, "len": entry_obj.len, "type": entry_obj.t_type,
                    "deviceID": entry_obj.device_id, "cmd": entry_obj.cmd, "time": entry_obj.d_time,
                    "x": entry_obj.x, "y": entry_obj.y, "ring": entry_obj.ring,"checkVerify":entry_obj.check_verify
                })
            print(f"shoot_info_dict::::::::{shoot_info_dict}")
            requests.post("http://127.0.0.1:9999/api/shot_info", json=shoot_info_dict)
            time.sleep(2)
        time.sleep(5)

tasks = []
with ThreadPoolExecutor(max_workers=7) as executor: #
    for divice_code in ["040079368400401c02d0", "042079368400402b0610"]:
        tasks.append(
            executor.submit(
                sendShoots,
                divice_code
            ))

    for future in as_completed(tasks):
        future.result()

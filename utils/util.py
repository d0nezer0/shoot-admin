from functools import wraps
from flask import jsonify
from models.targeting_system_settings import TrainSettingRecord, UnifiedTrainStatus, Mode


def my_response(code=200, data={}, message="success"):
    return {"code": code, "data": data, "message": message}

def http_interface_waper(func):
    @wraps(func)
    def inner(*args, **kwargs):
        try:
            res = func(*args, **kwargs)
        except Exception as e:
            return jsonify(my_response(code=500, message=str(e)))
        return res

    return inner


def get_current_train_info():
    current_train_setting = TrainSettingRecord.select().order_by((TrainSettingRecord.created_at.desc())).first()
    if current_train_setting and current_train_setting.status != UnifiedTrainStatus.Finished.value:
        return {"current_train_code": current_train_setting.code, "mode": Mode.UnifiedTraining.value, "status": current_train_setting.status}
    return {"mode": Mode.FreeTraining.value}


def update_current_train_status(record_code, status):
    TrainSettingRecord.update(status=status).where(TrainSettingRecord.code == record_code).execute()



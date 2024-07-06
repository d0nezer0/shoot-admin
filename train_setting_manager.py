from utils.util import get_current_train_info, update_current_train_status
from models.targeting_system_settings import TrainSettingRecord, UnifiedTrainStatus, Mode


class TrainSettingManager(object):
    def __init__(self):
        current_train_info = get_current_train_info()
        print(f"-------------current_train_info::{current_train_info}----------------------")
        self.mode = current_train_info.get("mode")
        self.current_train_record_code = current_train_info.get("current_train_code")
        self.status = current_train_info.get("status")
        self.connect_info = {}

    def add_connect_info(self, device_number):
        self.connect_info[device_number] = True

    def update_settings(self):
        current_train_info = get_current_train_info()
        self.mode = current_train_info.get("mode")
        self.current_train_record_code = current_train_info.get("current_train_code")
        self.status = current_train_info.get("status")

    def update_status(self, unified_status: UnifiedTrainStatus):
        if not self.current_train_record_code or self.status == UnifiedTrainStatus.Finished.value:
            print(f"--record:--{self.current_train_record_code}--status:-{self.status}----------------")
        else:
            update_current_train_status(self.current_train_record_code, unified_status.value)
            self.status = unified_status.value
            # if self.status == UnifiedTrainStatus.Finished.value:
            #     self.current_train_record_code = None
            #     self.mode = Mode.FreeTraining.value

    def update_mode(self, shoot_mode: Mode):
        self.mode = shoot_mode.value



ts_manager = TrainSettingManager()
from models.terminal_information_table import TerminalInformation
from models.targeting_system_settings import Mode
from my_widgets import DeviceCell, ShotInfoCell
from models.single_round import SingleRound
from train_setting_manager import ts_manager
from models.targeting_system_settings import TrainSettingRecord, UnifiedTrainStatus, Mode


class LeftDeviceInfoManager():
    def __init__(self):
        self.device_widgets = {}
        self.is_inited = False

    def init_left_devices(self, parent):
        for device in TerminalInformation.select():
            self.device_widgets[device.device_number] = DeviceCell(parent, int(device.device_number))
        self.is_inited = True

    def refresh_devices(self, mode, train_record_code):
        if mode == Mode.FreeTraining:

            pass
        else:
            # titles = ['IP地址', '设备编号', '显示名称', '设备状态', '是否开始', '子弹数量']
            for device_num, device_widget in self.device_widgets.items():
                single_round = SingleRound.select().where(SingleRound.train_record_code == train_record_code,
                                                          SingleRound.shoot_num == device_num,
                                                          SingleRound.started==1
                                                          ).order_by(SingleRound.id.desc()).first()
                if single_round:
                    self.device_widgets[device_num].set_value(mode, single_round.user_name, single_round.started, single_round.bullet_count)


class ShootInfoCellManager():
    def __init__(self):
        self.shot_widgets = {}
        self.is_inited = False

    def init_right_shoots(self, parent):
        for device in TerminalInformation.select():
            self.shot_widgets[device.device_number] = ShotInfoCell(parent, int(device.device_number))

    def refresh_shoots(self):
        if ts_manager.mode == Mode.FreeTraining.value:
            for _, shoot_cell in self.shot_widgets.items():
                shoot_cell.reset_shot_info()
        else:
            if ts_manager.current_train_record_code:
                for device_num, shoot_cell in self.shot_widgets.items():
                    singleRoundQuery = SingleRound.select().where(SingleRound.train_record_code == ts_manager.current_train_record_code,
                                                             SingleRound.shoot_num == device_num,
                                                             # SingleRound.started==1
                                                             ).order_by(SingleRound.id.asc())

                    sigleRounds = [singleRound for singleRound in singleRoundQuery]
                    if sigleRounds:
                        shoot_cell.refresh_round_info(sigleRounds)
                        for i in range(len(sigleRounds), 0, -1):
                            if sigleRounds[i-1].started:
                                shoot_cell.refresh_shot_info(sigleRounds[i-1])
                                break
                        else:
                            shoot_cell.refresh_shot_info(None)
                        # self.shot_widgets[device_num].refresh_shot_info(Mode.UnifiedTraining.value, singleRound)
                    else:
                        shoot_cell.refresh_round_info([])
                        shoot_cell.refresh_shot_info(None)
        for device_number, connected in ts_manager.connect_info.items():
            self.shot_widgets[device_number].update_connect_stat(connected)


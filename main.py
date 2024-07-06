import os
import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from models.terminal_information_table import TerminalInformation
from models.targeting_system_settings import TrainSettingRecord, UnifiedTrainStatus, Mode
from models.single_round import SingleRound
from models.single_shoot import SingleShoot
from models.user import User
from models.EntryData import Entry


def init_db_table():
    TerminalInformation.create_table()
    TrainSettingRecord.create_table()
    SingleRound.create_table()
    SingleShoot.create_table()
    User.create_table()
    Entry.create_table()

init_db_table()

from system import Ui_MainWindow

from apps import app as web_app
from pyfladesk import ApplicationThread
from train_settings_import import import_train_settings, import_device_infos

from api import LeftDeviceInfoManager, ShootInfoCellManager
from train_setting_manager import ts_manager
from PyQt5 import QtWidgets, QtGui


class mainpage(QMainWindow, Ui_MainWindow):  # 主页面的类

    def __init__(self):  # 主界面初始化
        super().__init__()
        self.setupUi(self)
        self.sign_connect()

        self.right_shot_manager = ShootInfoCellManager()

        self.right_shot_manager.init_right_shoots(self.centralwidget)
        self.scroll_area.setWidget(self.centralwidget)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateDateTime)
        self.timer.start(1000)
        self.refresh_right()
        self.start_btn.clicked.connect(self.start_shoot)
        self.finish_btn.clicked.connect(self.finish_shoot)

        self.resize_scorll(0, 0)


    def sign_connect(self):
        self.import_btn.clicked.connect(self.openFileDialog)


    def updateDateTime(self):
        self.right_shot_manager.refresh_shoots()
        if ts_manager.current_train_record_code and ts_manager.status == UnifiedTrainStatus.Started.value:
            self.update_round_rank(SingleRound.getTrainTop10(ts_manager.current_train_record_code))


    def ziyou(self):
        if ts_manager.mode == Mode.FreeTraining.value:
            pass
        self.mode = Mode.FreeTraining.value
        message = QMessageBox()
        message.setFont(QFont("微软雅黑", 13))
        message.setWindowTitle('点击')
        message.setText("点击了自由训练按钮    ")
        message.exec_()

    def tongyi(self):
        self.mode = Mode.UnifiedTraining.value
        self.pop_msg_box("点击了统一训练按钮")

    def start_shoot(self):
        if ts_manager.mode == Mode.FreeTraining.value:
            self.pop_msg_box("自由训练中！")
            return
        if ts_manager.current_train_record_code and ts_manager.status == UnifiedTrainStatus.Inited.value:
            ts_manager.update_status(UnifiedTrainStatus.Started)
            self.pop_msg_box("开始统一训练！")
        elif ts_manager.current_train_record_code and ts_manager.status == UnifiedTrainStatus.Started.value:
            self.pop_msg_box("已经统一训练中！")
        elif not ts_manager.current_train_record_code or (ts_manager.current_train_record_code and ts_manager.status == UnifiedTrainStatus.Finished.value):
            self.pop_msg_box("请先上传统一训练配置！")

    def finish_shoot(self):
        if ts_manager.mode == Mode.FreeTraining.value:
            self.pop_msg_box("自由训练中！")
            return
        if ts_manager.current_train_record_code and ts_manager.status == UnifiedTrainStatus.Inited.value:
            self.pop_msg_box("还没有开始！")
        elif ts_manager.current_train_record_code and ts_manager.status == UnifiedTrainStatus.Started.value:
            ts_manager.update_status(UnifiedTrainStatus.Finished)
            self.pop_msg_box("已经结束训练！")
        elif not ts_manager.current_train_record_code or (ts_manager.current_train_record_code and ts_manager.status == UnifiedTrainStatus.Finished.value):
            self.pop_msg_box("没有统一训练配置！")


    def openFileDialog(self):
        if ts_manager.mode == Mode.FreeTraining.value:
            self.pop_msg_box("自由训练中！")
            return
        if ts_manager.current_train_record_code and ts_manager.status == UnifiedTrainStatus.Started.value:
            self.pop_msg_box("正在统一训练中！")
        else:
            try:
                filedialog = QFileDialog(self)
                filepath, _ = filedialog.getOpenFileName(self, '选择文件')
                if filepath:
                    import_train_settings(filepath)
                    ts_manager.update_settings()
                    self.pop_msg_box("导入成功！！！")
            except Exception as e:
                self.pop_msg_box(f"发生错误：{str(e)}， 请修改后重新导入！")

    def pop_msg_box(self, msg):
        message = QMessageBox()
        message.setFont(QFont("微软雅黑", 13))
        message.setWindowTitle('点击')
        message.setText(msg)
        message.exec_()

    def refresh_right(self):
        """
        请用下面的数据初始化"实时监控"tab页下的控件。
        :return:
        """
        self.right_shot_manager.refresh_shoots()


    def play_current_track(self, device_number):
        self.right_shot_manager.shot_widgets[device_number].play_current_track()
        print(f"----------------play_current_track:{device_number}")

    def play_history_clicked(self, device_number):
        self.right_shot_manager.shot_widgets[device_number].play_history_clicked()
        print("----------------play_history_clicked")


if __name__ == "__main__":
    import_device_infos(f"{os.getcwd()}/device_info.csv")
    qt_app = QApplication(sys.argv)
    qt_app.setStyle("fusion")
    qt_app.setAttribute(Qt.AA_EnableHighDpiScaling)

    window = mainpage()
    window.setWindowState(Qt.WindowMaximized)

    web_app_th = ApplicationThread(web_app, 9999)
    web_app_th.start()
    qt_app.aboutToQuit.connect(web_app_th.terminate)

    window.show()

    sys.exit(qt_app.exec_())

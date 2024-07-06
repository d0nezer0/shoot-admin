import math
from peewee import SQL

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPen, QPainter
from PyQt5.QtCore import QPoint, Qt, QRectF, QTimer
from PyQt5.QtWidgets import QTableWidgetItem, QVBoxLayout, QPushButton, QWidget
from models.targeting_system_settings import Mode
from models.single_round import SingleRound
from models.single_shoot import SingleShoot
from models.EntryData import Entry
from functools import partial


class DeviceCell():
    def __init__(self, parent, device_number):
        x = 130 + (device_number-1) % 2 * 440
        y = 50 + int((device_number-1)/2) * 160
        self.left = QtWidgets.QTableWidget(parent)
        self.left.setGeometry(QtCore.QRect(x, y, 181, 151))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.left.setFont(font)
        self.left.setStyleSheet("background-color: rgb(173, 181, 185);\n"
"color: rgb(170, 255, 255);")
        self.left.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.left.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.left.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.left.setRowCount(6)
        self.left.setColumnCount(1)
        self.left.setObjectName(f"table_left_{device_number}")
        self.left.horizontalHeader().setVisible(False)
        self.left.horizontalHeader().setDefaultSectionSize(180)
        self.left.horizontalHeader().setHighlightSections(True)
        self.left.horizontalHeader().setMinimumSectionSize(25)
        self.left.verticalHeader().setVisible(False)
        self.left.verticalHeader().setDefaultSectionSize(25)
        self.left.verticalHeader().setMinimumSectionSize(25)
        self.right = QtWidgets.QTableWidget(parent)
        self.right.setGeometry(QtCore.QRect(x + 180, y, 181, 151))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.right.setFont(font)
        self.right.setStyleSheet("background-color: rgb(187, 187, 187);\n"
"color: rgb(170, 255, 255);")
        self.right.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.right.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.right.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.right.setRowCount(6)
        self.right.setColumnCount(1)
        self.right.setObjectName(f"table_right_{device_number}")
        self.right.horizontalHeader().setVisible(False)
        self.right.horizontalHeader().setDefaultSectionSize(180)
        self.right.horizontalHeader().setHighlightSections(True)
        self.right.horizontalHeader().setMinimumSectionSize(25)
        self.right.verticalHeader().setVisible(False)
        self.right.verticalHeader().setDefaultSectionSize(25)
        self.right.verticalHeader().setMinimumSectionSize(25)
        titles = ['IP地址', '设备编号', '显示名称', '设备状态', '是否开始', '子弹数量']
        for index, value in enumerate(titles):
            self.left.setItem(index, 0, QTableWidgetItem(value))
        self.right.setItem(0, 0, QTableWidgetItem("192.168.1.0"))
        self.right.setItem(1, 0, QTableWidgetItem(str(device_number)))

    def set_value(self, mode, user_name, started, bout_count):
        if mode == Mode.FreeTraining.value:
            self.right.setItem(3, 0, QTableWidgetItem("自由射击"))
        else:
            self.right.setItem(3, 0, QTableWidgetItem("统一训练"))
            if started:
                self.right.setItem(4, 0, QTableWidgetItem("已开始"))
            else:
                self.right.setItem(4, 0, QTableWidgetItem("未开始"))
            self.right.setItem(2, 0, QTableWidgetItem(user_name))
            self.right.setItem(5, 0, QTableWidgetItem(str(bout_count)))


class ShotInfoCell(QtWidgets.QFrame):
    def translateui(self):
        _translate = QtCore.QCoreApplication.translate
        # self.label_8.setText(_translate("MainWindow", "胸环靶"))
        self.label_177.setText(_translate("MainWindow", "25米靶"))
        self.number_1.setText(_translate("MainWindow", str(self.device_number)))
        self.target_current_track_1.setText(_translate("MainWindow", "实时轨迹"))
        self.target_history_track_1.setText(_translate("MainWindow", "回放轨迹"))
        self.target_total_bullets_1.setText(_translate("MainWindow", "-1"))
        self.label_186.setText(_translate("MainWindow", "子弹数:"))
        self.target_number_bullets_1.setText(_translate("MainWindow", "10"))
        self.label_188.setText(_translate("MainWindow", "总发数:"))
        self.label_189.setText(_translate("MainWindow", "射击训练分析系统"))
        item = self.target_table1_1.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "局ID"))
        item = self.target_table1_1.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "名字"))
        item = self.target_table1_1.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "当前发序"))
        item = self.target_table1_1.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "当前环数"))
        item = self.target_table1_1.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "总环数"))

        item = self.target_table2_1.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "查看"))
        item = self.target_table2_1.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "发序"))
        item = self.target_table2_1.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "环数"))
        item = self.target_table2_1.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "方向"))
        item = self.target_table2_1.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "用时"))

    def __init__(self, parent, device_number):
        super().__init__(parent)
        self.device_number = device_number
        self.show_history = False
        # self = QtWidgets.QFrame(parent)
        x = 595 * math.floor((device_number-1) % 4)
        y = 265 * (math.floor((device_number-1) / 4))

        self.setGeometry(QtCore.QRect(x, y, 591, 260))
        self.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.setFrameShadow(QtWidgets.QFrame.Raised)
        self.setObjectName("frame_35")

        self.label_177 = QtWidgets.QLabel(self)
        self.label_177.setGeometry(QtCore.QRect(50, 5, 91, 21))
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(15)
        self.label_177.setFont(font)
        self.label_177.setStyleSheet("background-color: rgb(92, 135, 133);\n"
                                     "color: rgb(255, 255, 255);")
        self.label_177.setAlignment(QtCore.Qt.AlignCenter)
        self.label_177.setObjectName("label_177")

        self.label_8 = QtWidgets.QLabel(self)
        self.label_8.setGeometry(QtCore.QRect(10, 190, 171, 21))
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(15)
        self.label_8.setFont(font)
        self.label_8.setStyleSheet("color: rgb(43, 106, 77);")
        self.label_8.setAlignment(QtCore.Qt.AlignCenter)
        self.label_8.setObjectName("label_8")


        self.target_1 = QtWidgets.QLabel(self)
        # self.target_1.setGeometry(QtCore.QRect(15, 30, 161, 161))
        self.target_1.setGeometry(QtCore.QRect(5, 30, 200, 200))
        self.target_1.setStyleSheet("image: url(:/新前缀/res/ba.jpg);")
        self.target_1.setText("")
        self.target_1.setObjectName("target_1")

        self.number_1 = QtWidgets.QLabel(self)
        self.number_1.setGeometry(QtCore.QRect(180, 30, 41, 31))
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(30)
        self.number_1.setFont(font)
        self.number_1.setStyleSheet("color: rgb(92, 135, 133);")
        self.number_1.setObjectName("number_1")

        self.layout = QVBoxLayout(self)
        self.layout.setGeometry(QtCore.QRect(5, 30, 200, 200))
        self.lineWidget = DrawLine()
        self.layout.addWidget(self.lineWidget)

        self.target_current_track_1 = QtWidgets.QRadioButton(self)
        # self.target_current_track_1.setGeometry(QtCore.QRect(5, 211, 91, 16))
        self.target_current_track_1.setGeometry(QtCore.QRect(5, 241, 91, 16))
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.target_current_track_1.setFont(font)
        self.target_current_track_1.setStyleSheet("color: rgb(43, 106, 77);")
        self.target_current_track_1.setChecked(True)
        self.target_current_track_1.setObjectName("target_current_track_1")
        self.target_history_track_1 = QtWidgets.QRadioButton(self)
        self.target_history_track_1.setGeometry(QtCore.QRect(100, 241, 89, 16))
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(12)
        self.target_history_track_1.setFont(font)
        self.target_history_track_1.setStyleSheet("color: rgb(43, 106, 77);")
        self.target_history_track_1.setObjectName("target_history_track_1")
        self.target_total_bullets_1 = QtWidgets.QLabel(self)
        self.target_total_bullets_1.setGeometry(QtCore.QRect(260, 199, 31, 31))
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(15)
        self.target_total_bullets_1.setFont(font)
        self.target_total_bullets_1.setStyleSheet("color: rgb(43, 106, 77);\n"
"background-color: rgb(240, 240, 240);")
        self.target_total_bullets_1.setAlignment(QtCore.Qt.AlignCenter)
        self.target_total_bullets_1.setObjectName("target_total_bullets_1")
        self.label_186 = QtWidgets.QLabel(self)
        self.label_186.setGeometry(QtCore.QRect(325, 200, 61, 31))
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(13)
        self.label_186.setFont(font)
        self.label_186.setStyleSheet("background-color: rgb(240, 240, 240);")
        self.label_186.setAlignment(QtCore.Qt.AlignCenter)
        self.label_186.setObjectName("label_186")
        self.target_number_bullets_1 = QtWidgets.QLabel(self)
        self.target_number_bullets_1.setGeometry(QtCore.QRect(380, 200, 31, 31))
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(15)
        self.target_number_bullets_1.setFont(font)
        self.target_number_bullets_1.setStyleSheet("color: rgb(43, 106, 77);\n"
"background-color: rgb(240, 240, 240);")
        self.target_number_bullets_1.setAlignment(QtCore.Qt.AlignCenter)
        self.target_number_bullets_1.setObjectName("target_number_bullets_1")
        self.label_188 = QtWidgets.QLabel(self)
        self.label_188.setGeometry(QtCore.QRect(220, 199, 61, 31))
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(13)
        self.label_188.setFont(font)
        self.label_188.setStyleSheet("background-color: rgb(240, 240, 240);")
        self.label_188.setAlignment(QtCore.Qt.AlignCenter)
        self.label_188.setObjectName("label_188")
        self.clock_1 = QtWidgets.QLabel(self)
        self.clock_1.setGeometry(QtCore.QRect(409, 189, 161, 41))
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(12)
        self.clock_1.setFont(font)
        self.clock_1.setStyleSheet("color: rgb(43, 106, 77);\n"
"background-color: rgb(240, 240, 240);")
        self.clock_1.setText("")
        self.clock_1.setAlignment(QtCore.Qt.AlignCenter)
        self.clock_1.setObjectName("clock_1")
        self.label_189 = QtWidgets.QLabel(self)
        self.label_189.setGeometry(QtCore.QRect(220, 5, 131, 21))
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(11)
        self.label_189.setFont(font)
        self.label_189.setStyleSheet("background-color: rgb(43, 106, 77);\n"
"color: rgb(255, 255, 255);")
        self.label_189.setObjectName("label_189")
        self.target_table1_1 = QtWidgets.QTableWidget(self)
        self.target_table1_1.setGeometry(QtCore.QRect(220, 25, 351, 51))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.target_table1_1.setFont(font)
        self.target_table1_1.setStyleSheet("QHeaderView::section { \n"
"background-color: rgb(231, 245, 251);\n"
"    color: rgb(43, 106, 77);\n"
" }\n"
"\n"
"")
        self.target_table1_1.setFrameShape(QtWidgets.QFrame.Box)
        self.target_table1_1.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.target_table1_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.target_table1_1.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.target_table1_1.setRowCount(1)
        self.target_table1_1.setColumnCount(5)
        self.target_table1_1.setObjectName("target_table1_1")
        item = QtWidgets.QTableWidgetItem()
        self.target_table1_1.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.target_table1_1.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.target_table1_1.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.target_table1_1.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.target_table1_1.setHorizontalHeaderItem(4, item)
        self.target_table1_1.horizontalHeader().setVisible(True)
        self.target_table1_1.horizontalHeader().setDefaultSectionSize(70)
        self.target_table1_1.horizontalHeader().setSortIndicatorShown(False)
        self.target_table1_1.verticalHeader().setVisible(False)
        self.target_table1_1.verticalHeader().setDefaultSectionSize(27)
        self.target_table1_1.verticalHeader().setHighlightSections(True)
        self.target_table2_1 = QtWidgets.QTableWidget(self)
        self.target_table2_1.setGeometry(QtCore.QRect(220, 74, 371, 108))
        self.target_table2_1.setStyleSheet("QHeaderView::section { \n"
"background-color: rgb(231, 245, 251);\n"
"    color: rgb(43, 106, 77);\n"
" }")
        self.target_table2_1.setFrameShape(QtWidgets.QFrame.Box)
        self.target_table2_1.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.target_table2_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.target_table2_1.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.target_table2_1.setRowCount(3)
        self.target_table2_1.setColumnCount(5)
        self.target_table2_1.setObjectName("target_table2_1")
        item = QtWidgets.QTableWidgetItem()
        self.target_table2_1.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.target_table2_1.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.target_table2_1.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.target_table2_1.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.target_table2_1.setHorizontalHeaderItem(4, item)
        self.target_table2_1.horizontalHeader().setVisible(True)
        self.target_table2_1.horizontalHeader().setDefaultSectionSize(70)
        self.target_table2_1.horizontalHeader().setSortIndicatorShown(False)
        self.target_table2_1.verticalHeader().setVisible(False)
        self.target_table2_1.verticalHeader().setDefaultSectionSize(27)
        self.target_table2_1.verticalHeader().setHighlightSections(True)

        self.trace_type_group = QtWidgets.QButtonGroup(self)
        self.trace_type_group.addButton(self.target_current_track_1, 1)
        self.trace_type_group.addButton(self.target_history_track_1, 2)

        self.history_track_group = QtWidgets.QButtonGroup(self)
        self.history_button_num = 0
        self.translateui()

        self.target_current_track_1.clicked.connect(self.play_current_track)
        self.target_history_track_1.clicked.connect(self.play_history_clicked)
        self.current_single_shoot_id = -1
        self.latest_single_shoot_id = -1
        self.latest_round_id = -1

    def refresh_shot_info(self, mode, round_model_data: SingleRound=None):
        if mode == Mode.FreeTraining.value:
            pass
        if mode == Mode.UnifiedTraining.value:
            if round_model_data:
                self.latest_round_id = round_model_data.id
                latest_single_shoots = SingleShoot.select().where(
                    SingleShoot.single_round == round_model_data
                ).order_by(SQL('shoot_preface').desc()).first()
                if latest_single_shoots and self.latest_single_shoot_id == latest_single_shoots.id:
                    print("========refresh_shot_info do nothing!!!!===========================================")
                    return

                round_infos = [round_model_data.bout_num, round_model_data.user_name,
                               round_model_data.current_seq, round_model_data.current_ring,
                               round_model_data.total_ring, round_model_data.bullet_count]
                self.target_number_bullets_1.setText(str(round_model_data.bullet_count))
                for i in range(5):
                    self.target_table1_1.setItem(0, i, QTableWidgetItem(str(round_infos[i])))

                # self.target_table2_1.clear()
                single_shoots = SingleShoot.select().where(
                    SingleShoot.single_round == round_model_data
                ).order_by(SQL('shoot_preface').desc())
                print(f"========single_shoots.count()::::{single_shoots.count()}!!!!===========================================")
                self.target_table2_1.setRowCount(single_shoots.count())
                for btn in self.history_track_group.buttons():
                    self.history_track_group.removeButton(btn)
                self.history_button_num = 0
                row = 0

                for single_shoot_info in single_shoots:
                    play_button = QtWidgets.QRadioButton()
                    self.history_track_group.addButton(play_button, single_shoot_info.id)
                    self.history_button_num += 1
                    play_button.clicked.connect(partial(self.play_track, single_shoot_info))

                    if self.trace_type_group.checkedButton() == self.target_current_track_1:
                        play_button.setDisabled(True)
                        if row == 0:
                            self.current_single_shoot_id = single_shoot_info.id
                            self.latest_single_shoot_id = single_shoot_info.id
                    else:
                        play_button.setDisabled(False)

                    if self.current_single_shoot_id == single_shoot_info.id:
                        play_button.setChecked(True)


                    print(f"=====self.trace_type_group.checkedButton()::::{self.trace_type_group.checkedButton()}=====")

                    d = [play_button, single_shoot_info.shoot_preface, single_shoot_info.ring, single_shoot_info.direction, single_shoot_info.time_second]
                    for i in range(5):
                        if i == 0:
                            self.target_table2_1.setCellWidget(row, i, d[i])
                        else:
                            self.target_table2_1.setItem(row, i, QTableWidgetItem(str(d[i])))
                    row += 1
                self.play_track(self.current_single_shoot_id)

    def play_current_track(self):
        print("------------------play_current_track clicked")
        self.show_history = False
        self.refresh_button_status()
        if self.latest_single_shoot_id != -1:
            self.history_track_group.button(self.latest_single_shoot_id).setChecked(True)
            self.play_track(self.latest_single_shoot_id)



    def play_history_clicked(self):
        print("------------------play_history_clicked clicked")
        self.show_history = True
        self.refresh_button_status()

    def refresh_button_status(self):
        for i in range(self.target_table2_1.rowCount()):
            button = self.target_table2_1.cellWidget(i, 0)
            if button:
                button.setDisabled(not self.show_history)

    def play_track(self, single_shoot_id):
        # self.lineWidget.setpoints(datalist)
        print(f"------------------single_shoot_id:::{single_shoot_id}")
        try:
            single_shot_data = SingleShoot.get_by_id(single_shoot_id)
            if single_shot_data:
                entry_list = Entry.select().where(Entry.single_shot == single_shot_data)
                point_list = []
                shoot_points = []
                for entry_data in entry_list:
                    point_list.append((entry_data.y*20, entry_data.x*20))
                    if entry_data.t_type == 1:
                        shoot_points.append((entry_data.y*20, entry_data.x*20))

                self.lineWidget.set_shoot_points(shoot_points)
                print(f"------------------point_list =:::{point_list}")

                self.lineWidget.setpoints(point_list)
        except Exception as e:
            print(e)


class DrawLine(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.timer = QTimer(self)  # 更新时间戳，
        self.points = []
        self.shoot_points = []
        self.current_idx = 0
        self.width = self.width()
        self.height = self.height()
        print(f"width=========={self.width}")
        print(f"height=========={self.height}")


    def set_shoot_points(self, points):
        self.shoot_points = points


    def setpoints(self, points):
        # print(f"entering set points::::::{points}")
        self.points = points
        self.current_idx = 0
        self.timer.start(100)
        self.timer.timeout.connect(self.update)

    def draw_round(self):
        painter = QtGui.QPainter(self)  # 初始化painter
        painter.translate(96, 135)
        painter.rotate(270)
        # painter.setWindow(QtCore.QRect(15, 30, 161, 161))
        # painter.setViewport(0, 0, 161 * 4, 161 * 4)
        # painter.setViewport(QtCore.QRect(15, 30, 161 * 4, 161* 4))
        pen = QPen(Qt.red)
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setRenderHint(QPainter.Antialiasing)
        # the_points = []
        # for i in range(len(self.points)):
        #     print(f"(self.points[i][0]+i, self.points[i][1]+i):{self.points[i][0]+i}, {self.points[i][1]+i}")
        #     the_points.append(QPoint(self.points[i][0]+i, self.points[i][1]+i))

        # painter.drawPoints()
        for i in range(0, 100, 10):
            for j in range(0, 100, 10):
                painter.drawPoint(QPoint(i, j))
        radius = 20
        # rect = QtCore.QRectF(-radius, -radius, radius * 2, radius * 2)  # 扇形所在圆区域
        rect = QtCore.QRectF(-radius, -radius, radius * 2, radius * 2)  # 扇形所在圆区域
        rg = QtGui.QRadialGradient(0, 0, radius, 0, 0)
        # painter.setBrush(rg)
        ratio = 0.9
        painter.drawPie(rect, 0, 360 * 16)
        radius1 = radius + 20
        painter.drawPie(QtCore.QRectF(-radius1, -radius1, radius1 * 2, radius1 * 2), 0, 360 * 16)

        radius2 = radius1 + 20
        painter.drawPie(QtCore.QRectF(-radius2, -radius2, radius2 * 2, radius2 * 2), 0, 360 * 16)

        radius3 = radius2 + 20
        painter.drawPie(QtCore.QRectF(-radius3, -radius3, radius3 * 2, radius3 * 2), 0, 360 * 16)

        # radius4 = radius3 + 20
        # painter.drawPie(QtCore.QRectF(-radius4, -radius4, radius4 * 2, radius4 * 2), 0, 360 * 16)

        # radius5 = radius4 + 20
        # painter.drawPie(QtCore.QRectF(-radius5, -radius5, radius5 * 2, radius5 * 2), 0, 360 * 16)

    def paintEvent(self, event):
        print(f"----------event::::::{event}---------------------")
        print(self.points)
        painter = QtGui.QPainter(self)  # 初始化painter
        painter.setRenderHint(QPainter.Antialiasing)
        pen = QPen(Qt.blue)
        pen.setWidth(3)
        painter.setPen(pen)
        painter.translate(96, 135)
        painter.rotate(270)
        self.current_idx = max(min(self.current_idx+1, len(self.points) - 1), 0)
        print(f"-------------self.current_idx:{self.current_idx}-------------------")
        for i in range(self.current_idx):
            startPoint = QPoint(*self.points[i])
            endPoint = QPoint(*self.points[i + 1])
            painter.drawLine(startPoint, endPoint)

        black_pen = QPen(Qt.black)
        black_pen.setWidth(5)

        red_pen = QPen(Qt.red)
        red_pen.setWidth(3)

        if self.current_idx == max(len(self.points) - 1, 0):
            for i in range(len(self.shoot_points)):
                painter.setPen(black_pen)
                if i == len(self.shoot_points) - 1:
                    painter.setPen(red_pen)
                    painter.drawPoint(QPoint(*self.shoot_points[i]))
                else:
                    painter.drawPoint(QPoint(*self.shoot_points[i]))
            self.timer.stop()
        painter.end()




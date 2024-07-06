import enum
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


class ColorType(enum.Enum):
    RED = 0
    YELLOW = 1
    BLUE = 2


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


class ShotInfoCell():
    def translateui(self):
        _translate = QtCore.QCoreApplication.translate
        self.number_1.setText(_translate("MainWindow", str(self.device_number)))
        self.target_current_track_1.setText(_translate("MainWindow", "实时轨迹"))
        self.target_history_track_1.setText(_translate("MainWindow", "回放发序"))

    def __init__(self, parent, device_number):
        self.device_number = device_number
        self.show_history = False
        self.frame_35 = QtWidgets.QFrame(parent)
        self.width = 591
        self.height = 260
        self.connect_stat = False


        desktop = QtWidgets.QApplication.desktop()
        desktop_width = desktop.width()
        desktop_height = desktop.height()

        h_count = math.floor(desktop_width / self.width)
        h_gap = int((desktop_width % self.width)/h_count)

        x = (self.width + h_gap) * math.floor((device_number-1) % h_count)
        y = (self.height + 5) * (math.floor((device_number-1) / h_count))

        self.frame_35.setGeometry(QtCore.QRect(x, y, self.width, self.height))
        self.frame_35.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.frame_35.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_35.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_35.setObjectName("frame_35")


        self.label_8 = QtWidgets.QLabel(self.frame_35)
        self.label_8.setGeometry(QtCore.QRect(10, 190, 171, 21))
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(15)
        self.label_8.setFont(font)
        self.label_8.setStyleSheet("color: rgb(43, 106, 77);")
        self.label_8.setAlignment(QtCore.Qt.AlignCenter)
        self.label_8.setObjectName("label_8")


        self.target_1 = QtWidgets.QLabel(self.frame_35)
        self.target_1.setGeometry(QtCore.QRect(5, 30, 200, 200))
        self.target_1.setStyleSheet("image: url(:/新前缀/res/ba.jpg);")
        self.target_1.setText("")
        self.target_1.setObjectName("target_1")

        self.number_1 = QtWidgets.QLabel(self.frame_35)
        self.number_1.setGeometry(QtCore.QRect(18, 30, 41, 31))
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(30)
        self.number_1.setFont(font)
        self.number_1.setStyleSheet("color: rgb(92, 135, 133);")
        self.number_1.setObjectName("number_1")

        self.layout = QVBoxLayout(self.frame_35)
        self.layout.setGeometry(QtCore.QRect(5, 30, 200, 200))
        self.lineWidget = DrawLine()
        self.layout.addWidget(self.lineWidget)

        self.target_current_track_1 = QtWidgets.QRadioButton(self.frame_35)
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
        self.target_history_track_1 = QtWidgets.QRadioButton(self.frame_35)
        self.target_history_track_1.setGeometry(QtCore.QRect(100, 241, 89, 16))
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(12)
        self.target_history_track_1.setFont(font)
        self.target_history_track_1.setStyleSheet("color: rgb(43, 106, 77);")
        self.target_history_track_1.setObjectName("target_history_track_1")

        self.target_table1_1 = QtWidgets.QTableWidget(self.frame_35)
        self.target_table1_1.setGeometry(QtCore.QRect(220, 25, 351, 111))
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
        self.target_table1_1.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.target_table1_1.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.target_table1_1.setRowCount(3)
        self.target_table1_1.setColumnCount(6)
        self.target_table1_1.setObjectName("target_table1_1")

        self.target_table1_1.horizontalHeader().setVisible(True)
        self.target_table1_1.horizontalHeader().setDefaultSectionSize(59)
        self.target_table1_1.horizontalHeader().setSortIndicatorShown(False)
        self.target_table1_1.verticalHeader().setVisible(False)
        self.target_table1_1.verticalHeader().setDefaultSectionSize(27)
        self.target_table1_1.verticalHeader().setHighlightSections(True)
        self.target_table2_1 = QtWidgets.QTableWidget(self.frame_35)
        self.target_table2_1.setGeometry(QtCore.QRect(220, 124, 371, 108))
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

        self.target_table2_1.horizontalHeader().setVisible(True)
        self.target_table2_1.horizontalHeader().setDefaultSectionSize(70)
        self.target_table2_1.horizontalHeader().setSortIndicatorShown(False)
        self.target_table2_1.verticalHeader().setVisible(False)
        self.target_table2_1.verticalHeader().setDefaultSectionSize(27)
        self.target_table2_1.verticalHeader().setHighlightSections(True)

        self.trace_type_group = QtWidgets.QButtonGroup(self.frame_35)
        self.trace_type_group.addButton(self.target_current_track_1, 1)
        self.trace_type_group.addButton(self.target_history_track_1, 2)

        self.history_track_group = QtWidgets.QButtonGroup(self.frame_35)
        self.history_button_num = 0
        self.translateui()
        self.init_target_table1()
        self.init_target_table2()

        self.target_current_track_1.clicked.connect(self.play_current_track)
        self.target_history_track_1.clicked.connect(self.play_history_clicked)
        self.current_single_shoot_id = -1
        self.latest_single_shoot_id = -1
        self.latest_round_id = -1
        self.shoot_points = []

    def init_target_table1(self):
        self.target_table1_1.clear()
        _translate = QtCore.QCoreApplication.translate
        target_table1_headers = ["局ID", "名字", "是否开始", "当前发序", "当前环数", "总环数"]
        for i in range(len(target_table1_headers)):
            item = QtWidgets.QTableWidgetItem()
            self.target_table1_1.setHorizontalHeaderItem(i, item)
            item.setText(_translate("MainWindow", target_table1_headers[i]))

    def init_target_table2(self):
        self.target_table2_1.clear()
        _translate = QtCore.QCoreApplication.translate

        target_table2_headers = ["查看", "发序", "环数", "方向", "用时"]
        for i in range(len(target_table2_headers)):
            item = QtWidgets.QTableWidgetItem()
            self.target_table2_1.setHorizontalHeaderItem(i, item)
            item.setText(_translate("MainWindow", target_table2_headers[i]))
        self.shoot_points = []

    def reset_shot_info(self):
        self.init_target_table1()
        self.init_target_table2()
        self.lineWidget.reset_point()
        self.current_single_shoot_id = -1
        self.latest_single_shoot_id = -1
        self.latest_round_id = -1

    def refresh_round_info(self, round_list: list):
        self.init_target_table1()
        self.target_table1_1.setRowCount(len(round_list))

        if round_list:
            for idx, round_model_data in enumerate(round_list):
                self.target_table1_1.setItem(idx, 0, QTableWidgetItem(str(round_model_data.bout_num)))
                self.target_table1_1.setItem(idx, 1, QTableWidgetItem(str(round_model_data.user_name)))
                if round_model_data.started:

                    if idx+1 < len(round_list) and round_list[idx+1].started:
                        self.target_table1_1.setItem(idx, 2, QTableWidgetItem("已结束"))
                    else:
                        self.target_table1_1.setItem(idx, 2, QTableWidgetItem("进行中"))
                else:
                    self.target_table1_1.setItem(idx, 2, QTableWidgetItem("未开始"))
                self.target_table1_1.setItem(idx, 3, QTableWidgetItem(str(round_model_data.current_seq)))
                self.target_table1_1.setItem(idx, 4, QTableWidgetItem(str(round_model_data.current_ring)))
                self.target_table1_1.setItem(idx, 5, QTableWidgetItem(str(round_model_data.total_ring)))
        else:
            self.target_table1_1.clear()
            self.init_target_table1()


    def refresh_shot_info(self, round_model_data: SingleRound):
        if  not round_model_data:
            self.target_table2_1.clear()
            self.init_target_table2()
            self.latest_round_id = -1
            self.lineWidget.reset_point()
            return

        if self.latest_round_id != round_model_data.id:
            self.target_table2_1.clear()
            self.init_target_table2()
            self.latest_round_id = round_model_data.id
            self.lineWidget.reset_point()

        latest_single_shoots = SingleShoot.select().where(
            SingleShoot.single_round == round_model_data
        ).order_by(SQL('shoot_preface').desc()).first()
        if latest_single_shoots and self.latest_single_shoot_id == latest_single_shoots.id:
            # print("========refresh_shot_info do nothing!!!!===========================================")
            return

        single_shoots = SingleShoot.select().where(
            SingleShoot.single_round == round_model_data
        ).order_by(SQL('shoot_preface').desc())
        print(f"========single_shoots.count()::::{single_shoots.count()}!!!!===========================================")
        self.target_table2_1.setRowCount(single_shoots.count())
        for btn in self.history_track_group.buttons():
            self.history_track_group.removeButton(btn)

        self.history_button_num = 0
        row = 0
        shoot_points = []
        for single_shoot_info in single_shoots:
            entry_list = Entry.select().where(Entry.single_shot == single_shoot_info, Entry.t_type == 1)
            for entry_data in entry_list:
                shoot_points.insert(0, (entry_data.y*20, entry_data.x*20))

            play_button = QtWidgets.QRadioButton()
            self.history_track_group.addButton(play_button, single_shoot_info.id)
            self.history_button_num += 1
            play_button.clicked.connect(partial(self.play_track, single_shoot_info))

            if self.trace_type_group.checkedButton() == self.target_current_track_1:
                self.show_history = False
                play_button.setDisabled(True)
                if row == 0:
                    self.current_single_shoot_id = single_shoot_info.id
                    self.latest_single_shoot_id = single_shoot_info.id
            else:
                play_button.setDisabled(False)
                self.show_history = True

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
        self.lineWidget.set_shoot_points(shoot_points)
        self.lineWidget.set_show_trace(self.show_history)
        self.play_track(self.current_single_shoot_id)


    def play_current_track(self):
        print("------------------play_current_track clicked")
        self.show_history = False
        self.refresh_button_status()
        self.lineWidget.set_show_trace(self.show_history)


    def play_history_clicked(self):
        print("------------------play_history_clicked clicked")
        self.show_history = True
        self.refresh_button_status()
        self.lineWidget.set_show_trace(self.show_history)
        if self.latest_single_shoot_id != -1:
            self.history_track_group.button(self.latest_single_shoot_id).setChecked(True)
            self.play_track(self.latest_single_shoot_id)

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
                # shoot_points = []
                blue_count = 0
                for entry_data in entry_list:
                    if entry_data.t_type == 1:
                        blue_count = 5
                        range_num = min(5, len(point_list))
                        for i in range(range_num):
                            idx = i - range_num
                            point_list[idx][3] = ColorType.YELLOW
                        point_list.append([entry_data.y * 20, entry_data.x * 20,
                                           1, ColorType.BLUE])
                    else:
                        if blue_count > 0:
                            point_list.append([entry_data.y * 20, entry_data.x * 20,
                                               0, ColorType.BLUE])
                            blue_count -= 1
                        else:
                            point_list.append([entry_data.y * 20, entry_data.x * 20,
                                               0, ColorType.RED])

                    # point_list.append([entry_data.y * 20, entry_data.x * 20, 0, ColorType.RED])

                    # if entry_data.t_type == 1:
                    #     shoot_points.append((entry_data.y*20, entry_data.x*20))

                # self.lineWidget.set_shoot_points(shoot_points)
                print(f"------------------point_list =:::{point_list}")
                self.lineWidget.setpoints(point_list)
        except Exception as e:
            print(e)

    def update_connect_stat(self, connected):
        if self.connect_stat != connected:
            self.connect_stat = connected
            self.lineWidget.set_connect_stat(self.connect_stat)


class DrawLine(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.timer = QTimer(self)  # 更新时间戳，
        self.points = []
        self.shoot_points = []
        self.current_idx = 0
        self.width = self.width()
        self.height = self.height()
        self.show_trace = False
        self.connect_stat = False
        print(f"width=========={self.width}")
        print(f"height=========={self.height}")

    def set_connect_stat(self, connect_stat):
        if connect_stat != self.connect_stat:
            self.connect_stat = connect_stat
            self.update()

    def set_show_trace(self, show_trace):
        self.show_trace = show_trace
        self.update()

    def set_shoot_points(self, points):
        self.shoot_points = points


    def setpoints(self, points):
        # print(f"entering set points::::::{points}")
        self.points = points
        self.current_idx = 0
        self.timer.stop()
        self.timer.start(100)
        self.timer.timeout.connect(self.update)

    def reset_point(self):
        self.points = []
        self.shoot_points = []
        self.update()

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
        # print(f"----------event::::::{event}---------------------")
        # print(self.points)
        painter = QtGui.QPainter(self)  # 初始化painter
        painter.setRenderHint(QPainter.Antialiasing)
        pen = QPen(Qt.blue)
        pen.setWidth(3)
        painter.setPen(pen)
        painter.translate(96, 135)
        painter.rotate(270)
        red_pen = QPen(Qt.red, 10, Qt.SolidLine, Qt.RoundCap)
        small_red_pen = QPen(Qt.red, 2, Qt.SolidLine, Qt.RoundCap)
        blue_pen = QPen(Qt.blue, 2, Qt.SolidLine, Qt.RoundCap)
        green_pen = QPen(Qt.green, 10, Qt.SolidLine, Qt.RoundCap)
        yellow_pen = QPen(Qt.yellow, 2, Qt.SolidLine, Qt.RoundCap)

        if self.show_trace:
            self.current_idx = max(min(self.current_idx + 1, len(self.points) - 1), 0)
            print(f"-------------self.current_idx:{self.current_idx}-------------------")
            for i in range(self.current_idx):
                from_point = self.points[i]
                to_point = self.points[i+1]
                startPoint = QPoint(from_point[0], from_point[1])
                endPoint = QPoint(to_point[0], to_point[1])
                if from_point[3] == ColorType.BLUE:
                    painter.setPen(blue_pen)
                elif from_point[3] == ColorType.RED:
                    painter.setPen(small_red_pen)
                elif from_point[3] == ColorType.YELLOW:
                    painter.setPen(yellow_pen)
                painter.drawLine(startPoint, endPoint)
                if from_point[2] == 1:
                    painter.setPen(QPen(Qt.red, 5, Qt.SolidLine, Qt.RoundCap))
                    painter.drawPoint(QPoint(from_point[0], from_point[1]))

            if self.current_idx == max(len(self.points) - 1, 0):
                # for i in range(len(self.shoot_points)):
                #     painter.setPen(black_pen)
                #     if i == len(self.shoot_points) - 1:
                #         painter.setPen(red_pen)
                #         painter.drawPoint(QPoint(*self.shoot_points[i]))
                #     else:
                #         painter.drawPoint(QPoint(*self.shoot_points[i]))
                self.timer.stop()
        else:
            black_pen = QPen(Qt.black, 15, Qt.SolidLine, Qt.RoundCap)
            black_pen.setWidth(10)

            red_pen = QPen(Qt.red, 15, Qt.SolidLine, Qt.RoundCap)
            red_pen.setWidth(10)
            for i in range(len(self.shoot_points)):
                painter.setPen(black_pen)
                if i == len(self.shoot_points) - 1:
                    painter.setPen(red_pen)
                    painter.drawPoint(QPoint(*self.shoot_points[i]))
                    # painter.drawPie(QtCore.QRectF(self.shoot_points[i][0], self.shoot_points[i][1], 10 * 2, 10 * 2), 0, 360 * 16)
                else:
                    painter.drawPoint(QPoint(*self.shoot_points[i]))
            self.timer.stop()

        if self.connect_stat:
            painter.setPen(green_pen)
        else:
            painter.setPen(red_pen)

        painter.drawPoint(QPoint(90, 80))

        painter.end()


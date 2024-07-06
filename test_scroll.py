import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class Ui_Form(QMainWindow):
    def __init__(self):
        # 初始化继承父类(QMainWindow)
        super(Ui_Form, self).__init__()
        # 获取屏幕大小
        self.desktop = QApplication.desktop()
        self.height = self.desktop.height()
        self.width = self.desktop.width()

        # 设置窗口大小，并显示在屏幕中间
        self.resize(int(self.width * 0.5), int(self.height * 0.65))
        self.setWindowTitle("合成gif")
        self.setWindowIcon(QIcon(':/pic/aehvi-0m7h6-001.ico'))

        self.set_center()
        self.initUI()

    def set_center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()  # desktop的availableGeometry()获取可用位置和尺寸（除去任务栏等）
        qr.moveCenter(cp)
        self.move(qr.topLeft())


    def initUI(self):
        # 滚动区域，存放图片
        self.scroll_area = QScrollArea(self)
        self.scroll_area_contentwidget = QWidget(self)
        self.gridLayout = QGridLayout(self.scroll_area_contentwidget)
        self.scroll_area.setWidget(self.scroll_area_contentwidget)
        # 设置滚动区域的位置和大小
        self.scroll_area.setGeometry(10, 10, int(self.width*0.5-20), int(self.height*0.6/3*2))

        # scroll_area_palette = self.scroll_area.palette()  # 获取已有的调色板
        # scroll_area_palette.setColor(QPalette.Window, Qt.white)  # 修改背景色为白色
        # self.scroll_area.setPalette(scroll_area_palette)  # 为组件设置调色板
        # self.scroll_area.setAutoFillBackground(True)  # 组件生效调色板
        # 添加两个按钮
        self.btnwidget = QWidget(self)
        self.btnwidget.setGeometry(QRect(10, int(self.height * 0.6 / 3 * 2) + 20, 211, 50))  # 按钮控件布局及大小

        self.hlayout_btn = QHBoxLayout(self.btnwidget)  # 加水平布局
        self.hlayout_btn.setSpacing(10)  # 水平布局中控件的间隔

        # 添加文件按钮
        self.add_file_btn = QPushButton('添加文件', self.btnwidget)
        self.add_file_btn.setMaximumSize(QSize(113, 38))  # 设置按钮大小
        self.add_file_btn.setIcon(QIcon(':/pic/add.png'))  # 按钮添加图片
        self.add_file_btn.setStyleSheet("border-radius:10px;border:1px groove gray;")  # 设置按钮样式
        self.add_file_btn.setCursor(Qt.PointingHandCursor)  # 鼠标移入显示手型

        self.empty_btn = QPushButton('清空列表', self.btnwidget)
        self.empty_btn.setMaximumSize(QSize(113, 38))
        self.empty_btn.setIcon(QIcon(':/pic/cal.png'))
        self.empty_btn.setStyleSheet("border-radius:10px;border:1px groove gray;")
        self.empty_btn.setCursor(Qt.PointingHandCursor)
        self.empty_btn.setEnabled(False)  # 设置按钮不可用

        # 水平布局加入按钮
        self.hlayout_btn.addWidget(self.add_file_btn)
        self.hlayout_btn.addWidget(self.empty_btn)

        # self.hlayout_btn.addWidget(self.label_out)
        # self.hlayout_btn.addWidget(self.radio_btn1)
        # self.hlayout_btn.addWidget(self.radio_btn2)
        # self.hlayout_btn.addWidget(self.custom_edit)
        # self.hlayout_btn.addWidget(self.custom_btn)
        self.hlayout_btn.addStretch()  # 设置拉伸

        # self.hlayout_duration = QHBoxLayout(self.switchDuration)
        pDoubleValidator = QDoubleValidator() # 数值校验器，只能输入数字
        pDoubleValidator.setRange(0, 100) # 输入数值范围
        pDoubleValidator.setNotation(QDoubleValidator.StandardNotation)
        pDoubleValidator.setDecimals(1)  # 输入精度位
        # self.duration_edit.setValidator(pDoubleValidator)  # 文本输入框加入校验器

        self.com_btn = QPushButton('合成gif', self)
        self.com_btn.setStyleSheet("background-color: rgb(170, 170, 255);color: white;"
                                   "border-radius: 10px;  border: 2px groove gray;")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Ui_Form()
    window.show()
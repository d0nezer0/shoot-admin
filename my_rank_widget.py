from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem

# CSS样式表
LEADERBOARD_STYLE = """
QTableWidget {
    font-size: 16px;
    padding: 5px;
}

#rank1, #rank2, #rank3 {
    font-weight: bold;
    color: red;
}

#title {
    font-size: 20px;
    font-weight: bold;
    padding-bottom: 10px;
}
"""


class LeaderboardWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.setGeometry(QRect(10, 10, 330, 400))
        # 设置样式表
        self.setStyleSheet(LEADERBOARD_STYLE)

        self.layout = QVBoxLayout()

        # 添加标题
        self.title_label = QLabel("统一训练排行榜")
        self.title_label.setObjectName("title")
        self.layout.addWidget(self.title_label)

        # 创建表格控件
        self.table = QTableWidget()
        self.table.verticalHeader().setVisible(False)
        # 设置表格列数
        self.table.setColumnCount(3)
        # 设置表格行数
        self.table.setRowCount(10)
        # 设置表头
        self.table.setHorizontalHeaderLabels(["排名", "名字", "成绩"])
        self.layout.addWidget(self.table)
        self.setLayout(self.layout)

    def update_rank(self, leaderboard_data):
        self.table.clear()
        # 设置表格列数
        self.table.setColumnCount(3)
        # 设置表格行数
        self.table.setRowCount(len(leaderboard_data))

        # 设置表头
        self.table.setHorizontalHeaderLabels(["排名", "名字", "成绩"])
        self.table.verticalHeader().setVisible(False)
        # 填充表格数据
        for row, (player, score) in enumerate(leaderboard_data, start=1):
            rank_item = QTableWidgetItem(str(row))
            player_item = QTableWidgetItem(player)
            score_item = QTableWidgetItem(str(score))

            # if row <= 3:
            #     rank_item.setFont(QFont("Arial", 12, QFont.Bold))
            #     player_item.setFont(QFont("Arial", 12, QFont.Bold))
            #     score_item.setFont(QFont("Arial", 12, QFont.Bold))

            self.table.setItem(row - 1, 0, rank_item)
            self.table.setItem(row - 1, 1, player_item)
            self.table.setItem(row - 1, 2, score_item)


if __name__ == "__main__":
    leaderboard_data = [("Player 1", 100), ("Player 2", 90), ("Player 3", 80), ("Player 4", 70), ("Player 5", 60)]

    app = QApplication([])

    widget = LeaderboardWidget(leaderboard_data)
    widget.show()

    app.exec_()
from PyQt5.QtCore import Qt
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
    def __init__(self, leaderboard_data):
        super().__init__()
        self.setWindowTitle("Leaderboard")

        # 设置样式表
        self.setStyleSheet(LEADERBOARD_STYLE)

        self.layout = QVBoxLayout()

        # 添加标题
        title_label = QLabel("Leaderboard")
        title_label.setObjectName("title")
        self.layout.addWidget(title_label)

        # 创建表格控件
        table = QTableWidget()

        # 设置表格列数
        table.setColumnCount(3)

        # 设置表格行数
        table.setRowCount(len(leaderboard_data))

        # 设置表头
        table.setHorizontalHeaderLabels(["Rank", "Player", "Score"])

        # 填充表格数据
        for row, (player, score) in enumerate(leaderboard_data, start=1):
            rank_item = QTableWidgetItem(str(row))
            player_item = QTableWidgetItem(player)
            score_item = QTableWidgetItem(str(score))

            if row <= 3:
                rank_item.setFont(QFont("Arial", 12, QFont.Bold))
                player_item.setFont(QFont("Arial", 12, QFont.Bold))
                score_item.setFont(QFont("Arial", 12, QFont.Bold))

            table.setItem(row - 1, 0, rank_item)
            table.setItem(row - 1, 1, player_item)
            table.setItem(row - 1, 2, score_item)

        self.layout.addWidget(table)

        self.setLayout(self.layout)


if __name__ == "__main__":
    leaderboard_data = [("Player 1", 100), ("Player 2", 90), ("Player 3", 80), ("Player 4", 70), ("Player 5", 60)]

    app = QApplication([])

    widget = LeaderboardWidget(leaderboard_data)
    widget.show()

    app.exec_()
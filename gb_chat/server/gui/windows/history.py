from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QTableView, QPushButton


class History(QDialog):
    def __init__(self):
        super().__init__()
        self.exit = None
        self.history = None
        self.init()

    def init(self):
        # Настройки окна:
        self.setWindowTitle('Статистика клиентов')
        self.setFixedSize(600, 700)
        self.setAttribute(Qt.WA_DeleteOnClose)

        # Кнапка закрытия окна
        self.exit = QPushButton('Закрыть', self)
        self.exit.move(250, 650)
        self.exit.clicked.connect(self.close)

        # Лист с собственно историей
        self.history = QTableView(self)
        self.history.move(10, 10)
        self.history.setFixedSize(580, 620)

        self.show()

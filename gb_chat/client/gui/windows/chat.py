from PyQt5.QtCore import QRect, Qt
from PyQt5.QtGui import QStandardItemModel, QBrush, QColor, QStandardItem
from PyQt5.QtWidgets import QDialog, QPushButton, QApplication, QLabel, QTextEdit, QListView, qApp


class Chat(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("gb_chat")
        self.setFixedSize(756, 534)

        self.refresh = QPushButton("Обновить", self)
        self.refresh.setGeometry(QRect(10, 450, 251, 31))

        self.message = QTextEdit(self)
        self.message.setGeometry(QRect(290, 420, 451, 61))

        self.label_message = QLabel("Введите новое сообщение:", self)
        self.label_message.setGeometry(QRect(290, 400, 171, 16))

        self._contacts = QListView(self)
        self._contacts.setGeometry(QRect(10, 20, 251, 431))
        self.contacts = QStandardItemModel()
        self._contacts.setModel(self.contacts)

        self.login = QPushButton("Авторизоваться", self)
        self.login.setGeometry(QRect(10, 480, 251, 31))

        self._messages = QListView(self)
        self._messages.setGeometry(QRect(290, 30, 451, 371))
        self._messages.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self._messages.setWordWrap(True)
        self.messages = QStandardItemModel()
        self._messages.setModel(self.messages)

        self.label_contacts = QLabel("Список присутствующих в чате", self)
        self.label_contacts.setGeometry(QRect(10, 0, 171, 16))

        self.send = QPushButton("Отправить сообщение", self)
        self.send.setGeometry(QRect(290, 480, 451, 31))

        self.close = QPushButton("Покинуть чат", self)
        self.close.setGeometry(QRect(290, 0, 451, 31))
        self.close.clicked.connect(qApp.exit)


if __name__ == '__main__':
    app = QApplication([])
    dial = Chat()
    row = QStandardItem("sss")
    row.setEditable(False)
    dial.contacts.appendRow(row)
    dial.show()
    app.exec_()

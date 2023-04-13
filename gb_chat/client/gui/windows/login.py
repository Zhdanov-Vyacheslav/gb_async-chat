from PyQt5.QtWidgets import QDialog, QPushButton, QLineEdit, QApplication, QLabel, qApp


class Login(QDialog):
    def __init__(self):
        super().__init__()

        self.login = None

        self.setWindowTitle("gb_chat")
        self.setFixedSize(250, 90)

        self.label = QLabel("Введите имя пользователя:", self)
        self.label.move(50, 10)
        self.label.setFixedSize(150, 10)

        self._login = QLineEdit(self)
        self._login.setFixedSize(150, 20)
        self._login.move(50, 30)

        self.ok = QPushButton("Присоединиться", self)
        self.ok.setFixedSize(100, 25)
        self.ok.move(10, 60)
        self.ok.clicked.connect(self.click)

        self.cancel = QPushButton("Выход", self)
        self.cancel.setFixedSize(100, 25)
        self.cancel.move(140, 60)
        self.cancel.clicked.connect(qApp.exit)

    def click(self):
        if self._login.text():
            self.login = self._login.text()
            qApp.exit()


if __name__ == '__main__':
    app = QApplication([])
    dial = Login()
    dial.show()
    app.exec_()

from PyQt5.QtWidgets import QDialog, QPushButton, QLineEdit, QApplication, QLabel, qApp


class Login(QDialog):
    def __init__(self):
        super().__init__()

        self.login = None
        self.password = None

        self.setWindowTitle("gb_chat")
        self.setFixedSize(250, 150)

        self.label = QLabel("Введите имя пользователя:", self)
        self.label.move(50, 10)
        self.label.setFixedSize(150, 10)

        self._login = QLineEdit(self)
        self._login.setFixedSize(150, 20)
        self._login.move(50, 30)

        self._login = QLineEdit(self)
        self._login.setFixedSize(150, 20)
        self._login.move(50, 30)

        self.label_pass = QLabel("Введите пароль:", self)
        self.label_pass.move(50, 60)
        self.label_pass.setFixedSize(150, 10)

        self._password = QLineEdit(self)
        self._password.setFixedSize(150, 20)
        self._password.move(50, 80)

        self.ok = QPushButton("Присоединиться", self)
        self.ok.setFixedSize(100, 25)
        self.ok.move(10, 120)
        self.ok.clicked.connect(self.click)

        self.cancel = QPushButton("Выход", self)
        self.cancel.setFixedSize(100, 25)
        self.cancel.move(140, 120)
        self.cancel.clicked.connect(qApp.exit)

    def click(self):
        if self._login.text():
            self.login = self._login.text()
            self.password = self._password.text()
            qApp.exit()


if __name__ == '__main__':
    app = QApplication([])
    dial = Login()
    dial.show()
    app.exec_()

from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QFileDialog, QPushButton


class Setting(QDialog):
    def __init__(self):
        super().__init__()
        self.ip_label = None
        self.ip = None
        self.port = None
        self.port_label = None
        self.path_label = None
        self.path = None
        self.path_select = None
        self.file_label = None
        self.file = None
        self.save = None
        self.exit = None

        self.init()

    def init(self):
        # Настройки окна
        self.setFixedSize(365, 260)
        self.setWindowTitle("Настройки сервера")

        # Надпись о файле базы данных:
        self.path_label = QLabel("Путь до файла базы данных: ", self)
        self.path_label.move(10, 10)
        self.path_label.setFixedSize(240, 15)

        # Строка с путём базы
        self.path = QLineEdit(self)
        self.path.setFixedSize(250, 20)
        self.path.move(10, 30)
        self.path.setReadOnly(True)

        # Кнопка выбора пути.
        self.path_select = QPushButton("Обзор...", self)
        self.path_select.move(275, 28)

        # Функция обработчик открытия окна выбора папки
        def open_file_dialog():
            dialog = QFileDialog(self)
            path = dialog.getExistingDirectory()
            path = path.replace('/', '\\')
            self.path.insert(path)

        self.path_select.clicked.connect(open_file_dialog)

        self.file_label = QLabel("Имя файла базы данных: ", self)
        self.file_label.move(10, 68)
        self.file_label.setFixedSize(180, 15)

        self.file = QLineEdit(self)
        self.file.move(200, 66)
        self.file.setFixedSize(150, 20)

        self.port_label = QLabel('Номер порта для соединений:', self)
        self.port_label.move(10, 108)
        self.port_label.setFixedSize(180, 15)

        # Поле для ввода номера порта
        self.port = QLineEdit(self)
        self.port.move(200, 108)
        self.port.setFixedSize(150, 20)

        # Метка с адресом для соединений
        self.ip_label = QLabel('С какого IP принимаем соединения:', self)
        self.ip_label.move(10, 148)
        self.ip_label.setFixedSize(180, 15)

        # Поле для ввода ip
        self.ip = QLineEdit(self)
        self.ip.move(200, 148)
        self.ip.setFixedSize(150, 20)

        self.save = QPushButton("Сохранить", self)
        self.save.move(190, 220)

        self.exit = QPushButton("Закрыть", self)
        self.exit.move(275, 220)
        self.exit.clicked.connect(self.close)

        self.show()

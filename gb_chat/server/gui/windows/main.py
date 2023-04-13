from PyQt5.QtWidgets import QMainWindow, QAction, qApp, QLabel, QTableView


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        # Кнопки
        self.refresh = QAction("Обновить список", self)
        self.config = QAction("Настройки сервера", self)
        self.history = QAction("История клиентов", self)
        self.restart = QAction("Перезагрузка сервера", self)
        self.exit = QAction("Выход", self)
        # Прочие объекты
        self.toolbar = None
        self.label = None
        self.clients = None
        # Инициализация форматирование и отображения
        self.init()

    def init(self):
        # Кнопка выхода
        self.exit.setShortcut("Ctrl+Q")
        self.exit.triggered.connect(qApp.quit)

        # Статусбар
        self.statusBar()

        # Тулбар
        self.toolbar = self.addToolBar("MainBar")
        self.toolbar.addAction(self.exit)
        self.toolbar.addAction(self.refresh_button)
        self.toolbar.addAction(self.show_history_button)
        self.toolbar.addAction(self.config_btn)

        # Настройки геометрии основного окна
        self.setFixedSize(800, 600)
        self.setWindowTitle("Messaging Server alpha release")

        # Надпись о том, что ниже список подключённых клиентов
        self.label = QLabel("Список подключённых клиентов:", self)
        self.label.setFixedSize(240, 15)
        self.label.move(10, 25)

        # Окно со списком подключённых клиентов.
        self.clients = QTableView(self)
        self.clients.move(10, 45)
        self.clients.setFixedSize(780, 400)

        # Отображаем окно.
        self.show()

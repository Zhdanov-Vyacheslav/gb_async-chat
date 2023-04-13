import os
import sys
from threading import Lock

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QMessageBox

from gb_chat.server import ChatServer, logger
from gb_chat.server.gui.models import clients, contacts
from gb_chat.server.gui.windows import Main, Setting, History
from gb_chat.storage.server import ServerDB

LOCK = Lock()


class GUIChatServer:
    def __init__(self, config):
        self.__config = config
        self.db = None
        self.path = None
        self.__server = None

    def run(self):
        config = self.__config
        self.__server = ChatServer(config)
        logger.info("Server rdy")
        self.__server.daemon = True
        self.__server.start()

        db = ServerDB(os.path.join(config["db"]["path"], config["db"]["name"]))

        server_app = QApplication(sys.argv)
        main = Main()

        # Инициализируем параметры в окна
        main.statusBar().showMessage('Server Working')
        # main.active_clients_table.setModel(clients(db))
        # main.active_clients_table.resizeColumnsToContents()
        # main.active_clients_table.resizeRowsToContents()

        # Функция обновляющяя список подключённых, проверяет флаг подключения, и
        # если надо обновляет список
        # def list_update():
        #     global new_connection
        #     if new_connection:
        #         main.active_clients_table.setModel(
        #             clients(db))
        #         main.active_clients_table.resizeColumnsToContents()
        #         main.active_clients_table.resizeRowsToContents()
        #         with LOCK:
        #             new_connection = False

        # Функция создающяя окно со статистикой клиентов
        # def show_statistics():
        #     global stat_window
        #     stat_window = History()
        #     stat_window.history.setModel(contacts(db))
        #     stat_window.history.resizeColumnsToContents()
        #     stat_window.history.resizeRowsToContents()
        #     stat_window.show()

        # Функция создающяя окно с настройками сервера.
        def server_config():
            global config_window
            # Создаём окно и заносим в него текущие параметры
            config_window = Setting()
            config_window.path.insert(config["db"]["path"])
            config_window.file.insert(config["db"]["name"])
            config_window.port.insert(config["DEFAULT_PORT"])
            config_window.ip.insert(config["DEFAULT_ADDRESS"])
            config_window.save.clicked.connect(save_server_config)

        # Функция сохранения настроек
        def save_server_config():
            global config_window
            message = QMessageBox()
            config["db"]["path"] = config_window.path.text()
            config["db"]["name"] = config_window.file.text()
            try:
                port = int(config_window.port.text())
            except ValueError:
                message.warning(config_window, 'Ошибка', 'Порт должен быть числом')
            else:
                config["DEFAULT_ADDRESS"] = config_window.ip.text()
                if 1023 < port < 65536:
                    config["DEFAULT_PORT"] = str(port)
                    print(port)
                    with open('server.ini', 'w') as conf:
                        config.write(conf)
                        message.information(
                            config_window, 'OK', 'Настройки успешно сохранены!')
                else:
                    message.warning(
                        config_window,
                        'Ошибка',
                        'Порт должен быть от 1024 до 65536')

        # Таймер, обновляющий список клиентов 1 раз в секунду
        # timer = QTimer()
        # timer.timeout.connect(list_update)
        # timer.start(1000)

        # Связываем кнопки с процедурами
        # main.refresh.triggered.connect(list_update)
        # main.history.triggered.connect(show_statistics)
        main.config.triggered.connect(server_config)

        # Запускаем GUI
        server_app.exec_()


if __name__ == '__main__':
    pass
    # main()

import traceback
from json import JSONDecodeError

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItem, QBrush, QColor
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from jsonschema.exceptions import ValidationError

from gb_chat.client import logger, ChatClient
from gb_chat.client.gui import Chat
from gb_chat.tools.requests import request_msg


class ClientMainWindow(QMainWindow):
    def __init__(self, client: ChatClient):
        super().__init__()

        self.recipient = None
        self.user = client.account["login"]
        self.room = "#server"
        self.db = client.db
        self.client = client

        self.messages = QMessageBox()

        self.chat = Chat()
        self.chat.send.clicked.connect(self.send_message)
        self.chat.login.clicked.connect(self.login)
        self.chat.refresh.clicked.connect(self.refresh_clients)
        self.chat._contacts.doubleClicked.connect(self.select_recipient)

        self.refresh_clients()
        self.set_disabled_input()

    def set_disabled_input(self):
        # Блокируем доступ к списку контактов если данный пользователь должен авторизовать
        if not self.client.is_connected:
            self.chat._contacts.setDisabled(True)
        self.chat.message.setText("Не выбран получатель. (Двойной клик по участнику чата)")
        self.chat.message.setDisabled(True)
        self.chat.send.setDisabled(True)

    def select_recipient(self):
        if self.recipient is None:
            self.set_active()
        self.recipient = self.chat._contacts.currentIndex().data()

    def set_active(self):
        self.chat.message.clear()
        self.chat.send.setDisabled(False)
        self.chat.message.setDisabled(False)

    def login(self):
        self.client.login()

    def refresh_clients(self):
        self.chat.contacts.clear()
        row = QStandardItem(self.room)
        row.setEditable(False)
        self.chat.contacts.appendRow(row)
        for contact in sorted(self.db.Contacts.get_contacts(self.client.session)):
            row = QStandardItem(contact)
            row.setEditable(False)
            self.chat.contacts.appendRow(row)

    def send_message(self):
        message_text = self.chat.message.toPlainText()
        self.chat.message.clear()
        msg = request_msg(
            sender=self.user,
            to=self.recipient,
            message=message_text,
            encoding=self.client.encoding
        )
        if self.recipient[0] != "#":
            self.message(msg)
        if message_text:
            try:
                self.client.send_data(data=msg)
            except (OSError, ConnectionResetError, ConnectionAbortedError):
                self.messages.critical(self, "Ошибка", "Потеряно соединение с сервером!")
                self.close()
                self.database.save_message(self.current_chat, 'out', message_text)
                logger.debug(f'Отправлено сообщение для {self.current_chat}: {message_text}')
                self.history_list_update()

    def receiver(self):
        while True:
            try:
                data = self.client.get_data()
                logger.debug("Received: {}".format(data))
                if "action" in data:
                    if self.client.validator.validate_data("action", data):
                        msg = self.client.action(data)
                        if msg is not None:
                            self.message(msg)
                else:
                    if "response" in data:
                        msg = self.client.responses(data)
                        if msg is not None:
                            self.message({
                                "from": "System",
                                "to": self.user,
                                "message": msg
                            })
                        if data["response"] == 203:
                            self.chat.login.setDisabled(True)
                            self.chat._contacts.setDisabled(False)
            except (JSONDecodeError, ValidationError) as e:
                logger.error(str(e))
            except (OSError, ConnectionError, ConnectionAbortedError, ConnectionResetError) as ex:
                self.message({
                    "from": "System",
                    "to": self.user,
                    "message": "Соединение с сервером, разорвано"
                })
                logger.critical(ex.with_traceback(traceback.print_exc()), exc_info=True)
                break

    def message(self, message: dict):
        msg = QStandardItem("{sender} -> {to}: {msg}".format(
            sender=message["from"], to=message["to"], msg=message["message"]))
        msg.setEditable(False)
        # Выделяем цветом свои сообщения
        if self.user == message["from"]:
            msg.setBackground(QBrush(QColor(204, 255, 204)))
        # Выделяем цветом приватное сообщение
        elif self.user == message["to"]:
            msg.setBackground(QBrush(QColor(255, 213, 213)))
        msg.setTextAlignment(Qt.AlignLeft)
        self.chat.messages.appendRow(msg)


# if __name__ == '__main__':
#     app = QApplication([])
#     dial = ClientMainWindow()
#     dial.show()
#     app.exec_()

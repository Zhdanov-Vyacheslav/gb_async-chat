import os
import sys
from threading import Lock, Thread, Event

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QMessageBox
from gb_chat.client import ChatClient, logger
from gb_chat.client.gui.windows import Login, Chat
from gb_chat.client.gui.windows.main import ClientMainWindow

LOCK = Lock()
EVENT = Event()


class GUIChatClient:
    def __init__(self, client: ChatClient):
        self.app = None
        self.__client = client

    def login(self):
        msg = None
        login = Login()
        login._login.setText(self.__client.account["login"])
        login.show()
        self.app.exec_()
        if login.login:
            self.__client.account = {"login": login.login, "password": login.password}
            del login
            msg = self.__client.connect()
        else:
            exit(0)
        return msg

    def run(self):
        self.app = QApplication([])
        msg = self.login()
        self.__client.db.Contacts.refresh([], session=1)
        main = ClientMainWindow(self.__client)
        if msg is not None:
            main.message({
                "from": "Server",
                "to": self.__client.account["login"],
                "message": msg
            })
        receiver = Thread(target=main.receiver)
        receiver.daemon = True
        receiver.start()
        self.__client.get_contacts()
        timer = QTimer()
        timer.timeout.connect(self.__client.get_contacts)
        timer.start(1000*10)
        main.chat.show()
        self.app.exec_()


if __name__ == '__main__':
    pass
    # main()

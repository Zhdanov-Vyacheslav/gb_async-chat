import json
import sys
import time
import traceback
from datetime import datetime
from json import JSONDecodeError
from socket import SOCK_STREAM, AF_INET, socket
from threading import Thread, Lock
from typing import Optional

from gb_chat.tools.responses import RESPONSE
from jsonschema.exceptions import ValidationError

from .logger import logger
from gb_chat.tools.validator import Validator
from gb_chat.tools.requests import request_msg, request_presence, request_quit, request_get_contacts, \
    request_authenticate
from gb_chat.metaclass import ClientVerifier
from gb_chat.storage.client import ClientDB

LOCK = Lock()


class ChatClient:
    def __init__(self, config: dict):
        self.__is_logged = None
        self._config = config
        self.encoding = config["encoding"]
        self.socket = None
        self.address = config["address"]
        self.port = config["port"]
        self.account = config["account"]
        self.validator = Validator(config["schema"])
        self.is_connected = False
        self.db = ClientDB()
        self.session = 1

    def init(self):
        self.db.init("client_{}_{}.db".format(self.account["login"], str(datetime.utcnow().microsecond)))
        _socket = socket(AF_INET, SOCK_STREAM)
        self.socket = _socket
        logger.info("Client socket init at {address}:{port}".format(
            address=self.address, port=self.port
        ))

    def send_data(self, *, data: dict):
        data = json.dumps(data).encode(self.encoding)
        self.socket.send(data)

    def get_data(self) -> dict:
        data = self.socket.recv(1024)
        data = json.loads(data)
        return data

    # def check_data(self, data) -> bool:
    #     if "response" in data and data["response"] != 200:
    #         if "error" in data:
    #             print(data["error"])
    #         self.socket.close()
    #         return False
    #     else:
    #         if "alert" in data:
    #             print(data["alert"])
    #         return True

    def responses(self, response: dict) -> Optional[str]:
        message = None
        code = response["response"]
        data = response["alert"] if "alert" in response else response["error"] if "error" in response else ""
        if code in RESPONSE:
            if code == 202:
                if isinstance(data, list):
                    self.save_contacts(data)
            else:
                if code == 203:
                    self.is_connected = True
                    self.__is_logged = True
                elif code == 401:
                    self.__is_logged = False
                    data = ""
                elif code == 402:
                    self.__is_logged = False
                message = data if data != "" else RESPONSE[code]
                logger.info(message)
        else:
            message = "Unknown response: {code} {message}".format(code=code, message=data)
        return message

    def connect(self):
        self.init()
        logger.debug("client: {name}, try connect to {ip}:{port}".format(
            name=self.account["login"], ip=self._config["address"], port=self._config["port"]
        ))
        self.socket.connect((self._config["address"], self._config["port"]))
        logger.info("client: {name}, connected to {ip}:{port}".format(
            name=self.account["login"], ip=self._config["address"], port=self._config["port"]
        ))
        presence = request_presence(self.account["login"])
        logger.debug("client: {name}, try send presence: {presence}".format(
            name=self.account["login"], presence=presence
        ))
        self.send_data(data=presence)
        data = self.get_data()
        if "response" in data:
            if data["response"] == 200:
                self.__is_logged = True
            return self.responses(data)

    def login(self):
        self.send_data(data=request_authenticate(account_name=self.account["login"], password=self.account["password"]))

    def action(self, data: dict) -> Optional[dict]:
        msg = None
        action = data["action"]
        if action == "msg":
            if self.validator.validate_data(action, data):
                sender = data["from"]
                recipient = data["to"]
                self.db.Messages.create(session=self.session, message=data["message"],
                                        sender=sender, recipient=recipient,
                                        is_private=(sender.find("#") == -1 and recipient.find("#") == -1))
                msg = data
        elif action == "probe":
            if self.validator.validate_data(action, data):
                self.send_data(data=request_presence(self.account["login"]))
        return msg

    def get_contacts(self):
        logger.debug("client: {name}, try get_contacts".format(name=self.account["login"]))
        request = request_get_contacts(self.account["login"])
        self.send_data(data=request)

    def save_contacts(self, contacts: list):
        self.db.Contacts.refresh(contacts=contacts, session=self.session)

    def receiver(self):
        while True:
            try:
                data = self.get_data()
                logger.debug("Received: {}".format(data))
                if self.validator.validate_data("action", data):
                    data = self.action(data)
                    if data is not None:
                        print("\n{sender}: {msg}".format(sender=data["from"], msg=data["message"]))
            except (JSONDecodeError, ValidationError) as e:
                logger.error(str(e))
            except (OSError, ConnectionError, ConnectionAbortedError, ConnectionResetError) as ex:
                print("Соединение с сервером, разорвано")
                logger.critical(ex.with_traceback(traceback.print_exc()), exc_info=True)
                break

    def cli(self):
        while True:
            command = input("Введите команду: ")
            if command == "help":
                print("Доступные команды:")
                print("name - сменить имя (до подключения)")
                print("connect - подключиться к чату")
                print("! - выход из cli")
                print("exit - выход из программы")
                print("help - доступные команды")
            elif command == "connect":
                print("Введите знак '!' чтобы перейти в cli ")
                self.connect()
                if self.is_connected:
                    break
                else:
                    print("Подключение не удалось")
            elif command == "name":
                if sys._getframe(1).f_code.co_name == "run":
                    name = input("Ведите имя: ")
                    self.account["login"] = name
                else:
                    print("Смена имени доступна только при запуске!")
            elif command == "!":
                break
            elif command == "exit":
                try:
                    self.send_data(data=request_quit())
                    time.sleep(1)
                    sys.exit(1)
                except OSError:
                    pass

    def chat(self):
        while True:
            addressee = input("Введите адресата: ")
            msg = input("Сообщение: ")
            if msg == "!" or addressee == "!":
                self.cli()
            msg = request_msg(sender=self.account["login"], to=addressee, encoding=self.encoding, message=msg)
            logger.debug("client: {name}, try send msg: {msg}".format(
                name=self.account["login"], msg=msg
            ))
            self.send_data(data=msg)

    def run(self):
        if self.is_connected:
            receiver = Thread(target=self.receiver)
            receiver.daemon = True
            receiver.start()
            chat = Thread(target=self.chat)
            chat.daemon = True
            chat.start()
            while True:
                if receiver.is_alive() and chat.is_alive():
                    time.sleep(1)
                    continue
                else:
                    break

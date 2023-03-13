import json
import sys
import time
import traceback
from json import JSONDecodeError
from socket import SOCK_STREAM, AF_INET, socket
from typing import Optional

from jsonschema.exceptions import ValidationError

from .logger import logger
from gb_chat.tools.validator import Validator
from gb_chat.tools.requests import request_msg, request_presence, request_quit


class ChatClient:
    def __init__(self, config: dict, mode: str = "r"):
        self._config = config
        self.encoding = config["encoding"]
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.account = config["account"]
        self.mode = mode  # Временно, для выполнения ДЗ-7
        self.validator = Validator(config["schema"])

    def send_data(self, *, data: dict):
        data = json.dumps(data).encode(self.encoding)
        self.socket.send(data)

    def get_data(self) -> dict:
        data = self.socket.recv(1024)
        data = json.loads(data)
        return data

    def check_data(self, data) -> bool:
        if "response" in data and data["response"] != 200:
            if "error" in data:
                print(data["error"])
            self.socket.close()
            return False
        else:
            if "alert" in data:
                print(data["alert"])
            return True

    def connect(self):
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
        if self.check_data(data):
            self.chat()

    def action(self, data: dict) -> Optional[dict]:
        msg = None
        action = data["action"]
        if action == "msg":
            if self.validator.validate_data(action, data):
                msg = data
        elif action == "probe":
            if self.validator.validate_data(action, data):
                self.send_data(data=request_presence(self.account["login"]))
        return msg

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
        # Временная модификация, для выполнения ДЗ-7
        if self.mode == "w":
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
        if self.mode == "r":
            self.receiver()

    def run(self):
        self.cli()

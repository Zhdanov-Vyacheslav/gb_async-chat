import json
import time
from socket import SOCK_STREAM, AF_INET, socket

from .logger import logger


class ChatClient:
    def __init__(self, config: dict, mode: str = "r"):
        self._config = config
        self.encoding = config["encoding"]
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.account = config["account"]
        self.mode = mode  # Временно, для выполнения ДЗ-7

    def presence(self) -> bytes:
        data = {
            "action": "presence",
            "time": time.time(),
            "type": "status",
            "user": {
                "account_name": self.account,
                "status": "Yep, I am here!"
            }
        }
        data = json.dumps(data).encode(self.encoding)
        return data

    def msg(self, to: str, msg: str) -> bytes:
        data = {
            "action": "msg",
            "time": time.time(),
            "to": to,
            "from": self.account,
            "encoding": self.encoding,
            "message": msg
        }
        data = json.dumps(data).encode(self.encoding)
        return data

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
            name=self.account, ip=self._config["address"], port=self._config["port"]
        ))
        self.socket.connect((self._config["address"], self._config["port"]))
        logger.info("client: {name}, connected to {ip}:{port}".format(
            name=self.account, ip=self._config["address"], port=self._config["port"]
        ))
        presence = self.presence()
        logger.debug("client: {name}, try send presence: {presence}".format(
            name=self.account, presence=presence
        ))
        self.socket.send(presence)
        data = self.get_data()
        if self.check_data(data):
            self.chat()

    def chat(self):
        # Временная модификация, для выполнения ДЗ-7
        if self.mode == "w":
            while True:
                msg = input("Сообщение: ")
                msg = self.msg("server", msg)
                logger.debug("client: {name}, try send msg: {msg}".format(
                    name=self.account, msg=msg
                ))
                self.socket.send(msg)
                # data = self.get_data()
                # if not self.check_data(data):
                #     break
        if self.mode == "r":
            while True:
                data = self.get_data()
                if data is not None:
                    logger.debug("Server, send msg: {msg}".format(
                        name=self.account, msg=data
                    ))
                    print("{user}: {msg}".format(user=data["from"], msg=data["message"]))






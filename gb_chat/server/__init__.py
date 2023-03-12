import json
import select
import time
from json import JSONDecodeError
from socket import AF_INET, SOCK_STREAM, socket

from jsonschema.exceptions import ValidationError

from .logger import logger
from gb_chat.tools.validator import Validator


class ChatServer:
    def __init__(self, config):
        self.clients = []
        self.socket = None
        self.msg_validator = Validator(config["schema"]["msg"])
        self.presence_validator = Validator(config["schema"]["presence"])
        self.encoding = config["encoding"]
        self.limit = config["input_limit"]
        self.select_wait = config["select_wait"]
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.bind((config["address"], config["port"]))
        self.socket.listen(config["listen"])
        self.socket.settimeout(config["timeout"])

    def error_400(self, error: str = None) -> bytes:
        result = {
            "response": 400,
            "time": time.time(),
        }
        if error is not None:
            result["error"] = error
        result = json.dumps(result).encode(self.encoding)
        return result

    def error_500(self, error: str = None) -> bytes:
        result = {
            "response": 500,
            "time": time.time(),
        }
        if error is not None:
            result["error"] = error
        result = json.dumps(result).encode(self.encoding)
        return result

    def ok(self, msg: str = None) -> bytes:
        result = {
            "response": 200
        }
        if msg is not None:
            result["alert"] = msg
        result = json.dumps(result).encode(self.encoding)
        return result

    def get_data(self, *, client: socket) -> dict:
        try:
            data = client.recv(self.limit).decode(self.encoding)
            data = json.loads(data)
            return data
        except ConnectionResetError:
            logger.info(str(client.getpeername()) + " disconnected")
            self.clients.remove(client)

    def send_data(self, *, client: socket, data: dict):
        data = json.dumps(data).encode(self.encoding)
        client.send(data)

    def writer(self, clients, msgs: dict):
        for sender, msg in msgs.items():
            for client in clients:
                try:
                    self.send_data(client=client, data=msg)
                except ConnectionResetError:
                    if client in self.clients:
                        log = str(client.getpeername()) + " disconnected"
                        logger.info(log)
                        self.clients.remove(client)

    def reader(self, clients) -> dict:
        msg = None
        msgs = {}
        for client in clients:
            try:
                msgs[client] = self.get_data(client=client)
            except (JSONDecodeError, ValidationError) as e:
                msg = self.error_400("incorrect JSON object")
                logger.error(str(e))
            finally:
                if msg is not None:
                    client.send(msg)
                    client.close()
                    if client in self.clients:
                        self.clients.remove(client)
        return msgs

    def accept(self):
        try:
            client, addr = self.socket.accept()
        except OSError:
            return
        logger.info("Запрос на соединение от: {}".format(addr))
        client.settimeout(self.select_wait)
        try:
            data = self.get_data(client=client)
            client.settimeout(None)
            if self.presence_validator.validate_data(data):
                self.clients.append(client)
                client.send(self.ok("Welcome"))
        except OSError:
            return
        except (JSONDecodeError, ValidationError) as e:
            client.send(self.error_400("incorrect JSON object"))
            client.close()
            logger.error(str(e))

    def run(self):
        while True:
            self.accept()
            read = []
            write = []
            error = []
            try:
                read, write, error = select.select(self.clients, self.clients, [], self.select_wait)
            except OSError:
                pass
            msgs = self.reader(read)
            if msgs:
                self.writer(write, msgs)

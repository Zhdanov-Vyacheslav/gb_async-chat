import json
import select
from json import JSONDecodeError
from socket import AF_INET, SOCK_STREAM, socket
from typing import Optional

from jsonschema.exceptions import ValidationError

from .logger import logger
from gb_chat.tools.validator import Validator
from gb_chat.tools.responses import error_400, error_500, ok, RESPONSE
from gb_chat.tools.requests import request_msg


class ChatServer:
    def __init__(self, config):
        self.clients = {}
        self.socket = None
        self.validator = Validator(config["schema"])
        self.encoding = config["encoding"]
        self.limit = config["input_limit"]
        self.select_wait = config["select_wait"]
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.bind((config["address"], config["port"]))
        self.socket.listen(config["listen"])
        self.socket.settimeout(config["timeout"])

    def get_data(self, *, client: socket) -> dict:
        try:
            data = client.recv(self.limit).decode(self.encoding)
            data = json.loads(data)
            return data
        except ConnectionResetError:
            logger.info(str(client.getpeername()) + " disconnected")
            self.clients.pop(client)

    def send_data(self, *, client: socket, data: dict):
        data = json.dumps(data).encode(self.encoding)
        client.send(data)

    def action(self, client: socket, data: dict) -> Optional[dict]:
        msg = None
        action = data["action"]
        if action == "msg":
            if self.validator.validate_data(action, data):
                msg = data
        elif action == "presence":
            if self.validator.validate_data(action, data):
                self.send_data(client=client, data=ok())
        elif action == "authenticate":
            if self.validator.validate_data(action, data):
                pass
        elif action == "quit":
            if client in self.clients:
                msg = request_msg(
                    sender="server", to="global", encoding=self.encoding,
                    message="Пользователь: {user}, покинул чат!".format(user=self.clients[client])
                )
            self.quite(client, ok("Goodbye!"))
        elif action == "join":
            pass
        elif action == "leave":
            pass
        return msg

    def quite(self, client: socket, msg: dict):
        if client in self.clients:
            self.clients.pop(client)
            self.send_data(client=client, data=msg)
            client.close()

    def writer(self, clients: list[socket], msgs: dict):
        for sender, msg in msgs.items():
            if msg["to"] == "#server":
                for client in clients:
                    try:
                        self.send_data(client=client, data=msg)
                    except ConnectionResetError:
                        if client in self.clients:
                            log = str(client.getpeername()) + " disconnected"
                            logger.info(log)
                            self.clients.pop(client)
            elif msg["to"] in self.clients.values():
                client = list(self.clients.keys())[list(self.clients.values()).index(msg["to"])]
                self.send_data(client=client, data=msg)

    def reader(self, clients: list[socket]) -> dict:
        error = None
        msgs = {}
        for client in clients:
            try:
                data = self.get_data(client=client)
                if self.validator.validate_data("action", data):
                    if data["action"] == "msg":
                        self.validator.validate_data("msg", data)
                        data = self.action(client, data)
                        if data is not None:
                            msgs[client] = data
            except (JSONDecodeError, ValidationError) as e:
                error = error_400()
                logger.error(str(e))
            finally:
                if error is not None:
                    try:
                        self.send_data(client=client, data=error)
                        client.close()
                    except ConnectionResetError:
                        if client in self.clients:
                            user = self.clients.pop(client)
                            msg = "Пользователь: '{user}' покинул чат!".format(user=user)
                            msgs[client] = request_msg(sender="server", to="#server",
                                                       encoding=self.encoding, message=msg)
                        logger.info("Потеряно соединение с: {}".format(client.getpeername()))

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
            if self.validator.validate_data("presence", data):
                user = data["user"]["account_name"]
                if user not in self.clients.values():
                    self.clients.setdefault(client, user)
                    self.send_data(client=client, data=ok("Welcome"))
                else:
                    self.send_data(client=client, data=error_400(code=409))
                    client.close()
                    logger.error("User: {user}, {error}".format(user=user, error=RESPONSE[409]))
        except OSError:
            return
        except (JSONDecodeError, ValidationError) as e:
            self.send_data(client=client, data=error_400())
            client.close()
            logger.error(str(e))

    def run(self):
        while True:
            self.accept()
            read = []
            write = []
            error = []
            try:
                read, write, error = select.select(self.clients.keys(), self.clients.keys(), [], self.select_wait)
            except OSError:
                pass
            msgs = self.reader(read)
            if msgs:
                self.writer(write, msgs)

import json
import os
import re
import select
import time
import traceback
from argparse import ArgumentParser, Namespace
from json import JSONDecodeError
from socket import AF_INET, SOCK_STREAM, socket
from typing import Optional

from jsonschema import FormatChecker
from jsonschema.exceptions import ValidationError
from jsonschema.validators import Draft6Validator

from log.server_log_config import logger

CONFIG_PATH = os.getenv("CONFIG_PATH", os.path.join(os.path.split(os.path.dirname(__file__))[0], "config.json"))


def open_json(path: str, encoding: str = "utf-8") -> Optional[dict]:
    try:
        with open(path, "r", encoding=encoding) as f:
            result = json.load(f)
    except (FileNotFoundError, JSONDecodeError):
        return None
    return result


def prepare_config(options: Namespace, config_path: str) -> dict:
    result = open_json(config_path)

    if result is None:
        raise FileNotFoundError("Config is not found or has problem in {}".format(config_path))

    result = {**result["general"], **result["server"]}
    addr = re.match(result["RE_IP"], options.addr)

    if addr is None:
        raise ValueError(options.addr, "is not IP or 'localhost'")
    else:
        addr = addr[0]

    port = options.port if options.port is not None else result["DEFAULT_PORT"]

    if port not in range(*result["PORT_RANGE"]):
        raise ValueError("port: {} not in range 1024-49151".format(port))

    result["address"] = addr
    result["port"] = port

    return result


class Validator(object):
    def __init__(self, schema_path: str):
        schema_path = os.path.join(os.path.split(os.path.dirname(__file__))[0], schema_path)
        schema = open_json(schema_path)
        if schema is not None:
            self.schema = schema
        else:
            raise FileNotFoundError("schema not found in {}".format(schema_path))
        checker = FormatChecker()
        self._validator = Draft6Validator(self.schema, format_checker=checker)

    def validate_data(self, data: dict) -> bool:
        try:
            self._validator.validate(data)
            return True
        except ValidationError as e:
            field = "-".join(e.absolute_path)
            raise ValidationError("Validate Error, field[{field}], error msg: {msg}"
                                  .format(field=field, msg=e.message))


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


def main():
    ap = ArgumentParser()
    ap.add_argument("-a", dest="addr", required=False, default="0.0.0.0", help="IP-address or 'localhost'")
    ap.add_argument("-p", dest="port", type=int, required=False, help="port in range 1024-49151")
    options = ap.parse_args()
    config = prepare_config(options, config_path=CONFIG_PATH)
    server = ChatServer(config)
    logger.info("Server rdy")
    server.run()


if __name__ == "__main__":
    try:
        main()
    except Exception as ex:
        logger.critical(ex.with_traceback(traceback.print_exc()), exc_info=True)

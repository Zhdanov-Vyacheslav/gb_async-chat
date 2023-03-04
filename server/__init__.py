import json
import os
import re
import time
import traceback
from argparse import ArgumentParser, Namespace
from json import JSONDecodeError
from socket import AF_INET, SOCK_STREAM, socket
from typing import Optional

from jsonschema import FormatChecker
from jsonschema.exceptions import ValidationError
from jsonschema.validators import Draft6Validator

from log.server_log_config import logger, log

CONFIG_PATH = os.getenv("CONFIG_PATH", os.path.join(os.path.split(os.path.dirname(__file__))[0], "config.json"))


@log
def open_json(path: str, encoding: str = "utf-8") -> Optional[dict]:
    try:
        with open(path, "r", encoding=encoding) as f:
            result = json.load(f)
    except (FileNotFoundError, JSONDecodeError):
        return None
    return result


@log
def prepare_config(options: Namespace, config_path: str) -> dict:
    result = open_json(config_path)

    if result is None:
        raise FileNotFoundError("Config is not found in {}".format(config_path))

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
        self.client = None
        self.msg_validator = Validator(config["schema"]["msg"])
        self.presence_validator = Validator(config["schema"]["presence"])
        self.encoding = config["encoding"]
        self.limit = config["input_limit"]
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.bind((config["address"], config["port"]))
        self.socket.listen(config["listen"])

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

    @log
    def ok(self, msg: str = None) -> bytes:
        result = {
            "response": 200
        }
        if msg is not None:
            result["alert"] = msg
        result = json.dumps(result).encode(self.encoding)
        return result

    def get_data(self) -> dict:
        data = self.client.recv(self.limit).decode(self.encoding)
        data = json.loads(data)
        return data

    def accept(self):
        client, addr = self.socket.accept()
        logger.info("Запрос на соединение от: {}".format(addr))
        self.client = client
        data = self.get_data()
        if self.presence_validator.validate_data(data):
            client.send(self.ok())
            self.chat()

    def chat(self):
        while True:
            msg = self.get_data()
            if self.msg_validator.validate_data(msg):
                client = self.client.getpeername()
                logger.debug("{ip}:{port} прислал сообщение: {msg}".format(ip=client[0], port=client[1], msg=msg))
                self.client.send(self.ok("Сообщение получено"))


def main():
    ap = ArgumentParser()
    ap.add_argument("-a", dest="addr", required=False, default="0.0.0.0", help="IP-address or 'localhost'")
    ap.add_argument("-p", dest="port", type=int, required=False, help="port in range 1024-49151")
    options = ap.parse_args()
    config = prepare_config(options, config_path=CONFIG_PATH)
    server = ChatServer(config)
    logger.info("Server rdy")
    while True:
        msg = None
        try:
            server.accept()
        except (JSONDecodeError, ValidationError) as e:
            msg = server.error_400("incorrect JSON object")
            logger.error(str(e))
        except Exception as e:
            msg = server.error_500("Все сломалось...")
            logger.critical(e.with_traceback(traceback.print_exc()), exc_info=True)
        finally:
            if msg is not None:
                server.client.send(msg)
                server.client.close()


if __name__ == "__main__":
    try:
        main()
    except Exception as ex:
        logger.critical(ex.with_traceback(traceback.print_exc()), exc_info=True)

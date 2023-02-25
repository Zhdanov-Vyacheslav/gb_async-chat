import json
import os
import re
import time
import traceback
from argparse import Namespace, ArgumentParser
from json import JSONDecodeError
from socket import SOCK_STREAM, AF_INET, socket
from typing import Optional

CONFIG_PATH = os.getenv("CONFIG_PATH", os.path.join(os.path.abspath(os.path.dirname(__file__)), "..", "config.json"))


def open_json(path: str, encoding: str = "utf-8") -> Optional[dict]:
    try:
        with open(path, "r", encoding=encoding) as f:
            result = json.load(f)
    except (FileNotFoundError, JSONDecodeError, UnicodeDecodeError):
        return None
    return result


class ChatClient:
    def __init__(self, config):
        self._config = config
        self.encoding = config["encoding"]
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.account = config["account"]

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
        self.socket.connect((self._config["address"], self._config["port"]))
        self.socket.send(self.presence())
        data = self.get_data()
        if self.check_data(data):
            self.chat()

    def chat(self):
        while True:
            msg = input("Сообщение: ")
            self.socket.send(self.msg("server", msg))
            data = self.get_data()
            if not self.check_data(data):
                break


def prepare_config(options: Namespace, config_path) -> dict:
    result = open_json(config_path)

    if result is None:
        raise FileNotFoundError("Config is not found in {}".format(config_path))

    result = {**result["general"], **result["client"]}
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


def main():
    ap = ArgumentParser()
    ap.add_argument("addr", help="IP-address or 'localhost'")
    ap.add_argument("--port", dest="port", type=int, required=False, help="port in range 1024-49151")

    options = ap.parse_args()
    config = prepare_config(options, config_path=CONFIG_PATH)
    client = ChatClient(config)
    try:
        client.connect()
    except Exception as e:
        print(e.with_traceback(traceback.print_exc()))


if __name__ == "__main__":
    try:
        main()
    except Exception as ex:
        print(ex.with_traceback(traceback.print_exc()))

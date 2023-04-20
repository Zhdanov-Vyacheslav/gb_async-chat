import re
from argparse import Namespace

from .file import open_json


def prepare_config(options: Namespace, config_path: str, service: str) -> dict:
    result = open_json(config_path)

    if result is None:
        raise FileNotFoundError("Config is not found or has problem in {}".format(config_path))

    result = {**result["general"], **result[service]}
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


def config_file(config_path: str, service: str, address: str = None, port: int = None) -> dict:
    result = open_json(config_path)

    if result is None:
        raise FileNotFoundError("Config is not found or has problem in {}".format(config_path))

    result = {**result["general"], **result[service]}
    if address is not None:
        addr = re.match(result["RE_IP"], address)

        if addr is None:
            raise ValueError(address, "is not IP or 'localhost'")
        else:
            addr = addr[0]
    else:
        addr = "localhost"

    if port is not None:
        port = port
        if port not in range(*result["PORT_RANGE"]):
            raise ValueError("port: {} not in range 1024-49151".format(port))
    else:
        port = result["DEFAULT_PORT"]

    result["address"] = addr
    result["port"] = port

    return result

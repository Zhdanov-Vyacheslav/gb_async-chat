import time


def request_msg(*, sender: str, to: str, encoding: str, message: str) -> dict:
    data = {
        "action": "msg",
        "time": time.time(),
        "to": to,
        "from": sender,
        "encoding": encoding,
        "message": message
    }
    return data


def request_presence(account_name: str, status: str = "Yep, I am here!") -> dict:
    data = {
        "action": "presence",
        "time": time.time(),
        "type": "status",
        "user": {
            "account_name": account_name,
            "status": status
        }
    }
    return data


def request_authenticate(account_name: str, password: str) -> dict:
    data = {
        "action": "authenticate",
        "time": time.time(),
        "user": {
            "account_name": account_name,
            "password": password
        }
    }
    return data


def request_quit() -> dict:
    data = {
        "action": "quit",
        "time": time.time(),
    }
    return data


def request_probe() -> dict:
    data = {
        "action": "probe",
        "time": time.time(),
    }
    return data


def request_join(room: str) -> dict:
    data = {
        "action": "join",
        "time": time.time(),
        "room": room
    }
    return data


def request_leave(room: str) -> dict:
    data = {
        "action": "leave",
        "time": time.time(),
        "room": room
    }
    return data

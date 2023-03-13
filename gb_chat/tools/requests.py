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

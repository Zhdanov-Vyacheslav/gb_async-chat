import time

RESPONSE = {
    400: "incorrect JSON object",
    401: "Permissions denied, you need to log in",
    402: 'This could be "wrong password" or "no account with that name"',
    409: "Someone is already connected with the given user name",
}


def error_400(error: str = None, code: int = 400) -> dict:
    if code in RESPONSE and error is None:
        error = RESPONSE[code]
    result = {
        "response": code,
        "time": time.time(),
    }
    if error is not None:
        result["error"] = error
    return result


def error_500(error: str = None, code: int = 500) -> dict:
    result = {
        "response": code,
        "time": time.time(),
    }
    if error is not None:
        result["error"] = error
    return result


def ok(msg=None, code: int = 200) -> dict:
    result = {
        "response": code
    }
    if msg is not None:
        result["alert"] = msg
    return result

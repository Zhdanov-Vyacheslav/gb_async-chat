import inspect
import sys
from functools import wraps
from logging import Formatter, FileHandler, getLogger
import os

DEBUG = os.getenv("DEBUG", "")
DEBUG = True if "1" == DEBUG or "true" == DEBUG.lower() else False

FORMATTER = Formatter("[%(asctime)s]-[%(levelname)s]-[%(module)s]: %(message)s")
ENCODING = "utf-8"
NAME = "Client"
LEVEL = "INFO"
FILE = "client-gb_async-chat.log"

handler = FileHandler(FILE, encoding=ENCODING)
handler.setFormatter(FORMATTER)

logger = getLogger(NAME)
logger.addHandler(handler)
if DEBUG:
    logger.setLevel("DEBUG")
else:
    logger.setLevel(LEVEL)


def log(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        print(inspect.stack()[1][3])
        # не использовал inspect потому что при, обертки метода и функции результаты будут отличаться
        logger.debug("Функция {name} вызвана из функции {caller}".format(
            name=wrap.__name__, caller=sys._getframe(1).f_code.co_name)
        )
        return func(*args, **kwargs)

    return wrap

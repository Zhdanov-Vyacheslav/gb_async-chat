import os
import traceback
from argparse import ArgumentParser

from server import ChatServer, logger
from tools.config import prepare_config

CONFIG_PATH = os.getenv("CONFIG_PATH", os.path.join(os.path.split(os.path.dirname(__file__))[0], "config.json"))


def main():
    ap = ArgumentParser()
    ap.add_argument("-a", dest="addr", required=False, default="0.0.0.0", help="IP-address or 'localhost'")
    ap.add_argument("-p", dest="port", type=int, required=False, help="port in range 1024-49151")
    options = ap.parse_args()
    config = prepare_config(options, config_path=CONFIG_PATH, service="server")
    server = ChatServer(config)
    logger.info("Server rdy")
    server.run()


if __name__ == "__main__":
    try:
        main()
    except Exception as ex:
        logger.critical(ex.with_traceback(traceback.print_exc()), exc_info=True)

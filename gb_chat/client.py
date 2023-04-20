import os
import traceback
from argparse import ArgumentParser

from gb_chat.client.gui import GUIChatClient
from tools.config import prepare_config
from client import ChatClient, logger

CONFIG_PATH = os.getenv("CONFIG_PATH", os.path.join(os.path.abspath(os.path.dirname(__file__)), "..", "config.json"))


def main():
    ap = ArgumentParser()
    ap.add_argument("addr", help="IP-address or 'localhost'")
    ap.add_argument("--port", dest="port", type=int, required=False, help="port in range 1024-49151")

    options = ap.parse_args()
    config = prepare_config(options, config_path=CONFIG_PATH, service="client")
    client = ChatClient(config)
    gui = GUIChatClient(client)
    try:
        gui.run()
    except Exception as e:
        logger.critical(e.with_traceback(traceback.print_exc()), exc_info=True)

    # try:
    #     client.cli()
    #     client.run()
    # except Exception as e:
    #     logger.critical(e.with_traceback(traceback.print_exc()), exc_info=True)


if __name__ == "__main__":
    try:
        main()
    except Exception as ex:
        logger.critical(ex.with_traceback(traceback.print_exc()), exc_info=True)

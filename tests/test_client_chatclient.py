import json
import os
import unittest

from gb_chat.client import ChatClient
from gb_chat.tools.validator import Validator

CONFIG_PATH = os.path.join(os.path.split(os.path.dirname(__file__))[0], "config.json")


class ChatClientTestCase(unittest.TestCase):
    def setUp(self):
        with open(CONFIG_PATH) as f:
            result = json.load(f)
        config = {**result["general"], **result["client"], "address": "0.0.0.0"}
        config["port"] = config["DEFAULT_PORT"]
        self.schemas = result["server"]["schema"]
        self.chat_client = ChatClient(config)

    def tearDown(self):
        self.chat_client.socket.close()

    def test_presence(self):
        presence = self.chat_client.presence()
        try:
            presence = json.loads(presence)
            validator = Validator(self.schemas["presence"])
            return self.assertTrue(validator.validate_data("presence", presence))
        except Exception:
            return self.fail()

    def test_msg(self):
        msg = self.chat_client.msg("server", "hellow")
        try:
            msg = json.loads(msg)
            validator = Validator(self.schemas["msg"])
            return self.assertTrue(validator.validate_data("msg", msg))
        except Exception:
            return self.fail()


if __name__ == '__main__':
    unittest.main()

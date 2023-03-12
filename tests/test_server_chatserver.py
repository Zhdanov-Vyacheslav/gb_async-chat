import json
import os
import unittest

from gb_chat.server import ChatServer

CONFIG_PATH = os.path.join(os.path.split(os.path.dirname(__file__))[0], "config.json")


class ChatServerTestCase(unittest.TestCase):
    def setUp(self):
        with open(CONFIG_PATH) as f:
            result = json.load(f)
        config = {**result["general"], **result["server"], "address": "0.0.0.0"}
        config["port"] = config["DEFAULT_PORT"]
        self.chat_server = ChatServer(config)

    def tearDown(self):
        self.chat_server.socket.close()

    def test_response_ok(self):
        ok = self.chat_server.ok()
        try:
            ok = json.loads(ok)
            return self.assertEqual(ok["response"], 200)
        except Exception:
            return self.fail()

    def test_response_ok_msg(self):
        ok = self.chat_server.ok("hello")
        try:
            ok = json.loads(ok)
            return self.assertEqual((ok["response"], ok["alert"]), (200, "hello"))
        except Exception:
            return self.fail()

    def test_response_error_400(self):
        error_400 = self.chat_server.error_400()
        try:
            error_400 = json.loads(error_400)
            return self.assertEqual(error_400["response"], 400)
        except Exception:
            return self.fail()

    def test_response_error_400_msg(self):
        error_400 = self.chat_server.error_400(error="hello")
        try:
            error_400 = json.loads(error_400)
            return self.assertEqual((error_400["response"], error_400["error"]), (400, "hello"))
        except Exception:
            return self.fail()

    def test_response_error_500(self):
        error_500 = self.chat_server.error_500()
        try:
            error_500 = json.loads(error_500)
            return self.assertEqual(error_500["response"], 500)
        except Exception:
            return self.fail()

    def test_response_error_500_msg(self):
        error_500 = self.chat_server.error_500(error="hello")
        try:
            error_500 = json.loads(error_500)
            return self.assertEqual((error_500["response"], error_500["error"]), (500, "hello"))
        except Exception:
            return self.fail()


if __name__ == '__main__':
    unittest.main()

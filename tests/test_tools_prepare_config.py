import json
import os
import unittest
from argparse import Namespace

from gb_chat.tools.config import prepare_config

CONFIG_PATH = os.path.join(os.path.split(os.path.dirname(__file__))[0], "config.json")


class ServerPrepareConfigTestCase(unittest.TestCase):
    def setUp(self):
        with open(CONFIG_PATH) as f:
            result = json.load(f)
        self.file_config = {**result["general"], **result["server"]}

    def test_none(self):
        options = Namespace(**{"addr": "0.0.0.0", "port": None})
        self.file_config["address"] = "0.0.0.0"
        self.file_config["port"] = self.file_config["DEFAULT_PORT"]
        self.assertEqual(prepare_config(options, CONFIG_PATH, "server"), self.file_config)

    def test_port_1023(self):
        options = Namespace(**{"addr": "0.0.0.0", "port": 1023})
        try:
            prepare_config(options, CONFIG_PATH, "server")
        except Exception as e:
            return self.assertTrue(isinstance(e, ValueError))
        self.fail()
        # self.assertRaises(ValueError, prepare_config(options, CONFIG_PATH)) #  Не понял почему так не работает...

    def test_port_49152(self):
        options = Namespace(**{"addr": "0.0.0.0", "port": 49152})
        try:
            prepare_config(options, CONFIG_PATH, "server")
        except Exception as e:
            return self.assertTrue(isinstance(e, ValueError))
        self.fail()

    def test_port_1024(self):
        options = Namespace(**{"addr": "0.0.0.0", "port": 1024})
        self.file_config["address"] = "0.0.0.0"
        self.file_config["port"] = 1024
        self.assertEqual(prepare_config(options, CONFIG_PATH, "server"), self.file_config)

    def test_port_49151(self):
        options = Namespace(**{"addr": "0.0.0.0", "port": 49151})
        self.file_config["address"] = "0.0.0.0"
        self.file_config["port"] = 49151
        self.assertEqual(prepare_config(options, CONFIG_PATH, "server"), self.file_config)

    def test_address_localhost(self):
        options = Namespace(**{"addr": "localhost", "port": None})
        self.file_config["address"] = "localhost"
        self.file_config["port"] = self.file_config["DEFAULT_PORT"]
        self.assertEqual(prepare_config(options, CONFIG_PATH, "server"), self.file_config)

    def test_address_normal(self):
        options = Namespace(**{"addr": "192.168.10.3", "port": None})
        self.file_config["address"] = "192.168.10.3"
        self.file_config["port"] = self.file_config["DEFAULT_PORT"]
        self.assertEqual(prepare_config(options, CONFIG_PATH, "server"), self.file_config)

    def test_address_int_str(self):
        options = Namespace(**{"addr": "1.as.2.3.s", "port": None})
        try:
            prepare_config(options, CONFIG_PATH, "server")
        except Exception as e:
            self.assertTrue(isinstance(e, ValueError))

    def test_address_over(self):
        options = Namespace(**{"addr": "256.10.2.3", "port": None})
        try:
            prepare_config(options, CONFIG_PATH, "server")
        except Exception as e:
            return self.assertTrue(isinstance(e, ValueError))
        self.fail()

    def test_address_trash(self):
        options = Namespace(**{"addr": "asda123das12", "port": None})
        try:
            prepare_config(options, CONFIG_PATH, "server")
        except Exception as e:
            return self.assertTrue(isinstance(e, ValueError))
        self.fail()

    def test_path_bad(self):
        options = Namespace(**{"addr": "0.0.0.0", "port": None})
        try:
            prepare_config(options, "trash/path", "server")
        except Exception as e:
            return self.assertTrue(isinstance(e, FileNotFoundError))
        self.fail()


class ClientPrepareConfigTestCase(unittest.TestCase):
    def setUp(self):
        with open(CONFIG_PATH) as f:
            result = json.load(f)
        self.file_config = {**result["general"], **result["client"]}

    def test_none(self):
        options = Namespace(**{"addr": "localhost", "port": None})
        self.file_config["address"] = "localhost"
        self.file_config["port"] = self.file_config["DEFAULT_PORT"]
        self.assertEqual(prepare_config(options, CONFIG_PATH, "client"), self.file_config)

    def test_port_1023(self):
        options = Namespace(**{"addr": "localhost", "port": 1023})
        try:
            prepare_config(options, CONFIG_PATH, "client")
        except Exception as e:
            return self.assertTrue(isinstance(e, ValueError))
        self.fail()
        # self.assertRaises(ValueError, prepare_config(options, CONFIG_PATH)) #  Не понял почему так не работает...

    def test_port_49152(self):
        options = Namespace(**{"addr": "localhost", "port": 49152})
        try:
            prepare_config(options, CONFIG_PATH, "client")
        except Exception as e:
            return self.assertTrue(isinstance(e, ValueError))
        self.fail()

    def test_port_1024(self):
        options = Namespace(**{"addr": "localhost", "port": 1024})
        self.file_config["address"] = "localhost"
        self.file_config["port"] = 1024
        self.assertEqual(prepare_config(options, CONFIG_PATH, "client"), self.file_config)

    def test_port_49151(self):
        options = Namespace(**{"addr": "localhost", "port": 49151})
        self.file_config["address"] = "localhost"
        self.file_config["port"] = 49151
        self.assertEqual(prepare_config(options, CONFIG_PATH, "client"), self.file_config)

    def test_address_localhost(self):
        options = Namespace(**{"addr": "localhost", "port": None})
        self.file_config["address"] = "localhost"
        self.file_config["port"] = self.file_config["DEFAULT_PORT"]
        self.assertEqual(prepare_config(options, CONFIG_PATH, "client"), self.file_config)

    def test_address_normal(self):
        options = Namespace(**{"addr": "192.168.10.3", "port": None})
        self.file_config["address"] = "192.168.10.3"
        self.file_config["port"] = self.file_config["DEFAULT_PORT"]
        self.assertEqual(prepare_config(options, CONFIG_PATH, "client"), self.file_config)

    def test_address_int_str(self):
        options = Namespace(**{"addr": "1.as.2.3.s", "port": None})
        try:
            prepare_config(options, CONFIG_PATH, "client")
        except Exception as e:
            self.assertTrue(isinstance(e, ValueError))

    def test_address_over(self):
        options = Namespace(**{"addr": "256.10.2.3", "port": None})
        try:
            prepare_config(options, CONFIG_PATH, "client")
        except Exception as e:
            return self.assertTrue(isinstance(e, ValueError))
        self.fail()

    def test_address_trash(self):
        options = Namespace(**{"addr": "asda123das12", "port": None})
        try:
            prepare_config(options, CONFIG_PATH, "client")
        except Exception as e:
            return self.assertTrue(isinstance(e, ValueError))
        self.fail()

    def test_path_bad(self):
        options = Namespace(**{"addr": "localhost", "port": None})
        try:
            prepare_config(options, "trash/path", "client")
        except Exception as e:
            return self.assertTrue(isinstance(e, FileNotFoundError))
        self.fail()


if __name__ == '__main__':
    unittest.main()

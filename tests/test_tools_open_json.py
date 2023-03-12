import json
import os
import unittest

from gb_chat.tools.file import open_json

CONFIG_PATH = os.path.join(os.path.split(os.path.dirname(__file__))[0], "config.json")


class ToolsOpenJsonTestCase(unittest.TestCase):
    def setUp(self):
        with open("test.txt", "w", encoding="utf-8") as f:
            f.write("hello")
        with open("test.json", "w", encoding="utf-8") as f:
            json.dump({"hello": "привет"}, f)
        self.file_name = "test"

    def tearDown(self):
        if os.path.isfile("test.txt"):
            os.remove("test.txt")
        if os.path.isfile("test.json"):
            os.remove("test.json")

    def test_default(self):
        file = open_json("test.json")
        self.assertEqual(file, {"hello": "привет"})

    def test_not_json(self):
        file = open_json("test.txt")
        self.assertTrue(file is None)

    @unittest.expectedFailure
    def test_bad_encode(self):
        file = open_json("test.json", "utf-34")
        self.assertTrue(isinstance(file, dict))

    def test_encode_16(self):
        file = open_json("test.txt", "utf-16")
        self.assertTrue(file is None)


if __name__ == '__main__':
    unittest.main()

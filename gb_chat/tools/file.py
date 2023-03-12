import json
from json import JSONDecodeError
from typing import Optional


def open_json(path: str, encoding: str = "utf-8") -> Optional[dict]:
    try:
        with open(path, "r", encoding=encoding) as f:
            result = json.load(f)
    except (FileNotFoundError, JSONDecodeError):
        return None
    return result

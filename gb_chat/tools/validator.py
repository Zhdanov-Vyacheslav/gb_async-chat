import os

from jsonschema import FormatChecker
from jsonschema.exceptions import ValidationError
from jsonschema.validators import Draft6Validator

from ..tools.file import open_json


class Validator(object):
    def __init__(self, schemes: dict):
        self.schemes = {}
        self._validator = {}
        self.init(schemes)

    def init(self, schemas: dict):
        checker = FormatChecker()
        for name, path in schemas.items():
            schema_path = os.path.join(os.path.split(os.path.dirname(__file__))[0], path)
            schema = open_json(schema_path)
            if schema is None:
                raise FileNotFoundError("schema not found in {}".format(schema_path))
            self.schemes.setdefault(name, schema)
            self._validator.setdefault(name, Draft6Validator(schema, format_checker=checker))

    def validate_data(self, name: str, data: dict) -> bool:
        try:
            self._validator[name].validate(data)
            return True
        except ValidationError as e:
            field = "-".join(e.absolute_path)
            raise ValidationError("Validate Error, field[{field}], error msg: {msg}"
                                  .format(field=field, msg=e.message))

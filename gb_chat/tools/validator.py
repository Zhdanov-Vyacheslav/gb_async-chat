import os

from jsonschema import FormatChecker
from jsonschema.exceptions import ValidationError
from jsonschema.validators import Draft6Validator

from ..tools.file import open_json


class Validator(object):
    def __init__(self, schema_path: str):
        schema_path = os.path.join(os.path.split(os.path.dirname(__file__))[0], schema_path)
        schema = open_json(schema_path)
        if schema is not None:
            self.schema = schema
        else:
            raise FileNotFoundError("schema not found in {}".format(schema_path))
        checker = FormatChecker()
        self._validator = Draft6Validator(self.schema, format_checker=checker)

    def validate_data(self, data: dict) -> bool:
        try:
            self._validator.validate(data)
            return True
        except ValidationError as e:
            field = "-".join(e.absolute_path)
            raise ValidationError("Validate Error, field[{field}], error msg: {msg}"
                                  .format(field=field, msg=e.message))

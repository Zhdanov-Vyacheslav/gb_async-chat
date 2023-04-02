import os
from datetime import datetime

from peewee import AutoField, DateField, CharField, Model, DoesNotExist, BinaryUUIDField

from gb_chat.storage import BaseModel
from gb_chat.tools.hash import generate_hash


class Client(BaseModel):
    id = AutoField(primary_key=True)
    name = CharField(null=False, unique=True)
    password = CharField(null=True)
    salt = BinaryUUIDField(null=False)
    created = DateField(null=False, default=datetime.utcnow())
    modified = DateField(null=False, default=datetime.utcnow())

    class Meta:
        table_name = "Clients"

    @classmethod
    def login(cls, name: str, password: str = None):
        try:
            client = cls.get(cls.name == name)
            _password = generate_hash(password, client.salt) if password is not None else None
            if _password == client.password:
                return client.id
            else:
                return None
        except DoesNotExist:
            salt = os.urandom(16)
            _password = generate_hash(password, salt) if password is not None else None
            client = cls(name=name, password=_password, salt=salt)
            client.save()
            return client.id

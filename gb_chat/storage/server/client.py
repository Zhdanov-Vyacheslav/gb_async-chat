import os
from datetime import datetime

from peewee import AutoField, DateField, CharField, BooleanField, BlobField

from gb_chat.storage import BaseModel
from gb_chat.tools.hash import generate_hash


class Client(BaseModel):
    id = AutoField(primary_key=True)
    name = CharField(null=False, unique=True)
    password = BlobField(null=True)
    salt = BlobField(null=False)
    created = DateField(null=False, default=datetime.utcnow())
    modified = DateField(null=False, default=datetime.utcnow())
    is_moderator = BooleanField(default=False)

    class Meta:
        table_name = "Clients"

    @classmethod
    def login(cls, name: str, password: str = None, **kwargs):
        client = cls.get(cls.name == name)
        if client is not None:
            _password = generate_hash(password, client.salt) if password is not None else None
            if _password == client.password:
                return client.id
            else:
                return None
        else:
            salt = os.urandom(16)
            _password = generate_hash(password, salt) if password is not None else None
            client = cls(name=name, password=_password, salt=salt, **kwargs)
            client.save()
            return client.id

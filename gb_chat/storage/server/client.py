import os
from datetime import datetime

from peewee import AutoField, DateField, CharField, BooleanField, BlobField

from gb_chat.storage import BaseModel
from gb_chat.tools.hash import generate_hash


class Client(BaseModel):
    id = AutoField(primary_key=True)
    name = CharField(null=False, unique=True)
    password = BlobField(null=False)
    salt = BlobField(null=False)
    created = DateField(null=False, default=datetime.utcnow())
    modified = DateField(null=False, default=datetime.utcnow())
    is_moderator = BooleanField(default=False)

    class Meta:
        table_name = "Clients"

    @classmethod
    def __add(cls, name: str, password: str, client=None, **kwargs):
        salt = os.urandom(16)
        _password = generate_hash(password, salt) if password is not None else None
        if client is None:
            client = cls(name=name, password=_password, salt=salt, **kwargs)
        else:
            client.current_update(name=name, password=_password, salt=salt, **kwargs)
        client.save()
        return client.id

    @classmethod
    def login(cls, name: str, password: str = None, **kwargs):
        result = None
        client = cls.get(cls.name == name)
        if client is not None:
            if client.password is None:
                result = client.id if password is None else cls.__add(name=name, password=password, client=client, **kwargs)
            elif password is not None:
                if generate_hash(password, client.salt) == client.password:
                    result = client.id
        else:
            result = cls.__add(name=name, password=password, **kwargs)
        return result

    @classmethod
    def is_registered(cls, name: str):
        client = cls.get(cls.name == name)
        if client is not None:
            if client.password is not None:
                return True
        return False

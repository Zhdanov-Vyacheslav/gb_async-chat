from peewee import AutoField, ForeignKeyField

from gb_chat.storage import BaseModel
from gb_chat.storage.server.client import Client
from gb_chat.storage.server.history import History


class Contacts(BaseModel):
    id = AutoField(primary_key=True)
    client_id = ForeignKeyField(Client, unique=True)
    history_id = ForeignKeyField(History)

    class Meta:
        table_name = "Contacts"

    @classmethod
    def delete_by_client(cls, *args, **kwargs):
        client = Client.get(*args, **kwargs)
        contact = cls.get(cls.client_id == client.id)
        if contact is not None:
            contact.delete_instance()
            contact.save()

    @classmethod
    def list(cls, *args, **kwargs):
        result = []
        for user in Client.select(Client.name).join(cls):
            result.append(user.name)
        return result

    @classmethod
    def is_authorize(cls, name: str):
        result = False
        history = History.select(History.is_authorize).join(cls).join(Client).where(Client.name == name).limit(1)
        if len(history) > 0:
            result = history[0].is_authorize
        return result

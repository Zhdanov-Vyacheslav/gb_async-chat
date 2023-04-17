from datetime import datetime

from peewee import AutoField, DateField, IntegerField, ForeignKeyField, CharField, BooleanField

from gb_chat.storage import BaseModel
from gb_chat.storage.server.client import Client


class History(BaseModel):
    id = AutoField(primary_key=True)
    client_id = ForeignKeyField(Client)
    ip = CharField(null=False)
    port = IntegerField(null=False)
    logging = DateField(null=False, default=datetime.utcnow())
    is_authorize = BooleanField(default=False)

    class Meta:
        table_name = "History"

    @classmethod
    def login(cls, **kwargs):
        history = cls(**kwargs)
        history.save()
        return history.id

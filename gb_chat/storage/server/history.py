from datetime import datetime

from peewee import AutoField, DateField, IntegerField, ForeignKeyField, CharField, BooleanField

from .client import Client
from .. import BaseModel


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

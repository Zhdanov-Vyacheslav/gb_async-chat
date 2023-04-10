from peewee import AutoField, CharField, IntegerField

from gb_chat.storage import BaseModel


class Contacts(BaseModel):
    id = AutoField(primary_key=True)
    name = CharField(null=False, unique=True)
    session = IntegerField(null=False)

    class Meta:
        table_name = "Contacts"

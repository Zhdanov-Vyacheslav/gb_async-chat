from typing import Union

from peewee import AutoField, CharField, IntegerField

from gb_chat.storage import BaseModel


class Contacts(BaseModel):
    id = AutoField(primary_key=True)
    name = CharField(null=False, unique=False)
    session = IntegerField(null=False)

    class Meta:
        table_name = "Contacts"

    @classmethod
    def get_contacts(cls, session: int = None) -> list:
        result = []
        if session is None:
            cursor = cls.select(cls.name.unique).distinct()
        else:
            cursor = cls.select(cls.name).where(cls.session == session)
        for user in cursor:
            result.append(user.name)
        return result

    @classmethod
    def refresh(cls, contacts: list, session: int):
        session = session
        raw = set(contacts)
        old = set(cls.get_contacts(session=session))
        cls.remove_list(names=old - raw, session=session)
        cls.add_list(names=raw - old, session=session)

    @classmethod
    def add_list(cls, names: Union[list, set], session: int):
        for name in names:
            cls.create(name=name, session=session)

    @classmethod
    def remove_list(cls, names: Union[list, set], session: int):
        for name in names:
            contact = cls.get(cls.name == name, cls.session == session)
            contact.delete_instance()

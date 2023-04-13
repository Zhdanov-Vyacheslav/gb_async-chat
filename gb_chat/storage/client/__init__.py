from peewee import SqliteDatabase

from gb_chat.storage.client.contacts import Contacts
from gb_chat.storage.client.messages import Messages

TABLES = [
    Contacts,
    Messages
]


class ClientDB:
    def __init__(self):
        self.path = None
        self.__db = None

    def init(self, path):
        self.path = path
        self.__db = SqliteDatabase(self.path)
        self.__db.bind(TABLES)
        for table in TABLES:
            self.__setattr__(table._meta.table_name, table)
        self.__db.create_tables(TABLES)

    def close(self):
        if self.__db is not None:
            self.__db.close()

    def __str__(self):
        return self.path

    def __del__(self):
        self.close()


if __name__ == "__main__":
    s = ClientDB()
    s.init("lol.db")
    s.close()

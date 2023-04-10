from socket import socket
from typing import Union


class Contacts:
    def __init__(self, db):
        self.db = db

    def __call__(self, data: dict, client: socket, *args, **kwargs) -> Union[bool, list]:
        moderator = data.get("user_login")
        if self.is_moderator(moderator, client):
            return getattr(self, data["action"])(data)
        else:
            return False

    def is_moderator(self, name: str, client: socket) -> bool:
        queue = self.db.History \
            .select(self.db.History) \
            .join(Contacts) \
            .join(self.db.Clients) \
            .where((self.db.Clients.name == name) & (self.db.Clients.is_moderator == True))
        if len(queue) == 1:
            queue = queue[0]
            ip, port = client.getpeername()
            if ip == queue.ip and port == queue.port:
                return True
        return False

    @staticmethod
    def add_contact(data: dict) -> bool:
        return False

    def del_contact(self, data: dict) -> bool:
        user_id = data.get("user_id")
        if user_id is not None:
            self.db.Contacts.delete_by_client(self.db.Clients.name == user_id)
            return True
        return False

    def get_contacts(self, data: dict) -> list:
        queue = self.db.Clients.select(self.db.Clients).join(self.db.Contacts)
        result = []
        for client in queue:
            result.append(client.name)
        return result

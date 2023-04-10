from PyQt5.QtGui import QStandardItemModel, QStandardItem


def clients(database):
    queue = database.Clients.select(database.Clients).join(database.Contacts)
    clients = QStandardItemModel()
    clients.setHorizontalHeaderLabels(['Имя Клиента', 'IP Адрес', 'Порт', 'Время подключения'])
    for row in queue:
        user, ip, port, time = row
        user = QStandardItem(user)
        user.setEditable(False)
        ip = QStandardItem(ip)
        ip.setEditable(False)
        port = QStandardItem(str(port))
        port.setEditable(False)
        time = QStandardItem(str(time.replace(microsecond=0)))
        time.setEditable(False)
        clients.appendRow([user, ip, port, time])
    return clients


# GUI - Функция реализующая заполнение таблицы историей сообщений.
def contacts(database):
    # Список записей из базы
    historys = database.message_history()

    # Объект модели данных:
    contacts = QStandardItemModel()
    contacts.setHorizontalHeaderLabels(
        ['Имя Клиента', 'Последний раз входил', 'Сообщений отправлено', 'Сообщений получено'])
    for row in hist_list:
        user, last_seen, sent, recvd = row
        user = QStandardItem(user)
        user.setEditable(False)
        last_seen = QStandardItem(str(last_seen.replace(microsecond=0)))
        last_seen.setEditable(False)
        sent = QStandardItem(str(sent))
        sent.setEditable(False)
        recvd = QStandardItem(str(recvd))
        recvd.setEditable(False)
        contacts.appendRow([user, last_seen, sent, recvd])
    return contacts

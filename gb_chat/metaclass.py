import dis
from socket import socket


class ClientVerifier(type):
    def __init__(self, clsname, bases, clsdict):
        methods = []
        attrs = []
        classes = []
        allowed = ["Validator"]

        for key, value in clsdict.items():
            if isinstance(value, socket):
                # Проверяем отсутствие создания сокетов на уровне классов,
                # конструкций такого вида: class Client: s = socket()
                raise TypeError("Incorrect socket initialization.")
            try:
                instructions = dis.get_instructions(value)
            except TypeError:
                pass
            else:
                for instruction in instructions:
                    if key == "__init__":
                        if instruction.opname == 'LOAD_GLOBAL':
                            if instruction.argval not in allowed:
                                # Проверяем отсутствие создания сокетов на уровне классов,
                                # конструкций такого вида: class Client: def __init__(...): s = socket()
                                raise TypeError("Incorrect initialization.")
                    if instruction.opname == 'LOAD_METHOD':
                        if instruction.argval not in methods:
                            methods.append(instruction.argval)
                    elif instruction.opname == 'LOAD_ATTR':
                        if instruction.argval not in attrs:
                            attrs.append(instruction.argval)
                    elif instruction.opname == 'LOAD_GLOBAL':
                        if instruction.argval not in classes:
                            classes.append(instruction.argval)

        # Проверка отсутствия вызовов accept и listen для сокетов;
        for command in ('accept', 'listen'):
            if command in methods:
                raise TypeError('Method "{}" forbidden in class'.format(command))

        # Проверка использования сокетов для работы по TCP
        if not ("SOCK_STREAM" in classes and "AF_INET" in classes):
            if not ("SOCK_STREAM" in attrs and "AF_INET" in attrs):
                raise TypeError("Incorrect socket initialization.")

        super().__init__(clsname, bases, clsdict)


class ServerVerifier(type):
    def __init__(self, clsname, bases, clsdict):
        methods = []
        attrs = []
        classes = []
        allowed = ["Validator"]

        for key, value in clsdict.items():
            if isinstance(value, socket):
                # Проверяем отсутствие создания сокетов на уровне классов,
                # конструкций такого вида: class Client: s = socket()
                raise TypeError("Incorrect socket initialization.")
            try:
                instructions = dis.get_instructions(value)
            except TypeError:
                pass
            else:
                for instruction in instructions:
                    if key == "__init__":
                        if instruction.opname == 'LOAD_GLOBAL':
                            if instruction.argval not in allowed:
                                # Проверяем отсутствие создания сокетов на уровне классов,
                                # конструкций такого вида: class Client: def __init__(...): s = socket()
                                raise TypeError("Incorrect initialization.")
                    if instruction.opname == 'LOAD_METHOD':
                        if instruction.argval not in methods:
                            methods.append(instruction.argval)
                    elif instruction.opname == 'LOAD_ATTR':
                        if instruction.argval not in attrs:
                            attrs.append(instruction.argval)
                    elif instruction.opname == 'LOAD_GLOBAL':
                        if instruction.argval not in classes:
                            classes.append(instruction.argval)

        # Проверка отсутствия вызовов connect для сокетов
        if 'connect' in methods:
            raise TypeError("connect not allowed in server class")
        # Проверка использования сокетов для работы по TCP
        if not ("SOCK_STREAM" in classes and "AF_INET" in classes):
            if not ("SOCK_STREAM" in attrs and "AF_INET" in attrs):
                raise TypeError("Incorrect socket initialization.")

        super().__init__(clsname, bases, clsdict)
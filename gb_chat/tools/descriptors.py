PORT_RANGE = [1024, 49152]


class Port:
    def __set_name__(self, owner, name):
        self.name = name

    def __set__(self, instance, value):
        try:
            _value = int(value)
        except ValueError:
            raise ValueError("Port {} is not integer".format(value))
        if _value not in range(*PORT_RANGE):
            raise ValueError("Port {} not in range 1024-49151".format(value))
        setattr(instance, self.name, _value)

    def __get__(self, instance, owner):
        return getattr(instance, self.name)

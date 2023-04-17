from peewee import Model, DoesNotExist


class BaseModel(Model):

    @classmethod
    def get(cls, *args, **kwargs):
        try:
            return super().get(*args, **kwargs)
        except DoesNotExist:
            return None

    def current_update(self, **kwargs):
        for k, v in kwargs.items():
            if k in self.__dict__["__data__"]:
                self.__dict__["__data__"][k] = v

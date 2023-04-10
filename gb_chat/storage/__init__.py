from peewee import Model, DoesNotExist


class BaseModel(Model):

    @classmethod
    def get(cls, *args, **kwargs):
        try:
            return super().get(*args, **kwargs)
        except DoesNotExist:
            return None

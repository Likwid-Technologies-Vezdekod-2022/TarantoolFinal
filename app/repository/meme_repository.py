from tarantool.response import Response
from tarantool.space import Space

from db import Store
import models


class MemeRepository:
    def __init__(self, store: Store):
        self.store = store
        self.space: Space = self.store.get_space('meme')

    def get_all_memes(self) -> list[models.Meme]:
        data = list(self.space.select())
        data = [models.Meme.get_from_db_data(obj) for obj in data]
        print(data)
        return data

    def create_meme(self, instance: models.Meme) -> models.Meme:
        r: Response = self.space.insert(instance.get_data_to_save())
        obj = models.Meme.get_from_db_data(r.data[0])
        return obj

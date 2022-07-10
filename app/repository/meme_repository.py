from typing import Union

from tarantool.response import Response
from tarantool.space import Space

from db import Store
import models


class MemeRepository:
    def __init__(self, store: Store):
        self.store = store
        self.space: Space = self.store.get_space('meme')

    def get_all_memes(self, to_dict=False) -> list[models.Meme]:
        """

        :rtype: object
        """
        data = list(self.space.select())
        if to_dict:
            data = [models.Meme.get_from_db_data(obj).dict() for obj in data]
        else:
            data = [models.Meme.get_from_db_data(obj) for obj in data]
        return data

    def get_meme(self, pk) -> Union[models.Meme, None]:
        r: Response = self.space.select(pk)
        if not r.data:
            return None

        obj = models.Meme.get_from_db_data(r.data[0])
        return obj

    def create_meme(self, instance: models.Meme) -> models.Meme:
        r: Response = self.space.insert(instance.get_data_to_save())
        obj = models.Meme.get_from_db_data(r.data[0])
        return obj

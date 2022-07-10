import tarantool


class Store:
    def __init__(self, url: str, port: int):
        self.connection = tarantool.connect(url, port)

    def get_space(self, space_name: str):
        return self.connection.space(space_name)

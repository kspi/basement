from common import Object

class Tile(Object):
    def __init__(self, level, x, y):
        self.level = level
        self.x = x
        self.y = y
        self.actor = None

    @property
    def is_occupied(self):
        return self.actor is not None

    @classmethod
    def from_symbol(cls, symbol):
        try:
            return cls._symbol_map[symbol]
        except AttributeError:
            cls._symbol_map = {c.symbol: c for c in cls.__subclasses__()}
            return cls._symbol_map[symbol]

    def __str__(self):
        if self.is_occupied:
            return str(self.actor)
        return super().__str__()


class Ground(Tile):
    is_passable = True
    symbol = '.'


class Wall(Tile):
    is_passable = False
    symbol = '#'



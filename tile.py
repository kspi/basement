from common import Object

class Tile(Object):
    def __init__(self, level, x, y):
        self.level = level
        self.x = x
        self.y = y
        self.actor = None
        self.items = set()

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

    @property
    def symbol(self):
        if self.is_occupied:
            return self.actor.symbol
        if self.items:
            return next(iter(self.items)).symbol
        return self.tile_symbol


class Ground(Tile):
    is_passable = True
    tile_symbol = '.'


class Wall(Tile):
    is_passable = False
    tile_symbol = '#'



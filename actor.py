from common import Object


class MovementObstructed(Exception):
    pass


class Actor(Object):
    speed = 100

    def __init__(self, tile):
        assert(not tile.is_occupied)
        tile.actor = self
        self.tile = tile
        self.inventory = set()
        self.level.actors.add(self)

    def act(self):
        pass

    @property
    def x(self):
        return self.tile.x

    @property
    def y(self):
        return self.tile.y

    @property
    def level(self):
        return self.tile.level

    def move_to(self, tile):
        if not tile.is_passable or tile.is_occupied:
            raise MovementObstructed
        self.tile.actor = None
        self.tile = tile
        tile.actor = self
        if self.tile.level != tile.level:
            self.tile.level.actors.remove(self)
            tile.level.actors.add(self)

    def move_by(self, dx, dy):
        self.move_to(self.level[self.x + dx, self.y + dy])


class Player(Actor):
    symbol = '@'



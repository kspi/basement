from level import Level
from tile import Ground
import math
import noise
import random
import numpy


def dnorm(x, mu, sig):
    return numpy.exp(-numpy.pow(x - mu, 2.) / (2 * numpy.pow(sig, 2.)))


def bitmap_level(bitmap, xofs, yofs):
    level = Level()
    w, h = bitmap.shape
    for x in range(w):
        for y in range(h):
            if bitmap[x, y]:
                lx = x + xofs
                ly = y + yofs
                level[lx, ly] = Ground(level, lx, ly)
    return level


def caverns(granularity, radius):
    xofs = random.randint(-10000, 10000)
    yofs = random.randint(-10000, 10000)
    radius = int(radius)
    sigma = radius / 3
    level = Level()
    for x in range(-radius, radius):
        for y in range(-radius, radius):
            r = math.sqrt(x * x + y * y)
            n = abs(noise.pnoise2((xofs + x) / granularity, (yofs + y) / granularity, octaves=3))
            d = dnorm(r, 0, sigma) * n
            if d > 0.09:
                level[x, y] = Ground(level, x, y)
    return level



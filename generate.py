from level import Level
from tile import Ground
import math
import noise
import random
import numpy


def dnorm(x, mu, sig):
    return numpy.exp(-numpy.power(x - mu, 2.) / (2 * numpy.power(sig, 2.)))


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


def caverns():
    radius = int(radius)
    
    return bitmap_level(bitmap, ex, ey)

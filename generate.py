from level import Level
from tile import Ground
import math
import noise
import random
import numpy


def norm2(x, y):
    return numpy.sqrt(x * x + y * y)


def normal_density(x, mu, sig):
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
    size = 100
    sigma = size / 2
    bitmap = numpy.ndarray(
    return bitmap_level(bitmap, ex, ey)

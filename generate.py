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
    size = 300
    sigma = size / 40
    ex, ey = size // 2, size // 2
    density = numpy.zeros((size, size), numpy.float32)
    for blob in range(1):
        #bx = random.normalvariate(ex, sigma)
        #by = random.normalvariate(ey, sigma)
        #sm = 100
        #sk = 3
        #bsize = random.gammavariate(sk, sk / sm)
        bx = ex
        by = ey
        bsize = 20
        for x in range(size):
            for y in range(size):
                density[x, y] += normal_density(norm2(x - bx, y - by), 0, bsize)
    print(numpy.max(density))
    density /= numpy.max(density)

    bitmap = density > 0.5
    return bitmap_level(bitmap, ex, ey)

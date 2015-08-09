from level import Level
from tile import Ground
import math
import noise
import random
import numpy


def dnorm(x, mu, sig):
    return math.exp(-pow(x - mu, 2.) / (2 * pow(sig, 2.)))


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



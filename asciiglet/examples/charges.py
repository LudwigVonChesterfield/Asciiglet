import random

import numpy as np

from asciiglet.environment import Environment
from asciiglet.particle import Particle
from asciiglet.transform import Transform
from asciiglet.emitter import Emitter
from asciiglet.vector import Vector
from asciiglet.particle_effect import *


environment = Environment()

for i in range(30):
    x = random.uniform(0, 1024)
    y = random.uniform(0, 720)

    charge = random.uniform(-5.0, 5.0)

    mass = random.uniform(0.25, 1.0)

    symbol = "+"
    if charge < 0:
        symbol = "-"
    elif charge == 0:
        symbol = "n"

    size = charge * mass * 2

    scale = Vector.new(size, size)

    p = Particle(sprite=symbol, transform=Transform(pos=Vector.new(x, y), scale=scale))
    p.name = symbol + str(i)
    p.add_effect(ChargedPE(weight=mass, charges={"electricity": charge}))

    environment.particles.append(p)

if __name__ == "__main__":
    environment.run()

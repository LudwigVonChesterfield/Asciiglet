import numpy as np
import random

from asciiglet import *

e = Environment()


for i in range(50):
    x = 500.0 + random.randrange(-300, 300)
    y = 400.0 + random.randrange(-300, 300)
    t = Transform(pos=Vector.new(x, y))
    e.particles.extend(get_gas(None, e=e, t=t))

e.run()

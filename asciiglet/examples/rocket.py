import random

import numpy as np

from asciiglet.environment import Environment
from asciiglet.particle import Particle
from asciiglet.transform import Transform
from asciiglet.emitter import Emitter
from asciiglet.vector import Vector
from asciiglet.particle_effect import *


e = Environment()

p1 = Particle(
    transform=Transform(
        pos=Vector.new(500.0, 350.0),
        scale=Vector.new(3.0, 3.0)
    )
)
p1.effects.append(GravityPE(p1, weight=3.0))
p1.velocity = np.array([10.0, 0.0])
p1.sprite.set_color("GREEN")

p2 = Particle(
    transform=Transform(
        pos=Vector.new(500.0, 250.0),
        scale=Vector.new(5.0, 5.0)
    )
)
p2.effects.append(GravityPE(p2, weight=5.0))
p2.effects.append(DissipatePE(p2, amount=1.0, loss=0.05))
p2.transform.face(p1.transform)
p2.sprite.set_color("PINK")

t3 = Transform(pos=Vector.new(300.0, 450.0))
p3 = Particle(transform=t3, sprite=")o>")
p3.sprite.set_color("WHITE")
p3.velocity = Vector.new(15.0, 0.0)
p3.acceleration = Vector.new(-0.1, 0.0)
p3.effects.append(GravityPE(p3, weight=1.0))
p3.effects.append(FaceMovementPE(p3, turn_speed=10))


def get_smoke(emitter):
    vx = 10 - random.uniform(0.0, 8.0)
    vy = random.uniform(-3.0, 3.0)

    vel = Vector.rotate(Vector.new(vx, vy), emitter.transform.parent.angle)

    size = random.uniform(0.2, 0.5)

    t = Transform(
        pos=np.copy(emitter.transform.pos), scale=np.array([size, size])
    )
    t.pos -= emitter.transform.parent.forward() * 12

    s = Particle(transform=t)
    s.velocity = vel
    s.effects.append(DissipatePE(s, amount=1, loss=0.1))
    s.sprite.set_color(random.choice(["RED", "ORANGE", "YELLOW"]))
    # s.effects.append(ConstantPE(velocity=Vector.new(vx, vy)))

    return [s]


e3 = Emitter(e, particles=get_smoke)
e3.transform.setParent(t3)

e.particles.extend([p1, p2, p3, e3])

e.run()

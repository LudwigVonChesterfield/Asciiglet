import math

import numpy as np

from .abstract_object import AbstractObject
from .vector import Vector


class ParticleEffect(AbstractObject):
    def __init__(self, particle):
        super().__init__()
        self.particle = particle

        self.velocity = Vector.new(0, 0)
        self.acceleration = Vector.new(0.0, 0.0)

        self.rotation = 0
        self.rotation_acceleration = 0

    def __destroy__(self):
        self.particle = None
        super().__destroy__()

    def apply(self, particle, dt):
        pass


class GravityPE(ParticleEffect):
    bodies = []

    def __init__(self, particle, weight=1.0):
        super().__init__(particle)
        self.weight = weight
        GravityPE.bodies.append(self)

    def __destroy__(self):
        GravityPE.bodies.remove(self)
        super().__destroy__()

    def apply(self, particle, dt):
        self.acceleration = np.array([0.0, 0.0])

        for g in GravityPE.bodies:
            dpos = g.particle.transform.pos - particle.transform.pos
            if dpos[0] == 0 and dpos[1] == 0:
                continue

            distance_squared = Vector.magnitudeSquared(dpos)
            attr = g.weight / distance_squared

            self.acceleration += dpos * attr * dt


class ChargedPE(ParticleEffect):
    bodies = []

    def __init__(self, particle, weight=1.0, charges={}):
        super().__init__(particle)
        self.weight = weight
        self.charges = charges
        ChargedPE.bodies.append(self)

    def __destroy__(self):
        ChargedPE.bodies.remove(self)
        super().__destroy__()

    def apply(self, particle, dt):
        self.acceleration = np.array([0.0, 0.0])

        for c in ChargedPE.bodies:
            dpos = c.particle.transform.pos - particle.transform.pos
            if dpos[0] == 0 and dpos[1] == 0:
                continue

            distance_squared = Vector.magnitudeSquared(dpos)
            attr = 0
            for field, q1 in self.charges.items():
                q2 = 0
                if field in c.charges.keys():
                    q2 = c.charges[field]

                attr += -(q1 * q2) / (distance_squared * self.weight)

            self.acceleration += dpos * attr * dt


class DissipatePE(ParticleEffect):
    def __init__(
        self,
        particle,
        sprites="@ao*.",
        amount=1,
        loss=0.0,
        loss_perc=0.0
    ):
        super().__init__(particle)

        self.sprites = sprites

        self.amount = amount
        self.max_amount = amount

        self.loss = loss
        self.loss_perc = loss_perc

    def apply(self, particle, dt):
        self.amount -= self.loss * dt
        self.amount -= self.amount * self.loss_perc * dt

        if self.amount <= 0.0:
            particle.destroy()
            return

        perc_left = self.amount / self.max_amount

        symbol_pos = len(self.sprites) - math.ceil(
            len(self.sprites) * perc_left
        )

        sprite_symbol = self.sprites[symbol_pos]

        particle.sprite.set_sprite(sprite_symbol)


class EmitPE(ParticleEffect):
    def __init__(self, particle, particles):
        super().__init__(particle)
        self.particles = particles

    def apply(self, particle, dt):
        for particle in self.particles(self):
            self.environment.particles.append(particle)


class TimedPE(ParticleEffect):
    """
    Adds an *effect* after *time*.
    """

    def __init__(
        self,
        particle,
        effect,
        time=1.0,
    ):
        super().__init__(particle)

        self.effect = effect
        self.time = time

    def __destroy__(self):
        self.effect.destroy()

    def apply(self, particle, dt):
        self.time -= dt
        if self.time <= 0:
            particle.effects.append(self.effect)
            self.destroy()


class LastingPE(ParticleEffect):
    """
    Trigger *effect* each tick, delete after *time*.
    """

    def __init__(
        self,
        particle,
        effect,
        time=1.0,
    ):
        super().__init__(particle)

        self.effect = effect
        self.time = time

    def __destroy__(self):
        self.effect.destroy()

    def apply(self, particle, dt):
        self.effect.apply(particle, dt)

        self.time -= dt
        if self.time <= 0:
            self.destroy()


class CooldownPE(ParticleEffect):
    """
    Trigger *effect* every *time* seconds.
    """

    def __init__(
        self,
        particle,
        effect,
        time=1.0,
    ):
        super().__init__(particle)

        self.effect = effect
        self.time = time
        self.max_time = time

    def __destroy__(self):
        self.effect.destroy()

    def apply(self, particle, dt):
        self.time -= dt
        if self.time <= 0:
            self.effect.apply(particle, dt)
            self.time = self.max_time


class FaceMovementPE(ParticleEffect):
    """
    Changes angle to face velocity.
    """

    def __init__(
        self,
        particle,
        turn_speed=1.0,
    ):
        super().__init__(particle)

        self.turn_speed = turn_speed

    def apply(self, particle, dt):
        if particle.velocity[0] != 0 or particle.velocity[1] != 0:
            angle = Vector.angleRotateTo(
                particle.transform.forward(), particle.velocity
            )
            self.rotation = Vector.angleRotateTo(
                particle.transform.forward(), particle.velocity
            ) * self.turn_speed * dt

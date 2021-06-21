import math

import numpy as np

from .abstract_object import AbstractObject
from .vector import Vector
from .emitter import Emitter


class ParticleEffect(AbstractObject):
    def __init__(self):
        super().__init__()
        self.particle = None

        self.velocity = Vector.new(0, 0)
        self.acceleration = Vector.new(0.0, 0.0)

        self.rotation = 0
        self.rotation_acceleration = 0

    def __destroy__(self):
        self.particle = None
        super().__destroy__()

    @property
    def particle(self):
        return self._particle

    @particle.setter
    def particle(self, value):
        self._particle = value

    def apply(self, particle, dt):
        pass


class GravityPE(ParticleEffect):
    bodies = []

    def __init__(self, weight=1.0):
        super().__init__()
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

    def __init__(self, weight=1.0, charges={}):
        super().__init__()
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
        sprites="@ao*.",
        amount=None,
        max_amount=1,
        loss=0.0,
        loss_perc=0.0
    ):
        super().__init__()

        self.sprites = sprites

        if amount is None:
            amount = max_amount

        self.amount = amount
        self.max_amount = max_amount

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
    def __init__(self, environment, particles):
        super().__init__()
        self.environment = environment
        self.particles = particles

    def __destroy__(self):
        self.environment = None
        super().__destroy__()

    def apply(self, particle, dt):
        for particle in self.particles(self):
            self.environment.particles.append(particle)


class SpawnEmitterPE(ParticleEffect):
    def __init__(
        self,
        environment,
        particles,
        cooldown=1,
        to_live=-1
    ):
        super().__init__()
        self.environment = environment
        self.particles = particles

        self.cooldown = cooldown
        self.to_live = to_live

    def __destroy__(self):
        self.environment = None
        super().__destroy__()

    def apply(self, particle, dt):
        t = particle.transform.copy()
        e = Emitter(
            self.environment,
            transform=t,
            particles=self.particles,
            cooldown=self.cooldown,
            to_live=self.to_live
        )
        self.environment.particles.append(e)


class TimedPE(ParticleEffect):
    """
    Adds an *effect* after *time*.
    """

    def __init__(
        self,
        effect,
        time=1.0,
    ):
        self.effect = effect
        super().__init__()
        self.time = time

    @ParticleEffect.particle.setter
    def particle(self, value):
        self._particle = value
        self.effect.particle = value

    def apply(self, particle, dt):
        self.time -= dt
        if self.time <= 0:
            particle.add_effect(self.effect)
            self.destroy()


class LastingPE(ParticleEffect):
    """
    Trigger *effect* each tick, delete after *time*.
    """

    def __init__(
        self,
        effect,
        time=1.0,
    ):
        self.effect = effect
        super().__init__()
        self.time = time

    def __destroy__(self):
        self.effect.destroy()
        super().__destroy__()

    @ParticleEffect.particle.setter
    def particle(self, value):
        self._particle = value
        self.effect.particle = value

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
        effect,
        time=1.0,
    ):
        self.effect = effect
        super().__init__()
        self.time = time
        self.max_time = time

    def __destroy__(self):
        self.effect.destroy()
        super().__destroy__()

    @ParticleEffect.particle.setter
    def particle(self, value):
        self._particle = value
        self.effect.particle = value

    def apply(self, particle, dt):
        self.time -= dt
        if self.time <= 0:
            self.effect.apply(particle, dt)
            self.time = self.max_time


class FaceMovementPE(ParticleEffect):
    """
    Changes angle to face velocity.
    """

    def __init__(self, turn_speed=1.0):
        super().__init__()

        self.turn_speed = turn_speed

    def apply(self, particle, dt):
        if particle.velocity[0] != 0 or particle.velocity[1] != 0:
            self.rotation = Vector.angleRotateTo(
                particle.transform.forward(), particle.velocity
            ) * self.turn_speed * dt


class ForwardMovementPE(ParticleEffect):
    """
    Applied acceleration in the forward direction.
    """

    def __init__(self, forward_velocity=0.0, forward_acceleration=0.0):
        super().__init__()

        self.forward_velocity = forward_velocity
        self.forward_acceleration = forward_acceleration

    def apply(self, particle, dt):
        self.velocity = particle.transform.forward() * self.forward_velocity
        self.acceleration = (
            particle.transform.forward() * self.forward_acceleration
        )


class OnDestroyPE(ParticleEffect):
    """
    Issues *effect* when particle is destroyed.
    """

    def __init__(
        self,
        effect,
    ):
        self.effect = effect
        super().__init__()
        self.dt = 0

    def __destroy__(self):
        self.effect.apply(self.particle, self.dt)
        self.effect.destroy()
        super().__destroy__()

    @ParticleEffect.particle.setter
    def particle(self, value):
        self._particle = value
        self.effect.particle = value

    def apply(self, particle, dt):
        self.dt = dt

from .sprite import Sprite
from .game_object import GameObject
from .vector import Vector


class Particle(GameObject):
    def __init__(self, transform=None, sprite="@"):
        super().__init__(transform=transform)

        self.sprite = Sprite(sprite)

        self.effects = []

        self.velocity = Vector.new(0.0, 0.0)
        self.acceleration = Vector.new(0.0, 0.0)

        self.rotation = 0
        self.rotation_acceleration = 0

    def __destroy__(self):
        for effect in self.effects:
            effect.destroy()
        self.effects = []

        super().__destroy__()

    def destroy(self):
        self.destroying = True
        self.__destroy__()

    def update(self, dt):
        super().update(dt)

        for effect in self.effects:
            effect.apply(self, dt)

        self.velocity += self.m_acceleration * dt
        self.transform.pos += self.m_velocity * dt

        self.rotation += self.m_rotation_acceleration * dt
        self.transform.angle += self.m_rotation * dt

        """
        Face where you are going.

        if self.velocity[0] != 0 or self.velocity[1] != 0:
            self.transform.angle += Vector.angleRotateTo(
                self.transform.forward(), self.velocity
            ) * dt
        """

    @property
    def m_velocity(self):
        v = Vector.new(0.0, 0.0)
        for effect in self.effects:
            v += effect.velocity
        return self.velocity + v

    @property
    def m_acceleration(self):
        a = Vector.new(0.0, 0.0)
        for effect in self.effects:
            a += effect.acceleration
        return self.acceleration + a

    @property
    def m_rotation(self):
        r = 0
        for effect in self.effects:
            r += effect.rotation
        return self.rotation + r

    @property
    def m_rotation_acceleration(self):
        ra = 0
        for effect in self.effects:
            ra += effect.rotation_acceleration
        return self.rotation_acceleration + ra

    def draw(self):
        self.sprite.render(self.transform)

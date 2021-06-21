from .game_object import GameObject


class Emitter(GameObject):
    def __init__(
        self,
        environment,
        transform=None,
        particles=None,
        cooldown=1,
        to_live=-1
    ):
        super().__init__(transform=transform)

        self.environment = environment

        self.particles = particles

        self.next_spawn = 0
        self.cooldown = cooldown

        self.to_live = to_live
        self.infinite = True

        if self.to_live > 0:
            self.infinite = False

    def __destroy__(self):
        self.environment = None
        super().__destroy__()

    def update(self, dt):
        super().update(dt)

        if not self.infinite:
            self.to_live -= dt
            if self.to_live < 0:
                self.destroy()
                return

        if self.next_spawn > 0.0:
            self.next_spawn -= dt
            return

        self.next_spawn = self.cooldown

        for particle in self.particles(self):
            self.environment.particles.append(particle)

    def draw(self):
        pass

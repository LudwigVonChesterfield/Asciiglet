from .game_object import GameObject


class Emitter(GameObject):
    def __init__(self, environment, transform=None, particles=None):
        super().__init__(transform=transform)

        self.environment = environment

        self.particles = particles

        self.next_spawn = 0
        self.spawn_cooldown = 1

    def __destroy__(self):
        self.environment = None
        super().__destroy__()

    def update(self, dt):
        super().update(dt)

        if self.next_spawn > self.spawn_cooldown:
            self.next_spawn -= dt
            return

        self.next_spawn = self.spawn_cooldown

        for particle in self.particles(self):
            self.environment.particles.append(particle)

    def draw(self):
        pass

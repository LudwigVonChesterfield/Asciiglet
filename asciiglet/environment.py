import pyglet


class Environment:
    def __init__(self):
        self.window = self.create_window(width=1024, height=720)

        self.event_loop = self.create_event_loop()

        self.particles = []

    def create_event_loop(self, *args, **kwargs):
        e = pyglet.app.EventLoop(*args, **kwargs)

        @e.event
        def on_window_close(window):
            if window == self.window:
                e.exit()
                return pyglet.event.EVENT_HANDLED

        return e

    def create_window(self, *args, **kwargs):
        w = pyglet.window.Window(*args, **kwargs)

        @w.event
        def on_draw():
            self.draw(w)

        return w

    def run(self):
        """
        while True:
            dt = pyglet.clock.tick()

            for window in pyglet.app.windows:
                window.switch_to()
                window.dispatch_events()
                window.dispatch_event('on_draw')
                window.flip()

            for particle in self.particles:
                particle.update(dt)
        """
        def u(dt, interval):
            self.update(dt)

        pyglet.clock.schedule(u, .05)
        pyglet.app.run()

    def update(self, dt):
        for particle in self.particles:
            particle.update(dt)
            if particle.destroying:
                self.particles.remove(particle)

    def draw(self, window):
        window.clear()
        pyglet.gl.glLoadIdentity()

        for particle in self.particles:
            particle.draw()

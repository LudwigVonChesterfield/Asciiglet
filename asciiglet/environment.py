import pyglet

from .transform import Transform
from .vector import Vector


class Environment:
    def __init__(self, max_x=1024, max_y=720, width=1024, height=720, window=None, event_loop=None):
        if window is None:
            self.window = self.create_window(width=width, height=height)
        else:
            self.window = window

        self.max_x = max_x
        self.max_y = max_y

        self.width = width
        self.height = height

        scale_x = width / max_x
        scale_y = height / max_y

        self.center = Vector.new(max_x * 0.5, max_y * 0.5)
        self.origin = Vector.new(0.0, 0.0)

        self.transform = Transform(scale=Vector.new(scale_x, scale_y))

        if event_loop is None:
            self.event_loop = self.create_event_loop()
        else:
            self.event_loop = event_loop

        self.particles = []

        self.halt_after = -1
        self.iteration = 0

        self.on_update = None

    def reset_scale(self):
        self.transform.scale = self.window_size() / self.size()

    def set_window_size(self, width, height):
        self.width = width
        self.height = height

        self.window.set_size(width, height)

    def set_size(self, max_x, max_y):
        self.max_x = max_x
        self.max_y = max_y

    def window_size(self):
        return Vector.new(self.width, self.height)

    def size(self):
        return Vector.new(self.max_x, self.max_y)

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

    def run(self, halt_after=-1, on_update=None):
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
        def u(dt):
            self.iteration += 1
            if self.halt_after > 0 and self.iteration > self.halt_after:
                self.window.close()
                self.event_loop.exit()
                pyglet.clock.unschedule(u)
                return

            self.update(dt)

        self.halt_after = halt_after

        self.on_update = on_update

        pyglet.clock.schedule_interval(u, 0.05)
        pyglet.app.run()

    def update(self, dt):
        if self.on_update is not None:
            self.on_update(self, dt)

        for particle in self.particles:
            particle.update(self, dt)
            if particle.destroying:
                self.particles.remove(particle)

    def draw(self, window):
        window.clear()
        pyglet.gl.glLoadIdentity()

        for particle in self.particles:
            particle.draw(self, self.iteration)

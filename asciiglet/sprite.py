import pyglet

from pyglet.gl import *


class Sprite:
    colors = {
        "BLACK": (0, 0, 0, 255),
        "WHITE": (255, 255, 255, 255),
        "RED": (255, 0, 0, 255),
        "GREEN": (0, 255, 0, 255),
        "CYAN": (0, 255, 255, 255),
        "RUSTY": (139, 49, 3, 255),
        "ORANGE": (255, 125, 0, 255),
        "YELLOW": (255, 255, 0, 255),
        "PINK": (255, 105, 180, 255),
        "SIENNA": (160, 82, 45, 255),
        "BLUE": (0, 0, 255, 255),
        "PURPLE": (255, 0, 255, 255),
    }

    def __init__(self, sprite):
        self.sprite = sprite

        self.label = pyglet.text.Label(
            self.sprite,
            font_name='Consolas',
            font_size=13,
            anchor_x='right',
            anchor_y='center'
        )

        self._color = "WHITE"

        self.color = self._color

    def render(self, transform):
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

        glTranslatef(transform.pos[0], transform.pos[1], 0.0)
        glScalef(transform.scale[0], transform.scale[1], 1.0)
        glRotatef(transform.angle, 0.0, 0.0, 1.0)

        self.label.draw()

        glLoadIdentity()

    def set_sprite(self, new_sprite):
        self.label.text = new_sprite

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        if type(value) is str:
            value = self.colors[value]
        self._color = value
        self.label.color = value

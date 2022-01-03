"""
Compass Engine v 2.0.0
"""

import typing

import pygame
import toml
import uuid_by_string

from pygame.math import Vector2 as Vec2


VecLike = Vec2 | typing.Tuple[int, int]


def map_range(val, from_min, from_max, to_min, to_max):
    fromRange = from_max - from_min
    toRange = to_max - to_min
    sc = toRange / fromRange
    co = -1 * from_min * sc + to_min
    return val * sc + co


# fast lerp
def lerp_f(a, b, t):
    return a + t * (b - a)


# good lerp
def lerp_p(a, b, t):
    return (1 - t) * a + t * b


def blit_fit_rect(surface: pygame.Surface, image: pygame.Surface, rect: pygame.Rect):
    blit_im = pygame.transform.scale(image, (rect.w, rect.h))
    surface.blit(blit_im, (rect.x, rect.y), area=rect)


class Window:
    def __init__(self, title: str, res: typing.Tuple[int, int] | Vec2):
        self._title = title
        self._res = res
        self.screen = pygame.display.set_mode(res, pygame.RESIZABLE)
        pygame.display.set_caption(title)
        self.fullscreen = False
        self.mouse_state = {'left': 0, 'middle': 0, 'right': 0}

    def handle_compass_events(self, event):
        if event.type == pygame.VIDEORESIZE:
            self.res = (event.w, event.h)
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == pygame.BUTTON_LEFT:
                self.mouse_state['left'] = 1
            elif event.button == pygame.BUTTON_MIDDLE:
                self.mouse_state['middle'] = 1
            elif event.button == pygame.BUTTON_RIGHT:
                self.mouse_state['right'] = 1

    @property
    def res(self):
        return self._res

    @res.setter
    def res(self, value: typing.Tuple[int, int] | Vec2):
        self._res = value
        self.display = pygame.display.set_mode(value, pygame.RESIZABLE)

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value: str):
        self._title = value
        pygame.display.set_caption(value)


class Animation:
    def __init__(self, data):



class Entity:
    def __init__(self, data: str):
        self.data_folder = data
        self.data = toml.load(data)
        self.name = self.data['name']
        animations = self.data['animations']
        self.attributes = self.data['attributes']

        self.uuid = uuid_by_string.generate_uuid(data)

        self.is_flipped = False
        self.frame = 0
        self.animations = animations

        self.vel = Vec2(0, 0)
        self.weight = self.attributes['weight']

        self._x = 0
        self._y = 0
        self._rect = pygame.Rect(0, 0, 10, 10)  # (self.animations[0].get_width(), self.animations[0].get_height()))
        self.angle = 0

    def get_processed_image(self):
        image: pygame.Surface = self.animations[self.frame]
        if self.is_flipped:
            image = pygame.transform.flip(image, True, False)
        if self.angle != 0:
            image = pygame.transform.rotate(image, self.angle)
        return image

    def draw(self, surface: pygame.Surface, pos: VecLike):
        image = self.get_processed_image()
        surface.blit(image, pos)

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, val):
        self._x = val
        self._rect.x = val

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, val):
        self._y = val
        self._rect.y = val

    @property
    def rect(self):
        return self._rect

    @rect.setter
    def rect(self, val):
        self._rect = val
        self._x = val.x
        self._y = val.y


class Level:
    def __init__(self, tiles: typing.List[typing.List[int]], images: typing.List[pygame.Surface], tile_size: int):
        self.tiles = tiles
        self.images = images
        self.tile_size = tile_size

    def render(self, screen, pos: VecLike):
        for y, row in enumerate(self.tiles):
            for x, tile in enumerate(row):
                if tile is not None:
                    screen.blit(self.images[tile], (Vec2(x, y) * self.tile_size) + pos)


if __name__ == '__main__':
    player = Entity('data/Entities/Player.entity')

import sys
import typing
import random
from time import perf_counter

import pygame
import Engine

from pygame.math import Vector2 as Vec2


pygame.init()


class DebugOptions:
    def __init__(self):
        self.draw_hitboxes = False


def load_image(image, no_alpha=False):
    im = pygame.image.load(image)
    if no_alpha:
        im = im.convert()
    else:
        im = im.convert_alpha()
    return pygame.transform.scale2x(im)


if __name__ == '__main__':
    # Main Game Loop

    window = Engine.Window("Slimey Man go wee woo", (640, 448))

    player = Engine.Entity("data/Entities/Player.entity")
    player.y = -100

    clock = pygame.time.Clock()

    camera = Vec2(0, 0)

    dt = 1

    debug_options = DebugOptions()

    tree = load_image("data/Backgrounds/Tree.png")

    trees = [random.randint(-640, 640) for i in range(10)]

    tiles = [load_image('data/Tiles/dirt.png', True).convert()]
    level = Engine.Level([
        [1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    ], tiles, 64)

    physics_data = Engine.PhysicsData(1.8, level.rects, 0.9)

    def get_render_pos(pos: Vec2 | typing.Tuple[int, int]):
        pos = Vec2(pos) - camera + window.res / 2
        return Vec2(pos.x - player.rect.w / 2, pos.y + window.res.y / 15)

    while True:
        start_time = perf_counter()
        player.update(dt, physics_data)

        camera += (Vec2(player.x, player.y) - camera) / 16

        window.screen.fill((10, 10, 10))

        if debug_options.draw_hitboxes:
            for r in physics_data.rects:
                r_pos = get_render_pos(r.topleft)
                rect = pygame.Rect(*r_pos.xy, r.w, r.h)
                pygame.draw.rect(window.screen, (255, 255, 255), rect, 3)
            p_pos = get_render_pos(player.rect.topleft)
            pygame.draw.rect(window.screen, (0, 255, 0), pygame.Rect(*p_pos.xy, player.rect.w, player.rect.h))

        pygame.draw.rect(window.screen, (75, 105, 47), pygame.Rect(0, get_render_pos((0, -100)).y, *window.res.xy))

        for t in trees:
            window.screen.blit(tree, get_render_pos((t, -300)))

        level.render(window.screen, get_render_pos((0, 0)))

        player.draw(window.screen, get_render_pos(player.rect.topleft))

        pygame.display.update()

        for event in pygame.event.get():
            window.handle_compass_events(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            player.vel.x -= player.attributes['speed'] * dt
        if keys[pygame.K_d]:
            player.vel.x += player.attributes['speed'] * dt
        if keys[pygame.K_w] and player.collisions['down']:
            player.vel.y = -70

        if keys[pygame.K_b]:
            debug_options.draw_hitboxes = not debug_options.draw_hitboxes

        end_time = perf_counter()
        # print(end_time - start_time)
        dt = clock.tick(60) / 60

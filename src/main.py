import sys

import pygame
import Engine

from pygame.math import Vector2 as Vec2


pygame.init()


if __name__ == '__main__':
    # Main Game Loop

    window = Engine.Window("Slimey Man go wee woo", (640, 448))

    player = Engine.Entity("data/Entities/Player.entity")
    player.y = -50
    print(player.random_uuid)

    clock = pygame.time.Clock()

    camera = Vec2(0, 0)

    dt = 1

    tiles = [pygame.image.load('data/Tiles/dirt.png').convert()]
    level = Engine.Level([
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    ], tiles, 32)

    physics_data = Engine.PhysicsData(0.2, level.rects, 0.9)

    while True:

        player.update(dt, physics_data)

        camera += (Vec2(player.x, player.y) - camera) / 8

        window.screen.fill((10, 10, 10))

        level.render(window.screen, -camera)

        player.draw(window.screen, Vec2(player.rect.center) - camera)

        pygame.display.update()

        for event in pygame.event.get():
            window.handle_compass_events(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        dt = clock.tick(60) * 60

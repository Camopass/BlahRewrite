import sys

import pygame
import Engine


pygame.init()


if __name__ == '__main__':
    # Main Game Loop

    window = Engine.Window("Slimey Man go wee woo", (500, 400))

    player = Engine.Entity("data/Entities/Player.entity")
    print(player.random_uuid)

    clock = pygame.time.Clock()

    while True:
        window.screen.fill((255, 255, 255))
        player.draw(window.screen, player.rect.center)

        pygame.display.update()

        for event in pygame.event.get():
            window.handle_compass_events(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        dt = clock.tick(60)

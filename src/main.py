import pygame
import Engine


pygame.init()


if __name__ == '__main__':
    # Main Game Loop

    window = Engine.Window("Slimey Man go wee woo", (500, 400))

    player = Engine.Entity("data/Entities/Player.entity")

    clock = pygame.time.Clock()

    while True:
        window.screen.fill((255, 255, 255))
        player.draw(window.screen, player.rect.xy)

        window.screen.blit()
        pygame.display.update()

        for event in pygame.event.get():
            window.handle_compass_events(event)
            if event.type == pygame.QUIT:
                pygame.quit()

    dt = clock.tick(60)

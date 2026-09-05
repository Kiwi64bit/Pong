import pygame
from game import Game


def main() -> None:
    pygame.init()

    game = Game((1280, 720), "Pong")

    run: bool = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        game.update(pygame.key.get_pressed())
        game.render()

        # Updating window
        pygame.display.flip()
        game.clock.tick(game.FPS)

    pygame.quit()


if __name__ == '__main__':
    main()

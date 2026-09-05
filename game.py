from typing import Sequence

import pygame
from pygame import Clock, Vector2, Surface
from pygame.math import clamp
from pygame.typing import SequenceLike

from ball import Ball
from paddle import Paddle


class Game:
    def __init__(self, size: SequenceLike[float], title: str, fps: int = 60):
        self.size: Vector2 = Vector2(size)
        self.surface: Surface = pygame.display.set_mode(size)
        self.clock: Clock = Clock()
        self.FPS: int = fps

        pygame.display.set_caption(title)

        self.player1: Paddle = Paddle(
                color="#FFFFFF",
                position=(15, self.size.y / 2),
                size=(10, 140),
                speed=10,
                controls={'up': pygame.K_w, 'down': pygame.K_s, },
        )

        self.player2: Paddle = Paddle(
                color="#FFFFFF",
                position=(self.size.x - 15, self.size.y / 2),
                size=(10, 140),
                speed=10,
                controls={'up': pygame.K_UP, 'down': pygame.K_DOWN},
        )

        self.ball: Ball = Ball(
                "#FFFFFF",
                10,
                self.size / 2,
                10,
        )

    def update(self, keys: Sequence[bool]) -> None:
        self.player1.update(keys)
        self.player2.update(keys)
        self.ball.update()
        self.handle_collision()

    def render(self) -> None:
        self.draw_background()
        self.player1.draw(self.surface)
        self.player2.draw(self.surface)
        self.ball.draw(self.surface)
        self.render_score()

    def handle_collision(self) -> None:
        self.player1.rect.top = clamp(
                self.player1.rect.top,
                0,
                self.size.y - self.player1.rect.height,
        )

        self.player2.rect.top = clamp(
                self.player2.rect.top,
                0,
                self.size.y - self.player2.rect.height,
        )

        if not (0 < self.ball.rect.top < self.size.y - self.ball.rect.height):
            self.ball.velocity.y *= -1

        if self.ball.rect.left < 0:
            self.ball.rect.center = self.size / 2
            self.ball.velocity.x *= -1
            self.player2.score += 1

        if self.ball.rect.right > self.size.x:
            self.ball.rect.center = self.size / 2
            self.ball.velocity.x *= -1
            self.player1.score += 1

        if self.ball.rect.colliderect(self.player1.rect):
            self.ball.velocity.x *= -1
            self.ball.rect.left = self.player1.rect.right
        if self.ball.rect.colliderect(self.player2.rect):
            self.ball.velocity.x *= -1
            self.ball.rect.right = self.player2.rect.left

    def draw_background(self) -> None:
        self.surface.fill('#1e1e28')
        pygame.draw.aaline(
                self.surface,
                "#ffffff",
                (self.size.x / 2, 0),
                (self.size.x / 2, self.size.y),
        )
        pygame.draw.aacircle(self.surface, '#ffffff', self.size / 2, 120, 1)
        pygame.draw.aacircle(self.surface, '#ffffff', self.size / 2, 3)

    def render_score(self) -> None:
        font: pygame.Font = pygame.font.Font(size=30)

        score1 = font.render(str(self.player1.score), True, "#ffffff")
        self.surface.blit(
                score1,
                self.size / 2 + (-30, 0) - Vector2(score1.size) / 2,
        )

        score2 = font.render(str(self.player2.score), True, "#ffffff")
        self.surface.blit(
                score2,
                self.size / 2 + (30, 0) - Vector2(score2.size) / 2,
        )

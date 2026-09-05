import pygame
from pygame import Rect, Vector2, Surface, Color
from pygame.typing import ColorLike, SequenceLike


class Ball:
    def __init__(
            self,
            color: ColorLike,
            radius: int,
            position: SequenceLike[float],
            speed: int,
    ) -> None:
        self.color: Color = Color(color)
        self.radius: int = radius
        self.rect: Rect = Rect((0, 0), (radius * 2, radius * 2))
        self.rect.center = position
        self.velocity: Vector2 = Vector2(1, 1).normalize() * speed

    def update(self) -> None:
        self.rect.center += self.velocity

    def draw(self, surface: Surface) -> None:
        pygame.draw.aacircle(surface, self.color, self.rect.center, self.radius)

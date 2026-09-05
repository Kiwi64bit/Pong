from typing import Sequence, TypeAlias

import pygame
from pygame import Color, Vector2, Rect, Surface
from pygame.typing import ColorLike, SequenceLike

KeyMap: TypeAlias = dict[str, int]


class Paddle:
    def __init__(
            self,
            color: ColorLike,
            size: SequenceLike[float],
            position: SequenceLike[float],
            speed: int,
            controls: KeyMap = None,
    ) -> None:
        if controls is None:
            controls = {
                    'up'  : pygame.K_UP,
                    'down': pygame.K_DOWN,
            }

        self.color: Color = Color(color)
        self.size: Vector2 = Vector2(size)
        self.rect: Rect = Rect((0, 0), size)
        self.rect.center = position
        self.speed: int = speed
        self.controls: KeyMap = controls
        self.score: int = 0

    def update(self, keys: Sequence[bool]) -> None:
        if keys[self.controls['up']]:
            self.move_up()
        if keys[self.controls['down']]:
            self.move_down()

    def move_up(self) -> None:
        self.rect.y += -1 * self.speed

    def move_down(self) -> None:
        self.rect.y += 1 * self.speed

    def draw(self, surface: Surface) -> None:
        pygame.draw.rect(surface, self.color, self.rect)

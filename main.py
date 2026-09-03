import pygame
from pygame import Vector2


pygame.init()


def lerp(a, b, t):
    return a * (1 - t) + b * t


# Game Class
class Game:
    def __init__(self, size, title):
        self.size = Vector2(size)
        self.surface = pygame.display.set_mode(size)
        self.clock = pygame.Clock()
        self.FPS = 60

        self.run = False
        pygame.display.set_caption(title)

    def draw_background(self):
        self.surface.fill('#1e1e28')
        pygame.draw.aaline(game.surface, "#ffffff", (self.size.x / 2, 0), (self.size.x / 2, self.size.y))
        pygame.draw.aacircle(game.surface, '#ffffff', game.size / 2, 120, 1)
        pygame.draw.aacircle(game.surface, '#ffffff', game.size / 2, 3)

    def render_text(self):
        score_font = pygame.font.SysFont('JetBrainsMonoRegular', 30)

        score1 = score_font.render(str(player1.score), True, "#ffffff")
        self.surface.blit(score1, self.size / 2 + Vector2(-30, 0) - Vector2(score1.size) / 2)

        score2 = score_font.render(str(player2.score), True, "#ffffff")
        self.surface.blit(score2, self.size / 2 + Vector2(30, 0) - Vector2(score2.size) / 2)

        ticks = score_font.render(f'{pygame.time.get_ticks() / 1000:.2f}s', True, "#ffffff")
        self.surface.blit(ticks, (0, 0))

        self.cooldown_timer()

    def cooldown_timer(self):
        duration = pygame.time.get_ticks() - ball.score_time
        t = (duration / 1000) % 1

        if duration < 3000:
            timer_font = pygame.font.SysFont('jetbrainsmonoregular', round(lerp(40, 100, t)))
            timer_surface = pygame.Surface(lerp(Vector2(40, 40), Vector2(100, 100), t), pygame.SRCALPHA)
            timer_rect = timer_surface.get_rect()
            timer_rect.center = self.size / 2
            pygame.draw.aacircle(timer_surface, '#ffffff', Vector2(timer_surface.size) / 2, lerp(20, 50, t))
            timer_surface.set_alpha(lerp(255, 0, t ** 0.25))

            number = timer_font.render(str(3 - duration // 1000), True, "#000000")
            text_rect = number.get_rect()
            text_rect.center = self.size / 2

            self.surface.blit(timer_surface, timer_rect)
            self.surface.blit(number, text_rect)


# Racket Class
class Racket:
    # Constants

    # Methods
    def __init__(self, color, pos, size, velocity, ai, controls=(pygame.K_UP, pygame.K_DOWN)):
        self.rect = pygame.Rect((0, 0), size)
        self.color = color
        self.velocity = Vector2(velocity)
        self.ai = ai
        self.controls = controls
        self.rect.center = pos
        self.score = 0
        self.font = pygame.font.SysFont("cambriamath", 20)

    def move(self):
        # Movement
        if not self.ai:
            if pygame.key.get_pressed()[self.controls[0]]:
                self.rect.centery -= self.velocity.y

            if pygame.key.get_pressed()[self.controls[1]]:
                self.rect.centery += self.velocity.y

        if self.ai:
            self.rect.centery = ball.rect.centery

        # Check bounds
        if self.rect.top < 0:
            self.rect.top = 0

        if self.rect.bottom > game.surface.height:
            self.rect.bottom = game.surface.height

        pygame.draw.rect(game.surface, self.color, self.rect)


# Ball Class
class Ball:
    # Constants

    # Methods
    def __init__(self, color, pos, radius, velocity):
        self.color = color
        self.radius = radius
        self.init_velocity = Vector2(velocity)
        self.velocity = Vector2(velocity)
        self.rect = pygame.Rect((0, 0), (radius * 2, radius * 2))
        self.rect.center = pos
        self.score_time = pygame.time.get_ticks()

    def reset(self):
        self.velocity.x *= -1
        self.rect.center = Vector2(game.surface.size) / 2
        self.score_time = pygame.time.get_ticks()

    def move(self):
        if pygame.time.get_ticks() - self.score_time < 3 * 1000:
            self.velocity = Vector2()
        else:
            self.velocity = self.init_velocity

        self.rect.center += self.velocity

        # Check bounds
        if self.rect.top <= 0 or self.rect.bottom >= game.surface.height:
            self.velocity.y *= -1

        if self.rect.left <= 0:
            player2.score += 1
            self.reset()

        if self.rect.right >= game.surface.width:
            player1.score += 1
            self.reset()

        # Check collision
        if self.rect.colliderect(player1.rect):
            self.rect.left = player1.rect.right
            self.velocity.x *= -1

        if self.rect.colliderect(player2.rect):
            self.rect.right = player2.rect.left
            self.velocity.x *= -1

        pygame.draw.aacircle(game.surface, self.color, self.rect.center, self.radius)


# Game
game = Game((1280, 720), "Pong")

# Objects
ball = Ball(color="#FFFFFF",
            pos=0.5 * Vector2(game.surface.size),
            radius=10,
            velocity=(5, 5))

player1 = Racket(color="#FFFFFF",
                 pos=(15, game.surface.height / 2),
                 size=(10, 140),
                 velocity=(0, 10),
                 ai=True,
                 controls=[pygame.K_w, pygame.K_s])

player2 = Racket(color="#FFFFFF",
                 pos=(game.surface.width - 15, game.surface.height / 2),
                 size=(10, 140),
                 velocity=(0, 10),
                 ai=False)

# Main loop
game.run = True
while game.run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game.run = False

    # Background
    game.draw_background()

    # objects
    ball.move()
    player1.move()
    player2.move()

    # Text
    game.render_text()

    # Updating window
    pygame.display.flip()
    game.clock.tick(game.FPS)

pygame.quit()

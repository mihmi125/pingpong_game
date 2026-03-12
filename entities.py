"""
Logic for game world objects.
Handles physics, autonomous movement (AI), and visual effects.
"""
import pygame
import random
from constants import *

class Particle:
    """A single spark effect that moves and fades over time."""
    def __init__(self, x, y, color):
        self.x, self.y = x, y
        # Velocity randomized for 'explosion' feel
        self.vx, self.vy = random.uniform(-4, 4), random.uniform(-4, 4)
        self.lifetime = 255
        self.color = color

    def update(self):
        """Move particle and decrease its visibility."""
        self.x += self.vx
        self.y += self.vy
        self.lifetime -= 12

    def draw(self, surface):
        """Render particle with alpha transparency."""
        if self.lifetime > 0:
            s = pygame.Surface((3, 3))
            s.set_alpha(self.lifetime)
            s.fill(self.color)
            surface.blit(s, (self.x, self.y))

class Paddle(pygame.Rect):
    """
    Extends pygame.Rect to represent a player's paddle.
    Includes collision detection and movement boundaries.
    """
    def __init__(self, x, y, color):
        super().__init__(x, y, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.color = color
        self.speed = 0

    def move_manual(self):
        """Update position based on keyboard input and clamp to screen."""
        self.y = max(0, min(HEIGHT - PADDLE_HEIGHT, self.y + self.speed))

    def move_cpu(self, ball_y, cpu_speed, error_margin):
        """
        AI logic that tracks the ball.
        Moves only if ball is outside 'error_margin' for human-like delay.
        """
        if abs(self.center[1] - ball_y) > error_margin:
            if self.center[1] < ball_y: self.y += cpu_speed
            else: self.y -= cpu_speed
        self.y = max(0, min(HEIGHT - PADDLE_HEIGHT, self.y))

class Ball(pygame.Rect):
    """Handles ball movement and resets."""
    def __init__(self, base_speed):
        super().__init__(WIDTH//2, HEIGHT//2, BALL_SIZE, BALL_SIZE)
        self.base_speed = base_speed
        self.vx = base_speed
        self.vy = base_speed

    def update(self):
        """Standard linear movement."""
        self.x += self.vx
        self.y += self.vy

    def reset(self):
        """Reset ball to center with randomized starting direction."""
        self.center = (WIDTH // 2, HEIGHT // 2)
        self.vx = self.base_speed * random.choice((1, -1))
        self.vy = self.base_speed * random.choice((1, -1))
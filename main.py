"""
Neon Pong - Main Application.
The 'orchestrator' file that runs the game loop and state machine.
"""
import pygame
import sys
import random
from constants import *
from entities import Paddle, Ball, Particle
from ui import Interface
from audio import AudioManager

class Game:
    """
    Primary class that manages the application lifecycle.
    Controls events, physics updates, and visual rendering.
    """
    def __init__(self):
        """Initialize the game engine and world state."""
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Neon Pong")
        self.clock = pygame.time.Clock()

        # Core Managers
        self.ui = Interface()
        self.audio = AudioManager()

        # Session State
        self.state = "MENU"
        self.winning_score = DEFAULT_WINNING_SCORE
        self.score_a = 0
        self.score_b = 0
        self.screen_shake = 0

        # World Entities
        self.player_a = Paddle(50, HEIGHT//2 - 50, CYAN)
        self.player_b = Paddle(WIDTH - 50 - PADDLE_WIDTH, HEIGHT//2 - 50, MAGENTA)
        self.ball = Ball(INITIAL_BALL_SPEED)
        self.particles = []

        # UI Attribute Initialization (PEP 8 Compliance)
        self.btn_cpu = pygame.Rect(0,0,0,0)
        self.btn_pvp = pygame.Rect(0,0,0,0)
        self.btn_set = pygame.Rect(0,0,0,0)
        self.btn_plus = pygame.Rect(0,0,0,0)
        self.btn_minus = pygame.Rect(0,0,0,0)
        self.btn_back = pygame.Rect(0,0,0,0)

    def spawn_particles(self, x, y, color):
        """Create visual explosion on impact."""
        for _ in range(10):
            self.particles.append(Particle(x, y, color))

    def handle_events(self):
        """Process keyboard and mouse inputs."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_clicks(event.pos)

            if event.type == pygame.KEYDOWN:
                # Player 1 Controls
                if event.key == pygame.K_w: self.player_a.speed = -PLAYER_SPEED
                if event.key == pygame.K_s: self.player_a.speed = PLAYER_SPEED
                # Player 2 Controls (PVP Only)
                if self.state == "PVP":
                    if event.key == pygame.K_UP: self.player_b.speed = -PLAYER_SPEED
                    if event.key == pygame.K_DOWN: self.player_b.speed = PLAYER_SPEED
                if event.key == pygame.K_ESCAPE: self.state = "MENU"

            if event.type == pygame.KEYUP:
                if event.key in (pygame.K_w, pygame.K_s): self.player_a.speed = 0
                if event.key in (pygame.K_UP, pygame.K_DOWN): self.player_b.speed = 0

    def handle_clicks(self, pos):
        """Route menu interactions based on current state."""
        if self.state == "MENU":
            if self.btn_cpu.collidepoint(pos): self.reset_match("PVCPU")
            if self.btn_pvp.collidepoint(pos): self.reset_match("PVP")
            if self.btn_set.collidepoint(pos): self.state = "SETTINGS"
        elif self.state == "SETTINGS":
            if self.btn_plus.collidepoint(pos): self.winning_score += 1
            if self.btn_minus.collidepoint(pos) and self.winning_score > 1: self.winning_score -= 1
            if self.btn_back.collidepoint(pos): self.state = "MENU"
        elif self.state == "GAMEOVER":
            if self.btn_back.collidepoint(pos): self.state = "MENU"

    def reset_match(self, mode):
        """Prepare for a new game session."""
        self.score_a = self.score_b = 0
        self.state = mode
        self.ball.reset()

    def update(self):
        """Main physics and collision logic."""
        if self.state in ["PVCPU", "PVP"]:
            self.player_a.move_manual()
            if self.state == "PVCPU":
                self.player_b.move_cpu(self.ball.y, CPU_SPEED, CPU_ERROR_MARGIN)
            else:
                self.player_b.move_manual()

            self.ball.update()

            # Boundary Physics
            if self.ball.top <= 0 or self.ball.bottom >= HEIGHT:
                self.ball.vy *= -1
                self.audio.play_sfx("hit")
                self.spawn_particles(self.ball.centerx, self.ball.centery, WHITE)

            # Collision Logic (with Ball Acceleration)
            if self.ball.colliderect(self.player_a) and self.ball.vx < 0:
                self.ball.vx *= -1.1
                self.screen_shake = 8
                self.audio.play_sfx("hit")
                self.spawn_particles(self.ball.left, self.ball.centery, CYAN)

            if self.ball.colliderect(self.player_b) and self.ball.vx > 0:
                self.ball.vx *= -1.1
                self.screen_shake = 8
                self.audio.play_sfx("hit")
                self.spawn_particles(self.ball.right, self.ball.centery, MAGENTA)

            # Scoring States
            if self.ball.left <= 0:
                self.score_b += 1
                self.audio.play_sfx("score")
                if self.score_b >= self.winning_score: self.state = "GAMEOVER"
                else: self.ball.reset()
            elif self.ball.right >= WIDTH:
                self.score_a += 1
                self.audio.play_sfx("score")
                if self.score_a >= self.winning_score: self.state = "GAMEOVER"
                else: self.ball.reset()

            # Visual Effect Logic
            for p in self.particles[:]:
                p.update()
                if p.lifetime <= 0: self.particles.remove(p)

    def draw(self):
        """Coordinate rendering of the game world and UI."""
        # Calculate Screen Shake Offset
        offset = [random.randint(-self.screen_shake, self.screen_shake) for _ in range(2)] if self.screen_shake > 0 else [0,0]
        if self.screen_shake > 0: self.screen_shake -= 1

        self.screen.fill(BLACK)

        if self.state == "MENU":
            self.ui.draw_text(self.screen, "NEON PONG", "font_title", MAGENTA, 150)
            self.btn_cpu = self.ui.button(self.screen, "PLAYER vs CPU", 300)
            self.btn_pvp = self.ui.button(self.screen, "PLAYER vs PLAYER", 380)
            self.btn_set = self.ui.button(self.screen, "SETTINGS", 460)

        elif self.state == "SETTINGS":
            self.ui.draw_text(self.screen, "SETTINGS", "font_title", CYAN, 150)
            self.ui.draw_text(self.screen, f"WINNING SCORE: {self.winning_score}", "font_ui", WHITE, 300)
            self.btn_plus = self.ui.button(self.screen, "+", 300, x_pos=WIDTH//2 + 200)
            self.btn_minus = self.ui.button(self.screen, "-", 300, x_pos=WIDTH//2 - 200)
            self.btn_back = self.ui.button(self.screen, "BACK", 450)

        elif self.state == "GAMEOVER":
            winner = "P1" if self.score_a >= self.winning_score else "P2/CPU"
            self.ui.draw_text(self.screen, f"{winner} WINS!", "font_title", CYAN, 150)
            self.btn_back = self.ui.button(self.screen, "MAIN MENU", 350)

        else:
            # Render Active Playfield
            self.ui.draw_center_line(self.screen)
            for p in self.particles: p.draw(self.screen)

            # Entities rendered with offset for impact shake
            pygame.draw.ellipse(self.screen, WHITE, self.ball.move(offset[0], offset[1]))
            pygame.draw.rect(self.screen, CYAN, self.player_a.move(offset[0], offset[1]))
            pygame.draw.rect(self.screen, MAGENTA, self.player_b.move(offset[0], offset[1]))

            self.ui.draw_text(self.screen, f"{self.score_a}   {self.score_b}", "font_ui", WHITE, 50)
            self.ui.draw_text(self.screen, f"SPEED: {round(abs(self.ball.vx), 1)}", "font_small", GRAY, HEIGHT - 30, x_pos=WIDTH - 80)

        pygame.display.flip()

    def run(self):
        """Execute the continuous game loop."""
        while True:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

if __name__ == "__main__":
    Game().run()
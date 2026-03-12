"""
Interface management module.
Renders text, handles button logic, and decorative UI layers.
"""
import pygame
from constants import *

class Interface:
    """Manages all graphical user interface elements."""
    def __init__(self):
        # Initialize different font sizes for hierarchy
        self.font_title = pygame.font.Font(None, 100)
        self.font_ui = pygame.font.Font(None, 40)
        self.font_small = pygame.font.Font(None, 30)

    def draw_text(self, screen, text, font_type, color, y_pos, x_pos=WIDTH//2):
        """Helper method to render centered text strings."""
        font = getattr(self, font_type)
        text_surf = font.render(text, True, color)
        text_rect = text_surf.get_rect(center=(x_pos, y_pos))
        screen.blit(text_surf, text_rect)

    def button(self, screen, text, y_pos, x_pos=WIDTH//2):
        """
        Renders an interactive button.
        Returns the clickable Rect for event handling.
        """
        text_surf = self.font_ui.render(text, True, WHITE)
        rect = text_surf.get_rect(center=(x_pos, y_pos))
        click_area = rect.inflate(40, 20)
        is_hovered = click_area.collidepoint(pygame.mouse.get_pos())

        # Color feedback for hover state
        color = CYAN if is_hovered else WHITE
        if is_hovered:
            pygame.draw.rect(screen, DARK_GRAY, click_area, border_radius=10)

        screen.blit(self.font_ui.render(text, True, color), rect)
        return click_area

    def draw_center_line(self, screen):
        """Renders the retro dashed line in the middle of the playfield."""
        for y in range(0, HEIGHT, 40):
            pygame.draw.rect(screen, LINE_COLOR, (WIDTH // 2 - 2, y, 4, 20))
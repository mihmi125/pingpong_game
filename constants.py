"""
Global configuration for Neon Pong.
Contains window dimensions, gameplay physics, and the color palette.
"""

# Window & Performance
WIDTH, HEIGHT = 800, 600
FPS = 60

# Physical Dimensions
PADDLE_WIDTH, PADDLE_HEIGHT = 15, 100
BALL_SIZE = 15

# Gameplay Balancing
DEFAULT_WINNING_SCORE = 5
INITIAL_BALL_SPEED = 6
PLAYER_SPEED = 7
CPU_SPEED = 5.5
CPU_ERROR_MARGIN = 25  # Lower value = harder CPU

# Color Palette (RGB)
WHITE   = (255, 255, 255)
BLACK   = (20, 20, 20)
CYAN    = (0, 255, 255)
MAGENTA = (255, 0, 255)
GRAY    = (60, 60, 60)
LINE_COLOR = (40, 40, 40)  # Subdued color for background elements
DARK_GRAY = (30, 30, 30)   # Used for button hover states
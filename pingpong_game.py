import pygame
import sys

# --- 1. Initialization and Setup ---
# Initialize Pygame modules
pygame.init()

# Define constants
WIDTH, HEIGHT = 800, 600
PADDLE_WIDTH, PADDLE_HEIGHT = 15, 100
BALL_SIZE = 15
FPS = 60 # Frames Per Second for smooth animation

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# Setup the window (surface)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame Pong")
clock = pygame.time.Clock()

# --- 2. Game Objects ---

# Paddles (Rectangles)
# Rect(left, top, width, height)
player_a = pygame.Rect(50, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
player_b = pygame.Rect(WIDTH - 50 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)

# Ball (Rectangle)
ball = pygame.Rect(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)

# Movement Speeds
player_a_speed = 0
player_b_speed = 0
ball_x_speed = 4
ball_y_speed = 4

# Score
score_a = 0
score_b = 0
font = pygame.font.Font(None, 74) # Default font, size 74

# --- 3. Game Functions ---

def move_paddles():
    """Moves paddles and ensures they stay within the screen boundaries."""
    # Player A
    player_a.y += player_a_speed
    if player_a.top < 0:
        player_a.top = 0
    if player_a.bottom > HEIGHT:
        player_a.bottom = HEIGHT

    # Player B
    player_b.y += player_b_speed
    if player_b.top < 0:
        player_b.top = 0
    if player_b.bottom > HEIGHT:
        player_b.bottom = HEIGHT

def move_ball():
    """Moves the ball and handles wall/paddle collisions and scoring."""
    global ball_x_speed, ball_y_speed, score_a, score_b

    ball.x += ball_x_speed
    ball.y += ball_y_speed

    # Top/Bottom Wall Collision
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_y_speed *= -1

    # Scoring (Left/Right Wall)
    if ball.left <= 0:
        score_b += 1
        reset_ball()
    elif ball.right >= WIDTH:
        score_a += 1
        reset_ball()

    # Paddle Collisions
    # Check if ball hits Paddle A (Left)
    if ball.colliderect(player_a):
        # Move ball back slightly to prevent sticking
        ball.left = player_a.right
        ball_x_speed *= -1

    # Check if ball hits Paddle B (Right)
    if ball.colliderect(player_b):
        # Move ball back slightly to prevent sticking
        ball.right = player_b.left
        ball_x_speed *= -1

def reset_ball():
    """Resets the ball to the center and reverses its horizontal direction."""
    global ball_x_speed, ball_y_speed
    ball.center = (WIDTH // 2, HEIGHT // 2)
    # Give the point winner the serve (reverse the horizontal direction)
    ball_x_speed *= -1

def draw_elements():
    """Draws all game elements on the screen."""
    screen.fill(BLACK)
    
    # Draw Paddles and Ball
    pygame.draw.rect(screen, WHITE, player_a)
    pygame.draw.rect(screen, WHITE, player_b)
    pygame.draw.ellipse(screen, WHITE, ball)
    
    # Draw Center Line (Optional)
    pygame.draw.aaline(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))

    # Draw Score
    text_a = font.render(str(score_a), 1, WHITE)
    screen.blit(text_a, (WIDTH // 4, 20))
    text_b = font.render(str(score_b), 1, WHITE)
    screen.blit(text_b, (WIDTH * 3 // 4 - text_b.get_width(), 20))


# --- 4. Main Game Loop ---
running = True
while running:
    # Event Handling (Input)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()

        # Keypress DOWN
        if event.type == pygame.KEYDOWN:
            # Player A (W/S)
            if event.key == pygame.K_w:
                player_a_speed = -6
            if event.key == pygame.K_s:
                player_a_speed = 6
            # Player B (Up/Down)
            if event.key == pygame.K_UP:
                player_b_speed = -6
            if event.key == pygame.K_DOWN:
                player_b_speed = 6

        # Keypress UP (Stop movement)
        if event.type == pygame.KEYUP:
            # Player A
            if event.key == pygame.K_w or event.key == pygame.K_s:
                player_a_speed = 0
            # Player B
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                player_b_speed = 0

    # Game Logic Updates
    move_paddles()
    move_ball()
    
    # Drawing
    draw_elements()

    # Update the full display Surface to the screen
    pygame.display.flip()
    
    # Control the frame rate
    clock.tick(FPS)
import pygame
import random

# Initialize pygame
pygame.init()

# Screen dimensions
width = 800
height = 600

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)

# Create the game window
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pong")

# Paddle settings
paddle_width = 10
paddle_height = 100
paddle_speed = 10

# Ball settings
ball_radius = 10
ball_speed_x = 7
ball_speed_y = 7

# Scoring
player1_score = 0
player2_score = 0
font = pygame.font.SysFont("comicsansms", 35)
small_font = pygame.font.SysFont("comicsansms", 20)  # Smaller font for "Press X to Quit"

# Player paddles
player1_paddle = pygame.Rect(50, height // 2 - paddle_height // 2, paddle_width, paddle_height)
player2_paddle = pygame.Rect(width - 50 - paddle_width, height // 2 - paddle_height // 2, paddle_width, paddle_height)

# Ball
ball = pygame.Rect(width // 2 - ball_radius, height // 2 - ball_radius, ball_radius * 2, ball_radius * 2)

# Clock to control frame rate
clock = pygame.time.Clock()

# AI difficulty (easier version)
ai_speed = 7  # Reduced speed for easier AI
ai_reaction_delay =  0# Number of frames to wait before the AI reacts
ai_reaction_counter = 0  # Counter to track reaction delay

def draw_game():
    screen.fill(black)
    pygame.draw.rect(screen, red, player1_paddle)
    pygame.draw.rect(screen, blue, player2_paddle)
    pygame.draw.ellipse(screen, white, ball)
    pygame.draw.aaline(screen, white, (width // 2, 0), (width // 2, height))

    # Display scores
    score_text = font.render(f"{player1_score} - {player2_score}", True, white)
    screen.blit(score_text, (width // 2 - score_text.get_width() // 2, 20))

    # Display "Press X to Quit" at the top right corner
    quit_text = small_font.render("Press X to Quit", True, white)
    screen.blit(quit_text, (width - quit_text.get_width() - 10, 10))

    pygame.display.flip()

def handle_paddle_movement(keys, paddle, up_key, down_key):
    if keys[up_key] and paddle.top > 0:
        paddle.y -= paddle_speed
    if keys[down_key] and paddle.bottom < height:
        paddle.y += paddle_speed

def ai_move(ball, paddle):
    global ai_reaction_counter

    # Delay AI reaction
    if ai_reaction_counter < ai_reaction_delay:
        ai_reaction_counter += 1
        return
    ai_reaction_counter = 0  # Reset counter after reacting

    # Add randomness to AI movement for imperfection
    if random.random() > 0.3:  # 70% chance to follow the ball
        if paddle.centery < ball.centery and paddle.bottom < height:
            paddle.y += ai_speed
        elif paddle.centery > ball.centery and paddle.top > 0:
            paddle.y -= ai_speed

def reset_ball():
    ball.x = width // 2 - ball_radius
    ball.y = height // 2 - ball_radius
    return random.choice((-1, 1)) * ball_speed_x, random.choice((-1, 1)) * ball_speed_y

def game_loop(single_player):
    global ball_speed_x, ball_speed_y, player1_score, player2_score
    ball_speed_x, ball_speed_y = reset_ball()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit'  # Properly handle quitting the game

        keys = pygame.key.get_pressed()

        # Handle quitting to menu
        if keys[pygame.K_x]:
            return 'menu'  # Return to the menu screen

        handle_paddle_movement(keys, player1_paddle, pygame.K_w, pygame.K_s)

        if single_player:
            ai_move(ball, player2_paddle)  # AI control for the second paddle
        else:
            handle_paddle_movement(keys, player2_paddle, pygame.K_UP, pygame.K_DOWN)

        # Move the ball
        ball.x += ball_speed_x
        ball.y += ball_speed_y

        # Ball collision with top and bottom walls
        if ball.top <= 0 or ball.bottom >= height:
            ball_speed_y *= -1

        # Ball collision with paddles
        if ball.colliderect(player1_paddle) or ball.colliderect(player2_paddle):
            ball_speed_x *= -1

        # Ball out of bounds (left and right)
        if ball.left <= 0:
            player2_score += 1
            ball_speed_x, ball_speed_y = reset_ball()
        if ball.right >= width:
            player1_score += 1
            ball_speed_x, ball_speed_y = reset_ball()

        # Draw everything
        draw_game()

        # Frame rate
        clock.tick(60)

def show_menu():
    screen.fill(black)
    title_text = font.render("Pong Game", True, white)
    single_player_text = font.render("Press 1 for Single Player", True, white)
    two_player_text = font.render("Press 2 for Two Player", True, white)

    screen.blit(title_text, (width // 2 - title_text.get_width() // 2, height // 3))
    screen.blit(single_player_text, (width // 2 - single_player_text.get_width() // 2, height // 2))
    screen.blit(two_player_text, (width // 2 - two_player_text.get_width() // 2, height // 2 + 50))

    pygame.display.flip()

def menu_loop():
    menu = True
    while menu:
        show_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    menu = False
                    result = game_loop(single_player=True)  # Start single player mode
                    if result == 'menu':
                        menu = True
                if event.key == pygame.K_2:
                    menu = False
                    result = game_loop(single_player=False)  # Start two player mode
                    if result == 'menu':
                        menu = True

# Start the menu loop
menu_loop()
#!/usr/bin/env python3
"""
🐍 Snake Game
A classic snake game built with Python and Pygame
"""

import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 20, 60)
GREEN = (0, 200, 0)
DARK_GREEN = (0, 100, 0)
YELLOW = (255, 215, 0)
GRAY = (50, 50, 50)

# Game settings
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE

# FPS
FPS = 10
SPEED_INCREMENT = 0.5
MAX_SPEED = 25

# Initialize display
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("🐍 Snake Game")
clock = pygame.time.Clock()

# Fonts
font = pygame.font.Font(None, 36)
large_font = pygame.font.Font(None, 72)


def draw_grid():
    """Draw the grid lines"""
    for x in range(0, WINDOW_WIDTH, GRID_SIZE):
        pygame.draw.line(screen, GRAY, (x, 0), (x, WINDOW_HEIGHT))
    for y in range(0, WINDOW_HEIGHT, GRID_SIZE):
        pygame.draw.line(screen, GRAY, (0, y), (WINDOW_WIDTH, y))


def draw_snake(snake):
    """Draw the snake"""
    for i, segment in enumerate(snake):
        if i == 0:
            pygame.draw.rect(screen, GREEN, 
                          (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, 
                           GRID_SIZE - 2, GRID_SIZE - 2),
                          border_radius=4)
        else:
            pygame.draw.rect(screen, DARK_GREEN,
                          (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE,
                           GRID_SIZE - 2, GRID_SIZE - 2),
                          border_radius=4)


def draw_food(food):
    """Draw the food"""
    pygame.draw.circle(screen, RED,
                     (food[0] * GRID_SIZE + GRID_SIZE // 2,
                      food[1] * GRID_SIZE + GRID_SIZE // 2),
                      GRID_SIZE // 2 - 2)


def draw_score(score):
    """Draw the current score"""
    score_text = font.render(f"Score: {score}", True, YELLOW)
    screen.blit(score_text, (10, 10))


def draw_game_over(score):
    """Draw the game over screen"""
    overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    overlay.set_alpha(180)
    overlay.fill(BLACK)
    screen.blit(overlay, (0, 0))
    
    game_over_text = large_font.render("GAME OVER", True, RED)
    score_text = font.render(f"Final Score: {score}", True, WHITE)
    restart_text = font.render("Press SPACE to restart or Q to quit", True, GRAY)
    
    screen.blit(game_over_text, 
                (WINDOW_WIDTH // 2 - game_over_text.get_width() // 2,
                 WINDOW_HEIGHT // 2 - 80))
    screen.blit(score_text,
                (WINDOW_WIDTH // 2 - score_text.get_width() // 2,
                 WINDOW_HEIGHT // 2))
    screen.blit(restart_text,
                (WINDOW_WIDTH // 2 - restart_text.get_width() // 2,
                 WINDOW_HEIGHT // 2 + 60))


def generate_food(snake):
    """Generate food in a position not occupied by snake"""
    while True:
        food = (random.randint(0, GRID_WIDTH - 1),
                random.randint(0, GRID_HEIGHT - 1))
        if food not in snake:
            return food


def reset_game():
    """Reset the game state"""
    snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2),
             (GRID_WIDTH // 2 - 1, GRID_HEIGHT // 2),
             (GRID_WIDTH // 2 - 2, GRID_HEIGHT // 2)]
    direction = (1, 0)
    food = generate_food(snake)
    score = 0
    speed = FPS
    paused = False
    game_over = False
    return snake, direction, food, score, speed, paused, game_over


def main():
    """Main game loop"""
    snake, direction, food, score, speed, paused, game_over = reset_game()
    
    running = True
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            elif event.type == pygame.KEYDOWN:
                if game_over:
                    if event.key == pygame.K_SPACE:
                        snake, direction, food, score, speed, paused, game_over = reset_game()
                    elif event.key == pygame.K_q:
                        running = False
                elif paused:
                    if event.key == pygame.K_SPACE:
                        paused = False
                else:
                    # Change direction (prevent 180 degree turns)
                    if (event.key == pygame.K_UP and direction != (0, 1)):
                        direction = (0, -1)
                    elif (event.key == pygame.K_DOWN and direction != (0, -1)):
                        direction = (0, 1)
                    elif (event.key == pygame.K_LEFT and direction != (1, 0)):
                        direction = (-1, 0)
                    elif (event.key == pygame.K_RIGHT and direction != (-1, 0)):
                        direction = (1, 0)
                    elif event.key == pygame.K_SPACE:
                        paused = True
                    elif event.key == pygame.K_q:
                        running = False
        
        if not game_over and not paused:
            # Move snake
            new_head = (snake[0][0] + direction[0],
                       snake[0][1] + direction[1])
            
            # Check wall collision
            if (new_head[0] < 0 or new_head[0] >= GRID_WIDTH or
                new_head[1] < 0 or new_head[1] >= GRID_HEIGHT):
                game_over = True
            
            # Check self collision
            elif new_head in snake:
                game_over = True
            
            else:
                snake.insert(0, new_head)
                
                # Check food collision
                if new_head == food:
                    score += 10
                    food = generate_food(snake)
                    # Increase speed
                    if score % 30 == 0 and speed < MAX_SPEED:
                        speed += SPEED_INCREMENT
                else:
                    snake.pop()
        
        # Drawing
        screen.fill(BLACK)
        draw_grid()
        draw_snake(snake)
        draw_food(food)
        draw_score(score)
        
        if paused:
            pause_text = large_font.render("PAUSED", True, YELLOW)
            screen.blit(pause_text,
                       (WINDOW_WIDTH // 2 - pause_text.get_width() // 2,
                        WINDOW_HEIGHT // 2 - pause_text.get_height() // 2))
        
        if game_over:
            draw_game_over(score)
        
        pygame.display.flip()
        clock.tick(speed)
    
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()

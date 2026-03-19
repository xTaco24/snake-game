#!/usr/bin/env python3
"""
🐍 Snake Game - Terminal Version
Built with Python's curses library (no external dependencies!)
Works with Python 3.14+
"""

import curses
import random
import time

def main(stdscr):
    # Setup
    curses.curs_set(0)
    stdscr.nodelay(1)
    stdscr.timeout(100)
    
    # Colors
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLACK)
    
    # Get terminal size
    sh, sw = stdscr.getmaxyx()
    
    # Game area (leave room for score)
    game_height = sh - 4
    game_width = sw - 2
    
    # Snake (center of screen)
    snake = [
        [game_height // 2, game_width // 2],
        [game_height // 2, game_width // 2 - 1],
        [game_height // 2, game_width // 2 - 2]
    ]
    
    # Direction (right)
    direction = [0, 1]
    
    # Food
    food = [random.randint(1, game_height - 2), random.randint(1, game_width - 2)]
    while food in snake:
        food = [random.randint(1, game_height - 2), random.randint(1, game_width - 2)]
    
    # Score
    score = 0
    
    # Game speed (ms)
    speed = 100
    
    # Game loop
    running = True
    game_over = False
    
    while running:
        stdscr.clear()
        
        # Draw border
        for i in range(game_width + 1):
            stdscr.addch(0, i, '#')
            stdscr.addch(game_height + 1, i, '#')
        for i in range(game_height + 2):
            stdscr.addch(i, 0, '#')
            stdscr.addch(i, game_width + 1, '#')
        
        # Draw score
        score_text = f" Score: {score} | SPACE: Pause | Q: Quit "
        stdscr.addstr(sh - 2, (sw - len(score_text)) // 2, score_text, curses.color_pair(3))
        
        if game_over:
            go_text = "GAME OVER!"
            stdscr.addstr(game_height // 2, (game_width - len(go_text)) // 2, go_text, curses.color_pair(2) | curses.A_BOLD)
            restart_text = "Press SPACE to restart or Q to quit"
            stdscr.addstr(game_height // 2 + 2, (game_width - len(restart_text)) // 2, restart_text, curses.color_pair(4))
        else:
            # Draw snake
            for i, segment in enumerate(snake):
                if 0 <= segment[0] < game_height + 1 and 0 <= segment[1] < game_width + 1:
                    char = 'O' if i == 0 else 'o'
                    stdscr.addch(segment[0], segment[1], char, curses.color_pair(1) | curses.A_BOLD)
            
            # Draw food
            if 0 <= food[0] < game_height + 1 and 0 <= food[1] < game_width + 1:
                stdscr.addch(food[0], food[1], '*', curses.color_pair(2) | curses.A_BOLD)
        
        stdscr.refresh()
        
        if not game_over:
            # Get input
            try:
                key = stdscr.getch()
            except:
                key = -1
            
            if key == ord('q') or key == ord('Q'):
                running = False
            elif key == ord(' '):
                # Pause
                paused = True
                while paused:
                    try:
                        pause_key = stdscr.getch()
                    except:
                        pause_key = -1
                    if pause_key == ord(' '):
                        paused = False
                    elif pause_key in [ord('q'), ord('Q')]:
                        running = False
                        paused = False
            elif key == curses.KEY_UP and direction != [1, 0]:
                direction = [-1, 0]
            elif key == curses.KEY_DOWN and direction != [-1, 0]:
                direction = [1, 0]
            elif key == curses.KEY_LEFT and direction != [0, 1]:
                direction = [0, -1]
            elif key == curses.KEY_RIGHT and direction != [0, -1]:
                direction = [0, 1]
            
            # Move snake
            new_head = [snake[0][0] + direction[0], snake[0][1] + direction[1]]
            
            # Check wall collision
            if new_head[0] <= 0 or new_head[0] >= game_height + 1 or new_head[1] <= 0 or new_head[1] >= game_width + 1:
                game_over = True
            # Check self collision
            elif new_head in snake:
                game_over = True
            else:
                snake.insert(0, new_head)
                
                # Check food
                if new_head == food:
                    score += 10
                    food = [random.randint(1, game_height - 2), random.randint(1, game_width - 2)]
                    while food in snake:
                        food = [random.randint(1, game_height - 2), random.randint(1, game_width - 2)]
                    # Increase speed
                    if score % 30 == 0 and speed > 30:
                        speed -= 5
                        stdscr.timeout(speed)
                else:
                    snake.pop()
        else:
            # Game over - wait for restart or quit
            try:
                key = stdscr.getch()
            except:
                key = -1
            
            if key == ord(' '):
                # Restart
                snake = [
                    [game_height // 2, game_width // 2],
                    [game_height // 2, game_width // 2 - 1],
                    [game_height // 2, game_width // 2 - 2]
                ]
                direction = [0, 1]
                food = [random.randint(1, game_height - 2), random.randint(1, game_width - 2)]
                score = 0
                speed = 100
                stdscr.timeout(speed)
                game_over = False
            elif key in [ord('q'), ord('Q')]:
                running = False
        
        time.sleep(0.01)

if __name__ == "__main__":
    curses.wrapper(main)

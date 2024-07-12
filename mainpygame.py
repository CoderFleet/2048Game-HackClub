import pygame
import sys
import random
import time
from copy import deepcopy

pygame.init()

SCREEN_SIZE = 400
GRID_SIZE = 4
GRID_PADDING = 10
GRID_LINE_WIDTH = 2
BACKGROUND_COLOR = pygame.Color('#92877d')
EMPTY_TILE_COLOR = pygame.Color('#9e948a')
INSTRUCTION_COLOR = pygame.Color('#776e65')

FPS = 60
ANIMATION_SPEED = 10

screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
pygame.display.set_caption('2048 Game')

# Sound Effects
merge_sound = pygame.mixer.Sound('merge.wav')
win_sound = pygame.mixer.Sound('win.wav')

# Fun variable names
grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
score = 0
previous_grid = None
previous_score = 0
high_score = 0

def draw_background():
    screen.fill(BACKGROUND_COLOR)
    pygame.draw.rect(screen, pygame.Color('#bbada0'), (GRID_PADDING, GRID_PADDING, SCREEN_SIZE - 2 * GRID_PADDING, SCREEN_SIZE - 2 * GRID_PADDING))

def draw_grid():
    for i in range(GRID_SIZE + 1):
        x = GRID_PADDING + i * (SCREEN_SIZE - GRID_PADDING * 2) // GRID_SIZE
        pygame.draw.line(screen, pygame.Color('#776e65'), (x, GRID_PADDING), (x, SCREEN_SIZE - GRID_PADDING), GRID_LINE_WIDTH)

    for i in range(GRID_SIZE + 1):
        y = GRID_PADDING + i * (SCREEN_SIZE - GRID_PADDING * 2) // GRID_SIZE
        pygame.draw.line(screen, pygame.Color('#776e65'), (GRID_PADDING, y), (SCREEN_SIZE - GRID_PADDING, y), GRID_LINE_WIDTH)

def draw_tiles():
    tile_size = (SCREEN_SIZE - (GRID_PADDING * (GRID_SIZE + 1))) // GRID_SIZE
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            value = grid[i][j]
            rect = pygame.Rect(GRID_PADDING + j * (tile_size + GRID_PADDING),
                               GRID_PADDING + i * (tile_size + GRID_PADDING),
                               tile_size, tile_size)
            if value > 0:
                color = get_tile_color(value)
                pygame.draw.rect(screen, color, rect)
                font_size = 36 if value < 100 else 28
                font = pygame.font.Font(None, font_size)
                text = font.render(str(value), True, pygame.Color('white'))
                text_rect = text.get_rect(center=rect.center)
                screen.blit(text, text_rect)
            else:
                pygame.draw.rect(screen, EMPTY_TILE_COLOR, rect)

def get_tile_color(value):
    base_color = pygame.Color('#bbada0')
    if value > 0:
        exponent = min(11, value.bit_length() - 1)
        base_color = pygame.Color('#%x' % (value << exponent | value))
    return base_color

def add_random_tile():
    empty_cells = [(i, j) for i in range(GRID_SIZE) for j in range(GRID_SIZE) if grid[i][j] == 0]
    if empty_cells:
        i, j = random.choice(empty_cells)
        grid[i][j] = random.choice([2, 4])

def move_tiles(direction):
    global score, previous_grid, previous_score
    previous_grid = deepcopy(grid)
    previous_score = score
    moved = False
    if direction == 'up':
        for j in range(GRID_SIZE):
            for i in range(1, GRID_SIZE):
                if grid[i][j] != 0:
                    moved |= merge_tiles(i, j, -1, 0)
    elif direction == 'down':
        for j in range(GRID_SIZE):
            for i in range(GRID_SIZE - 2, -1, -1):
                if grid[i][j] != 0:
                    moved |= merge_tiles(i, j, 1, 0)
    elif direction == 'left':
        for i in range(GRID_SIZE):
            for j in range(1, GRID_SIZE):
                if grid[i][j] != 0:
                    moved |= merge_tiles(i, j, 0, -1)
    elif direction == 'right':
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE - 2, -1, -1):
                if grid[i][j] != 0:
                    moved |= merge_tiles(i, j, 0, 1)
    if moved:
        add_random_tile()
        animate_move()
        time.sleep(0.1)

def merge_tiles(row, col, dr, dc):
    global score, high_score
    moved = False
    while 0 <= row + dr < GRID_SIZE and 0 <= col + dc < GRID_SIZE:
        if grid[row + dr][col + dc] == 0:
            grid[row + dr][col + dc] = grid[row][col]
            grid[row][col] = 0
            row += dr
            col += dc
            moved = True
        elif grid[row + dr][col + dc] == grid[row][col]:
            grid[row + dr][col + dc] *= 2
            score += grid[row + dr][col + dc]
            grid[row][col] = 0
            moved = True
            merge_sound.play()  # Play merge sound effect
            if grid[row + dr][col + dc] == 2048:
                win_sound.play()  # Play win sound effect if 2048 tile is formed
            break
        else:
            break
    if score > high_score:
        high_score = score
    return moved

def handle_events():
    global score, grid, previous_grid, previous_score
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                move_tiles('up')
            elif event.key == pygame.K_DOWN:
                move_tiles('down')
            elif event.key == pygame.K_LEFT:
                move_tiles('left')
            elif event.key == pygame.K_RIGHT:
                move_tiles('right')
            elif event.key == pygame.K_r:
                initialize_game()
            elif event.key == pygame.K_u:  # Undo feature
                if previous_grid:
                    grid = deepcopy(previous_grid)
                    score = previous_score

def initialize_game():
    global grid, score, previous_grid, previous_score, high_score
    grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
    score = 0
    previous_grid = None
    previous_score = 0
    add_random_tile()
    add_random_tile()

def is_game_over():
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if grid[i][j] == 0:
                return False
            if i > 0 and grid[i][j] == grid[i - 1][j]:
                return False
            if i < GRID_SIZE - 1 and grid[i][j] == grid[i + 1][j]:
                return False
            if j > 0 and grid[i][j] == grid[i][j - 1]:
                return False
            if j < GRID_SIZE - 1 and grid[i][j] == grid[i][j + 1]:
                return False
    return True

def game_over_screen():
    screen.fill(pygame.Color('black'))
    font = pygame.font.Font(None, 48)
    text = font.render("Game Over!", True, pygame.Color('white'))
    text_rect = text.get_rect(center=(SCREEN_SIZE // 2, SCREEN_SIZE // 2 - 40))
    screen.blit(text, text_rect)
    font = pygame.font.Font(None, 28)
    text = font.render("Press 'R' to Restart", True, pygame.Color('white'))
    text_rect = text.get_rect(center=(SCREEN_SIZE // 2, SCREEN_SIZE // 2 + 20))
    screen.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.wait(2000)

def draw_score():
    font = pygame.font.Font(None, 24)
    text = font.render(f"Score: {score}", True, pygame.Color('white'))
    screen.blit(text, (GRID_PADDING, SCREEN_SIZE - GRID_PADDING - 40))
    text = font.render(f"High Score: {high_score}", True, pygame.Color('white'))
    screen.blit(text, (GRID_PADDING, SCREEN_SIZE - GRID_PADDING - 20))

def draw_instructions():
    font = pygame.font.Font(None, 16)
    instructions = [
        "Use arrow keys to move tiles",
        "Combine tiles with the same number",
        "Reach 2048 to win!",
        "Press 'R' to restart",
        "Press 'U' to undo"
    ]
    for i, text in enumerate(instructions):
        text_surface = font.render(text, True, INSTRUCTION_COLOR)
        text_rect = text_surface.get_rect(left=GRID_PADDING, top=GRID_SIZE * 70 + i * 20)
        screen.blit(text_surface, text_rect)

def draw_animated_tiles():
    tile_size = (SCREEN_SIZE - (GRID_PADDING * (GRID_SIZE + 1))) // GRID_SIZE
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            value = grid[i][j]
            rect = pygame.Rect(GRID_PADDING + j * (tile_size + GRID_PADDING),
                               GRID_PADDING + i * (tile_size + GRID_PADDING),
                               tile_size, tile_size)
            if value > 0:
                color = get_tile_color(value)
                pygame.draw.rect(screen, color, rect)
                font_size = 36 if value < 100 else 28
                font = pygame.font.Font(None, font_size)
                text = font.render(str(value), True, pygame.Color('white'))
                text_rect = text.get_rect(center=rect.center)
                screen.blit(text, text_rect)
                pygame.display.update(rect)

def you_win_screen():
    screen.fill(pygame.Color('black'))
    font = pygame.font.Font(None, 48)
    text = font.render("You Win!", True, pygame.Color('white'))
    text_rect = text.get_rect(center=(SCREEN_SIZE // 2, SCREEN_SIZE // 2 - 40))
    screen.blit(text, text_rect)
    font = pygame.font.Font(None, 28)
    text = font.render("Press 'R' to Restart", True, pygame.Color('white'))
    text_rect = text.get_rect(center=(SCREEN_SIZE // 2, SCREEN_SIZE // 2 + 20))
    screen.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.wait(2000)

def animate_move():
    draw_animated_tiles()
    time.sleep(0.1)

def main():
    clock = pygame.time.Clock()
    initialize_game()
    while True:
        handle_events()
        draw_background()
        draw_grid()
        draw_tiles()
        draw_score()
        draw_instructions()
        if is_game_over():
            game_over_screen()
            initialize_game()
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()

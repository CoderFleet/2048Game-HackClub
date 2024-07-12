import pygame
import sys
import random

pygame.init()

SCREEN_SIZE = 400
GRID_SIZE = 4
GRID_PADDING = 10
GRID_LINE_WIDTH = 2

screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
pygame.display.set_caption('2048 Game')

grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]

def draw_grid():
    for i in range(GRID_SIZE + 1):
        x = GRID_PADDING + i * (SCREEN_SIZE - GRID_PADDING * 2) // GRID_SIZE
        pygame.draw.line(screen, pygame.Color('gray'), (x, GRID_PADDING), (x, SCREEN_SIZE - GRID_PADDING), GRID_LINE_WIDTH)

    for i in range(GRID_SIZE + 1):
        y = GRID_PADDING + i * (SCREEN_SIZE - GRID_PADDING * 2) // GRID_SIZE
        pygame.draw.line(screen, pygame.Color('gray'), (GRID_PADDING, y), (SCREEN_SIZE - GRID_PADDING, y), GRID_LINE_WIDTH)

def draw_tiles():
    tile_size = (SCREEN_SIZE - (GRID_PADDING * (GRID_SIZE + 1))) // GRID_SIZE
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            value = grid[i][j]
            if value > 0:
                color = get_tile_color(value)
                rect = pygame.Rect(GRID_PADDING + j * (tile_size + GRID_PADDING),
                                   GRID_PADDING + i * (tile_size + GRID_PADDING),
                                   tile_size, tile_size)
                pygame.draw.rect(screen, color, rect)
                font = pygame.font.Font(None, 36)
                text = font.render(str(value), True, pygame.Color('white'))
                text_rect = text.get_rect(center=rect.center)
                screen.blit(text, text_rect)

def get_tile_color(value):
    colors = {
        2: pygame.Color('#eee4da'),
        4: pygame.Color('#ede0c8'),
        8: pygame.Color('#f2b179'),
        16: pygame.Color('#f59563'),
        32: pygame.Color('#f67c5f'),
        64: pygame.Color('#f65e3b'),
        128: pygame.Color('#edcf72'),
        256: pygame.Color('#edcc61'),
        512: pygame.Color('#edc850'),
        1024: pygame.Color('#edc53f'),
        2048: pygame.Color('#edc22e'),
    }
    return colors.get(value, pygame.Color('#3c3a32'))

def add_random_tile():
    empty_cells = [(i, j) for i in range(GRID_SIZE) for j in range(GRID_SIZE) if grid[i][j] == 0]
    if empty_cells:
        i, j = random.choice(empty_cells)
        grid[i][j] = random.choice([2, 4])

def move_tiles(direction):
    if direction == 'up':
        for j in range(GRID_SIZE):
            for i in range(1, GRID_SIZE):
                if grid[i][j] != 0:
                    merge_tiles(i, j, -1, 0)
    elif direction == 'down':
        for j in range(GRID_SIZE):
            for i in range(GRID_SIZE - 2, -1, -1):
                if grid[i][j] != 0:
                    merge_tiles(i, j, 1, 0)
    elif direction == 'left':
        for i in range(GRID_SIZE):
            for j in range(1, GRID_SIZE):
                if grid[i][j] != 0:
                    merge_tiles(i, j, 0, -1)
    elif direction == 'right':
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE - 2, -1, -1):
                if grid[i][j] != 0:
                    merge_tiles(i, j, 0, 1)
    add_random_tile()

def merge_tiles(row, col, dr, dc):
    while 0 <= row + dr < GRID_SIZE and 0 <= col + dc < GRID_SIZE:
        if grid[row + dr][col + dc] == 0:
            grid[row + dr][col + dc] = grid[row][col]
            grid[row][col] = 0
            row += dr
            col += dc
        elif grid[row + dr][col + dc] == grid[row][col]:
            grid[row + dr][col + dc] *= 2
            grid[row][col] = 0
            break
        else:
            break

def handle_events():
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
    text_rect = text.get_rect(center=(SCREEN_SIZE // 2, SCREEN_SIZE // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.wait(2000)

def update_game_state():
    if is_game_over():
        game_over_screen()
        pygame.quit()
        sys.exit()

def render():
    screen.fill(pygame.Color('black'))
    draw_grid()
    draw_tiles()

def main():
    add_random_tile()
    while True:
        handle_events()
        update_game_state()
        render()
        pygame.display.flip()

if __name__ == '__main__':
    main()

import pygame
import sys
import random

pygame.init()

screen_size = 400
grid_size = 4
grid_padding = 10
grid_line_width = 2

screen = pygame.display.set_mode((screen_size, screen_size))
pygame.display.set_caption('2048 Game')

grid = [[0] * grid_size for _ in range(grid_size)]

def draw_grid():
    for i in range(grid_size + 1):
        x = grid_padding + i * (screen_size - grid_padding * 2) // grid_size
        pygame.draw.line(screen, pygame.Color('gray'), (x, grid_padding), (x, screen_size - grid_padding), grid_line_width)

    for i in range(grid_size + 1):
        y = grid_padding + i * (screen_size - grid_padding * 2) // grid_size
        pygame.draw.line(screen, pygame.Color('gray'), (grid_padding, y), (screen_size - grid_padding, y), grid_line_width)

def draw_tiles():
    tile_size = (screen_size - (grid_padding * (grid_size + 1))) // grid_size
    for i in range(grid_size):
        for j in range(grid_size):
            value = grid[i][j]
            if value > 0:
                color = get_tile_color(value)
                rect = pygame.Rect(grid_padding + j * (tile_size + grid_padding),
                                   grid_padding + i * (tile_size + grid_padding),
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
    empty_cells = [(i, j) for i in range(grid_size) for j in range(grid_size) if grid[i][j] == 0]
    if empty_cells:
        i, j = random.choice(empty_cells)
        grid[i][j] = random.choice([2, 4])

def move_tiles(direction):
    if direction == 'up':
        for j in range(grid_size):
            for i in range(1, grid_size):
                if grid[i][j] != 0:
                    merge_tiles(i, j, -1, 0)
    elif direction == 'down':
        for j in range(grid_size):
            for i in range(grid_size - 2, -1, -1):
                if grid[i][j] != 0:
                    merge_tiles(i, j, 1, 0)
    elif direction == 'left':
        for i in range(grid_size):
            for j in range(1, grid_size):
                if grid[i][j] != 0:
                    merge_tiles(i, j, 0, -1)
    elif direction == 'right':
        for i in range(grid_size):
            for j in range(grid_size - 2, -1, -1):
                if grid[i][j] != 0:
                    merge_tiles(i, j, 0, 1)
    add_random_tile()

def merge_tiles(i, j, di, dj):
    while 0 <= i + di < grid_size and 0 <= j + dj < grid_size:
        if grid[i + di][j + dj] == 0:
            grid[i + di][j + dj] = grid[i][j]
            grid[i][j] = 0
            i += di
            j += dj
        elif grid[i + di][j + dj] == grid[i][j]:
            grid[i + di][j + dj] *= 2
            grid[i][j] = 0
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

def update_game_state():
    pass

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

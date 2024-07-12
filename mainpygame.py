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
                color = pygame.Color('blue')  # Placeholder color
                rect = pygame.Rect(grid_padding + j * (tile_size + grid_padding),
                                   grid_padding + i * (tile_size + grid_padding),
                                   tile_size, tile_size)
                pygame.draw.rect(screen, color, rect)
                font = pygame.font.Font(None, 36)
                text = font.render(str(value), True, pygame.Color('white'))
                text_rect = text.get_rect(center=rect.center)
                screen.blit(text, text_rect)

def add_random_tile():
    empty_cells = [(i, j) for i in range(grid_size) for j in range(grid_size) if grid[i][j] == 0]
    if empty_cells:
        i, j = random.choice(empty_cells)
        grid[i][j] = random.choice([2, 4])  # Randomly choose 2 or 4 for new tile

def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

def update_game_state():
    pass

def render():
    screen.fill(pygame.Color('black'))
    draw_grid()
    draw_tiles()

def main():
    add_random_tile()  # Add initial random tile
    while True:
        handle_events()
        update_game_state()
        render()
        pygame.display.flip()

if __name__ == '__main__':
    main()

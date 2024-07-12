import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_SIZE = 400
GRID_SIZE = 4
GRID_PADDING = 10
GRID_WIDTH = 2

# Set up the screen
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
pygame.display.set_caption('2048 Game')

def draw_grid():
    # Draw vertical lines
    for i in range(GRID_SIZE + 1):
        x = GRID_PADDING + i * (SCREEN_SIZE - GRID_PADDING * 2) // GRID_SIZE
        pygame.draw.line(screen, pygame.Color('gray'), (x, GRID_PADDING), (x, SCREEN_SIZE - GRID_PADDING), GRID_WIDTH)

    # Draw horizontal lines
    for i in range(GRID_SIZE + 1):
        y = GRID_PADDING + i * (SCREEN_SIZE - GRID_PADDING * 2) // GRID_SIZE
        pygame.draw.line(screen, pygame.Color('gray'), (GRID_PADDING, y), (SCREEN_SIZE - GRID_PADDING, y), GRID_WIDTH)

def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

def update():
    # I will do this ;
    pass

def draw():
    screen.fill(pygame.Color('black'))
    draw_grid()
    # Gonna Do

def main():
    while True:
        handle_events()
        update()
        draw()
        pygame.display.flip()

if __name__ == '__main__':
    main()

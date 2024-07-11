import tkinter as tk
import random

class Puzzle2048:
    def __init__(self, window):
        self.window = window
        self.window.title("Puzzle2048 Game")
        self.size = 4
        self.tile_size = 100
        self.grid = [[0] * self.size for _ in range(self.size)]
        self.create_tiles()
        self.add_random_tile()
        self.add_random_tile()
        self.refresh_tiles()
        self.setup_controls()
        self.game_over = False

    def create_tiles(self):
        self.tiles = []
        for x in range(self.size):
            row = []
            for y in range(self.size):
                cell = tk.Frame(self.window, width=self.tile_size, height=self.tile_size)
                cell.grid(row=x, column=y, padx=5, pady=5)
                label = tk.Label(self.window, text="", justify=tk.CENTER, font=("Arial", 24))
                label.grid(row=x, column=y)
                row.append(label)
            self.tiles.append(row)

    def add_random_tile(self):
        if not self.game_over:
            empty_cells = [(x, y) for x in range(self.size) for y in range(self.size) if self.grid[x][y] == 0]
            if empty_cells:
                x, y = random.choice(empty_cells)
                self.grid[x][y] = 2 if random.random() < 0.9 else 4
            if self.check_game_over():
                self.display_game_over()

    def refresh_tiles(self):
        for x in range(self.size):
            for y in range(self.size):
                value = self.grid[x][y]
                self.tiles[x][y].config(text=str(value) if value != 0 else "")
        if self.check_game_over():
            self.display_game_over()

    def setup_controls(self):
        self.window.bind("<Up>", self.go_up)
        self.window.bind("<Down>", self.go_down)
        self.window.bind("<Left>", self.go_left)
        self.window.bind("<Right>", self.go_right)

    def go_up(self, event):
        self.shift_tiles_vertically(-1)
        self.add_random_tile()
        self.refresh_tiles()

    def go_down(self, event):
        self.shift_tiles_vertically(1)
        self.add_random_tile()
        self.refresh_tiles()

    def go_left(self, event):
        self.shift_tiles_horizontally(-1)
        self.add_random_tile()
        self.refresh_tiles()

    def go_right(self, event):
        self.shift_tiles_horizontally(1)
        self.add_random_tile()
        self.refresh_tiles()

    def shift_tiles_vertically(self, direction):
        for y in range(self.size):
            column = [self.grid[x][y] for x in range(self.size)]
            column = self.merge_tiles(column, direction)
            for x in range(self.size):
                self.grid[x][y] = column[x]

    def shift_tiles_horizontally(self, direction):
        for x in range(self.size):
            row = self.grid[x][:]
            row = self.merge_tiles(row, direction)
            self.grid[x] = row

    def merge_tiles(self, line, direction):
        if direction == 1:
            line = line[::-1]
        merged = []
        while line:
            if len(line) >= 2 and line[0] == line[1]:
                merged.append(2 * line[0])
                line = line[2:]
            else:
                merged.append(line[0])
                line = line[1:]
        merged += [0] * (self.size - len(merged))
        if direction == 1:
            merged = merged[::-1]
        return merged

    def check_game_over(self):
        for x in range(self.size):
            for y in range(self.size):
                if self.grid[x][y] == 0:
                    return False
                if x > 0 and self.grid[x][y] == self.grid[x - 1][y]:
                    return False
                if x < self.size - 1 and self.grid[x][y] == self.grid[x + 1][y]:
                    return False
                if y > 0 and self.grid[x][y] == self.grid[x][y - 1]:
                    return False
                if y < self.size - 1 and self.grid[x][y] == self.grid[x][y + 1]:
                    return False
        return True

    def display_game_over(self):
        self.game_over = True
        for x in range(self.size):
            for y in range(self.size):
                self.tiles[x][y].config(text="Game Over", bg="red", fg="white")
        game_over_label = tk.Label(
            self.window,
            text="Game Over",
            bg="black",
            fg="white",
            font=("Arial", 48)
        )
        game_over_label.grid(row=0, column=0, columnspan=self.size, rowspan=self.size)
        self.window.unbind("<Up>")
        self.window.unbind("<Down>")
        self.window.unbind("<Left>")
        self.window.unbind("<Right>")

app = tk.Tk()
game = Puzzle2048(app)
app.mainloop()

import tkinter as tk
import random

class Game2048:
    def __init__(self, master):
        self.master = master
        self.master.title("2048 Game")
        self.grid_size = 4
        self.cell_size = 100
        self.board = [[0] * self.grid_size for _ in range(self.grid_size)]
        self.create_grid()
        self.spawn_new_tile()
        self.spawn_new_tile()
        self.update_grid()

    def create_grid(self):
        self.cells = []
        for i in range(self.grid_size):
            row = []
            for j in range(self.grid_size):
                frame = tk.Frame(self.master, width=self.cell_size, height=self.cell_size)
                frame.grid(row=i, column=j, padx=5, pady=5)
                label = tk.Label(self.master, text="", justify=tk.CENTER, font=("Arial", 24))
                label.grid(row=i, column=j)
                row.append(label)
            self.cells.append(row)

    def spawn_new_tile(self):
        empty_cells = [(i, j) for i in range(self.grid_size) for j in range(self.grid_size) if self.board[i][j] == 0]
        if empty_cells:
            i, j = random.choice(empty_cells)
            self.board[i][j] = 2 if random.random() < 0.9 else 4

    def update_grid(self):
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                value = self.board[i][j]
                self.cells[i][j].config(text=str(value) if value != 0 else "")

root = tk.Tk()
game = Game2048(root)
root.mainloop()

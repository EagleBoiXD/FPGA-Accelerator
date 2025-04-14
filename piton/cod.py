import tkinter as tk
from tkinter import messagebox
import time
import heapq

class AStarApp:
    def __init__(self, root):
        self.root = root
        self.root.title("A* Pathfinding Algorithm Visualizer")
        self.size = 20  # Grid size
        self.cell_size = 30
        self.start = None
        self.end = None
        self.to_choose = 0
        self.blocks = set()

        self.map_frame = tk.Frame(root,relief=tk.RAISED, borderwidth=1)
        self.map_frame.pack(side=tk.LEFT, padx=10, pady=10)

        self.canvas = tk.Canvas(self.map_frame, width=self.size * self.cell_size, height=self.size * self.cell_size)
        self.canvas.pack()

        self.canvas.bind("<Button-1>", self.set_point)
        self.canvas.bind("<Button-3>", self.set_block)

        self.status_label = tk.Label(root, text="Left-click: Start/End, Right-click: Block")
        self.status_label.pack()

        self.time_label = tk.Label(root, text="Calculation Time: 0 ms")
        self.time_label.pack()

        self.run_button = tk.Button(root, text="Run A*", command=self.run_astar)
        self.run_button.pack()

        self.reset_button = tk.Button(root, text="Reset", command=self.reset)
        self.reset_button.pack()

        self.draw_grid()

    def draw_grid(self):
        for i in range(self.size):
            for j in range(self.size):
                x0, y0 = i * self.cell_size, j * self.cell_size
                x1, y1 = x0 + self.cell_size, y0 + self.cell_size
                self.canvas.create_rectangle(x0, y0, x1, y1, outline="black", fill="white")

    def set_point(self, event):
        x, y = event.x // self.cell_size, event.y // self.cell_size
        if self.to_choose == 0:
            self.start = (x, y)
            self.draw_cell(x, y, "green")
            self.to_choose == 1
        elif self.to_choose == 1:
            self.end = (x, y)
            self.draw_cell(x, y, "red")
            self.to_choose = 0

    def set_block(self, event):
        x, y = event.x // self.cell_size, event.y // self.cell_size
        if (x, y) not in [self.start, self.end]:
            self.blocks.add((x, y))
            self.draw_cell(x, y, "black")

    def draw_cell(self, x, y, color):
        x0, y0 = x * self.cell_size, y * self.cell_size
        x1, y1 = x0 + self.cell_size, y0 + self.cell_size
        self.canvas.create_rectangle(x0, y0, x1, y1, outline="black", fill=color)

    def heuristic(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def neighbors(self, node, search_mode):
        x, y = node
        neighbors = [(x+dx, y+dy) for dx, dy in search_mode if 0 <= x+dx < self.size and 0 <= y+dy < self.size]
        neighbors.sort(key=lambda n: self.heuristic(n, self.end))
        return neighbors

    def astar(self):
        start_time = time.time()
        open_set = [(0, self.start)]
        heapq.heapify(open_set)
        g_score = {self.start: 0}
        f_score = {self.start: self.heuristic(self.start, self.end)}
        came_from = {}

        while open_set:
            _, current = heapq.heappop(open_set)
            if current == self.end:
                self.reconstruct_path(came_from)
                self.time_label.config(text=f"Calculation Time: {int((time.time() - start_time) * 1000)} ms")
                return
            for neighbor in self.neighbors(current):
                if neighbor in self.blocks:
                    continue
                tentative_g_score = g_score[current] + 1
                if tentative_g_score < g_score.get(neighbor, float('inf')):
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + self.heuristic(neighbor, self.end)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))
        messagebox.showinfo("Path Not Found", "No path could be found!")

    def reconstruct_path(self, came_from):
        current = self.end
        while current in came_from:
            current = came_from[current]
            self.draw_cell(current[0], current[1], "blue")

    def run_astar(self):
        if self.start and self.end:
            self.astar()

    def reset(self):
        self.canvas.delete("all")
        self.start = None
        self.end = None
        self.blocks.clear()
        self.draw_grid()

root = tk.Tk()
app = AStarApp(root)
root.mainloop()

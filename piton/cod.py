import tkinter as tk
from tkinter import messagebox
import time
import math

class AStarApp:
    def __init__(self, root):
        self.root = root
        self.root.title("A* Pathfinding Algorithm Visualizer")
        self.size = 20  # Grid size
        self.cell_size = 30
        self.cells = {}
        self.start = None
        self.end = None
        self.blocks = set()
        self.selected_tool = "start"
        self.drawing = False
        self.last_cell = None
        self.visited_cells = set()
        self.path_cells = set()
        self.algorithm = "astar"  # "astar" or "greedy"

        # Create main frames
        self.map_frame = tk.Frame(root, relief=tk.RAISED, borderwidth=1)
        self.map_frame.pack(side=tk.LEFT, padx=10, pady=10)
        
        self.control_frame = tk.Frame(root)
        self.control_frame.pack(side=tk.RIGHT, padx=10, pady=10)

        # Create canvas
        self.canvas = tk.Canvas(self.map_frame, 
                               width=self.size * self.cell_size, 
                               height=self.size * self.cell_size)
        self.canvas.pack()

        # Bind mouse events
        self.canvas.bind("<Button-1>", self.handle_click)
        self.canvas.bind("<B1-Motion>", self.handle_drag)
        self.canvas.bind("<ButtonRelease-1>", self.handle_release)

        # Tool selection buttons
        tool_frame = tk.LabelFrame(self.control_frame, text="Tools", padx=5, pady=5)
        tool_frame.pack(fill=tk.X, pady=5)
        
        self.start_button = tk.Button(tool_frame, text="Start (Green)", 
                                    command=lambda: self.select_tool("start"))
        self.start_button.pack(fill=tk.X)
        
        self.end_button = tk.Button(tool_frame, text="End (Red)", 
                                  command=lambda: self.select_tool("end"))
        self.end_button.pack(fill=tk.X)
        
        self.block_button = tk.Button(tool_frame, text="Block (Black)", 
                                    command=lambda: self.select_tool("block"))
        self.block_button.pack(fill=tk.X)

        # Algorithm selection buttons
        algo_frame = tk.LabelFrame(self.control_frame, text="Algorithm", padx=5, pady=5)
        algo_frame.pack(fill=tk.X, pady=5)
        
        self.astar_button = tk.Button(algo_frame, text="Standard A* (Manhattan)", 
                                    command=lambda: self.select_algorithm("astar"))
        self.astar_button.pack(fill=tk.X)
        
        self.greedy_button = tk.Button(algo_frame, text="Greedy (Euclidean)", 
                                     command=lambda: self.select_algorithm("greedy"))
        self.greedy_button.pack(fill=tk.X)

        # Status labels
        status_frame = tk.LabelFrame(self.control_frame, text="Status", padx=5, pady=5)
        status_frame.pack(fill=tk.X, pady=5)
        
        self.status_label = tk.Label(status_frame, 
                                    text="Selected: Start (Green)")
        self.status_label.pack()
        
        self.algorithm_label = tk.Label(status_frame,
                                      text="Algorithm: Standard A* (Manhattan)")
        self.algorithm_label.pack()
        
        self.time_label = tk.Label(status_frame, 
                                  text="Calculation Time: 0 ms")
        self.time_label.pack()

        # Action buttons
        action_frame = tk.LabelFrame(self.control_frame, text="Actions", padx=5, pady=5)
        action_frame.pack(fill=tk.X, pady=5)
        
        self.run_button = tk.Button(action_frame, 
                                   text="Run Algorithm", 
                                   command=self.run_algorithm)
        self.run_button.pack(fill=tk.X)
        
        self.reset_button = tk.Button(action_frame, 
                                     text="Reset", 
                                     command=self.reset)
        self.reset_button.pack(fill=tk.X)

        self.draw_grid()

    def draw_grid(self):
        for i in range(self.size):
            for j in range(self.size):
                x0, y0 = i * self.cell_size, j * self.cell_size
                x1, y1 = x0 + self.cell_size, y0 + self.cell_size
                rect = self.canvas.create_rectangle(x0, y0, x1, y1, 
                                                  outline="black", fill="white")
                self.cells[(i, j)] = rect

    def select_tool(self, tool):
        self.selected_tool = tool
        color = "green" if tool == "start" else "red" if tool == "end" else "black"
        self.status_label.config(text=f"Selected: {tool.capitalize()} ({color.capitalize()})")

    def select_algorithm(self, algorithm):
        self.algorithm = algorithm
        if algorithm == "astar":
            self.algorithm_label.config(text="Algorithm: Standard A* (Manhattan)")
        else:
            self.algorithm_label.config(text="Algorithm: Greedy (Euclidean)")

    def handle_click(self, event):
        x, y = event.x // self.cell_size, event.y // self.cell_size
        self.last_cell = (x, y)
        self.process_cell(x, y)

    def handle_drag(self, event):
        x, y = event.x // self.cell_size, event.y // self.cell_size
        current_cell = (x, y)
        
        if self.selected_tool == "block" and current_cell != self.last_cell:
            self.process_cell(x, y)
            self.last_cell = current_cell

    def handle_release(self, event):
        self.last_cell = None

    def process_cell(self, x, y):
        if not (0 <= x < self.size and 0 <= y < self.size):
            return

        cell = (x, y)
        
        if self.selected_tool == "start":
            if cell in self.blocks:
                return
            if self.start:
                self.draw_cell(self.start[0], self.start[1], "white")
            self.start = cell
            self.draw_cell(x, y, "green")
            
        elif self.selected_tool == "end":
            if cell in self.blocks:
                return
            if self.end:
                self.draw_cell(self.end[0], self.end[1], "white")
            self.end = cell
            self.draw_cell(x, y, "red")
            
        elif self.selected_tool == "block":
            if cell not in [self.start, self.end]:
                if cell in self.blocks:
                    self.blocks.remove(cell)
                    self.draw_cell(x, y, "white")
                else:
                    self.blocks.add(cell)
                    self.draw_cell(x, y, "black")

    def draw_cell(self, x, y, color):
        if (x, y) in self.cells:
            self.canvas.itemconfig(self.cells[(x, y)], fill=color)

    def clear_visualization(self):
        for cell in self.visited_cells:
            if cell not in [self.start, self.end] and cell not in self.blocks:
                self.draw_cell(cell[0], cell[1], "white")
        for cell in self.path_cells:
            if cell not in [self.start, self.end] and cell not in self.blocks:
                self.draw_cell(cell[0], cell[1], "white")
        self.visited_cells.clear()
        self.path_cells.clear()

    def heuristic(self, a, b):
        if self.algorithm == "astar":
            return abs(a[0] - b[0]) + abs(a[1] - b[1])
        else:
            return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

    def neighbors(self, node):
        x, y = node
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        return [(x + dx, y + dy) for dx, dy in directions 
            if 0 <= x + dx < self.size and 0 <= y + dy < self.size]

    class PriorityQueue:
        def __init__(self):
            self.elements = []
            
        def empty(self):
            return len(self.elements) == 0
            
        def put(self, item, priority):
            self.elements.append((priority, item))
            self.elements.sort(key=lambda x: x[0])
            
        def get(self):
            return self.elements.pop(0)[1]

    def astar(self):
        if not self.start or not self.end:
            messagebox.showwarning("Missing Points", "Please set both start and end points!")
            return

        self.clear_visualization()

        start_time = time.time()
        frontier = self.PriorityQueue()
        frontier.put(self.start, 0)
        came_from = {}
        cost_so_far = {}
        came_from[self.start] = None
        cost_so_far[self.start] = 0

        while not frontier.empty():
            current = frontier.get()
            
            if current == self.end:
                break
                
            for neighbor in self.neighbors(current):
                if neighbor in self.blocks:
                    continue
                    
                # Cost is 1 for straight, sqrt(2) for diagonal (only in greedy)
                move_cost = 1.414 if abs(current[0]-neighbor[0]) and abs(current[1]-neighbor[1]) else 1
                new_cost = cost_so_far[current] + move_cost
                
                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    priority = new_cost + self.heuristic(neighbor, self.end)
                    frontier.put(neighbor, priority)
                    came_from[neighbor] = current
                    
                    if neighbor != self.end:
                        self.draw_cell(neighbor[0], neighbor[1], "lightblue")
                        self.visited_cells.add(neighbor)
                        self.canvas.update()
                        time.sleep(0.01)

        if self.end not in came_from:
            messagebox.showinfo("Path Not Found", "No path could be found!")
            return
            
        self.reconstruct_path(came_from)
        self.time_label.config(text=f"Calculation Time: {int((time.time() - start_time) * 1000)} ms")

    def reconstruct_path(self, came_from):
        current = self.end
        path = []
        while current != self.start:
            path.append(current)
            current = came_from[current]
        path.reverse()
        
        for node in path:
            if node != self.start and node != self.end:
                self.draw_cell(node[0], node[1], "blue")
                self.path_cells.add(node)
                self.canvas.update()
                time.sleep(0.05)

    def run_algorithm(self):
        self.astar()

    def reset(self):
        self.canvas.delete("all")
        self.cells = {}
        self.start = None
        self.end = None
        self.blocks.clear()
        self.visited_cells.clear()
        self.path_cells.clear()
        self.draw_grid()

root = tk.Tk()
app = AStarApp(root)
root.mainloop()
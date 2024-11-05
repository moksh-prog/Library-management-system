import tkinter as tk
import heapq
import random
from tkinter import messagebox, font
from PIL import Image, ImageTk

class Graph:
    def __init__(self):
        self.graph = {}

    def add_edge(self, city1, city2, distance):
        if city1 not in self.graph:
            self.graph[city1] = []
        if city2 not in self.graph:
            self.graph[city2] = []
        self.graph[city1].append((city2, distance))
        self.graph[city2].append((city1, distance))

    def dijkstra(self, start):
        distances = {vertex: float('infinity') for vertex in self.graph}
        distances[start] = 0
        previous = {vertex: None for vertex in self.graph}
        priority_queue = [(0, start)]
        while priority_queue:
            current_distance, current_vertex = heapq.heappop(priority_queue)
            if current_distance > distances[current_vertex]:
                continue
            for neighbor, distance in self.graph[current_vertex]:
                path_distance = current_distance + distance
                if path_distance < distances[neighbor]:
                    distances[neighbor] = path_distance
                    previous[neighbor] = current_vertex
                    heapq.heappush(priority_queue, (path_distance, neighbor))
        return distances, previous

class DijkstraApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Interactive City Navigator with Animated Car")
        self.graph = Graph()
        self.cities_positions = {}
        self.car_id = None
        self.setup_fonts()
        self.create_widgets()

    def setup_fonts(self):
        self.custom_font = font.Font(family="Arial", size=12, weight="bold")
        self.title_font = font.Font(family="Arial", size=16, weight="bold")
        self.button_font = font.Font(family="Arial", size=10)

    def create_widgets(self):
        # Load the background and car images
        self.background_image = Image.open("krakow-mapa-cracow-poland-vector-260nw-1689236293.jpg")  # Replace with your image path
        self.background_image = self.background_image.resize((800, 600), Image.LANCZOS)
        self.bg_image_tk = ImageTk.PhotoImage(self.background_image)
        
        self.car_image = Image.open("car.png")  # Replace with your car image path
        self.car_image = self.car_image.resize((25, 25), Image.LANCZOS)
        self.car_image_tk = ImageTk.PhotoImage(self.car_image)

        # Canvas with background image
        self.canvas = tk.Canvas(self.root, width=800, height=600, bg="lightblue")
        self.canvas.grid(row=0, column=0, rowspan=10, columnspan=2, padx=10, pady=10)
        self.canvas.create_image(0, 0, image=self.bg_image_tk, anchor="nw")

        tk.Label(self.root, text="Add City Connection", font=self.title_font).grid(row=0, column=2, sticky="w", pady=(10, 5))
        tk.Label(self.root, text="City 1:", font=self.custom_font).grid(row=1, column=2, sticky="w")
        self.city1_entry = tk.Entry(self.root, font=self.custom_font)
        self.city1_entry.grid(row=1, column=3, pady=5)

        tk.Label(self.root, text="City 2:", font=self.custom_font).grid(row=2, column=2, sticky="w")
        self.city2_entry = tk.Entry(self.root, font=self.custom_font)
        self.city2_entry.grid(row=2, column=3, pady=5)

        tk.Label(self.root, text="Distance (km):", font=self.custom_font).grid(row=3, column=2, sticky="w")
        self.distance_entry = tk.Entry(self.root, font=self.custom_font)
        self.distance_entry.grid(row=3, column=3, pady=5)

        self.add_edge_button = tk.Button(self.root, text="Add Connection", font=self.button_font, command=self.add_edge)
        self.add_edge_button.grid(row=4, column=2, columnspan=2, pady=10)

        tk.Label(self.root, text="Find Shortest Path", font=self.title_font).grid(row=5, column=2, sticky="w", pady=(10, 5))
        tk.Label(self.root, text="Start City:", font=self.custom_font).grid(row=6, column=2, sticky="w")
        self.start_city_entry = tk.Entry(self.root, font=self.custom_font)
        self.start_city_entry.grid(row=6, column=3, pady=5)

        tk.Label(self.root, text="End City:", font=self.custom_font).grid(row=7, column=2, sticky="w")
        self.end_city_entry = tk.Entry(self.root, font=self.custom_font)
        self.end_city_entry.grid(row=7, column=3, pady=5)

        self.calculate_button = tk.Button(self.root, text="Calculate Shortest Path", font=self.button_font, command=self.calculate_shortest_path)
        self.calculate_button.grid(row=8, column=2, columnspan=2, pady=10)

        self.result_text = tk.Text(self.root, width=40, height=10, wrap="word", font=self.custom_font, state="disabled")
        self.result_text.grid(row=9, column=2, columnspan=2, pady=10)

    def add_edge(self):
        city1 = self.city1_entry.get().strip()
        city2 = self.city2_entry.get().strip()
        distance = self.distance_entry.get().strip()

        try:
            distance = int(distance)
            self.graph.add_edge(city1, city2, distance)

            # Place cities with animation
            if city1 not in self.cities_positions:
                self.animate_place_city(city1)
            if city2 not in self.cities_positions:
                self.animate_place_city(city2)

            # Animate drawing the edge
            self.animate_edge(city1, city2, distance)

            # Clear input fields
            self.clear_input_fields()
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid integer for distance.")

    def animate_place_city(self, city):
        x, y = self.random_position()
        self.cities_positions[city] = (x, y)

        def draw_city(step=0):
            if step < 30:
                radius = step / 30 * 15
                self.canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill="orange")
                self.canvas.create_text(x, y, text=city, font=self.custom_font, fill="black")
                self.root.after(20, draw_city, step + 1)

        draw_city()

    def random_position(self):
        return random.randint(50, 750), random.randint(50, 550)

    def animate_edge(self, city1, city2, distance):
        x1, y1 = self.cities_positions[city1]
        x2, y2 = self.cities_positions[city2]
        steps = 50
        dx = (x2 - x1) / steps
        dy = (y2 - y1) / steps

        def draw_segment(step=0):
            if step <= steps:
                self.canvas.create_line(x1, y1, x1 + step * dx, y1 + step * dy, fill="green", width=3)
                if step == steps:
                    self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=f"{distance} km", font=self.custom_font, fill="blue")
                self.root.after(20, draw_segment, step + 1)

        draw_segment()

    def calculate_shortest_path(self):
        start_city = self.start_city_entry.get().strip()
        end_city = self.end_city_entry.get().strip()
        distances, previous = self.graph.dijkstra(start_city)
        
        if end_city in distances:
            self.result_text.config(state="normal")
            self.result_text.delete(1.0, tk.END)
            result = f"Shortest distance from '{start_city}' to '{end_city}': {distances[end_city]} km.\nPath:\n"
            path_edges = self.get_path_edges(start_city, end_city, previous)
            self.animate_path(path_edges)
        else:
            result = f"'{end_city}' is not reachable from '{start_city}'."
        
        self.result_text.insert(tk.END, result)
        self.result_text.config(state="disabled")

    def get_path_edges(self, start, end, previous):
        path = []
        current_city = end
        while previous[current_city] is not None:
            prev_city = previous[current_city]
            for neighbor, dist in self.graph.graph[prev_city]:
                if neighbor == current_city:
                    path.append((prev_city, current_city, dist))
                    break
            current_city = prev_city
        return path[::-1]

    def animate_path(self, path_edges):
        def animate_edges(index=0):
            if index < len(path_edges):
                city1, city2, _ = path_edges[index]
                self.highlight_edge(city1, city2)
                self.move_car(city1, city2, animate_edges, index + 1)
            else:
                messagebox.showinfo("Complete", "Car has reached the destination!")

        animate_edges()

    def highlight_edge(self, city1, city2):
        x1, y1 = self.cities_positions[city1]
        x2, y2 = self.cities_positions[city2]
        self.canvas.create_line(x1, y1, x2, y2, fill="red", width=5)

    def move_car(self, city1, city2, callback, next_index):
        x1, y1 = self.cities_positions[city1]
        x2, y2 = self.cities_positions[city2]
        steps = 100
        dx = (x2 - x1) / steps
        dy = (y2 - y1) / steps

        if self.car_id is None:
            self.car_id = self.canvas.create_image(x1, y1, image=self.car_image_tk)
        else:
            self.canvas.coords(self.car_id, x1, y1)

        def animate_car(step=0):
            if step < steps:
                self.canvas.move(self.car_id, dx, dy)
                if step % 10 < 5:
                    self.canvas.move(self.car_id, 0, -1)
                else:
                    self.canvas.move(self.car_id, 0, 1)
                self.root.after(20, animate_car, step + 1)
            else:
                callback(next_index)

        animate_car()

    def clear_input_fields(self):
        self.city1_entry.delete(0, tk.END)
        self.city2_entry.delete(0, tk.END)
        self.distance_entry.delete(0, tk.END)
        self.start_city_entry.delete(0, tk.END)
        self.end_city_entry.delete(0, tk.END)

root = tk.Tk()
app = DijkstraApp(root)
root.mainloop()

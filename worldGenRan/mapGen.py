import random
import numpy as np
import tkinter as tk
from flask import Flask, render_template
from noise import pnoise3

class Biome:
    def __init__(self, biome_id, name, symbol, elevation_range, climate_range, neighbors):
        self.biome_id = biome_id
        self.name = name
        self.symbol = symbol
        self.elevation_range = elevation_range
        self.climate_range = climate_range
        self.neighbors = neighbors

    def is_valid_neighbor(self, other_biome):
        return other_biome.biome_id in self.neighbors

# Define biomes
biomes = [
    Biome(1, 'Frozen River', '\u2744\u1F30A', (0, 0.33), (0, 0.33), [2, 3, 4]),
    Biome(2, 'Snowy Tundra', '\u2744', (0.33, 0.66), (0, 0.33), [1, 3, 4, 5]),
    Biome(3, 'Snowy Mountains', '\u26F0', (0.66, 1), (0, 0.33), [1, 2, 4, 5, 6]),
    Biome(4, 'Tundra', '\u2744', (0.33, 0.66), (0.33, 0.66), [1, 2, 3, 5, 6]),
    Biome(5, 'Boreal Forest', '\u1F341', (0.33, 0.66), (0.33, 0.66), [2, 3, 4, 6, 10, 11]),
    Biome(6, 'Alpine', '\u26F0', (0.66, 1), (0.33, 0.66), [3, 4, 5, 10, 11]),
    Biome(7, 'Plains', '\u2693', (0, 0.33), (0.66, 1), [8, 9, 10, 16, 18]),
    Biome(8, 'Forest', '\u1F332', (0.33, 0.66), (0.66, 1), [7, 9, 10, 11, 12]),
    Biome(9, 'Mountains', '\u26F0', (0.66, 1), (0.66, 1), [8, 7, 10, 16, 12]),
    Biome(10, 'Grassland', '\u1F33F', (0, 0.33), (0.66, 1), [7, 8, 9, 18, 11]),
    Biome(11, 'Deciduous Forest', '\u1F333', (0.33, 0.66), (0.66, 1), [5, 6, 10, 8, 12]),
    Biome(12, 'Temperate Rainforest', '\u1F333', (0.66, 1), (0.66, 1), [8, 9, 11]),
    Biome(13, 'Desert', '\u2600', (0, 0.33), (0.66, 1), [14, 15, 16, 20]),
    Biome(14, 'Savanna', '\u1F405', (0.33, 0.66), (0.66, 1), [13, 15, 16, 17]),
    Biome(15, 'Desert Hills', '\u2600\u26F0', (0.66, 1), (0.66, 1), [13, 14, 16, 20]),
    Biome(16, 'Chaparral', '\u1F33E', (0.33, 0.66), (0.66, 1), [7, 9, 10, 13, 14, 15, 17]),
    Biome(17, 'Tropical Rainforest', '\u1F34C', (0.66, 1), (0.66, 1), [14, 16, 18, 19]),
    Biome(18, 'Wetlands', '\u1F4A7', (0, 0.33), (0.66, 1), [7, 10, 17, 19]),
    Biome(19, 'Mangrove', '\u1F33C', (0.33, 0.66), (0.66, 1), [17, 18]),
    Biome(20, 'Badlands', '\u1F3D4', (0.66, 1), (0.66, 1), [13, 15]),
    # Cave biomes
 
    Biome(21, 'Limestone Cave', '\u26F1', (0, 0.33), (0, 0.33), [25]),
    Biome(22, 'Ice Cave', '\u2744', (0, 0.33), (0, 0.33), [25]),
    Biome(23, 'Crystal Cave', '\u2747', (0, 0.33), (0, 0.33), [25]),
    Biome(24, 'Volcanic Cave', '\u1F30B', (0, 0.33), (0, 0.33), [25]),
    Biome(25, 'Ston', '\u1F5FF', (0, 1), (0, 1), [21, 22, 23, 24, 25]),
]

# Create a lookup dictionary for biomes by ID
biomes_by_id = {biome.biome_id: biome for biome in biomes}

def generate_elevation_grid(grid_size, height, scale=100.0):
    elevation = np.zeros((grid_size, grid_size, height))
    for i in range(grid_size):
        for j in range(grid_size):
            for k in range(height):
                elevation[i][j][k] = pnoise3(i / scale, j / scale, k / scale, octaves=6, persistence=0.5, lacunarity=2.0, repeatx=grid_size, repeaty=grid_size, repeatz=height, base=42)
    elevation = (elevation - elevation.min()) / (elevation.max() - elevation.min())
    return elevation

def generate_climate_grid(grid_size):
    climate = np.zeros((grid_size, grid_size))
    for i in range(grid_size):
        for j in range(grid_size):
            latitude_factor = abs((i / grid_size) - 0.5) * 2
            climate[i][j] = latitude_factor
    return climate

def generate_caves(grid_size, height, scale=50.0):
    caves = np.zeros((grid_size, grid_size, height))
    for i in range(grid_size):
        for j in range(grid_size):
            for k in range(height):
                caves[i][j][k] = pnoise3(i / scale, j / scale, k / scale, octaves=4, persistence=0.5, lacunarity=2.0, repeatx=grid_size, repeaty=grid_size, repeatz=height, base=84)
    caves = (caves > 0.5).astype(int)  # Threshold to create cave spaces
    return caves

def get_biome_id(climate, elevation, is_cave=False):
    if is_cave:
        cave_biomes = [biomes_by_id[21], biomes_by_id[22], biomes_by_id[23], biomes_by_id[24]]
        return random.choice(cave_biomes).biome_id
    else:
        for biome in biomes:
            if biome.elevation_range[0] <= elevation <= biome.elevation_range[1] and biome.climate_range[0] <= climate <= biome.climate_range[1]:
                return biome.biome_id
    return None

def assign_biomes(elevation_grid, climate_grid, grid_size, height, caves_grid):
    biomes_grid = np.empty((grid_size, grid_size, height), dtype=int)
    for i in range(grid_size):
        for j in range(grid_size):
            for k in range(height):
                is_cave = caves_grid[i, j, k] == 1
                climate = climate_grid[i, j]
                elevation = elevation_grid[i, j, k]
                biomes_grid[i, j, k] = get_biome_id(climate, elevation, is_cave)
    return biomes_grid

def is_valid_transition(biome1_id, biome2_id):
    if biome1_id == biome2_id:
        return True
    if biome1_id in biomes_by_id and biome2_id in biomes_by_id:
        return biomes_by_id[biome1_id].is_valid_neighbor(biomes_by_id[biome2_id])
    return False

def smooth_biome_transitions(biomes_grid, grid_size, height):
    new_biomes = biomes_grid.copy()
    for i in range(1, grid_size-1):
        for j in range(1, grid_size-1):
            for k in range(1, height-1):
                current_biome = biomes_grid[i, j, k]
                surrounding_biomes = [
                    biomes_grid[i-1, j, k], biomes_grid[i+1, j, k], biomes_grid[i, j-1, k], biomes_grid[i, j+1, k],
                    biomes_grid[i, j, k-1], biomes_grid[i, j, k+1]
                ]
                for neighbor in surrounding_biomes:
                    if not is_valid_transition(current_biome, neighbor):
                        valid_neighbors = [b for b in surrounding_biomes if is_valid_transition(current_biome, b)]
                        if valid_neighbors:
                            new_biomes[i, j, k] = random.choice(valid_neighbors)
                        break
    return new_biomes

def generate_world_grid(grid_size=50, height=50):
    elevation_grid = generate_elevation_grid(grid_size, height)
    climate_grid = generate_climate_grid(grid_size)
    caves_grid = generate_caves(grid_size, height)
    biomes_grid = assign_biomes(elevation_grid, climate_grid, grid_size, height, caves_grid)
    smoothed_biomes = smooth_biome_transitions(biomes_grid, grid_size, height)
    
    # Combine elevation, caves, and biomes into one grid
    world_grid = np.empty((grid_size, grid_size, height), dtype=object)
    for i in range(grid_size):
        for j in range(grid_size):
            for k in range(height):
                biome_id = smoothed_biomes[i, j, k]
                world_grid[i, j, k] = biomes_by_id[biome_id].symbol
    return world_grid

# Testing function to display the world
def generate_gui(world_grid): 
    root = tk.Tk()
    canvas = tk.Canvas(root, width=100, height=100)
    canvas.pack()

    cell_size = 8

    for i in range(len(world_grid[0][0])):  # Iterate over height
        for j in range(len(world_grid)):  # Iterate over grid_size
            for k in range(len(world_grid[0])):  # Iterate over grid_size
                symbol = world_grid[j, k, i]
                x1 = k * cell_size
                y1 = j * cell_size
                x2 = x1 + cell_size
                y2 = y1 + cell_size

                canvas.create_rectangle(x1, y1, x2, y2, fill='white')
                canvas.create_text((x1 + x2) // 2, (y1 + y2) // 2, text=symbol)

    root.mainloop()

def SetworldGrid():
    # Generate a world grid
    world_grid = generate_world_grid()
    return world_grid

def web():
    app = Flask(__name__, template_folder='templates')

    @app.route('/')
    def home():
        world_grid = SetworldGrid()
        world_grid_list = world_grid.tolist()
        return render_template('index.html', world_grid=world_grid_list)

    if __name__ == '__main__':
        app.run(debug=True)

web()

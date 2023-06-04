import random
import numpy as np
import tensorflow as tf
import tensorflow_probability as tfp
import tkinter as tk
import time

biomes = {
    'Plains': ['Forest', 'Sunflower Plains', 'Birch Forest', 'Swamp', 'Village', 'Farm', 'City', 'Roads'],
    'Sunflower Plains': ['Plains', 'Forest', 'Village', 'Farm', 'City', 'Roads'],
    'Forest': ['Plains', 'Sunflower Plains', 'Birch Forest', 'Dark Forest', 'Village', 'City', 'Roads'],
    'Birch Forest': ['Plains', 'Forest', 'Dark Forest', 'Mountains', 'Village', 'City', 'Roads'],
    'Dark Forest': ['Forest', 'Birch Forest', 'Mountains', 'Village', 'City', 'Roads'],
    'Mountains': ['Birch Forest', 'Dark Forest', 'Jungle', 'Taiga', 'Snowy Tundra', 'City', 'Roads'],
    'Jungle': ['Mountains', 'Bamboo Jungle', 'Savanna', 'City', 'Roads'],
    'Bamboo Jungle': ['Jungle', 'Savanna', 'City', 'Roads'],
    'Savanna': ['Jungle', 'Bamboo Jungle', 'Desert', 'Plains', 'City', 'Roads'],
    'Desert': ['Savanna', 'Plains', 'Badlands', 'Mountains', 'City', 'Roads'],
    'Badlands': ['Desert', 'Mountains', 'City', 'Roads'],
    'Taiga': ['Mountains', 'Snowy Tundra', 'Snowy Taiga', 'City', 'Roads'],
    'Snowy Tundra': ['Mountains', 'Taiga', 'Snowy Taiga', 'Frozen River', 'City', 'Roads'],
    'Snowy Taiga': ['Taiga', 'Snowy Tundra', 'Snowy Taiga Mountains', 'City', 'Roads'],
    'Frozen River': ['Snowy Tundra', 'River', 'City', 'Roads'],
    'River': ['Frozen River', 'Beach', 'City', 'Roads'],
    'Ocean': ['River', 'Beach', 'City', 'Roads'],
    'Beach': ['River', 'Ocean', 'City', 'Roads'],
    'Stone Shore': ['Beach', 'River', 'City', 'Roads'],
    'Mushroom Fields': ['Mushroom Field Shore', 'City', 'Roads'],
    'Mushroom Field Shore': ['Mushroom Fields', 'City', 'Roads'],
    'Swamp': ['Plains', 'Forest', 'Jungle', 'Swamp Hills', 'City', 'Roads'],
    'Swamp Hills': ['Swamp', 'Mountains', 'City', 'Roads'],
    'Giant Tree Taiga': ['Taiga', 'Giant Spruce Taiga', 'City', 'Roads'],
    'Giant Spruce Taiga': ['Giant Tree Taiga', 'City', 'Roads'],
    'Giant Spruce Taiga Hills': ['Giant Spruce Taiga', 'City', 'Roads'],
    'Modified Jungle': ['Jungle', 'Jungle Edge', 'City', 'Roads'],
    'Jungle Edge': ['Modified Jungle', 'Jungle', 'City', 'Roads'],
    'Modified Jungle Edge': ['Jungle Edge', 'Jungle', 'City', 'Roads'],
    'Bamboo Jungle Hills': ['Bamboo Jungle', 'City', 'Roads'],
    'Modified Badlands Plateau': ['Badlands Plateau', 'City', 'Roads'],
    'Badlands Plateau': ['Badlands', 'City', 'Roads'],
    'Wooded Badlands Plateau': ['Badlands Plateau', 'City', 'Roads'],
    'Modified Wooded Badlands Plateau': ['Wooded Badlands Plateau', 'City', 'Roads'],
    'Desert Hills': ['Desert', 'City', 'Roads'],
    'Snowy Taiga Hills': ['Snowy Taiga', 'City', 'Roads'],
    'Snowy Taiga Mountains': ['Snowy Taiga', 'Snowy Taiga Hills', 'City', 'Roads'],
    'Snowy Spruce Taiga': ['Snowy Taiga', 'City', 'Roads'],
    'Snowy Spruce Taiga Hills': ['Snowy Spruce Taiga', 'City', 'Roads'],
    'Birch Forest Hills': ['Birch Forest', 'City', 'Roads'],
    'Dark Forest Hills': ['Dark Forest', 'City', 'Roads'],
    'Taiga Hills': ['Taiga', 'City', 'Roads'],
    'Mountain Edge': ['Mountains', 'City', 'Roads'],
    'Gravelly Mountains': ['Mountains', 'City', 'Roads'],
    'City': ['Plains', 'Mountains', 'Jungle', 'Savanna', 'Desert', 'Badlands', 'Farm', 'Village', 'Roads'],
    'Village': ['Plains', 'Sunflower Plains', 'Forest', 'Birch Forest', 'Farm', 'City', 'Roads'],
    'Roads': ['Savanna', 'City', 'Village'],
    'Farm': ['Plains', 'Sunflower Plains', 'Forest', 'Birch Forest', 'Village', 'City', 'Roads'],
}

biome_symbols = {
    'Plains': '\u2693',  # anchor
    'Sunflower Plains': '\u2600',  # sun
    'Forest': '\u1F332',  # tree
    'Birch Forest': '\u1F333',  # deciduous tree
    'Dark Forest': '\u1F43B',  # bear, suggesting wildlife
    'Mountains': '\u26F0',  # mountain
    'Jungle': '\u1F34C',  # banana, suggesting tropical
    'Bamboo Jungle': '\u1F38D',  # bamboo decoration
    'Savanna': '\u1F405',  # lion, suggesting wildlife
    'Desert': '\u2600',  # sun, suggesting heat
    'Badlands': '\u1F3D4',  # volcano
    'Taiga': '\u1F341',  # maple leaf
    'Snowy Tundra': '\u2744',  # snowflake
    'Snowy Taiga': '\u2746',  # more snowflakes
    'Frozen River': '\u2744\u1F30A',  # snowflake and wave, suggesting cold water
    'River': '\u1F30A',  # wave
    'Ocean': '\u1F30A\u1F30A',  # two waves
    'Beach': '\u2600\u1F30A',  # sun and wave, suggesting pleasant water-side location
    'Stone Shore': '\u26FA',  # tent, suggesting wilderness
    'Mushroom Fields': '\u1F344',  # mushroom
    'Mushroom Field Shore': '\u1F344\u1F30A',  # mushroom and wave, suggesting mushroom near water
    'Swamp': '\u1F4A7',  # droplet, suggesting water and possibly wetlands
    'Swamp Hills': '\u1F4A7\u26F0',  # droplet and mountain, suggesting hilly swamp
    'Giant Tree Taiga': '\u1F332\u1F332',  # two trees, suggesting lots of greenery
    'Giant Spruce Taiga': '\u1F332\u1F340',  # tree and clover, suggesting lots of greenery
    'Giant Spruce Taiga Hills': '\u1F332\u1F340\u26F0',  # tree, clover, and mountain, suggesting hilly green area
    'Modified Jungle': '\u1F34C\u273F',  # banana and sparkles, suggesting an exceptional jungle
    'Jungle Edge': '\u1F34C\u2693',  # banana and anchor, suggesting the edge of a jungle
    'Modified Jungle Edge': '\u1F34C\u2693\u273F',  # banana, anchor, and sparkles, suggesting an exceptional edge of a jungle
    'Bamboo Jungle Hills': '\u1F38D\u26F0',  # bamboo and mountain, suggesting hilly bamboo area
    'Modified Badlands Plateau': '\u1F3D4\u273F',  # volcano and sparkles, suggesting an exceptional badlands
    'Badlands Plateau': '\u1F3D4\u26F0',  # volcano and mountain, suggesting a plateau in the badlands
    'Wooded Badlands Plateau': '\u1F3D4\u1F332\u26F0',  # volcano, tree, and mountain, suggesting a wooded plateau in the badlands
    'Modified Wooded Badlands Plateau': '\u1F3D4\u1F332\u26F0\u273F',  # volcano, tree, mountain, and sparkles, suggesting an exceptional wooded plateau in the badlands
    'Desert Hills': '\u2600\u26F0',  # sun and mountain, suggesting hilly desert
    'Snowy Taiga Hills': '\u2744\u1F341\u26F0',  # snowflake, maple leaf, and mountain, suggesting hilly snowy area
    'Snowy Taiga Mountains': '\u2744\u1F341\u26F0',  # snowflake, maple leaf, and mountain, suggesting mountainous snowy area
    'Snowy Spruce Taiga': '\u2744\u1F332',  # snowflake and tree, suggesting snowy greenery
    'Snowy Spruce Taiga Hills': '\u2744\u1F332\u26F0',  # snowflake, tree, and mountain, suggesting hilly snowy greenery
    'Birch Forest Hills': '\u1F333\u26F0',  # deciduous tree and mountain, suggesting hilly forest
    'Dark Forest Hills': '\u1F43B\u26F0',  # bear and mountain, suggesting hilly wildlife area
    'Taiga Hills': '\u1F341\u26F0',  # maple leaf and mountain, suggesting hilly area with maple trees
    'Mountain Edge': '\u26F0\u2693',  # mountain and anchor, suggesting the edge of a mountain
    'Gravelly Mountains': '\u26F0\u26F0',  # two mountains, suggesting rocky area
    'City': '\u1F3E0',  # house, suggesting a residential area
    'Village': '\u1F3D8',  # park, suggesting a rural area
    'Roads': '\u1F6A5',  # traffic light, suggesting transportation
    'Farm': '\u1F33D',  # ear of corn, suggesting agriculture
}

def generate_random_world(start_biome, biome_coverage, linked_biomes):
    stack = [start_biome]
    visited = set()

    while stack:
        current_biome = stack.pop()
        visited.add(current_biome)

        biome_coverage[current_biome] = np.random.uniform(0, 100)

        connected_biomes = linked_biomes[current_biome]

        for biome in connected_biomes:
            if biome not in visited:
                stack.append(biome)

    return biome_coverage

def generate_random_world(start_biome, biome_coverage, linked_biomes):
    stack = [start_biome]
    visited = set()

    while stack:
        current_biome = stack.pop()
        visited.add(current_biome)

        biome_coverage[current_biome] = np.random.uniform(0, 100)

        connected_biomes = linked_biomes[current_biome]

        for biome in connected_biomes:
            if biome not in visited:
                stack.append(biome)

    return biome_coverage

def generate_linked_world():
    total_land_area = 100

    biome_coverage = {}
    linked_biomes = {}

    start_biome = random.choice(list(biomes.keys()))
    biome_coverage[start_biome] = np.random.uniform(0, 100)

    for biome in biomes:
        if biome not in biome_coverage:
            biome_coverage = generate_random_world(biome, biome_coverage, biomes)

    total_biome_coverage = sum(biome_coverage.values())
    scaling_factor = total_land_area / total_biome_coverage
    biome_coverage = {biome: value * scaling_factor for biome, value in biome_coverage.items()}

    return biome_coverage

def generate_world_grid(world, biome_symbols, grid_size=10000):
    # Flatten the grid into 1D
    world_grid = np.zeros((grid_size * grid_size,), dtype=np.object)

    # Calculate total area for scaling
    total_area = sum(world.values())

    # Create a flattened representation of the grid
    idx = 0
    for biome, area in world.items():
        # Calculate the number of cells to fill for this biome
        num_cells = int((area / total_area) * (grid_size * grid_size))

        # Get the symbol for this biome
        symbol = biome_symbols.get(biome, '?')

        # Fill the cells
        for _ in range(num_cells):
            world_grid[idx] = symbol
            idx += 1

    # Randomize the grid to distribute biomes
    np.random.shuffle(world_grid)

    # Reshape the grid back into 2D
    world_grid = np.reshape(world_grid, (grid_size, grid_size))

    return world_grid

def generate_gui(world_grid):
    root = tk.Tk()
    text = tk.Text(root, font=("Arial", 8), state='normal')

    for row in world_grid:
        line = ''.join(map(str, row))   
        text.insert('end', line + '\n')
    text.pack()

    root.mainloop()


# Start timer
start_time = time.time()

# Generate a linked world
world = generate_linked_world()

# Print the biome coverage
for biome, coverage in world.items():
    print(f"{biome}: {coverage}")

# Generate a world grid
world_grid = generate_world_grid(world, biome_symbols)

# Print the world grid
print(world_grid)


# End timer
end_time = time.time()

# Print the elapsed time
print(f"Elapsed time: {end_time - start_time} seconds")

# Generate a GUI
generate_gui(world_grid)

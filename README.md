# Bot-Swarm-Simulation

[![Static Badge](https://img.shields.io/badge/pygame-cyan)](https://www.pygame.org/docs/)
[![Static Badge](https://img.shields.io/badge/random-magenta)](https://docs.python.org/3/library/random.html)
[![Static Badge](https://img.shields.io/badge/sys-gray)](https://docs.python.org/3/library/sys.html)
[![Static Badge](https://img.shields.io/badge/math-teal)](https://docs.python.org/3/library/math.html)

The code initializes Pygame, sets display dimensions, defines functions for color blending and randomization, initializes food and bot groups, handles events, updates, draws sprites, and handles bot reproduction. 

# Table of Contents

- [About](#about)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Rating: 7/10](#rating)

# About

The code initializes Pygame, sets up the display, defines functions for color blending and random color generation, and creates two groups (food_list and bot_list) for holding food and bot sprites. It adds food and bots to their groups, handles events, updates the game state, draws sprites, moves bots towards food, handles collisions, and potentially adds more bots. The code simulates a simulation where bots move towards food items, eat them upon collision, and reproduce/repopulate when colliding.

# Features

The code provides a detailed description of a 2D game simulation that includes features such as Pygame Initialization, Display Setup, Color Blending and Random Color Generation Functions, Sprite Groups, Adding Food and Bots to Groups, Event Handling, Game State Updates, Sprite Rendering and Movement, Collision Handling, and Bot Reproduction/Population Growth. It initializes the Pygame library, sets up the display window, defines color blending and random color generation functions, creates two Sprite Groups (food_list and bot_list), adds food and bots to their respective groups, handles event handling, updates the game state based on events and other conditions, and handles sprites on the screen. It also handles collision handling, triggering actions like eating the food when a bot collides with a food item. The code also simulates bot reproduction or population growth, adding new bots to the game when bots collide. Overall, the code combines elements of game development, physics, and artificial life simulation to create a simulation where bots move towards food, consume it upon collision, and potentially multiply through reproduction.

# Installation

1) HTTPS - https://github.com/Statute8234/Bot-Swarm-Simulation.git
2) CLONE - Statute8234/Bot-Swarm-Simulation

# Usage

1) Initialization:
   - Import the required modules (pygame, random, sys, math).
   - Initialize Pygame with pygame.init().
   - Set up the display window with the desired width and height using pygame.display.set_mode().
   - Initialize the clock for controlling the frame rate with pygame.time.Clock().
2) Define Colors:
   - Define functions for blending colors (BLEND_COLORS) and generating random colors (RANDOM_COLOR).
   - Define color constants (RED, GREEN, BLUE, WHITE, BLACK) for convenience.
3) Circle Class:
   - Define a class circle to represent the circles (bots and food).
   - Each circle has attributes like radius, color, image, rect, and speed.
   - Method draw_shape() is used to draw the circle.
   - Method memory() is used to check if a point is in the memory list.
   - Method move_towards_food() is responsible for moving the circle towards food.
4) Adding Food and Bots:
   - Use functions addFood() and addBots() to populate the simulation with food items and bots, respectively.
5) Main Loop:
   - Create sprite groups (food_list, bot_list, all_sprites) to manage sprites.
   - Enter the main loop where the simulation takes place.
   - Handle events, such as quitting the game.
   - Update all sprites and draw them on the screen.
   - Move bots towards food, handle collisions, and repopulate bots.
   - Add more food periodically.
   - Update the display, control the frame rate, and handle user input.

# Rating

The code is clear and well-structured, with variable names being descriptive and comments provided where needed. However, some parts could be further clarified, particularly in the logic behind bot replication and repopulation. The simulation appears to work as intended, with bots moving towards food, eating it upon collision, and replicating/repopulating when colliding with each other. However, there might be issues with bot replication logic, such as arbitrary conditions leading to unpredictable behavior. The code could be more efficient in terms of performance, such as the method of choosing whether to replicate bots (random.randint). The code is reasonably readable, but there are still parts that could be made clearer, especially regarding the replication logic. The code provides a solid foundation for a circle simulation but could benefit from improvements in efficiency, scalability, and clarity, especially in the replication logic.

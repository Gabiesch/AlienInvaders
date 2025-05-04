# Alien Invasion

A classic space shooter game with modern features, built using Python and Pygame.

## Game Description

Alien Invasion is a space shooter game where you control a spaceship to defend Earth against an alien invasion. The game features various power-ups, upgrades, and increasingly challenging levels.

## Features

- **Dynamic Gameplay**: Fight against waves of aliens that increase in speed and difficulty
- **Power-ups**: Collect various power-ups that drop from destroyed aliens:
  - **Rocket**: Fires a powerful rocket that explodes on impact
  - **Boost**: Temporarily increases your ship's speed
  - **Bigger Bullets**: Temporarily increases your bullet size
  - **Faster Aliens**: Temporarily increases alien movement speed
  - **More Alien Bullets**: Temporarily allows aliens to fire more bullets
- **Upgrade System**: Between levels, spend points to upgrade your ship:
  - Increase ship speed
  - Allow more bullets on screen
  - Increase bullet speed
- **Score Tracking**: Compete for high scores with a persistent high score system
- **Visual Effects**: Enjoy particle effects for explosions and power-ups

## Controls

- **Arrow Keys**: Move your ship (Up, Down, Left, Right)
- **Spacebar**: Fire bullets
- **Q**: Quit the game
- **Mouse**: Click buttons in menus and the upgrade screen

## Installation

### Prerequisites
- Python 3.x
- Pygame

### Installation Steps
1. Clone or download this repository
2. Install the required dependencies:
   ```
   pip install pygame
   ```
3. Run the game:
   ```
   python alien_invasion.py
   ```

### Creating an Executable
To create a standalone executable:
1. Install PyInstaller:
   ```
   pip install pyinstaller
   ```
2. Run the build command:
   ```
   pyinstaller alien_invasion.spec
   ```
3. The executable will be created in the `dist` folder

## Game Rules

1. Destroy all aliens to advance to the next level
2. Avoid alien bullets and collisions with aliens
3. Collect power-ups to gain temporary advantages
4. Use points earned from destroying aliens to purchase permanent upgrades
5. The game ends when you lose all your ships

## Scoring

- Each alien destroyed: 50 points
- Points multiply with each level
- High score is saved between sessions

## Development

This game was developed using:
- Python
- Pygame
- Object-oriented programming principles

## Credits

Created as a learning project for Python game development.

## License

This project is open source and available for personal and educational use. 

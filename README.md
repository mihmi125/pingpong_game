🕹️ Neon Pong - v1.0.0

Overview
Neon Pong is an exhilarating, high-energy gaming experience built with Python. It features a modular, object-oriented architecture designed for easy expansion and maintenance. With a vibrant neon UI, stunning visual effects, and integrated audio, players can enjoy an immersive, retro-modern atmosphere.

✨ Key Features
Modular Architecture: Built with clean, extensible Python classes (Ball, Paddle, Particle).

Neon UI: High-contrast, engaging visuals with a dynamic speed meter.

Juicy Visual Effects: Features screen shake on impact and custom particle explosions.

Audio Integration: Dedicated AudioManager for tactile sound effects and music.

Customizable Gameplay: In-game settings menu allows players to adjust winning scores.

Smart AI: Adaptive CPU opponent with human-like reaction margins.

🚀 Installation & Setup
Clone the repository: ```bash
git clone https://github.com/mihmi125/pingpong_game.git

Navigate into the directory: ```bash
cd pingpong_game

Install the required dependencies: ```bash
pip install pygame


🎮 How to Play
Start the game: ```bash
python main.py

Controls:

Player 1: W / S keys.

Player 2 (PVP): Up / Down arrow keys.

Menu: Use the mouse to navigate and ESC to return to the main menu.

🛠️ Project Structure
main.py: The game orchestrator and state machine.

entities.py: Logic for the ball, paddles, and particles.

ui.py: Button rendering and text interface.

audio.py: Sound and music management.

constants.py: Global game settings (colors, speeds, dimensions).

📝 License
This project is licensed under the MIT License.
# Euler Plays Crystal

## Description
This project uses the PyBoy emulator to play Pokémon Crystal while calculating digits of Euler's number (e, the base of the natural logarithm).

## Requirements
- Python 3.x
- PyBoy
- keyboard

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Connor-Miller/algorithms_play_games.git
   cd algorithms_play_games
   ```

2. Install the required dependencies:
   ```bash
   pip install pyboy keyboard
   ```

3. Ensure you have the ROM file:
   - Place your Pokémon Crystal ROM file in the `ROMs` directory and name it `Pokemon - Crystal Version.gbc`.


## Running the Project

To run the project, execute the following command:

```bash
python euler_plays_crystal.py
```

## Notes
- The `euler_digits.txt` file should contain the digits of Euler's number, NO DECIMAL POINT.
- The `frame_count_target` and `button_press_length` variables can be adjusted to change the speed of the game.
- Press `Page Down` to turn manual mode on. In manual mode, you can control the character movement with WASD.
- Press `Page Up` to toggle manual mode off. In this mode, the game will progress automatically.

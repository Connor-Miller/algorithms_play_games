from pyboy import PyBoy
import keyboard  # Import keyboard library for key detection
from Algorithms.eulers_number import calc_next_digit_of_euler, factorial

pyboy = PyBoy("ROMs/Pokemon - Crystal Version.gbc")
pyboy.set_emulation_speed(0)

# Control mapping with weights
weightedControlMap = {
    0: 'a', # a = 4 occurrences
    1: 'a',
    2: 'a',
    3: 'a',
    4: 'b', # b = 2 occurrences
    5: 'b',
    6: 'up', # up = 1 occurrence
    7: 'left', # left = 1 occurrence
    8: 'right', # right = 1 occurrence
    9: 'down', # down = 1 occurrence
}

# Euler sequence variables
euler_sum = 0
euler_term = 0
euler_digit = 0

# Open the file to read Euler digits
with open("Algorithms/euler_digits.txt", "r") as file:
    euler_digits = file.read().strip()  # Read all digits as a string
    current_index = 0  # Initialize index to track the current digit

while not keyboard.is_pressed('esc'):  # Run until Escape is pressed
    frame_count = 0
    while frame_count < 60:

        pyboy.tick()  # Process the emulator
        
        frame_count += 1

    if frame_count == 60:
        # Get the next Euler digit from the file
        euler_digit = int(euler_digits[current_index])  # Read the next digit
        current_index += 1  # Move to the next digit

        # Ensure we don't go out of bounds
        if current_index >= len(euler_digits):
            current_index = 0  # Reset to the beginning if we reach the end

        # Map the result to controls
        control_choice = euler_digit % 10  # Total weight is 4 + 2*5 + 1 = 11
        pyboy.button(weightedControlMap[control_choice], 30)  # Send the mapped control input
        print(weightedControlMap[control_choice], control_choice, euler_digit)
        for _ in range(30):
            pyboy.tick()
        frame_count = 0  # Reset frame count for the next iteration



pyboy.stop()  # Stop the emulator

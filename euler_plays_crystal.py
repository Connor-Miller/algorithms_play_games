from pyboy import PyBoy
import keyboard  # Import keyboard library for key detection
from Algorithms.eulers_number import calc_next_digit_of_euler, factorial

pyboy = PyBoy("ROMs/Pokemon - Crystal Version.gbc")
pyboy.set_emulation_speed(4)
pyboy.tick()

# Control mapping with weights
frame_count_target = 30
button_press_length = 15
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

# Manual mode variable
manual_mode = True

while not keyboard.is_pressed('esc'):  # Run until Escape is pressed
    frame_count = 0
    while frame_count < frame_count_target:

        pyboy.tick()  # Process the emulator
        
        # Check for Page Up key to toggle manual mode
        if keyboard.is_pressed('page up'):
            manual_mode = False  # Toggle manual mode
            print("Manual mode:", manual_mode)
            pyboy.set_emulation_speed(0)

        # Check for Page Down key to toggle manual mode
        if keyboard.is_pressed('page down'):
            manual_mode = True  # Toggle manual mode
            print("Manual mode:", manual_mode)
            pyboy.set_emulation_speed(2)

        if not manual_mode:  # Only progress if not in manual mode
            frame_count += 1
            

    if frame_count == frame_count_target and not manual_mode:
        # Get the next Euler digit from the file
        euler_digit = int(euler_digits[current_index])  # Read the next digit
        current_index += 1  # Move to the next digit

        # Ensure we don't go out of bounds
        if current_index >= len(euler_digits):
            current_index = 0  # Reset to the beginning if we reach the end

        # Map the result to controls
        control_choice = euler_digit % 10  # Total weight is 4 + 2*5 + 1 = 11
        pyboy.button(weightedControlMap[control_choice], button_press_length)  # Send the mapped control input
        print("Pressed: " + weightedControlMap[control_choice] + " Digit: " + str(euler_digit))
        for _ in range(button_press_length):
            pyboy.tick()
        frame_count = 0  # Reset frame count for the next iteration



pyboy.stop()  # Stop the emulator

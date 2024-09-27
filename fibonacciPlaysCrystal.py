from pyboy import PyBoy
import keyboard  # Import keyboard library for key detection

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
    10: 'start' # start = 1 occurrence
}

# Fibonacci sequence variables
fib1, fib2 = 0, 1

while not keyboard.is_pressed('esc'):  # Run until Escape is pressed
    frame_count = 0
    while frame_count < 60:

        pyboy.tick()  # Process the emulator
        
        frame_count += 1

    if frame_count == 60:
        # Calculate the next Fibonacci number
        fib_next = fib1 + fib2
        fib1, fib2 = fib2, fib_next

        # Map the result to controls
        control_choice = fib_next % 10  # Total weight is 4 + 2*5 + 1 = 11
        pyboy.button(weightedControlMap[control_choice])  # Send the mapped control input
        print(weightedControlMap[control_choice], control_choice, fib_next)
        frame_count = 0  # Reset frame count for the next iteration



pyboy.stop()  # Stop the emulator

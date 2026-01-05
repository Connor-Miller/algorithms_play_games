"""
Basic Controls Example

Demonstrates simple button inputs and navigation.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from wrapper import GBAWrapper, Button

def main():
	rom_path = "../ROMs/Pokemon - Emerald Version (USA, Europe).gba"
	
	try:
		with GBAWrapper(rom_path) as gba:
			print(f"Started emulator: {gba}")
			print("Running basic control demo...")
			
			gba.set_speed(2.0)
			
			print("Pressing A button 5 times...")
			gba.input.tap(Button.A, times=5, delay_frames=20)
			
			print("Holding B for 30 frames...")
			gba.input.hold(Button.B, frames=30)
			
			print("Navigating menu: DOWN, DOWN, A...")
			gba.input.navigate_menu([Button.DOWN, Button.DOWN], confirm=True)
			
			print("Pressing button combo (START + SELECT)...")
			gba.input.combo([Button.START, Button.SELECT], hold_frames=10)
			
			print("Waiting 60 frames...")
			gba.input.wait_frames(60)
			
			print(f"Demo complete! Final state: {gba.get_state()}")
			
	except ImportError as e:
		print(f"Error: {e}")
		print("\nMake sure pygba and mgba are installed:")
		print("  pip install pygba")
		print("  pip install mgba")

if __name__ == "__main__":
	main()


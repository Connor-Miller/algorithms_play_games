"""
Full Automation Example

Demonstrates a complete automation workflow using all wrapper features.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from wrapper import GBAWrapper, Button, ScreenRegion

def main():
	rom_path = "../ROMs/Pokemon - Emerald Version (USA, Europe).gba"
	
	try:
		with GBAWrapper(rom_path) as gba:
			print(f"Started emulator: {gba}")
			print("Running full automation demo...\n")
			
			gba.set_speed(2.0)
			
			print("Step 1: Quick save initial state")
			gba.save_state.quick_save()
			print("  ✓ Quick save created")
			
			print("\nStep 2: Navigate through intro")
			for i in range(10):
				gba.input.press(Button.A)
				gba.input.wait_frames(15)
				
				if i % 3 == 0:
					gba.screen.save_screenshot(f"screenshots/frame_{i:03d}.png")
					print(f"  Screenshot saved: frame_{i:03d}.png")
			
			print("\nStep 3: Monitor memory")
			gba.memory.watch(0x02000000)
			gba.memory.watch(0x02000010)
			
			for _ in range(50):
				gba.tick()
				changes = gba.memory.get_watched_changes()
				if changes:
					print("  Memory changed:", 
						  {f"0x{addr:08X}": f"{old}->{new}" 
						   for addr, (old, new) in changes.items()})
			
			print("\nStep 4: Save state to file")
			gba.save_state.save_state_file("saves/automation_checkpoint.state")
			print("  ✓ State saved to file")
			
			print("\nStep 5: Test save state system")
			original_frame = gba.frame_count
			print(f"  Current frame: {original_frame}")
			
			gba.run_frames(100)
			print(f"  After 100 frames: {gba.frame_count}")
			
			print("  Loading quick save...")
			gba.save_state.quick_load()
			print(f"  Frame after load: {gba.frame_count}")
			
			print("\nStep 6: Speed control demo")
			speeds = [1.0, 2.0, 0]
			for speed in speeds:
				if speed == 0:
					print("  Testing turbo mode...")
					gba.turbo_mode()
				else:
					print(f"  Testing {speed}x speed...")
					gba.set_speed(speed)
				
				start_frame = gba.frame_count
				gba.run_frames(60)
				print(f"    Ran from frame {start_frame} to {gba.frame_count}")
			
			print("\nStep 7: Screen capture")
			try:
				screen = gba.screen.capture()
				print(f"  Captured screen: {screen.size} pixels")
				
				pixel = gba.screen.get_pixel(120, 80)
				print(f"  Center pixel RGB: {pixel}")
				
				region = gba.screen.get_region(0, 0, 50, 50)
				print(f"  Captured region: {region.size} pixels")
			except ImportError as e:
				print(f"  Skipping screen capture (PIL not installed)")
			
			print("\nStep 8: OCR demo (if available)")
			try:
				dialog_region = ScreenRegion(0, 120, 240, 40)
				text = gba.screen.read_text(region=dialog_region.as_tuple())
				if text:
					print(f"  Detected text: '{text}'")
				else:
					print("  No text detected")
			except ImportError:
				print("  Skipping OCR (pytesseract not installed)")
			
			print("\n" + "="*50)
			print("Automation demo complete!")
			print(f"Final state: {gba}")
			print(f"Total frames processed: {gba.frame_count}")
			print("="*50)
			
	except ImportError as e:
		print(f"Error: {e}")
		print("\nMake sure pygba and mgba are installed:")
		print("  pip install pygba")
		print("  pip install mgba")
	except FileNotFoundError as e:
		print(f"Error: {e}")
		print("\nMake sure the ROM file exists at the specified path")

if __name__ == "__main__":
	Path("screenshots").mkdir(exist_ok=True)
	Path("saves").mkdir(exist_ok=True)
	main()


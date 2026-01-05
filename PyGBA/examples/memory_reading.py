"""
Memory Reading Example

Demonstrates reading various data types from game memory.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from wrapper import GBAWrapper, Button, MemoryAddress

def main():
	rom_path = "../ROMs/Pokemon - Emerald Version (USA, Europe).gba"
	
	try:
		with GBAWrapper(rom_path) as gba:
			print(f"Started emulator: {gba}")
			print("Running memory reading demo...")
			
			gba.turbo_mode()
			
			gba.input.tap(Button.START, times=3)
			gba.input.wait_frames(100)
			
			print("\nReading memory values:")
			
			byte_val = gba.memory.read_byte(0x02000000)
			print(f"Byte at 0x02000000: 0x{byte_val:02X} ({byte_val})")
			
			u16_val = gba.memory.read_u16(0x02000000)
			print(f"U16 at 0x02000000: 0x{u16_val:04X} ({u16_val})")
			
			u32_val = gba.memory.read_u32(0x02000000)
			print(f"U32 at 0x02000000: 0x{u32_val:08X} ({u32_val})")
			
			bytes_val = gba.memory.read_bytes(0x02000000, 8)
			print(f"8 bytes at 0x02000000: {bytes_val.hex()}")
			
			print("\nWatching memory addresses...")
			gba.memory.watch(0x02000000)
			gba.memory.watch(0x02000001)
			
			for i in range(100):
				gba.tick()
				changes = gba.memory.get_watched_changes()
				if changes:
					print(f"Frame {gba.frame_count}: Memory changes detected!")
					for addr, (old, new) in changes.items():
						print(f"  0x{addr:08X}: {old} -> {new}")
			
			print("\nDemo complete!")
			
	except ImportError as e:
		print(f"Error: {e}")
		print("\nMake sure pygba and mgba are installed:")
		print("  pip install pygba")
		print("  pip install mgba")

if __name__ == "__main__":
	main()


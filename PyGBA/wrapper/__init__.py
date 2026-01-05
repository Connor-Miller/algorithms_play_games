"""
GBA Wrapper - A high-level wrapper around pygba/mGBA for game automation
"""

from .types import Button, ScreenRegion, MemoryAddress, GameState

__all__ = [
	"Button",
	"ScreenRegion", 
	"MemoryAddress",
	"GameState",
]

try:
	from .gba_wrapper import GBAWrapper
	__all__.append("GBAWrapper")
except ImportError as e:
	import warnings
	warnings.warn(
		f"GBAWrapper could not be imported. Make sure pygba and mgba are installed. Error: {e}"
	)


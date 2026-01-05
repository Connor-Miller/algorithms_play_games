from enum import Enum
from dataclasses import dataclass
from typing import Tuple, Optional

class Button(Enum):
	"""GBA button inputs"""
	A = "button_a"
	B = "button_b"
	START = "button_start"
	SELECT = "button_select"
	UP = "button_up"
	DOWN = "button_down"
	LEFT = "button_left"
	RIGHT = "button_right"
	L = "button_l"
	R = "button_r"

@dataclass
class ScreenRegion:
	"""Defines a rectangular region on the screen"""
	x: int
	y: int
	width: int
	height: int
	
	def as_tuple(self) -> Tuple[int, int, int, int]:
		return (self.x, self.y, self.width, self.height)

@dataclass
class MemoryAddress:
	"""Type-safe memory address wrapper"""
	address: int
	
	def __post_init__(self):
		if not (0 <= self.address <= 0xFFFFFFFF):
			raise ValueError(f"Invalid memory address: 0x{self.address:08X}")
	
	def __str__(self) -> str:
		return f"0x{self.address:08X}"

@dataclass
class GameState:
	"""Generic game state container"""
	frame_count: int
	running: bool
	speed_multiplier: float = 1.0


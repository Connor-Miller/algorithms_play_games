from typing import Optional, Union
from pathlib import Path
from .types import GameState
from .input_helper import InputHelper
from .memory_helper import MemoryHelper
from .screen_helper import ScreenHelper
from .save_state_helper import SaveStateHelper

class GBAWrapper:
	"""
	High-level wrapper around pygba/mGBA for GBA game automation.
	
	Provides convenient helper methods for input, memory reading, screen capture,
	save states, and game speed control.
	
	Usage:
		with GBAWrapper("path/to/rom.gba") as gba:
			gba.input.press(Button.A)
			hp = gba.memory.read_u16(0x02000000)
			gba.screen.save_screenshot("frame.png")
	"""
	
	def __init__(self, rom_path: Union[str, Path], autoload_save: bool = True):
		"""
		Initialize the GBA wrapper.
		
		Args:
			rom_path: Path to the GBA ROM file
			autoload_save: Whether to automatically load the save file
		"""
		self.rom_path = Path(rom_path)
		self.autoload_save = autoload_save
		self.gba = None
		self._running = False
		self._frame_count = 0
		self._speed_multiplier = 1.0
		
		if not self.rom_path.exists():
			raise FileNotFoundError(f"ROM file not found: {self.rom_path}")
		
		self.input = InputHelper(self)
		self.memory = MemoryHelper(self)
		self.screen = ScreenHelper(self)
		self.save_state = SaveStateHelper(self)
	
	def _ensure_pygba(self) -> None:
		"""Ensure pygba is initialized"""
		if self.gba is None:
			raise RuntimeError(
				"GBA emulator not initialized. Use 'with GBAWrapper(...)' or call start() first.\n"
				"Note: pygba and mgba Python bindings must be installed."
			)
	
	def start(self) -> None:
		"""
		Start the emulator.
		
		Note: This is automatically called when using the context manager.
		"""
		try:
			from pygba import PyGBA
			
			self.gba = PyGBA.load(str(self.rom_path), autoload_save=self.autoload_save)
			self._running = True
			self._frame_count = 0
			
		except ImportError as e:
			raise ImportError(
				f"Cannot import pygba. Make sure pygba and mgba are installed.\n"
				f"Error: {e}\n\n"
				f"Installation:\n"
				f"  pip install pygba\n"
				f"  pip install mgba  (Note: May require building from source on Windows)"
			)
	
	def stop(self) -> None:
		"""
		Stop the emulator and clean up resources.
		
		Note: This is automatically called when using the context manager.
		"""
		if self.gba is not None:
			try:
				self.input.release_all()
			except Exception:
				pass
			
			self.gba = None
			self._running = False
	
	def tick(self) -> None:
		"""
		Advance the emulation by one frame.
		"""
		self._ensure_pygba()
		self.gba.step()
		self._frame_count += 1
	
	def run_frames(self, frames: int) -> None:
		"""
		Run the emulator for a specified number of frames.
		
		Args:
			frames: Number of frames to run
		"""
		for _ in range(frames):
			self.tick()
	
	def set_speed(self, multiplier: float) -> None:
		"""
		Set the emulation speed.
		
		Args:
			multiplier: Speed multiplier (1.0 = normal, 2.0 = 2x speed, 0 = unlimited)
		"""
		self._ensure_pygba()
		self._speed_multiplier = multiplier
		
		if multiplier == 0:
			self.gba.set_speed(0)
		else:
			target_fps = 60.0 * multiplier
			self.gba.set_speed(int(target_fps))
	
	def turbo_mode(self) -> None:
		"""
		Enable turbo mode (run as fast as possible).
		"""
		self.set_speed(0)
	
	def normal_speed(self) -> None:
		"""
		Reset to normal speed (60 FPS).
		"""
		self.set_speed(1.0)
	
	def frame_advance(self) -> None:
		"""
		Advance exactly one frame (same as tick()).
		"""
		self.tick()
	
	def reset(self) -> None:
		"""
		Reset the emulator (soft reset).
		"""
		self._ensure_pygba()
		self.gba.reset()
		self._frame_count = 0
	
	def get_state(self) -> GameState:
		"""
		Get the current game state information.
		
		Returns:
			GameState object with current frame count and other info
		"""
		return GameState(
			frame_count=self._frame_count,
			running=self._running,
			speed_multiplier=self._speed_multiplier
		)
	
	@property
	def frame_count(self) -> int:
		"""Get the current frame count"""
		return self._frame_count
	
	@property
	def is_running(self) -> bool:
		"""Check if the emulator is running"""
		return self._running
	
	def __enter__(self):
		"""Context manager entry"""
		self.start()
		return self
	
	def __exit__(self, exc_type, exc_val, exc_tb):
		"""Context manager exit"""
		self.stop()
		return False
	
	def __repr__(self) -> str:
		status = "running" if self._running else "stopped"
		return f"GBAWrapper(rom={self.rom_path.name}, status={status}, frame={self._frame_count})"


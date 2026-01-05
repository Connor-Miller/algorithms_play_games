from typing import Union, Dict, Optional, TYPE_CHECKING
from pathlib import Path
import pickle

if TYPE_CHECKING:
	from .gba_wrapper import GBAWrapper

class SaveStateHelper:
	"""Helper class for managing save states"""
	
	def __init__(self, wrapper: 'GBAWrapper'):
		self.wrapper = wrapper
		self._slots: Dict[int, bytes] = {}
		self._quick_save_slot: Optional[bytes] = None
	
	def save_state(self, slot: int = 0) -> None:
		"""
		Save the current state to a numbered slot.
		
		Args:
			slot: Slot number (0-9)
		"""
		if not (0 <= slot <= 9):
			raise ValueError(f"Slot must be between 0 and 9, got {slot}")
		
		try:
			self.wrapper._ensure_pygba()
			state = self.wrapper.gba.save_state()
			self._slots[slot] = state
		except AttributeError:
			raise RuntimeError("Cannot save state - pygba not initialized")
	
	def load_state(self, slot: int = 0) -> None:
		"""
		Load a state from a numbered slot.
		
		Args:
			slot: Slot number (0-9)
		"""
		if not (0 <= slot <= 9):
			raise ValueError(f"Slot must be between 0 and 9, got {slot}")
		
		if slot not in self._slots:
			raise ValueError(f"No save state found in slot {slot}")
		
		try:
			self.wrapper._ensure_pygba()
			self.wrapper.gba.load_state(self._slots[slot])
		except AttributeError:
			raise RuntimeError("Cannot load state - pygba not initialized")
	
	def save_state_file(self, path: Union[str, Path]) -> None:
		"""
		Save the current state to a file.
		
		Args:
			path: File path to save the state
		"""
		path = Path(path)
		try:
			self.wrapper._ensure_pygba()
			state = self.wrapper.gba.save_state()
			
			with open(path, 'wb') as f:
				pickle.dump(state, f)
		except AttributeError:
			raise RuntimeError("Cannot save state - pygba not initialized")
	
	def load_state_file(self, path: Union[str, Path]) -> None:
		"""
		Load a state from a file.
		
		Args:
			path: File path to load the state from
		"""
		path = Path(path)
		if not path.exists():
			raise FileNotFoundError(f"Save state file not found: {path}")
		
		try:
			self.wrapper._ensure_pygba()
			
			with open(path, 'rb') as f:
				state = pickle.load(f)
			
			self.wrapper.gba.load_state(state)
		except AttributeError:
			raise RuntimeError("Cannot load state - pygba not initialized")
	
	def quick_save(self) -> None:
		"""
		Quick save to a temporary slot (overwrites previous quick save).
		"""
		try:
			self.wrapper._ensure_pygba()
			self._quick_save_slot = self.wrapper.gba.save_state()
		except AttributeError:
			raise RuntimeError("Cannot quick save - pygba not initialized")
	
	def quick_load(self) -> None:
		"""
		Quick load from the temporary slot.
		"""
		if self._quick_save_slot is None:
			raise ValueError("No quick save found")
		
		try:
			self.wrapper._ensure_pygba()
			self.wrapper.gba.load_state(self._quick_save_slot)
		except AttributeError:
			raise RuntimeError("Cannot quick load - pygba not initialized")
	
	def has_save(self, slot: int) -> bool:
		"""
		Check if a save state exists in a slot.
		
		Args:
			slot: Slot number to check
			
		Returns:
			True if a save exists in the slot
		"""
		return slot in self._slots
	
	def clear_slot(self, slot: int) -> None:
		"""
		Clear a save state slot.
		
		Args:
			slot: Slot number to clear
		"""
		self._slots.pop(slot, None)
	
	def clear_all_slots(self) -> None:
		"""Clear all save state slots"""
		self._slots.clear()
		self._quick_save_slot = None
	
	def list_slots(self) -> list[int]:
		"""
		Get a list of all occupied save slots.
		
		Returns:
			List of slot numbers that have saves
		"""
		return sorted(self._slots.keys())


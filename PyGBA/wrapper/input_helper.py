from typing import List, Union, TYPE_CHECKING
from .types import Button

if TYPE_CHECKING:
	from .gba_wrapper import GBAWrapper

class InputHelper:
	"""Helper class for handling GBA input/button presses"""
	
	def __init__(self, wrapper: 'GBAWrapper'):
		self.wrapper = wrapper
		self._pressed_buttons: set[Button] = set()
	
	def press(self, button: Button) -> None:
		"""
		Press a button for a single frame.
		
		Args:
			button: The button to press
		"""
		try:
			self.wrapper._ensure_pygba()
			self.wrapper.gba.button_press(button.value)
			self._pressed_buttons.add(button)
			self.wrapper.tick()
			self.wrapper.gba.button_release(button.value)
			self._pressed_buttons.discard(button)
		except AttributeError:
			raise RuntimeError("Cannot press button - pygba not initialized")
	
	def hold(self, button: Button, frames: int) -> None:
		"""
		Hold a button down for multiple frames.
		
		Args:
			button: The button to hold
			frames: Number of frames to hold the button
		"""
		try:
			self.wrapper._ensure_pygba()
			self.wrapper.gba.button_press(button.value)
			self._pressed_buttons.add(button)
			
			for _ in range(frames):
				self.wrapper.tick()
			
			self.wrapper.gba.button_release(button.value)
			self._pressed_buttons.discard(button)
		except AttributeError:
			raise RuntimeError("Cannot hold button - pygba not initialized")
	
	def tap(self, button: Button, times: int = 1, delay_frames: int = 10) -> None:
		"""
		Tap a button multiple times with delay between taps.
		
		Args:
			button: The button to tap
			times: Number of times to tap
			delay_frames: Frames to wait between taps
		"""
		for _ in range(times):
			self.press(button)
			self.wait_frames(delay_frames)
	
	def combo(self, buttons: List[Button], hold_frames: int = 1) -> None:
		"""
		Press multiple buttons simultaneously.
		
		Args:
			buttons: List of buttons to press together
			hold_frames: How long to hold the combo
		"""
		try:
			self.wrapper._ensure_pygba()
			
			for button in buttons:
				self.wrapper.gba.button_press(button.value)
				self._pressed_buttons.add(button)
			
			for _ in range(hold_frames):
				self.wrapper.tick()
			
			for button in buttons:
				self.wrapper.gba.button_release(button.value)
				self._pressed_buttons.discard(button)
		except AttributeError:
			raise RuntimeError("Cannot execute combo - pygba not initialized")
	
	def navigate_menu(self, directions: List[Union[Button, str]], confirm: bool = True) -> None:
		"""
		Navigate through menus using directional inputs.
		
		Args:
			directions: List of directions (Button.UP, Button.DOWN, etc.) or strings ("up", "down")
			confirm: Whether to press A at the end
		
		Example:
			gba.input.navigate_menu([Button.DOWN, Button.DOWN, Button.RIGHT], confirm=True)
			gba.input.navigate_menu(["down", "down", "right"], confirm=True)
		"""
		for direction in directions:
			if isinstance(direction, str):
				direction = Button[direction.upper()]
			
			self.press(direction)
			self.wait_frames(10)
		
		if confirm:
			self.press(Button.A)
	
	def wait_frames(self, frames: int) -> None:
		"""
		Wait for a specified number of frames without input.
		
		Args:
			frames: Number of frames to wait
		"""
		for _ in range(frames):
			self.wrapper.tick()
	
	def release_all(self) -> None:
		"""Release all currently pressed buttons"""
		try:
			self.wrapper._ensure_pygba()
			for button in list(self._pressed_buttons):
				self.wrapper.gba.button_release(button.value)
			self._pressed_buttons.clear()
		except AttributeError:
			pass


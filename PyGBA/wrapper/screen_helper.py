from typing import Tuple, Optional, Union, TYPE_CHECKING
from pathlib import Path
from .types import ScreenRegion

if TYPE_CHECKING:
	from .gba_wrapper import GBAWrapper
	from PIL import Image

class ScreenHelper:
	"""Helper class for screen capture and OCR"""
	
	def __init__(self, wrapper: 'GBAWrapper'):
		self.wrapper = wrapper
		self._pil_available = False
		self._pytesseract_available = False
		
		try:
			import PIL
			self._pil_available = True
		except ImportError:
			pass
		
		try:
			import pytesseract
			self._pytesseract_available = True
		except ImportError:
			pass
	
	def _ensure_pil(self) -> None:
		"""Ensure PIL is available"""
		if not self._pil_available:
			raise ImportError("PIL/Pillow is required for screen operations. Install with: pip install pillow")
	
	def _ensure_ocr(self) -> None:
		"""Ensure pytesseract is available"""
		if not self._pytesseract_available:
			raise ImportError("pytesseract is required for OCR. Install with: pip install pytesseract")
	
	def capture(self) -> 'Image.Image':
		"""
		Capture the current screen as a PIL Image.
		
		Returns:
			PIL Image object of the current screen
		"""
		self._ensure_pil()
		try:
			self.wrapper._ensure_pygba()
			from PIL import Image
			import numpy as np
			
			screen_array = self.wrapper.gba.get_screen()
			return Image.fromarray(screen_array.astype('uint8'), 'RGB')
		except AttributeError:
			raise RuntimeError("Cannot capture screen - pygba not initialized")
	
	def save_screenshot(self, path: Union[str, Path]) -> None:
		"""
		Save a screenshot to a file.
		
		Args:
			path: File path to save the screenshot
		"""
		img = self.capture()
		img.save(str(path))
	
	def get_pixel(self, x: int, y: int) -> Tuple[int, int, int]:
		"""
		Get the RGB color of a specific pixel.
		
		Args:
			x: X coordinate (0-239 for GBA)
			y: Y coordinate (0-159 for GBA)
			
		Returns:
			RGB tuple (r, g, b)
		"""
		img = self.capture()
		return img.getpixel((x, y))
	
	def get_region(self, x: int, y: int, width: int, height: int) -> 'Image.Image':
		"""
		Capture a specific region of the screen.
		
		Args:
			x: X coordinate of top-left corner
			y: Y coordinate of top-left corner
			width: Width of the region
			height: Height of the region
			
		Returns:
			PIL Image of the specified region
		"""
		img = self.capture()
		return img.crop((x, y, x + width, y + height))
	
	def get_region_from_rect(self, region: ScreenRegion) -> 'Image.Image':
		"""
		Capture a region using a ScreenRegion object.
		
		Args:
			region: ScreenRegion defining the area to capture
			
		Returns:
			PIL Image of the specified region
		"""
		return self.get_region(region.x, region.y, region.width, region.height)
	
	def read_text(self, region: Optional[Union[ScreenRegion, Tuple[int, int, int, int]]] = None, 
				  config: str = '--psm 6') -> str:
		"""
		Use OCR to read text from the screen.
		
		Args:
			region: Optional region to read from (full screen if None)
			config: Tesseract configuration string
			
		Returns:
			Extracted text
		"""
		self._ensure_ocr()
		import pytesseract
		
		if region is None:
			img = self.capture()
		elif isinstance(region, ScreenRegion):
			img = self.get_region_from_rect(region)
		else:
			x, y, w, h = region
			img = self.get_region(x, y, w, h)
		
		text = pytesseract.image_to_string(img, config=config)
		return text.strip()
	
	def wait_for_text(self, text: str, timeout_frames: int = 300, 
					  region: Optional[Union[ScreenRegion, Tuple[int, int, int, int]]] = None,
					  case_sensitive: bool = False) -> bool:
		"""
		Wait for specific text to appear on screen.
		
		Args:
			text: Text to wait for
			timeout_frames: Maximum frames to wait
			region: Optional region to check
			case_sensitive: Whether to match case exactly
			
		Returns:
			True if text was found, False if timeout reached
		"""
		search_text = text if case_sensitive else text.lower()
		
		for _ in range(timeout_frames):
			try:
				screen_text = self.read_text(region)
				if not case_sensitive:
					screen_text = screen_text.lower()
				
				if search_text in screen_text:
					return True
			except Exception:
				pass
			
			self.wrapper.tick()
		
		return False
	
	def compare_screens(self, img1: 'Image.Image', img2: 'Image.Image') -> float:
		"""
		Compare two screen images and return a similarity score.
		
		Args:
			img1: First image
			img2: Second image
			
		Returns:
			Similarity score (0.0 to 1.0, where 1.0 is identical)
		"""
		self._ensure_pil()
		import numpy as np
		
		arr1 = np.array(img1)
		arr2 = np.array(img2)
		
		if arr1.shape != arr2.shape:
			raise ValueError("Images must have the same dimensions")
		
		diff = np.abs(arr1.astype(float) - arr2.astype(float))
		max_diff = 255.0 * arr1.size
		total_diff = np.sum(diff)
		
		return 1.0 - (total_diff / max_diff)
	
	def wait_for_screen_change(self, threshold: float = 0.95, timeout_frames: int = 300) -> bool:
		"""
		Wait for the screen to change significantly.
		
		Args:
			threshold: Similarity threshold (lower means more sensitive to changes)
			timeout_frames: Maximum frames to wait
			
		Returns:
			True if screen changed, False if timeout reached
		"""
		initial_screen = self.capture()
		
		for _ in range(timeout_frames):
			self.wrapper.tick()
			current_screen = self.capture()
			
			similarity = self.compare_screens(initial_screen, current_screen)
			if similarity < threshold:
				return True
		
		return False


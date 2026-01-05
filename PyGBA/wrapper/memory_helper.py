from typing import Union, Dict, Optional, TYPE_CHECKING
from .types import MemoryAddress

if TYPE_CHECKING:
	from .gba_wrapper import GBAWrapper

class MemoryHelper:
	"""Helper class for reading GBA memory"""
	
	def __init__(self, wrapper: 'GBAWrapper'):
		self.wrapper = wrapper
		self._watched_addresses: Dict[int, any] = {}
	
	def read_byte(self, address: Union[int, MemoryAddress]) -> int:
		"""
		Read a single byte from memory.
		
		Args:
			address: Memory address to read from
			
		Returns:
			Byte value (0-255)
		"""
		addr = address.address if isinstance(address, MemoryAddress) else address
		try:
			self.wrapper._ensure_pygba()
			return self.wrapper.gba.read_memory(addr, 1)[0]
		except AttributeError:
			raise RuntimeError("Cannot read memory - pygba not initialized")
	
	def read_bytes(self, address: Union[int, MemoryAddress], length: int) -> bytes:
		"""
		Read multiple bytes from memory.
		
		Args:
			address: Starting memory address
			length: Number of bytes to read
			
		Returns:
			Bytes object containing the data
		"""
		addr = address.address if isinstance(address, MemoryAddress) else address
		try:
			self.wrapper._ensure_pygba()
			return bytes(self.wrapper.gba.read_memory(addr, length))
		except AttributeError:
			raise RuntimeError("Cannot read memory - pygba not initialized")
	
	def read_u16(self, address: Union[int, MemoryAddress], little_endian: bool = True) -> int:
		"""
		Read a 16-bit unsigned integer from memory.
		
		Args:
			address: Memory address to read from
			little_endian: Whether to use little-endian byte order (default: True)
			
		Returns:
			16-bit integer value
		"""
		data = self.read_bytes(address, 2)
		return int.from_bytes(data, byteorder='little' if little_endian else 'big', signed=False)
	
	def read_u32(self, address: Union[int, MemoryAddress], little_endian: bool = True) -> int:
		"""
		Read a 32-bit unsigned integer from memory.
		
		Args:
			address: Memory address to read from
			little_endian: Whether to use little-endian byte order (default: True)
			
		Returns:
			32-bit integer value
		"""
		data = self.read_bytes(address, 4)
		return int.from_bytes(data, byteorder='little' if little_endian else 'big', signed=False)
	
	def read_i16(self, address: Union[int, MemoryAddress], little_endian: bool = True) -> int:
		"""
		Read a 16-bit signed integer from memory.
		
		Args:
			address: Memory address to read from
			little_endian: Whether to use little-endian byte order (default: True)
			
		Returns:
			16-bit signed integer value
		"""
		data = self.read_bytes(address, 2)
		return int.from_bytes(data, byteorder='little' if little_endian else 'big', signed=True)
	
	def read_i32(self, address: Union[int, MemoryAddress], little_endian: bool = True) -> int:
		"""
		Read a 32-bit signed integer from memory.
		
		Args:
			address: Memory address to read from
			little_endian: Whether to use little-endian byte order (default: True)
			
		Returns:
			32-bit signed integer value
		"""
		data = self.read_bytes(address, 4)
		return int.from_bytes(data, byteorder='little' if little_endian else 'big', signed=True)
	
	def read_string(self, address: Union[int, MemoryAddress], length: int, encoding: str = 'ascii') -> str:
		"""
		Read a string from memory.
		
		Args:
			address: Memory address to read from
			length: Maximum length to read
			encoding: Text encoding (default: 'ascii')
			
		Returns:
			Decoded string (stops at null terminator if found)
		"""
		data = self.read_bytes(address, length)
		null_pos = data.find(b'\x00')
		if null_pos != -1:
			data = data[:null_pos]
		
		try:
			return data.decode(encoding)
		except UnicodeDecodeError:
			return data.decode(encoding, errors='replace')
	
	def watch(self, address: Union[int, MemoryAddress]) -> None:
		"""
		Start watching a memory address for changes.
		
		Args:
			address: Memory address to watch
		"""
		addr = address.address if isinstance(address, MemoryAddress) else address
		self._watched_addresses[addr] = self.read_byte(addr)
	
	def get_watched_changes(self) -> Dict[int, tuple[any, any]]:
		"""
		Get all watched addresses that have changed.
		
		Returns:
			Dictionary mapping address -> (old_value, new_value)
		"""
		changes = {}
		for addr, old_value in list(self._watched_addresses.items()):
			new_value = self.read_byte(addr)
			if new_value != old_value:
				changes[addr] = (old_value, new_value)
				self._watched_addresses[addr] = new_value
		return changes
	
	def unwatch(self, address: Union[int, MemoryAddress]) -> None:
		"""
		Stop watching a memory address.
		
		Args:
			address: Memory address to stop watching
		"""
		addr = address.address if isinstance(address, MemoryAddress) else address
		self._watched_addresses.pop(addr, None)
	
	def clear_watches(self) -> None:
		"""Clear all watched addresses"""
		self._watched_addresses.clear()


# GBA Automation Wrapper

A high-level Python wrapper around pygba/mGBA for easy Game Boy Advance game automation with excellent developer experience.

## Features

- **Input Control**: Press, hold, tap, and combo button inputs
- **Memory Reading**: Read bytes, integers, and strings from game memory
- **Screen Capture**: Capture screenshots and read pixels
- **OCR Support**: Extract text from the game screen
- **Save States**: Manage save states with slots and quick save/load
- **Speed Control**: Control emulation speed, turbo mode, and frame stepping
- **Type-Safe**: Full type hints for excellent IDE autocomplete
- **Context Manager**: Clean resource management with `with` statement

## Installation

### Basic Installation

```bash
pip install -r requirements.txt
```

### Installing mGBA Python Bindings

**Note**: The `mgba` Python bindings are required but may not be available as pre-built wheels for Windows.

#### Linux/macOS (Python 3.10+)
```bash
pip install mgba
```

#### Windows
Building from source is required. See the [pygba documentation](https://github.com/dvruette/pygba) for detailed instructions.

## Quick Start

```python
from wrapper import GBAWrapper, Button

with GBAWrapper("ROMs/Pokemon - Emerald Version (USA, Europe).gba") as gba:
	gba.set_speed(2.0)
	
	gba.input.tap(Button.A, times=5)
	gba.input.navigate_menu([Button.DOWN, Button.DOWN], confirm=True)
	
	hp = gba.memory.read_u16(0x02000000)
	print(f"HP: {hp}")
	
	gba.screen.save_screenshot("screenshot.png")
	
	gba.save_state.quick_save()
```

## API Reference

### GBAWrapper

Main wrapper class that provides access to all helper modules.

```python
wrapper = GBAWrapper(rom_path, autoload_save=True)
wrapper.start()
wrapper.stop()
wrapper.tick()
wrapper.run_frames(60)
wrapper.set_speed(2.0)
wrapper.turbo_mode()
wrapper.reset()
```

### Input Helper

Access via `wrapper.input`

```python
gba.input.press(Button.A)
gba.input.hold(Button.B, frames=30)
gba.input.tap(Button.START, times=3, delay_frames=10)
gba.input.combo([Button.L, Button.R], hold_frames=5)
gba.input.navigate_menu([Button.DOWN, Button.RIGHT], confirm=True)
gba.input.wait_frames(60)
gba.input.release_all()
```

#### Available Buttons

- `Button.A`, `Button.B`
- `Button.START`, `Button.SELECT`
- `Button.UP`, `Button.DOWN`, `Button.LEFT`, `Button.RIGHT`
- `Button.L`, `Button.R`

### Memory Helper

Access via `wrapper.memory`

```python
byte = gba.memory.read_byte(0x02000000)
u16 = gba.memory.read_u16(0x02000000)
u32 = gba.memory.read_u32(0x02000000)
i16 = gba.memory.read_i16(0x02000000)
i32 = gba.memory.read_i32(0x02000000)
data = gba.memory.read_bytes(0x02000000, 16)
text = gba.memory.read_string(0x02000000, 20)

gba.memory.watch(0x02000000)
changes = gba.memory.get_watched_changes()
gba.memory.unwatch(0x02000000)
```

### Screen Helper

Access via `wrapper.screen`

```python
image = gba.screen.capture()
gba.screen.save_screenshot("frame.png")

pixel = gba.screen.get_pixel(120, 80)
region = gba.screen.get_region(0, 0, 50, 50)

text = gba.screen.read_text(region=(0, 120, 240, 40))
found = gba.screen.wait_for_text("GAME OVER", timeout_frames=300)

changed = gba.screen.wait_for_screen_change(threshold=0.95)
```

### Save State Helper

Access via `wrapper.save_state`

```python
gba.save_state.save_state(slot=0)
gba.save_state.load_state(slot=0)

gba.save_state.save_state_file("checkpoint.state")
gba.save_state.load_state_file("checkpoint.state")

gba.save_state.quick_save()
gba.save_state.quick_load()

has_save = gba.save_state.has_save(slot=0)
slots = gba.save_state.list_slots()
```

## Examples

Check out the `examples/` directory:

- **basic_controls.py**: Simple button inputs and navigation
- **memory_reading.py**: Reading and monitoring game memory
- **full_automation.py**: Complete automation workflow

Run examples:
```bash
cd PyGBA
python examples/basic_controls.py
python examples/memory_reading.py
python examples/full_automation.py
```

## Architecture

```
GBAWrapper
├── input (InputHelper)
│   └── Button press/hold/combo
├── memory (MemoryHelper)
│   └── Read bytes/integers/strings
├── screen (ScreenHelper)
│   └── Capture/OCR/pixel reading
└── save_state (SaveStateHelper)
    └── Save/load state management
```

## Type Definitions

```python
from wrapper import Button, ScreenRegion, MemoryAddress, GameState

button = Button.A
region = ScreenRegion(x=0, y=120, width=240, height=40)
addr = MemoryAddress(0x02000000)
state = gba.get_state()
```

## Dependencies

- **pygba**: GBA emulator wrapper
- **mgba**: mGBA Python bindings (required)
- **numpy**: Numerical operations
- **pillow**: Image processing
- **pytesseract**: OCR (optional)

## Troubleshooting

### "No module named 'mgba'"

The mGBA Python bindings need to be installed separately. On Windows, this requires building from source.

See: https://github.com/dvruette/pygba#installation

### "GBA emulator not initialized"

Make sure to use the context manager or call `start()` before using the wrapper:

```python
with GBAWrapper(rom_path) as gba:
	pass
```

or

```python
gba = GBAWrapper(rom_path)
gba.start()
try:
	pass
finally:
	gba.stop()
```

### OCR Not Working

Install Tesseract OCR:
- **Windows**: Download from https://github.com/UB-Mannheim/tesseract/wiki
- **Linux**: `sudo apt-get install tesseract-ocr`
- **macOS**: `brew install tesseract`

Then install the Python wrapper:
```bash
pip install pytesseract
```

## License

This wrapper is provided as-is for educational and automation purposes. Make sure you own the ROMs you're automating.

## Contributing

Feel free to extend this wrapper with additional features! Some ideas:

- Game-specific wrappers (Pokemon, Zelda, etc.)
- AI/ML integration
- Recording and playback
- Network multiplayer support
- Performance profiling

## Credits

Built on top of:
- [pygba](https://github.com/dvruette/pygba) by Dimitri von Rütte
- [mGBA](https://mgba.io/) emulator


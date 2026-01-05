# GBA Wrapper Quick Start Guide

## Installation Steps

### 1. Install Python 3.12

If you don't have Python 3.12 yet, download and install it from:
https://www.python.org/downloads/release/python-31210/

Make sure to check "Add Python to PATH" during installation!

### 2. Install Dependencies

```bash
cd PyGBA
py -3.12 -m pip install -r requirements.txt
```

### 3. Install mGBA (Required but Tricky on Windows)

The `mgba` Python bindings are not available as pre-built wheels for Windows. You'll need to either:

**Option A**: Build from source (advanced)
- Follow instructions at: https://github.com/dvruette/pygba#installation

**Option B**: Wait for pre-built wheels (may not be available)

**Option C**: Use this wrapper as a template/learning resource while waiting for mgba support

## Usage

### Basic Example

```python
from wrapper import GBAWrapper, Button

with GBAWrapper("ROMs/Pokemon - Emerald Version (USA, Europe).gba") as gba:
	gba.set_speed(2.0)
	gba.input.press(Button.A)
	gba.screen.save_screenshot("screenshot.png")
```

### Running Examples

```bash
cd PyGBA
py -3.12 examples/basic_controls.py
```

## Common Tasks

### Press Buttons

```python
gba.input.press(Button.A)
gba.input.hold(Button.B, frames=30)
gba.input.tap(Button.START, times=3)
```

### Read Memory

```python
hp = gba.memory.read_u16(0x02000000)
name = gba.memory.read_string(0x02000010, 10)
```

### Capture Screen

```python
gba.screen.save_screenshot("frame.png")
pixel_color = gba.screen.get_pixel(120, 80)
```

### Save States

```python
gba.save_state.quick_save()
gba.input.tap(Button.A, times=10)
gba.save_state.quick_load()
```

### Speed Control

```python
gba.set_speed(2.0)
gba.turbo_mode()
gba.normal_speed()
```

## Project Structure

```
PyGBA/
├── wrapper/              # Core wrapper code
│   ├── gba_wrapper.py    # Main wrapper class
│   ├── input_helper.py   # Input controls
│   ├── memory_helper.py  # Memory reading
│   ├── screen_helper.py  # Screen capture
│   ├── save_state_helper.py  # Save states
│   └── types.py          # Type definitions
├── examples/             # Example scripts
├── ROMs/                 # Place your GBA ROMs here
├── README.md             # Full documentation
└── requirements.txt      # Python dependencies
```

## Tips

1. **Use context manager**: Always use `with GBAWrapper(...) as gba:` for automatic cleanup

2. **Type hints**: Your IDE will show you all available methods and parameters

3. **Frame timing**: GBA runs at 60 FPS, so 60 frames = 1 second

4. **Memory addresses**: Find them using Cheat Engine or game-specific documentation

5. **Speed up automation**: Use `gba.turbo_mode()` to run as fast as possible

## Next Steps

- Read the full [README.md](README.md) for complete API documentation
- Check out the examples in `examples/` directory
- Look up memory addresses for your specific game
- Join the pygba community for support

## Troubleshooting

**"No module named 'mgba'"**
- This is expected on Windows. The wrapper is designed and ready to use once mgba bindings become available.

**"ROM file not found"**
- Place your GBA ROM files in the `PyGBA/ROMs/` directory
- Make sure the path in your script is correct

**"PIL not available"**
- Install pillow: `py -3.12 -m pip install pillow`

**OCR not working**
- Install pytesseract: `py -3.12 -m pip install pytesseract`
- Install Tesseract OCR: https://github.com/UB-Mannheim/tesseract/wiki

## Happy Automating! 🎮


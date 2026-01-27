# Emulator Logic Improvements

## Overview
Requirements for enhancing the emulator control script parsing to support alphanumeric character mapping with ignored characters.

---

## Control Script Parsing Requirements

### Current State
- **Fibonacci script**: Reads Fibonacci numbers, maps to controls via modulo
- **Euler script**: Reads digit file, maps digits 0-9 to controls

### New Requirements

#### 1. Alphanumeric Character Mapping

**Goal**: Accept any character in `.txt` files. Map alphanumeric characters to controls, ignore others.

**Character Set**:
- `0-9` (digits): 10 characters
- `a-z` (lowercase): 26 characters  
- `A-Z` (uppercase): 26 characters
- **Total**: 62 mappable characters

**Mapping Strategy Options**:

##### Option A: Modulo Mapping (Simple)
```python
control_map = {
    0: 'a',
    1: 'b', 
    2: 'up',
    3: 'down',
    4: 'left',
    5: 'right',
    6: 'start',
    7: 'select'
}

def char_to_control(char):
    if not char.isalnum():
        return None  # Ignore non-alphanumeric
    
    # Convert to ordinal value
    if char.isdigit():
        value = int(char)  # 0-9
    elif char.islower():
        value = ord(char) - ord('a') + 10  # 10-35
    elif char.isupper():
        value = ord(char) - ord('A') + 36  # 36-61
    
    return control_map[value % len(control_map)]
```

##### Option B: Weighted Distribution
```python
# More strategic - vowels = A, consonants = other buttons
weighted_map = {
    'aeiouAEIOU': 'a',      # Vowels = A button (most common)
    'bcdfgBCDFG': 'b',      # Some consonants = B
    'hjklmHJKLM': 'up',
    'npqrsNPQRS': 'down',
    'tvwxzTVWXZ': 'left',
    '0123456789': 'right',
    'yY': 'start'
}
```

##### Option C: User-Defined Mapping
Allow users to upload a mapping file alongside their control script:

**mapping.json**:
```json
{
    "a": "a",
    "e": "a", 
    "i": "a",
    "b": "b",
    "0": "up",
    "1": "down",
    "default": "a"
}
```

**Recommendation**: Start with Option A (modulo), add Option C later for advanced users.

---

#### 2. Non-Alphanumeric Handling

**Ignored Characters**:
- Whitespace (spaces, tabs, newlines)
- Punctuation (`,`, `.`, `;`, etc.)
- Special characters (`@`, `#`, `%`, etc.)

**Behavior**:
```python
def parse_control_script(file_content):
    controls = []
    for char in file_content:
        if char.isalnum():
            control = char_to_control(char)
            controls.append(control)
        # else: silently skip
    return controls
```

**Use Case**: Users can paste formatted text, code, or natural language and it becomes a control sequence.

---

#### 3. Control Script Metadata

Add optional header to `.txt` files for configuration:

```txt
# ALGORITHM: custom
# MAPPING: modulo
# FRAME_RATE: 60
# BUTTON_PRESS_LENGTH: 30
---
The quick brown fox jumps over the lazy dog 123456789
```

**Parsing Logic**:
```python
def parse_script_with_metadata(file_content):
    lines = file_content.split('\n')
    metadata = {}
    script_start = 0
    
    for i, line in enumerate(lines):
        if line.startswith('#'):
            key, value = line[1:].split(':', 1)
            metadata[key.strip()] = value.strip()
        elif line.strip() == '---':
            script_start = i + 1
            break
    
    script = ''.join(lines[script_start:])
    return metadata, script
```

---

## Implementation Changes Needed

### 1. Refactor Control Reading

**Current** (`euler_plays_crystal.py:29-31`):
```python
with open("Algorithms/euler_digits.txt", "r") as file:
    euler_digits = file.read().strip()
    current_index = 0
```

**New**:
```python
from control_parser import parse_control_script

with open("control_script.txt", "r") as file:
    metadata, controls = parse_control_script(file.read())
    current_index = 0
```

### 2. Create `control_parser.py` Module

**New file**: `AlgorthmPlays/control_parser.py`

Functions needed:
- `parse_control_script(content: str) -> tuple[dict, list[str]]`
- `char_to_control(char: str, mapping: dict) -> str | None`
- `validate_control_script(content: str) -> tuple[bool, str]`

### 3. Update Emulator Main Loop

**Current** (`euler_plays_crystal.py:60-69`):
```python
euler_digit = int(euler_digits[current_index])
control_choice = euler_digit % 7
pyboy.button(weightedControlMap[control_choice], button_press_length)
```

**New**:
```python
control = controls[current_index]
if control:  # None if character was ignored
    pyboy.button(control, button_press_length)
```

---

## Testing Requirements

### Test Cases

#### Valid Inputs
- **Digits only**: `0123456789`
- **Letters only**: `abcdefghijklmnopqrstuvwxyz`
- **Mixed case**: `AaBbCcDd`
- **With punctuation**: `Hello, World! 123`
- **Code snippet**: `function main() { return 42; }`

#### Edge Cases
- **Empty file**: Should handle gracefully (no controls = idle emulator)
- **Only whitespace**: Same as empty
- **Only ignored chars**: `!!!@@@###`
- **Very large file**: 1MB+ text (memory concerns)
- **Unicode**: `こんにちは世界` (should ignore)

#### Expected Outputs
```python
# Input: "Hello123"
# Output controls: ['left', 'a', 'down', 'down', 'right', 'up', 'b', 'a']

# Input: "A!B@C#"
# Output controls: ['a', 'b', 'start']  # Punctuation ignored
```

---

## Configuration Options

### Emulator Settings

Allow per-script configuration:

```python
class ControlScriptConfig:
    frame_rate: int = 60              # Frames between inputs
    button_press_length: int = 30     # Frames to hold button
    mapping_type: str = 'modulo'      # 'modulo' | 'weighted' | 'custom'
    custom_mapping: dict | None = None
    loop: bool = True                 # Restart from beginning when end reached
    emulation_speed: int = 1          # 0=unlimited, 1=1x, 2=2x, etc.
```

---

## API Integration Points

### Upload Endpoint
```typescript
POST /api/control-scripts
Content-Type: multipart/form-data

{
  name: string
  file: File  // .txt file
  mapping?: File  // Optional mapping.json
  config?: {
    frameRate: number
    buttonPressLength: number
    mappingType: 'modulo' | 'weighted' | 'custom'
  }
}

Response: {
  id: string
  name: string
  characterCount: number
  controlCount: number  // After filtering non-alphanumeric
  preview: string[]  // First 10 controls
}
```

### Validation Endpoint
```typescript
POST /api/control-scripts/validate

{
  content: string
  config: ScriptConfig
}

Response: {
  valid: boolean
  errors: string[]
  stats: {
    totalChars: number
    mappedChars: number
    ignoredChars: number
    estimatedDuration: number  // seconds
  }
}
```

---

## Performance Considerations

### Memory Optimization

For large scripts (1MB+), don't load entire file into memory:

```python
class StreamingControlReader:
    def __init__(self, file_path: str):
        self.file = open(file_path, 'r')
        self.buffer = []
        self.buffer_size = 1000
    
    def next_control(self) -> str | None:
        if not self.buffer:
            self._fill_buffer()
        
        if self.buffer:
            return self.buffer.pop(0)
        return None
    
    def _fill_buffer(self):
        while len(self.buffer) < self.buffer_size:
            char = self.file.read(1)
            if not char:
                break
            if char.isalnum():
                self.buffer.append(char_to_control(char))
```

### Preprocessing

Pre-process and cache control sequences:

```python
# When script is uploaded, convert to binary control sequence
original: "Hello World 123"
processed: [0x04, 0x00, 0x03, 0x03, 0x05, 0x05, 0x06, 0x01, 0x00]

# Saves parsing time during playback
```

---

## Future Enhancements

### 1. Visual Script Editor
- Web UI to create control sequences visually
- Drag-and-drop button timeline
- Export to `.txt` format

### 2. Algorithm Generators
- Built-in algorithms: Fibonacci, Euler, Pi, etc.
- Generate control scripts programmatically
- Parameters: length, seed, mapping

### 3. Script Sharing
- Community library of control scripts
- Upvote/downvote interesting playthroughs
- Tags: "speedrun-attempt", "chaos", "artistic"

### 4. Live Editing
- Modify control script while emulator running
- Insert/delete controls
- Pause/resume at specific points

---

## Migration Path

### Phase 1: Core Functionality
- Implement alphanumeric parsing
- Add ignored character handling
- Basic modulo mapping

### Phase 2: Configuration
- Metadata header support
- Custom mappings
- Config validation

### Phase 3: Optimization
- Streaming reader for large files
- Preprocessing/caching
- Performance benchmarks

### Phase 4: Advanced Features
- Visual editor
- Algorithm generators
- Community sharing

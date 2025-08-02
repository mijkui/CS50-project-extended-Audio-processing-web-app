# Audio Processing Tools - CS50 Project

This project contains three audio processing programs for WAV files:

## 1. Volume Control (`volume.c`)

Modifies the volume of a WAV audio file by scaling each sample by a given factor.

### Usage
```bash
./volume input.wav output.wav factor
```

### Examples
```bash
# Double the volume
./volume input.wav output.wav 2.0

# Halve the volume
./volume input.wav output.wav 0.5
```

## 2. Frequency Changer (`frequency.c`)

Changes the frequency of an audio file by modifying the sample rate in the WAV header. This affects both pitch and playback speed.

### Usage
```bash
./frequency input.wav output.wav factor
```

### Examples
```bash
# Double frequency (higher pitch, faster playback)
./frequency input.wav output.wav 2.0

# Halve frequency (lower pitch, slower playback)
./frequency input.wav output.wav 0.5
```

## 3. Pitch Shifter (`pitch_shift.c`)

Changes the pitch of an audio file while preserving the original duration using time-stretching techniques.

### Usage
```bash
./pitch_shift input.wav output.wav factor
```

### Examples
```bash
# Double pitch (higher pitch, same duration)
./pitch_shift input.wav output.wav 2.0

# Halve pitch (lower pitch, same duration)
./pitch_shift input.wav output.wav 0.5
```

## How They Work

### Volume Control
- Reads the 44-byte WAV header and copies it unchanged
- Reads each 16-bit sample, multiplies by the factor, and writes to output
- Includes overflow protection to clamp values to valid range

### Frequency Changer
- Modifies the sample rate in the WAV header
- Keeps audio data unchanged
- Changes both pitch and playback speed
- Recalculates byte rate and file size

### Pitch Shifter
- Uses linear interpolation for resampling
- Processes each audio channel separately
- Changes pitch while preserving duration
- More computationally intensive but preserves timing

## Compilation

```bash
# Compile all programs
make all

# Or compile individually
make volume
make frequency
make pitch_shift
```

## Testing

### Create Test Files
```bash
python3 create_test_wav.py
```

### Analyze Results
```bash
python3 analyze_all.py          # Volume analysis
python3 analyze_frequency.py    # Frequency analysis
```

### Listen to Results
```bash
# On macOS
afplay input.wav
afplay output.wav
afplay output_high.wav
afplay output_pitch_high.wav
```

## File Structure

- `volume.c` - Volume control program
- `frequency.c` - Frequency changer program
- `pitch_shift.c` - Pitch shifter program
- `Makefile` - Compilation rules
- `create_test_wav.py` - Test WAV file generator
- `analyze_*.py` - Analysis scripts
- `README.md` - This documentation

## Technical Details

All programs:
- Support 16-bit PCM WAV files
- Handle mono and stereo audio
- Include proper error handling
- Preserve WAV file format integrity
- Use standard C libraries only

## CS50 Submission

For CS50 submission, use only the `volume.c` program:
```bash
check50 cs50/problems/2025/x/volume
submit50 cs50/problems/2025/x/volume
``` 
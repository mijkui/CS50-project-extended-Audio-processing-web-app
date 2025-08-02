# 🎵 Audio Processing Demo Guide

## Overview

This demo showcases three audio processing tools built for CS50:
1. **Volume Control** - Adjust audio volume
2. **Frequency Changer** - Modify pitch and playback speed
3. **Pitch Shifter** - Change pitch while preserving duration

## Quick Start

### 1. Start the Demo
```bash
./start_demo.sh
```

### 2. Open Your Browser
Go to: **http://localhost:5000**

### 3. Upload a WAV File
- Drag and drop a WAV file onto the upload area, or
- Click "Choose File" to browse and select a file

## Features

### 📊 File Analysis
After uploading, you'll see detailed information about your audio file:
- **Duration** - Length of the audio
- **Sample Rate** - Audio quality (Hz)
- **Channels** - Mono (1) or Stereo (2)
- **Max Amplitude** - Peak volume level
- **RMS Level** - Average volume level
- **File Size** - Size in kilobytes

### 🎛️ Audio Effects

#### 🔊 Volume Control
- **Range**: 0.1x to 5.0x
- **Effect**: Makes audio louder or quieter
- **Example**: 2.0x = twice as loud, 0.5x = half volume

#### 🎼 Frequency Changer
- **Range**: 0.5x to 3.0x
- **Effect**: Changes both pitch AND playback speed
- **Example**: 2.0x = higher pitch + faster playback

#### 🎤 Pitch Shifter
- **Range**: 0.5x to 3.0x
- **Effect**: Changes pitch while keeping same duration
- **Example**: 2.0x = higher pitch, same length

### 🎧 Results
After processing, you can:
- **Play** the processed audio directly in your browser
- **Download** the processed file to your computer
- **Compare** the before/after statistics

## How to Use

### Step 1: Upload
1. Click the upload area or drag a WAV file
2. Wait for file analysis to complete
3. Review the file statistics

### Step 2: Choose Effect
1. Select one of the three effect cards
2. Adjust the slider to your desired factor
3. Click the "Process" button

### Step 3: Listen & Download
1. Wait for processing to complete
2. Click "Play" to hear the result
3. Click "Download" to save the file

## Technical Details

### Supported Files
- **Format**: WAV only
- **Bit Depth**: 16-bit recommended
- **Channels**: Mono or Stereo
- **Sample Rate**: Any standard rate (44.1kHz, 48kHz, etc.)
- **Max Size**: 16MB

### Processing Time
- **Small files** (< 1MB): ~1-2 seconds
- **Medium files** (1-5MB): ~3-5 seconds
- **Large files** (5-16MB): ~5-10 seconds

## Troubleshooting

### Common Issues

**"File not found" error**
- Make sure you're uploading a WAV file
- Check that the file isn't corrupted

**"Processing failed" error**
- Try a smaller file
- Check that the file is a valid WAV format

**Audio won't play**
- Make sure your browser supports audio playback
- Check that your system volume is turned on

**Slow processing**
- Large files take longer to process
- Close other applications to free up memory

### Browser Compatibility
- **Chrome**: Full support ✅
- **Firefox**: Full support ✅
- **Safari**: Full support ✅
- **Edge**: Full support ✅

## Examples

### Test Files
You can create test files using the included Python script:
```bash
python3 create_test_wav.py
```

This creates `input.wav` - a 2-second 440Hz sine wave perfect for testing.

### Effect Examples

**Volume Control**
- 0.5x: Quiet background music
- 1.0x: Original volume
- 2.0x: Loud, attention-grabbing audio

**Frequency Changer**
- 0.5x: Slow, deep voice
- 1.0x: Original speed and pitch
- 2.0x: Fast, high-pitched voice

**Pitch Shifter**
- 0.5x: Deep voice, same duration
- 1.0x: Original pitch
- 2.0x: High-pitched voice, same duration

## Advanced Usage

### Command Line
You can also use the tools directly from the command line:

```bash
# Volume control
./volume input.wav output.wav 2.0

# Frequency change
./frequency input.wav output.wav 1.5

# Pitch shift
./pitch_shift input.wav output.wav 0.8
```

### Batch Processing
For multiple files, you can create scripts:

```bash
#!/bin/bash
for file in *.wav; do
    ./volume "$file" "loud_$file" 2.0
done
```

## File Management

### Uploads Directory
Processed files are stored in the `uploads/` directory:
- Files are automatically cleaned up when the server stops
- Each file gets a unique ID to prevent conflicts
- Original and processed files are kept separate

### File Naming
Processed files follow this pattern:
- `{id}_volume_{factor}.wav` - Volume processed files
- `{id}_frequency_{factor}.wav` - Frequency processed files
- `{id}_pitch_{factor}.wav` - Pitch processed files

## Performance Tips

1. **Use smaller files** for faster processing
2. **Close other applications** to free up memory
3. **Use mono files** instead of stereo for faster processing
4. **Lower sample rates** (22kHz) for quicker results

## Support

If you encounter issues:
1. Check the browser console for error messages
2. Verify your WAV file is valid
3. Try a different browser
4. Restart the web server

---

**Enjoy experimenting with audio processing! 🎵** 
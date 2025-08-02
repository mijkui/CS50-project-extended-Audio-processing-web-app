# 🎵 Audio Processing Project - CS50

A comprehensive audio processing toolkit featuring volume control, frequency modification, and pitch shifting with a modern web interface.

## 📁 Project Structure

```
volume/
├── src/                    # Source code
│   ├── volume/            # Volume control program
│   ├── frequency/         # Frequency changer program
│   └── pitch_shift/       # Pitch shifter program
├── build/                 # Compiled executables
├── web/                   # Web interface
│   ├── templates/         # HTML templates
│   ├── static/           # Static assets
│   └── uploads/          # Uploaded files
├── tools/                 # Utility scripts
├── tests/                 # Test files and audio samples
└── docs/                  # Documentation
```

## 🚀 Quick Start

### 1. Build the Project
```bash
make all
```

### 2. Install Dependencies
```bash
make install-deps
```

### 3. Create Test Files
```bash
make test-files
```

### 4. Start Web Interface
```bash
make web
```

Then open your browser to: **http://localhost:8080**

## 🎛️ Core Programs

### Volume Control
```bash
./build/volume input.wav output.wav 2.0
```
- Adjusts audio volume by scaling samples
- Range: 0.1x to 5.0x
- Preserves pitch and speed

### Frequency Changer
```bash
./build/frequency input.wav output.wav 2.0
```
- Changes frequency by modifying sample rate
- Range: 0.5x to 3.0x
- Affects both pitch and playback speed

### Pitch Shifter
```bash
./build/pitch_shift input.wav output.wav 2.0
```
- Changes pitch while preserving duration
- Range: 0.5x to 3.0x
- Uses time-stretching techniques

## 🌐 Web Interface

The web interface provides:
- **Drag & drop** file upload
- **Real-time** audio analysis
- **Interactive** effect controls
- **Live preview** of processed audio
- **Download** processed files

## 🛠️ Available Commands

```bash
make all          # Build all programs
make volume       # Build volume program only
make frequency    # Build frequency program only
make pitch_shift  # Build pitch shifter only
make web          # Start web interface
make test         # Run all tests
make analyze      # Analyze test results
make clean        # Clean build files
make help         # Show all commands
```

## 📚 Documentation

- [Demo Guide](docs/DEMO_GUIDE.md) - How to use the web interface
- [Project Summary](docs/PROJECT_SUMMARY.md) - Complete project overview
- [Original README](docs/README.md) - Detailed technical documentation

## 🧪 Testing

### Run Tests
```bash
make test
```

### Analyze Results
```bash
make analyze
```

### Create Test Files
```bash
make test-files
```

## 🎯 CS50 Submission

For CS50 submission, use only the volume program:
```bash
check50 cs50/problems/2025/x/volume
submit50 cs50/problems/2025/x/volume
```

## 🔧 Development

### Project Structure
- **Source Code**: `src/` - C programs organized by feature
- **Build Output**: `build/` - Compiled executables
- **Web Interface**: `web/` - Flask application and templates
- **Tools**: `tools/` - Python utility scripts
- **Tests**: `tests/` - Audio files and test data
- **Documentation**: `docs/` - Project documentation

### Adding New Features
1. Add source code to appropriate `src/` subdirectory
2. Update `Makefile` with new build targets
3. Add tests to `tests/` directory
4. Update documentation in `docs/`

## 📈 Performance

- **Small files** (< 1MB): ~1-2 seconds
- **Medium files** (1-5MB): ~3-5 seconds  
- **Large files** (5-16MB): ~5-10 seconds

## 🎵 Supported Formats

- **Input**: WAV files (16-bit recommended)
- **Output**: WAV files
- **Channels**: Mono or Stereo
- **Sample Rates**: Any standard rate

## 🤝 Contributing

1. Follow the existing directory structure
2. Add tests for new features
3. Update documentation
4. Use the provided Makefile targets

## 📄 License

This project is part of CS50 coursework.

---

**Status**: 🟢 **Complete and Ready for Demo** 🟢 
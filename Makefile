# Audio Processing Project - Main Makefile

# Directories
SRC_DIR = src
BUILD_DIR = build

# Programs
VOLUME_SRC = $(SRC_DIR)/volume/volume.c
FREQUENCY_SRC = $(SRC_DIR)/frequency/frequency.c
PITCH_SRC = $(SRC_DIR)/pitch_shift/pitch_shift.c

# Executables
VOLUME_BIN = $(BUILD_DIR)/volume
FREQUENCY_BIN = $(BUILD_DIR)/frequency
PITCH_BIN = $(BUILD_DIR)/pitch_shift

# Compiler flags
CC = clang
CFLAGS = -fsanitize=signed-integer-overflow -fsanitize=undefined -ggdb3 -O0 -std=c11 -Wall -Werror -Wextra -Wno-sign-compare -Wno-unused-parameter -Wno-unused-variable -Wshadow -lm

# Default target
all: build-dir volume frequency pitch_shift

# Create build directory
build-dir:
	@mkdir -p $(BUILD_DIR)

# Compile volume program
volume: $(VOLUME_SRC)
	$(CC) $(CFLAGS) $(VOLUME_SRC) -o $(VOLUME_BIN)

# Compile frequency program
frequency: $(FREQUENCY_SRC)
	$(CC) $(CFLAGS) $(FREQUENCY_SRC) -o $(FREQUENCY_BIN)

# Compile pitch_shift program
pitch_shift: $(PITCH_SRC)
	$(CC) $(CFLAGS) $(PITCH_SRC) -o $(PITCH_BIN)

# Web interface
web: build-dir volume frequency pitch_shift
	@echo "🌐 Starting web interface..."
	@cd web && python3 web_ui.py

# Clean build files
clean:
	@echo "🧹 Cleaning build files..."
	@rm -rf $(BUILD_DIR)

.PHONY: all build-dir volume frequency pitch_shift web clean

# Create test files
test-files:
	@echo "🎵 Creating test audio files..."
	@cd tools && python3 create_test_wav.py
	@cd tools && python3 convert_system_sounds.py

# Install Python dependencies
install-deps:
	@echo "📦 Installing Python dependencies..."
	@cd web && pip3 install -r requirements.txt

# Help
help:
	@echo "🎵 Available commands:"
	@echo "  make all          - Build all programs"
	@echo "  make web          - Start web interface"
	@echo "  make test-files   - Create test files"
	@echo "  make install-deps - Install dependencies"
	@echo "  make clean        - Clean build files"

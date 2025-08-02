#!/usr/bin/env python3
import wave
import struct
import math

# Create a simple sine wave WAV file
def create_test_wav(filename, duration=1.0, frequency=440.0, sample_rate=44100):
    # Open WAV file for writing
    with wave.open(filename, 'w') as wav_file:
        # Set parameters
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 16-bit samples
        wav_file.setframerate(sample_rate)
        
        # Generate sine wave samples
        num_samples = int(duration * sample_rate)
        for i in range(num_samples):
            # Generate sine wave
            sample = math.sin(2 * math.pi * frequency * i / sample_rate)
            # Convert to 16-bit integer
            sample_int = int(sample * 32767)
            # Pack as little-endian 16-bit integer
            wav_file.writeframes(struct.pack('<h', sample_int))

if __name__ == "__main__":
    create_test_wav("../tests/input.wav", duration=2.0, frequency=440.0)
    print("Created ../tests/input.wav - a 2-second 440Hz sine wave") 
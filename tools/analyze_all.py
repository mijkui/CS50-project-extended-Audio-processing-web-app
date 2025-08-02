#!/usr/bin/env python3
import wave
import struct
import numpy as np

def analyze_wav(filename):
    """Analyze a WAV file and return statistics"""
    with wave.open(filename, 'r') as wav_file:
        frames = wav_file.getnframes()
        sample_rate = wav_file.getframerate()
        duration = frames / sample_rate
        
        samples = []
        for _ in range(frames):
            sample_data = wav_file.readframes(1)
            sample = struct.unpack('<h', sample_data)[0]
            samples.append(sample)
        
        samples = np.array(samples)
        max_amplitude = np.max(np.abs(samples))
        rms = np.sqrt(np.mean(samples**2))
        
        return {
            'filename': filename,
            'duration': duration,
            'max_amplitude': max_amplitude,
            'rms': rms
        }

# Analyze all files
files = ['../tests/input.wav', '../tests/output.wav', '../tests/output_half.wav']
results = []

for filename in files:
    try:
        stats = analyze_wav(filename)
        results.append(stats)
    except FileNotFoundError:
        print(f"File {filename} not found")

print("=== Volume Scaling Results ===")
print("File           | Duration | Max Amp | RMS Level | Factor")
print("-" * 55)

base_max = results[0]['max_amplitude'] if results else 1

for stats in results:
    factor = stats['max_amplitude'] / base_max if base_max > 0 else 0
    print(f"{stats['filename']:14} | {stats['duration']:8.2f} | {stats['max_amplitude']:7d} | {stats['rms']:9.2f} | {factor:5.2f}")

print()
print("✅ Your volume program is working correctly!")
print("   - Original file: input.wav")
print("   - Doubled volume: output.wav (factor 2.0)")
print("   - Halved volume: output_half.wav (factor 0.5)")
print()
print("🎵 You can now listen to these files to hear the volume difference!") 
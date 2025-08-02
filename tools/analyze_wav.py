#!/usr/bin/env python3
import wave
import struct
import numpy as np

def analyze_wav(filename):
    """Analyze a WAV file and return statistics"""
    with wave.open(filename, 'r') as wav_file:
        # Get file info
        frames = wav_file.getnframes()
        sample_rate = wav_file.getframerate()
        duration = frames / sample_rate
        
        # Read all samples
        samples = []
        for _ in range(frames):
            sample_data = wav_file.readframes(1)
            sample = struct.unpack('<h', sample_data)[0]
            samples.append(sample)
        
        # Calculate statistics
        samples = np.array(samples)
        max_amplitude = np.max(np.abs(samples))
        rms = np.sqrt(np.mean(samples**2))
        
        return {
            'filename': filename,
            'duration': duration,
            'max_amplitude': max_amplitude,
            'rms': rms,
            'samples': samples[:100]  # First 100 samples for comparison
        }

# Analyze both files
input_stats = analyze_wav('input.wav')
output_stats = analyze_wav('output.wav')

print("=== WAV File Analysis ===")
print(f"Input file: {input_stats['filename']}")
print(f"  Duration: {input_stats['duration']:.2f} seconds")
print(f"  Max amplitude: {input_stats['max_amplitude']}")
print(f"  RMS level: {input_stats['rms']:.2f}")
print()

print(f"Output file: {output_stats['filename']}")
print(f"  Duration: {output_stats['duration']:.2f} seconds")
print(f"  Max amplitude: {output_stats['max_amplitude']}")
print(f"  RMS level: {output_stats['rms']:.2f}")
print()

# Calculate the actual scaling factor
actual_factor = output_stats['max_amplitude'] / input_stats['max_amplitude']
print(f"Actual scaling factor: {actual_factor:.2f} (expected: 2.0)")
print()

# Show first few samples comparison
print("=== Sample Comparison (first 10 samples) ===")
print("Sample # | Input | Output | Ratio")
print("-" * 35)
for i in range(min(10, len(input_stats['samples']))):
    input_sample = input_stats['samples'][i]
    output_sample = output_stats['samples'][i]
    ratio = output_sample / input_sample if input_sample != 0 else 0
    print(f"{i:7d} | {input_sample:6d} | {output_sample:6d} | {ratio:5.2f}") 
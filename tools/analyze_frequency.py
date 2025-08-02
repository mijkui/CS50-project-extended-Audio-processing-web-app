#!/usr/bin/env python3
import wave
import struct
import numpy as np
import os

def analyze_wav(filename):
    """Analyze a WAV file and return detailed statistics"""
    if not os.path.exists(filename):
        return None
        
    with wave.open(filename, 'r') as wav_file:
        # Get file info
        frames = wav_file.getnframes()
        sample_rate = wav_file.getframerate()
        duration = frames / sample_rate
        channels = wav_file.getnchannels()
        sample_width = wav_file.getsampwidth()
        
        # Read all samples
        samples = []
        for _ in range(frames):
            sample_data = wav_file.readframes(1)
            if sample_width == 2:  # 16-bit
                sample = struct.unpack('<h', sample_data)[0]
            else:  # 8-bit
                sample = struct.unpack('<B', sample_data)[0] - 128
            samples.append(sample)
        
        # Calculate statistics
        samples = np.array(samples)
        max_amplitude = np.max(np.abs(samples))
        rms = np.sqrt(np.mean(samples**2))
        
        # Calculate frequency spectrum (simple approach)
        if len(samples) > 0:
            # Take first 1024 samples for FFT
            fft_samples = samples[:min(1024, len(samples))]
            fft_result = np.fft.fft(fft_samples)
            fft_magnitude = np.abs(fft_result)
            # Find dominant frequency
            dominant_freq_idx = np.argmax(fft_magnitude[1:len(fft_magnitude)//2]) + 1
            dominant_freq = dominant_freq_idx * sample_rate / len(fft_samples)
        else:
            dominant_freq = 0
        
        return {
            'filename': filename,
            'duration': duration,
            'sample_rate': sample_rate,
            'channels': channels,
            'max_amplitude': max_amplitude,
            'rms': rms,
            'dominant_freq': dominant_freq
        }

# Analyze all files
files_to_analyze = [
    '../tests/input.wav',
    '../tests/output_high.wav', 
    '../tests/output_low.wav',
    '../tests/output_pitch_high.wav',
    '../tests/output_pitch_low.wav'
]

print("=== Audio Frequency Analysis ===")
print("File                | Duration | Sample Rate | Max Amp | Dominant Freq")
print("-" * 65)

results = []
for filename in files_to_analyze:
    stats = analyze_wav(filename)
    if stats:
        results.append(stats)
        print(f"{filename:18} | {stats['duration']:8.2f} | {stats['sample_rate']:11d} | {stats['max_amplitude']:7d} | {stats['dominant_freq']:12.1f} Hz")

print()
print("=== Summary ===")
if len(results) >= 2:
    base = results[0]
    print(f"Original file: {base['filename']}")
    print(f"  - Sample rate: {base['sample_rate']} Hz")
    print(f"  - Dominant frequency: {base['dominant_freq']:.1f} Hz")
    print()
    
    for result in results[1:]:
        if 'high' in result['filename']:
            freq_ratio = result['sample_rate'] / base['sample_rate']
            print(f"{result['filename']}: Sample rate changed by factor {freq_ratio:.2f}")
        elif 'low' in result['filename']:
            freq_ratio = result['sample_rate'] / base['sample_rate']
            print(f"{result['filename']}: Sample rate changed by factor {freq_ratio:.2f}")

print()
print("🎵 You can now listen to compare the different effects:")
print("   - input.wav: Original 440Hz tone")
print("   - output_high.wav: Higher frequency (faster playback)")
print("   - output_low.wav: Lower frequency (slower playback)")
print("   - output_pitch_high.wav: Higher pitch (same duration)")
print("   - output_pitch_low.wav: Lower pitch (same duration)") 
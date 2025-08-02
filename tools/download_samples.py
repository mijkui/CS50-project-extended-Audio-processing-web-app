#!/usr/bin/env python3
import urllib.request
import os

def download_file(url, filename):
    """Download a file from URL"""
    try:
        print(f"Downloading {filename}...")
        urllib.request.urlretrieve(url, filename)
        print(f"✅ Downloaded {filename}")
        return True
    except Exception as e:
        print(f"❌ Failed to download {filename}: {e}")
        return False

def create_sample_wav():
    """Create a simple WAV file using Python"""
    import wave
    import struct
    import math
    
    # Create a 3-second audio file with multiple frequencies
    sample_rate = 44100
    duration = 3.0
    num_samples = int(duration * sample_rate)
    
    with wave.open('sample_music.wav', 'w') as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 16-bit
        wav_file.setframerate(sample_rate)
        
        for i in range(num_samples):
            # Create a melody with different frequencies
            t = i / sample_rate
            if t < 1.0:
                freq = 440  # A4
            elif t < 2.0:
                freq = 523  # C5
            else:
                freq = 659  # E5
            
            sample = math.sin(2 * math.pi * freq * t)
            sample_int = int(sample * 16383)  # Half amplitude
            wav_file.writeframes(struct.pack('<h', sample_int))
    
    print("✅ Created sample_music.wav (3-second melody)")

def main():
    print("🎵 Downloading Sample WAV Files for Testing")
    print("=" * 50)
    
    # Create a simple test file
    create_sample_wav()
    
    # Try to download some sample files (these URLs might not work, but worth trying)
    samples = [
        {
            'url': 'https://www.soundjay.com/misc/sounds/bell-ringing-05.wav',
            'filename': 'bell.wav'
        },
        {
            'url': 'https://www.soundjay.com/misc/sounds/phone-ring-1.wav', 
            'filename': 'phone.wav'
        }
    ]
    
    print("\n📥 Attempting to download sample files...")
    for sample in samples:
        download_file(sample['url'], sample['filename'])
    
    print("\n🎧 Available WAV files for testing:")
    wav_files = [f for f in os.listdir('.') if f.endswith('.wav')]
    for file in wav_files:
        size = os.path.getsize(file) / 1024  # KB
        print(f"   • {file} ({size:.1f} KB)")
    
    print("\n💡 Tips:")
    print("   • Use sample_music.wav for testing effects")
    print("   • Convert your MP3 files to WAV using:")
    print("     afconvert -f WAVE -d LEI16 input.mp3 output.wav")
    print("   • Or use online converters like convertio.co")

if __name__ == "__main__":
    main() 
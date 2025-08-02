#!/usr/bin/env python3
import os
import subprocess

def convert_aiff_to_wav(aiff_file, wav_file):
    """Convert AIFF file to WAV using afconvert"""
    try:
        cmd = ['afconvert', '-f', 'WAVE', '-d', 'LEI16', aiff_file, wav_file]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Converted {aiff_file} to {wav_file}")
            return True
        else:
            print(f"❌ Failed to convert {aiff_file}: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error converting {aiff_file}: {e}")
        return False

def main():
    print("🎵 Converting macOS System Sounds to WAV")
    print("=" * 45)
    
    system_sounds_dir = "/System/Library/Sounds"
    if not os.path.exists(system_sounds_dir):
        print("❌ System sounds directory not found")
        return
    
    # Get list of AIFF files
    aiff_files = [f for f in os.listdir(system_sounds_dir) if f.endswith('.aiff')]
    
    if not aiff_files:
        print("❌ No AIFF files found in system sounds")
        return
    
    print(f"Found {len(aiff_files)} system sound files")
    print("\nConverting to WAV format...")
    
    converted_count = 0
    for aiff_file in aiff_files[:5]:  # Convert first 5 files
        aiff_path = os.path.join(system_sounds_dir, aiff_file)
        wav_file = os.path.join("../tests", aiff_file.replace('.aiff', '.wav'))
        
        if convert_aiff_to_wav(aiff_path, wav_file):
            converted_count += 1
    
    print(f"\n✅ Successfully converted {converted_count} files")
    
    # List all WAV files now available
    print("\n🎧 Available WAV files for testing:")
    tests_dir = "../tests"
    wav_files = [f for f in os.listdir(tests_dir) if f.endswith('.wav')]
    for file in sorted(wav_files):
        file_path = os.path.join(tests_dir, file)
        size = os.path.getsize(file_path) / 1024  # KB
        print(f"   • {file} ({size:.1f} KB)")
    
    print("\n💡 Ready to test in the web UI!")
    print("   Upload any of these WAV files to see the effects")

if __name__ == "__main__":
    main() 
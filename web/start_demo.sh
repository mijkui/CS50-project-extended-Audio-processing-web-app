#!/bin/bash

echo "🎵 Starting Audio Processing Demo UI..."
echo ""

# Check if all required files exist
if [ ! -f "../build/volume" ]; then
    echo "❌ Error: volume executable not found. Run 'make volume' first."
    exit 1
fi

if [ ! -f "../build/frequency" ]; then
    echo "❌ Error: frequency executable not found. Run 'make frequency' first."
    exit 1
fi

if [ ! -f "../build/pitch_shift" ]; then
    echo "❌ Error: pitch_shift executable not found. Run 'make pitch_shift' first."
    exit 1
fi

if [ ! -f "web_ui.py" ]; then
    echo "❌ Error: web_ui.py not found."
    exit 1
fi

echo "✅ All required files found!"
echo ""
echo "🌐 Starting web server..."
echo "📱 Open your browser and go to: http://localhost:8080"
echo ""
echo "🎧 Features:"
echo "   • Upload WAV files via drag & drop"
echo "   • Real-time audio analysis"
echo "   • Volume control (0.1x - 5.0x)"
echo "   • Frequency changer (0.5x - 3.0x)"
echo "   • Pitch shifter (0.5x - 3.0x)"
echo "   • Play processed audio in browser"
echo "   • Download processed files"
echo ""
echo "⏹️  Press Ctrl+C to stop the server"
echo ""

# Start the web server
python3 web_ui.py 
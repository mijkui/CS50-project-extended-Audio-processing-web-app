#!/usr/bin/env python3
from flask import Flask, render_template, request, send_file, jsonify
import os
import subprocess
import tempfile
import uuid
from werkzeug.utils import secure_filename
import wave
import struct
import numpy as np

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create uploads directory if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Allowed file extensions
ALLOWED_EXTENSIONS = {'wav'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def analyze_wav_file(filepath):
    """Analyze a WAV file and return statistics"""
    try:
        with wave.open(filepath, 'r') as wav_file:
            frames = wav_file.getnframes()
            sample_rate = wav_file.getframerate()
            duration = frames / sample_rate
            channels = wav_file.getnchannels()
            sample_width = wav_file.getsampwidth()
            
            # Read samples for analysis
            samples = []
            for _ in range(min(frames, 10000)):  # Limit for performance
                sample_data = wav_file.readframes(1)
                if sample_width == 2:  # 16-bit
                    sample = struct.unpack('<h', sample_data)[0]
                else:  # 8-bit
                    sample = struct.unpack('<B', sample_data)[0] - 128
                samples.append(sample)
            
            samples = np.array(samples)
            max_amplitude = np.max(np.abs(samples))
            rms = np.sqrt(np.mean(samples**2))
            
            return {
                'duration': round(duration, 2),
                'sample_rate': sample_rate,
                'channels': channels,
                'max_amplitude': int(max_amplitude),
                'rms': round(rms, 2),
                'file_size': os.path.getsize(filepath)
            }
    except Exception as e:
        return {'error': str(e)}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'Only WAV files are allowed'}), 400
    
    # Generate unique filename
    filename = secure_filename(file.filename)
    unique_id = str(uuid.uuid4())
    input_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{unique_id}_{filename}")
    
    # Save uploaded file
    file.save(input_path)
    
    # Analyze the file
    analysis = analyze_wav_file(input_path)
    
    return jsonify({
        'success': True,
        'file_id': unique_id,
        'filename': filename,
        'analysis': analysis
    })

@app.route('/process', methods=['POST'])
def process_audio():
    data = request.get_json()
    file_id = data.get('file_id')
    effect_type = data.get('effect_type')  # 'volume', 'frequency', 'pitch'
    factor = float(data.get('factor', 1.0))
    
    # Find the input file
    input_files = [f for f in os.listdir(app.config['UPLOAD_FOLDER']) if f.startswith(file_id)]
    if not input_files:
        return jsonify({'error': 'File not found'}), 404
    
    input_path = os.path.join(app.config['UPLOAD_FOLDER'], input_files[0])
    output_filename = f"{file_id}_{effect_type}_{factor}.wav"
    output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
    
    try:
        # Run the appropriate processing command
        if effect_type == 'volume':
            cmd = ['../build/volume', input_path, output_path, str(factor)]
        elif effect_type == 'frequency':
            cmd = ['../build/frequency', input_path, output_path, str(factor)]
        elif effect_type == 'pitch':
            cmd = ['../build/pitch_shift', input_path, output_path, str(factor)]
        else:
            return jsonify({'error': 'Invalid effect type'}), 400
        
        # Execute the command
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        if result.returncode != 0:
            return jsonify({'error': f'Processing failed: {result.stderr}'}), 500
        
        # Analyze the output file
        output_analysis = analyze_wav_file(output_path)
        
        return jsonify({
            'success': True,
            'output_file': output_filename,
            'analysis': output_analysis,
            'command_output': result.stdout
        })
        
    except subprocess.TimeoutExpired:
        return jsonify({'error': 'Processing timed out'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download/<filename>')
def download_file(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    return jsonify({'error': 'File not found'}), 404

@app.route('/play/<filename>')
def play_file(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(file_path):
        return send_file(file_path, mimetype='audio/wav')
    return jsonify({'error': 'File not found'}), 404

if __name__ == '__main__':
    print("Starting Audio Processing Demo UI...")
    print("Open your browser and go to: http://localhost:8080")
    app.run(debug=True, host='0.0.0.0', port=8080) 
from pydantic_settings import BaseSettings
from flask import Flask, request, jsonify
from flask_cors import CORS  # Add this import for CORS support
from moviepy.editor import AudioFileClip
import assemblyai as aai
import os

# Environment setup
gkey = "AIzaSyC2w_s0gzTC5bNkDeiOnloUdKf7RAIIlbM"
aikey = "687063c7417345c4b8de68a676b60714"

aai.settings.api_key = aikey
transcriber = aai.Transcriber()

# The description function
def aud_desc(video_path):
    audioclip = AudioFileClip(video_path)
    duration = audioclip.duration
    segment_length = 300
    transcriptions = []

    for start in range(0, int(duration), segment_length):
        end = min(start + segment_length, duration)
        segment = audioclip.subclip(start, end)
        output_file = f"audio_{start}_{end}.mp3"
        segment.write_audiofile(output_file)
        transcript = transcriber.transcribe(output_file)
        transcriptions.append(transcript.text)
        os.remove(output_file)

    full_transcript = " ".join(transcriptions)
    return full_transcript

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/')
def home():
    return 'Hello World'

@app.route('/upload', methods=['POST'])
def upload_video():
    if 'video' not in request.files:
        return jsonify({'error': 'No video file provided'}), 400

    video = request.files['video']
    video_path = os.path.join('uploads', video.filename)
    video.save(video_path)

    try:
        summary = aud_desc(video_path)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        os.remove(video_path)

    return jsonify({'summary': summary}), 200

if __name__ == '__main__':
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    app.run(debug=True, port=5000, threaded=True)

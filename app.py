from flask import Flask, request, jsonify, send_file, render_template_string
from flask_cors import CORS  # Import CORS from flask_cors
import os
from moviepy.editor import VideoFileClip

app = Flask(__name__)
CORS(app)  # Apply CORS to your Flask app

# Define global variables
vp = ""
ap = ""

def aud_desc(video_path):
    try:
        video = VideoFileClip(video_path)
        audio = video.audio
        audio_path = os.path.join('uploads', 'extracted_audio.mp3')
        audio.write_audiofile(audio_path, codec='mp3')
        video.reader.close()
        video.audio.reader.close_proc()
        return audio_path
    except Exception as e:
        return str(e)



@app.route('/', methods=['POST'])
def upload_video():
    global vp, ap
    if 'video' not in request.files:
        return jsonify({'error': 'No video file provided'}), 400
    
    video = request.files['video']
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    video_path = os.path.join('uploads', video.filename)
    video.save(video_path)
    
    try:
        audio_path = aud_desc(video_path)
        vp = video_path
        ap = audio_path
        return send_file(audio_path, as_attachment=True)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/delete', methods=['POST'])
def delete():
    global vp, ap
    try:
        if os.path.exists(vp):
            os.remove(vp)
        if os.path.exists(ap):
            os.remove(ap)
        vp, ap = "", ""
        return jsonify({'message': 'Files deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

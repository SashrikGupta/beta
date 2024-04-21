from flask import Flask, request, jsonify
import gdown
from moviepy.editor import VideoFileClip
import assemblyai as aai
import os

app = Flask(__name__)


# Set up AssemblyAI API key
aai.settings.api_key = "87063c7417345c4b8de68a676b60714"

@app.route('/transcribe', methods=['POST'])
def transcribe_video():
    # Get URL from request
    url = request.json.get('url')
    
    # Download the video file
    file_id = url.split('/')[-2]
    prefix = 'https://drive.google.com/uc?/export=download&id='
    gdown.download(prefix + file_id, 'video.mp4')

    # Extract audio from the video
    video_clip = VideoFileClip('video.mp4')
    audio_clip = video_clip.audio
    audio_clip.write_audiofile('audio.mp3')

    # Close the clips
    video_clip.close()
    audio_clip.close()

    # Transcribe audio using AssemblyAI
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe("audio.mp3")
    transcript_text = transcript.text
    
    # Delete the downloaded files
    os.remove('audio.mp3')
    os.remove('video.mp4')

    return jsonify({'transcript': transcript_text})

if __name__ == '__main__':
    app.run(debug=True)

import os
import uuid
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
from moviepy.editor import VideoFileClip
from PIL import Image
import io
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
Config.init_app(app)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def generate_thumbnail(video_path, thumbnail_path):
    try:
        clip = VideoFileClip(video_path)
        frame = clip.get_frame(1)  # Get frame at 1 second
        im = Image.fromarray(frame)
        im.save(thumbnail_path)
        clip.close()
        return True
    except Exception as e:
        print(f"Error generating thumbnail: {e}")
        return False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        uploaded_files = request.files.getlist('videos')
        
        if len(uploaded_files) > app.config['MAX_UPLOADS_AT_ONCE']:
            return "You can upload maximum 15 videos at a time", 400
            
        video_links = []
        
        for file in uploaded_files:
            if file and allowed_file(file.filename):
                # Generate unique filename
                unique_id = str(uuid.uuid4())
                filename = secure_filename(file.filename)
                ext = filename.rsplit('.', 1)[1].lower()
                new_filename = f"{unique_id}.{ext}"
                
                # Save video
                video_path = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)
                file.save(video_path)
                
                # Generate thumbnail
                thumbnail_filename = f"{unique_id}.jpg"
                thumbnail_path = os.path.join(app.config['THUMBNAIL_FOLDER'], thumbnail_filename)
                generate_thumbnail(video_path, thumbnail_path)
                
                # Store video info
                video_links.append({
                    'original_name': filename,
                    'video_url': url_for('view_video', video_id=unique_id, _external=True),
                    'thumbnail_url': url_for('get_thumbnail', filename=thumbnail_filename, _external=True)
                })
        
        return render_template('upload.html', video_links=video_links)
    
    return render_template('upload.html')

@app.route('/video/<video_id>')
def view_video(video_id):
    # Find the video file
    for filename in os.listdir(app.config['UPLOAD_FOLDER']):
        if filename.startswith(video_id):
            video_url = url_for('get_video', filename=filename)
            thumbnail_filename = f"{video_id}.jpg"
            thumbnail_url = url_for('get_thumbnail', filename=thumbnail_filename)
            return render_template('video.html', video_url=video_url, thumbnail_url=thumbnail_url)
    
    return "Video not found", 404

@app.route('/uploads/videos/<filename>')
def get_video(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/uploads/thumbnails/<filename>')
def get_thumbnail(filename):
    return send_from_directory(app.config['THUMBNAIL_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = 'your-secret-key-here'
    UPLOAD_FOLDER = os.path.join(basedir, 'uploads', 'videos')
    THUMBNAIL_FOLDER = os.path.join(basedir, 'uploads', 'thumbnails')
    ALLOWED_EXTENSIONS = {'mp4', 'mov', 'avi', 'mkv', 'webm'}
    MAX_CONTENT_LENGTH = 2 * 1024 * 1024 * 1024  # 2GB max upload
    MAX_UPLOADS_AT_ONCE = 15
    
    @staticmethod
    def init_app(app):
        # Create upload directories if they don't exist
        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
        os.makedirs(Config.THUMBNAIL_FOLDER, exist_ok=True)
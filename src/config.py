import os


BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'cambiar_por_una_clave_muy_segura'
    SESSION_TYPE = 'filesystem'
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')

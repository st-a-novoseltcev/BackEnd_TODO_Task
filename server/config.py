import os
from datetime import timedelta


class Config:
    SECRET_KEY = os.urandom(20).hex()
    USE_PERMANENT_SESSION = True
    PERMANENT_SESSION_LIFETIME = timedelta(days=5)
    task_title_len = 25
    category_name_len = 15
    filename_len = 228
    files_dir_len = 0
    UPLOAD_FOLDER = os.path.join('data', 'files')
    ROOT = 'server'
import os
import uuid
from werkzeug.utils import secure_filename
from flask import current_app
import hashlib
from datetime import datetime

# 支持的音频文件格式
ALLOWED_AUDIO_EXTENSIONS = {'mp3', 'wav', 'm4a', 'flac', 'aac', 'ogg'}

# 支持的图片文件格式
ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

# 文件大小限制 (字节)
MAX_AUDIO_SIZE = 50 * 1024 * 1024  # 50MB
MAX_IMAGE_SIZE = 5 * 1024 * 1024   # 5MB

def allowed_file(filename, file_type='audio'):
    """检查文件扩展名是否被允许"""
    if not filename or '.' not in filename:
        return False
    
    extension = filename.rsplit('.', 1)[1].lower()
    
    if file_type == 'audio':
        return extension in ALLOWED_AUDIO_EXTENSIONS
    elif file_type == 'image':
        return extension in ALLOWED_IMAGE_EXTENSIONS
    
    return False

def get_file_size_mb(file_size_bytes):
    """将文件大小转换为MB"""
    return round(file_size_bytes / (1024 * 1024), 2)

def validate_file_size(file_size, file_type='audio'):
    """验证文件大小"""
    if file_type == 'audio':
        return file_size <= MAX_AUDIO_SIZE
    elif file_type == 'image':
        return file_size <= MAX_IMAGE_SIZE
    
    return False

def generate_unique_filename(original_filename):
    """生成唯一的文件名"""
    if '.' in original_filename:
        name, ext = original_filename.rsplit('.', 1)
        ext = ext.lower()
    else:
        name = original_filename
        ext = ''
    
    # 使用UUID和时间戳确保唯一性
    unique_id = str(uuid.uuid4())
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    if ext:
        return f"{timestamp}_{unique_id}.{ext}"
    else:
        return f"{timestamp}_{unique_id}"

def save_audio_file(file, practice_record_id):
    """保存音频文件"""
    if not file or not allowed_file(file.filename, 'audio'):
        raise ValueError("不支持的音频文件格式")
    
    # 检查文件大小
    file.seek(0, 2)  # 移动到文件末尾
    file_size = file.tell()
    file.seek(0)  # 重置到文件开头
    
    if not validate_file_size(file_size, 'audio'):
        raise ValueError(f"音频文件过大，最大支持{MAX_AUDIO_SIZE//1024//1024}MB")
    
    # 生成文件名
    filename = generate_unique_filename(file.filename)
    
    # 创建文件夹路径
    upload_folder = current_app.config['UPLOAD_FOLDER']
    audio_folder = os.path.join(upload_folder, 'audio')
    
    if not os.path.exists(audio_folder):
        os.makedirs(audio_folder)
    
    # 保存文件
    file_path = os.path.join(audio_folder, filename)
    file.save(file_path)
    
    return os.path.join('audio', filename)

def save_avatar_file(file, user_id):
    """保存头像文件"""
    if not file or not allowed_file(file.filename, 'image'):
        raise ValueError("不支持的图片文件格式")
    
    # 检查文件大小
    file.seek(0, 2)  # 移动到文件末尾
    file_size = file.tell()
    file.seek(0)  # 重置到文件开头
    
    if not validate_file_size(file_size, 'image'):
        raise ValueError(f"图片文件过大，最大支持{MAX_IMAGE_SIZE//1024//1024}MB")
    
    # 生成文件名
    filename = generate_unique_filename(file.filename)
    
    # 创建文件夹路径
    upload_folder = current_app.config['UPLOAD_FOLDER']
    avatar_folder = os.path.join(upload_folder, 'avatars')
    
    if not os.path.exists(avatar_folder):
        os.makedirs(avatar_folder)
    
    # 保存文件
    file_path = os.path.join(avatar_folder, filename)
    file.save(file_path)
    
    return os.path.join('avatars', filename)

def delete_file(file_path):
    """删除文件"""
    try:
        if file_path and os.path.exists(file_path):
            os.remove(file_path)
            return True
    except Exception as e:
        print(f"删除文件失败: {e}")
    
    return False

def get_file_hash(file_path):
    """计算文件的MD5哈希值"""
    hash_md5 = hashlib.md5()
    try:
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    except Exception as e:
        print(f"计算文件哈希失败: {e}")
        return None

def ensure_upload_directory():
    """确保上传目录存在"""
    upload_folder = current_app.config.get('UPLOAD_FOLDER', 'uploads')
    
    directories = [
        upload_folder,
        os.path.join(upload_folder, 'audio'),
        os.path.join(upload_folder, 'avatars'),
        os.path.join(upload_folder, 'temp')
    ]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
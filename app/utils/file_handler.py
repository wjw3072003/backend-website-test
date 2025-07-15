import os
import uuid
from datetime import datetime
from flask import current_app
from werkzeug.utils import secure_filename

def allowed_file(filename):
    """检查文件扩展名是否被允许"""
    if not filename:
        return False
    
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

def generate_unique_filename(original_filename):
    """生成唯一的文件名"""
    if not original_filename:
        return None
    
    # 获取文件扩展名
    extension = ''
    if '.' in original_filename:
        extension = '.' + original_filename.rsplit('.', 1)[1].lower()
    
    # 生成唯一文件名
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    unique_id = str(uuid.uuid4())[:8]
    
    return f"{timestamp}_{unique_id}{extension}"

def save_audio_file(file, practice_record_id):
    """保存音频文件"""
    if not file or not allowed_file(file.filename):
        raise ValueError("不支持的文件格式")
    
    # 生成唯一文件名
    filename = generate_unique_filename(file.filename)
    
    # 创建按日期分类的子目录
    date_dir = datetime.now().strftime('%Y/%m/%d')
    upload_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], 'audio', date_dir)
    
    # 确保目录存在
    os.makedirs(upload_dir, exist_ok=True)
    
    # 保存文件
    file_path = os.path.join(upload_dir, filename)
    file.save(file_path)
    
    # 返回相对路径用于数据库存储
    relative_path = os.path.join('audio', date_dir, filename)
    return relative_path

def save_score_file(file, practice_id):
    """保存乐谱文件"""
    if not file:
        raise ValueError("文件不能为空")
    
    # 生成唯一文件名
    filename = generate_unique_filename(file.filename)
    
    # 创建乐谱文件目录
    upload_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], 'scores')
    os.makedirs(upload_dir, exist_ok=True)
    
    # 保存文件
    file_path = os.path.join(upload_dir, filename)
    file.save(file_path)
    
    # 返回相对路径
    relative_path = os.path.join('scores', filename)
    return relative_path

def get_file_info(file_path):
    """获取文件信息"""
    if not os.path.exists(file_path):
        return None
    
    stat = os.stat(file_path)
    
    return {
        'size': stat.st_size,
        'created_at': datetime.fromtimestamp(stat.st_ctime),
        'modified_at': datetime.fromtimestamp(stat.st_mtime),
        'extension': os.path.splitext(file_path)[1].lower()
    }

def delete_file(file_path):
    """删除文件"""
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
    except Exception as e:
        print(f"删除文件失败: {e}")
    return False

def get_audio_duration(file_path):
    """获取音频文件时长（秒）"""
    # 这里应该使用音频处理库如librosa或mutagen
    # 目前返回模拟值
    try:
        # 简单的文件大小估算（实际应用中应使用专业音频库）
        file_size = os.path.getsize(file_path)
        # 假设平均比特率为128kbps
        estimated_duration = file_size / (128 * 1024 / 8)  # 秒
        return round(estimated_duration, 2)
    except:
        return None

def validate_audio_file(file_path):
    """验证音频文件完整性"""
    if not os.path.exists(file_path):
        return False, "文件不存在"
    
    # 检查文件大小
    file_size = os.path.getsize(file_path)
    if file_size == 0:
        return False, "文件为空"
    
    # 检查文件头（简单验证）
    try:
        with open(file_path, 'rb') as f:
            header = f.read(4)
            
            # 检查常见音频格式的文件头
            if header.startswith(b'ID3') or header.startswith(b'\xff\xfb'):
                return True, "MP3文件"
            elif header.startswith(b'RIFF'):
                return True, "WAV文件"
            elif header.startswith(b'fLaC'):
                return True, "FLAC文件"
            elif header.startswith(b'OggS'):
                return True, "OGG文件"
            else:
                return False, "未知音频格式"
                
    except Exception as e:
        return False, f"文件读取错误: {e}"

def compress_audio(input_path, output_path, quality='medium'):
    """压缩音频文件（占位符函数）"""
    # 这里应该使用FFmpeg或其他音频处理工具
    # 目前只是复制文件
    try:
        import shutil
        shutil.copy2(input_path, output_path)
        return True, "压缩完成"
    except Exception as e:
        return False, f"压缩失败: {e}"
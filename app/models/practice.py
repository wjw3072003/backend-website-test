from datetime import datetime
from app import db

class Practice(db.Model):
    """练习曲目模型"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    composer = db.Column(db.String(100))
    difficulty_level = db.Column(db.Integer, default=1)  # 1-10难度等级
    genre = db.Column(db.String(50))  # 音乐类型
    description = db.Column(db.Text)
    
    # 标准音频文件
    standard_audio_path = db.Column(db.String(500))
    standard_score_path = db.Column(db.String(500))  # 标准乐谱路径
    
    # 状态
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    practice_records = db.relationship('PracticeRecord', backref='practice', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'title': self.title,
            'composer': self.composer,
            'difficulty_level': self.difficulty_level,
            'genre': self.genre,
            'description': self.description,
            'standard_audio_path': self.standard_audio_path,
            'standard_score_path': self.standard_score_path,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<Practice {self.title}>'

class PracticeRecord(db.Model):
    """练习记录模型"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    practice_id = db.Column(db.Integer, db.ForeignKey('practice.id'), nullable=False)
    
    # 练习信息
    duration = db.Column(db.Integer)  # 练习时长（秒）
    score = db.Column(db.Float)  # AI评分 (0-100)
    
    # AI分析结果
    tempo_accuracy = db.Column(db.Float)  # 节拍准确度
    pitch_accuracy = db.Column(db.Float)  # 音准度
    rhythm_accuracy = db.Column(db.Float)  # 节奏准确度
    
    # 反馈信息
    ai_feedback = db.Column(db.Text)  # AI反馈文本
    improvement_suggestions = db.Column(db.Text)  # 改进建议
    
    # 状态
    status = db.Column(db.String(20), default='completed')  # completed, analyzing, failed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 关系
    audio_files = db.relationship('AudioFile', backref='practice_record', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'practice_id': self.practice_id,
            'practice_title': self.practice.title if self.practice else None,
            'duration': self.duration,
            'score': self.score,
            'tempo_accuracy': self.tempo_accuracy,
            'pitch_accuracy': self.pitch_accuracy,
            'rhythm_accuracy': self.rhythm_accuracy,
            'ai_feedback': self.ai_feedback,
            'improvement_suggestions': self.improvement_suggestions,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'audio_files': [audio.to_dict() for audio in self.audio_files]
        }
    
    def __repr__(self):
        return f'<PracticeRecord {self.id}>'

class AudioFile(db.Model):
    """音频文件模型"""
    id = db.Column(db.Integer, primary_key=True)
    practice_record_id = db.Column(db.Integer, db.ForeignKey('practice_record.id'), nullable=False)
    
    # 文件信息
    filename = db.Column(db.String(200), nullable=False)
    original_filename = db.Column(db.String(200), nullable=False)
    file_path = db.Column(db.String(500), nullable=False)
    file_size = db.Column(db.Integer)  # 文件大小（字节）
    file_type = db.Column(db.String(20))  # 文件类型
    duration = db.Column(db.Float)  # 音频时长（秒）
    
    # 状态
    upload_status = db.Column(db.String(20), default='uploaded')  # uploaded, processing, processed, failed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'practice_record_id': self.practice_record_id,
            'filename': self.filename,
            'original_filename': self.original_filename,
            'file_path': self.file_path,
            'file_size': self.file_size,
            'file_type': self.file_type,
            'duration': self.duration,
            'upload_status': self.upload_status,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<AudioFile {self.filename}>'
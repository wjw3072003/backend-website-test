from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from app import db

# 学生班级关联表
student_classes = db.Table('student_classes',
    db.Column('student_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('class_id', db.Integer, db.ForeignKey('class.id'), primary_key=True),
    db.Column('enrolled_at', db.DateTime, default=datetime.utcnow)
)

# 老师班级关联表
teacher_classes = db.Table('teacher_classes',
    db.Column('teacher_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('class_id', db.Integer, db.ForeignKey('class.id'), primary_key=True),
    db.Column('assigned_at', db.DateTime, default=datetime.utcnow)
)

class Class(db.Model):
    """班级模型"""
    __tablename__ = 'class'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    code = db.Column(db.String(20), unique=True, nullable=False)
    grade_level = db.Column(db.String(50))
    subject = db.Column(db.String(50))
    
    # 状态
    is_active = db.Column(db.Boolean, default=True)
    
    # 时间戳
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    students = db.relationship('User', secondary=student_classes, lazy='subquery',
                             backref=db.backref('classes', lazy=True))
    teachers = db.relationship('User', secondary=teacher_classes, lazy='subquery',
                             backref=db.backref('teaching_classes', lazy=True))
    
    def __repr__(self):
        return f'<Class {self.name}>'

class Assignment(db.Model):
    """作业模型"""
    __tablename__ = 'assignment'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    instructions = db.Column(db.Text)
    
    # 关联
    class_id = db.Column(db.Integer, db.ForeignKey('class.id'), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # 类型和难度
    assignment_type = db.Column(db.String(50), default='practice')
    difficulty_level = db.Column(db.Integer, default=1)
    max_score = db.Column(db.Integer, default=100)
    
    # 时间设置
    start_date = db.Column(db.DateTime, default=datetime.utcnow)
    due_date = db.Column(db.DateTime)
    
    # 状态
    is_active = db.Column(db.Boolean, default=True)
    is_published = db.Column(db.Boolean, default=False)
    
    # 时间戳
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    teacher = db.relationship('User', backref='assignments')
    
    def __repr__(self):
        return f'<Assignment {self.title}>'
    
    @property
    def is_overdue(self):
        """检查是否过期"""
        if self.due_date:
            return datetime.utcnow() > self.due_date
        return False

class Grade(db.Model):
    """成绩模型"""
    __tablename__ = 'grade'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # 关联
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    assignment_id = db.Column(db.Integer, db.ForeignKey('assignment.id'), nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey('class.id'), nullable=False)
    graded_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    # 成绩信息
    score = db.Column(db.Float)
    max_score = db.Column(db.Integer, default=100)
    percentage = db.Column(db.Float)
    letter_grade = db.Column(db.String(5))
    
    # 评价
    feedback = db.Column(db.Text)
    comments = db.Column(db.Text)
    
    # 状态
    status = db.Column(db.String(20), default='pending')
    
    # 时间戳
    submitted_at = db.Column(db.DateTime)
    graded_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    student = db.relationship('User', foreign_keys=[student_id], backref='grades_received')
    grader = db.relationship('User', foreign_keys=[graded_by], backref='grades_given')
    
    def __repr__(self):
        return f'<Grade {self.score}>'

class TeachingResource(db.Model):
    """教学资源模型"""
    __tablename__ = 'teaching_resource'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    content = db.Column(db.Text)
    
    # 文件信息
    file_path = db.Column(db.String(500))
    file_name = db.Column(db.String(200))
    file_size = db.Column(db.Integer)
    file_type = db.Column(db.String(50))
    
    # 分类
    category = db.Column(db.String(50))
    tags = db.Column(db.String(500))
    subject = db.Column(db.String(50))
    grade_level = db.Column(db.String(50))
    
    # 权限
    is_public = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    
    # 关联
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # 统计
    download_count = db.Column(db.Integer, default=0)
    view_count = db.Column(db.Integer, default=0)
    
    # 时间戳
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    creator = db.relationship('User', backref='teaching_resources')
    
    def __repr__(self):
        return f'<TeachingResource {self.title}>'

class Announcement(db.Model):
    """公告模型"""
    __tablename__ = 'announcement'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    
    # 关联
    class_id = db.Column(db.Integer, db.ForeignKey('class.id'), nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # 类型和优先级
    announcement_type = db.Column(db.String(50), default='general')
    priority = db.Column(db.String(20), default='normal')
    
    # 状态
    is_published = db.Column(db.Boolean, default=True)
    is_pinned = db.Column(db.Boolean, default=False)
    
    # 时间设置
    publish_at = db.Column(db.DateTime, default=datetime.utcnow)
    expire_at = db.Column(db.DateTime)
    
    # 时间戳
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    creator = db.relationship('User', backref='announcements')
    
    def __repr__(self):
        return f'<Announcement {self.title}>'

class Attendance(db.Model):
    """考勤模型"""
    __tablename__ = 'attendance'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # 关联
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey('class.id'), nullable=False)
    recorded_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    # 考勤信息
    attendance_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), nullable=False)
    check_in_time = db.Column(db.DateTime)
    check_out_time = db.Column(db.DateTime)
    
    # 备注
    notes = db.Column(db.Text)
    reason = db.Column(db.String(200))
    
    # 时间戳
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 关系
    student = db.relationship('User', foreign_keys=[student_id], backref='attendances')
    recorder = db.relationship('User', foreign_keys=[recorded_by], backref='recorded_attendances')
    
    def __repr__(self):
        return f'<Attendance {self.status}>' 
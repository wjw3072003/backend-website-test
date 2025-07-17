from datetime import datetime, timedelta
from app import db
import uuid

class PasswordResetToken(db.Model):
    """密码重置令牌模型"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    token = db.Column(db.String(100), unique=True, nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)
    used = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 关系
    user = db.relationship('User', backref='reset_tokens')
    
    def __init__(self, user_id, **kwargs):
        super(PasswordResetToken, self).__init__(**kwargs)
        self.user_id = user_id
        self.token = str(uuid.uuid4())
        # 令牌1小时后过期
        self.expires_at = datetime.utcnow() + timedelta(hours=1)
    
    def is_valid(self):
        """检查令牌是否有效"""
        return not self.used and datetime.utcnow() < self.expires_at
    
    def mark_as_used(self):
        """标记令牌为已使用"""
        self.used = True
        db.session.commit()
    
    @staticmethod
    def create_token(user):
        """为用户创建重置令牌"""
        # 先删除用户现有的未使用令牌
        PasswordResetToken.query.filter_by(
            user_id=user.id, 
            used=False
        ).delete()
        
        # 创建新令牌
        token = PasswordResetToken(user_id=user.id)
        db.session.add(token)
        db.session.commit()
        return token
    
    @staticmethod
    def verify_token(token_string):
        """验证令牌"""
        token = PasswordResetToken.query.filter_by(token=token_string).first()
        if token and token.is_valid():
            return token
        return None
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'token': self.token,
            'expires_at': self.expires_at.isoformat() if self.expires_at else None,
            'used': self.used,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<PasswordResetToken {self.token[:8]}...>'

class ContactMessage(db.Model):
    """联系消息模型"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    
    # 状态
    status = db.Column(db.String(20), default='unread')  # unread, read, replied
    admin_reply = db.Column(db.Text)
    
    # 时间戳
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    replied_at = db.Column(db.DateTime)
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'subject': self.subject,
            'message': self.message,
            'status': self.status,
            'admin_reply': self.admin_reply,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'replied_at': self.replied_at.isoformat() if self.replied_at else None
        }
    
    def __repr__(self):
        return f'<ContactMessage {self.subject}>' 
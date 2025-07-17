import os
from app import create_app, db
from app.models import User, Role, Practice, PracticeRecord, AudioFile, PasswordResetToken, ContactMessage

# 创建应用实例
app = create_app(os.environ.get('FLASK_ENV', 'development'))

@app.shell_context_processor
def make_shell_context():
    """为Flask shell提供上下文"""
    return {
        'db': db,
        'User': User,
        'Role': Role,
        'Practice': Practice,
        'PracticeRecord': PracticeRecord,
        'AudioFile': AudioFile,
        'PasswordResetToken': PasswordResetToken,
        'ContactMessage': ContactMessage
    }

@app.cli.command()
def init_db():
    """初始化数据库"""
    print("创建数据库表...")
    db.create_all()
    
    # 创建基本角色
    print("创建基本角色...")
    roles = [
        {'name': 'admin', 'description': '系统管理员'},
        {'name': 'teacher', 'description': '教师'},
        {'name': 'student', 'description': '学生'}
    ]
    
    for role_data in roles:
        role = Role.query.filter_by(name=role_data['name']).first()
        if not role:
            role = Role(name=role_data['name'], description=role_data['description'])
            db.session.add(role)
    
    db.session.commit()
    print("基本角色创建完成")
    
    # 创建管理员账户
    admin_email = 'admin@aimuspal.com'
    admin = User.query.filter_by(email=admin_email).first()
    if not admin:
        print("创建管理员账户...")
        admin = User(
            email=admin_email,
            username='admin',
            password='admin123',
            first_name='系统',
            last_name='管理员',
            is_verified=True
        )
        
        admin_role = Role.query.filter_by(name='admin').first()
        if admin_role:
            admin.add_role(admin_role)
        
        db.session.add(admin)
        db.session.commit()
        print(f"管理员账户创建完成：{admin_email} / admin123")
    else:
        print("管理员账户已存在")

@app.cli.command()
def create_sample_data():
    """创建示例数据"""
    print("创建示例练习曲目...")
    
    sample_practices = [
        {
            'title': '小星星变奏曲',
            'composer': '莫扎特',
            'difficulty_level': 3,
            'genre': '古典',
            'description': '经典的初学者练习曲目，适合掌握基本指法和节奏。'
        },
        {
            'title': '月光奏鸣曲第一乐章',
            'composer': '贝多芬',
            'difficulty_level': 7,
            'genre': '古典',
            'description': '贝多芬著名的钢琴奏鸣曲，情感深沉，技巧要求较高。'
        },
        {
            'title': '天空之城',
            'composer': '久石让',
            'difficulty_level': 5,
            'genre': '流行',
            'description': '宫崎骏动画电影《天空之城》主题曲，旋律优美动听。'
        },
        {
            'title': '卡农',
            'composer': '帕赫贝尔',
            'difficulty_level': 6,
            'genre': '古典',
            'description': '巴洛克时期的经典作品，和声进行优美，广受喜爱。'
        },
        {
            'title': '致爱丽丝',
            'composer': '贝多芬',
            'difficulty_level': 4,
            'genre': '古典',
            'description': '贝多芬的小品，旋律简洁优美，适合中级学习者。'
        }
    ]
    
    for practice_data in sample_practices:
        practice = Practice.query.filter_by(title=practice_data['title']).first()
        if not practice:
            practice = Practice(**practice_data)
            db.session.add(practice)
    
    db.session.commit()
    print("示例练习曲目创建完成")

@app.cli.command()
def reset_db():
    """重置数据库"""
    print("警告：这将删除所有数据！")
    confirm = input("确认重置数据库吗？(y/N): ")
    if confirm.lower() == 'y':
        db.drop_all()
        print("数据库已重置")
        # 重新初始化
        init_db()
        create_sample_data()
    else:
        print("操作已取消")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
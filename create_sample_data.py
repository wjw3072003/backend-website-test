#!/usr/bin/env python3

"""
创建示例数据脚本
用于为AiMusPal应用创建测试数据
"""

import os
from app import create_app, db
from app.models.user import User, Role
from app.models.practice import Practice, PracticeRecord
from datetime import datetime
import random

def create_sample_data():
    """创建示例数据"""
    app = create_app()
    
    with app.app_context():
        # 创建数据库表
        db.create_all()
        
        print("开始创建示例数据...")
        
        # 1. 创建角色
        print("创建角色...")
        roles_data = [
            {'name': 'admin', 'description': '系统管理员'},
            {'name': 'teacher', 'description': '教师'},
            {'name': 'student', 'description': '学生'}
        ]
        
        for role_data in roles_data:
            role = Role.query.filter_by(name=role_data['name']).first()
            if not role:
                role = Role(name=role_data['name'], description=role_data['description'])
                db.session.add(role)
                print(f"  创建角色: {role_data['name']}")
        
        db.session.commit()
        
        # 2. 创建用户
        print("创建用户...")
        users_data = [
            {
                'email': 'admin@aimuspal.com',
                'username': 'admin',
                'password': 'admin123',
                'first_name': '系统',
                'last_name': '管理员',
                'role': 'admin',
                'is_verified': True
            },
            {
                'email': 'teacher@aimuspal.com', 
                'username': 'teacher',
                'password': 'teacher123',
                'first_name': '张',
                'last_name': '老师',
                'role': 'teacher',
                'is_verified': True
            },
            {
                'email': 'student@aimuspal.com',
                'username': 'student',
                'password': 'student123', 
                'first_name': '李',
                'last_name': '同学',
                'role': 'student',
                'is_verified': True
            },
            {
                'email': 'student2@aimuspal.com',
                'username': 'student2',
                'password': 'student123',
                'first_name': '王',
                'last_name': '同学',
                'role': 'student',
                'is_verified': True
            }
        ]
        
        for user_data in users_data:
            user = User.query.filter_by(email=user_data['email']).first()
            if not user:
                user = User(
                    email=user_data['email'],
                    username=user_data['username'],
                    password=user_data['password'],
                    first_name=user_data['first_name'],
                    last_name=user_data['last_name'],
                    is_verified=user_data['is_verified']
                )
                
                # 分配角色
                role = Role.query.filter_by(name=user_data['role']).first()
                if role:
                    user.roles.append(role)
                
                db.session.add(user)
                print(f"  创建用户: {user_data['username']} ({user_data['role']})")
        
        db.session.commit()
        
        # 3. 创建练习曲目
        print("创建练习曲目...")
        practices_data = [
            {
                'title': '小星星',
                'composer': '法国民谣',
                'difficulty_level': 1,
                'genre': '儿歌',
                'description': '最经典的入门练习曲目，适合初学者练习基本的音符和节拍。旋律简单易记，是培养音感的绝佳选择。'
            },
            {
                'title': '欢乐颂',
                'composer': '贝多芬',
                'difficulty_level': 3,
                'genre': '古典音乐',
                'description': '贝多芬第九交响曲中的著名旋律，优美动听，适合有一定基础的学习者练习。可以很好地锻炼音准和表现力。'
            },
            {
                'title': '卡农',
                'composer': '帕赫贝尔',
                'difficulty_level': 5,
                'genre': '古典音乐',
                'description': '巴洛克时期的经典作品，旋律层次丰富，需要较好的技巧和音乐理解力。是提高音乐表现力的优秀练习曲目。'
            },
            {
                'title': '茉莉花',
                'composer': '中国民歌',
                'difficulty_level': 2,
                'genre': '民族音乐',
                'description': '中国经典民歌，旋律优美，具有浓郁的民族特色。适合练习中国风格的音乐表达和韵味。'
            },
            {
                'title': '生日快乐歌',
                'composer': '传统歌曲',
                'difficulty_level': 1,
                'genre': '流行音乐',
                'description': '世界各地都熟悉的生日歌，简单易学，是练习基本音准和节奏的理想选择。'
            },
            {
                'title': '月光奏鸣曲第一乐章',
                'composer': '贝多芬',
                'difficulty_level': 7,
                'genre': '古典音乐',
                'description': '贝多芬著名的钢琴奏鸣曲，情感深邃，技巧性较强。适合有较高水平的学习者挑战。'
            },
            {
                'title': '青花瓷',
                'composer': '周杰伦',
                'difficulty_level': 4,
                'genre': '流行音乐',
                'description': '现代流行音乐经典，融合了中国风元素，旋律优美，适合练习现代音乐的表达技巧。'
            },
            {
                'title': '天空之城',
                'composer': '久石让',
                'difficulty_level': 6,
                'genre': '动漫音乐',
                'description': '宫崎骏动画电影主题曲，旋律空灵优美，富有想象力，需要较好的音乐感知力和表现力。'
            }
        ]
        
        for practice_data in practices_data:
            practice = Practice.query.filter_by(title=practice_data['title']).first()
            if not practice:
                practice = Practice(
                    title=practice_data['title'],
                    composer=practice_data['composer'],
                    difficulty_level=practice_data['difficulty_level'],
                    genre=practice_data['genre'],
                    description=practice_data['description'],
                    is_active=True
                )
                db.session.add(practice)
                print(f"  创建练习曲目: {practice_data['title']} (难度{practice_data['difficulty_level']})")
        
        db.session.commit()
        
        # 4. 创建示例练习记录
        print("创建示例练习记录...")
        students = User.query.join(User.roles).filter(Role.name == 'student').all()
        practices = Practice.query.all()
        
        for student in students:
            # 为每个学生创建一些练习记录
            for i in range(random.randint(3, 8)):
                practice = random.choice(practices)
                
                # 根据练习难度和学生水平生成模拟分数
                base_score = max(40, 95 - practice.difficulty_level * 8)
                score = base_score + random.uniform(-15, 15)
                score = max(30, min(100, score))  # 限制在30-100之间
                
                # 生成各项指标
                tempo_accuracy = score + random.uniform(-10, 10)
                pitch_accuracy = score + random.uniform(-10, 10)
                rhythm_accuracy = score + random.uniform(-10, 10)
                
                # 限制在0-100之间
                tempo_accuracy = max(0, min(100, tempo_accuracy))
                pitch_accuracy = max(0, min(100, pitch_accuracy))
                rhythm_accuracy = max(0, min(100, rhythm_accuracy))
                
                # 生成反馈
                if score >= 85:
                    feedback = "优秀的表现！音准、节拍和节奏都很准确，继续保持这种水平。"
                elif score >= 70:
                    feedback = "良好的表现！还有一些地方可以改进，特别注意音准和节拍的稳定性。"
                elif score >= 60:
                    feedback = "及格的表现，但还需要更多练习。建议多听标准音频，加强基本功训练。"
                else:
                    feedback = "需要更多练习。建议从简单曲目开始，逐步提高音准和节拍的准确性。"
                
                record = PracticeRecord(
                    user_id=student.id,
                    practice_id=practice.id,
                    score=score,
                    tempo_accuracy=tempo_accuracy,
                    pitch_accuracy=pitch_accuracy,
                    rhythm_accuracy=rhythm_accuracy,
                    feedback=feedback,
                    duration=random.randint(60, 300),  # 1-5分钟
                    status='completed'
                )
                db.session.add(record)
        
        db.session.commit()
        print(f"  为{len(students)}个学生创建了练习记录")
        
        print("\n✅ 示例数据创建完成！")
        print("\n登录信息:")
        print("管理员: admin@aimuspal.com / admin123")
        print("教师:   teacher@aimuspal.com / teacher123") 
        print("学生:   student@aimuspal.com / student123")
        print("学生2:  student2@aimuspal.com / student123")
        print("\n🚀 可以开始测试应用程序了！")

if __name__ == '__main__':
    create_sample_data()
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
创建老师端数据表的迁移脚本
"""

import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from app import create_app, db
from app.models.teacher_simple import (
    Class, Assignment, Grade, TeachingResource, 
    Announcement, Attendance
)

def create_teacher_tables():
    """创建老师端相关数据表"""
    app = create_app()
    
    with app.app_context():
        print("🏗️ 开始创建老师端数据表...")
        
        try:
            # 创建所有表
            db.create_all()
            print("✅ 数据表创建成功!")
            
            # 验证表是否创建成功
            tables_created = []
            inspector = db.inspect(db.engine)
            existing_tables = inspector.get_table_names()
            
            expected_tables = [
                'class', 'assignment', 'grade', 'teaching_resource',
                'announcement', 'attendance', 'student_classes', 'teacher_classes'
            ]
            
            for table in expected_tables:
                if table in existing_tables:
                    tables_created.append(table)
                    print(f"  ✅ {table} 表已创建")
                else:
                    print(f"  ❌ {table} 表创建失败")
            
            print(f"\n📊 创建结果:")
            print(f"  预期表数: {len(expected_tables)}")
            print(f"  实际创建: {len(tables_created)}")
            print(f"  成功率: {len(tables_created)/len(expected_tables)*100:.1f}%")
            
            if len(tables_created) == len(expected_tables):
                print("\n🎉 所有老师端数据表创建成功!")
                return True
            else:
                print("\n⚠️ 部分表创建失败，请检查数据库连接和权限")
                return False
                
        except Exception as e:
            print(f"❌ 创建数据表时出错: {e}")
            db.session.rollback()
            return False

def create_sample_data():
    """创建示例数据"""
    app = create_app()
    
    with app.app_context():
        print("\n📝 创建示例数据...")
        
        try:
            # 获取老师用户
            from app.models.user import User
            teacher = User.query.filter_by(email='teacher@aimuspal.com').first()
            if not teacher:
                print("❌ 未找到老师用户，跳过示例数据创建")
                return False
            
            # 创建示例班级
            sample_class = Class(
                name="音乐基础班",
                description="适合初学者的音乐基础课程",
                code="MUS-101",
                grade_level="初级",
                subject="音乐"
            )
            
            # 添加老师到班级
            sample_class.teachers.append(teacher)
            
            db.session.add(sample_class)
            db.session.commit()
            
            # 创建示例作业
            sample_assignment = Assignment(
                title="音阶练习",
                description="练习C大调音阶",
                instructions="请录制一段C大调音阶演奏，要求节拍准确，音准标准",
                class_id=sample_class.id,
                teacher_id=teacher.id,
                assignment_type="practice",
                difficulty_level=3,
                max_score=100
            )
            
            db.session.add(sample_assignment)
            
            # 创建示例公告
            sample_announcement = Announcement(
                title="课程开始通知",
                content="音乐基础班正式开课，请同学们准时参加。",
                class_id=sample_class.id,
                created_by=teacher.id,
                announcement_type="general",
                priority="normal"
            )
            
            db.session.add(sample_announcement)
            
            # 创建示例教学资源
            sample_resource = TeachingResource(
                title="C大调音阶教学视频",
                description="详细讲解C大调音阶的指法和技巧",
                category="视频",
                tags="音阶,C大调,基础",
                subject="音乐",
                grade_level="初级",
                created_by=teacher.id,
                is_public=True
            )
            
            db.session.add(sample_resource)
            db.session.commit()
            
            print("✅ 示例数据创建成功!")
            print(f"  - 班级: {sample_class.name}")
            print(f"  - 作业: {sample_assignment.title}")
            print(f"  - 公告: {sample_announcement.title}")
            print(f"  - 资源: {sample_resource.title}")
            
            return True
            
        except Exception as e:
            print(f"❌ 创建示例数据时出错: {e}")
            db.session.rollback()
            return False

if __name__ == '__main__':
    print("🚀 开始老师端数据库初始化...")
    
    # 创建数据表
    tables_success = create_teacher_tables()
    
    if tables_success:
        # 创建示例数据
        sample_success = create_sample_data()
        
        if sample_success:
            print("\n🎉 老师端数据库初始化完成!")
        else:
            print("\n⚠️ 数据表创建成功，但示例数据创建失败")
    else:
        print("\n❌ 数据表创建失败，停止初始化") 
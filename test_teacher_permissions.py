#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试老师权限修复的脚本
"""

import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from app import create_app, db
from app.models.user import User, Role, TeacherInviteCode

def test_teacher_permissions():
    """测试老师权限修复"""
    app = create_app()
    
    with app.app_context():
        print("🔍 测试老师权限修复...")
        
        # 检查老师账户
        teacher = User.query.filter_by(email='teacher@aimuspal.com').first()
        if not teacher:
            print("❌ 未找到老师账户")
            return False
        
        print(f"✅ 找到老师账户: {teacher.username}")
        
        # 检查老师角色
        has_teacher_role = teacher.has_role('teacher')
        has_admin_role = teacher.has_role('admin')
        
        print(f"👨‍🏫 老师角色: {'✅' if has_teacher_role else '❌'}")
        print(f"👑 管理员角色: {'✅' if has_admin_role else '❌'}")
        
        # 检查推广码
        invite = TeacherInviteCode.query.filter_by(teacher_id=teacher.id).first()
        if invite:
            print(f"✅ 推广码存在: {invite.code}")
        else:
            print("❌ 未找到推广码")
        
        # 检查学生关联
        students = User.query.join(User.roles).filter(
            User.teacher_id == teacher.id,
            Role.name == 'student'
        ).all()
        
        print(f"👥 关联学生数量: {len(students)}")
        for student in students:
            print(f"  - {student.username} ({student.email})")
        
        # 权限建议
        print("\n📋 权限修复建议:")
        if has_admin_role:
            print("⚠️  老师账户同时拥有管理员角色，建议移除管理员权限")
            print("   老师应该只能访问老师专用功能，不能访问用户管理")
        else:
            print("✅ 老师权限设置正确")
        
        if not invite:
            print("⚠️  老师没有推广码，需要生成推广码")
        else:
            print("✅ 推广码功能正常")
        
        return True

def generate_teacher_invite_code():
    """为老师生成推广码"""
    app = create_app()
    
    with app.app_context():
        print("\n🔧 为老师生成推广码...")
        
        teacher = User.query.filter_by(email='teacher@aimuspal.com').first()
        if not teacher:
            print("❌ 未找到老师账户")
            return False
        
        # 检查是否已有推广码
        existing_invite = TeacherInviteCode.query.filter_by(teacher_id=teacher.id).first()
        if existing_invite:
            print(f"✅ 推广码已存在: {existing_invite.code}")
            return True
        
        # 生成推广码
        import random
        import string
        
        def generate_invite_code(length=8):
            chars = string.ascii_uppercase + string.digits
            return ''.join(random.choices(chars, k=length))
        
        code = generate_invite_code()
        while TeacherInviteCode.query.filter_by(code=code).first():
            code = generate_invite_code()
        
        invite = TeacherInviteCode(teacher_id=teacher.id, code=code)
        db.session.add(invite)
        db.session.commit()
        
        print(f"✅ 推广码生成成功: {code}")
        return True

if __name__ == '__main__':
    print("🚀 开始测试老师权限修复...")
    
    # 测试权限
    test_teacher_permissions()
    
    # 生成推广码
    generate_teacher_invite_code()
    
    print("\n✅ 测试完成！") 
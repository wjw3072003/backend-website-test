#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from app import create_app, db
from app.models.user import User, Role

def check_teacher_accounts():
    """检查数据库中的老师账号"""
    app = create_app()
    
    with app.app_context():
        print("🔍 检查数据库中的用户和角色...")
        
        # 检查角色表
        roles = Role.query.all()
        print(f"\n📋 系统角色 ({len(roles)} 个):")
        for role in roles:
            print(f"  - {role.name}: {role.description}")
        
        # 检查用户表
        users = User.query.all()
        print(f"\n👥 系统用户 ({len(users)} 个):")
        for user in users:
            user_roles = [role.name for role in user.roles]
            status = "激活" if user.is_active else "禁用"
            print(f"  - {user.email} ({user.username}) - 角色: {', '.join(user_roles) if user_roles else '无'} - 状态: {status}")
        
        # 检查是否有老师角色
        teacher_role = Role.query.filter_by(name='teacher').first()
        if teacher_role:
            print(f"\n👨‍🏫 老师角色存在: {teacher_role.description}")
            teachers = User.query.join(User.roles).filter(Role.name == 'teacher').all()
            print(f"老师账号数量: {len(teachers)}")
            for teacher in teachers:
                print(f"  - {teacher.email} ({teacher.username})")
        else:
            print("\n⚠️ 未找到老师角色")
        
        # 检查是否有管理员
        admin_users = User.query.join(User.roles).filter(Role.name == 'admin').all()
        print(f"\n👑 管理员账号数量: {len(admin_users)}")
        for admin in admin_users:
            print(f"  - {admin.email} ({admin.username})")

if __name__ == '__main__':
    check_teacher_accounts() 
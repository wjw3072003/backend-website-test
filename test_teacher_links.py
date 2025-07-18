#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试老师页面链接的脚本
"""

import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from app import create_app

def test_teacher_links():
    """测试老师页面的所有链接"""
    app = create_app()
    
    with app.app_context():
        print("🔗 测试老师页面链接...")
        
        # 测试所有老师路由
        test_routes = [
            ('/teacher/dashboard', '老师仪表板'),
            ('/teacher/students', '学生管理'),
            ('/teacher/classes', '班级管理'),
            ('/teacher/assignments', '作业管理'),
            ('/teacher/grades', '成绩管理'),
            ('/teacher/reports', '教学报告'),
            ('/teacher/resources', '教学资源'),
            ('/teacher/announcements', '公告管理'),
            ('/teacher/practice-records', '练习记录'),
            ('/teacher/invite-codes', '推广码管理'),
        ]
        
        print("\n📋 路由测试结果:")
        for route, description in test_routes:
            try:
                with app.test_client() as client:
                    # 模拟老师登录
                    from app.models.user import User
                    teacher = User.query.filter_by(email='teacher@aimuspal.com').first()
                    if teacher:
                        with client.session_transaction() as sess:
                            sess['user_id'] = teacher.id
                        
                        response = client.get(route, follow_redirects=True)
                        if response.status_code == 200:
                            print(f"  ✅ {route} -> {description}")
                        elif response.status_code == 302:
                            print(f"  ⚠️  {route} -> {description} (重定向)")
                        else:
                            print(f"  ❌ {route} -> {description} (状态码: {response.status_code})")
                    else:
                        print(f"  ❌ {route} -> {description} (未找到老师账户)")
            except Exception as e:
                print(f"  ❌ {route} -> {description} (错误: {e})")
        
        # 测试模板中的url_for调用
        print("\n🔍 检查模板中的url_for调用...")
        
        import os
        template_dir = 'app/templates/teacher'
        if os.path.exists(template_dir):
            for filename in os.listdir(template_dir):
                if filename.endswith('.html'):
                    filepath = os.path.join(template_dir, filename)
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            content = f.read()
                            if 'url_for(' in content:
                                print(f"  📄 {filename} - 包含url_for调用")
                    except Exception as e:
                        print(f"  ❌ {filename} - 读取失败: {e}")
        
        print("\n✅ 链接测试完成！")

if __name__ == '__main__':
    test_teacher_links() 
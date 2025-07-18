#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
老师重定向测试脚本
验证老师访问学生页面时会被正确重定向到老师仪表板
"""

import sys
import os
import requests
from datetime import datetime
sys.path.insert(0, os.path.abspath('.'))

def test_teacher_redirects():
    """测试老师重定向功能"""
    
    print("🔄 老师重定向测试")
    print(f"⏰ 测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    base_url = "http://localhost:5005"
    
    # 创建会话以保持登录状态
    session = requests.Session()
    
    # 先登录老师账户
    print("🔐 登录老师账户...")
    login_data = {
        'email': 'teacher@aimuspal.com',
        'password': 'teacher123'
    }
    
    try:
        login_response = session.post(f"{base_url}/auth/login", data=login_data, allow_redirects=False)
        if login_response.status_code == 302:
            print("  ✅ 老师登录成功")
        else:
            print(f"  ❌ 老师登录失败，状态码: {login_response.status_code}")
            return False
    except Exception as e:
        print(f"  ❌ 登录请求失败: {e}")
        return False
    
    # 测试学生页面重定向
    student_pages = [
        ("/dashboard", "学生仪表板"),
        ("/practices", "练习曲目"),
        ("/stats", "学习统计"),
        ("/practice-records", "练习记录"),
        ("/practices/1", "练习详情"),
        ("/practices/1/upload", "练习上传"),
        ("/practice-result/1", "练习结果")
    ]
    
    print("\n🔄 测试学生页面重定向:")
    redirect_success = 0
    
    for route, name in student_pages:
        try:
            response = session.get(f"{base_url}{route}", allow_redirects=False)
            
            if response.status_code == 302:
                # 检查重定向目标
                redirect_url = response.headers.get('Location', '')
                if '/teacher/dashboard' in redirect_url:
                    print(f"  ✅ {name} ({route}) - 正确重定向到老师仪表板")
                    redirect_success += 1
                else:
                    print(f"  ❌ {name} ({route}) - 重定向到错误位置: {redirect_url}")
            elif response.status_code == 200:
                print(f"  ❌ {name} ({route}) - 没有重定向，直接显示页面")
            else:
                print(f"  ❌ {name} ({route}) - 错误状态码: {response.status_code}")
                
        except Exception as e:
            print(f"  ❌ {name} ({route}) - 请求失败: {e}")
    
    print(f"\n📊 重定向测试结果: {redirect_success}/{len(student_pages)} 正确重定向")
    
    # 测试老师页面正常访问
    print("\n✅ 测试老师页面正常访问:")
    teacher_pages = [
        ("/teacher/dashboard", "老师仪表板"),
        ("/teacher/students", "学生管理"),
        ("/teacher/classes", "班级管理"),
        ("/teacher/assignments", "作业管理"),
        ("/teacher/grades", "成绩管理"),
        ("/teacher/reports", "教学报告"),
        ("/teacher/invite-codes", "推广码管理")
    ]
    
    teacher_success = 0
    
    for route, name in teacher_pages:
        try:
            response = session.get(f"{base_url}{route}", allow_redirects=False)
            
            if response.status_code == 200:
                print(f"  ✅ {name} ({route}) - 正常访问")
                teacher_success += 1
            elif response.status_code == 302:
                redirect_url = response.headers.get('Location', '')
                if '/auth/login' in redirect_url:
                    print(f"  ❌ {name} ({route}) - 需要重新登录")
                else:
                    print(f"  ❌ {name} ({route}) - 意外重定向: {redirect_url}")
            else:
                print(f"  ❌ {name} ({route}) - 错误状态码: {response.status_code}")
                
        except Exception as e:
            print(f"  ❌ {name} ({route}) - 请求失败: {e}")
    
    print(f"\n📊 老师页面测试结果: {teacher_success}/{len(teacher_pages)} 正常访问")
    
    # 总结
    total_tests = len(student_pages) + len(teacher_pages)
    total_success = redirect_success + teacher_success
    
    print(f"\n🎯 总体测试结果: {total_success}/{total_tests} 通过")
    
    if total_success == total_tests:
        print("🎉 所有测试通过！老师重定向功能正常工作。")
        return True
    else:
        print("⚠️ 部分测试失败，需要进一步检查。")
        return False

if __name__ == "__main__":
    test_teacher_redirects() 
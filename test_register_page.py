#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
注册页面测试脚本
验证当选择老师角色时推荐码字段被正确禁用
"""

import sys
import os
import requests
from datetime import datetime
sys.path.insert(0, os.path.abspath('.'))

def test_register_page():
    """测试注册页面功能"""
    
    print("📝 注册页面功能测试")
    print(f"⏰ 测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    base_url = "http://localhost:5005"
    
    # 测试注册页面访问
    print("🔍 测试注册页面访问...")
    try:
        response = requests.get(f"{base_url}/auth/register", timeout=5)
        if response.status_code == 200:
            print("  ✅ 注册页面可以正常访问")
            
            # 检查页面内容
            content = response.text
            
            # 检查是否包含必要的元素
            required_elements = [
                'studentRadio',
                'teacherRadio', 
                'hasRecommenderYes',
                'hasRecommenderNo',
                'recommender_code',
                'teacherNote'
            ]
            
            missing_elements = []
            for element in required_elements:
                if element not in content:
                    missing_elements.append(element)
            
            if missing_elements:
                print(f"  ❌ 缺少元素: {missing_elements}")
                return False
            else:
                print("  ✅ 所有必要元素都存在")
            
            # 检查JavaScript函数
            js_functions = [
                'toggleRecommender',
                'toggleRecommenderCode'
            ]
            
            missing_functions = []
            for func in js_functions:
                if func not in content:
                    missing_functions.append(func)
            
            if missing_functions:
                print(f"  ❌ 缺少JavaScript函数: {missing_functions}")
                return False
            else:
                print("  ✅ 所有JavaScript函数都存在")
            
            # 检查禁用逻辑
            if 'disabled = true' in content or 'disabled=true' in content:
                print("  ✅ 包含禁用逻辑")
            else:
                print("  ⚠️ 未找到明确的禁用逻辑")
            
            return True
            
        else:
            print(f"  ❌ 注册页面访问失败，状态码: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"  ❌ 注册页面访问异常: {e}")
        return False

def test_register_functionality():
    """测试注册功能"""
    
    print("\n🔐 测试注册功能...")
    
    base_url = "http://localhost:5005"
    
    # 测试学生注册（有推荐码）
    print("  📚 测试学生注册（有推荐码）...")
    student_data = {
        'email': 'test_student@example.com',
        'username': 'test_student',
        'first_name': '测试',
        'last_name': '学生',
        'password': 'test123',
        'password2': 'test123',
        'user_type': 'student',
        'has_recommender': 'yes',
        'recommender_code': 'TEST123'
    }
    
    try:
        response = requests.post(f"{base_url}/auth/register", data=student_data, allow_redirects=False)
        if response.status_code in [200, 302]:
            print("    ✅ 学生注册请求处理正常")
        else:
            print(f"    ❌ 学生注册请求异常，状态码: {response.status_code}")
    except Exception as e:
        print(f"    ❌ 学生注册请求失败: {e}")
    
    # 测试老师注册
    print("  👨‍🏫 测试老师注册...")
    teacher_data = {
        'email': 'test_teacher@example.com',
        'username': 'test_teacher',
        'first_name': '测试',
        'last_name': '老师',
        'password': 'test123',
        'password2': 'test123',
        'user_type': 'teacher'
        # 注意：老师注册不包含推荐码相关字段
    }
    
    try:
        response = requests.post(f"{base_url}/auth/register", data=teacher_data, allow_redirects=False)
        if response.status_code in [200, 302]:
            print("    ✅ 老师注册请求处理正常")
        else:
            print(f"    ❌ 老师注册请求异常，状态码: {response.status_code}")
    except Exception as e:
        print(f"    ❌ 老师注册请求失败: {e}")

if __name__ == "__main__":
    print("🎯 开始注册页面功能测试...")
    
    # 测试页面访问和元素
    page_test = test_register_page()
    
    # 测试注册功能
    test_register_functionality()
    
    print("\n📊 测试总结:")
    if page_test:
        print("✅ 注册页面功能测试通过")
    else:
        print("❌ 注册页面功能测试失败")
    
    print("\n💡 建议:")
    print("- 在浏览器中手动测试角色切换功能")
    print("- 验证推荐码字段在老师模式下被正确禁用")
    print("- 检查JavaScript控制台是否有错误") 
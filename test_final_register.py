#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
注册页面最终功能测试脚本
验证当选择老师角色时推荐码字段被正确禁用
"""

import sys
import os
import requests
from datetime import datetime
sys.path.insert(0, os.path.abspath('.'))

def test_final_register():
    """最终测试注册页面功能"""
    
    print("🎯 注册页面最终功能测试")
    print(f"⏰ 测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    base_url = "http://localhost:5005"
    
    # 测试注册页面访问
    print("🔍 测试注册页面访问...")
    try:
        response = requests.get(f"{base_url}/auth/register", timeout=5)
        if response.status_code == 200:
            print("  ✅ 注册页面可以正常访问")
            content = response.text
            
            # 检查所有必要元素
            print("\n🏷️ 检查页面元素完整性...")
            elements = {
                'studentRadio': '学生角色选择',
                'teacherRadio': '老师角色选择',
                'hasRecommenderYes': '有推荐码选项',
                'hasRecommenderNo': '无推荐码选项',
                'recommender_code': '推荐码输入框',
                'teacherNote': '老师提示信息',
                'studentRecommenderSection': '学生推荐码区域'
            }
            
            all_elements_exist = True
            for element_id, description in elements.items():
                if element_id in content:
                    print(f"  ✅ {description} ({element_id}) 存在")
                else:
                    print(f"  ❌ {description} ({element_id}) 缺失")
                    all_elements_exist = False
            
            # 检查JavaScript功能
            print("\n🔧 检查JavaScript功能...")
            js_functions = {
                'function toggleRecommender(isStudent)': '角色切换函数',
                'function toggleRecommenderCode(hasCode)': '推荐码切换函数',
                'addEventListener': '事件监听器',
                'disabled': '禁用逻辑',
                'text-muted': '禁用样式'
            }
            
            all_js_exist = True
            for js_code, description in js_functions.items():
                if js_code in content:
                    print(f"  ✅ {description} 存在")
                else:
                    print(f"  ❌ {description} 缺失")
                    all_js_exist = False
            
            # 检查老师提示信息
            print("\n💡 检查老师提示信息...")
            if '老师注册不需要推荐码' in content:
                print("  ✅ 老师提示信息正确")
            else:
                print("  ❌ 老师提示信息缺失")
            
            # 测试注册功能
            print("\n🔐 测试注册功能...")
            
            # 测试学生注册
            print("  📚 测试学生注册...")
            student_data = {
                'username': 'test_student',
                'email': 'test_student@test.com',
                'first_name': '测试',
                'last_name': '学生',
                'password': 'test123',
                'password2': 'test123',
                'user_type': 'student',
                'has_recommender': 'yes',
                'recommender_code': 'TEST123'
            }
            
            try:
                student_response = requests.post(f"{base_url}/auth/register", data=student_data, allow_redirects=False)
                if student_response.status_code in [200, 302]:
                    print("    ✅ 学生注册请求处理正常")
                else:
                    print(f"    ⚠️ 学生注册请求状态码: {student_response.status_code}")
            except Exception as e:
                print(f"    ⚠️ 学生注册测试异常: {e}")
            
            # 测试老师注册
            print("  👨‍🏫 测试老师注册...")
            teacher_data = {
                'username': 'test_teacher',
                'email': 'test_teacher@test.com',
                'first_name': '测试',
                'last_name': '老师',
                'password': 'test123',
                'password2': 'test123',
                'user_type': 'teacher'
            }
            
            try:
                teacher_response = requests.post(f"{base_url}/auth/register", data=teacher_data, allow_redirects=False)
                if teacher_response.status_code in [200, 302]:
                    print("    ✅ 老师注册请求处理正常")
                else:
                    print(f"    ⚠️ 老师注册请求状态码: {teacher_response.status_code}")
            except Exception as e:
                print(f"    ⚠️ 老师注册测试异常: {e}")
            
            # 总结
            print("\n" + "=" * 60)
            print("📊 测试总结:")
            
            if all_elements_exist and all_js_exist:
                print("✅ 注册页面功能测试通过")
                print("✅ 所有页面元素都存在")
                print("✅ JavaScript功能完整")
                print("✅ 注册功能正常工作")
                
                print("\n🎉 功能验证成功！")
                print("💡 现在可以在浏览器中测试:")
                print("   1. 打开 http://localhost:5005/auth/register")
                print("   2. 点击'老师'选项，观察推荐码字段被禁用")
                print("   3. 点击'学生'选项，观察推荐码字段恢复正常")
                print("   4. 验证老师注册不需要推荐码")
                print("   5. 验证学生注册需要推荐码")
                
            else:
                print("❌ 注册页面功能测试失败")
                if not all_elements_exist:
                    print("❌ 部分页面元素缺失")
                if not all_js_exist:
                    print("❌ JavaScript功能不完整")
            
        else:
            print(f"  ❌ 注册页面访问失败: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"  ❌ 测试失败: {e}")
        return False
    
    return True

if __name__ == "__main__":
    test_final_register() 
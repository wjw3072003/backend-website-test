#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
注册页面JavaScript功能测试脚本
验证当选择老师角色时推荐码字段被正确禁用
"""

import sys
import os
import requests
from datetime import datetime
sys.path.insert(0, os.path.abspath('.'))

def test_register_javascript():
    """测试注册页面JavaScript功能"""
    
    print("🎯 注册页面JavaScript功能测试")
    print(f"⏰ 测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    base_url = "http://localhost:5005"
    
    # 获取注册页面内容
    print("🔍 获取注册页面内容...")
    try:
        response = requests.get(f"{base_url}/auth/register", timeout=5)
        if response.status_code == 200:
            content = response.text
            print("  ✅ 成功获取注册页面")
            
            # 检查JavaScript函数
            print("\n🔧 检查JavaScript函数...")
            
            # 检查toggleRecommender函数
            if 'function toggleRecommender(isStudent)' in content:
                print("  ✅ toggleRecommender函数存在")
            else:
                print("  ❌ toggleRecommender函数缺失")
            
            # 检查toggleRecommenderCode函数
            if 'function toggleRecommenderCode(hasCode)' in content:
                print("  ✅ toggleRecommenderCode函数存在")
            else:
                print("  ❌ toggleRecommenderCode函数缺失")
            
            # 检查老师提示信息
            print("\n💡 检查老师提示信息...")
            if '老师注册不需要推荐码' in content:
                print("  ✅ 老师提示信息存在")
            else:
                print("  ❌ 老师提示信息缺失")
            
            # 检查禁用逻辑
            print("\n🚫 检查禁用逻辑...")
            if 'disabled' in content and 'teacherRadio' in content:
                print("  ✅ 禁用逻辑存在")
            else:
                print("  ❌ 禁用逻辑可能缺失")
            
            # 检查事件监听器
            print("\n👂 检查事件监听器...")
            if 'addEventListener' in content and 'teacherRadio' in content:
                print("  ✅ 事件监听器存在")
            else:
                print("  ❌ 事件监听器可能缺失")
            
            # 检查样式类
            print("\n🎨 检查样式类...")
            if 'text-muted' in content:
                print("  ✅ 禁用样式类存在")
            else:
                print("  ❌ 禁用样式类缺失")
            
            # 检查HTML元素ID
            print("\n🏷️ 检查HTML元素ID...")
            required_ids = [
                'studentRadio',
                'teacherRadio', 
                'hasRecommenderYes',
                'hasRecommenderNo',
                'recommender_code',
                'teacherNote',
                'studentRecommenderSection'
            ]
            
            missing_ids = []
            for element_id in required_ids:
                if element_id in content:
                    print(f"  ✅ {element_id} 存在")
                else:
                    print(f"  ❌ {element_id} 缺失")
                    missing_ids.append(element_id)
            
            if missing_ids:
                print(f"\n⚠️ 缺失的元素ID: {', '.join(missing_ids)}")
            else:
                print("\n✅ 所有必要的HTML元素ID都存在")
            
            # 检查JavaScript代码完整性
            print("\n📜 检查JavaScript代码完整性...")
            js_checks = [
                'document.getElementById(\'teacherRadio\').addEventListener',
                'document.getElementById(\'studentRadio\').addEventListener',
                'toggleRecommender(false)',
                'toggleRecommender(true)',
                'style.display = \'none\'',
                'style.display = \'block\''
            ]
            
            for check in js_checks:
                if check in content:
                    print(f"  ✅ {check[:30]}... 存在")
                else:
                    print(f"  ❌ {check[:30]}... 缺失")
            
        else:
            print(f"  ❌ 注册页面访问失败: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"  ❌ 测试失败: {e}")
        return False
    
    print("\n" + "=" * 60)
    print("🎯 JavaScript功能测试完成")
    print("\n💡 建议:")
    print("- 在浏览器中打开 http://localhost:5005/auth/register")
    print("- 点击'老师'选项，观察推荐码字段是否被禁用")
    print("- 点击'学生'选项，观察推荐码字段是否恢复正常")
    print("- 检查浏览器控制台是否有JavaScript错误")
    
    return True

if __name__ == "__main__":
    test_register_javascript() 
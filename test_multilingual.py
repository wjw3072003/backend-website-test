#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
多语言功能测试脚本
"""

import sys
import os
import requests
from datetime import datetime
sys.path.insert(0, os.path.abspath('.'))

def test_multilingual():
    """测试多语言功能"""
    
    print("🌍 多语言功能测试")
    print(f"⏰ 测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    base_url = "http://localhost:5005"
    
    # 测试不同语言的首页
    languages = {
        'zh_CN': '简体中文',
        'zh_TW': '繁體中文', 
        'en': 'English'
    }
    
    print("🔍 测试语言切换功能...")
    
    for lang_code, lang_name in languages.items():
        print(f"\n📝 测试 {lang_name} ({lang_code})...")
        
        try:
            # 测试语言切换
            response = requests.get(f"{base_url}/i18n/set-language/{lang_code}", allow_redirects=False)
            if response.status_code == 302:
                print(f"  ✅ {lang_name} 语言切换成功")
                
                # 获取重定向后的页面
                redirect_url = response.headers.get('Location', '')
                if redirect_url:
                    page_response = requests.get(f"{base_url}{redirect_url}")
                    if page_response.status_code == 200:
                        print(f"  ✅ {lang_name} 页面加载成功")
                        
                        # 检查页面内容
                        content = page_response.text
                        
                        # 检查导航栏文本
                        if lang_code == 'zh_CN':
                            if '首页' in content and '仪表板' in content:
                                print(f"  ✅ {lang_name} 导航栏文本正确")
                            else:
                                print(f"  ❌ {lang_name} 导航栏文本错误")
                        elif lang_code == 'zh_TW':
                            if '首頁' in content and '儀表板' in content:
                                print(f"  ✅ {lang_name} 导航栏文本正确")
                            else:
                                print(f"  ❌ {lang_name} 导航栏文本错误")
                        elif lang_code == 'en':
                            if 'Home' in content and 'Dashboard' in content:
                                print(f"  ✅ {lang_name} 导航栏文本正确")
                            else:
                                print(f"  ❌ {lang_name} 导航栏文本错误")
                    else:
                        print(f"  ❌ {lang_name} 页面加载失败: {page_response.status_code}")
                else:
                    print(f"  ❌ {lang_name} 重定向URL为空")
            else:
                print(f"  ❌ {lang_name} 语言切换失败: {response.status_code}")
                
        except Exception as e:
            print(f"  ❌ {lang_name} 测试异常: {e}")
    
    # 测试语言信息页面
    print("\n🌐 测试语言信息页面...")
    try:
        response = requests.get(f"{base_url}/i18n/language")
        if response.status_code == 200:
            print("  ✅ 语言信息页面可以访问")
            content = response.text
            
            # 检查是否包含语言选择选项
            if '简体中文' in content and '繁體中文' in content and 'English' in content:
                print("  ✅ 语言选择选项完整")
            else:
                print("  ❌ 语言选择选项不完整")
        else:
            print(f"  ❌ 语言信息页面访问失败: {response.status_code}")
    except Exception as e:
        print(f"  ❌ 语言信息页面测试异常: {e}")
    
    # 测试首页默认语言
    print("\n🏠 测试首页默认语言...")
    try:
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            print("  ✅ 首页可以访问")
            content = response.text
            
            # 检查默认语言（应该是简体中文）
            if '首页' in content and '仪表板' in content:
                print("  ✅ 默认语言为简体中文")
            else:
                print("  ❌ 默认语言不是简体中文")
        else:
            print(f"  ❌ 首页访问失败: {response.status_code}")
    except Exception as e:
        print(f"  ❌ 首页测试异常: {e}")
    
    print("\n" + "=" * 60)
    print("🎯 多语言功能测试完成")
    print("\n💡 建议:")
    print("1. 在浏览器中访问 http://localhost:5005")
    print("2. 点击导航栏右上角的语言选择器")
    print("3. 测试不同语言的切换效果")
    print("4. 验证页面文本是否正确翻译")
    
    return True

if __name__ == "__main__":
    test_multilingual() 
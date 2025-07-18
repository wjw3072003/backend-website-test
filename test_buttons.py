#!/usr/bin/env python3
"""
测试AiMusPal主页按钮跳转功能
"""

import requests
import time
from urllib.parse import urljoin

# 配置
BASE_URL = "http://192.168.31.56:5005"
TIMEOUT = 10

def test_page_access():
    """测试页面访问"""
    print("🔍 测试页面访问...")
    
    # 测试主页重定向
    try:
        response = requests.get(f"{BASE_URL}/", timeout=TIMEOUT, allow_redirects=True)
        print(f"✅ 主页重定向: {response.status_code} -> {response.url}")
        if "aimuspal" in response.url:
            print("✅ 主页正确重定向到 /aimuspal")
        else:
            print("❌ 主页重定向路径不正确")
    except Exception as e:
        print(f"❌ 主页访问失败: {e}")
    
    # 测试直接访问aimuspal页面
    try:
        response = requests.get(f"{BASE_URL}/aimuspal", timeout=TIMEOUT)
        print(f"✅ 直接访问 /aimuspal: {response.status_code}")
        if response.status_code == 200:
            print("✅ /aimuspal 页面可正常访问")
        else:
            print("❌ /aimuspal 页面访问失败")
    except Exception as e:
        print(f"❌ /aimuspal 访问失败: {e}")

def test_auth_pages():
    """测试认证页面"""
    print("\n🔐 测试认证页面...")
    
    # 测试登录页面
    try:
        response = requests.get(f"{BASE_URL}/auth/login", timeout=TIMEOUT)
        print(f"✅ 登录页面: {response.status_code}")
        if response.status_code == 200:
            print("✅ 登录页面可正常访问")
        else:
            print("❌ 登录页面访问失败")
    except Exception as e:
        print(f"❌ 登录页面访问失败: {e}")
    
    # 测试注册页面
    try:
        response = requests.get(f"{BASE_URL}/auth/register", timeout=TIMEOUT)
        print(f"✅ 注册页面: {response.status_code}")
        if response.status_code == 200:
            print("✅ 注册页面可正常访问")
        else:
            print("❌ 注册页面访问失败")
    except Exception as e:
        print(f"❌ 注册页面访问失败: {e}")

def test_button_links():
    """测试按钮链接"""
    print("\n🔗 测试按钮链接...")
    
    # 获取主页内容
    try:
        response = requests.get(f"{BASE_URL}/aimuspal", timeout=TIMEOUT)
        content = response.text
        
        # 检查登录按钮
        if 'onclick="window.location.href=\'/auth/login\'"' in content:
            print("✅ 登录按钮链接正确")
        else:
            print("❌ 登录按钮链接错误或缺失")
        
        # 检查注册按钮
        if 'onclick="window.location.href=\'/auth/register\'"' in content:
            print("✅ 注册按钮链接正确")
        else:
            print("❌ 注册按钮链接错误或缺失")
        
        # 统计按钮数量
        login_buttons = content.count('onclick="window.location.href=\'/auth/login\'"')
        register_buttons = content.count('onclick="window.location.href=\'/auth/register\'"')
        
        print(f"📊 找到 {login_buttons} 个登录按钮")
        print(f"📊 找到 {register_buttons} 个注册按钮")
        
    except Exception as e:
        print(f"❌ 获取页面内容失败: {e}")

def test_manual_navigation():
    """测试手动导航"""
    print("\n🧪 测试手动导航...")
    
    print("请手动测试以下链接:")
    print(f"1. 主页: {BASE_URL}/")
    print(f"2. 直接访问: {BASE_URL}/aimuspal")
    print(f"3. 登录页面: {BASE_URL}/auth/login")
    print(f"4. 注册页面: {BASE_URL}/auth/register")
    print(f"5. 备用首页: {BASE_URL}/index_back")

def main():
    """主测试函数"""
    print("🚀 开始测试AiMusPal主页按钮功能")
    print("=" * 50)
    
    test_page_access()
    test_auth_pages()
    test_button_links()
    test_manual_navigation()
    
    print("\n" + "=" * 50)
    print("✅ 测试完成！")
    print("\n💡 建议:")
    print("1. 在浏览器中访问主页，点击各个按钮")
    print("2. 确认按钮能正确跳转到登录/注册页面")
    print("3. 测试不同设备尺寸下的按钮功能")

if __name__ == "__main__":
    main() 
#!/usr/bin/env python3
"""
按钮功能测试脚本
测试主页按钮是否能正常工作
"""

import requests
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

def test_button_functionality():
    """测试按钮功能"""
    print("🔧 开始测试按钮功能...")
    
    # 配置Chrome选项
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # 无头模式
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    
    try:
        # 启动浏览器
        driver = webdriver.Chrome(options=chrome_options)
        driver.get("http://192.168.31.56:5005/aimuspal")
        
        print("✅ 页面加载成功")
        
        # 等待页面完全加载
        time.sleep(3)
        
        # 查找按钮
        buttons = driver.find_elements(By.TAG_NAME, "button")
        target_buttons = []
        
        for button in buttons:
            text = button.text.strip()
            if text in ['Sign In', 'Start Free Trial', 'Start for Free']:
                target_buttons.append((button, text))
                print(f"找到按钮: {text}")
        
        if not target_buttons:
            print("❌ 未找到目标按钮")
            return False
        
        # 测试每个按钮
        for button, text in target_buttons:
            try:
                print(f"测试按钮: {text}")
                
                # 滚动到按钮位置
                driver.execute_script("arguments[0].scrollIntoView();", button)
                time.sleep(1)
                
                # 点击按钮
                button.click()
                time.sleep(2)
                
                # 检查URL是否改变
                current_url = driver.current_url
                print(f"当前URL: {current_url}")
                
                if text == 'Sign In' and '/auth/login' in current_url:
                    print(f"✅ {text} 按钮跳转成功")
                elif text in ['Start Free Trial', 'Start for Free'] and '/auth/register' in current_url:
                    print(f"✅ {text} 按钮跳转成功")
                else:
                    print(f"❌ {text} 按钮跳转失败")
                
                # 返回主页继续测试
                driver.get("http://192.168.31.56:5005/aimuspal")
                time.sleep(2)
                
            except Exception as e:
                print(f"❌ 测试按钮 {text} 时出错: {e}")
        
        print("✅ 按钮功能测试完成")
        return True
        
    except Exception as e:
        print(f"❌ 测试过程中出错: {e}")
        return False
    
    finally:
        try:
            driver.quit()
        except:
            pass

def test_page_access():
    """测试页面访问"""
    print("🌐 测试页面访问...")
    
    urls = [
        "http://192.168.31.56:5005/",
        "http://192.168.31.56:5005/aimuspal",
        "http://192.168.31.56:5005/auth/login",
        "http://192.168.31.56:5005/auth/register"
    ]
    
    for url in urls:
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                print(f"✅ {url} - 访问成功")
            else:
                print(f"❌ {url} - 状态码: {response.status_code}")
        except Exception as e:
            print(f"❌ {url} - 访问失败: {e}")

if __name__ == "__main__":
    print("🚀 开始按钮功能测试")
    print("=" * 50)
    
    # 测试页面访问
    test_page_access()
    print()
    
    # 测试按钮功能
    test_button_functionality()
    
    print("=" * 50)
    print("🎉 测试完成") 
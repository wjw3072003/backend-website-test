#!/usr/bin/env python3
import re
import os
import requests
from urllib.parse import urlparse
import time

def extract_font_urls(html_content):
    """从HTML内容中提取所有Google Fonts URL"""
    # 匹配Google Fonts的URL
    pattern = r'https://fonts\.gstatic\.com/[^"\s]+\.woff2'
    urls = re.findall(pattern, html_content)
    
    # 去重
    unique_urls = list(set(urls))
    return unique_urls

def download_font(url, local_path):
    """下载单个字体文件"""
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        # 确保目录存在
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        
        # 写入文件
        with open(local_path, 'wb') as f:
            f.write(response.content)
        
        print(f"✓ 下载成功: {os.path.basename(local_path)}")
        return True
    except Exception as e:
        print(f"✗ 下载失败: {url} - {str(e)}")
        return False

def main():
    # 读取原网站HTML
    with open('original_homepage.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # 提取字体URL
    font_urls = extract_font_urls(html_content)
    print(f"找到 {len(font_urls)} 个唯一字体URL")
    
    # 创建static/fonts目录
    static_dir = 'static/fonts'
    os.makedirs(static_dir, exist_ok=True)
    
    # 下载所有字体
    success_count = 0
    for i, url in enumerate(font_urls, 1):
        print(f"[{i}/{len(font_urls)}] 下载: {url}")
        
        # 从URL提取文件名
        filename = os.path.basename(urlparse(url).path)
        local_path = os.path.join(static_dir, filename)
        
        if download_font(url, local_path):
            success_count += 1
        
        # 添加延迟避免请求过快
        time.sleep(0.5)
    
    print(f"\n字体下载完成! 成功: {success_count}/{len(font_urls)}")
    
    # 生成字体映射文件
    generate_font_mapping(font_urls, static_dir)

def generate_font_mapping(font_urls, static_dir):
    """生成字体URL映射文件"""
    mapping = {}
    for url in font_urls:
        filename = os.path.basename(urlparse(url).path)
        local_path = f"/static/fonts/{filename}"
        mapping[url] = local_path
    
    # 保存映射到文件
    with open('font_mapping.txt', 'w', encoding='utf-8') as f:
        for original_url, local_path in mapping.items():
            f.write(f"{original_url} -> {local_path}\n")
    
    print(f"字体映射已保存到 font_mapping.txt")

if __name__ == "__main__":
    main() 
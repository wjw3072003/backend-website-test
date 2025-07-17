#!/usr/bin/env python3
import re
import os
import requests
from urllib.parse import urlparse
import time

def extract_image_urls(html_content):
    """从HTML内容中提取所有图片URL"""
    # 匹配所有framerusercontent.com的图片链接
    pattern = r'https://framerusercontent\.com/images/[^"\s]+\.(?:png|jpg|jpeg|gif|svg|webp)'
    urls = re.findall(pattern, html_content)
    
    # 去重并清理URL
    unique_urls = []
    for url in urls:
        # 移除URL参数
        clean_url = url.split('?')[0]
        if clean_url not in unique_urls:
            unique_urls.append(clean_url)
    
    return unique_urls

def download_image(url, local_path):
    """下载单个图片"""
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
    
    # 提取图片URL
    image_urls = extract_image_urls(html_content)
    print(f"找到 {len(image_urls)} 个唯一图片URL")
    
    # 创建static/images目录
    static_dir = 'static/images'
    os.makedirs(static_dir, exist_ok=True)
    
    # 下载所有图片
    success_count = 0
    for i, url in enumerate(image_urls, 1):
        print(f"[{i}/{len(image_urls)}] 下载: {url}")
        
        # 从URL提取文件名
        filename = os.path.basename(urlparse(url).path)
        local_path = os.path.join(static_dir, filename)
        
        if download_image(url, local_path):
            success_count += 1
        
        # 添加延迟避免请求过快
        time.sleep(0.5)
    
    print(f"\n下载完成! 成功: {success_count}/{len(image_urls)}")
    
    # 生成图片映射文件
    generate_image_mapping(image_urls, static_dir)

def generate_image_mapping(image_urls, static_dir):
    """生成图片URL映射文件"""
    mapping = {}
    for url in image_urls:
        filename = os.path.basename(urlparse(url).path)
        local_path = f"/static/images/{filename}"
        mapping[url] = local_path
    
    # 保存映射到文件
    with open('image_mapping.txt', 'w', encoding='utf-8') as f:
        for original_url, local_path in mapping.items():
            f.write(f"{original_url} -> {local_path}\n")
    
    print(f"图片映射已保存到 image_mapping.txt")

if __name__ == "__main__":
    main() 
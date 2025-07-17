#!/usr/bin/env python3
import re
import os
import requests
from urllib.parse import urlparse
import time

def extract_js_css_urls(html_content):
    """提取所有JS/MJS/CSS资源URL"""
    pattern = r'https://framerusercontent\.com/[^"\s>]+\.(?:js|mjs|css)'
    urls = re.findall(pattern, html_content)
    return list(set(urls))

def download_file(url, local_path):
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        with open(local_path, 'wb') as f:
            f.write(response.content)
        print(f"✓ 下载成功: {os.path.basename(local_path)}")
        return True
    except Exception as e:
        print(f"✗ 下载失败: {url} - {str(e)}")
        return False

def main():
    with open('original_homepage.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
    urls = extract_js_css_urls(html_content)
    print(f"共找到{len(urls)}个JS/MJS/CSS资源")
    static_dir = 'static/js'
    os.makedirs(static_dir, exist_ok=True)
    for i, url in enumerate(urls, 1):
        filename = os.path.basename(urlparse(url).path)
        local_path = os.path.join(static_dir, filename)
        print(f"[{i}/{len(urls)}] 下载: {url}")
        download_file(url, local_path)
        time.sleep(0.5)
    print("全部下载完成！")
    # 生成映射
    with open('js_css_mapping.txt', 'w', encoding='utf-8') as f:
        for url in urls:
            filename = os.path.basename(urlparse(url).path)
            local_path = f"/static/js/{filename}"
            f.write(f"{url} -> {local_path}\n")
    print("映射已保存到js_css_mapping.txt")

if __name__ == "__main__":
    main() 
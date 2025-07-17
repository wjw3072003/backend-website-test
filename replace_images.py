#!/usr/bin/env python3
import re
import os

def load_image_mapping():
    """加载图片映射"""
    mapping = {}
    with open('image_mapping.txt', 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if ' -> ' in line:
                original_url, local_path = line.split(' -> ')
                mapping[original_url] = local_path
    return mapping

def replace_image_urls(html_content, mapping):
    """替换HTML中的图片URL"""
    # 替换所有framerusercontent.com的图片链接
    for original_url, local_path in mapping.items():
        # 处理带参数的URL
        pattern = re.escape(original_url) + r'(?:\?[^"\s]*)?'
        html_content = re.sub(pattern, local_path, html_content)
    
    return html_content

def main():
    # 加载图片映射
    mapping = load_image_mapping()
    print(f"加载了 {len(mapping)} 个图片映射")
    
    # 读取原网站HTML
    with open('original_homepage.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # 替换图片URL
    modified_html = replace_image_urls(html_content, mapping)
    
    # 保存修改后的HTML
    with open('aimuspal_homepage_localized.html', 'w', encoding='utf-8') as f:
        f.write(modified_html)
    
    print("图片URL替换完成，已保存到 aimuspal_homepage_localized.html")
    
    # 统计替换次数
    replacement_count = 0
    for original_url in mapping:
        if original_url in html_content:
            replacement_count += html_content.count(original_url)
    
    print(f"总共替换了 {replacement_count} 个图片链接")

if __name__ == "__main__":
    main() 
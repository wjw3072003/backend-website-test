#!/usr/bin/env python3
import re
import os

def load_font_mapping():
    """加载字体映射"""
    mapping = {}
    with open('font_mapping.txt', 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if ' -> ' in line:
                original_url, local_path = line.split(' -> ')
                mapping[original_url] = local_path
    return mapping

def replace_font_urls(html_content, mapping):
    """替换HTML中的字体URL"""
    # 替换所有Google Fonts的链接
    for original_url, local_path in mapping.items():
        # 处理带参数的URL
        pattern = re.escape(original_url) + r'(?:\?[^"\s]*)?'
        html_content = re.sub(pattern, local_path, html_content)
    
    return html_content

def main():
    # 加载字体映射
    mapping = load_font_mapping()
    print(f"加载了 {len(mapping)} 个字体映射")
    
    # 读取已本地化的HTML
    with open('aimuspal_homepage_localized.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # 替换字体URL
    modified_html = replace_font_urls(html_content, mapping)
    
    # 保存修改后的HTML
    with open('aimuspal_homepage_complete.html', 'w', encoding='utf-8') as f:
        f.write(modified_html)
    
    print("字体URL替换完成，已保存到 aimuspal_homepage_complete.html")
    
    # 统计替换次数
    replacement_count = 0
    for original_url in mapping:
        if original_url in html_content:
            replacement_count += html_content.count(original_url)
    
    print(f"总共替换了 {replacement_count} 个字体链接")

if __name__ == "__main__":
    main() 
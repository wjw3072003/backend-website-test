#!/usr/bin/env python3
import re

def clean_external_scripts(html_content):
    """移除HTML中的外部JavaScript依赖"""
    
    # 移除framer-search-index meta标签
    html_content = re.sub(r'<meta name="framer-search-index"[^>]*>', '', html_content)
    
    # 移除所有modulepreload链接
    html_content = re.sub(r'<link rel="modulepreload"[^>]*>', '', html_content)
    
    # 移除framer的JavaScript脚本
    html_content = re.sub(r'<script[^>]*framerusercontent\.com[^>]*></script>', '', html_content)
    
    # 移除framer事件脚本
    html_content = re.sub(r'<script[^>]*events\.framer\.com[^>]*></script>', '', html_content)
    
    # 移除Google Fonts预连接
    html_content = re.sub(r'<link href="https://fonts\.gstatic\.com"[^>]*>', '', html_content)
    
    # 移除canonical和og:url链接
    html_content = re.sub(r'<link rel="canonical"[^>]*>', '', html_content)
    html_content = re.sub(r'<meta property="og:url"[^>]*>', '', html_content)
    
    return html_content

def main():
    # 读取最终HTML文件
    with open('aimuspal_homepage_final.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # 清理外部脚本
    cleaned_html = clean_external_scripts(html_content)
    
    # 保存清理后的HTML
    with open('aimuspal_homepage_clean.html', 'w', encoding='utf-8') as f:
        f.write(cleaned_html)
    
    print("外部脚本清理完成，已保存到 aimuspal_homepage_clean.html")
    
    # 检查是否还有外部链接
    external_links = re.findall(r'https://[^"\s]+', cleaned_html)
    if external_links:
        print(f"警告：还有 {len(external_links)} 个外部链接")
        for link in external_links[:5]:  # 只显示前5个
            print(f"  - {link}")
    else:
        print("✓ 所有外部链接已清理完成")

if __name__ == "__main__":
    main() 
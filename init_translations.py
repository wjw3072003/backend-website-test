#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
初始化翻译文件
"""

import os
import subprocess
import sys

def init_translations():
    """初始化翻译文件"""
    
    print("🌍 初始化多语言翻译...")
    
    # 检查是否安装了Babel
    try:
        import babel
        print("✅ Babel已安装")
    except ImportError:
        print("❌ Babel未安装，请先安装: pip install Babel")
        return False
    
    # 创建翻译目录
    translations_dir = "app/translations"
    if not os.path.exists(translations_dir):
        os.makedirs(translations_dir)
        print(f"✅ 创建翻译目录: {translations_dir}")
    
    # 提取消息
    print("📝 提取需要翻译的消息...")
    try:
        subprocess.run([
            "pybabel", "extract", 
            "-F", "babel.cfg", 
            "-k", "_l", 
            "-o", "app/translations/messages.pot", 
            "."
        ], check=True)
        print("✅ 消息提取完成")
    except subprocess.CalledProcessError as e:
        print(f"❌ 消息提取失败: {e}")
        return False
    
    # 为每种语言创建翻译目录
    languages = ['zh_CN', 'zh_TW', 'en']
    
    for lang in languages:
        lang_dir = f"app/translations/{lang}"
        if not os.path.exists(lang_dir):
            os.makedirs(lang_dir)
            print(f"✅ 创建语言目录: {lang_dir}")
        
        # 初始化翻译文件
        po_file = f"app/translations/{lang}/LC_MESSAGES/messages.po"
        if not os.path.exists(po_file):
            try:
                subprocess.run([
                    "pybabel", "init", 
                    "-i", "app/translations/messages.pot", 
                    "-d", "app/translations", 
                    "-l", lang
                ], check=True)
                print(f"✅ 初始化 {lang} 翻译文件")
            except subprocess.CalledProcessError as e:
                print(f"❌ 初始化 {lang} 翻译文件失败: {e}")
                return False
    
    print("\n🎉 翻译初始化完成！")
    print("\n📋 下一步操作:")
    print("1. 编辑翻译文件:")
    print("   - app/translations/zh_CN/LC_MESSAGES/messages.po (简体中文)")
    print("   - app/translations/zh_TW/LC_MESSAGES/messages.po (繁体中文)")
    print("   - app/translations/en/LC_MESSAGES/messages.po (英文)")
    print("2. 编译翻译文件: python compile_translations.py")
    print("3. 重启应用以应用翻译")
    
    return True

if __name__ == "__main__":
    init_translations() 
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
编译翻译文件
"""

import os
import subprocess
import sys

def compile_translations():
    """编译翻译文件"""
    
    print("🔨 编译翻译文件...")
    
    # 检查翻译目录是否存在
    translations_dir = "app/translations"
    if not os.path.exists(translations_dir):
        print("❌ 翻译目录不存在，请先运行: python init_translations.py")
        return False
    
    # 编译所有语言的翻译文件
    languages = ['zh_CN', 'zh_TW', 'en']
    
    for lang in languages:
        po_file = f"app/translations/{lang}/LC_MESSAGES/messages.po"
        mo_file = f"app/translations/{lang}/LC_MESSAGES/messages.mo"
        
        if os.path.exists(po_file):
            try:
                subprocess.run([
                    "pybabel", "compile", 
                    "-d", "app/translations", 
                    "-l", lang
                ], check=True)
                print(f"✅ 编译 {lang} 翻译文件")
            except subprocess.CalledProcessError as e:
                print(f"❌ 编译 {lang} 翻译文件失败: {e}")
                return False
        else:
            print(f"⚠️ {lang} 翻译文件不存在: {po_file}")
    
    print("\n🎉 翻译编译完成！")
    print("💡 现在可以重启应用以应用翻译")
    
    return True

if __name__ == "__main__":
    compile_translations() 
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
添加翻译内容
"""

import os

def add_translations():
    """添加翻译内容"""
    
    print("📝 添加翻译内容...")
    
    # 简体中文翻译
    zh_cn_content = '''# Chinese (Simplified) translations for PROJECT.
# Copyright (C) 2024 ORGANIZATION
# This file is distributed under the same license as the PROJECT project.
# FIRST AUTHOR <EMAIL@ADDRESS>, 2024.
#
msgid ""
msgstr ""
"Project-Id-Version: PROJECT VERSION\n"
"Report-Msgid-Bugs-To: EMAIL@ADDRESS\n"
"POT-Creation-Date: 2024-07-18 04:13+0000\n"
"PO-Revision-Date: 2024-07-18 04:13+0000\n"
"Last-Translator: FULL NAME <EMAIL@ADDRESS>\n"
"Language: zh_CN\n"
"MIME-Version: 1.0\n"
"Content-Type: text/plain; charset=UTF-8\n"
"Content-Transfer-Encoding: 8bit\n"
"Generated-By: Babel 2.13.1\n"

msgid "首页"
msgstr "首页"

msgid "仪表板"
msgstr "仪表板"

msgid "练习曲目"
msgstr "练习曲目"

msgid "学习统计"
msgstr "学习统计"

msgid "管理后台"
msgstr "管理后台"

msgid "老师后台"
msgstr "老师后台"

msgid "关于"
msgstr "关于"

msgid "登录"
msgstr "登录"

msgid "注册"
msgstr "注册"

msgid "个人资料"
msgstr "个人资料"

msgid "登出"
msgstr "登出"

msgid "联系我们"
msgstr "联系我们"

msgid "隐私政策"
msgstr "隐私政策"

msgid "服务条款"
msgstr "服务条款"

msgid "语言设置"
msgstr "语言设置"

msgid "当前语言"
msgstr "当前语言"

msgid "当前系统语言："
msgstr "当前系统语言："
'''
    
    # 繁体中文翻译
    zh_tw_content = '''# Chinese (Traditional) translations for PROJECT.
# Copyright (C) 2024 ORGANIZATION
# This file is distributed under the same license as the PROJECT project.
# FIRST AUTHOR <EMAIL@ADDRESS>, 2024.
#
msgid ""
msgstr ""
"Project-Id-Version: PROJECT VERSION\n"
"Report-Msgid-Bugs-To: EMAIL@ADDRESS\n"
"POT-Creation-Date: 2024-07-18 04:13+0000\n"
"PO-Revision-Date: 2024-07-18 04:13+0000\n"
"Last-Translator: FULL NAME <EMAIL@ADDRESS>\n"
"Language: zh_TW\n"
"MIME-Version: 1.0\n"
"Content-Type: text/plain; charset=UTF-8\n"
"Content-Transfer-Encoding: 8bit\n"
"Generated-By: Babel 2.13.1\n"

msgid "首页"
msgstr "首頁"

msgid "仪表板"
msgstr "儀表板"

msgid "练习曲目"
msgstr "練習曲目"

msgid "学习统计"
msgstr "學習統計"

msgid "管理后台"
msgstr "管理後台"

msgid "老师后台"
msgstr "老師後台"

msgid "关于"
msgstr "關於"

msgid "登录"
msgstr "登錄"

msgid "注册"
msgstr "註冊"

msgid "个人资料"
msgstr "個人資料"

msgid "登出"
msgstr "登出"

msgid "联系我们"
msgstr "聯繫我們"

msgid "隐私政策"
msgstr "隱私政策"

msgid "服务条款"
msgstr "服務條款"

msgid "语言设置"
msgstr "語言設置"

msgid "当前语言"
msgstr "當前語言"

msgid "当前系统语言："
msgstr "當前系統語言："
'''
    
    # 英文翻译
    en_content = '''# English translations for PROJECT.
# Copyright (C) 2024 ORGANIZATION
# This file is distributed under the same license as the PROJECT project.
# FIRST AUTHOR <EMAIL@ADDRESS>, 2024.
#
msgid ""
msgstr ""
"Project-Id-Version: PROJECT VERSION\n"
"Report-Msgid-Bugs-To: EMAIL@ADDRESS\n"
"POT-Creation-Date: 2024-07-18 04:13+0000\n"
"PO-Revision-Date: 2024-07-18 04:13+0000\n"
"Last-Translator: FULL NAME <EMAIL@ADDRESS>\n"
"Language: en\n"
"MIME-Version: 1.0\n"
"Content-Type: text/plain; charset=UTF-8\n"
"Content-Transfer-Encoding: 8bit\n"
"Generated-By: Babel 2.13.1\n"

msgid "首页"
msgstr "Home"

msgid "仪表板"
msgstr "Dashboard"

msgid "练习曲目"
msgstr "Practice Pieces"

msgid "学习统计"
msgstr "Learning Statistics"

msgid "管理后台"
msgstr "Admin Panel"

msgid "老师后台"
msgstr "Teacher Panel"

msgid "关于"
msgstr "About"

msgid "登录"
msgstr "Login"

msgid "注册"
msgstr "Register"

msgid "个人资料"
msgstr "Profile"

msgid "登出"
msgstr "Logout"

msgid "联系我们"
msgstr "Contact Us"

msgid "隐私政策"
msgstr "Privacy Policy"

msgid "服务条款"
msgstr "Terms of Service"

msgid "语言设置"
msgstr "Language Settings"

msgid "当前语言"
msgstr "Current Language"

msgid "当前系统语言："
msgstr "Current system language: "
'''
    
    # 写入翻译文件
    translations = {
        'zh_CN': zh_cn_content,
        'zh_TW': zh_tw_content,
        'en': en_content
    }
    
    for lang, content in translations.items():
        po_file = f"app/translations/{lang}/LC_MESSAGES/messages.po"
        try:
            with open(po_file, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ 添加 {lang} 翻译内容")
        except Exception as e:
            print(f"❌ 添加 {lang} 翻译内容失败: {e}")
            return False
    
    print("\n🎉 翻译内容添加完成！")
    return True

if __name__ == "__main__":
    add_translations() 
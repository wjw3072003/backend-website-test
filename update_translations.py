#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
更新翻译内容脚本
"""

import os

def update_translations():
    """更新翻译内容"""
    
    print("📝 更新翻译内容...")
    
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

msgid "AiMusPal - AI音乐教育平台"
msgstr "AiMusPal - AI音乐教育平台"

msgid "智能音乐教育平台"
msgstr "智能音乐教育平台"

msgid "使用AI技术分析您的音乐练习，提供个性化反馈，让音乐学习更高效、更有趣。"
msgstr "使用AI技术分析您的音乐练习，提供个性化反馈，让音乐学习更高效、更有趣。"

msgid "立即注册"
msgstr "立即注册"

msgid "进入仪表板"
msgstr "进入仪表板"

msgid "开始练习"
msgstr "开始练习"

msgid "平台特色"
msgstr "平台特色"

msgid "AI驱动的音乐教育解决方案"
msgstr "AI驱动的音乐教育解决方案"

msgid "AI智能分析"
msgstr "AI智能分析"

msgid "先进的AI技术实时分析您的演奏，从节拍、音准、节奏等多个维度提供精准评估。"
msgstr "先进的AI技术实时分析您的演奏，从节拍、音准、节奏等多个维度提供精准评估。"

msgid "个性化反馈"
msgstr "个性化反馈"

msgid "根据您的演奏水平和学习进度，提供量身定制的练习建议和改进方案。"
msgstr "根据您的演奏水平和学习进度，提供量身定制的练习建议和改进方案。"

msgid "学习追踪"
msgstr "学习追踪"

msgid "详细记录您的学习历程，可视化展示进步轨迹，让每一次练习都有明确目标。"
msgstr "详细记录您的学习历程，可视化展示进步轨迹，让每一次练习都有明确目标。"

msgid "如何使用"
msgstr "如何使用"

msgid "简单三步，开启智能音乐学习之旅"
msgstr "简单三步，开启智能音乐学习之旅"

msgid "选择曲目"
msgstr "选择曲目"

msgid "从我们精心准备的曲库中选择适合您水平的练习曲目"
msgstr "从我们精心准备的曲库中选择适合您水平的练习曲目"

msgid "录制演奏"
msgstr "录制演奏"

msgid "使用手机或电脑录制您的演奏音频，上传到平台"
msgstr "使用手机或电脑录制您的演奏音频，上传到平台"

msgid "获得反馈"
msgstr "获得反馈"

msgid "AI分析完成后，获得详细的演奏评估和改进建议"
msgstr "AI分析完成后，获得详细的演奏评估和改进建议"

msgid "注册用户"
msgstr "注册用户"

msgid "练习记录"
msgstr "练习记录"

msgid "用户满意度"
msgstr "用户满意度"

msgid "准备开始您的音乐学习之旅了吗？"
msgstr "准备开始您的音乐学习之旅了吗？"

msgid "加入我们，体验AI驱动的个性化音乐教育"
msgstr "加入我们，体验AI驱动的个性化音乐教育"

msgid "免费注册"
msgstr "免费注册"

msgid "了解更多"
msgstr "了解更多"

msgid "注册新账户"
msgstr "注册新账户"

msgid "用户名"
msgstr "用户名"

msgid "邮箱"
msgstr "邮箱"

msgid "姓名"
msgstr "姓名"

msgid "姓氏"
msgstr "姓氏"

msgid "密码"
msgstr "密码"

msgid "确认密码"
msgstr "确认密码"

msgid "注册身份"
msgstr "注册身份"

msgid "学生"
msgstr "学生"

msgid "老师"
msgstr "老师"

msgid "是否有老师推荐码"
msgstr "是否有老师推荐码"

msgid "有推荐码"
msgstr "有推荐码"

msgid "无推荐码"
msgstr "无推荐码"

msgid "老师推荐码"
msgstr "老师推荐码"

msgid "提示："
msgstr "提示："

msgid "老师注册不需要推荐码，注册成功后系统会自动为您生成专属推广码。"
msgstr "老师注册不需要推荐码，注册成功后系统会自动为您生成专属推广码。"

msgid "记住我"
msgstr "记住我"

msgid "没有账户？"
msgstr "没有账户？"

msgid "忘记密码？"
msgstr "忘记密码？"

msgid "已有账户？"
msgstr "已有账户？"

msgid "学习仪表板"
msgstr "学习仪表板"

msgid "练习次数"
msgstr "练习次数"

msgid "练习时长"
msgstr "练习时长"

msgid "小时"
msgstr "小时"

msgid "平均分数"
msgstr "平均分数"

msgid "分"
msgstr "分"

msgid "本月目标"
msgstr "本月目标"

msgid "次"
msgstr "次"

msgid "最近练习记录"
msgstr "最近练习记录"

msgid "查看全部"
msgstr "查看全部"

msgid "练习时间"
msgstr "练习时间"

msgid "分数"
msgstr "分数"

msgid "状态"
msgstr "状态"

msgid "操作"
msgstr "操作"

msgid "已完成"
msgstr "已完成"

msgid "分析中"
msgstr "分析中"

msgid "失败"
msgstr "失败"

msgid "查看"
msgstr "查看"

msgid "还没有练习记录"
msgstr "还没有练习记录"

msgid "开始您的第一次练习吧！"
msgstr "开始您的第一次练习吧！"

msgid "学习目标"
msgstr "学习目标"

msgid "本月练习目标"
msgstr "本月练习目标"

msgid "已完成"
msgstr "已完成"

msgid "次练习"
msgstr "次练习"

msgid "本周推荐"
msgstr "本周推荐"

msgid "暂无推荐练习"
msgstr "暂无推荐练习"

msgid "浏览曲目"
msgstr "浏览曲目"

msgid "共"
msgstr "共"

msgid "首曲目"
msgstr "首曲目"

msgid "您已练习"
msgstr "您已练习"

msgid "我的记录"
msgstr "我的记录"

msgid "搜索"
msgstr "搜索"

msgid "按标题"
msgstr "按标题"

msgid "按难度"
msgstr "按难度"

msgid "最新添加"
msgstr "最新添加"

msgid "所有难度"
msgstr "所有难度"

msgid "难度"
msgstr "难度"

msgid "所有风格"
msgstr "所有风格"

msgid "清除所有筛选"
msgstr "清除所有筛选"

msgid "作曲家"
msgstr "作曲家"

msgid "风格"
msgstr "风格"

msgid "已练习"
msgstr "已练习"

msgid "最佳"
msgstr "最佳"

msgid "查看详情"
msgstr "查看详情"

msgid "上一页"
msgstr "上一页"

msgid "下一页"
msgstr "下一页"

msgid "未找到匹配的练习曲目"
msgstr "未找到匹配的练习曲目"

msgid "没有找到符合当前筛选条件的曲目，试试调整搜索条件"
msgstr "没有找到符合当前筛选条件的曲目，试试调整搜索条件"

msgid "清除筛选条件"
msgstr "清除筛选条件"

msgid "管理员还未添加练习曲目，请稍后再来查看。"
msgstr "管理员还未添加练习曲目，请稍后再来查看。"
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

msgid "AiMusPal - AI音乐教育平台"
msgstr "AiMusPal - AI音樂教育平台"

msgid "智能音乐教育平台"
msgstr "智能音樂教育平台"

msgid "使用AI技术分析您的音乐练习，提供个性化反馈，让音乐学习更高效、更有趣。"
msgstr "使用AI技術分析您的音樂練習，提供個性化反饋，讓音樂學習更高效、更有趣。"

msgid "立即注册"
msgstr "立即註冊"

msgid "进入仪表板"
msgstr "進入儀表板"

msgid "开始练习"
msgstr "開始練習"

msgid "平台特色"
msgstr "平台特色"

msgid "AI驱动的音乐教育解决方案"
msgstr "AI驅動的音樂教育解決方案"

msgid "AI智能分析"
msgstr "AI智能分析"

msgid "先进的AI技术实时分析您的演奏，从节拍、音准、节奏等多个维度提供精准评估。"
msgstr "先進的AI技術實時分析您的演奏，從節拍、音準、節奏等多個維度提供精準評估。"

msgid "个性化反馈"
msgstr "個性化反饋"

msgid "根据您的演奏水平和学习进度，提供量身定制的练习建议和改进方案。"
msgstr "根據您的演奏水平和學習進度，提供量身定制的練習建議和改進方案。"

msgid "学习追踪"
msgstr "學習追蹤"

msgid "详细记录您的学习历程，可视化展示进步轨迹，让每一次练习都有明确目标。"
msgstr "詳細記錄您的學習歷程，可視化展示進步軌跡，讓每一次練習都有明確目標。"

msgid "如何使用"
msgstr "如何使用"

msgid "简单三步，开启智能音乐学习之旅"
msgstr "簡單三步，開啟智能音樂學習之旅"

msgid "选择曲目"
msgstr "選擇曲目"

msgid "从我们精心准备的曲库中选择适合您水平的练习曲目"
msgstr "從我們精心準備的曲庫中選擇適合您水平的練習曲目"

msgid "录制演奏"
msgstr "錄製演奏"

msgid "使用手机或电脑录制您的演奏音频，上传到平台"
msgstr "使用手機或電腦錄製您的演奏音頻，上傳到平台"

msgid "获得反馈"
msgstr "獲得反饋"

msgid "AI分析完成后，获得详细的演奏评估和改进建议"
msgstr "AI分析完成後，獲得詳細的演奏評估和改進建議"

msgid "注册用户"
msgstr "註冊用戶"

msgid "练习记录"
msgstr "練習記錄"

msgid "用户满意度"
msgstr "用戶滿意度"

msgid "准备开始您的音乐学习之旅了吗？"
msgstr "準備開始您的音樂學習之旅了嗎？"

msgid "加入我们，体验AI驱动的个性化音乐教育"
msgstr "加入我們，體驗AI驅動的個性化音樂教育"

msgid "免费注册"
msgstr "免費註冊"

msgid "了解更多"
msgstr "了解更多"

msgid "注册新账户"
msgstr "註冊新賬戶"

msgid "用户名"
msgstr "用戶名"

msgid "邮箱"
msgstr "郵箱"

msgid "姓名"
msgstr "姓名"

msgid "姓氏"
msgstr "姓氏"

msgid "密码"
msgstr "密碼"

msgid "确认密码"
msgstr "確認密碼"

msgid "注册身份"
msgstr "註冊身份"

msgid "学生"
msgstr "學生"

msgid "老师"
msgstr "老師"

msgid "是否有老师推荐码"
msgstr "是否有老師推薦碼"

msgid "有推荐码"
msgstr "有推薦碼"

msgid "无推荐码"
msgstr "無推薦碼"

msgid "老师推荐码"
msgstr "老師推薦碼"

msgid "提示："
msgstr "提示："

msgid "老师注册不需要推荐码，注册成功后系统会自动为您生成专属推广码。"
msgstr "老師註冊不需要推薦碼，註冊成功後系統會自動為您生成專屬推廣碼。"

msgid "记住我"
msgstr "記住我"

msgid "没有账户？"
msgstr "沒有賬戶？"

msgid "忘记密码？"
msgstr "忘記密碼？"

msgid "已有账户？"
msgstr "已有賬戶？"

msgid "学习仪表板"
msgstr "學習儀表板"

msgid "练习次数"
msgstr "練習次數"

msgid "练习时长"
msgstr "練習時長"

msgid "小时"
msgstr "小時"

msgid "平均分数"
msgstr "平均分數"

msgid "分"
msgstr "分"

msgid "本月目标"
msgstr "本月目標"

msgid "次"
msgstr "次"

msgid "最近练习记录"
msgstr "最近練習記錄"

msgid "查看全部"
msgstr "查看全部"

msgid "练习时间"
msgstr "練習時間"

msgid "分数"
msgstr "分數"

msgid "状态"
msgstr "狀態"

msgid "操作"
msgstr "操作"

msgid "已完成"
msgstr "已完成"

msgid "分析中"
msgstr "分析中"

msgid "失败"
msgstr "失敗"

msgid "查看"
msgstr "查看"

msgid "还没有练习记录"
msgstr "還沒有練習記錄"

msgid "开始您的第一次练习吧！"
msgstr "開始您的第一次練習吧！"

msgid "学习目标"
msgstr "學習目標"

msgid "本月练习目标"
msgstr "本月練習目標"

msgid "已完成"
msgstr "已完成"

msgid "次练习"
msgstr "次練習"

msgid "本周推荐"
msgstr "本週推薦"

msgid "暂无推荐练习"
msgstr "暫無推薦練習"

msgid "浏览曲目"
msgstr "瀏覽曲目"

msgid "共"
msgstr "共"

msgid "首曲目"
msgstr "首曲目"

msgid "您已练习"
msgstr "您已練習"

msgid "我的记录"
msgstr "我的記錄"

msgid "搜索"
msgstr "搜索"

msgid "按标题"
msgstr "按標題"

msgid "按难度"
msgstr "按難度"

msgid "最新添加"
msgstr "最新添加"

msgid "所有难度"
msgstr "所有難度"

msgid "难度"
msgstr "難度"

msgid "所有风格"
msgstr "所有風格"

msgid "清除所有筛选"
msgstr "清除所有篩選"

msgid "作曲家"
msgstr "作曲家"

msgid "风格"
msgstr "風格"

msgid "已练习"
msgstr "已練習"

msgid "最佳"
msgstr "最佳"

msgid "查看详情"
msgstr "查看詳情"

msgid "上一页"
msgstr "上一頁"

msgid "下一页"
msgstr "下一頁"

msgid "未找到匹配的练习曲目"
msgstr "未找到匹配的練習曲目"

msgid "没有找到符合当前筛选条件的曲目，试试调整搜索条件"
msgstr "沒有找到符合當前篩選條件的曲目，試試調整搜索條件"

msgid "清除筛选条件"
msgstr "清除篩選條件"

msgid "管理员还未添加练习曲目，请稍后再来查看。"
msgstr "管理員還未添加練習曲目，請稍後再來查看。"
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

msgid "AiMusPal - AI音乐教育平台"
msgstr "AiMusPal - AI Music Education Platform"

msgid "智能音乐教育平台"
msgstr "Intelligent Music Education Platform"

msgid "使用AI技术分析您的音乐练习，提供个性化反馈，让音乐学习更高效、更有趣。"
msgstr "Use AI technology to analyze your music practice, provide personalized feedback, making music learning more efficient and enjoyable."

msgid "立即注册"
msgstr "Register Now"

msgid "进入仪表板"
msgstr "Enter Dashboard"

msgid "开始练习"
msgstr "Start Practice"

msgid "平台特色"
msgstr "Platform Features"

msgid "AI驱动的音乐教育解决方案"
msgstr "AI-Driven Music Education Solution"

msgid "AI智能分析"
msgstr "AI Intelligent Analysis"

msgid "先进的AI技术实时分析您的演奏，从节拍、音准、节奏等多个维度提供精准评估。"
msgstr "Advanced AI technology analyzes your performance in real-time, providing precise evaluation from multiple dimensions including tempo, pitch, and rhythm."

msgid "个性化反馈"
msgstr "Personalized Feedback"

msgid "根据您的演奏水平和学习进度，提供量身定制的练习建议和改进方案。"
msgstr "Provide tailored practice suggestions and improvement plans based on your performance level and learning progress."

msgid "学习追踪"
msgstr "Learning Tracking"

msgid "详细记录您的学习历程，可视化展示进步轨迹，让每一次练习都有明确目标。"
msgstr "Detailed recording of your learning journey, visual display of progress trajectory, making every practice session have clear goals."

msgid "如何使用"
msgstr "How to Use"

msgid "简单三步，开启智能音乐学习之旅"
msgstr "Simple three steps to start your intelligent music learning journey"

msgid "选择曲目"
msgstr "Choose Pieces"

msgid "从我们精心准备的曲库中选择适合您水平的练习曲目"
msgstr "Choose practice pieces suitable for your level from our carefully prepared repertoire"

msgid "录制演奏"
msgstr "Record Performance"

msgid "使用手机或电脑录制您的演奏音频，上传到平台"
msgstr "Use your phone or computer to record your performance audio and upload to the platform"

msgid "获得反馈"
msgstr "Get Feedback"

msgid "AI分析完成后，获得详细的演奏评估和改进建议"
msgstr "After AI analysis is complete, receive detailed performance evaluation and improvement suggestions"

msgid "注册用户"
msgstr "Registered Users"

msgid "练习记录"
msgstr "Practice Records"

msgid "用户满意度"
msgstr "User Satisfaction"

msgid "准备开始您的音乐学习之旅了吗？"
msgstr "Ready to start your music learning journey?"

msgid "加入我们，体验AI驱动的个性化音乐教育"
msgstr "Join us and experience AI-driven personalized music education"

msgid "免费注册"
msgstr "Free Registration"

msgid "了解更多"
msgstr "Learn More"

msgid "注册新账户"
msgstr "Register New Account"

msgid "用户名"
msgstr "Username"

msgid "邮箱"
msgstr "Email"

msgid "姓名"
msgstr "First Name"

msgid "姓氏"
msgstr "Last Name"

msgid "密码"
msgstr "Password"

msgid "确认密码"
msgstr "Confirm Password"

msgid "注册身份"
msgstr "Registration Type"

msgid "学生"
msgstr "Student"

msgid "老师"
msgstr "Teacher"

msgid "是否有老师推荐码"
msgstr "Do you have a teacher referral code?"

msgid "有推荐码"
msgstr "Have referral code"

msgid "无推荐码"
msgstr "No referral code"

msgid "老师推荐码"
msgstr "Teacher Referral Code"

msgid "提示："
msgstr "Note: "

msgid "老师注册不需要推荐码，注册成功后系统会自动为您生成专属推广码。"
msgstr "Teachers don't need referral codes for registration. After successful registration, the system will automatically generate a unique promotion code for you."

msgid "记住我"
msgstr "Remember Me"

msgid "没有账户？"
msgstr "Don't have an account? "

msgid "忘记密码？"
msgstr "Forgot password?"

msgid "已有账户？"
msgstr "Already have an account? "

msgid "学习仪表板"
msgstr "Learning Dashboard"

msgid "练习次数"
msgstr "Practice Count"

msgid "练习时长"
msgstr "Practice Duration"

msgid "小时"
msgstr "hours"

msgid "平均分数"
msgstr "Average Score"

msgid "分"
msgstr "pts"

msgid "本月目标"
msgstr "Monthly Goal"

msgid "次"
msgstr "times"

msgid "最近练习记录"
msgstr "Recent Practice Records"

msgid "查看全部"
msgstr "View All"

msgid "练习时间"
msgstr "Practice Time"

msgid "分数"
msgstr "Score"

msgid "状态"
msgstr "Status"

msgid "操作"
msgstr "Actions"

msgid "已完成"
msgstr "Completed"

msgid "分析中"
msgstr "Analyzing"

msgid "失败"
msgstr "Failed"

msgid "查看"
msgstr "View"

msgid "还没有练习记录"
msgstr "No practice records yet"

msgid "开始您的第一次练习吧！"
msgstr "Start your first practice session!"

msgid "学习目标"
msgstr "Learning Goals"

msgid "本月练习目标"
msgstr "Monthly Practice Goal"

msgid "已完成"
msgstr "Completed"

msgid "次练习"
msgstr "practice sessions"

msgid "本周推荐"
msgstr "This Week's Recommendations"

msgid "暂无推荐练习"
msgstr "No recommended practices"

msgid "浏览曲目"
msgstr "Browse Pieces"

msgid "共"
msgstr "Total"

msgid "首曲目"
msgstr "pieces"

msgid "您已练习"
msgstr "You have practiced"

msgid "我的记录"
msgstr "My Records"

msgid "搜索"
msgstr "Search"

msgid "按标题"
msgstr "By Title"

msgid "按难度"
msgstr "By Difficulty"

msgid "最新添加"
msgstr "Recently Added"

msgid "所有难度"
msgstr "All Difficulties"

msgid "难度"
msgstr "Difficulty"

msgid "所有风格"
msgstr "All Genres"

msgid "清除所有筛选"
msgstr "Clear All Filters"

msgid "作曲家"
msgstr "Composer"

msgid "风格"
msgstr "Genre"

msgid "已练习"
msgstr "Practiced"

msgid "最佳"
msgstr "Best"

msgid "查看详情"
msgstr "View Details"

msgid "上一页"
msgstr "Previous"

msgid "下一页"
msgstr "Next"

msgid "未找到匹配的练习曲目"
msgstr "No matching practice pieces found"

msgid "没有找到符合当前筛选条件的曲目，试试调整搜索条件"
msgstr "No pieces found matching current filters, try adjusting search criteria"

msgid "清除筛选条件"
msgstr "Clear Filters"

msgid "管理员还未添加练习曲目，请稍后再来查看。"
msgstr "Administrator hasn't added practice pieces yet, please check back later."
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
            print(f"✅ 更新 {lang} 翻译内容")
        except Exception as e:
            print(f"❌ 更新 {lang} 翻译内容失败: {e}")
            return False
    
    print("\n🎉 翻译内容更新完成！")
    return True

if __name__ == "__main__":
    update_translations() 
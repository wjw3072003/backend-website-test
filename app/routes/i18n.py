# -*- coding: utf-8 -*-
"""
国际化路由
处理语言切换功能
"""

from flask import Blueprint, request, session, redirect, url_for, flash
from flask_login import current_user
from app import db
from app.models.user import User

i18n = Blueprint('i18n', __name__)

@i18n.route('/set_language/<language>')
def set_language(language):
    """设置语言"""
    # 支持的语言列表
    supported_languages = ['zh_CN', 'zh_TW', 'en']
    
    if language not in supported_languages:
        flash('不支持的语言', 'error')
        return redirect(request.referrer or url_for('main.index'))
    
    # 保存到session
    session['lang'] = language
    
    # 如果用户已登录，保存到用户设置
    if current_user.is_authenticated:
        try:
            current_user.language = language
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            flash('保存语言设置失败', 'error')
    
    # 返回上一页或首页
    return redirect(request.referrer or url_for('main.index'))

@i18n.route('/language')
def language_info():
    """语言信息页面"""
    from flask import render_template
    return render_template('i18n/language_info.html') 
from functools import wraps
from flask import abort, flash, redirect, url_for, request, jsonify
from flask_login import current_user

def roles_required(*roles):
    """角色权限装饰器"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                if request.is_json:
                    return jsonify({'error': '请先登录'}), 401
                flash('请先登录', 'error')
                return redirect(url_for('auth.login'))
            
            # 检查用户是否有任何一个要求的角色
            user_roles = [role.name for role in current_user.roles]
            if not any(role in user_roles for role in roles):
                if request.is_json:
                    return jsonify({'error': '权限不足'}), 403
                flash('权限不足', 'error')
                abort(403)
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def verified_required(f):
    """邮箱验证装饰器"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            if request.is_json:
                return jsonify({'error': '请先登录'}), 401
            flash('请先登录', 'error')
            return redirect(url_for('auth.login'))
        
        if not current_user.is_verified:
            if request.is_json:
                return jsonify({'error': '请先验证邮箱'}), 403
            flash('请先验证邮箱', 'warning')
            return redirect(url_for('auth.profile'))
        
        return f(*args, **kwargs)
    return decorated_function

def active_required(f):
    """账户激活装饰器"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            if request.is_json:
                return jsonify({'error': '请先登录'}), 401
            flash('请先登录', 'error')
            return redirect(url_for('auth.login'))
        
        if not current_user.is_active:
            if request.is_json:
                return jsonify({'error': '账户已被禁用'}), 403
            flash('您的账户已被禁用，请联系管理员', 'error')
            return redirect(url_for('main.index'))
        
        return f(*args, **kwargs)
    return decorated_function
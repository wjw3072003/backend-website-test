from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash
import uuid
from datetime import datetime

from app import db
from app.models.user import User, Role
from app.utils.email import send_verification_email
from app.utils.decorators import roles_required

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    """用户注册"""
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        
        email = data.get('email', '').strip().lower()
        username = data.get('username', '').strip()
        password = data.get('password', '')
        user_type = data.get('user_type', 'student')  # student or teacher
        
        # 验证输入
        if not email or not username or not password:
            message = '请填写所有必填字段'
            if request.is_json:
                return jsonify({'error': message}), 400
            flash(message, 'error')
            return render_template('auth/register.html')
        
        # 检查用户是否已存在
        if User.query.filter_by(email=email).first():
            message = '该邮箱已被注册'
            if request.is_json:
                return jsonify({'error': message}), 400
            flash(message, 'error')
            return render_template('auth/register.html')
        
        if User.query.filter_by(username=username).first():
            message = '该用户名已被使用'
            if request.is_json:
                return jsonify({'error': message}), 400
            flash(message, 'error')
            return render_template('auth/register.html')
        
        try:
            # 创建新用户
            user = User(
                email=email,
                username=username,
                password=password,
                verification_token=str(uuid.uuid4())
            )
            
            # 分配角色
            if user_type == 'teacher':
                role = Role.query.filter_by(name='teacher').first()
            else:
                role = Role.query.filter_by(name='student').first()
            
            if role:
                user.add_role(role)
            
            db.session.add(user)
            db.session.commit()
            
            # 发送验证邮件
            send_verification_email(user)
            
            message = '注册成功！请查看邮箱完成验证。'
            if request.is_json:
                return jsonify({'message': message, 'user_id': user.id}), 201
            
            flash(message, 'success')
            return redirect(url_for('auth.login'))
            
        except Exception as e:
            db.session.rollback()
            message = '注册失败，请稍后重试'
            if request.is_json:
                return jsonify({'error': message}), 500
            flash(message, 'error')
    
    return render_template('auth/register.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    """用户登录"""
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        remember = data.get('remember', False)
        
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            if not user.is_active:
                message = '账户已被禁用'
                if request.is_json:
                    return jsonify({'error': message}), 403
                flash(message, 'error')
                return render_template('auth/login.html')
            
            # 更新最后登录时间
            user.last_login = datetime.utcnow()
            db.session.commit()
            
            login_user(user, remember=remember)
            
            if request.is_json:
                return jsonify({
                    'message': '登录成功',
                    'user': user.to_dict(),
                    'redirect_url': url_for('main.dashboard')
                }), 200
            
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            return redirect(url_for('main.dashboard'))
        else:
            message = '邮箱或密码错误'
            if request.is_json:
                return jsonify({'error': message}), 401
            flash(message, 'error')
    
    return render_template('auth/login.html')

@auth.route('/logout')
@login_required
def logout():
    """用户登出"""
    logout_user()
    flash('您已成功登出', 'info')
    return redirect(url_for('main.index'))

@auth.route('/verify/<token>')
def verify_email(token):
    """邮箱验证"""
    user = User.query.filter_by(verification_token=token).first()
    
    if not user:
        flash('验证链接无效', 'error')
        return redirect(url_for('main.index'))
    
    user.is_verified = True
    user.verification_token = None
    db.session.commit()
    
    flash('邮箱验证成功！', 'success')
    return redirect(url_for('auth.login'))

@auth.route('/profile')
@login_required
def profile():
    """用户个人资料"""
    return render_template('auth/profile.html', user=current_user)

@auth.route('/profile', methods=['POST'])
@login_required
def update_profile():
    """更新用户个人资料"""
    data = request.get_json() if request.is_json else request.form
    
    current_user.first_name = data.get('first_name', '').strip()
    current_user.last_name = data.get('last_name', '').strip()
    current_user.phone = data.get('phone', '').strip()
    
    try:
        db.session.commit()
        message = '个人资料更新成功'
        if request.is_json:
            return jsonify({'message': message, 'user': current_user.to_dict()}), 200
        flash(message, 'success')
    except Exception as e:
        db.session.rollback()
        message = '更新失败，请稍后重试'
        if request.is_json:
            return jsonify({'error': message}), 500
        flash(message, 'error')
    
    return redirect(url_for('auth.profile'))
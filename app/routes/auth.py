from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash
import uuid
from datetime import datetime

from app import db
from app.models.user import User, Role
from app.models.auth import PasswordResetToken
from app.utils.email import send_verification_email, send_password_reset_email
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

@auth.route('/change-password', methods=['POST'])
@login_required
def change_password():
    """修改密码"""
    data = request.get_json() if request.is_json else request.form
    
    current_password = data.get('current_password', '')
    new_password = data.get('new_password', '')
    confirm_password = data.get('confirm_password', '')
    
    # 验证输入
    if not current_password or not new_password or not confirm_password:
        message = '请填写所有密码字段'
        if request.is_json:
            return jsonify({'error': message}), 400
        flash(message, 'error')
        return redirect(url_for('auth.profile'))
    
    # 验证当前密码
    if not current_user.check_password(current_password):
        message = '当前密码错误'
        if request.is_json:
            return jsonify({'error': message}), 400
        flash(message, 'error')
        return redirect(url_for('auth.profile'))
    
    # 验证新密码
    if len(new_password) < 6:
        message = '新密码长度至少6位'
        if request.is_json:
            return jsonify({'error': message}), 400
        flash(message, 'error')
        return redirect(url_for('auth.profile'))
    
    if new_password != confirm_password:
        message = '两次输入的新密码不一致'
        if request.is_json:
            return jsonify({'error': message}), 400
        flash(message, 'error')
        return redirect(url_for('auth.profile'))
    
    try:
        # 更新密码
        current_user.password_hash = generate_password_hash(new_password)
        db.session.commit()
        
        message = '密码修改成功'
        if request.is_json:
            return jsonify({'message': message}), 200
        flash(message, 'success')
    except Exception as e:
        db.session.rollback()
        message = '密码修改失败，请稍后重试'
        if request.is_json:
            return jsonify({'error': message}), 500
        flash(message, 'error')
    
    return redirect(url_for('auth.profile'))

@auth.route('/upload-avatar', methods=['POST'])
@login_required
def upload_avatar():
    """上传头像"""
    if 'avatar_file' not in request.files:
        return jsonify({'success': False, 'error': '请选择头像文件'}), 400
    
    file = request.files['avatar_file']
    if file.filename == '':
        return jsonify({'success': False, 'error': '请选择头像文件'}), 400
    
    try:
        from app.utils.file_handler import save_avatar_file, delete_file
        from flask import current_app
        import os
        
        # 删除旧头像
        if current_user.avatar:
            old_avatar_path = os.path.join(current_app.config['UPLOAD_FOLDER'], current_user.avatar)
            delete_file(old_avatar_path)
        
        # 保存新头像
        avatar_filename = save_avatar_file(file, current_user.id)
        
        # 更新用户头像信息
        current_user.avatar = avatar_filename
        db.session.commit()
        
        return jsonify({
            'success': True, 
            'message': '头像上传成功！',
            'avatar_url': f"/static/uploads/{avatar_filename}"
        }), 200
        
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': '头像上传失败，请稍后重试'}), 500

@auth.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    """忘记密码"""
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        email = data.get('email', '').strip().lower()
        
        if not email:
            message = '请输入邮箱地址'
            if request.is_json:
                return jsonify({'error': message}), 400
            flash(message, 'error')
            return render_template('auth/forgot_password.html')
        
        user = User.query.filter_by(email=email).first()
        
        if user:
            # 创建重置令牌
            reset_token = PasswordResetToken.create_token(user)
            
            # 发送重置邮件
            try:
                send_password_reset_email(user, reset_token.token)
                message = '密码重置邮件已发送，请查看您的邮箱'
                if request.is_json:
                    return jsonify({'message': message}), 200
                flash(message, 'success')
            except Exception as e:
                message = '邮件发送失败，请稍后重试'
                if request.is_json:
                    return jsonify({'error': message}), 500
                flash(message, 'error')
        else:
            # 即使用户不存在也显示成功消息，防止邮箱枚举攻击
            message = '如果邮箱存在，密码重置邮件已发送'
            if request.is_json:
                return jsonify({'message': message}), 200
            flash(message, 'info')
        
        return redirect(url_for('auth.login'))
    
    return render_template('auth/forgot_password.html')

@auth.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    """重置密码"""
    reset_token = PasswordResetToken.verify_token(token)
    
    if not reset_token:
        flash('重置链接无效或已过期', 'error')
        return redirect(url_for('auth.forgot_password'))
    
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        password = data.get('password', '')
        password_confirm = data.get('password_confirm', '')
        
        if not password or len(password) < 6:
            message = '密码长度至少6位'
            if request.is_json:
                return jsonify({'error': message}), 400
            flash(message, 'error')
            return render_template('auth/reset_password.html', token=token)
        
        if password != password_confirm:
            message = '两次输入的密码不一致'
            if request.is_json:
                return jsonify({'error': message}), 400
            flash(message, 'error')
            return render_template('auth/reset_password.html', token=token)
        
        try:
            # 更新用户密码
            user = reset_token.user
            user.set_password(password)
            
            # 标记令牌为已使用
            reset_token.mark_as_used()
            
            db.session.commit()
            
            message = '密码重置成功，请使用新密码登录'
            if request.is_json:
                return jsonify({'message': message}), 200
            
            flash(message, 'success')
            return redirect(url_for('auth.login'))
            
        except Exception as e:
            db.session.rollback()
            message = '密码重置失败，请稍后重试'
            if request.is_json:
                return jsonify({'error': message}), 500
            flash(message, 'error')
    
    return render_template('auth/reset_password.html', token=token)
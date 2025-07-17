from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from datetime import datetime, timedelta

from app import db
from app.models.user import User, Role
from app.models.practice import Practice, PracticeRecord, AudioFile
from app.utils.decorators import roles_required

admin = Blueprint('admin', __name__)

@admin.route('/')
@login_required
@roles_required('admin', 'teacher')
def dashboard():
    """管理员仪表板"""
    # 基本统计数据
    total_users = User.query.count()
    total_students = User.query.join(User.roles).filter(Role.name == 'student').count()
    total_teachers = User.query.join(User.roles).filter(Role.name == 'teacher').count()
    total_practices = Practice.query.count()
    total_records = PracticeRecord.query.count()
    
    # 时间范围统计
    now = datetime.utcnow()
    seven_days_ago = now - timedelta(days=7)
    thirty_days_ago = now - timedelta(days=30)
    this_month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    
    # 最近活动统计
    new_users_week = User.query.filter(User.created_at >= seven_days_ago).count()
    new_records_week = PracticeRecord.query.filter(PracticeRecord.created_at >= seven_days_ago).count()
    monthly_records = PracticeRecord.query.filter(PracticeRecord.created_at >= this_month_start).count()
    
    # 最新用户（最近注册的5个）
    recent_users = User.query.order_by(User.created_at.desc()).limit(5).all()
    
    # 练习趋势数据（最近30天每天的练习记录数）
    trend_data = []
    for i in range(30):
        day_start = (now - timedelta(days=i)).replace(hour=0, minute=0, second=0, microsecond=0)
        day_end = day_start + timedelta(days=1)
        day_count = PracticeRecord.query.filter(
            PracticeRecord.created_at >= day_start,
            PracticeRecord.created_at < day_end
        ).count()
        trend_data.append({
            'date': day_start.strftime('%m-%d'),
            'count': day_count
        })
    
    # 反转数据，使最早的日期在前面
    trend_data.reverse()
    
    # 热门练习曲目（按练习次数排序）
    popular_practices = db.session.query(
        Practice.title,
        db.func.count(PracticeRecord.id).label('practice_count')
    ).join(PracticeRecord).group_by(Practice.id).order_by(
        db.desc('practice_count')
    ).limit(5).all()
    
    stats = {
        'total_users': total_users,
        'total_students': total_students,
        'total_teachers': total_teachers,
        'total_practices': total_practices,
        'total_records': total_records,
        'new_users_week': new_users_week,
        'new_records_week': new_records_week,
        'monthly_records': monthly_records,
        'recent_users': recent_users,
        'trend_data': trend_data,
        'popular_practices': popular_practices
    }
    
    return render_template('admin/dashboard.html', stats=stats)

@admin.route('/export/<export_type>')
@login_required
@roles_required('admin')
def export_data(export_type):
    """数据导出功能"""
    from flask import make_response
    import csv
    import io
    
    # 创建CSV内容
    output = io.StringIO()
    writer = csv.writer(output)
    
    if export_type == 'users':
        # 导出用户数据
        writer.writerow(['ID', '用户名', '邮箱', '姓名', '角色', '状态', '注册时间', '最后登录'])
        users = User.query.all()
        for user in users:
            roles = ', '.join([role.name for role in user.roles])
            status = '激活' if user.is_active else '禁用'
            writer.writerow([
                user.id,
                user.username,
                user.email,
                f"{user.first_name or ''} {user.last_name or ''}".strip(),
                roles,
                status,
                user.created_at.strftime('%Y-%m-%d %H:%M') if user.created_at else '',
                user.last_login.strftime('%Y-%m-%d %H:%M') if user.last_login else ''
            ])
        filename = 'users_export.csv'
        
    elif export_type == 'practices':
        # 导出练习曲目数据
        writer.writerow(['ID', '标题', '作曲家', '难度', '风格', '状态', '练习次数', '创建时间'])
        practices = Practice.query.all()
        for practice in practices:
            practice_count = PracticeRecord.query.filter_by(practice_id=practice.id).count()
            status = '激活' if practice.is_active else '禁用'
            writer.writerow([
                practice.id,
                practice.title,
                practice.composer or '',
                practice.difficulty_level,
                practice.genre or '',
                status,
                practice_count,
                practice.created_at.strftime('%Y-%m-%d %H:%M') if practice.created_at else ''
            ])
        filename = 'practices_export.csv'
        
    elif export_type == 'records':
        # 导出练习记录数据
        writer.writerow(['ID', '用户', '练习曲目', '分数', '节拍准确度', '音高准确度', '节奏准确度', '状态', '练习时间'])
        records = PracticeRecord.query.join(User).join(Practice).all()
        for record in records:
            writer.writerow([
                record.id,
                record.user.username,
                record.practice.title,
                record.score or '',
                record.tempo_accuracy or '',
                record.pitch_accuracy or '',
                record.rhythm_accuracy or '',
                record.status,
                record.created_at.strftime('%Y-%m-%d %H:%M') if record.created_at else ''
            ])
        filename = 'practice_records_export.csv'
        
    else:
        flash('无效的导出类型', 'error')
        return redirect(url_for('admin.dashboard'))
    
    # 创建响应
    response = make_response(output.getvalue())
    response.headers['Content-Type'] = 'text/csv; charset=utf-8'
    response.headers['Content-Disposition'] = f'attachment; filename={filename}'
    
    return response

# 用户管理
@admin.route('/users')
@login_required
@roles_required('admin')
def users():
    """用户管理页面"""
    page = request.args.get('page', 1, type=int)
    per_page = 20
    
    search = request.args.get('search', '')
    role_filter = request.args.get('role', '')
    
    query = User.query
    
    if search:
        query = query.filter(
            db.or_(
                User.username.contains(search),
                User.email.contains(search),
                User.first_name.contains(search),
                User.last_name.contains(search)
            )
        )
    
    if role_filter:
        query = query.join(User.roles).filter(Role.name == role_filter)
    
    users = query.order_by(User.created_at.desc())\
        .paginate(page=page, per_page=per_page, error_out=False)
    
    roles = Role.query.all()
    
    return render_template('admin/users.html', users=users, roles=roles, 
                         search=search, role_filter=role_filter)

@admin.route('/users/new', methods=['GET', 'POST'])
@login_required
@roles_required('admin')
def new_user():
    """添加新用户"""
    roles = Role.query.all()
    
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        
        # 验证必填字段
        email = data.get('email', '').strip().lower()
        username = data.get('username', '').strip()
        password = data.get('password', '').strip()
        
        if not email or not username or not password:
            message = '邮箱、用户名和密码都是必填项'
            if request.is_json:
                return jsonify({'error': message}), 400
            flash(message, 'error')
            return render_template('admin/user_form.html', roles=roles, user=None)
        
        # 检查邮箱和用户名是否已存在
        if User.query.filter_by(email=email).first():
            message = '该邮箱已被注册'
            if request.is_json:
                return jsonify({'error': message}), 400
            flash(message, 'error')
            return render_template('admin/user_form.html', roles=roles, user=None)
            
        if User.query.filter_by(username=username).first():
            message = '该用户名已被注册'
            if request.is_json:
                return jsonify({'error': message}), 400
            flash(message, 'error')
            return render_template('admin/user_form.html', roles=roles, user=None)
        
        try:
            # 创建新用户
            user = User(
                email=email,
                username=username,
                password=password
            )
            
            # 设置其他信息
            user.first_name = data.get('first_name', '').strip()
            user.last_name = data.get('last_name', '').strip()
            user.phone = data.get('phone', '').strip()
            user.is_active = data.get('is_active') == 'on' or data.get('is_active') == True
            user.is_verified = data.get('is_verified') == 'on' or data.get('is_verified') == True
            
            db.session.add(user)
            db.session.flush()  # 获取用户ID
            
            # 分配角色
            role_ids = data.getlist('roles') if hasattr(data, 'getlist') else data.get('roles', [])
            if isinstance(role_ids, str):
                role_ids = [role_ids]
                
            for role_id in role_ids:
                role = Role.query.get(role_id)
                if role:
                    user.add_role(role)
            
            # 如果没有分配角色，默认为学生
            if not user.roles:
                student_role = Role.query.filter_by(name='student').first()
                if student_role:
                    user.add_role(student_role)
            
            db.session.commit()
            
            message = f'用户 {username} 创建成功'
            if request.is_json:
                return jsonify({'message': message, 'user_id': user.id}), 201
            
            flash(message, 'success')
            return redirect(url_for('admin.user_detail', user_id=user.id))
            
        except Exception as e:
            db.session.rollback()
            message = '创建用户失败，请稍后重试'
            if request.is_json:
                return jsonify({'error': message}), 500
            flash(message, 'error')
            return render_template('admin/user_form.html', roles=roles, user=None)
    
    return render_template('admin/user_form.html', roles=roles, user=None)

@admin.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
@login_required
@roles_required('admin')
def edit_user(user_id):
    """编辑用户"""
    user = User.query.get_or_404(user_id)
    roles = Role.query.all()
    
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        
        # 验证必填字段
        email = data.get('email', '').strip().lower()
        username = data.get('username', '').strip()
        
        if not email or not username:
            message = '邮箱和用户名都是必填项'
            if request.is_json:
                return jsonify({'error': message}), 400
            flash(message, 'error')
            return render_template('admin/user_form.html', roles=roles, user=user)
        
        # 检查邮箱和用户名是否被其他用户使用
        email_user = User.query.filter_by(email=email).first()
        if email_user and email_user.id != user.id:
            message = '该邮箱已被其他用户使用'
            if request.is_json:
                return jsonify({'error': message}), 400
            flash(message, 'error')
            return render_template('admin/user_form.html', roles=roles, user=user)
            
        username_user = User.query.filter_by(username=username).first()
        if username_user and username_user.id != user.id:
            message = '该用户名已被其他用户使用'
            if request.is_json:
                return jsonify({'error': message}), 400
            flash(message, 'error')
            return render_template('admin/user_form.html', roles=roles, user=user)
        
        try:
            # 更新用户信息
            user.email = email
            user.username = username
            user.first_name = data.get('first_name', '').strip()
            user.last_name = data.get('last_name', '').strip()
            user.phone = data.get('phone', '').strip()
            user.is_active = data.get('is_active') == 'on' or data.get('is_active') == True
            user.is_verified = data.get('is_verified') == 'on' or data.get('is_verified') == True
            
            # 更新密码（如果提供）
            new_password = data.get('password', '').strip()
            if new_password:
                user.set_password(new_password)
            
            # 更新角色
            user.roles.clear()
            role_ids = data.getlist('roles') if hasattr(data, 'getlist') else data.get('roles', [])
            if isinstance(role_ids, str):
                role_ids = [role_ids]
                
            for role_id in role_ids:
                role = Role.query.get(role_id)
                if role:
                    user.add_role(role)
            
            user.updated_at = datetime.utcnow()
            db.session.commit()
            
            message = f'用户 {username} 更新成功'
            if request.is_json:
                return jsonify({'message': message}), 200
            
            flash(message, 'success')
            return redirect(url_for('admin.user_detail', user_id=user.id))
            
        except Exception as e:
            db.session.rollback()
            message = '更新用户失败，请稍后重试'
            if request.is_json:
                return jsonify({'error': message}), 500
            flash(message, 'error')
            return render_template('admin/user_form.html', roles=roles, user=user)
    
    return render_template('admin/user_form.html', roles=roles, user=user)

@admin.route('/users/<int:user_id>')
@login_required
@roles_required('admin')
def user_detail(user_id):
    """用户详情页面"""
    user = User.query.get_or_404(user_id)
    
    # 获取用户的练习记录
    practice_records = PracticeRecord.query.filter_by(user_id=user_id)\
        .order_by(PracticeRecord.created_at.desc()).limit(10).all()
    
    return render_template('admin/user_detail.html', user=user, 
                         practice_records=practice_records)

@admin.route('/users/<int:user_id>/toggle-status', methods=['POST'])
@login_required
@roles_required('admin')
def toggle_user_status(user_id):
    """切换用户状态（激活/禁用）"""
    user = User.query.get_or_404(user_id)
    
    if user.id == current_user.id:
        flash('不能禁用自己的账户', 'error')
        return redirect(url_for('admin.user_detail', user_id=user_id))
    
    user.is_active = not user.is_active
    db.session.commit()
    
    status = '激活' if user.is_active else '禁用'
    flash(f'用户 {user.username} 已{status}', 'success')
    
    return redirect(url_for('admin.user_detail', user_id=user_id))

@admin.route('/users/<int:user_id>/roles', methods=['POST'])
@login_required
@roles_required('admin')
def update_user_roles(user_id):
    """更新用户角色"""
    user = User.query.get_or_404(user_id)
    data = request.get_json() if request.is_json else request.form
    
    role_ids = data.getlist('roles') if hasattr(data, 'getlist') else data.get('roles', [])
    
    # 清除现有角色
    user.roles.clear()
    
    # 添加新角色
    for role_id in role_ids:
        role = Role.query.get(role_id)
        if role:
            user.add_role(role)
    
    db.session.commit()
    
    if request.is_json:
        return jsonify({'message': '角色更新成功'}), 200
    
    flash('用户角色更新成功', 'success')
    return redirect(url_for('admin.user_detail', user_id=user_id))

# 练习曲目管理
@admin.route('/practices')
@login_required
@roles_required('admin', 'teacher')
def practices():
    """练习曲目管理页面"""
    page = request.args.get('page', 1, type=int)
    per_page = 20
    
    search = request.args.get('search', '')
    difficulty = request.args.get('difficulty', type=int)
    genre = request.args.get('genre', '')
    
    query = Practice.query
    
    if search:
        query = query.filter(
            db.or_(
                Practice.title.contains(search),
                Practice.composer.contains(search)
            )
        )
    
    if difficulty:
        query = query.filter_by(difficulty_level=difficulty)
    
    if genre:
        query = query.filter_by(genre=genre)
    
    practices = query.order_by(Practice.created_at.desc())\
        .paginate(page=page, per_page=per_page, error_out=False)
    
    return render_template('admin/practices.html', practices=practices, 
                         search=search, difficulty=difficulty, genre=genre)

@admin.route('/practices/new', methods=['GET', 'POST'])
@login_required
@roles_required('admin', 'teacher')
def new_practice():
    """添加新练习曲目"""
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        
        practice = Practice(
            title=data.get('title'),
            composer=data.get('composer', ''),
            difficulty_level=int(data.get('difficulty_level', 1)),
            genre=data.get('genre', ''),
            description=data.get('description', '')
        )
        
        db.session.add(practice)
        db.session.commit()
        
        if request.is_json:
            return jsonify({'message': '练习曲目创建成功', 'id': practice.id}), 201
        
        flash('练习曲目创建成功', 'success')
        return redirect(url_for('admin.practices'))
    
    return render_template('admin/practice_form.html', practice=None)

@admin.route('/practices/<int:practice_id>/edit', methods=['GET', 'POST'])
@login_required
@roles_required('admin', 'teacher')
def edit_practice(practice_id):
    """编辑练习曲目"""
    practice = Practice.query.get_or_404(practice_id)
    
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        
        practice.title = data.get('title', practice.title)
        practice.composer = data.get('composer', practice.composer)
        practice.difficulty_level = int(data.get('difficulty_level', practice.difficulty_level))
        practice.genre = data.get('genre', practice.genre)
        practice.description = data.get('description', practice.description)
        practice.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        if request.is_json:
            return jsonify({'message': '练习曲目更新成功'}), 200
        
        flash('练习曲目更新成功', 'success')
        return redirect(url_for('admin.practices'))
    
    return render_template('admin/practice_form.html', practice=practice)

@admin.route('/practices/<int:practice_id>/toggle-status', methods=['POST'])
@login_required
@roles_required('admin', 'teacher')
def toggle_practice_status(practice_id):
    """切换练习曲目状态"""
    practice = Practice.query.get_or_404(practice_id)
    
    practice.is_active = not practice.is_active
    db.session.commit()
    
    status = '激活' if practice.is_active else '禁用'
    flash(f'练习曲目 {practice.title} 已{status}', 'success')
    
    return redirect(url_for('admin.practices'))

# 练习记录管理
@admin.route('/practice-records')
@login_required
@roles_required('admin', 'teacher')
def practice_records():
    """练习记录管理页面"""
    page = request.args.get('page', 1, type=int)
    per_page = 20
    
    user_search = request.args.get('user_search', '')
    practice_search = request.args.get('practice_search', '')
    date_from = request.args.get('date_from', '')
    date_to = request.args.get('date_to', '')
    
    query = PracticeRecord.query.join(User).join(Practice)
    
    if user_search:
        query = query.filter(
            db.or_(
                User.username.contains(user_search),
                User.email.contains(user_search)
            )
        )
    
    if practice_search:
        query = query.filter(Practice.title.contains(practice_search))
    
    if date_from:
        query = query.filter(PracticeRecord.created_at >= datetime.strptime(date_from, '%Y-%m-%d'))
    
    if date_to:
        query = query.filter(PracticeRecord.created_at <= datetime.strptime(date_to, '%Y-%m-%d'))
    
    records = query.order_by(PracticeRecord.created_at.desc())\
        .paginate(page=page, per_page=per_page, error_out=False)
    
    return render_template('admin/practice_records.html', records=records,
                         user_search=user_search, practice_search=practice_search,
                         date_from=date_from, date_to=date_to)

@admin.route('/practice-records/<int:record_id>')
@login_required
@roles_required('admin', 'teacher')
def practice_record_detail(record_id):
    """练习记录详情"""
    record = PracticeRecord.query.get_or_404(record_id)
    return render_template('admin/practice_record_detail.html', record=record)

# 联系消息管理
@admin.route('/contact-messages')
@login_required
@roles_required('admin')
def contact_messages():
    """联系消息管理页面"""
    from app.models.auth import ContactMessage
    
    page = request.args.get('page', 1, type=int)
    per_page = 20
    
    status_filter = request.args.get('status', '')
    search = request.args.get('search', '')
    
    query = ContactMessage.query
    
    if status_filter:
        query = query.filter_by(status=status_filter)
    
    if search:
        query = query.filter(
            db.or_(
                ContactMessage.name.contains(search),
                ContactMessage.email.contains(search),
                ContactMessage.subject.contains(search)
            )
        )
    
    messages = query.order_by(ContactMessage.created_at.desc())\
        .paginate(page=page, per_page=per_page, error_out=False)
    
    return render_template('admin/contact_messages.html', messages=messages,
                         status_filter=status_filter, search=search)

@admin.route('/contact-messages/<int:message_id>')
@login_required
@roles_required('admin')
def contact_message_detail(message_id):
    """联系消息详情"""
    from app.models.auth import ContactMessage
    
    message = ContactMessage.query.get_or_404(message_id)
    
    # 标记为已读
    if message.status == 'unread':
        message.status = 'read'
        db.session.commit()
    
    return render_template('admin/contact_message_detail.html', message=message)

@admin.route('/contact-messages/<int:message_id>/reply', methods=['POST'])
@login_required
@roles_required('admin')
def reply_contact_message(message_id):
    """回复联系消息"""
    from app.models.auth import ContactMessage
    
    message = ContactMessage.query.get_or_404(message_id)
    data = request.get_json() if request.is_json else request.form
    
    reply_content = data.get('reply', '').strip()
    if not reply_content:
        flash('回复内容不能为空', 'error')
        return redirect(url_for('admin.contact_message_detail', message_id=message_id))
    
    try:
        # 更新消息状态和回复
        message.admin_reply = reply_content
        message.status = 'replied'
        message.replied_at = datetime.utcnow()
        
        db.session.commit()
        
        # 发送邮件回复（这里简化为添加到待发送队列）
        from app.utils.email import send_contact_reply
        send_contact_reply(message.email, message.name, message.subject, reply_content)
        
        flash('回复发送成功', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash('回复发送失败，请稍后重试', 'error')
    
    return redirect(url_for('admin.contact_message_detail', message_id=message_id))

@admin.route('/contact-messages/<int:message_id>/status', methods=['POST'])
@login_required
@roles_required('admin')
def update_contact_message_status(message_id):
    """更新联系消息状态"""
    from app.models.auth import ContactMessage
    
    message = ContactMessage.query.get_or_404(message_id)
    data = request.get_json() if request.is_json else request.form
    
    new_status = data.get('status')
    if new_status not in ['unread', 'read', 'replied']:
        flash('无效的状态', 'error')
        return redirect(url_for('admin.contact_message_detail', message_id=message_id))
    
    message.status = new_status
    db.session.commit()
    
    flash('状态更新成功', 'success')
    return redirect(url_for('admin.contact_message_detail', message_id=message_id))
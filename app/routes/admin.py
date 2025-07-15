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
    # 统计数据
    total_users = User.query.count()
    total_students = User.query.join(User.roles).filter(Role.name == 'student').count()
    total_teachers = User.query.join(User.roles).filter(Role.name == 'teacher').count()
    total_practices = Practice.query.count()
    total_records = PracticeRecord.query.count()
    
    # 最近7天的新用户
    seven_days_ago = datetime.utcnow() - timedelta(days=7)
    new_users_week = User.query.filter(User.created_at >= seven_days_ago).count()
    
    # 最近7天的练习记录
    new_records_week = PracticeRecord.query.filter(PracticeRecord.created_at >= seven_days_ago).count()
    
    stats = {
        'total_users': total_users,
        'total_students': total_students,
        'total_teachers': total_teachers,
        'total_practices': total_practices,
        'total_records': total_records,
        'new_users_week': new_users_week,
        'new_records_week': new_records_week
    }
    
    return render_template('admin/dashboard.html', stats=stats)

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
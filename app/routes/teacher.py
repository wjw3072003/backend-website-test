from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user
from datetime import datetime, timedelta
from sqlalchemy import func

from app import db
from app.models.user import User, Role, TeacherInviteCode
from app.models.teacher_simple import Class, Assignment, Grade, TeachingResource, Announcement, Attendance
from app.utils.cache import get_cache, set_cache
from app.models.practice import PracticeRecord

teacher = Blueprint('teacher', __name__)

def require_teacher_role():
    """装饰器：要求老师角色"""
    if not current_user.has_role('teacher'):
        flash('需要老师权限才能访问此页面', 'error')
        return redirect(url_for('main.dashboard'))
    return None

@teacher.route('/dashboard')
@login_required
def dashboard():
    """老师仪表板"""
    role_check = require_teacher_role()
    if role_check:
        return role_check
    
    # 只统计与当前老师直接关联的学生
    total_students = User.query.join(User.roles).filter(
        User.teacher_id == current_user.id,
        Role.name == 'student'
    ).count()
    
    total_assignments = Assignment.query.filter_by(teacher_id=current_user.id).count()
    pending_grades = Grade.query.filter_by(status='pending').join(Assignment).filter(
        Assignment.teacher_id == current_user.id
    ).count()
    
    recent_assignments = Assignment.query.filter_by(teacher_id=current_user.id).order_by(
        Assignment.created_at.desc()
    ).limit(5).all()
    recent_grades = Grade.query.join(Assignment).filter(
        Assignment.teacher_id == current_user.id
    ).order_by(Grade.created_at.desc()).limit(5).all()

    # 查询最近关联到自己的学生（如最近5个）
    recent_students = User.query.join(User.roles).filter(
        User.teacher_id == current_user.id,
        Role.name == 'student'
    ).order_by(User.created_at.desc()).limit(5).all()
    
    # 推荐码和推荐链接
    invite = TeacherInviteCode.query.filter_by(teacher_id=current_user.id).first()
    invite_code = invite.code if invite else None
    invite_link = None
    if invite_code:
        from flask import request
        base_url = request.host_url.rstrip('/')
        invite_link = f"{base_url}/auth/register?invite={invite_code}"
    
    stats = {
        'total_students': total_students,
        'total_assignments': total_assignments,
        'pending_grades': pending_grades
    }
    
    return render_template('teacher/dashboard.html',
                         stats=stats,
                         recent_assignments=recent_assignments,
                         recent_grades=recent_grades,
                         recent_students=recent_students,
                         invite_code=invite_code,
                         invite_link=invite_link)

@teacher.route('/students')
@login_required
def students():
    """学生管理"""
    role_check = require_teacher_role()
    if role_check:
        return role_check
    
    # 只显示通过推荐码注册的学生
    students = User.query.join(User.roles).filter(
        User.teacher_id == current_user.id,
        Role.name == 'student'
    ).all()
    
    # 可选：统计信息
    all_students = []
    for student in students:
                total_assignments = Assignment.query.filter_by(teacher_id=current_user.id).count()
                completed_assignments = Grade.query.join(Assignment).filter(
                    Assignment.teacher_id == current_user.id,
                    Grade.student_id == student.id,
                    Grade.status == 'graded'
                ).count()
                avg_score = db.session.query(func.avg(Grade.score)).join(Assignment).filter(
                    Assignment.teacher_id == current_user.id,
                    Grade.student_id == student.id,
                    Grade.status == 'graded'
                ).scalar()
                all_students.append({
                    'student': student,
                    'total_assignments': total_assignments,
                    'completed_assignments': completed_assignments,
                    'avg_score': round(avg_score, 1) if avg_score else 0
                })
    
    return render_template('teacher/students.html',
                         students=all_students)

@teacher.route('/students/<int:student_id>')
@login_required
def student_detail(student_id):
    """学生详情页面"""
    role_check = require_teacher_role()
    if role_check:
        return role_check
    
    # 获取学生信息，确保是当前老师的学生
    student = User.query.join(User.roles).filter(
        User.id == student_id,
        User.teacher_id == current_user.id,
        Role.name == 'student'
    ).first_or_404()
    
    # 获取学生的练习记录
    practice_records = PracticeRecord.query.filter_by(user_id=student.id).order_by(
        PracticeRecord.created_at.desc()
    ).limit(10).all()
    
    # 获取学生的作业成绩
    grades = Grade.query.join(Assignment).filter(
        Assignment.teacher_id == current_user.id,
        Grade.student_id == student.id
    ).order_by(Grade.created_at.desc()).limit(10).all()
    
    # 统计信息
    total_practices = PracticeRecord.query.filter_by(user_id=student.id).count()
    total_assignments = Grade.query.join(Assignment).filter(
        Assignment.teacher_id == current_user.id,
        Grade.student_id == student.id
    ).count()
    avg_score = db.session.query(func.avg(Grade.score)).join(Assignment).filter(
        Assignment.teacher_id == current_user.id,
        Grade.student_id == student.id,
        Grade.status == 'graded'
    ).scalar()
    
    return render_template('teacher/student_detail.html',
                         student=student,
                         practice_records=practice_records,
                         grades=grades,
                         total_practices=total_practices,
                         total_assignments=total_assignments,
                         avg_score=round(avg_score, 1) if avg_score else 0)

@teacher.route('/classes')
@login_required
def classes():
    """班级管理"""
    role_check = require_teacher_role()
    if role_check:
        return role_check
    
    # 获取老师的班级
    teacher_classes = Class.query.filter(Class.teachers.contains(current_user)).all()
    
    # 为每个班级添加统计信息
    classes_with_stats = []
    for cls in teacher_classes:
        assignments_count = Assignment.query.filter_by(class_id=cls.id).count()
        pending_grades = Grade.query.filter_by(class_id=cls.id, status='pending').count()
        
        classes_with_stats.append({
            'class': cls,
            'student_count': len(cls.students),
            'assignments_count': assignments_count,
            'pending_grades': pending_grades
        })
    
    return render_template('teacher/classes.html', classes=classes_with_stats)

@teacher.route('/assignments')
@login_required  
def assignments():
    """作业管理"""
    role_check = require_teacher_role()
    if role_check:
        return role_check
    
    # 获取筛选参数
    class_filter = request.args.get('class_id', '', type=int)
    status_filter = request.args.get('status', '')
    
    # 构建查询
    query = Assignment.query.filter_by(teacher_id=current_user.id)
    
    if class_filter:
        query = query.filter_by(class_id=class_filter)
    
    if status_filter:
        if status_filter == 'active':
            query = query.filter_by(is_active=True)
        elif status_filter == 'published':
            query = query.filter_by(is_published=True)
        elif status_filter == 'overdue':
            query = query.filter(Assignment.due_date < datetime.utcnow())
    
    assignments = query.order_by(Assignment.created_at.desc()).all()
    
    # 获取老师的班级用于筛选
    teacher_classes = Class.query.filter(Class.teachers.contains(current_user)).all()
    
    # 为每个作业添加统计信息
    assignments_with_stats = []
    for assignment in assignments:
        submitted_count = Grade.query.filter_by(assignment_id=assignment.id).count()
        graded_count = Grade.query.filter_by(assignment_id=assignment.id, status='graded').count()
        
        # 获取班级名称
        class_obj = Class.query.get(assignment.class_id)
        class_name = class_obj.name if class_obj else 'N/A'
        
        assignments_with_stats.append({
            'assignment': assignment,
            'submitted_count': submitted_count,
            'graded_count': graded_count,
            'class_name': class_name
        })
    
    return render_template('teacher/assignments.html',
                         assignments=assignments_with_stats,
                         teacher_classes=teacher_classes,
                         current_filters={
                             'class_id': class_filter,
                             'status': status_filter
                         })

@teacher.route('/grades')
@login_required
def grades():
    """成绩管理"""
    role_check = require_teacher_role()
    if role_check:
        return role_check
    
    grades = Grade.query.join(Assignment).filter(Assignment.teacher_id == current_user.id).all()
    
    return render_template('teacher/grades.html', grades=grades)

@teacher.route('/reports')
@login_required
def reports():
    """教学报告"""
    role_check = require_teacher_role()
    if role_check:
        return role_check
    
    stats = {
        'total_classes': 0,
        'total_students': 0,
        'total_assignments': Assignment.query.filter_by(teacher_id=current_user.id).count(),
    }
    
    return render_template('teacher/reports.html', stats=stats)

@teacher.route('/resources')
@login_required
def resources():
    """教学资源管理"""
    role_check = require_teacher_role()
    if role_check:
        return role_check
    
    resources = TeachingResource.query.filter_by(created_by=current_user.id).all()
    
    return render_template('teacher/resources.html', resources=resources)

@teacher.route('/announcements')
@login_required
def announcements():
    """公告管理"""
    role_check = require_teacher_role()
    if role_check:
        return role_check
    
    announcements = Announcement.query.filter_by(created_by=current_user.id).all()
    
    return render_template('teacher/announcements.html', announcements=announcements) 

@teacher.route('/practice-records')
@login_required
def practice_records():
    """只显示自己学生的练习记录"""
    role_check = require_teacher_role()
    if role_check:
        return role_check

    # 获取所有自己学生的id
    student_ids = [s.id for s in User.query.join(User.roles).filter(
        User.teacher_id == current_user.id,
        Role.name == 'student'
    ).all()]

    # 查询这些学生的练习记录
    page = request.args.get('page', 1, type=int)
    per_page = 10
    query = PracticeRecord.query.filter(PracticeRecord.user_id.in_(student_ids))
    records = query.order_by(PracticeRecord.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)

    return render_template('teacher/practice_records.html', records=records) 

@teacher.route('/invite-codes')
@login_required
def invite_codes():
    """推广码管理页面"""
    role_check = require_teacher_role()
    if role_check:
        return role_check
    
    # 获取当前老师的推荐码
    invite = TeacherInviteCode.query.filter_by(teacher_id=current_user.id).first()
    invite_code = invite.code if invite else None
    invite_link = None
    
    if invite_code:
        from flask import request
        base_url = request.host_url.rstrip('/')
        invite_link = f"{base_url}/auth/register?invite={invite_code}"
    
    # 获取通过此推荐码注册的学生统计
    student_count = 0
    if invite_code:
        student_count = User.query.join(User.roles).filter(
            User.teacher_id == current_user.id,
            Role.name == 'student'
        ).count()
    
    # 获取最近通过推荐码注册的学生
    recent_students = User.query.join(User.roles).filter(
        User.teacher_id == current_user.id,
        Role.name == 'student'
    ).order_by(User.created_at.desc()).limit(10).all()
    
    return render_template('teacher/invite_codes.html',
                         invite_code=invite_code,
                         invite_link=invite_link,
                         student_count=student_count,
                         recent_students=recent_students) 

@teacher.route('/classes/<int:class_id>')
@login_required
def view_class(class_id):
    """查看班级详情"""
    role_check = require_teacher_role()
    if role_check:
        return role_check
    
    # 获取班级信息，确保是当前老师的班级
    cls = Class.query.filter(
        Class.id == class_id,
        Class.teachers.contains(current_user)
    ).first_or_404()
    
    # 获取班级学生
    students = cls.students
    
    # 获取班级作业
    assignments = Assignment.query.filter_by(class_id=cls.id).order_by(Assignment.created_at.desc()).all()
    
    return render_template('teacher/class_detail.html',
                         class_obj=cls,
                         students=students,
                         assignments=assignments)

@teacher.route('/classes/create', methods=['POST'])
@login_required
def create_class():
    """创建班级"""
    role_check = require_teacher_role()
    if role_check:
        return role_check
    
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        description = request.form.get('description', '').strip()
        code = request.form.get('code', '').strip()
        
        if not name or not code:
            flash('班级名称和代码是必填项', 'error')
            return redirect(url_for('teacher.classes'))
        
        # 检查代码是否已存在
        if Class.query.filter_by(code=code).first():
            flash('班级代码已存在', 'error')
            return redirect(url_for('teacher.classes'))
        
        try:
            cls = Class(
                name=name,
                description=description,
                code=code,
                grade_level='通用',
                subject='音乐'
            )
            cls.teachers.append(current_user)
            
            db.session.add(cls)
            db.session.commit()
            
            flash(f'班级 {name} 创建成功', 'success')
            return redirect(url_for('teacher.classes'))
            
        except Exception as e:
            db.session.rollback()
            flash('创建班级失败，请稍后重试', 'error')
            return redirect(url_for('teacher.classes'))

@teacher.route('/assignments/<int:assignment_id>')
@login_required
def view_assignment(assignment_id):
    """查看作业详情"""
    role_check = require_teacher_role()
    if role_check:
        return role_check
    
    # 获取作业信息，确保是当前老师的作业
    assignment = Assignment.query.filter_by(
        id=assignment_id,
        teacher_id=current_user.id
    ).first_or_404()
    
    # 获取作业成绩
    grades = Grade.query.filter_by(assignment_id=assignment.id).all()
    
    return render_template('teacher/assignment_detail.html',
                         assignment=assignment,
                         grades=grades)

@teacher.route('/assignments/create', methods=['POST'])
@login_required
def create_assignment():
    """创建作业"""
    role_check = require_teacher_role()
    if role_check:
        return role_check
    
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        class_id = request.form.get('class_id', type=int)
        
        if not title:
            flash('作业标题是必填项', 'error')
            return redirect(url_for('teacher.assignments'))
        
        try:
            assignment = Assignment(
                title=title,
                description=description,
                class_id=class_id,
                teacher_id=current_user.id,
                assignment_type='practice',
                difficulty_level=3,
                max_score=100
            )
            
            db.session.add(assignment)
            db.session.commit()
            
            flash(f'作业 {title} 创建成功', 'success')
            return redirect(url_for('teacher.assignments'))
            
        except Exception as e:
            db.session.rollback()
            flash('创建作业失败，请稍后重试', 'error')
            return redirect(url_for('teacher.assignments'))

@teacher.route('/assignments/<int:assignment_id>/grades')
@login_required
def assignment_grades(assignment_id):
    """作业成绩管理"""
    role_check = require_teacher_role()
    if role_check:
        return role_check
    
    # 获取作业信息，确保是当前老师的作业
    assignment = Assignment.query.filter_by(
        id=assignment_id,
        teacher_id=current_user.id
    ).first_or_404()
    
    # 获取作业成绩
    grades = Grade.query.filter_by(assignment_id=assignment.id).all()
    
    return render_template('teacher/assignment_grades.html',
                         assignment=assignment,
                         grades=grades)

@teacher.route('/students/add', methods=['POST'])
@login_required
def add_student():
    """添加学生到班级"""
    role_check = require_teacher_role()
    if role_check:
        return role_check
    
    if request.method == 'POST':
        student_email = request.form.get('student_email', '').strip()
        class_id = request.form.get('class_id', type=int)
        
        if not student_email:
            flash('学生邮箱是必填项', 'error')
            return redirect(url_for('teacher.students'))
        
        # 查找学生
        student = User.query.filter_by(email=student_email).join(User.roles).filter(Role.name == 'student').first()
        if not student:
            flash('未找到该学生', 'error')
            return redirect(url_for('teacher.students'))
        
        # 检查学生是否已经是当前老师的学生
        if student.teacher_id == current_user.id:
            flash('该学生已经是您的学生', 'info')
            return redirect(url_for('teacher.students'))
        
        try:
            # 将学生关联到当前老师
            student.teacher_id = current_user.id
            
            # 如果指定了班级，将学生添加到班级
            if class_id:
                cls = Class.query.filter(
                    Class.id == class_id,
                    Class.teachers.contains(current_user)
                ).first()
                if cls:
                    cls.students.append(student)
            
            db.session.commit()
            
            flash(f'学生 {student.username} 添加成功', 'success')
            return redirect(url_for('teacher.students'))
            
        except Exception as e:
            db.session.rollback()
            flash('添加学生失败，请稍后重试', 'error')
            return redirect(url_for('teacher.students')) 
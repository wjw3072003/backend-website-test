from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user
from datetime import datetime, timedelta
from sqlalchemy import func

from app import db
from app.models.user import User, Role
from app.models.teacher_simple import Class, Assignment, Grade, TeachingResource, Announcement, Attendance
from app.utils.cache import get_cache, set_cache

teacher = Blueprint('teacher', __name__)

def require_teacher_role():
    """装饰器：要求老师角色"""
    if not current_user.has_role('teacher'):
        flash('需要老师权限才能访问此页面', 'error')
        return redirect(url_for('main.dashboard'))
    return None

@teacher.route('/dashboard')
@login_required
def teacher_dashboard():
    """老师仪表板"""
    role_check = require_teacher_role()
    if role_check:
        return role_check
    
    # 获取老师的基本统计
    teacher_classes = Class.query.filter(Class.teachers.contains(current_user)).all()
    class_ids = [cls.id for cls in teacher_classes]
    
    # 统计信息
    total_classes = len(teacher_classes)
    total_students = db.session.query(func.count(func.distinct(Class.students))).filter(
        Class.id.in_(class_ids)
    ).scalar() if class_ids else 0
    
    total_assignments = Assignment.query.filter_by(teacher_id=current_user.id).count()
    pending_grades = Grade.query.filter_by(status='pending').join(Assignment).filter(
        Assignment.teacher_id == current_user.id
    ).count()
    
    # 最近的活动
    recent_assignments = Assignment.query.filter_by(teacher_id=current_user.id).order_by(
        Assignment.created_at.desc()
    ).limit(5).all()
    
    recent_grades = Grade.query.join(Assignment).filter(
        Assignment.teacher_id == current_user.id
    ).order_by(Grade.created_at.desc()).limit(5).all()
    
    stats = {
        'total_classes': total_classes,
        'total_students': total_students,
        'total_assignments': total_assignments,
        'pending_grades': pending_grades
    }
    
    return render_template('teacher/dashboard.html',
                         stats=stats,
                         teacher_classes=teacher_classes,
                         recent_assignments=recent_assignments,
                         recent_grades=recent_grades)

@teacher.route('/students')
@login_required
def students():
    """学生管理"""
    role_check = require_teacher_role()
    if role_check:
        return role_check
    
    # 获取老师的所有班级
    teacher_classes = Class.query.filter(Class.teachers.contains(current_user)).all()
    
    # 获取所有学生
    all_students = []
    for cls in teacher_classes:
        for student in cls.students:
            if student not in [s['student'] for s in all_students]:
                # 计算学生的统计信息
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
                    'classes': [c for c in teacher_classes if student in c.students],
                    'total_assignments': total_assignments,
                    'completed_assignments': completed_assignments,
                    'avg_score': round(avg_score, 1) if avg_score else 0
                })
    
    return render_template('teacher/students.html',
                         students=all_students,
                         teacher_classes=teacher_classes)

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
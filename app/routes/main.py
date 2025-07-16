from flask import Blueprint, render_template, jsonify, flash, redirect, url_for, request
from flask_login import login_required, current_user
from app.models.user import User
from app.models.practice import Practice, PracticeRecord
from app import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    """首页"""
    return render_template('index.html')

@main.route('/dashboard')
@login_required
def dashboard():
    """用户仪表板"""
    # 获取用户最近的练习记录
    recent_records = PracticeRecord.query.filter_by(user_id=current_user.id)\
        .order_by(PracticeRecord.created_at.desc()).limit(5).all()
    
    # 获取用户统计信息
    total_practices = PracticeRecord.query.filter_by(user_id=current_user.id).count()
    
    # 计算平均分数
    avg_score = db.session.query(db.func.avg(PracticeRecord.score))\
        .filter_by(user_id=current_user.id).scalar()
    
    stats = {
        'total_practices': total_practices,
        'average_score': round(avg_score, 1) if avg_score else 0,
        'recent_records': [record.to_dict() for record in recent_records]
    }
    
    return render_template('dashboard.html', stats=stats)

@main.route('/practices')
@login_required
def practices():
    """练习曲目列表"""
    practices = Practice.query.filter_by(is_active=True).all()
    return render_template('practices.html', practices=practices)

@main.route('/practice/<int:practice_id>')
@login_required
def practice_detail(practice_id):
    """练习执行页面"""
    practice = Practice.query.get_or_404(practice_id)
    
    # 获取用户该练习的历史记录
    user_records = PracticeRecord.query.filter_by(
        user_id=current_user.id, 
        practice_id=practice_id
    ).order_by(PracticeRecord.created_at.desc()).limit(5).all()
    
    # 计算用户在此练习上的最高分数
    best_score = db.session.query(db.func.max(PracticeRecord.score))\
        .filter_by(user_id=current_user.id, practice_id=practice_id).scalar()
    
    return render_template('practice_detail.html', 
                         practice=practice, 
                         user_records=user_records,
                         best_score=best_score or 0)

@main.route('/practice-result/<int:record_id>')
@login_required
def practice_result(record_id):
    """练习结果展示页面"""
    record = PracticeRecord.query.get_or_404(record_id)
    
    # 确保只有记录所有者才能查看
    if record.user_id != current_user.id:
        flash('您无权查看此练习记录', 'error')
        return redirect(url_for('main.dashboard'))
    
    return render_template('practice_result.html', record=record)

@main.route('/history')
@login_required
def practice_history():
    """用户练习历史"""
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    records = PracticeRecord.query.filter_by(user_id=current_user.id)\
        .order_by(PracticeRecord.created_at.desc())\
        .paginate(page=page, per_page=per_page, error_out=False)
    
    return render_template('practice_history.html', records=records)

@main.route('/about')
def about():
    """关于页面"""
    return render_template('about.html')

@main.route('/contact')
def contact():
    """联系页面"""
    return render_template('contact.html')

@main.route('/health')
def health_check():
    """健康检查接口"""
    return jsonify({
        'status': 'healthy',
        'service': 'aimuspal-web',
        'version': '1.0.0'
    })
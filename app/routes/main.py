from flask import Blueprint, render_template, jsonify
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
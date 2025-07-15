from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
import os
import uuid
from datetime import datetime, timedelta

from app import db
from app.models.user import User, Role
from app.models.practice import Practice, PracticeRecord, AudioFile
from app.utils.file_handler import allowed_file, save_audio_file
from app.utils.ai_analysis import analyze_audio_practice

api = Blueprint('api', __name__)

# API认证相关
@api.route('/auth/login', methods=['POST'])
def api_login():
    """API登录接口"""
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'error': '邮箱和密码是必填项'}), 400
    
    email = data['email'].strip().lower()
    password = data['password']
    
    user = User.query.filter_by(email=email).first()
    
    if user and user.check_password(password):
        if not user.is_active:
            return jsonify({'error': '账户已被禁用'}), 403
        
        # 更新最后登录时间
        user.last_login = datetime.utcnow()
        db.session.commit()
        
        # 创建访问令牌
        access_token = create_access_token(
            identity=user.id,
            expires_delta=timedelta(days=30)
        )
        
        return jsonify({
            'message': '登录成功',
            'access_token': access_token,
            'user': user.to_dict()
        }), 200
    
    return jsonify({'error': '邮箱或密码错误'}), 401

@api.route('/auth/register', methods=['POST'])
def api_register():
    """API注册接口"""
    data = request.get_json()
    
    required_fields = ['email', 'username', 'password']
    if not data or not all(field in data for field in required_fields):
        return jsonify({'error': '请填写所有必填字段'}), 400
    
    email = data['email'].strip().lower()
    username = data['username'].strip()
    password = data['password']
    user_type = data.get('user_type', 'student')
    
    # 检查用户是否已存在
    if User.query.filter_by(email=email).first():
        return jsonify({'error': '该邮箱已被注册'}), 400
    
    if User.query.filter_by(username=username).first():
        return jsonify({'error': '该用户名已被使用'}), 400
    
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
        
        # 创建访问令牌
        access_token = create_access_token(
            identity=user.id,
            expires_delta=timedelta(days=30)
        )
        
        return jsonify({
            'message': '注册成功',
            'access_token': access_token,
            'user': user.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': '注册失败，请稍后重试'}), 500

# 练习相关API
@api.route('/practices', methods=['GET'])
@jwt_required()
def get_practices():
    """获取练习曲目列表"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    difficulty = request.args.get('difficulty', type=int)
    genre = request.args.get('genre')
    
    query = Practice.query.filter_by(is_active=True)
    
    if difficulty:
        query = query.filter_by(difficulty_level=difficulty)
    if genre:
        query = query.filter_by(genre=genre)
    
    practices = query.order_by(Practice.created_at.desc())\
        .paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'practices': [practice.to_dict() for practice in practices.items],
        'total': practices.total,
        'pages': practices.pages,
        'current_page': page
    }), 200

@api.route('/practices/<int:practice_id>', methods=['GET'])
@jwt_required()
def get_practice(practice_id):
    """获取单个练习曲目详情"""
    practice = Practice.query.get_or_404(practice_id)
    
    if not practice.is_active:
        return jsonify({'error': '该练习曲目不可用'}), 404
    
    return jsonify(practice.to_dict()), 200

@api.route('/practices/<int:practice_id>/upload', methods=['POST'])
@jwt_required()
def upload_practice_audio(practice_id):
    """上传练习音频"""
    user_id = get_jwt_identity()
    practice = Practice.query.get_or_404(practice_id)
    
    if 'audio' not in request.files:
        return jsonify({'error': '请选择音频文件'}), 400
    
    file = request.files['audio']
    if file.filename == '':
        return jsonify({'error': '请选择音频文件'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': '不支持的文件格式'}), 400
    
    try:
        # 创建练习记录
        practice_record = PracticeRecord(
            user_id=user_id,
            practice_id=practice_id,
            status='analyzing'
        )
        db.session.add(practice_record)
        db.session.commit()
        
        # 保存音频文件
        filename = save_audio_file(file, practice_record.id)
        
        # 创建音频文件记录
        audio_file = AudioFile(
            practice_record_id=practice_record.id,
            filename=filename,
            original_filename=file.filename,
            file_path=os.path.join(current_app.config['UPLOAD_FOLDER'], filename),
            file_size=len(file.read()),
            file_type=file.content_type
        )
        
        file.seek(0)  # 重置文件指针
        
        db.session.add(audio_file)
        db.session.commit()
        
        # 异步分析音频（这里简化为同步）
        analysis_result = analyze_audio_practice(audio_file.file_path, practice)
        
        # 更新练习记录
        practice_record.score = analysis_result.get('score', 0)
        practice_record.tempo_accuracy = analysis_result.get('tempo_accuracy', 0)
        practice_record.pitch_accuracy = analysis_result.get('pitch_accuracy', 0)
        practice_record.rhythm_accuracy = analysis_result.get('rhythm_accuracy', 0)
        practice_record.ai_feedback = analysis_result.get('feedback', '')
        practice_record.improvement_suggestions = analysis_result.get('suggestions', '')
        practice_record.status = 'completed'
        
        db.session.commit()
        
        return jsonify({
            'message': '音频上传成功',
            'practice_record': practice_record.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': '上传失败，请稍后重试'}), 500

@api.route('/practice-records', methods=['GET'])
@jwt_required()
def get_practice_records():
    """获取用户练习记录"""
    user_id = get_jwt_identity()
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    records = PracticeRecord.query.filter_by(user_id=user_id)\
        .order_by(PracticeRecord.created_at.desc())\
        .paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'records': [record.to_dict() for record in records.items],
        'total': records.total,
        'pages': records.pages,
        'current_page': page
    }), 200

@api.route('/practice-records/<int:record_id>', methods=['GET'])
@jwt_required()
def get_practice_record(record_id):
    """获取单个练习记录详情"""
    user_id = get_jwt_identity()
    record = PracticeRecord.query.filter_by(id=record_id, user_id=user_id).first_or_404()
    
    return jsonify(record.to_dict()), 200

# 用户相关API
@api.route('/user/profile', methods=['GET'])
@jwt_required()
def get_user_profile():
    """获取用户资料"""
    user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)
    
    return jsonify(user.to_dict()), 200

@api.route('/user/profile', methods=['PUT'])
@jwt_required()
def update_user_profile():
    """更新用户资料"""
    user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)
    data = request.get_json()
    
    if not data:
        return jsonify({'error': '请提供更新数据'}), 400
    
    # 更新允许的字段
    allowed_fields = ['first_name', 'last_name', 'phone']
    for field in allowed_fields:
        if field in data:
            setattr(user, field, data[field])
    
    try:
        db.session.commit()
        return jsonify({
            'message': '个人资料更新成功',
            'user': user.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': '更新失败，请稍后重试'}), 500

@api.route('/user/stats', methods=['GET'])
@jwt_required()
def get_user_stats():
    """获取用户统计信息"""
    user_id = get_jwt_identity()
    
    # 练习次数
    total_practices = PracticeRecord.query.filter_by(user_id=user_id).count()
    
    # 平均分数
    avg_score = db.session.query(db.func.avg(PracticeRecord.score))\
        .filter_by(user_id=user_id).scalar()
    
    # 最近7天的练习次数
    seven_days_ago = datetime.utcnow() - timedelta(days=7)
    recent_practices = PracticeRecord.query.filter(
        PracticeRecord.user_id == user_id,
        PracticeRecord.created_at >= seven_days_ago
    ).count()
    
    return jsonify({
        'total_practices': total_practices,
        'average_score': round(avg_score, 1) if avg_score else 0,
        'recent_practices': recent_practices,
        'last_practice': None  # TODO: 添加最后练习时间
    }), 200
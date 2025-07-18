from flask import Blueprint, render_template, jsonify, request, flash, redirect, url_for, send_file
from flask_login import login_required, current_user
from app.models.user import User
from app.models.practice import Practice, PracticeRecord
from app import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    """默认主页 - 重定向到AI MusPal新首页"""
    return redirect(url_for('main.aimuspal_homepage'))

@main.route('/index_back')
def index_back():
    """备用首页 - 原来的首页"""
    return render_template('index.html')

@main.route('/aimuspal')
def aimuspal_homepage():
    """AI MusPal新首页"""
    import os
    return send_file(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'aimuspal_homepage_formatted.html'))



@main.route('/dashboard')
@login_required
def dashboard():
    """用户仪表板"""
    # 如果是老师，重定向到老师仪表板
    if current_user.has_role('teacher'):
        return redirect(url_for('teacher.dashboard'))
    
    from datetime import datetime, timedelta
    from app.utils.cache import get_stats_cache, set_stats_cache, get_common_cache
    
    # 尝试从缓存获取用户统计
    stats = get_stats_cache(current_user.id)
    
    if stats is None:
        # 获取用户最近的练习记录
        recent_records = PracticeRecord.query.filter_by(user_id=current_user.id)\
            .join(Practice).order_by(PracticeRecord.created_at.desc()).limit(5).all()
        
        # 获取用户统计信息
        total_practices = PracticeRecord.query.filter_by(user_id=current_user.id).count()
        
        # 计算平均分数
        avg_score = db.session.query(db.func.avg(PracticeRecord.score))\
            .filter_by(user_id=current_user.id).scalar()
        
        # 计算本月练习次数
        current_month = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        monthly_practices = PracticeRecord.query.filter(
            PracticeRecord.user_id == current_user.id,
            PracticeRecord.created_at >= current_month
        ).count()
        
        # 格式化最近练习记录
        formatted_records = []
        for record in recent_records:
            formatted_record = {
                'id': record.id,
                'practice_title': record.practice.title,
                'practice_composer': record.practice.composer,
                'created_at': record.created_at,
                'score': record.score,
                'status': record.status
            }
            formatted_records.append(formatted_record)
        
        stats = {
            'total_practices': total_practices,
            'average_score': round(avg_score, 1) if avg_score else 0,
            'monthly_practices': monthly_practices,
            'monthly_goal': 10,  # 默认目标，之后可以做成用户可配置的
            'recent_records': formatted_records
        }
        
        # 缓存用户统计数据（5分钟）
        set_stats_cache(current_user.id, stats)
    
    # 获取推荐练习（从缓存或数据库）
    recommended_practices = get_common_cache('recommended_practices')
    if recommended_practices is None:
        recommended_practices = Practice.query.filter_by(is_active=True)\
            .order_by(db.func.random()).limit(3).all()
        # 缓存推荐练习（10分钟）
        from app.utils.cache import CacheManager
        CacheManager.set('recommended_practices', recommended_practices, ttl=600, prefix='common')
    
    stats['recommended_practices'] = recommended_practices
    
    return render_template('dashboard.html', stats=stats)

@main.route('/practices')
@login_required
def practices():
    """练习曲目列表"""
    # 如果是老师，重定向到老师仪表板
    if current_user.has_role('teacher'):
        return redirect(url_for('teacher.dashboard'))
    
    # 获取搜索和筛选参数
    search = request.args.get('search', '').strip()
    difficulty = request.args.get('difficulty', type=int)
    genre = request.args.get('genre', '').strip()
    composer = request.args.get('composer', '').strip()
    sort_by = request.args.get('sort', 'title')  # title, difficulty, created_at
    
    # 获取分页参数
    page = request.args.get('page', 1, type=int)
    per_page = 12  # 每页显示12个曲目
    
    # 构建查询
    query = Practice.query.filter_by(is_active=True)
    
    # 应用搜索条件
    if search:
        search_pattern = f'%{search}%'
        query = query.filter(
            db.or_(
                Practice.title.ilike(search_pattern),
                Practice.composer.ilike(search_pattern),
                Practice.description.ilike(search_pattern)
            )
        )
    
    # 应用筛选条件
    if difficulty:
        query = query.filter(Practice.difficulty_level == difficulty)
    
    if genre:
        query = query.filter(Practice.genre.ilike(f'%{genre}%'))
    
    if composer:
        query = query.filter(Practice.composer.ilike(f'%{composer}%'))
    
    # 应用排序
    if sort_by == 'difficulty':
        query = query.order_by(Practice.difficulty_level)
    elif sort_by == 'created_at':
        query = query.order_by(Practice.created_at.desc())
    else:  # 默认按标题排序
        query = query.order_by(Practice.title)
    
    # 分页
    practices = query.paginate(page=page, per_page=per_page, error_out=False)
    
    # 获取筛选选项数据（使用缓存）
    from app.utils.cache import get_common_cache, CacheManager
    
    # 获取所有可用的难度等级
    difficulty_levels = get_common_cache('difficulty_levels')
    if difficulty_levels is None:
        difficulty_levels = db.session.query(Practice.difficulty_level)\
            .filter(Practice.is_active == True)\
            .distinct().order_by(Practice.difficulty_level).all()
        difficulty_levels = [level[0] for level in difficulty_levels]
        CacheManager.set('difficulty_levels', difficulty_levels, ttl=1800, prefix='common')
    
    # 获取所有可用的风格
    genres = get_common_cache('genres')
    if genres is None:
        genres = db.session.query(Practice.genre)\
            .filter(Practice.is_active == True, Practice.genre.isnot(None))\
            .distinct().order_by(Practice.genre).all()
        genres = [genre[0] for genre in genres if genre[0]]
        CacheManager.set('genres', genres, ttl=1800, prefix='common')
    
    # 获取所有可用的作曲家
    composers = get_common_cache('composers')
    if composers is None:
        composers = db.session.query(Practice.composer)\
            .filter(Practice.is_active == True, Practice.composer.isnot(None))\
            .distinct().order_by(Practice.composer).all()
        composers = [composer[0] for composer in composers if composer[0]]
        CacheManager.set('composers', composers, ttl=1800, prefix='common')
    
    # 统计信息
    total_practices = Practice.query.filter_by(is_active=True).count()
    user_practice_count = PracticeRecord.query.filter_by(user_id=current_user.id).count()
    
    # 获取用户在各个曲目上的练习统计
    user_stats = {}
    for practice in practices.items:
        # 获取用户在此曲目上的统计
        practice_records = PracticeRecord.query.filter_by(
            user_id=current_user.id,
            practice_id=practice.id
        ).all()
        
        if practice_records:
            attempts = len(practice_records)
            scores = [r.score for r in practice_records if r.score is not None]
            best_score = max(scores) if scores else None
            avg_score = sum(scores) / len(scores) if scores else None
            
            user_stats[practice.id] = {
                'attempts': attempts,
                'best_score': round(best_score, 1) if best_score else None,
                'avg_score': round(avg_score, 1) if avg_score else None,
                'last_practice': max(practice_records, key=lambda x: x.created_at).created_at
            }
    
    # 构建当前筛选条件（用于模板中的筛选状态保持）
    current_filters = {
        'search': search,
        'difficulty': difficulty,
        'genre': genre,
        'composer': composer,
        'sort': sort_by
            }
    
    return render_template('practices.html', 
                         practices=practices,
                         difficulty_levels=difficulty_levels,
                         genres=genres,
                         composers=composers,
                         total_practices=total_practices,
                         user_practice_count=user_practice_count,
                         user_stats=user_stats,
                         current_filters=current_filters)

@main.route('/practices/<int:practice_id>')
@login_required
def practice_detail(practice_id):
    """练习曲目详情页面"""
    # 如果是老师，重定向到老师仪表板
    if current_user.has_role('teacher'):
        return redirect(url_for('teacher.dashboard'))
    
    practice = Practice.query.get_or_404(practice_id)
    
    if not practice.is_active:
        flash('该练习曲目不可用', 'error')
        return redirect(url_for('main.practices'))
    
    # 获取用户的练习记录
    user_records = PracticeRecord.query.filter_by(
        user_id=current_user.id,
        practice_id=practice_id
    ).order_by(PracticeRecord.created_at.desc()).limit(10).all()
    
    # 计算用户在这个曲目上的统计信息
    total_attempts = len(user_records)
    best_score = max([record.score for record in user_records if record.score], default=0)
    avg_score = sum([record.score for record in user_records if record.score]) / max(total_attempts, 1) if user_records else 0
    
    stats = {
        'total_attempts': total_attempts,
        'best_score': round(best_score, 1),
        'average_score': round(avg_score, 1),
        'last_practice': user_records[0].created_at if user_records else None
    }
    
    return render_template('practice_detail.html', 
                         practice=practice, 
                         records=user_records, 
                         stats=stats)

@main.route('/practices/<int:practice_id>/upload', methods=['GET', 'POST'])
@login_required
def practice_upload(practice_id):
    """练习音频上传页面"""
    # 如果是老师，重定向到老师仪表板
    if current_user.has_role('teacher'):
        return redirect(url_for('teacher.dashboard'))
    
    practice = Practice.query.get_or_404(practice_id)
    
    if not practice.is_active:
        flash('该练习曲目不可用', 'error')
        return redirect(url_for('main.practices'))
    
    if request.method == 'POST':
        if 'audio_file' not in request.files:
            flash('请选择音频文件', 'error')
            return render_template('practice_upload.html', practice=practice)
        
        file = request.files['audio_file']
        if file.filename == '':
            flash('请选择音频文件', 'error')
            return render_template('practice_upload.html', practice=practice)
        
        try:
            from app.utils.file_handler import allowed_file, save_audio_file
            from app.utils.ai_analysis import analyze_audio_practice
            from app.models.practice import AudioFile
            
            if not allowed_file(file.filename):
                flash('不支持的文件格式', 'error')
                return render_template('practice_upload.html', practice=practice)
            
            # 创建练习记录
            practice_record = PracticeRecord(
                user_id=current_user.id,
                practice_id=practice_id,
                status='analyzing'
            )
            db.session.add(practice_record)
            db.session.flush()  # 获取ID
            
            # 保存音频文件
            filename = save_audio_file(file, practice_record.id)
            
            # 创建音频文件记录
            audio_file = AudioFile(
                practice_record_id=practice_record.id,
                filename=filename,
                original_filename=file.filename,
                file_path=filename,
                file_size=len(file.read()),
                file_type=file.content_type
            )
            
            file.seek(0)  # 重置文件指针
            db.session.add(audio_file)
            db.session.commit()
            
            # AI分析音频
            from flask import current_app
            import os
            full_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            analysis_result = analyze_audio_practice(full_path, practice)
            
            # 更新练习记录
            practice_record.score = analysis_result.get('score', 0)
            practice_record.tempo_accuracy = analysis_result.get('tempo_accuracy', 0)
            practice_record.pitch_accuracy = analysis_result.get('pitch_accuracy', 0)
            practice_record.rhythm_accuracy = analysis_result.get('rhythm_accuracy', 0)
            practice_record.ai_feedback = analysis_result.get('feedback', '')
            
            # 处理建议列表转换为字符串
            suggestions = analysis_result.get('suggestions', [])
            if isinstance(suggestions, list):
                practice_record.improvement_suggestions = '\n'.join(f"• {suggestion}" for suggestion in suggestions)
            else:
                practice_record.improvement_suggestions = str(suggestions)
            
            practice_record.status = 'completed'
            
            db.session.commit()
            
            # 清除用户统计缓存，因为数据已更新
            from app.utils.cache import invalidate_user_stats
            invalidate_user_stats(current_user.id)
            
            flash('音频上传成功，AI分析完成！', 'success')
            return redirect(url_for('main.practice_result', record_id=practice_record.id))
            
        except Exception as e:
            db.session.rollback()
            flash('上传失败，请稍后重试', 'error')
            print(f"上传错误: {e}")
    
    return render_template('practice_upload.html', practice=practice)

@main.route('/practice-result/<int:record_id>')
@login_required
def practice_result(record_id):
    """练习结果页面"""
    # 如果是老师，重定向到老师仪表板
    if current_user.has_role('teacher'):
        return redirect(url_for('teacher.dashboard'))
    
    record = PracticeRecord.query.filter_by(
        id=record_id, 
        user_id=current_user.id
    ).first_or_404()
    
    return render_template('practice_result.html', record=record)

@main.route('/stats')
@login_required
def user_stats():
    """用户统计页面"""
    # 如果是老师，重定向到老师仪表板
    if current_user.has_role('teacher'):
        return redirect(url_for('teacher.dashboard'))
    
    from datetime import datetime, timedelta
    import calendar
    
    # 基础统计
    total_practices = PracticeRecord.query.filter_by(user_id=current_user.id).count()
    completed_practices = PracticeRecord.query.filter_by(
        user_id=current_user.id, 
        status='completed'
    ).count()
    
    # 分数统计
    completed_records = PracticeRecord.query.filter_by(
        user_id=current_user.id, 
        status='completed'
    ).all()
    
    scores = [r.score for r in completed_records if r.score is not None]
    avg_score = sum(scores) / len(scores) if scores else 0
    best_score = max(scores) if scores else 0
    
    # 准确度统计
    tempo_accuracies = [r.tempo_accuracy for r in completed_records if r.tempo_accuracy is not None]
    pitch_accuracies = [r.pitch_accuracy for r in completed_records if r.pitch_accuracy is not None]
    rhythm_accuracies = [r.rhythm_accuracy for r in completed_records if r.rhythm_accuracy is not None]
    
    avg_tempo = sum(tempo_accuracies) / len(tempo_accuracies) if tempo_accuracies else 0
    avg_pitch = sum(pitch_accuracies) / len(pitch_accuracies) if pitch_accuracies else 0
    avg_rhythm = sum(rhythm_accuracies) / len(rhythm_accuracies) if rhythm_accuracies else 0
    
    # 最近30天练习趋势
    thirty_days_ago = datetime.now() - timedelta(days=30)
    daily_stats = {}
    
    for i in range(30):
        date = (datetime.now() - timedelta(days=i)).date()
        daily_count = PracticeRecord.query.filter(
            PracticeRecord.user_id == current_user.id,
            db.func.date(PracticeRecord.created_at) == date
        ).count()
        daily_stats[date.strftime('%Y-%m-%d')] = daily_count
    
    # 月度统计
    monthly_stats = {}
    for i in range(6):  # 最近6个月
        date = datetime.now().replace(day=1) - timedelta(days=i * 30)
        month_start = date.replace(day=1)
        if i == 0:
            month_end = datetime.now()
        else:
            next_month = month_start.replace(month=month_start.month + 1) if month_start.month < 12 else month_start.replace(year=month_start.year + 1, month=1)
            month_end = next_month - timedelta(days=1)
        
        month_count = PracticeRecord.query.filter(
            PracticeRecord.user_id == current_user.id,
            PracticeRecord.created_at >= month_start,
            PracticeRecord.created_at <= month_end
        ).count()
        
        month_label = f"{month_start.year}-{month_start.month:02d}"
        monthly_stats[month_label] = month_count
    
    # 难度分布统计
    difficulty_stats = {}
    for record in completed_records:
        difficulty = record.practice.difficulty_level
        if difficulty not in difficulty_stats:
            difficulty_stats[difficulty] = {'count': 0, 'total_score': 0}
        difficulty_stats[difficulty]['count'] += 1
        if record.score:
            difficulty_stats[difficulty]['total_score'] += record.score
    
    # 计算难度平均分
    for difficulty in difficulty_stats:
        if difficulty_stats[difficulty]['count'] > 0:
            difficulty_stats[difficulty]['avg_score'] = difficulty_stats[difficulty]['total_score'] / difficulty_stats[difficulty]['count']
        else:
            difficulty_stats[difficulty]['avg_score'] = 0
    
    # 练习最多的曲目 TOP 5
    popular_practices = db.session.query(
        Practice.title, 
        Practice.composer,
        db.func.count(PracticeRecord.id).label('practice_count'),
        db.func.avg(PracticeRecord.score).label('avg_score')
    ).join(PracticeRecord).filter(
        PracticeRecord.user_id == current_user.id
    ).group_by(Practice.id).order_by(
        db.func.count(PracticeRecord.id).desc()
    ).limit(5).all()
    
    # 最近的成就
    achievements = []
    
    # 连续练习天数
    if total_practices >= 10:
        achievements.append({
            'title': '练习达人',
            'description': '完成10次练习',
            'icon': 'fas fa-music',
            'color': 'success'
        })
    
    if avg_score >= 85:
        achievements.append({
            'title': '优秀表现',
            'description': '平均分达到85分',
            'icon': 'fas fa-star',
            'color': 'warning'
        })
    
    if best_score >= 95:
        achievements.append({
            'title': '完美演奏',
            'description': '单次练习达到95分',
            'icon': 'fas fa-trophy',
            'color': 'success'
        })
    
    return render_template('user_stats.html',
                         total_practices=total_practices,
                         completed_practices=completed_practices,
                         success_rate=round((completed_practices / total_practices * 100), 1) if total_practices > 0 else 0,
                         avg_score=round(avg_score, 1),
                         best_score=round(best_score, 1),
                         avg_tempo=round(avg_tempo, 1),
                         avg_pitch=round(avg_pitch, 1),
                         avg_rhythm=round(avg_rhythm, 1),
                         daily_stats=daily_stats,
                         monthly_stats=monthly_stats,
                         difficulty_stats=difficulty_stats,
                         popular_practices=popular_practices,
                         achievements=achievements)


@main.route('/practice-records')
@login_required
def practice_records():
    """练习记录列表页面"""
    # 如果是老师，重定向到老师仪表板
    if current_user.has_role('teacher'):
        return redirect(url_for('teacher.dashboard'))
    
    from datetime import datetime, timedelta
    
    # 获取分页参数
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    # 获取筛选参数
    status_filter = request.args.get('status', '')
    practice_filter = request.args.get('practice', '', type=int)
    date_filter = request.args.get('date', '')
    
    # 构建查询
    query = PracticeRecord.query.filter_by(user_id=current_user.id)\
        .join(Practice)
    
    # 应用筛选条件
    if status_filter:
        query = query.filter(PracticeRecord.status == status_filter)
    
    if practice_filter:
        query = query.filter(PracticeRecord.practice_id == practice_filter)
    
    if date_filter:
        if date_filter == 'today':
            today = datetime.now().date()
            query = query.filter(db.func.date(PracticeRecord.created_at) == today)
        elif date_filter == 'week':
            week_ago = datetime.now() - timedelta(days=7)
            query = query.filter(PracticeRecord.created_at >= week_ago)
        elif date_filter == 'month':
            month_ago = datetime.now() - timedelta(days=30)
            query = query.filter(PracticeRecord.created_at >= month_ago)
    
    # 分页查询
    records = query.order_by(PracticeRecord.created_at.desc())\
        .paginate(page=page, per_page=per_page, error_out=False)
    
    # 获取用户练习过的所有曲目（用于筛选下拉框）
    practiced_pieces = db.session.query(Practice.id, Practice.title)\
        .join(PracticeRecord)\
        .filter(PracticeRecord.user_id == current_user.id)\
        .distinct().order_by(Practice.title).all()
    
    # 统计信息
    total_records = PracticeRecord.query.filter_by(user_id=current_user.id).count()
    completed_records = PracticeRecord.query.filter_by(
        user_id=current_user.id, 
        status='completed'
    ).count()
    avg_score = db.session.query(db.func.avg(PracticeRecord.score))\
        .filter(PracticeRecord.user_id == current_user.id,
                PracticeRecord.status == 'completed').scalar()
    
    stats = {
        'total_records': total_records,
        'completed_records': completed_records,
        'success_rate': round((completed_records / total_records * 100), 1) if total_records > 0 else 0,
        'average_score': round(avg_score, 1) if avg_score else 0
    }
    
    return render_template('practice_records.html', 
                         records=records, 
                         practiced_pieces=practiced_pieces,
                         stats=stats,
                         current_filters={
                             'status': status_filter,
                             'practice': practice_filter,
                             'date': date_filter
                         })

@main.route('/cache-stats')
@login_required
def cache_stats():
    """缓存统计信息（仅管理员可见）"""
    if not current_user.has_role('admin'):
        flash('权限不足', 'error')
        return redirect(url_for('main.dashboard'))
    
    from app.utils.cache import get_cache_stats, cleanup_expired_cache
    
    # 清理过期缓存
    cleaned_count = cleanup_expired_cache()
    
    # 获取缓存统计
    stats = get_cache_stats()
    stats['cleaned_items'] = cleaned_count
    
    return render_template('cache_stats.html', stats=stats)

@main.route('/clear-cache')
@login_required
def clear_cache():
    """清空缓存（仅管理员可用）"""
    if not current_user.has_role('admin'):
        flash('权限不足', 'error')
        return redirect(url_for('main.dashboard'))
    
    from app.utils.cache import CacheManager
    
    cache_type = request.args.get('type', 'all')
    
    if cache_type == 'user':
        CacheManager.clear('user_data')
        flash('用户缓存已清空', 'success')
    elif cache_type == 'common':
        CacheManager.clear('common')
        flash('公共缓存已清空', 'success')
    else:
        CacheManager.clear()
        flash('所有缓存已清空', 'success')
    
    return redirect(url_for('main.cache_stats'))

@main.route('/about')
def about():
    """关于页面"""
    return render_template('about.html')

@main.route('/contact', methods=['GET', 'POST'])
def contact():
    """联系页面"""
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        
        name = data.get('name', '').strip()
        email = data.get('email', '').strip().lower()
        subject = data.get('subject', '').strip()
        message = data.get('message', '').strip()
        
        # 验证表单数据
        if not all([name, email, subject, message]):
            error_msg = '请填写所有必填字段'
            if request.is_json:
                return jsonify({'error': error_msg}), 400
            flash(error_msg, 'error')
            return render_template('contact.html')
        
        # 简单的邮箱格式验证
        if '@' not in email or '.' not in email:
            error_msg = '请输入有效的邮箱地址'
            if request.is_json:
                return jsonify({'error': error_msg}), 400
            flash(error_msg, 'error')
            return render_template('contact.html')
        
        try:
            # 保存联系消息到数据库
            from app.models.auth import ContactMessage
            contact_msg = ContactMessage(
                name=name,
                email=email,
                subject=subject,
                message=message
            )
            db.session.add(contact_msg)
            db.session.commit()
            
            # 发送通知邮件给管理员（可选）
            try:
                from app.utils.email import send_contact_notification
                send_contact_notification(contact_msg)
            except Exception as e:
                # 邮件发送失败不影响表单提交
                print(f"联系表单通知邮件发送失败: {e}")
            
            success_msg = '您的消息已发送成功，我们会尽快回复您！'
            if request.is_json:
                return jsonify({'message': success_msg}), 200
            
            flash(success_msg, 'success')
            return redirect(url_for('main.contact'))
            
        except Exception as e:
            db.session.rollback()
            error_msg = '发送失败，请稍后重试'
            if request.is_json:
                return jsonify({'error': error_msg}), 500
            flash(error_msg, 'error')
    
    return render_template('contact.html')

@main.route('/privacy')
def privacy():
    """隐私政策页面"""
    return render_template('privacy.html')

@main.route('/terms')
def terms():
    """服务条款页面"""
    return render_template('terms.html')

@main.route('/health')
def health_check():
    """健康检查接口"""
    return jsonify({
        'status': 'healthy',
        'service': 'aimuspal-web',
        'version': '1.0.0'
    })

@main.route('/test-buttons')
def test_buttons():
    """按钮测试页面"""
    import os
    return send_file(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'test_simple_buttons.html'))

@main.route('/button-test')
def button_test():
    """按钮功能测试页面"""
    import os
    return send_file(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'button_test.html'))
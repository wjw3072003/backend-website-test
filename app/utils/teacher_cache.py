"""
老师端缓存优化模块
提供老师端特有的缓存策略和高效缓存方法
"""

from flask import current_app
from functools import wraps
import hashlib
import json
from datetime import datetime, timedelta

from app.utils.cache import CacheManager

class TeacherCacheManager:
    """老师端缓存管理器"""
    
    CACHE_PREFIX = "teacher"
    
    # 缓存TTL配置（秒）
    CACHE_TTL = {
        'teacher_stats': 300,      # 5分钟 - 老师统计数据
        'teacher_classes': 600,    # 10分钟 - 老师班级列表
        'teacher_students': 600,   # 10分钟 - 老师学生列表
        'teacher_assignments': 300, # 5分钟 - 老师作业列表
        'class_students': 1200,    # 20分钟 - 班级学生列表
        'assignment_grades': 180,  # 3分钟 - 作业成绩统计
        'teacher_reports': 1800,   # 30分钟 - 教学报告数据
        'grade_stats': 300,        # 5分钟 - 成绩统计
    }
    
    @staticmethod
    def _get_cache_key(prefix, teacher_id, key, params=None):
        """生成老师端缓存键"""
        base_key = f"{TeacherCacheManager.CACHE_PREFIX}:{prefix}:teacher_{teacher_id}:{key}"
        
        if params:
            # 将参数转换为确定性字符串
            param_str = json.dumps(params, sort_keys=True)
            param_hash = hashlib.md5(param_str.encode()).hexdigest()[:8]
            base_key += f":{param_hash}"
        
        return base_key
    
    @staticmethod
    def get_teacher_stats(teacher_id):
        """获取老师统计数据缓存"""
        cache_key = TeacherCacheManager._get_cache_key('stats', teacher_id, 'dashboard')
        return CacheManager.get(cache_key, TeacherCacheManager.CACHE_PREFIX)
    
    @staticmethod
    def set_teacher_stats(teacher_id, stats):
        """设置老师统计数据缓存"""
        cache_key = TeacherCacheManager._get_cache_key('stats', teacher_id, 'dashboard')
        ttl = TeacherCacheManager.CACHE_TTL['teacher_stats']
        CacheManager.set(cache_key, stats, ttl, TeacherCacheManager.CACHE_PREFIX)
    
    @staticmethod
    def get_teacher_classes(teacher_id):
        """获取老师班级列表缓存"""
        cache_key = TeacherCacheManager._get_cache_key('data', teacher_id, 'classes')
        return CacheManager.get(cache_key, TeacherCacheManager.CACHE_PREFIX)
    
    @staticmethod
    def set_teacher_classes(teacher_id, classes):
        """设置老师班级列表缓存"""
        cache_key = TeacherCacheManager._get_cache_key('data', teacher_id, 'classes')
        ttl = TeacherCacheManager.CACHE_TTL['teacher_classes']
        CacheManager.set(cache_key, classes, ttl, TeacherCacheManager.CACHE_PREFIX)
    
    @staticmethod
    def get_teacher_students(teacher_id, class_id=None):
        """获取老师学生列表缓存"""
        params = {'class_id': class_id} if class_id else None
        cache_key = TeacherCacheManager._get_cache_key('data', teacher_id, 'students', params)
        return CacheManager.get(cache_key, TeacherCacheManager.CACHE_PREFIX)
    
    @staticmethod
    def set_teacher_students(teacher_id, students, class_id=None):
        """设置老师学生列表缓存"""
        params = {'class_id': class_id} if class_id else None
        cache_key = TeacherCacheManager._get_cache_key('data', teacher_id, 'students', params)
        ttl = TeacherCacheManager.CACHE_TTL['teacher_students']
        CacheManager.set(cache_key, students, ttl, TeacherCacheManager.CACHE_PREFIX)
    
    @staticmethod
    def get_assignment_grades(assignment_id):
        """获取作业成绩统计缓存"""
        cache_key = f"{TeacherCacheManager.CACHE_PREFIX}:grades:assignment_{assignment_id}"
        return CacheManager.get(cache_key, TeacherCacheManager.CACHE_PREFIX)
    
    @staticmethod
    def set_assignment_grades(assignment_id, grade_stats):
        """设置作业成绩统计缓存"""
        cache_key = f"{TeacherCacheManager.CACHE_PREFIX}:grades:assignment_{assignment_id}"
        ttl = TeacherCacheManager.CACHE_TTL['assignment_grades']
        CacheManager.set(cache_key, grade_stats, ttl, TeacherCacheManager.CACHE_PREFIX)
    
    @staticmethod
    def get_teacher_report(teacher_id, report_type, time_range, class_id=None):
        """获取教学报告缓存"""
        params = {
            'type': report_type,
            'time_range': time_range,
            'class_id': class_id
        }
        cache_key = TeacherCacheManager._get_cache_key('reports', teacher_id, 'data', params)
        return CacheManager.get(cache_key, TeacherCacheManager.CACHE_PREFIX)
    
    @staticmethod
    def set_teacher_report(teacher_id, report_data, report_type, time_range, class_id=None):
        """设置教学报告缓存"""
        params = {
            'type': report_type,
            'time_range': time_range,
            'class_id': class_id
        }
        cache_key = TeacherCacheManager._get_cache_key('reports', teacher_id, 'data', params)
        ttl = TeacherCacheManager.CACHE_TTL['teacher_reports']
        CacheManager.set(cache_key, report_data, ttl, TeacherCacheManager.CACHE_PREFIX)
    
    @staticmethod
    def invalidate_teacher_cache(teacher_id):
        """清空指定老师的所有缓存"""
        prefix = f"{TeacherCacheManager.CACHE_PREFIX}:*:teacher_{teacher_id}:*"
        CacheManager.clear(prefix)
    
    @staticmethod
    def invalidate_class_cache(class_id):
        """清空指定班级相关的缓存"""
        # 这里需要更复杂的逻辑来清理与班级相关的所有缓存
        prefix = f"{TeacherCacheManager.CACHE_PREFIX}:*:*:*class_{class_id}*"
        CacheManager.clear(prefix)
    
    @staticmethod
    def invalidate_assignment_cache(assignment_id):
        """清空指定作业相关的缓存"""
        cache_key = f"{TeacherCacheManager.CACHE_PREFIX}:grades:assignment_{assignment_id}"
        CacheManager.delete(cache_key, TeacherCacheManager.CACHE_PREFIX)

def teacher_cache(cache_type, ttl=None, key_params=None):
    """老师端缓存装饰器"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 从参数中获取teacher_id（通常是第一个参数或current_user.id）
            teacher_id = None
            if args and hasattr(args[0], 'id'):
                teacher_id = args[0].id
            elif 'teacher_id' in kwargs:
                teacher_id = kwargs['teacher_id']
            
            if not teacher_id:
                # 无法确定teacher_id，直接执行函数
                return func(*args, **kwargs)
            
            # 生成缓存键
            params = {}
            if key_params:
                for param in key_params:
                    if param in kwargs:
                        params[param] = kwargs[param]
            
            cache_key = TeacherCacheManager._get_cache_key(cache_type, teacher_id, func.__name__, params)
            
            # 尝试从缓存获取
            cached_result = CacheManager.get(cache_key, TeacherCacheManager.CACHE_PREFIX)
            if cached_result is not None:
                return cached_result
            
            # 执行函数并缓存结果
            result = func(*args, **kwargs)
            
            cache_ttl = ttl or TeacherCacheManager.CACHE_TTL.get(cache_type, 300)
            CacheManager.set(cache_key, result, cache_ttl, TeacherCacheManager.CACHE_PREFIX)
            
            return result
        return wrapper
    return decorator

def cache_teacher_stats(ttl=300):
    """老师统计数据缓存装饰器"""
    return teacher_cache('stats', ttl=ttl)

def cache_teacher_data(data_type, ttl=600):
    """老师数据缓存装饰器"""
    return teacher_cache('data', ttl=ttl, key_params=[data_type])

def cache_teacher_reports(ttl=1800):
    """老师报告缓存装饰器"""
    return teacher_cache('reports', ttl=ttl, key_params=['report_type', 'time_range', 'class_id'])

# 缓存预热功能
class TeacherCacheWarmer:
    """老师端缓存预热器"""
    
    @staticmethod
    def warm_teacher_dashboard(teacher_id):
        """预热老师仪表板缓存"""
        from app.models.teacher_simple import Class, Assignment, Grade
        from app.models.user import User
        from sqlalchemy import func
        
        try:
            # 预热基础统计数据
            teacher_classes = Class.query.filter(Class.teachers.any(User.id == teacher_id)).all()
            class_ids = [cls.id for cls in teacher_classes]
            
            stats = {
                'total_classes': len(teacher_classes),
                'total_students': len(set([student.id for cls in teacher_classes for student in cls.students])),
                'total_assignments': Assignment.query.filter_by(teacher_id=teacher_id).count(),
                'pending_grades': Grade.query.filter_by(status='pending').join(Assignment).filter(Assignment.teacher_id == teacher_id).count()
            }
            
            TeacherCacheManager.set_teacher_stats(teacher_id, stats)
            TeacherCacheManager.set_teacher_classes(teacher_id, teacher_classes)
            
            current_app.logger.info(f"预热老师 {teacher_id} 的仪表板缓存完成")
            return True
            
        except Exception as e:
            current_app.logger.error(f"预热老师 {teacher_id} 缓存失败: {e}")
            return False
    
    @staticmethod
    def warm_all_active_teachers():
        """预热所有活跃老师的缓存"""
        from app.models.user import User
        
        try:
            # 获取所有有老师角色的用户
            teachers = User.query.filter(User.roles.any(name='teacher')).filter_by(is_active=True).all()
            
            warmed_count = 0
            for teacher in teachers:
                if TeacherCacheWarmer.warm_teacher_dashboard(teacher.id):
                    warmed_count += 1
            
            current_app.logger.info(f"预热 {warmed_count}/{len(teachers)} 个老师的缓存")
            return warmed_count
            
        except Exception as e:
            current_app.logger.error(f"批量预热老师缓存失败: {e}")
            return 0

# 缓存统计和监控
def get_teacher_cache_stats():
    """获取老师端缓存统计"""
    from app.utils.cache import get_cache_stats
    
    overall_stats = get_cache_stats()
    
    # 统计老师端专用缓存
    teacher_cache_count = 0
    teacher_cache_size = 0
    
    # 这里可以添加更详细的老师端缓存统计逻辑
    
    return {
        'overall': overall_stats,
        'teacher_specific': {
            'cache_count': teacher_cache_count,
            'estimated_size_mb': teacher_cache_size,
            'hit_rate': 'N/A'  # 可以添加命中率统计
        }
    }

def optimize_teacher_cache():
    """优化老师端缓存性能"""
    try:
        # 清理过期缓存
        from app.utils.cache import cleanup_expired_cache
        cleaned = cleanup_expired_cache()
        
        # 预热活跃老师缓存
        warmed = TeacherCacheWarmer.warm_all_active_teachers()
        
        return {
            'cleaned_expired': cleaned,
            'warmed_teachers': warmed,
            'status': 'success'
        }
        
    except Exception as e:
        current_app.logger.error(f"优化老师端缓存失败: {e}")
        return {
            'status': 'error',
            'message': str(e)
        } 
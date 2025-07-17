"""
缓存工具函数
提供学生端常用的缓存功能
"""

from flask import current_app, session
from functools import wraps
import json
import hashlib
from datetime import datetime, timedelta
import pickle

# 内存缓存字典 (生产环境建议使用Redis)
_memory_cache = {}

class CacheManager:
    """缓存管理器"""
    
    @staticmethod
    def _get_cache_key(prefix, key):
        """生成缓存键"""
        return f"{prefix}:{key}"
    
    @staticmethod
    def _is_expired(timestamp, ttl):
        """检查是否过期"""
        if ttl is None:
            return False
        return datetime.now() > timestamp + timedelta(seconds=ttl)
    
    @staticmethod
    def set(key, value, ttl=None, prefix="default"):
        """设置缓存"""
        cache_key = CacheManager._get_cache_key(prefix, key)
        _memory_cache[cache_key] = {
            'value': value,
            'timestamp': datetime.now(),
            'ttl': ttl
        }
    
    @staticmethod
    def get(key, prefix="default", default=None):
        """获取缓存"""
        cache_key = CacheManager._get_cache_key(prefix, key)
        
        if cache_key not in _memory_cache:
            return default
        
        cached_item = _memory_cache[cache_key]
        
        # 检查是否过期
        if CacheManager._is_expired(cached_item['timestamp'], cached_item['ttl']):
            del _memory_cache[cache_key]
            return default
        
        return cached_item['value']
    
    @staticmethod
    def delete(key, prefix="default"):
        """删除缓存"""
        cache_key = CacheManager._get_cache_key(prefix, key)
        if cache_key in _memory_cache:
            del _memory_cache[cache_key]
    
    @staticmethod
    def clear(prefix=None):
        """清空缓存"""
        if prefix is None:
            _memory_cache.clear()
        else:
            keys_to_delete = [key for key in _memory_cache.keys() if key.startswith(f"{prefix}:")]
            for key in keys_to_delete:
                del _memory_cache[key]

def cache_result(ttl=300, prefix="query"):
    """查询结果缓存装饰器"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 生成缓存键
            cache_key = f"{func.__name__}:{hashlib.md5(str(args + tuple(kwargs.items())).encode()).hexdigest()}"
            
            # 尝试从缓存获取
            cached_result = CacheManager.get(cache_key, prefix)
            if cached_result is not None:
                return cached_result
            
            # 执行函数并缓存结果
            result = func(*args, **kwargs)
            CacheManager.set(cache_key, result, ttl, prefix)
            
            return result
        return wrapper
    return decorator

def cache_user_data(user_id, key, value, ttl=600):
    """缓存用户相关数据"""
    CacheManager.set(f"user_{user_id}_{key}", value, ttl, "user_data")

def get_user_cache(user_id, key, default=None):
    """获取用户缓存数据"""
    return CacheManager.get(f"user_{user_id}_{key}", "user_data", default)

def clear_user_cache(user_id):
    """清空用户缓存"""
    # 查找并删除用户相关的所有缓存
    user_prefix = f"user_data:user_{user_id}_"
    keys_to_delete = [key for key in _memory_cache.keys() if key.startswith(user_prefix)]
    for key in keys_to_delete:
        del _memory_cache[key]

def cache_practice_data(practice_id, key, value, ttl=1800):
    """缓存练习曲目数据"""
    CacheManager.set(f"practice_{practice_id}_{key}", value, ttl, "practice_data")

def get_practice_cache(practice_id, key, default=None):
    """获取练习曲目缓存"""
    return CacheManager.get(f"practice_{practice_id}_{key}", "practice_data", default)

def session_cache(key, value=None, ttl=1800):
    """会话级缓存"""
    if value is not None:
        # 设置会话缓存
        session[f"cache_{key}"] = {
            'value': value,
            'expires': (datetime.now() + timedelta(seconds=ttl)).timestamp()
        }
        return value
    else:
        # 获取会话缓存
        cached_item = session.get(f"cache_{key}")
        if cached_item and datetime.now().timestamp() < cached_item['expires']:
            return cached_item['value']
        return None

def get_stats_cache(user_id):
    """获取用户统计缓存"""
    return get_user_cache(user_id, "stats")

def set_stats_cache(user_id, stats):
    """设置用户统计缓存"""
    cache_user_data(user_id, "stats", stats, ttl=300)  # 5分钟缓存

def invalidate_user_stats(user_id):
    """使用户统计缓存失效"""
    CacheManager.delete(f"user_{user_id}_stats", "user_data")

# 预加载缓存函数
def preload_common_data():
    """预加载常用数据"""
    try:
        from app.models import Practice
        
        # 缓存活跃的练习曲目
        active_practices = Practice.query.filter_by(is_active=True).all()
        CacheManager.set("active_practices", active_practices, ttl=1800, prefix="common")
        
        # 缓存难度选项
        difficulty_levels = [p.difficulty_level for p in active_practices]
        unique_levels = sorted(list(set(difficulty_levels)))
        CacheManager.set("difficulty_levels", unique_levels, ttl=3600, prefix="common")
        
        # 缓存风格选项
        genres = [p.genre for p in active_practices if p.genre]
        unique_genres = sorted(list(set(genres)))
        CacheManager.set("genres", unique_genres, ttl=3600, prefix="common")
        
        current_app.logger.info("预加载缓存完成")
        
    except Exception as e:
        current_app.logger.error(f"预加载缓存失败: {e}")

def get_common_cache(key, default=None):
    """获取公共缓存数据"""
    return CacheManager.get(key, "common", default)

# 缓存清理函数
def cleanup_expired_cache():
    """清理过期缓存"""
    current_time = datetime.now()
    expired_keys = []
    
    for cache_key, cached_item in _memory_cache.items():
        if CacheManager._is_expired(cached_item['timestamp'], cached_item['ttl']):
            expired_keys.append(cache_key)
    
    for key in expired_keys:
        del _memory_cache[key]
    
    return len(expired_keys)

def get_cache_stats():
    """获取缓存统计信息"""
    total_items = len(_memory_cache)
    expired_count = 0
    size_estimate = 0
    
    current_time = datetime.now()
    
    for cached_item in _memory_cache.values():
        if CacheManager._is_expired(cached_item['timestamp'], cached_item['ttl']):
            expired_count += 1
        try:
            size_estimate += len(pickle.dumps(cached_item['value']))
        except:
            size_estimate += 100  # 估算值
    
    return {
        'total_items': total_items,
        'expired_items': expired_count,
        'active_items': total_items - expired_count,
        'estimated_size_mb': round(size_estimate / 1024 / 1024, 2)
    }

# 为老师端提供的简化缓存接口
def get_cache(key, prefix="teacher", default=None):
    """获取缓存 - 老师端简化接口"""
    return CacheManager.get(key, prefix, default)

def set_cache(key, value, ttl=600, prefix="teacher"):
    """设置缓存 - 老师端简化接口"""
    CacheManager.set(key, value, ttl, prefix) 
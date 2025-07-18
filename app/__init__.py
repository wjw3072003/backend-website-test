import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_babel import Babel
import redis
from config import config

# 初始化扩展
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
mail = Mail()
jwt = JWTManager()
babel = Babel()
redis_client = None

def create_app(config_name=None):
    """应用工厂函数"""
    app = Flask(__name__, static_folder='../static', static_url_path='/static')
    
    # 加载配置
    config_name = config_name or os.environ.get('FLASK_ENV', 'default')
    app.config.from_object(config[config_name])
    
    # 初始化扩展
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    mail.init_app(app)
    jwt.init_app(app)
    CORS(app)
    
    # 定义语言选择器函数
    def get_locale():
        """获取当前语言"""
        from flask import request, session
        from flask_login import current_user
        
        # 优先使用URL参数中的语言
        if request.args.get('lang'):
            return request.args.get('lang')
        
        # 其次使用session中保存的语言
        if session.get('lang'):
            return session.get('lang')
        
        # 再次使用用户设置的语言
        if current_user.is_authenticated and hasattr(current_user, 'language'):
            return current_user.language
        
        # 最后使用浏览器语言
        return request.accept_languages.best_match(['zh_CN', 'zh_TW', 'en'])
    
    # 初始化Babel并设置语言选择器
    babel.init_app(app, locale_selector=get_locale)
    
    # 配置登录管理器
    login_manager.login_view = 'auth.login'
    login_manager.login_message = '请登录以访问此页面。'
    login_manager.login_message_category = 'info'
    
    # 初始化Redis
    global redis_client
    redis_client = redis.from_url(app.config['REDIS_URL'])
    
    # 注册蓝图
    from app.routes.main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    from app.routes.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    
    from app.routes.admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')
    
    from app.routes.api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')
    
    from app.routes.teacher import teacher as teacher_blueprint
    app.register_blueprint(teacher_blueprint, url_prefix='/teacher')
    
    from app.routes.i18n import i18n as i18n_blueprint
    app.register_blueprint(i18n_blueprint, url_prefix='/i18n')
    
    # 导入模型以确保数据表创建
    from app.models.user import User, Role
    from app.models.practice import Practice, PracticeRecord, AudioFile
    from app.models.teacher_simple import (
        Class, Assignment, Grade, TeachingResource, 
        Announcement, Attendance
    )
    
    # 创建上传目录
    upload_folder = app.config['UPLOAD_FOLDER']
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
    
    # 应用启动后预加载缓存
    with app.app_context():
        try:
            from app.utils.cache import preload_common_data
            preload_common_data()
        except Exception as e:
            app.logger.error(f"预加载缓存失败: {e}")
    
    return app

@login_manager.user_loader
def load_user(user_id):
    """加载用户回调函数"""
    from app.models.user import User
    return User.query.get(int(user_id))
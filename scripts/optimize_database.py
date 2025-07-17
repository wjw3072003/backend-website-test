#!/usr/bin/env python3
"""
数据库优化脚本
添加索引、新字段和统计表来提升性能
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app import create_app, db
from sqlalchemy import text
import logging

def optimize_database():
    """执行数据库优化"""
    app = create_app()
    
    with app.app_context():
        try:
            print("开始数据库优化...")
            
            # 1. 添加用户表索引
            print("1. 添加用户表索引...")
            db.session.execute(text("CREATE INDEX IF NOT EXISTS idx_user_email ON user (email)"))
            db.session.execute(text("CREATE INDEX IF NOT EXISTS idx_user_created_at ON user (created_at)"))
            db.session.execute(text("CREATE INDEX IF NOT EXISTS idx_user_is_active ON user (is_active)"))
            
            # 2. 添加练习表索引
            print("2. 添加练习表索引...")
            db.session.execute(text("CREATE INDEX IF NOT EXISTS idx_practice_title ON practice (title)"))
            db.session.execute(text("CREATE INDEX IF NOT EXISTS idx_practice_difficulty ON practice (difficulty_level)"))
            db.session.execute(text("CREATE INDEX IF NOT EXISTS idx_practice_genre ON practice (genre)"))
            db.session.execute(text("CREATE INDEX IF NOT EXISTS idx_practice_is_active ON practice (is_active)"))
            db.session.execute(text("CREATE INDEX IF NOT EXISTS idx_practice_created_at ON practice (created_at)"))
            
            # 3. 添加练习记录表索引
            print("3. 添加练习记录表索引...")
            db.session.execute(text("CREATE INDEX IF NOT EXISTS idx_practice_record_user_id ON practice_record (user_id)"))
            db.session.execute(text("CREATE INDEX IF NOT EXISTS idx_practice_record_practice_id ON practice_record (practice_id)"))
            db.session.execute(text("CREATE INDEX IF NOT EXISTS idx_practice_record_status ON practice_record (status)"))
            db.session.execute(text("CREATE INDEX IF NOT EXISTS idx_practice_record_created_at ON practice_record (created_at)"))
            db.session.execute(text("CREATE INDEX IF NOT EXISTS idx_practice_record_user_practice ON practice_record (user_id, practice_id)"))
            
            # 4. 添加音频文件表索引
            print("4. 添加音频文件表索引...")
            db.session.execute(text("CREATE INDEX IF NOT EXISTS idx_audio_file_practice_record_id ON audio_file (practice_record_id)"))
            db.session.execute(text("CREATE INDEX IF NOT EXISTS idx_audio_file_created_at ON audio_file (created_at)"))
            
            # 5. 添加联系消息表索引
            print("5. 添加联系消息表索引...")
            db.session.execute(text("CREATE INDEX IF NOT EXISTS idx_contact_message_status ON contact_message (status)"))
            db.session.execute(text("CREATE INDEX IF NOT EXISTS idx_contact_message_created_at ON contact_message (created_at)"))
            
            # 6. 添加用户统计字段
            print("6. 添加用户统计字段...")
            try:
                db.session.execute(text("ALTER TABLE user ADD COLUMN total_practices INT DEFAULT 0"))
            except Exception as e:
                if "Duplicate column name" not in str(e):
                    print(f"添加total_practices字段时出错: {e}")
            
            try:
                db.session.execute(text("ALTER TABLE user ADD COLUMN average_score DECIMAL(5,2) DEFAULT 0.0"))
            except Exception as e:
                if "Duplicate column name" not in str(e):
                    print(f"添加average_score字段时出错: {e}")
            
            try:
                db.session.execute(text("ALTER TABLE user ADD COLUMN best_score DECIMAL(5,2) DEFAULT 0.0"))
            except Exception as e:
                if "Duplicate column name" not in str(e):
                    print(f"添加best_score字段时出错: {e}")
            
            # 7. 添加练习曲目统计字段
            print("7. 添加练习曲目统计字段...")
            try:
                db.session.execute(text("ALTER TABLE practice ADD COLUMN practice_count INT DEFAULT 0"))
            except Exception as e:
                if "Duplicate column name" not in str(e):
                    print(f"添加practice_count字段时出错: {e}")
            
            try:
                db.session.execute(text("ALTER TABLE practice ADD COLUMN view_count INT DEFAULT 0"))
            except Exception as e:
                if "Duplicate column name" not in str(e):
                    print(f"添加view_count字段时出错: {e}")
            
            # 8. 创建系统设置表
            print("8. 创建系统设置表...")
            db.session.execute(text("""
                CREATE TABLE IF NOT EXISTS system_settings (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    setting_key VARCHAR(100) NOT NULL UNIQUE,
                    setting_value TEXT,
                    setting_type VARCHAR(20) DEFAULT 'string',
                    description TEXT,
                    is_public BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                )
            """))
            
            # 9. 创建用户活动日志表
            print("9. 创建用户活动日志表...")
            db.session.execute(text("""
                CREATE TABLE IF NOT EXISTS user_activity_log (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL,
                    action VARCHAR(50) NOT NULL,
                    resource_type VARCHAR(50),
                    resource_id INT,
                    ip_address VARCHAR(45),
                    details TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    INDEX idx_user_activity_user_id (user_id),
                    INDEX idx_user_activity_action (action),
                    INDEX idx_user_activity_created_at (created_at)
                )
            """))
            
            # 10. 插入默认系统设置
            print("10. 插入默认系统设置...")
            settings = [
                ('app_name', 'AiMusPal', 'string', '应用程序名称', True),
                ('app_version', '1.0.0', 'string', '应用程序版本', True),
                ('max_upload_size', '52428800', 'int', '最大上传文件大小（字节）', False),
                ('allowed_audio_formats', '["mp3", "wav", "m4a", "flac"]', 'json', '允许的音频格式', False),
                ('ai_analysis_timeout', '300', 'int', 'AI分析超时时间（秒）', False),
                ('practice_records_per_page', '20', 'int', '每页练习记录数', False),
                ('user_registration_enabled', 'true', 'boolean', '是否允许用户注册', True),
                ('maintenance_mode', 'false', 'boolean', '维护模式', True),
            ]
            
            for setting_key, setting_value, setting_type, description, is_public in settings:
                db.session.execute(text("""
                    INSERT IGNORE INTO system_settings 
                    (setting_key, setting_value, setting_type, description, is_public) 
                    VALUES (:key, :value, :type, :desc, :public)
                """), {
                    'key': setting_key,
                    'value': setting_value,
                    'type': setting_type,
                    'desc': description,
                    'public': is_public
                })
            
            # 11. 更新现有用户的统计数据
            print("11. 更新现有用户的统计数据...")
            db.session.execute(text("""
                UPDATE user u SET 
                    total_practices = (
                        SELECT COUNT(*) FROM practice_record pr 
                        WHERE pr.user_id = u.id AND pr.status = 'completed'
                    ),
                    average_score = (
                        SELECT COALESCE(AVG(pr.score), 0) FROM practice_record pr 
                        WHERE pr.user_id = u.id AND pr.status = 'completed' AND pr.score IS NOT NULL
                    ),
                    best_score = (
                        SELECT COALESCE(MAX(pr.score), 0) FROM practice_record pr 
                        WHERE pr.user_id = u.id AND pr.status = 'completed' AND pr.score IS NOT NULL
                    )
                WHERE u.id > 0
            """))
            
            # 12. 更新现有练习曲目的统计数据
            print("12. 更新现有练习曲目的统计数据...")
            db.session.execute(text("""
                UPDATE practice p SET 
                    practice_count = (
                        SELECT COUNT(*) FROM practice_record pr 
                        WHERE pr.practice_id = p.id AND pr.status = 'completed'
                    )
                WHERE p.id > 0
            """))
            
            # 提交所有更改
            db.session.commit()
            print("✅ 数据库优化完成！")
            
            # 显示优化结果
            print("\n📊 优化结果统计:")
            
            # 用户统计
            user_count = db.session.execute(text("SELECT COUNT(*) FROM user")).scalar()
            print(f"  - 用户总数: {user_count}")
            
            # 练习曲目统计
            practice_count = db.session.execute(text("SELECT COUNT(*) FROM practice")).scalar()
            print(f"  - 练习曲目总数: {practice_count}")
            
            # 练习记录统计
            record_count = db.session.execute(text("SELECT COUNT(*) FROM practice_record")).scalar()
            print(f"  - 练习记录总数: {record_count}")
            
            # 索引统计
            index_count = db.session.execute(text("""
                SELECT COUNT(*) FROM information_schema.statistics 
                WHERE table_schema = DATABASE() AND index_name LIKE 'idx_%'
            """)).scalar()
            print(f"  - 新增索引数量: {index_count}")
            
            print(f"  - 系统设置已配置: {len(settings)} 项")
            
        except Exception as e:
            print(f"❌ 数据库优化失败: {e}")
            db.session.rollback()
            raise
        
        finally:
            db.session.close()

if __name__ == '__main__':
    print("🚀 AiMusPal 数据库优化工具")
    print("=" * 50)
    
    # 确认执行
    confirm = input("是否要执行数据库优化？(输入 'yes' 确认): ")
    if confirm.lower() != 'yes':
        print("❌ 操作已取消")
        sys.exit(1)
    
    optimize_database()
    print("\n🎉 数据库优化完成！建议重启应用以确保所有更改生效。") 
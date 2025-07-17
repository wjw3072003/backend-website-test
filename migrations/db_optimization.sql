-- 数据库优化脚本
-- 执行前请备份数据库

-- 1. 为用户表添加索引
CREATE INDEX IF NOT EXISTS idx_user_email ON user (email);
CREATE INDEX IF NOT EXISTS idx_user_username ON user (username);
CREATE INDEX IF NOT EXISTS idx_user_created_at ON user (created_at);
CREATE INDEX IF NOT EXISTS idx_user_last_login ON user (last_login);
CREATE INDEX IF NOT EXISTS idx_user_is_active ON user (is_active);

-- 2. 为练习曲目表添加索引
CREATE INDEX IF NOT EXISTS idx_practice_title ON practice (title);
CREATE INDEX IF NOT EXISTS idx_practice_composer ON practice (composer);
CREATE INDEX IF NOT EXISTS idx_practice_difficulty ON practice (difficulty_level);
CREATE INDEX IF NOT EXISTS idx_practice_genre ON practice (genre);
CREATE INDEX IF NOT EXISTS idx_practice_is_active ON practice (is_active);
CREATE INDEX IF NOT EXISTS idx_practice_created_at ON practice (created_at);

-- 3. 为练习记录表添加索引
CREATE INDEX IF NOT EXISTS idx_practice_record_user_id ON practice_record (user_id);
CREATE INDEX IF NOT EXISTS idx_practice_record_practice_id ON practice_record (practice_id);
CREATE INDEX IF NOT EXISTS idx_practice_record_status ON practice_record (status);
CREATE INDEX IF NOT EXISTS idx_practice_record_score ON practice_record (score);
CREATE INDEX IF NOT EXISTS idx_practice_record_created_at ON practice_record (created_at);
CREATE INDEX IF NOT EXISTS idx_practice_record_user_practice ON practice_record (user_id, practice_id);

-- 4. 为音频文件表添加索引
CREATE INDEX IF NOT EXISTS idx_audio_file_practice_record_id ON audio_file (practice_record_id);
CREATE INDEX IF NOT EXISTS idx_audio_file_upload_status ON audio_file (upload_status);
CREATE INDEX IF NOT EXISTS idx_audio_file_created_at ON audio_file (created_at);

-- 5. 为联系消息表添加索引
CREATE INDEX IF NOT EXISTS idx_contact_message_status ON contact_message (status);
CREATE INDEX IF NOT EXISTS idx_contact_message_created_at ON contact_message (created_at);
CREATE INDEX IF NOT EXISTS idx_contact_message_email ON contact_message (email);

-- 6. 为密码重置令牌表添加索引
CREATE INDEX IF NOT EXISTS idx_password_reset_token_user_id ON password_reset_token (user_id);
CREATE INDEX IF NOT EXISTS idx_password_reset_token_token ON password_reset_token (token);
CREATE INDEX IF NOT EXISTS idx_password_reset_token_expires_at ON password_reset_token (expires_at);
CREATE INDEX IF NOT EXISTS idx_password_reset_token_used ON password_reset_token (used);

-- 7. 为用户表添加统计字段
ALTER TABLE user ADD COLUMN IF NOT EXISTS total_practices INT DEFAULT 0;
ALTER TABLE user ADD COLUMN IF NOT EXISTS average_score DECIMAL(5,2) DEFAULT 0.0;
ALTER TABLE user ADD COLUMN IF NOT EXISTS best_score DECIMAL(5,2) DEFAULT 0.0;
ALTER TABLE user ADD COLUMN IF NOT EXISTS total_practice_time INT DEFAULT 0; -- 总练习时间（秒）

-- 8. 为练习曲目表添加统计字段
ALTER TABLE practice ADD COLUMN IF NOT EXISTS practice_count INT DEFAULT 0; -- 被练习次数
ALTER TABLE practice ADD COLUMN IF NOT EXISTS average_score DECIMAL(5,2) DEFAULT 0.0; -- 平均分数
ALTER TABLE practice ADD COLUMN IF NOT EXISTS view_count INT DEFAULT 0; -- 查看次数

-- 9. 为练习记录表添加更多分析字段
ALTER TABLE practice_record ADD COLUMN IF NOT EXISTS analysis_version VARCHAR(20) DEFAULT '1.0'; -- AI分析版本
ALTER TABLE practice_record ADD COLUMN IF NOT EXISTS device_info VARCHAR(200); -- 录音设备信息
ALTER TABLE practice_record ADD COLUMN IF NOT EXISTS practice_notes TEXT; -- 用户练习笔记

-- 10. 为音频文件表添加更多信息字段
ALTER TABLE audio_file ADD COLUMN IF NOT EXISTS sample_rate INT; -- 采样率
ALTER TABLE audio_file ADD COLUMN IF NOT EXISTS bit_depth INT; -- 位深度
ALTER TABLE audio_file ADD COLUMN IF NOT EXISTS channels INT DEFAULT 1; -- 声道数
ALTER TABLE audio_file ADD COLUMN IF NOT EXISTS checksum VARCHAR(64); -- 文件校验和

-- 11. 创建用户活动日志表
CREATE TABLE IF NOT EXISTS user_activity_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    action VARCHAR(50) NOT NULL,
    resource_type VARCHAR(50),
    resource_id INT,
    ip_address VARCHAR(45),
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_user_activity_user_id (user_id),
    INDEX idx_user_activity_action (action),
    INDEX idx_user_activity_created_at (created_at),
    FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE
);

-- 12. 创建系统设置表
CREATE TABLE IF NOT EXISTS system_settings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    setting_key VARCHAR(100) NOT NULL UNIQUE,
    setting_value TEXT,
    setting_type VARCHAR(20) DEFAULT 'string', -- string, int, float, boolean, json
    description TEXT,
    is_public BOOLEAN DEFAULT FALSE, -- 是否可以公开访问
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_system_settings_key (setting_key),
    INDEX idx_system_settings_public (is_public)
);

-- 13. 创建练习计划表
CREATE TABLE IF NOT EXISTS practice_plan (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    target_practices_per_week INT DEFAULT 3,
    target_score DECIMAL(5,2) DEFAULT 80.0,
    start_date DATE,
    end_date DATE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_practice_plan_user_id (user_id),
    INDEX idx_practice_plan_is_active (is_active),
    INDEX idx_practice_plan_dates (start_date, end_date),
    FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE
);

-- 14. 创建练习计划详情表
CREATE TABLE IF NOT EXISTS practice_plan_detail (
    id INT AUTO_INCREMENT PRIMARY KEY,
    plan_id INT NOT NULL,
    practice_id INT NOT NULL,
    target_score DECIMAL(5,2) DEFAULT 80.0,
    is_completed BOOLEAN DEFAULT FALSE,
    completed_at TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_practice_plan_detail_plan_id (plan_id),
    INDEX idx_practice_plan_detail_practice_id (practice_id),
    INDEX idx_practice_plan_detail_completed (is_completed),
    FOREIGN KEY (plan_id) REFERENCES practice_plan(id) ON DELETE CASCADE,
    FOREIGN KEY (practice_id) REFERENCES practice(id) ON DELETE CASCADE,
    UNIQUE KEY unique_plan_practice (plan_id, practice_id)
);

-- 15. 创建用户成就表
CREATE TABLE IF NOT EXISTS user_achievement (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    achievement_type VARCHAR(50) NOT NULL, -- first_practice, perfect_score, streak_7, etc.
    achievement_data JSON, -- 成就相关数据
    earned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_user_achievement_user_id (user_id),
    INDEX idx_user_achievement_type (achievement_type),
    INDEX idx_user_achievement_earned_at (earned_at),
    FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE,
    UNIQUE KEY unique_user_achievement (user_id, achievement_type)
);

-- 16. 插入一些默认的系统设置
INSERT IGNORE INTO system_settings (setting_key, setting_value, setting_type, description, is_public) VALUES
('app_name', 'AiMusPal', 'string', '应用程序名称', true),
('app_version', '1.0.0', 'string', '应用程序版本', true),
('max_upload_size', '52428800', 'int', '最大上传文件大小（字节）', false),
('allowed_audio_formats', '["mp3", "wav", "m4a", "flac"]', 'json', '允许的音频格式', false),
('ai_analysis_timeout', '300', 'int', 'AI分析超时时间（秒）', false),
('practice_records_per_page', '20', 'int', '每页练习记录数', false),
('user_registration_enabled', 'true', 'boolean', '是否允许用户注册', true),
('email_verification_required', 'false', 'boolean', '是否需要邮箱验证', false),
('maintenance_mode', 'false', 'boolean', '维护模式', true),
('announcement_text', '', 'string', '公告文本', true);

-- 17. 创建触发器来自动更新统计数据
DELIMITER $$

-- 用户练习统计更新触发器
CREATE TRIGGER IF NOT EXISTS update_user_stats_after_practice_insert
AFTER INSERT ON practice_record
FOR EACH ROW
BEGIN
    UPDATE user SET 
        total_practices = (
            SELECT COUNT(*) FROM practice_record 
            WHERE user_id = NEW.user_id AND status = 'completed'
        ),
        average_score = (
            SELECT COALESCE(AVG(score), 0) FROM practice_record 
            WHERE user_id = NEW.user_id AND status = 'completed' AND score IS NOT NULL
        ),
        best_score = (
            SELECT COALESCE(MAX(score), 0) FROM practice_record 
            WHERE user_id = NEW.user_id AND status = 'completed' AND score IS NOT NULL
        ),
        total_practice_time = (
            SELECT COALESCE(SUM(duration), 0) FROM practice_record 
            WHERE user_id = NEW.user_id AND status = 'completed' AND duration IS NOT NULL
        )
    WHERE id = NEW.user_id;
END$$

-- 练习曲目统计更新触发器
CREATE TRIGGER IF NOT EXISTS update_practice_stats_after_record_insert
AFTER INSERT ON practice_record
FOR EACH ROW
BEGIN
    UPDATE practice SET 
        practice_count = (
            SELECT COUNT(*) FROM practice_record 
            WHERE practice_id = NEW.practice_id AND status = 'completed'
        ),
        average_score = (
            SELECT COALESCE(AVG(score), 0) FROM practice_record 
            WHERE practice_id = NEW.practice_id AND status = 'completed' AND score IS NOT NULL
        )
    WHERE id = NEW.practice_id;
END$$

DELIMITER ;

-- 18. 创建视图来简化常用查询
-- 用户练习统计视图
CREATE OR REPLACE VIEW user_practice_stats AS
SELECT 
    u.id as user_id,
    u.username,
    u.email,
    COUNT(pr.id) as total_practices,
    COALESCE(AVG(pr.score), 0) as average_score,
    COALESCE(MAX(pr.score), 0) as best_score,
    COALESCE(SUM(pr.duration), 0) as total_practice_time,
    MAX(pr.created_at) as last_practice_date,
    COUNT(DISTINCT pr.practice_id) as unique_practices_count
FROM user u
LEFT JOIN practice_record pr ON u.id = pr.user_id AND pr.status = 'completed'
GROUP BY u.id, u.username, u.email;

-- 练习曲目统计视图
CREATE OR REPLACE VIEW practice_stats AS
SELECT 
    p.id as practice_id,
    p.title,
    p.composer,
    p.difficulty_level,
    p.genre,
    COUNT(pr.id) as practice_count,
    COALESCE(AVG(pr.score), 0) as average_score,
    COALESCE(MAX(pr.score), 0) as highest_score,
    COALESCE(MIN(pr.score), 0) as lowest_score,
    COUNT(DISTINCT pr.user_id) as unique_users_count
FROM practice p
LEFT JOIN practice_record pr ON p.id = pr.practice_id AND pr.status = 'completed'
WHERE p.is_active = 1
GROUP BY p.id, p.title, p.composer, p.difficulty_level, p.genre;

-- 最近活动视图
CREATE OR REPLACE VIEW recent_activities AS
SELECT 
    'practice' as activity_type,
    pr.id as activity_id,
    pr.user_id,
    u.username,
    p.title as activity_title,
    pr.score as activity_score,
    pr.created_at as activity_time
FROM practice_record pr
JOIN user u ON pr.user_id = u.id
JOIN practice p ON pr.practice_id = p.id
WHERE pr.status = 'completed'
UNION ALL
SELECT 
    'contact' as activity_type,
    cm.id as activity_id,
    NULL as user_id,
    cm.name as username,
    cm.subject as activity_title,
    NULL as activity_score,
    cm.created_at as activity_time
FROM contact_message cm
ORDER BY activity_time DESC;

-- 优化完成
SELECT 'Database optimization completed successfully!' as message; 
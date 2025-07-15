# AiMusPal - AI音乐教育平台

🎵 一个基于AI技术的智能音乐教育平台，为学生和教师提供个性化的音乐学习体验。

## 🚀 项目特色

- **AI智能分析**: 使用先进的AI技术分析音乐演奏，提供精准的节拍、音准、节奏评估
- **个性化反馈**: 根据用户水平和学习进度，提供定制化的练习建议
- **角色权限管理**: 支持学生、教师、管理员等不同角色，具有完善的权限控制
- **移动端API**: 提供完整的RESTful API，支持移动应用集成
- **现代化界面**: 响应式设计，支持多设备访问

## 🛠️ 技术栈

### 后端
- **框架**: Flask 2.3.3
- **数据库**: MySQL 8.0
- **缓存**: Redis 7
- **认证**: Flask-Login + JWT
- **数据库ORM**: SQLAlchemy
- **部署**: Docker + Docker Compose

### 前端
- **框架**: Bootstrap 5
- **图标**: Font Awesome 6
- **响应式设计**: 支持移动端和桌面端

## 📋 功能模块

### 用户管理
- 用户注册/登录
- 邮箱验证
- 个人资料管理
- 基于角色的权限控制

### 练习管理
- 练习曲目库
- 音频文件上传
- AI分析和评分
- 练习历史记录

### 管理后台
- 用户管理
- 练习曲目管理
- 数据统计和分析
- 系统配置

### API接口
- 用户认证API
- 练习数据API
- 文件上传API
- 移动端支持

## 🚀 快速开始

### 使用Docker部署（推荐）

1. **克隆项目**
```bash
git clone <repository-url>
cd aimuspal
```

2. **配置环境变量**
```bash
cp .env.example .env
# 编辑 .env 文件，设置数据库密码、JWT密钥等
```

3. **启动服务**
```bash
docker-compose up -d
```

4. **初始化数据库**
```bash
docker-compose exec web flask init-db
docker-compose exec web flask create-sample-data
```

5. **访问应用**
- 网站: http://localhost:5000
- 管理后台: http://localhost:5000/admin
- 数据库管理: http://localhost:8080 (Adminer)

### 本地开发

1. **安装依赖**
```bash
pip install -r requirements.txt
```

2. **配置数据库**
```bash
# 启动MySQL和Redis
# 创建数据库 aimuspal_db
```

3. **设置环境变量**
```bash
export FLASK_APP=app.py
export FLASK_ENV=development
```

4. **初始化数据库**
```bash
flask init-db
flask create-sample-data
```

5. **运行应用**
```bash
flask run
```

## 🔧 配置说明

### 环境变量

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| FLASK_ENV | 运行环境 | development |
| SECRET_KEY | Flask密钥 | - |
| JWT_SECRET_KEY | JWT密钥 | - |
| DATABASE_URL | 数据库连接 | - |
| REDIS_URL | Redis连接 | redis://localhost:6379/0 |
| MAIL_SERVER | 邮件服务器 | smtp.gmail.com |
| MAIL_USERNAME | 邮件用户名 | - |
| MAIL_PASSWORD | 邮件密码 | - |

### 数据库配置

项目使用MySQL作为主数据库，Redis作为缓存数据库。Docker Compose会自动配置这些服务。

## 👥 用户角色

1. **学生 (student)**
   - 浏览练习曲目
   - 上传练习音频
   - 查看AI分析结果
   - 管理个人资料

2. **教师 (teacher)**
   - 学生功能
   - 管理练习曲目
   - 查看学生练习记录
   - 后台数据分析

3. **管理员 (admin)**
   - 所有功能权限
   - 用户管理
   - 系统配置
   - 数据统计

## 📱 API文档

### 认证接口

#### 登录
```http
POST /api/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password"
}
```

#### 注册
```http
POST /api/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "username": "username",
  "password": "password",
  "user_type": "student"
}
```

### 练习接口

#### 获取练习列表
```http
GET /api/practices
Authorization: Bearer <token>
```

#### 上传练习音频
```http
POST /api/practices/{id}/upload
Authorization: Bearer <token>
Content-Type: multipart/form-data

audio: <audio_file>
```

## 🧪 测试

```bash
# 运行测试
python -m pytest

# 运行测试并生成覆盖率报告
python -m pytest --cov=app
```

## 📝 数据库管理

### 数据库迁移
```bash
# 生成迁移文件
flask db migrate -m "描述"

# 应用迁移
flask db upgrade

# 回滚迁移
flask db downgrade
```

### 常用命令
```bash
# 重置数据库
flask reset-db

# 创建示例数据
flask create-sample-data

# 进入Flask Shell
flask shell
```

## 🔒 安全考虑

- 密码使用bcrypt加密存储
- JWT令牌用于API认证
- CSRF保护
- SQL注入防护
- 文件上传安全检查
- 角色权限控制

## 📊 监控和日志

- 应用日志记录
- 错误监控
- 性能监控
- 用户行为分析

## 🤝 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 📞 联系我们

- 项目主页: https://github.com/your-org/aimuspal
- 问题报告: https://github.com/your-org/aimuspal/issues
- 邮箱: contact@aimuspal.com

## 🎯 路线图

- [ ] 增加更多乐器支持
- [ ] 实时音频分析
- [ ] 视频练习支持
- [ ] 社交功能
- [ ] 移动端应用
- [ ] 机器学习模型优化

---

**默认管理员账户**
- 邮箱: admin@aimuspal.com
- 密码: admin123

⚠️ **注意**: 生产环境请立即修改默认密码！
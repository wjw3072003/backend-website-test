# AI MusPal 网站页面分析

## 设计标准模板元素

### 颜色系统
- **主色调**: #ff5d47 (橙红色)
- **辅助色**: #666666 (灰色)
- **背景色**: #ffffff (白色)
- **浅灰背景**: #f5f3ef

### 字体系统
- **主字体**: Inter 字体家族
- **标题**: 粗体，大字号
- **正文**: 常规字重，16px

### 布局系统
- **圆角**: 20px (卡片), 100px (按钮)
- **阴影**: 多层阴影效果
- **间距**: 20px, 30px 统一间距
- **容器**: 最大宽度1200px

## 所有用户可访问的页面

### 1. 公共页面 (无需登录)
- `/` - 首页 (index.html)
- `/aimuspal` - AI MusPal新首页 (aimuspal_homepage_formatted.html)
- `/about` - 关于页面 (about.html)
- `/contact` - 联系页面 (contact.html)
- `/privacy` - 隐私政策 (privacy.html)
- `/terms` - 服务条款 (terms.html)
- `/auth/login` - 登录页面 (auth/login.html)
- `/auth/register` - 注册页面 (auth/register.html)
- `/auth/forgot-password` - 忘记密码 (auth/forgot_password.html)
- `/auth/reset-password/<token>` - 重置密码 (auth/reset_password.html)
- `/auth/verify/<token>` - 邮箱验证 (auth/verify_email.html)

### 2. 学生用户页面 (需要登录)
- `/dashboard` - 用户仪表板 (dashboard.html)
- `/practices` - 练习曲目列表 (practices.html)
- `/practices/<id>` - 练习曲目详情 (practice_detail.html)
- `/practices/<id>/upload` - 练习音频上传 (practice_upload.html)
- `/practice-result/<id>` - 练习结果 (practice_result.html)
- `/practice-records` - 练习记录列表 (practice_records.html)
- `/stats` - 用户统计 (user_stats.html)
- `/auth/profile` - 个人资料 (auth/profile.html)

### 3. 老师用户页面 (需要老师权限)
- `/teacher/dashboard` - 老师仪表板 (teacher/dashboard.html)
- `/teacher/students` - 学生管理 (teacher/students.html)
- `/teacher/classes` - 班级管理 (teacher/classes.html)
- `/teacher/assignments` - 作业管理 (teacher/assignments.html)
- `/teacher/grades` - 成绩管理 (teacher/grades.html)
- `/teacher/reports` - 教学报告 (teacher/reports.html)

### 4. 管理员页面 (需要管理员权限)
- `/admin/dashboard` - 管理仪表板 (admin/dashboard.html)
- `/admin/users` - 用户管理 (admin/users.html)
- `/admin/practices` - 练习管理 (admin/practices.html)
- `/admin/practice_records` - 练习记录管理 (admin/practice_records.html)
- `/cache-stats` - 缓存统计 (cache_stats.html)

### 5. API接口 (需要相应权限)
- `/api/*` - 各种API接口
- `/health` - 健康检查

## 页面改造优先级

### 高优先级 (核心功能页面)
1. 首页 (/) - 已改造
2. 登录页面 (/auth/login) - 已改造
3. 注册页面 (/auth/register) - 已改造
4. 仪表板 (/dashboard) - 已改造
5. 练习曲目列表 (/practices) - 已改造

### 中优先级 (重要功能页面)
6. 练习详情 (/practices/<id>)
7. 练习上传 (/practices/<id>/upload)
8. 练习结果 (/practice-result/<id>)
9. 练习记录 (/practice-records)
10. 用户统计 (/stats)
11. 个人资料 (/auth/profile)

### 低优先级 (辅助页面)
12. 关于页面 (/about)
13. 联系页面 (/contact)
14. 隐私政策 (/privacy)
15. 服务条款 (/terms)
16. 忘记密码 (/auth/forgot-password)
17. 重置密码 (/auth/reset-password)

### 管理页面 (最后改造)
18. 管理员仪表板 (/admin/dashboard)
19. 老师仪表板 (/teacher/dashboard)
20. 其他管理页面

## 改造策略

1. **保持功能完整性**: 所有原有功能必须保留
2. **统一设计风格**: 使用AI MusPal主页的设计元素
3. **渐进式改造**: 按优先级逐步改造
4. **响应式设计**: 确保移动端适配
5. **性能优化**: 保持页面加载速度 
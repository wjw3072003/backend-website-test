from flask import current_app, render_template_string
from flask_mail import Message
from app import mail
import threading

def send_async_email(app, msg):
    """异步发送邮件"""
    with app.app_context():
        try:
            mail.send(msg)
            print(f"邮件发送成功: {msg.subject}")
        except Exception as e:
            print(f"邮件发送失败: {e}")

def send_email(to, subject, template, **kwargs):
    """发送邮件的通用函数"""
    try:
        app = current_app._get_current_object()
        
        msg = Message(
            subject=f"[AiMusPal] {subject}",
            sender=app.config['MAIL_DEFAULT_SENDER'],
            recipients=[to] if isinstance(to, str) else to
        )
        
        msg.html = template
        
        # 异步发送邮件
        thread = threading.Thread(
            target=send_async_email,
            args=(app, msg)
        )
        thread.start()
        
        return True
        
    except Exception as e:
        print(f"邮件准备失败: {e}")
        return False

def send_verification_email(user, token):
    """发送邮箱验证邮件"""
    verification_url = f"{current_app.config['FRONTEND_URL']}/auth/verify/{token}"
    
    template = f"""
    <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #f4f4f4; }}
                .container {{ max-width: 600px; margin: 0 auto; background-color: white; padding: 20px; border-radius: 10px; }}
                .header {{ text-align: center; margin-bottom: 30px; }}
                .button {{ display: inline-block; background-color: #007bff; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; }}
                .footer {{ margin-top: 30px; text-align: center; font-size: 12px; color: #666; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🎵 AiMusPal</h1>
                    <h2>邮箱验证</h2>
                </div>
                
                <p>亲爱的 {user.username}，</p>
                
                <p>感谢您注册AiMusPal AI音乐教育平台！请点击下面的按钮验证您的邮箱地址：</p>
                
                <p style="text-align: center; margin: 30px 0;">
                    <a href="{verification_url}" class="button">验证邮箱</a>
                </p>
                
                <p>如果按钮无法点击，请复制以下链接到浏览器中打开：</p>
                <p style="word-break: break-all; color: #007bff;">{verification_url}</p>
                
                <p>此链接将在24小时后失效。</p>
                
                <div class="footer">
                    <p>如果您没有注册AiMusPal账户，请忽略此邮件。</p>
                    <p>© 2024 AiMusPal. All rights reserved.</p>
                </div>
            </div>
        </body>
    </html>
    """
    
    return send_email(
        to=user.email,
        subject="请验证您的邮箱地址",
        template=template
    )

def send_password_reset_email(user, token):
    """发送密码重置邮件"""
    reset_url = f"{current_app.config['FRONTEND_URL']}/auth/reset-password/{token}"
    
    template = f"""
    <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #f4f4f4; }}
                .container {{ max-width: 600px; margin: 0 auto; background-color: white; padding: 20px; border-radius: 10px; }}
                .header {{ text-align: center; margin-bottom: 30px; }}
                .button {{ display: inline-block; background-color: #dc3545; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; }}
                .footer {{ margin-top: 30px; text-align: center; font-size: 12px; color: #666; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🎵 AiMusPal</h1>
                    <h2>密码重置</h2>
                </div>
                
                <p>亲爱的 {user.username}，</p>
                
                <p>我们收到了您的密码重置请求。请点击下面的按钮重置您的密码：</p>
                
                <p style="text-align: center; margin: 30px 0;">
                    <a href="{reset_url}" class="button">重置密码</a>
                </p>
                
                <p>如果按钮无法点击，请复制以下链接到浏览器中打开：</p>
                <p style="word-break: break-all; color: #dc3545;">{reset_url}</p>
                
                <p>此链接将在1小时后失效。</p>
                
                <p><strong>如果您没有请求重置密码，请忽略此邮件。您的密码不会被更改。</strong></p>
                
                <div class="footer">
                    <p>为了您的账户安全，请不要将此邮件转发给他人。</p>
                    <p>© 2024 AiMusPal. All rights reserved.</p>
                </div>
            </div>
        </body>
    </html>
    """
    
    return send_email(
        to=user.email,
        subject="密码重置请求",
        template=template
    )

def send_welcome_email(user):
    """发送欢迎邮件"""
    template = f"""
    <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #f4f4f4; }}
                .container {{ max-width: 600px; margin: 0 auto; background-color: white; padding: 20px; border-radius: 10px; }}
                .header {{ text-align: center; margin-bottom: 30px; }}
                .feature {{ margin: 20px 0; padding: 15px; background-color: #f8f9fa; border-radius: 5px; }}
                .button {{ display: inline-block; background-color: #28a745; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; }}
                .footer {{ margin-top: 30px; text-align: center; font-size: 12px; color: #666; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🎵 欢迎来到AiMusPal！</h1>
                </div>
                
                <p>亲爱的 {user.username}，</p>
                
                <p>欢迎加入AiMusPal AI音乐教育平台！我们很高兴您选择我们作为您音乐学习的伙伴。</p>
                
                <div class="feature">
                    <h3>🎼 丰富的练习曲目</h3>
                    <p>从初级到高级，涵盖各种音乐风格的练习曲目等待您的探索。</p>
                </div>
                
                <div class="feature">
                    <h3>🤖 AI智能分析</h3>
                    <p>上传您的练习录音，获得专业的AI分析和个性化反馈。</p>
                </div>
                
                <div class="feature">
                    <h3>📊 学习进度追踪</h3>
                    <p>详细的统计数据帮助您了解学习进展，制定更好的练习计划。</p>
                </div>
                
                <p style="text-align: center; margin: 30px 0;">
                    <a href="{current_app.config['FRONTEND_URL']}/dashboard" class="button">开始学习之旅</a>
                </p>
                
                <p>如果您有任何问题或建议，请随时联系我们的客服团队。</p>
                
                <div class="footer">
                    <p>祝您学习愉快！</p>
                    <p>© 2024 AiMusPal. All rights reserved.</p>
                </div>
            </div>
        </body>
    </html>
    """
    
    return send_email(
        to=user.email,
        subject="欢迎来到AiMusPal！",
        template=template
    )

def send_practice_completed_email(user, practice, score):
    """发送练习完成通知邮件"""
    template = f"""
    <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #f4f4f4; }}
                .container {{ max-width: 600px; margin: 0 auto; background-color: white; padding: 20px; border-radius: 10px; }}
                .header {{ text-align: center; margin-bottom: 30px; }}
                .score {{ text-align: center; font-size: 48px; font-weight: bold; color: #28a745; margin: 20px 0; }}
                .button {{ display: inline-block; background-color: #007bff; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; }}
                .footer {{ margin-top: 30px; text-align: center; font-size: 12px; color: #666; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🎵 练习完成！</h1>
                </div>
                
                <p>亲爱的 {user.username}，</p>
                
                <p>恭喜您完成了《{practice.title}》的练习！</p>
                
                <div class="score">{score}分</div>
                
                <p style="text-align: center;">
                    {'🏆 出色的表现！' if score >= 90 else '👍 很好的进步！' if score >= 80 else '💪 继续努力！'}
                </p>
                
                <p style="text-align: center; margin: 30px 0;">
                    <a href="{current_app.config['FRONTEND_URL']}/practices/{practice.id}" class="button">查看详细分析</a>
                </p>
                
                <p>继续保持练习，您的音乐技能会不断提升！</p>
                
                <div class="footer">
                    <p>© 2024 AiMusPal. All rights reserved.</p>
                </div>
            </div>
        </body>
    </html>
    """
    
    return send_email(
        to=user.email,
        subject=f"练习完成 - {practice.title}",
        template=template
    )

def send_contact_notification(contact_message):
    """发送联系表单通知邮件给管理员"""
    admin_email = current_app.config.get('ADMIN_EMAIL', current_app.config['MAIL_DEFAULT_SENDER'])
    
    template = f"""
    <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #f4f4f4; }}
                .container {{ max-width: 600px; margin: 0 auto; background-color: white; padding: 20px; border-radius: 10px; }}
                .header {{ text-align: center; margin-bottom: 30px; }}
                .info {{ background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin: 15px 0; }}
                .message {{ background-color: #fff3cd; padding: 15px; border-radius: 5px; margin: 15px 0; }}
                .footer {{ margin-top: 30px; text-align: center; font-size: 12px; color: #666; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>📧 新的联系表单消息</h1>
                </div>
                
                <div class="info">
                    <p><strong>发送者：</strong> {contact_message.name}</p>
                    <p><strong>邮箱：</strong> {contact_message.email}</p>
                    <p><strong>主题：</strong> {contact_message.subject}</p>
                    <p><strong>时间：</strong> {contact_message.created_at.strftime('%Y-%m-%d %H:%M:%S')}</p>
                </div>
                
                <div class="message">
                    <p><strong>消息内容：</strong></p>
                    <p>{contact_message.message}</p>
                </div>
                
                <p>请及时回复用户的问题。</p>
                
                <div class="footer">
                    <p>© 2024 AiMusPal. All rights reserved.</p>
                </div>
            </div>
        </body>
    </html>
    """
    
    return send_email(
        to=admin_email,
        subject=f"新联系消息 - {contact_message.subject}",
        template=template
    )

def send_monthly_report_email(user, stats):
    """发送月度学习报告邮件"""
    template = f"""
    <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #f4f4f4; }}
                .container {{ max-width: 600px; margin: 0 auto; background-color: white; padding: 20px; border-radius: 10px; }}
                .header {{ text-align: center; margin-bottom: 30px; }}
                .stat {{ display: inline-block; text-align: center; margin: 10px; padding: 15px; background-color: #f8f9fa; border-radius: 5px; width: 120px; }}
                .stat-number {{ font-size: 24px; font-weight: bold; color: #007bff; }}
                .button {{ display: inline-block; background-color: #28a745; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; }}
                .footer {{ margin-top: 30px; text-align: center; font-size: 12px; color: #666; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>📊 您的月度学习报告</h1>
                </div>
                
                <p>亲爱的 {user.username}，</p>
                
                <p>以下是您这个月的学习统计：</p>
                
                <div style="text-align: center; margin: 30px 0;">
                    <div class="stat">
                        <div class="stat-number">{stats.get('monthly_practices', 0)}</div>
                        <div>练习次数</div>
                    </div>
                    <div class="stat">
                        <div class="stat-number">{stats.get('average_score', 0)}</div>
                        <div>平均分数</div>
                    </div>
                    <div class="stat">
                        <div class="stat-number">{stats.get('total_time', 0)}</div>
                        <div>总时长(小时)</div>
                    </div>
                </div>
                
                <p>{'🎉 这个月您的表现很棒！' if stats.get('monthly_practices', 0) >= 10 else '💪 下个月争取更多练习！'}</p>
                
                <p style="text-align: center; margin: 30px 0;">
                    <a href="{current_app.config['FRONTEND_URL']}/dashboard" class="button">查看详细统计</a>
                </p>
                
                <div class="footer">
                    <p>继续保持练习，您会越来越棒！</p>
                    <p>© 2024 AiMusPal. All rights reserved.</p>
                </div>
            </div>
        </body>
    </html>
    """
    
    return send_email(
        to=user.email,
        subject="您的月度学习报告",
        template=template
    )
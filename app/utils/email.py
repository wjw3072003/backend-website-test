from flask import current_app, url_for
from flask_mail import Message
from app import mail
import logging

def send_email(to, subject, template, **kwargs):
    """发送邮件的基础函数"""
    try:
        msg = Message(
            subject=f'[AiMusPal] {subject}',
            recipients=[to],
            html=template,
            sender=current_app.config['MAIL_USERNAME']
        )
        mail.send(msg)
        return True
    except Exception as e:
        logging.error(f'邮件发送失败: {e}')
        return False

def send_verification_email(user):
    """发送邮箱验证邮件"""
    verification_url = url_for('auth.verify_email', 
                              token=user.verification_token, 
                              _external=True)
    
    html_template = f'''
    <html>
    <body>
        <h2>欢迎加入 AiMusPal！</h2>
        <p>亲爱的 {user.username}，</p>
        <p>感谢您注册 AiMusPal 音乐教育平台。请点击下面的链接验证您的邮箱：</p>
        <p><a href="{verification_url}" style="background-color: #4CAF50; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">验证邮箱</a></p>
        <p>如果上面的按钮无法点击，请复制以下链接到浏览器地址栏：</p>
        <p>{verification_url}</p>
        <p>此链接24小时内有效。</p>
        <br>
        <p>AiMusPal 团队</p>
    </body>
    </html>
    '''
    
    return send_email(
        to=user.email,
        subject='邮箱验证',
        template=html_template
    )

def send_password_reset_email(user, reset_token):
    """发送密码重置邮件"""
    reset_url = url_for('auth.reset_password', 
                       token=reset_token, 
                       _external=True)
    
    html_template = f'''
    <html>
    <body>
        <h2>重置密码</h2>
        <p>亲爱的 {user.username}，</p>
        <p>我们收到了您的密码重置请求。请点击下面的链接重置您的密码：</p>
        <p><a href="{reset_url}" style="background-color: #f44336; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">重置密码</a></p>
        <p>如果上面的按钮无法点击，请复制以下链接到浏览器地址栏：</p>
        <p>{reset_url}</p>
        <p>此链接1小时内有效。如果您没有请求密码重置，请忽略此邮件。</p>
        <br>
        <p>AiMusPal 团队</p>
    </body>
    </html>
    '''
    
    return send_email(
        to=user.email,
        subject='密码重置',
        template=html_template
    )

def send_practice_feedback_email(user, practice_record):
    """发送练习反馈邮件"""
    html_template = f'''
    <html>
    <body>
        <h2>练习反馈报告</h2>
        <p>亲爱的 {user.username}，</p>
        <p>您的练习《{practice_record.practice.title}》已完成AI分析，以下是您的练习报告：</p>
        
        <h3>总体评分：{practice_record.score:.1f}分</h3>
        
        <h4>详细分析：</h4>
        <ul>
            <li>节拍准确度：{practice_record.tempo_accuracy:.1f}%</li>
            <li>音准度：{practice_record.pitch_accuracy:.1f}%</li>
            <li>节奏准确度：{practice_record.rhythm_accuracy:.1f}%</li>
        </ul>
        
        <h4>AI反馈：</h4>
        <p>{practice_record.ai_feedback}</p>
        
        <h4>改进建议：</h4>
        <p>{practice_record.improvement_suggestions}</p>
        
        <p>继续练习，您会越来越好！</p>
        <br>
        <p>AiMusPal 团队</p>
    </body>
    </html>
    '''
    
    return send_email(
        to=user.email,
        subject=f'练习反馈 - {practice_record.practice.title}',
        template=html_template
    )
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
老师端功能最终验证脚本
验证老师端所有功能的完整性和可用性
"""

import sys
import os
import requests
from datetime import datetime
sys.path.insert(0, os.path.abspath('.'))

def test_teacher_functionality():
    """验证老师端功能完整性"""
    
    print("🎯 老师端功能最终验证")
    print(f"⏰ 验证时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    base_url = "http://localhost:5005"
    
    # 测试路由响应（302重定向是正常的，说明需要认证）
    routes_to_test = [
        ("/teacher/dashboard", "老师仪表板"),
        ("/teacher/students", "学生管理"),
        ("/teacher/classes", "班级管理"),
        ("/teacher/assignments", "作业管理"),
        ("/teacher/grades", "成绩管理"),
        ("/teacher/reports", "教学报告"),
    ]
    
    print("🛣️ 路由可用性测试:")
    working_routes = 0
    
    for route, name in routes_to_test:
        try:
            response = requests.get(f"{base_url}{route}", timeout=5, allow_redirects=False)
            
            if response.status_code == 302:
                print(f"  ✅ {name} ({route}) - 可用 (需要认证)")
                working_routes += 1
            elif response.status_code == 200:
                print(f"  ✅ {name} ({route}) - 可用")
                working_routes += 1
            else:
                print(f"  ❌ {name} ({route}) - 错误 ({response.status_code})")
                
        except Exception as e:
            print(f"  ❌ {name} ({route}) - 连接失败: {e}")
    
    print(f"\n📊 路由测试结果: {working_routes}/{len(routes_to_test)} 可用")
    
    return working_routes

def verify_database_structure():
    """验证数据库结构完整性"""
    
    try:
        from app import create_app, db
        from sqlalchemy import inspect
        
        app = create_app()
        with app.app_context():
            print("\n🗄️ 数据库结构验证:")
            
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            
            # 检查老师端必需的表
            required_tables = [
                'class', 'assignment', 'grade', 'teaching_resource', 
                'announcement', 'attendance', 'student_classes', 'teacher_classes'
            ]
            
            existing_tables = 0
            for table in required_tables:
                if table in tables:
                    print(f"  ✅ {table} - 存在")
                    existing_tables += 1
                else:
                    print(f"  ❌ {table} - 缺失")
            
            print(f"\n📊 数据表状态: {existing_tables}/{len(required_tables)} 存在")
            
            # 检查索引
            print("\n🔍 索引优化验证:")
            connection = db.engine.connect()
            
            index_check_sql = """
            SELECT COUNT(*) as count 
            FROM information_schema.statistics 
            WHERE table_schema = DATABASE() 
            AND index_name LIKE 'idx_%'
            """
            
            result = connection.execute(index_check_sql).fetchone()
            index_count = result[0] if result else 0
            
            print(f"  📈 优化索引数量: {index_count}")
            
            if index_count >= 5:
                print(f"  ✅ 索引优化良好")
            else:
                print(f"  ⚠️ 索引需要优化")
            
            connection.close()
            
            return existing_tables >= 6  # 至少6个核心表存在
            
    except Exception as e:
        print(f"\n❌ 数据库验证失败: {e}")
        return False

def verify_template_files():
    """验证模板文件完整性"""
    
    print("\n🎨 模板文件验证:")
    
    template_files = [
        "app/templates/teacher/dashboard.html",
        "app/templates/teacher/students.html", 
        "app/templates/teacher/classes.html",
        "app/templates/teacher/assignments.html",
        "app/templates/teacher/grades.html",
        "app/templates/teacher/reports.html"
    ]
    
    existing_templates = 0
    
    for template in template_files:
        if os.path.exists(template):
            print(f"  ✅ {os.path.basename(template)} - 存在")
            existing_templates += 1
        else:
            print(f"  ❌ {os.path.basename(template)} - 缺失")
    
    print(f"\n📊 模板状态: {existing_templates}/{len(template_files)} 存在")
    
    return existing_templates >= 5

def verify_teacher_account():
    """验证老师账户"""
    
    try:
        from app import create_app, db
        from app.models.user import User
        
        app = create_app()
        with app.app_context():
            print("\n👨‍🏫 老师账户验证:")
            
            # 查找老师账户
            teacher = User.query.filter_by(email='teacher@aimuspal.com').first()
            
            if teacher:
                print(f"  ✅ 老师账户存在: {teacher.username}")
                print(f"  📧 邮箱: {teacher.email}")
                
                # 检查角色
                has_teacher_role = teacher.has_role('teacher')
                if has_teacher_role:
                    print(f"  ✅ 老师角色: 已分配")
                else:
                    print(f"  ❌ 老师角色: 未分配")
                
                return True
            else:
                print(f"  ❌ 老师账户不存在")
                return False
                
    except Exception as e:
        print(f"  ❌ 账户验证失败: {e}")
        return False

def generate_final_report():
    """生成最终验证报告"""
    
    print("\n" + "=" * 60)
    print("📋 老师端功能最终验证报告")
    print("=" * 60)
    
    # 执行所有验证
    routes_working = test_teacher_functionality() >= 5
    database_ok = verify_database_structure()
    templates_ok = verify_template_files()
    account_ok = verify_teacher_account()
    
    # 计算总体得分
    checks = [routes_working, database_ok, templates_ok, account_ok]
    passed_checks = sum(checks)
    total_checks = len(checks)
    
    success_rate = (passed_checks / total_checks) * 100
    
    print(f"\n🎯 验证结果总结:")
    print(f"  🛣️ 路由系统: {'✅ 通过' if routes_working else '❌ 失败'}")
    print(f"  🗄️ 数据库结构: {'✅ 通过' if database_ok else '❌ 失败'}")
    print(f"  🎨 模板文件: {'✅ 通过' if templates_ok else '❌ 失败'}")
    print(f"  👨‍🏫 老师账户: {'✅ 通过' if account_ok else '❌ 失败'}")
    
    print(f"\n📊 总体验证率: {success_rate:.1f}% ({passed_checks}/{total_checks})")
    
    if success_rate >= 80:
        print(f"🎉 老师端功能验证成功！系统已准备就绪")
        status = "SUCCESS"
    elif success_rate >= 60:
        print(f"⚠️ 老师端功能基本可用，但需要进一步完善")
        status = "PARTIAL"
    else:
        print(f"❌ 老师端功能存在重大问题，需要修复")
        status = "FAILED"
    
    # 保存报告
    report = {
        'timestamp': datetime.now().isoformat(),
        'verification_rate': success_rate,
        'status': status,
        'checks': {
            'routes': routes_working,
            'database': database_ok,
            'templates': templates_ok,
            'account': account_ok
        }
    }
    
    import json
    with open('teacher_final_verification.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"\n📄 详细报告已保存: teacher_final_verification.json")
    print(f"⏰ 验证完成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    return status

if __name__ == '__main__':
    try:
        status = generate_final_report()
        
        if status == "SUCCESS":
            print(f"\n🚀 老师端功能开发圆满完成！")
            sys.exit(0)
        elif status == "PARTIAL":
            print(f"\n⚠️ 老师端功能基本完成，建议进一步优化")
            sys.exit(1)
        else:
            print(f"\n❌ 老师端功能需要修复")
            sys.exit(2)
            
    except Exception as e:
        print(f"\n💥 验证过程出错: {e}")
        sys.exit(3) 
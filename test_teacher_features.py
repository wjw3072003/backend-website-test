#!/usr/bin/env python3
"""
老师端功能综合测试脚本
审查和测试所有老师端功能
"""

import requests
import sys
import os
from datetime import datetime
import json
from bs4 import BeautifulSoup

class TeacherFeatureTester:
    def __init__(self, base_url="http://localhost:5005"):
        self.base_url = base_url
        self.session = requests.Session()
        self.test_results = []
        self.missing_features = []
        
    def log_test(self, test_name, success, message=""):
        """记录测试结果"""
        status = "✅ PASS" if success else "❌ FAIL"
        result = {
            'test': test_name,
            'success': success,
            'message': message,
            'timestamp': datetime.now().isoformat()
        }
        self.test_results.append(result)
        print(f"{status}: {test_name} {message}")
        
    def log_missing_feature(self, feature_name, description, priority="high"):
        """记录缺失功能"""
        missing = {
            'feature': feature_name,
            'description': description,
            'priority': priority,
            'timestamp': datetime.now().isoformat()
        }
        self.missing_features.append(missing)
        print(f"🔍 缺失功能: {feature_name} - {description}")
    
    def test_teacher_login(self):
        """测试老师登录功能"""
        try:
            # 先获取登录页面
            login_page = self.session.get(f"{self.base_url}/auth/login")
            
            # 尝试老师登录
            login_data = {
                'email': 'teacher@aimuspal.com',
                'password': 'teacher123',
                'remember_me': False
            }
            
            response = self.session.post(f"{self.base_url}/auth/login", data=login_data)
            
            # 检查是否登录成功 (重定向到仪表板)
            success = response.status_code in [200, 302]
            if success:
                # 检查是否能访问仪表板
                dashboard_response = self.session.get(f"{self.base_url}/dashboard")
                success = dashboard_response.status_code == 200
                message = "老师登录成功，能访问仪表板"
                
                # 检查页面是否显示老师相关内容
                if "老师" in dashboard_response.text or "教师" in dashboard_response.text:
                    message += "，显示老师界面"
                else:
                    message += "，但可能没有老师专用界面"
            else:
                message = f"老师登录失败，状态码: {response.status_code}"
            
            self.log_test("老师登录", success, message)
            return success
        except Exception as e:
            self.log_test("老师登录", False, str(e))
            return False
    
    def analyze_dashboard(self):
        """分析老师仪表板功能"""
        try:
            response = self.session.get(f"{self.base_url}/dashboard")
            if response.status_code != 200:
                self.log_test("仪表板访问", False, f"状态码: {response.status_code}")
                return False
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 检查导航菜单
            nav_links = soup.find_all('a', class_=['nav-link', 'btn'])
            menu_items = [link.get_text().strip() for link in nav_links if link.get_text().strip()]
            
            print("\n📋 发现的导航菜单项:")
            for item in menu_items:
                print(f"  - {item}")
            
            # 检查老师专用功能
            teacher_features = [
                ('学生管理', ['学生', '学员', 'student']),
                ('班级管理', ['班级', '课程', 'class', 'course']), 
                ('作业管理', ['作业', '任务', 'assignment', 'homework']),
                ('成绩管理', ['成绩', '评分', 'grade', 'score']),
                ('进度跟踪', ['进度', '统计', 'progress', 'analytics']),
                ('教学资源', ['资源', '教材', 'resource', 'material'])
            ]
            
            content_text = response.text.lower()
            found_features = []
            missing_features = []
            
            for feature_name, keywords in teacher_features:
                found = any(keyword.lower() in content_text for keyword in keywords)
                if found:
                    found_features.append(feature_name)
                else:
                    missing_features.append(feature_name)
                    self.log_missing_feature(feature_name, f"仪表板缺少{feature_name}相关功能")
            
            print(f"\n✅ 发现的老师功能: {found_features}")
            print(f"❌ 缺失的老师功能: {missing_features}")
            
            self.log_test("仪表板分析", True, f"发现 {len(found_features)} 个功能，缺失 {len(missing_features)} 个功能")
            return True
            
        except Exception as e:
            self.log_test("仪表板分析", False, str(e))
            return False
    
    def test_teacher_routes(self):
        """测试老师专用路由"""
        teacher_routes = [
            ('/admin/users', '用户管理'),
            ('/admin/practices', '练习管理'),
            ('/admin/practice-records', '练习记录管理'),
            ('/teacher/students', '学生管理'),
            ('/teacher/classes', '班级管理'),
            ('/teacher/assignments', '作业管理'),
            ('/teacher/grades', '成绩管理'),
            ('/teacher/reports', '教学报告')
        ]
        
        print("\n🔍 测试老师专用路由:")
        available_routes = []
        missing_routes = []
        
        for route, description in teacher_routes:
            try:
                response = self.session.get(f"{self.base_url}{route}")
                if response.status_code == 200:
                    available_routes.append((route, description))
                    print(f"  ✅ {route} - {description}")
                elif response.status_code == 404:
                    missing_routes.append((route, description))
                    print(f"  ❌ {route} - {description} (404)")
                    self.log_missing_feature(description, f"路由 {route} 不存在")
                else:
                    print(f"  ⚠️ {route} - {description} (状态码: {response.status_code})")
            except Exception as e:
                missing_routes.append((route, description))
                print(f"  ❌ {route} - {description} (错误: {e})")
        
        self.log_test("老师路由测试", True, f"可用: {len(available_routes)}, 缺失: {len(missing_routes)}")
        return len(available_routes) > 0
    
    def analyze_admin_interface(self):
        """分析管理员界面（老师可能有部分权限）"""
        try:
            response = self.session.get(f"{self.base_url}/admin/")
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # 检查管理功能
                admin_features = soup.find_all(['h1', 'h2', 'h3', 'h4', 'a'])
                features = [elem.get_text().strip() for elem in admin_features if elem.get_text().strip()]
                
                print(f"\n📊 管理界面功能 (共 {len(features)} 项):")
                for i, feature in enumerate(features[:20]):  # 只显示前20项
                    print(f"  {i+1}. {feature}")
                
                # 检查是否有老师专用的管理功能
                teacher_admin_features = [
                    '学生管理', '班级管理', '成绩管理', '作业管理', 
                    '教学资源', '课程管理', '进度跟踪'
                ]
                
                content_lower = response.text.lower()
                missing_admin_features = []
                
                for feature in teacher_admin_features:
                    if feature.lower() not in content_lower:
                        missing_admin_features.append(feature)
                        self.log_missing_feature(f"管理界面-{feature}", f"管理界面缺少{feature}功能")
                
                self.log_test("管理界面分析", True, f"界面可访问，缺失 {len(missing_admin_features)} 个老师功能")
                return True
            else:
                self.log_test("管理界面访问", False, f"状态码: {response.status_code}")
                self.log_missing_feature("管理界面权限", "老师无法访问管理界面")
                return False
                
        except Exception as e:
            self.log_test("管理界面分析", False, str(e))
            return False
    
    def check_teacher_data_needs(self):
        """检查老师端需要的数据表和功能"""
        print("\n🗄️ 分析老师端数据需求:")
        
        # 老师端可能需要的数据表
        needed_tables = [
            ('classes', '班级表', '管理班级信息'),
            ('assignments', '作业表', '布置和管理作业'),
            ('student_classes', '学生班级关联表', '管理学生班级关系'),
            ('teacher_classes', '老师班级关联表', '管理老师班级关系'),
            ('grades', '成绩表', '记录学生成绩'),
            ('teaching_resources', '教学资源表', '管理教学资料'),
            ('announcements', '公告表', '发布班级公告'),
            ('attendance', '考勤表', '记录学生出勤')
        ]
        
        for table_name, description, purpose in needed_tables:
            self.log_missing_feature(f"数据表-{table_name}", f"{description}: {purpose}")
        
        print(f"  📝 建议新增 {len(needed_tables)} 个数据表")
    
    def run_teacher_audit(self):
        """运行老师端功能审查"""
        print("🚀 开始老师端功能审查")
        print(f"⏰ 审查时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        
        # 1. 老师登录测试
        print("\n🔐 老师认证测试:")
        login_success = self.test_teacher_login()
        
        if login_success:
            # 2. 仪表板功能分析
            print("\n📊 仪表板功能分析:")
            self.analyze_dashboard()
            
            # 3. 路由功能测试
            print("\n🛣️ 路由功能测试:")
            self.test_teacher_routes()
            
            # 4. 管理界面分析
            print("\n⚙️ 管理界面分析:")
            self.analyze_admin_interface()
            
            # 5. 数据需求分析
            self.check_teacher_data_needs()
        else:
            print("\n⚠️ 老师登录失败，跳过后续审查")
        
        # 生成审查报告
        self.generate_audit_report()
    
    def generate_audit_report(self):
        """生成审查报告"""
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result['success'])
        failed_tests = total_tests - passed_tests
        total_missing = len(self.missing_features)
        
        print("\n" + "=" * 60)
        print("📋 老师端功能审查报告:")
        print(f"  测试项目: {total_tests}")
        print(f"  通过测试: {passed_tests} ✅")
        print(f"  失败测试: {failed_tests} ❌")
        print(f"  缺失功能: {total_missing} 🔍")
        
        if self.missing_features:
            print(f"\n🚨 需要实现的功能 ({total_missing} 项):")
            
            # 按优先级分组
            high_priority = [f for f in self.missing_features if f.get('priority') == 'high']
            medium_priority = [f for f in self.missing_features if f.get('priority') == 'medium']
            low_priority = [f for f in self.missing_features if f.get('priority') == 'low']
            other_priority = [f for f in self.missing_features if f.get('priority') not in ['high', 'medium', 'low']]
            
            for priority, features in [('高优先级', high_priority + other_priority), 
                                     ('中优先级', medium_priority), 
                                     ('低优先级', low_priority)]:
                if features:
                    print(f"\n  📌 {priority}:")
                    for i, feature in enumerate(features, 1):
                        print(f"    {i}. {feature['feature']}: {feature['description']}")
        
        print(f"\n⏰ 审查完成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # 保存报告
        self.save_audit_report()
    
    def save_audit_report(self, filename="teacher_audit_report.json"):
        """保存审查报告"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'summary': {
                'total_tests': len(self.test_results),
                'passed_tests': sum(1 for r in self.test_results if r['success']),
                'failed_tests': sum(1 for r in self.test_results if not r['success']),
                'total_missing_features': len(self.missing_features)
            },
            'test_results': self.test_results,
            'missing_features': self.missing_features
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"📄 审查报告已保存: {filename}")

def main():
    """主函数"""
    tester = TeacherFeatureTester()
    
    try:
        tester.run_teacher_audit()
        
        # 根据缺失功能数量设置退出码
        missing_count = len(tester.missing_features)
        return 1 if missing_count > 0 else 0
        
    except KeyboardInterrupt:
        print("\n\n⚠️ 审查被用户中断")
        return 1
    except Exception as e:
        print(f"\n❌ 审查过程出错: {e}")
        return 1

if __name__ == "__main__":
    exit(main()) 
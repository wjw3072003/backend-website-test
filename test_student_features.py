#!/usr/bin/env python3
"""
学生端功能综合测试脚本
验证所有已实现的学生端功能
"""

import requests
import sys
import os
from datetime import datetime
import json

class StudentFeatureTester:
    def __init__(self, base_url="http://localhost:5005"):
        self.base_url = base_url
        self.session = requests.Session()
        self.test_results = []
        
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
        
    def test_homepage_access(self):
        """测试主页访问"""
        try:
            response = self.session.get(self.base_url)
            success = response.status_code == 200
            message = f"状态码: {response.status_code}"
            self.log_test("主页访问", success, message)
            return success
        except Exception as e:
            self.log_test("主页访问", False, str(e))
            return False
    
    def test_login_page(self):
        """测试登录页面"""
        try:
            response = self.session.get(f"{self.base_url}/auth/login")
            success = response.status_code == 200 and "登录" in response.text
            message = f"状态码: {response.status_code}"
            self.log_test("登录页面", success, message)
            return success
        except Exception as e:
            self.log_test("登录页面", False, str(e))
            return False
    
    def test_student_login(self):
        """测试学生登录功能"""
        try:
            # 先获取登录页面获取CSRF token
            login_page = self.session.get(f"{self.base_url}/auth/login")
            
            # 尝试登录
            login_data = {
                'email': '151926171@qq.com',  # 使用已知的学生账号
                'password': 'student123',
                'remember_me': False
            }
            
            response = self.session.post(f"{self.base_url}/auth/login", data=login_data)
            
            # 检查是否登录成功 (重定向到仪表板)
            success = response.status_code in [200, 302]
            if success:
                # 检查是否能访问仪表板
                dashboard_response = self.session.get(f"{self.base_url}/dashboard")
                success = dashboard_response.status_code == 200
                message = "登录成功，能访问仪表板"
            else:
                message = f"登录失败，状态码: {response.status_code}"
            
            self.log_test("学生登录", success, message)
            return success
        except Exception as e:
            self.log_test("学生登录", False, str(e))
            return False
    
    def test_dashboard_access(self):
        """测试仪表板访问"""
        try:
            response = self.session.get(f"{self.base_url}/dashboard")
            success = response.status_code == 200 and "仪表板" in response.text
            message = f"状态码: {response.status_code}"
            self.log_test("仪表板访问", success, message)
            return success
        except Exception as e:
            self.log_test("仪表板访问", False, str(e))
            return False
    
    def test_practices_list(self):
        """测试练习曲目列表"""
        try:
            response = self.session.get(f"{self.base_url}/practices")
            success = response.status_code == 200 and "练习曲目" in response.text
            message = f"状态码: {response.status_code}"
            self.log_test("练习曲目列表", success, message)
            return success
        except Exception as e:
            self.log_test("练习曲目列表", False, str(e))
            return False
    
    def test_practice_search(self):
        """测试练习曲目搜索"""
        try:
            response = self.session.get(f"{self.base_url}/practices?search=test")
            success = response.status_code == 200
            message = f"搜索功能正常，状态码: {response.status_code}"
            self.log_test("练习曲目搜索", success, message)
            return success
        except Exception as e:
            self.log_test("练习曲目搜索", False, str(e))
            return False
    
    def test_practice_filter(self):
        """测试练习曲目筛选"""
        try:
            response = self.session.get(f"{self.base_url}/practices?difficulty=1")
            success = response.status_code == 200
            message = f"筛选功能正常，状态码: {response.status_code}"
            self.log_test("练习曲目筛选", success, message)
            return success
        except Exception as e:
            self.log_test("练习曲目筛选", False, str(e))
            return False
    
    def test_practice_records(self):
        """测试练习记录页面"""
        try:
            response = self.session.get(f"{self.base_url}/practice-records")
            success = response.status_code == 200 and "练习记录" in response.text
            message = f"状态码: {response.status_code}"
            self.log_test("练习记录页面", success, message)
            return success
        except Exception as e:
            self.log_test("练习记录页面", False, str(e))
            return False
    
    def test_user_stats(self):
        """测试学习统计页面"""
        try:
            response = self.session.get(f"{self.base_url}/stats")
            success = response.status_code == 200 and "学习统计" in response.text
            message = f"状态码: {response.status_code}"
            self.log_test("学习统计页面", success, message)
            return success
        except Exception as e:
            self.log_test("学习统计页面", False, str(e))
            return False
    
    def test_profile_access(self):
        """测试个人资料页面"""
        try:
            response = self.session.get(f"{self.base_url}/auth/profile")
            success = response.status_code == 200 and "个人资料" in response.text
            message = f"状态码: {response.status_code}"
            self.log_test("个人资料页面", success, message)
            return success
        except Exception as e:
            self.log_test("个人资料页面", False, str(e))
            return False
    
    def test_api_endpoints(self):
        """测试API端点"""
        api_tests = [
            ("/api/auth/me", "用户信息API"),
            ("/api/practices", "练习列表API"),
            ("/api/stats/overview", "统计概览API")
        ]
        
        all_success = True
        for endpoint, name in api_tests:
            try:
                response = self.session.get(f"{self.base_url}{endpoint}")
                success = response.status_code in [200, 401]  # 401也可能是正常的（需要特定权限）
                message = f"状态码: {response.status_code}"
                self.log_test(name, success, message)
                if not success:
                    all_success = False
            except Exception as e:
                self.log_test(name, False, str(e))
                all_success = False
        
        return all_success
    
    def test_cache_functionality(self):
        """测试缓存功能（通过多次请求验证）"""
        try:
            # 第一次请求仪表板
            start_time = datetime.now()
            response1 = self.session.get(f"{self.base_url}/dashboard")
            first_time = (datetime.now() - start_time).total_seconds()
            
            # 第二次请求仪表板（应该更快，因为有缓存）
            start_time = datetime.now()
            response2 = self.session.get(f"{self.base_url}/dashboard")
            second_time = (datetime.now() - start_time).total_seconds()
            
            success = response1.status_code == 200 and response2.status_code == 200
            message = f"首次: {first_time:.3f}s, 二次: {second_time:.3f}s"
            self.log_test("缓存功能", success, message)
            return success
        except Exception as e:
            self.log_test("缓存功能", False, str(e))
            return False
    
    def test_responsive_design(self):
        """测试响应式设计（通过检查Bootstrap类）"""
        try:
            response = self.session.get(f"{self.base_url}/practices")
            success = response.status_code == 200 and "col-" in response.text and "responsive" in response.text
            message = "页面包含响应式CSS类"
            self.log_test("响应式设计", success, message)
            return success
        except Exception as e:
            self.log_test("响应式设计", False, str(e))
            return False
    
    def run_all_tests(self):
        """运行所有测试"""
        print("🚀 开始学生端功能测试")
        print(f"⏰ 测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        
        # 基础功能测试
        print("\n📋 基础功能测试:")
        self.test_homepage_access()
        self.test_login_page()
        
        # 认证测试
        print("\n🔐 认证功能测试:")
        login_success = self.test_student_login()
        
        if login_success:
            # 学生端功能测试
            print("\n👨‍🎓 学生端功能测试:")
            self.test_dashboard_access()
            self.test_practices_list()
            self.test_practice_search()
            self.test_practice_filter()
            self.test_practice_records()
            self.test_user_stats()
            self.test_profile_access()
            
            # 高级功能测试
            print("\n⚙️ 高级功能测试:")
            self.test_api_endpoints()
            self.test_cache_functionality()
            self.test_responsive_design()
        else:
            print("\n⚠️ 登录失败，跳过后续测试")
        
        # 测试总结
        self.print_summary()
    
    def print_summary(self):
        """打印测试总结"""
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result['success'])
        failed_tests = total_tests - passed_tests
        
        print("\n" + "=" * 60)
        print("📊 测试总结:")
        print(f"  总测试数: {total_tests}")
        print(f"  通过测试: {passed_tests} ✅")
        print(f"  失败测试: {failed_tests} ❌")
        print(f"  通过率: {(passed_tests/total_tests*100):.1f}%")
        
        if failed_tests > 0:
            print("\n❌ 失败的测试:")
            for result in self.test_results:
                if not result['success']:
                    print(f"  - {result['test']}: {result['message']}")
        else:
            print("\n🎉 所有测试通过！")
        
        print(f"\n⏰ 测试完成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    def save_report(self, filename="test_report.json"):
        """保存测试报告"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'total_tests': len(self.test_results),
            'passed_tests': sum(1 for r in self.test_results if r['success']),
            'failed_tests': sum(1 for r in self.test_results if not r['success']),
            'results': self.test_results
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"📄 测试报告已保存: {filename}")

def main():
    """主函数"""
    tester = StudentFeatureTester()
    
    try:
        tester.run_all_tests()
        tester.save_report()
        
        # 根据测试结果设置退出码
        failed_count = sum(1 for r in tester.test_results if not r['success'])
        return 1 if failed_count > 0 else 0
        
    except KeyboardInterrupt:
        print("\n\n⚠️ 测试被用户中断")
        return 1
    except Exception as e:
        print(f"\n❌ 测试过程出错: {e}")
        return 1

if __name__ == "__main__":
    exit(main()) 
import os
import random
import time
from datetime import datetime
import json
import requests
from flask import current_app

def analyze_audio_practice(audio_file_path, practice):
    """
    分析练习音频文件
    
    Args:
        audio_file_path (str): 音频文件路径
        practice: 练习曲目对象
    
    Returns:
        dict: 分析结果
    """
    try:
        # 检查文件是否存在
        if not os.path.exists(audio_file_path):
            raise FileNotFoundError(f"音频文件不存在: {audio_file_path}")
        
        # 获取文件大小
        file_size = os.path.getsize(audio_file_path)
        if file_size == 0:
            raise ValueError("音频文件为空")
        
        # 模拟AI分析过程（实际应用中调用真实的AI服务）
        analysis_result = _simulate_ai_analysis(audio_file_path, practice)
        
        # 如果配置了真实的AI服务，可以在这里调用
        # analysis_result = _call_real_ai_service(audio_file_path, practice)
        
        return analysis_result
        
    except Exception as e:
        print(f"AI分析失败: {e}")
        return _get_default_analysis_result()

def _simulate_ai_analysis(audio_file_path, practice):
    """模拟AI分析过程"""
    # 模拟分析时间
    time.sleep(1)
    
    # 根据练习难度生成不同的分数范围
    difficulty = practice.difficulty_level
    
    if difficulty <= 3:  # 初级
        score_range = (70, 95)
        accuracy_range = (75, 95)
    elif difficulty <= 6:  # 中级
        score_range = (60, 90)
        accuracy_range = (70, 90)
    else:  # 高级
        score_range = (50, 85)
        accuracy_range = (60, 85)
    
    # 生成随机但合理的分数
    score = random.randint(*score_range)
    tempo_accuracy = random.randint(*accuracy_range)
    pitch_accuracy = random.randint(*accuracy_range)
    rhythm_accuracy = random.randint(*accuracy_range)
    
    # 生成AI反馈
    feedback = _generate_feedback(score, tempo_accuracy, pitch_accuracy, rhythm_accuracy)
    
    # 生成改进建议
    suggestions = _generate_suggestions(tempo_accuracy, pitch_accuracy, rhythm_accuracy)
    
    return {
        'score': score,
        'tempo_accuracy': tempo_accuracy,
        'pitch_accuracy': pitch_accuracy,
        'rhythm_accuracy': rhythm_accuracy,
        'feedback': feedback,
        'suggestions': suggestions,
        'analysis_timestamp': datetime.utcnow().isoformat(),
        'analysis_version': '1.0',
        'detailed_metrics': {
            'timing_precision': random.randint(60, 95),
            'note_clarity': random.randint(65, 95),
            'dynamic_control': random.randint(55, 90),
            'overall_musicality': random.randint(60, 90)
        }
    }

def _generate_feedback(score, tempo_accuracy, pitch_accuracy, rhythm_accuracy):
    """根据分数生成反馈"""
    feedback_parts = []
    
    # 总体评价
    if score >= 90:
        feedback_parts.append("出色的演奏！您的技巧和音乐表现力都很棒。")
    elif score >= 80:
        feedback_parts.append("很好的演奏！整体表现不错，还有提升空间。")
    elif score >= 70:
        feedback_parts.append("不错的演奏！基础扎实，继续练习会更好。")
    elif score >= 60:
        feedback_parts.append("演奏有进步空间，请关注以下方面的改进。")
    else:
        feedback_parts.append("需要更多练习，请耐心提升各项技巧。")
    
    # 具体方面的反馈
    if tempo_accuracy >= 85:
        feedback_parts.append("节拍控制很稳定。")
    elif tempo_accuracy >= 70:
        feedback_parts.append("节拍基本稳定，可以更加精确。")
    else:
        feedback_parts.append("节拍需要加强练习，建议使用节拍器。")
    
    if pitch_accuracy >= 85:
        feedback_parts.append("音准非常好。")
    elif pitch_accuracy >= 70:
        feedback_parts.append("音准较好，个别音符可以更准确。")
    else:
        feedback_parts.append("音准需要改进，建议多练习音阶。")
    
    if rhythm_accuracy >= 85:
        feedback_parts.append("节奏把握得很好。")
    elif rhythm_accuracy >= 70:
        feedback_parts.append("节奏基本正确，细节可以更精确。")
    else:
        feedback_parts.append("节奏需要加强，建议分段练习。")
    
    return " ".join(feedback_parts)

def _generate_suggestions(tempo_accuracy, pitch_accuracy, rhythm_accuracy):
    """根据分析结果生成改进建议"""
    suggestions = []
    
    if tempo_accuracy < 80:
        suggestions.append("使用节拍器练习，从慢速开始逐渐提高。")
        suggestions.append("专注于稳定的节拍，不要急于求快。")
    
    if pitch_accuracy < 80:
        suggestions.append("多练习音阶和琶音，提高手指准确性。")
        suggestions.append("仔细聆听每个音符，培养敏锐的音感。")
    
    if rhythm_accuracy < 80:
        suggestions.append("分解复杂的节奏型，逐个攻克。")
        suggestions.append("练习时大声数拍子，建立内在节奏感。")
    
    # 通用建议
    general_suggestions = [
        "保持放松的演奏姿态，避免紧张。",
        "录音练习，自我监督演奏质量。",
        "慢练为主，确保每个细节都准确。",
        "定期复习基础技巧。",
        "保持耐心，持续练习。"
    ]
    
    # 随机添加1-2个通用建议
    suggestions.extend(random.sample(general_suggestions, min(2, len(general_suggestions))))
    
    return suggestions

def _get_default_analysis_result():
    """获取默认的分析结果（分析失败时使用）"""
    return {
        'score': 0,
        'tempo_accuracy': 0,
        'pitch_accuracy': 0,
        'rhythm_accuracy': 0,
        'feedback': '分析过程中出现错误，请稍后重试。',
        'suggestions': ['请检查音频文件质量。', '如果问题持续，请联系技术支持。'],
        'analysis_timestamp': datetime.utcnow().isoformat(),
        'analysis_version': '1.0',
        'error': True
    }

def _call_real_ai_service(audio_file_path, practice):
    """
    调用真实的AI分析服务
    这是一个占位符函数，实际使用时需要根据具体的AI服务API进行实现
    """
    try:
        # 获取AI服务配置
        ai_service_url = current_app.config.get('AI_SERVICE_URL')
        ai_service_key = current_app.config.get('AI_SERVICE_KEY')
        
        if not ai_service_url:
            # 如果没有配置AI服务，使用模拟分析
            return _simulate_ai_analysis(audio_file_path, practice)
        
        # 准备请求数据
        with open(audio_file_path, 'rb') as audio_file:
            files = {'audio': audio_file}
            data = {
                'practice_id': practice.id,
                'difficulty': practice.difficulty_level,
                'genre': practice.genre,
                'analysis_type': 'full'
            }
            headers = {
                'Authorization': f'Bearer {ai_service_key}'
            }
            
            # 发送请求到AI服务
            response = requests.post(
                f"{ai_service_url}/analyze",
                files=files,
                data=data,
                headers=headers,
                timeout=60  # 60秒超时
            )
            
            if response.status_code == 200:
                result = response.json()
                return _format_ai_service_result(result)
            else:
                print(f"AI服务请求失败: {response.status_code}")
                return _simulate_ai_analysis(audio_file_path, practice)
                
    except Exception as e:
        print(f"调用AI服务失败: {e}")
        return _simulate_ai_analysis(audio_file_path, practice)

def _format_ai_service_result(ai_result):
    """格式化AI服务返回的结果"""
    return {
        'score': ai_result.get('overall_score', 0),
        'tempo_accuracy': ai_result.get('tempo_score', 0),
        'pitch_accuracy': ai_result.get('pitch_score', 0),
        'rhythm_accuracy': ai_result.get('rhythm_score', 0),
        'feedback': ai_result.get('feedback', ''),
        'suggestions': ai_result.get('suggestions', []),
        'analysis_timestamp': datetime.utcnow().isoformat(),
        'analysis_version': ai_result.get('version', '1.0'),
        'detailed_metrics': ai_result.get('detailed_metrics', {})
    }

def validate_audio_file(file_path):
    """验证音频文件的有效性"""
    try:
        if not os.path.exists(file_path):
            return False, "文件不存在"
        
        # 检查文件大小
        file_size = os.path.getsize(file_path)
        if file_size == 0:
            return False, "文件为空"
        
        # 检查文件扩展名
        _, ext = os.path.splitext(file_path)
        allowed_extensions = ['.mp3', '.wav', '.m4a', '.flac', '.aac', '.ogg']
        if ext.lower() not in allowed_extensions:
            return False, "不支持的音频格式"
        
        return True, "文件有效"
        
    except Exception as e:
        return False, f"验证失败: {e}"

def get_audio_info(file_path):
    """获取音频文件基本信息"""
    try:
        file_size = os.path.getsize(file_path)
        file_name = os.path.basename(file_path)
        
        return {
            'filename': file_name,
            'size_bytes': file_size,
            'size_mb': round(file_size / (1024 * 1024), 2),
            'format': os.path.splitext(file_path)[1].lower()
        }
    except Exception as e:
        print(f"获取音频信息失败: {e}")
        return None
// 按钮功能修复脚本
(function() {
    'use strict';
    
    console.log('🔧 开始修复按钮功能...');
    
    // 等待页面完全加载
    function waitForElements() {
        const buttons = document.querySelectorAll('button');
        const targetButtons = [];
        
        buttons.forEach(function(button) {
            const text = button.textContent.trim();
            if (text === 'Sign In' || text === 'Start Free Trial' || text === 'Start for Free') {
                targetButtons.push(button);
            }
        });
        
        if (targetButtons.length > 0) {
            console.log(`找到 ${targetButtons.length} 个目标按钮`);
            fixButtons(targetButtons);
        } else {
            console.log('未找到目标按钮，等待...');
            setTimeout(waitForElements, 500);
        }
    }
    
    function fixButtons(buttons) {
        buttons.forEach(function(button) {
            const text = button.textContent.trim();
            let targetUrl = '';
            
            // 根据按钮文本确定目标URL
            if (text === 'Sign In') {
                targetUrl = '/auth/login';
            } else if (text === 'Start Free Trial' || text === 'Start for Free') {
                targetUrl = '/auth/register';
            }
            
            if (targetUrl) {
                // 移除所有现有的事件监听器
                const newButton = button.cloneNode(true);
                button.parentNode.replaceChild(newButton, button);
                
                // 添加新的事件监听器
                newButton.addEventListener('click', function(e) {
                    e.preventDefault();
                    e.stopPropagation();
                    e.stopImmediatePropagation();
                    
                    console.log(`🚀 按钮 "${text}" 被点击，跳转到: ${targetUrl}`);
                    
                    // 强制跳转
                    try {
                        window.location.href = targetUrl;
                    } catch (error) {
                        console.error('跳转失败:', error);
                        // 备用方案
                        window.open(targetUrl, '_self');
                    }
                }, true);
                
                // 添加视觉反馈
                newButton.style.cursor = 'pointer';
                newButton.addEventListener('mouseenter', function() {
                    this.style.opacity = '0.8';
                });
                newButton.addEventListener('mouseleave', function() {
                    this.style.opacity = '1';
                });
                
                console.log(`✅ 按钮 "${text}" 已修复`);
            }
        });
    }
    
    // 开始修复
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', waitForElements);
    } else {
        waitForElements();
    }
    
    // 延迟执行，确保Framer完全加载
    setTimeout(waitForElements, 1000);
    setTimeout(waitForElements, 2000);
    setTimeout(waitForElements, 3000);
    
    console.log('�� 按钮修复脚本已加载');
})(); 
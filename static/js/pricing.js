// 定价数据 - 完全按照参考网站 https://streamlined-founders-083360.framer.app/
const pricingData = {
    free: {
        title: "Free Membership",
        price: "HK$0",
        period: "",
        subtitle: "Limited usage",
        buttonText: "Start for Free",
        buttonClass: "btn-outline",
        features: [
            "Each account can scan sheet music 1 time (IP tracking)",
            "Each account can use AI reports 3 times (IP tracking)"
        ]
    },
    gold: {
        title: "Gold Membership", 
        originalPrice: "HK$461",
        price: "HK$323",
        period: "p/month",
        subtitle: "Only HK$3,880/year",
        buttonText: "Start Free Trial",
        buttonClass: "btn-primary",
        features: [
            "Free refund within 7 days",
            "50 sheet music scans per month", 
            "50 AI report usages per month"
        ]
    },
    platinum: {
        title: "Platinum Membership",
        originalPrice: "HK$550", 
        price: "HK$385",
        period: "p/month",
        subtitle: "Only HK$27/hour.",
        buttonText: "Start Free Trial",
        buttonClass: "btn-primary",
        features: [
            "Free refund within 7 days",
            "Unlimited usage of AI reports",
            "Unlimited usage of sheet music scans"
        ]
    }
};

// 动态生成定价卡片HTML
function generatePricingCard(planKey, planData) {
    const hasOriginalPrice = planData.originalPrice;
    
    return `
        <div class="framer-pricing-card" data-plan="${planKey}">
            <div class="framer-card-background">
                <div class="framer-card-content">
                    <div class="framer-card-header">
                        <p class="framer-plan-title">${planData.title}</p>
                        <div class="framer-price-section">
                            ${hasOriginalPrice ? `
                                <div class="framer-original-price">
                                    <span class="framer-strikethrough">${planData.originalPrice}</span>
                                </div>
                            ` : ''}
                            <div class="framer-current-price">
                                <span class="framer-price-amount">${planData.price}</span>
                            </div>
                            ${planData.period ? `<p class="framer-price-period">${planData.period}</p>` : ''}
                            ${planData.subtitle ? `<p class="framer-price-subtitle">${planData.subtitle}</p>` : ''}
                        </div>
                    </div>
                    
                    <button class="framer-pricing-button ${planData.buttonClass}" data-plan="${planKey}">
                        <div class="framer-button-text">
                            <p>${planData.buttonText}</p>
                        </div>
                    </button>
                    
                    <div class="framer-features-list">
                        ${planData.features.map(feature => `
                            <div class="framer-feature-row">
                                <div class="framer-check-icon">
                                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                                        <path d="M 12 2.25 C 6.615 2.25 2.25 6.615 2.25 12 C 2.25 17.385 6.615 21.75 12 21.75 C 17.385 21.75 21.75 17.385 21.75 12 C 21.74 6.62 17.38 2.26 12 2.25 Z M 16.641 10.294 L 11.147 15.544 C 11.005 15.677 10.817 15.751 10.622 15.75 C 10.429 15.753 10.244 15.679 10.106 15.544 L 7.359 12.919 C 7.152 12.738 7.06 12.458 7.121 12.189 C 7.181 11.92 7.384 11.706 7.649 11.632 C 7.914 11.557 8.199 11.634 8.391 11.831 L 10.622 13.959 L 15.609 9.206 C 15.912 8.942 16.37 8.964 16.647 9.255 C 16.923 9.547 16.921 10.005 16.641 10.294 Z" fill="rgb(64, 219, 113)"></path>
                                    </svg>
                                </div>
                                <div class="framer-feature-text">
                                    <p>${feature}</p>
                                </div>
                            </div>
                        `).join('')}
                    </div>
                </div>
            </div>
        </div>
    `;
}

// 初始化定价部分
function initializePricing() {
    // 尝试多种方式查找定价容器
    let pricingContainer = document.querySelector('.framer-pricing-container');
    if (!pricingContainer) {
        pricingContainer = document.querySelector('.framer-fp79f5');
    }
    if (!pricingContainer) {
        pricingContainer = document.querySelector('[data-framer-name="Container"]');
    }
    
    if (!pricingContainer) {
        console.error('Pricing container not found with any selector');
        return;
    }
    
    console.log('Found pricing container:', pricingContainer);
    
    // 清空容器并添加自定义类
    pricingContainer.innerHTML = '';
    pricingContainer.className = 'framer-fp79f5 framer-pricing-container';
    pricingContainer.style.opacity = '1';
    pricingContainer.style.transform = 'none';
    
    // 生成所有定价卡片
    const cardsHTML = Object.entries(pricingData)
        .map(([key, data]) => generatePricingCard(key, data))
        .join('');
    
    pricingContainer.innerHTML = cardsHTML;
    
    // 添加按钮事件监听器
    addButtonEventListeners();
}

// 添加按钮点击事件
function addButtonEventListeners() {
    const buttons = document.querySelectorAll('.framer-pricing-button');
    buttons.forEach(button => {
        button.addEventListener('click', function() {
            const plan = this.getAttribute('data-plan');
            handlePricingButtonClick(plan);
        });
    });
}

// 处理定价按钮点击
function handlePricingButtonClick(plan) {
    console.log(`Selected plan: ${plan}`);
    
    // 这里可以添加具体的处理逻辑，比如跳转到注册页面或显示模态框
    switch(plan) {
        case 'free':
            // 处理免费计划注册
            window.location.href = '/register?plan=free';
            break;
        case 'gold':
        case 'platinum':
            // 处理付费计划试用
            window.location.href = `/register?plan=${plan}`;
            break;
        default:
            console.error('Unknown plan:', plan);
    }
}

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', function() {
    initializePricing();
});

// 如果页面已经加载完成，立即初始化
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializePricing);
} else {
    initializePricing();
} 
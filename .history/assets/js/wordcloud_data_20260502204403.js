// Auto-generated Word Cloud Data from Publications
// Run generate_wordcloud.py to update this file
var wordCloud = null;
var lastWindowWidth = 0;

function initWordCloud() {
    const container = document.getElementById("word-cloud");
    if (!container) return;

    lastWindowWidth = container.parentElement.offsetWidth;
    
    function resizeContainer() {
        const width = container.parentElement.offsetWidth;
        if (Math.abs(lastWindowWidth - width) < 50) return;
        lastWindowWidth = width;
        container.style.height = (width * 0.75) + 'px';

        // 动态计算 minFontSize: width / 1000, 限制在 1 到 10 之间
        let calculatedSize = lastWindowWidth / 1000;
        const dynamicMinFontSize = Math.max(1, Math.min(10, calculatedSize));

        // 合并基础配置和动态计算的 minFontSize
        const currentConfig = Object.assign({}, getBaseConfig(), {
            minFontSize: dynamicMinFontSize
        });

        if (wordCloud) {
            container.innerHTML = '';
            wordCloud = new B2wordcloud(container, currentConfig);
        }
    }

    resizeContainer();

    let resizeTimer = null;
    window.addEventListener('resize', function() {
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(function() {
            resizeContainer();
        }, 200);
    });

    
    wordCloud = new B2wordcloud(container, wordCloudConfig);
}

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initWordCloud);
} else {
    initWordCloud();
}

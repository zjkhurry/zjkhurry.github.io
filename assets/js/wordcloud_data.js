// Auto-generated Word Cloud Data from Publications
// Run generate_wordcloud.py to update this file
var wordCloud = null;

// 动态调整词云尺寸
function initWordCloud() {
    const container = document.getElementById("word-cloud");
    if (!container) return;

    // 设置容器高度为宽度的 50% (2:1 宽高比)
    function resizeContainer() {
        const width = container.parentElement.offsetWidth;
        container.style.height = (width * 0.5) + 'px';
        container.style.minHeight = '300px';
    }

    // 初始化时设置尺寸
    resizeContainer();

    // 窗口大小改变时调整
    let resizeTimer = null;
    window.addEventListener('resize', function() {
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(function() {
            resizeContainer();
            // 重新初始化词云
            if (wordCloud) {
                // 清空容器
                container.innerHTML = '';
                // 重新创建词云
                wordCloud = new B2wordcloud(container, wordCloudConfig);
            }
        }, 200); // 防抖，避免频繁重绘
    });

    // 定义词云配置
    var wordCloudConfig = {
        list: [
            {word_list_str}
        ],
        weightFactor: 10,
        effect: 'linerMap',
        tooltip: {
            show: true,
            formatter: function(item) {
                return '<div>' + item[0] + '</div>'
            }
        },
        color: [
            '#00BFFF',
            '#1E90FF',
            ['#87CEFA', '#1E90FF'],  // 天蓝渐变
        ],
        autoFontSize: true,
        cursorWhenHover: 'pointer',
    };

    // 初始化词云
    wordCloud = new B2wordcloud(container, wordCloudConfig);
}

// 页面加载完成后初始化
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initWordCloud);
} else {
    initWordCloud();
}

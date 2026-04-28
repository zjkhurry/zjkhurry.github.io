// Auto-generated Word Cloud Data from Publications
// Run generate_wordcloud.py to update this file
var wordCloud = null;
var lastWindowWidth = null;

// 动态调整词云尺寸
function initWordCloud() {
    const container = document.getElementById("word-cloud");
    if (!container) return;

    // 设置容器高度为宽度的 50% (2:1 宽高比)
    function resizeContainer() {
        const width = container.parentElement.offsetWidth;
        container.style.height = (width * 0.5) + 'px';
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
    var wordCloudConfig = {
        list: [
            ['Wearable Electronics', 100],
            ['Sensors', 84],
            ['Flexibility', 80],
            ['Health Monitoring', 52],
            ['Energy Harvesting', 52],
            ['Skin-Interface', 28],
            ['Nanotechnology', 28],
            ['Haptic Interfaces', 24],
            ['Haptic Feedback', 24],
            ['Machine Learning', 20],
            ['Flexible Electronics', 20],
            ['Thermal Regulation', 16],
            ['Cell Biology', 16],
            ['Bioelectronics', 12],
            ['Soft Robotics', 12],
            ['Neuromorphic', 10],
            ['Microfluidics', 10],
            ['AR/VR', 10],
            ['Biomedical Engineering', 10]
        ],
        weightFactor: 10,
        effect: 'linerMap',
        tooltip: {
            show: false,
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
        cursorWhenHover: 'pointer'
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

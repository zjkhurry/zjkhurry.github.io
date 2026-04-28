// Auto-generated Word Cloud Data from Publications
// Run generate_wordcloud.py to update this file
var wordCloud = null;
var lastContainerWidth = 0; // 记录上次容器的宽度

// 动态调整词云尺寸
function initWordCloud() {
    const container = document.getElementById("word-cloud");
    if (!container) return;

    // 设置容器高度为宽度的 50% (2:1 宽高比)
    function resizeContainer() {
        const width = container.parentElement.offsetWidth;
        
        // 如果宽度没有显著变化，跳过重绘以优化移动端体验
        // 移动端地址栏伸缩通常只改变高度，不改变宽度
        if (Math.abs(width - lastContainerWidth) < 5) {
            return; 
        }
        
        lastContainerWidth = width;
        container.style.height = (width * 0.5) + 'px';

        // 重新初始化词云
        if (wordCloud) {
            // 清空容器
            container.innerHTML = '';
        }
        // 创建新实例
        wordCloud = new B2wordcloud(container, wordCloudConfig);
    }

    // 初始化时设置尺寸并创建词云
    resizeContainer();

    // 窗口大小改变时调整
    let resizeTimer = null;
    window.addEventListener('resize', function() {
        clearTimeout(resizeTimer);
        // 增加防抖时间，移动端滚动时频繁触发，适当延长
        resizeTimer = setTimeout(function() {
            resizeContainer();
        }, 300); 
    });

    // 定义词云配置
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
            show: true,
            formatter: function(item) {
                return '<div>' + item[0] + '</div>';
            }
        },
        color: [
            '#00BFFF',
            '#1E90FF',
            ['#87CEFA', '#1E90FF'],  // 天蓝渐变
            '#1E90FF',
            ['#87CEFA', '#1E90FF'],  // 天蓝渐变
        ],
        autoFontSize: true,
        cursorWhenHover: 'pointer',
    };

    // 初始化词云
    wordCloud = new B2wordcloud(container, wordCloudConfig);
}

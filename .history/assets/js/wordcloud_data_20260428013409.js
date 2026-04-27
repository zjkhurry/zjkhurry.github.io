// Auto-generated Word Cloud Data from Publications
// Run generate_wordcloud.py to update this file
var wordCloud = new B2wordcloud(document.getElementById("word-cloud"), {
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
})

wordCloud.dispatchAction({
    type: 'highlight',
    dataIndex: 0,
    keepAlive: false
})

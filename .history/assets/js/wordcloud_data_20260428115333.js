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
        container.style.height = (width * 0.5) + 'px';

        if (wordCloud) {
            container.innerHTML = '';
            wordCloud = new B2wordcloud(container, wordCloudConfig);
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

    var wordCloudConfig = {
        list: [
            ['loop sensing', 100],
        ['virtual reality', 100],
        ['skin electronics', 100],
        ['tactile sensing', 100],
        ['energy harvesting', 100],
        ['activated batteries', 100],
        ['human machine interfaces', 100],
        ['skin electronic tattoo', 50],
        ['stimulation system', 50],
        ['flexible electronic integration', 50],
        ['structured bioelectronic patch', 50],
        ['precise intracellular delivery', 50],
        ['neuromorphic robotic electronic skin', 50],
        ['injury perception', 50],
        ['active pain', 50],
        ['resistant wearable bioelectronics', 50],
        ['hyperuricemia using interference', 50],
        ['risk management', 50],
        ['prolonged monitoring', 50],
        ['therapeutic electronic wound bandage', 50],
        ['interfaced three', 50],
        ['dimensional closed', 50],
        ['performance metal oxide electronics', 50],
        ['room temperature', 50],
        ['plasmonic printing', 50],
        ['internal organs', 50],
        ['smart thermal regulation', 50],
        ['healthcare monitoring', 50],
        ['time sweat monitoring', 50],
        ['adhesive multimodal sensor', 50],
        ['inspired electronic skin', 50],
        ['dimensional tracking', 50],
        ['contact three', 50],
        ['active non', 50],
        ['wireless transient pacemaker', 50],
        ['functional adhesive hydrogel', 50],
        ['adhesive metal detector array', 50],
        ['wearable bio', 50],
        ['spinal implants', 50],
        ['adhering robotic interface', 50],
        ['chronic electrostimulation', 50],
        ['interactive displays', 50],
        ['integrated pulse sensing system', 50],
        ['reliable pulse monitoring', 50],
        ['cardiac function assessment', 50],
        ['deep learning', 50],
        ['assisted skin', 50],
        ['dimensional integrated electronic skins', 50],
        ['body conformable electronics', 50],
        ['thermoregulation enabled', 50]
        ],
        weightFactor: 5,
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
            ['#87CEFA', '#1E90FF'],
        ],
        autoFontSize: true,
        cursorWhenHover: 'pointer'
    };

    wordCloud = new B2wordcloud(container, wordCloudConfig);
}

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initWordCloud);
} else {
    initWordCloud();
}

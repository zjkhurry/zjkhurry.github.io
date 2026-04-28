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
            ['Wearable Electronics', 25],
        ['Sensors', 21],
        ['Flexibility', 20],
        ['Wireless & Battery-free', 17],
        ['Health Monitoring', 13],
        ['Haptic Interfaces', 10],
        ['Skin-Interface', 7],
        ['Sweat Analysis', 7],
        ['Machine Learning', 5],
        ['Energy Harvesting', 5],
        ['Thermal Regulation', 4],
        ['Implantable & Bioresorbable', 4],
        ['Bioelectronics', 3],
        ['Soft Robotics', 3],
        ['battery free', 3],
        ['Neuromorphic', 2],
        ['Wound Care', 2],
        ['Microfluidics', 2],
        ['Cardiovascular Health', 2],
        ['AR/VR', 2],
        ['virtual reality', 2],
        ['skin electronics', 2],
        ['tactile sensing', 2],
        ['energy harvesting', 2],
        ['human machine interfaces', 2],
        ['skin electronic tattoo', 1],
        ['flexible electronic integration', 1],
        ['kirigami structured bioelectronic patch', 1],
        ['precise intracellular delivery', 1],
        ['organ conformal', 1],
        ['neuromorphic robotic electronic skin', 1],
        ['injury perception', 1],
        ['active pain', 1],
        ['risk management', 1],
        ['prolonged monitoring', 1],
        ['therapeutic electronic wound bandage', 1],
        ['room temperature', 1],
        ['plasmonic printing', 1],
        ['internal organs', 1],
        ['smart thermal regulation', 1],
        ['healthcare monitoring', 1],
        ['skin adhesive multimodal sensor', 1],
        ['real time sweat monitoring', 1],
        ['sweat powered', 1],
        ['long term', 1],
        ['mormyroidea inspired electronic skin', 1],
        ['multi functional adhesive hydrogel', 1],
        ['wireless transient pacemaker', 1],
        ['bio interface', 1],
        ['spinal implants', 1],
        ['tissue adhering robotic interface', 1],
        ['non invasive', 1],
        ['chronic electrostimulation', 1],
        ['user interactive displays', 1],
        ['reliable pulse monitoring', 1],
        ['cardiac function assessment', 1],
        ['body conformable electronics', 1],
        ['thermoregulation enabled', 1],
        ['three dimensional liquid diode', 1],
        ['integrated permeable electronics', 1]
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
            ['#87CEFA', '#1E90FF'],
        ],
        autoFontSize: true,
        mask: 'image'
        cursorWhenHover: 'pointer'
    };

    wordCloud = new B2wordcloud(container, wordCloudConfig);
}

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initWordCloud);
} else {
    initWordCloud();
}

#!/usr/bin/env python3
"""
Generate word cloud data from publications.md using Hybrid Approach.
1. Manual High-Level Categories (for stability and broad topics).
2. Automatic Keyword Extraction (for specific trends and new terms).
Usage: python3 generate_wordcloud.py
"""

import re
import nltk
from collections import Counter
from rake_nltk import Rake

# --- 1. 配置手动定义的大类 (保留你之前的核心分类) ---
MANUAL_CATEGORIES = {
    "Wearable Electronics": [
        r"wearable",
        r"skin-interface",
        r" electronic",
        r"skin.*electronic",
        r" electronic tattoo",
    ],
    "Bioelectronics": [
        r"bioelectronic",
        r"bioelectronics",
        r"bio-electronic",
    ],
    "Sensors": [
        r"sens",
        r"monitor",
        r"measurement",
    ],
    "Health Monitoring": [
        r"health",
        r"monitoring",
        r"patient",
        r"diagnosis",
    ],
    "Skin-Interface": [
        r"skin.*interface",
        r"skin-adhesive",
        r"skin-conformal",
    ],
    "Neuromorphic": [
        r"neuromorphic",
        r"neural",
    ],
    "Flexibility": [
        r"flexible",
        r"stretchable",
        r"soft",
    ],
    "Energy Harvesting": [
        r"energy harvest",
        r"power generation",
        r"nanogenerator",
        r"triboelectric",
    ],
    "Microfluidics": [
        r"microfluidic",
        r"fluid",
    ],
    "Thermal Regulation": [
        r"thermal",
        r"cooling",
        r"heating",
    ],
    "Haptic Interfaces": [
        r"haptic",
        r"tactile",
        r"feedback",
    ],
    "Soft Robotics": [
        r"soft.*robotic",
        r"robotic",
    ],
    "Machine Learning": [
        r"machine.*learn",
        r"deep.*learn",
        r"ai",
        r"artificial.*intelligence",
    ],
    "Wireless & Battery-free": [
        r"wireless",
        r"battery-free",
        r"self-powered",
    ],
    "Sweat Analysis": [
        r"sweat",
    ],
    "Implantable & Bioresorbable": [
        r"implantable",
        r"bioresorbable",
        r"transient",
    ],
    "Cardiovascular Health": [
        r"cardiac",
        r"heart",
        r"pulse",
        r"ECG",
    ],
    "Wound Care": [
        r"wound",
        r"healing",
    ],
    "AR/VR": [
        r"ar.*vr",
        r"virtual.*reality",
        r"augmented.*reality",
    ],
}

# --- 2. NLTK 设置 ---
def ensure_nltk_data():
    resources = ['punkt', 'punkt_tab', 'stopwords']
    for resource in resources:
        try:
            if 'punkt' in resource:
                nltk.data.find(f'tokenizers/{resource}')
            else:
                nltk.data.find(f'corpora/{resource}')
        except LookupError:
            nltk.download(resource)

ensure_nltk_data()

PUBLICATIONS_FILE = "_pages/publications.md"
OUTPUT_FILE = "assets/js/wordcloud_data.js"

# 初始化 RAKE 提取器
# min_length=2, max_length=4 (增加长度以捕获更长的短语如 "closed-loop sensing system")
rake_extractor = Rake(min_length=2, max_length=4)

def extract_manual_keywords(title):
    """根据手动定义的正则提取大类关键词"""
    matched_categories = []
    title_lower = title.lower()
    for category, patterns in MANUAL_CATEGORIES.items():
        for pattern in patterns:
            if re.search(pattern, title_lower):
                matched_categories.append(category)
                break # 每个大类只计一次
    return matched_categories

def extract_auto_keywords(title):
    """
    优化自动提取：
    1. 预处理标题，保护连字符词汇（如 closed-loop -> closed loop）
    2. 使用 RAKE 提取
    3. 过滤噪声
    """
    # 预处理：将连字符替换为空格，以便 RAKE 能识别 "closed" 和 "loop" 为独立词但相邻
    # 同时保留标点分隔，RAKE 依赖标点分割句子
    processed_title = title.replace('-', ' ').replace('/', ' ')
    
    rake_extractor.extract_keywords_from_text(processed_title)
    phrases = rake_extractor.get_ranked_phrases()
    
    valid_phrases = []
    for phrase in phrases:
        phrase_clean = phrase.strip()
        # 过滤条件：
        # 1. 长度 > 3
        # 2. 包含字母
        # 3. 不以停用词开头或结尾 (RAKE 通常处理了，但额外保险)
        # 4. 排除纯数字或无意义短词
        if len(phrase_clean) > 3 and re.search(r'[a-zA-Z]', phrase_clean):
            # 可选：排除一些常见的无意义开头，如 "A study of", "Research on"
            if not re.match(r'^(study|research|review|paper|method|approach)\s', phrase_clean.lower()):
                valid_phrases.append(phrase_clean)
                
    return valid_phrases

def extract_hybrid_keywords():
    """
    混合提取：
    - 手动大类：每篇论文命中即+1
    - 自动短语：每篇论文提取出的有效短语+1
    """
    try:
        with open(PUBLICATIONS_FILE, "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: {PUBLICATIONS_FILE} not found")
        return Counter()

    papers = re.split(r"\n\s*&nbsp;\n", content)
    
    manual_counts = Counter()
    auto_counts = Counter()

    for paper in papers:
        # 提取标题
        title_match = re.search(r"\(\d{2}/\d{4}\)\.\s*(.+?)\.\s*\*\*\*", paper)
        if not title_match:
            continue
            
        title = title_match.group(1)
        
        # 1. 提取手动大类
        manual_cats = extract_manual_keywords(title)
        manual_counts.update(manual_cats)
        
        # 2. 提取自动短语
        auto_phrases = extract_auto_keywords(title)
        auto_counts.update(auto_phrases)

    # 合并计数
    # 注意：如果自动提取的短语和手动大类名字完全一样，它们会合并计数，这是期望的行为
    final_counts = manual_counts + auto_counts
    
    return final_counts


def generate_wordcloud_data():
    """Generate word cloud data file."""
    print("Extracting hybrid keywords (Manual + Auto)...")
    keyword_counts = extract_hybrid_keywords()

    if not keyword_counts:
        print("No keywords found in publications")
        return

    # 获取前 60 个最高频的词/短语
    sorted_keywords = sorted(keyword_counts.items(), key=lambda x: x[1], reverse=True)
    
    word_data = []
    for keyword, count in sorted_keywords[:100]: 
        freq = count
        word_data.append([keyword, freq])

    js_content = generate_js_file(word_data)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(js_content)

    print(f"Generated {OUTPUT_FILE} with {len(word_data)} keywords:")
    for item in word_data:
        print(f"  {item[0]}: {item[1]}")

def generate_js_file(word_data):
    """Generate JavaScript file content with B2wordcloud format."""
    safe_word_list = []
    for item in word_data:
        # 转义单引号，防止 JS 语法错误
        clean_key = item[0].replace("'", "\\'")
        safe_word_list.append(f"['{clean_key}', {item[1]}]")
        
    word_list_str = ",\n        ".join(safe_word_list)

    js_content = f"""// Auto-generated Word Cloud Data from Publications
// Run generate_wordcloud.py to update this file
var wordCloud = null;
var lastWindowWidth = 0;

function initWordCloud() {{
    const container = document.getElementById("word-cloud");
    if (!container) return;
    
    function wordCloudConfig {{
        return{{
            list: [
                {word_list_str}
            ],
            effect: 'linerMap',
            tooltip: {{
                show: true,
                formatter: function(item) {{
                    return '<div>' + item[0] + '</div>'
                }}
            }},
            color: [
                '#00BFFF',
                '#1E90FF',
                ['#87CEFA', '#1E90FF'],
            ],
            autoFontSize: true,
            maskImage: 'images/mask.png',
            cursorWhenHover: 'pointer'
        }};
    }}

    function resizeContainer() {{
        const width = container.parentElement.offsetWidth;
        if (Math.abs(lastWindowWidth - width) < 50) return;
        lastWindowWidth = width;
        container.style.height = (width * 0.75) + 'px';

        // 动态计算 minFontSize: width / 1000, 限制在 1 到 10 之间
        let calculatedSize = Math.round(lastWindowWidth / 100);
        const dynamicMinFontSize = Math.max(1, Math.min(10, calculatedSize));

        // 合并基础配置和动态计算的 minFontSize
        const currentConfig = Object.assign({}, wordCloudConfig(), {
            minFontSize: dynamicMinFontSize
        });

        if (wordCloud) {{
            container.innerHTML = '';
            wordCloud = new B2wordcloud(container, wordCloudConfig);
        }}
    }}

    resizeContainer();

    let resizeTimer = null;
    window.addEventListener('resize', function() {{
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(function() {{
            resizeContainer();
        }}, 200);
    }});

    

    wordCloud = new B2wordcloud(container, wordCloudConfig);
}}

if (document.readyState === 'loading') {{
    document.addEventListener('DOMContentLoaded', initWordCloud);
}} else {{
    initWordCloud();
}}
"""
    return js_content

if __name__ == "__main__":
    generate_wordcloud_data()
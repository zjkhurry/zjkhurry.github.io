#!/usr/bin/env python3
"""
Generate word cloud data from publications.md using Automatic Keyword Extraction.
No manual category definition required.
Usage: python3 generate_wordcloud.py
"""

import re
import nltk
from collections import Counter
from rake_nltk import Rake

# 确保 NLTK 数据已下载 (首次运行需要)
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('punkt')
    nltk.download('stopwords')

PUBLICATIONS_FILE = "_pages/publications.md"
OUTPUT_FILE = "assets/js/wordcloud_data.js"

# 初始化 RAKE 提取器
# min_length=2: 忽略单个单词（如 "the", "a"），只提取短语
# max_length=4: 最多提取4个单词组成的短语
rake_extractor = Rake(min_length=2, max_length=4)

def extract_auto_keywords():
    """
    自动从所有论文标题中提取高频短语。
    """
    try:
        with open(PUBLICATIONS_FILE, "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: {PUBLICATIONS_FILE} not found")
        return []

    papers = re.split(r"\n\s*&nbsp;\n", content)
    all_phrases = []

    for paper in papers:
        # 提取标题: (MM/YYYY). Title. ***
        title_match = re.search(r"\(\d{2}/\d{4}\)\.\s*(.+?)\.\s*\*\*\*", paper)

        if title_match:
            title = title_match.group(1)
            
            # 使用 RAKE 提取当前标题的关键短语
            rake_extractor.extract_keywords_from_text(title)
            phrases = rake_extractor.get_ranked_phrases()
            
            # 过滤掉太短或无意义的短语
            for phrase in phrases:
                phrase_clean = phrase.strip()
                # 只保留长度大于3且包含字母的短语
                if len(phrase_clean) > 3 and re.search(r'[a-zA-Z]', phrase_clean):
                    all_phrases.append(phrase_clean)

    # 统计所有短语的出现频率
    keyword_counts = Counter(all_phrases)
    return keyword_counts

def generate_frequency(count, max_count):
    """Generate frequency value (0-100)."""
    if max_count <= 0:
        return 10
    return max(10, int((count / max_count) * 100))

def generate_wordcloud_data():
    """Generate word cloud data file."""
    print("Automatically extracting keywords from titles...")
    keyword_counts = extract_auto_keywords()

    if not keyword_counts:
        print("No keywords found in publications")
        return

    max_count = max(keyword_counts.values()) if keyword_counts else 1

    # 获取前 50 个最高频的短语
    sorted_keywords = sorted(keyword_counts.items(), key=lambda x: x[1], reverse=True)
    
    word_data = []
    for keyword, count in sorted_keywords[:50]: 
        freq = generate_frequency(count, max_count)
        word_data.append([keyword, freq])

    js_content = generate_js_file(word_data)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(js_content)

    print(f"Generated {OUTPUT_FILE} with {len(word_data)} automatic keywords:")
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

    lastWindowWidth = container.parentElement.offsetWidth;
    
    function resizeContainer() {{
        const width = container.parentElement.offsetWidth;
        if (Math.abs(lastWindowWidth - width) < 50) return;
        lastWindowWidth = width;
        container.style.height = (width * 0.5) + 'px';

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

    var wordCloudConfig = {{
        list: [
            {word_list_str}
        ],
        weightFactor: 10,
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
        cursorWhenHover: 'pointer'
    }};

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
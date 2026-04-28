#!/usr/bin/env python3
"""
Generate word cloud data from publications.md using NLP keyword extraction.
Usage: python3 generate_wordcloud.py
"""

import re
import os
from collections import Counter

# 尝试导入 NLP 库，如果未安装则提示
try:
    from rake_nltk import Rake
    import nltk
except ImportError:
    raise ImportError("Please install required packages: pip install rake-nltk nltk")

PUBLICATIONS_FILE = "_pages/publications.md"
OUTPUT_FILE = "assets/js/wordcloud_data.js"

# 配置 Rake 参数
# min_length: 最小短语长度
# max_length: 最大短语长度
# ranking_metric: 排序算法
rake_nltk_var = Rake(min_length=2, max_length=4, ranking_metric=rake_nltk_var.Metric.DEGREE_TO_FREQUENCY_RATIO)

def download_nltk_data():
    """确保 NLTK 数据已下载"""
    try:
        nltk.data.find('tokenizers/punkt')
        nltk.data.find('corpora/stopwords')
    except LookupError:
        nltk.download('punkt')
        nltk.download('stopwords')

def extract_keywords_from_publications_auto():
    """
    使用 RAKE 算法自动从出版物标题中提取关键词。
    """
    download_nltk_data()
    
    try:
        with open(PUBLICATIONS_FILE, "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: {PUBLICATIONS_FILE} not found")
        return []

    # 分割论文条目
    papers = re.split(r"\n\s*&nbsp;\n", content)
    all_extracted_keywords = []

    for paper in papers:
        # 提取标题: (MM/YYYY). Title. ***
        title_match = re.search(r"\(\d{2}/\d{4}\)\.\s*(.+?)\.\s*\*\*\*", paper)

        if title_match:
            title = title_match.group(1)
            
            # 使用 RAKE 提取关键词
            # Rake 需要纯文本，去除特殊符号可能有助于提高准确性，但保留连字符对技术术语很重要
            rake_nltk_var.extract_keywords_from_text(title)
            keywords = rake_nltk_var.get_ranked_phrases()
            
            # 过滤掉太短或包含太多停用词的短语，并转换为标题格式
            valid_keywords = []
            for kw in keywords:
                # 简单清洗：去除首尾空白，忽略纯数字或单个字母
                kw_clean = kw.strip()
                if len(kw_clean) > 2 and not kw_clean.isdigit():
                    valid_keywords.append(kw_clean)
            
            all_extracted_keywords.extend(valid_keywords)

    # 统计频率
    keyword_counts = Counter(all_extracted_keywords)
    return keyword_counts


def generate_frequency(count, max_count):
    """Generate frequency value (0-100)."""
    if max_count <= 0:
        return 10
    return max(10, int((count / max_count) * 100))


def generate_wordcloud_data():
    """Generate word cloud data file."""
    print("Extracting keywords using NLP (RAKE)...")
    keyword_counts = extract_keywords_from_publications_auto()

    if not keyword_counts:
        print("No keywords found in publications")
        return

    max_count = max(keyword_counts.values()) if keyword_counts else 1

    # 获取前 80 个高频关键词 (增加数量以丰富词云)
    sorted_keywords = sorted(keyword_counts.items(), key=lambda x: x[1], reverse=True)
    
    word_data = []
    for keyword, count in sorted_keywords[:80]: 
        freq = generate_frequency(count, max_count)
        word_data.append([keyword, freq])

    js_content = generate_js_file(word_data)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(js_content)

    print(f"Generated {OUTPUT_FILE} with {len(word_data)} keywords:")
    for item in word_data:
        print(f"  {item[0]}: {item[1]}")


def generate_js_file(word_data):
    """Generate JavaScript file content with B2wordcloud format."""
    # Format word data as B2wordcloud list format
    # 注意：如果关键词中包含单引号，需要转义，防止 JS 语法错误
    safe_word_list = []
    for item in word_data:
        # 转义单引号
        clean_key = item[0].replace("'", "\\'")
        safe_word_list.append(f"['{clean_key}', {item[1]}]")
        
    word_list_str = ",\n        ".join(safe_word_list)

    # 注意：JS 代码中的所有花括号 { } 都必须转义为 {{ }}
    js_content = f"""// Auto-generated Word Cloud Data from Publications
// Run generate_wordcloud.py to update this file
var wordCloud = null;
var lastWindowWidth = 0;

// 动态调整词云尺寸
function initWordCloud() {{
    const container = document.getElementById("word-cloud");
    if (!container) return;

    lastWindowWidth = container.parentElement.offsetWidth;
    // 设置容器高度为宽度的 50% (2:1 宽高比)
    function resizeContainer() {{
        const width = container.parentElement.offsetWidth;
        if (Math.abs(lastWindowWidth - width) < 50) return; // 如果宽度变化不大，避免频繁调整
        lastWindowWidth = width;
        container.style.height = (width * 0.5) + 'px';

        // 重新初始化词云
        if (wordCloud) {{
            // 清空容器
            container.innerHTML = '';
            // 重新创建词云
            wordCloud = new B2wordcloud(container, wordCloudConfig);
        }}
    }}

    // 初始化时设置尺寸
    resizeContainer();

    // 窗口大小改变时调整
    let resizeTimer = null;
    window.addEventListener('resize', function() {{
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(function() {{
            resizeContainer();
            
        }}, 200); // 防抖，避免频繁重绘
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
            ['#87CEFA', '#1E90FF'],  // 天蓝渐变
        ],
        autoFontSize: true,
        cursorWhenHover: 'pointer'
    }};

    // 初始化词云
    wordCloud = new B2wordcloud(container, wordCloudConfig);
}}

// 页面加载完成后初始化
if (document.readyState === 'loading') {{
    document.addEventListener('DOMContentLoaded', initWordCloud);
}} else {{
    initWordCloud();
}}
"""
    return js_content


if __name__ == "__main__":
    generate_wordcloud_data()
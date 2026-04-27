#!/usr/bin/env python3
"""
Generate word cloud data from publications.md
Usage: python3 generate_wordcloud.py
"""

import re
from collections import Counter

PUBLICATIONS_FILE = "_pages/publications.md"
OUTPUT_FILE = "assets/js/wordcloud_data.js"

KEYWORD_PATTERNS = {
    "Wearable Electronics": [
        r"wearable", r"skin-interface", r" electronic",
        r"skin.*electronic", r" electronic tattoo",
    ],
    "Bioelectronics": [
        r"bioelectronic", r"bioelectronics", r"bio-electronic",
    ],
    "Sensors": [
        r"sens", r"monitor", r"measurement",
    ],
    "Health Monitoring": [
        r"health", r"monitoring", r"patient", r"diagnosis",
    ],
    "Skin-Interface": [
        r"skin.*interface", r"skin-adhesive", r"skin-conformal",
    ],
    "Neuromorphic": [
        r"neuromorphic", r"neural",
    ],
    "Flexibility": [
        r"flexible", r"stretchable", r"soft",
    ],
    "Energy Harvesting": [
        r"energy", r"harvest", r"power", r"battery",
    ],
    "Microfluidics": [
        r"microfluidic", r"fluid",
    ],
    "Thermal Regulation": [
        r"thermal", r"cooling", r"heating",
    ],
    "Haptic Interfaces": [
        r"haptic", r"feedback",
    ],
    "Neural Interfaces": [
        r"neural.*interface", r"brain.*computer",
    ],
    "Soft Robotics": [
        r"soft.*robotic", r"robotic",
    ],
    "Biomedical Engineering": [
        r"biomedical", r"biological",
    ],
    "Material Science": [
        r"material", r"polymer", r"nanomaterial",
    ],
    "Data Science": [
        r"data", r"signal", r"processing",
    ],
    "Machine Learning": [
        r"machine.*learn", r"deep.*learn", r"ai", r"artificial.*intelligence",
    ],
    "Cancer Research": [
        r"cancer", r"oncology",
    ],
    "Neuroscience": [
        r"neuroscience", r"neurological",
    ],
    "Cell Biology": [
        r"cell", r"cellular",
    ],
    "Organ-on-Chip": [
        r"organ.*chip", r"organ.*on.*chip",
    ],
    "Nanotechnology": [
        r"nano", r"nanofabrication",
    ],
    "Flexible Electronics": [
        r"flexible.*electronic", r"soft.*electronic",
    ],
    "Haptic Feedback": [
        r"haptic.*feedback", r" tactile",
    ],
    "AR/VR": [
        r"ar.*vr", r"vr.*ar", r"augmented.*reality", r"virtual.*reality",
    ],
}


def extract_keywords_from_publications():
    """Extract keywords from publications.md file."""
    try:
        with open(PUBLICATIONS_FILE, "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: {PUBLICATIONS_FILE} not found")
        return []

    papers = re.split(r"\n\s*&nbsp;\n", content)
    keyword_counts = Counter()
    
    for paper in papers:
        # Title comes after (MM/YYYY). and before ***
        title_match = re.search(r"\(\d{2}/\d{4}\)\.\s*(.+?)\.\s*\*\*\*", paper)
        
        if title_match:
            title = title_match.group(1).lower()
            
            for keyword, patterns in KEYWORD_PATTERNS.items():
                for pattern in patterns:
                    if re.search(pattern, title, re.IGNORECASE):
                        keyword_counts[keyword] += 1
                        break
    
    return keyword_counts


def generate_frequency(count, max_count):
    """Generate frequency value (0-100)."""
    if max_count <= 0:
        return 10
    return max(10, int((count / max_count) * 100))


def generate_wordcloud_data():
    """Generate word cloud data file."""
    keyword_counts = extract_keywords_from_publications()
    
    if not keyword_counts:
        print("No keywords found in publications")
        return
    
    max_count = max(keyword_counts.values()) if keyword_counts else 1
    
    sorted_keywords = sorted(
        keyword_counts.items(), 
        key=lambda x: x[1], 
        reverse=True
    )
    
    word_data = []
    for keyword, count in sorted_keywords[:60]:  # Get top 60 keywords
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
    word_list_str = ",\n        ".join(
        f"['{item[0]}', {item[1]}]" for item in word_data
    )
    
    js_content = f"""// Auto-generated Word Cloud Data from Publications
// Run generate_wordcloud.py to update this file
var wordCloud = new B2wordcloud(document.getElementById("word-cloud"), {{
    list: [
        {word_list_str}
    ],
    weightFactor: 10,
    effect: 'linerMap',
    tooltip: {{
        show: false,
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
}})

wordCloud.dispatchAction({{
    type: 'highlight',
    dataIndex: 0,
    keepAlive: false
}})
"""
    return js_content


if __name__ == "__main__":
    generate_wordcloud_data()

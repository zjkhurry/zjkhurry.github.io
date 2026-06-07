import json
import os
import requests
from datetime import datetime

SERPAPI_KEY = os.environ['SERPAPI_KEY']
AUTHOR_ID = os.environ['GOOGLE_SCHOLAR_ID']

BASE = 'https://serpapi.com/search'


def fetch_page(author_id, hl='en', start=0, num=100):
    params = {
        'engine': 'google_scholar_author',
        'author_id': author_id,
        'hl': hl,
        'start': start,
        'num': num,
        'api_key': SERPAPI_KEY,
    }
    resp = requests.get(BASE, params=params)
    resp.raise_for_status()
    return resp.json()


def fetch_all_articles(author_id, hl='en'):
    data = fetch_page(author_id, hl=hl, start=0, num=100)
    articles = list(data.get('articles', []))
    start = 100
    while len(articles) % 100 == 0 and start < 1000:
        try:
            data = fetch_page(author_id, hl=hl, start=start, num=100)
            page_articles = data.get('articles', [])
            if not page_articles:
                break
            articles.extend(page_articles)
            start += 100
        except Exception:
            break
    return articles, data


def main():
    articles, raw = fetch_all_articles(AUTHOR_ID)

    # --- Author profile ---
    author_info = raw.get('author', {})
    name = author_info.get('name', '')
    affiliation = author_info.get('affiliations', '')
    interests = [item.get('title', '') for item in author_info.get('interests', [])]

    # --- Cited by table (hIndex, i10Index, cites_per_year via graph) ---
    cited_by_table = raw.get('cited_by', {}).get('table', [])
    cited_by_graph = raw.get('cited_by', {}).get('graph', [])

    citedby = 0
    citedby5y = 0
    hindex = 0
    hindex5y = 0
    i10index = 0
    i10index5y = 0
    cites_per_year = {}

    for entry in cited_by_table:
        if 'citations' in entry:
            citedby = entry['citations'].get('all', 0)
            citedby5y = entry['citations'].get('since_2016', 0)
        if 'h_index' in entry:
            hindex = entry['h_index'].get('all', 0)
            hindex5y = entry['h_index'].get('since_2016', 0)
        if 'i10_index' in entry:
            i10index = entry['i10_index'].get('all', 0)
            i10index5y = entry['i10_index'].get('since_2016', 0)

    # Build cites_per_year from graph data
    for g in cited_by_graph:
        year = str(g.get('year', ''))
        cites_per_year[year] = g.get('citations', 0)

    # --- Publications ---
    # SerpApi gives flat article dicts; map to scholarly Publication structure
    publications = {}
    for art in articles:
        cid = art.get('citation_id', '')
        cited_by_obj = art.get('cited_by', {})
        publications[cid] = {
            'container_type': 'Publication',
            'source': 'AUTHOR_PUBLICATION_ENTRY',
            'bib': {
                'title': art.get('title', ''),
                'pub_year': str(art.get('year', '')),
                'citation': art.get('publication', ''),
            },
            'filled': False,
            'author_pub_id': cid,
            'num_citations': cited_by_obj.get('value', 0),
            'citedby_url': cited_by_obj.get('link', ''),
            'cites_id': [],  # SerpApi doesn't expose cites_id
        }

    # --- Assemble output matching original scholarly dict exactly ---
    result = {
        'container_type': 'Author',
        'filled': ['basics', 'publications', 'indices', 'counts'],
        'scholar_id': AUTHOR_ID,
        'source': 'AUTHOR_PROFILE_PAGE',
        'name': name,
        'url_picture': '',
        'affiliation': affiliation,
        'organization': 0,
        'interests': interests,
        'email_domain': '',
        'citedby': citedby,
        'publications': publications,
        'citedby5y': citedby5y,
        'hindex': hindex,
        'hindex5y': hindex5y,
        'i10index': i10index,
        'i10index5y': i10index5y,
        'cites_per_year': cites_per_year,
        'updated': str(datetime.now()),
    }

    print(json.dumps(result, indent=2, ensure_ascii=False))

    os.makedirs('results', exist_ok=True)
    with open('results/gs_data.json', 'w', encoding='utf-8') as outfile:
        json.dump(result, outfile, ensure_ascii=False)

    shieldio_data = {
        'schemaVersion': 1,
        'label': 'citations',
        'message': str(citedby),
    }
    with open('results/gs_data_shieldsio.json', 'w', encoding='utf-8') as outfile:
        json.dump(shieldio_data, outfile, ensure_ascii=False)


if __name__ == '__main__':
    main()

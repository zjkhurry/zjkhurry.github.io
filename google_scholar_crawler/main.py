from scholarly import scholarly, ProxyGenerator
import jsonpickle
import json
from datetime import datetime
import os

# main.py 顶部添加
from fp.fp import FreeProxy
import inspect

# 检查 get_proxy_list 是否需要 repeat 参数但 scholarly 没传
sig = inspect.signature(FreeProxy.get_proxy_list)
if 'repeat' in sig.parameters:
    _original_get_proxy_list = FreeProxy.get_proxy_list
    def _patched_get_proxy_list(self, *args, **kwargs):
        kwargs.setdefault('repeat', True)
        return _original_get_proxy_list(self, *args, **kwargs)
    FreeProxy.get_proxy_list = _patched_get_proxy_list

# 然后再执行原有的 scholarly 逻辑
scholarly.use_proxy(pg)

# Setup proxy
pg = ProxyGenerator()
pg.FreeProxies()  # Use free rotating proxies
scholarly.use_proxy(pg)

author: dict = scholarly.search_author_id(os.environ['GOOGLE_SCHOLAR_ID'])
scholarly.fill(author, sections=['basics', 'indices', 'counts', 'publications'])
name = author['name']
author['updated'] = str(datetime.now())
author['publications'] = {v['author_pub_id']:v for v in author['publications']}
print(json.dumps(author, indent=2))
os.makedirs('results', exist_ok=True)
with open(f'results/gs_data.json', 'w') as outfile:
    json.dump(author, outfile, ensure_ascii=False)

shieldio_data = {
  "schemaVersion": 1,
  "label": "citations",
  "message": f"{author['citedby']}",
}
with open(f'results/gs_data_shieldsio.json', 'w') as outfile:
    json.dump(shieldio_data, outfile, ensure_ascii=False)

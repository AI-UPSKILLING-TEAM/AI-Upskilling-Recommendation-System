"""Check outbound catalog references without downloading full articles."""
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
import sys
from urllib.request import Request,urlopen
from urllib.error import HTTPError
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from recommendations import CATALOG,CERTIFICATION_OPTIONS

def check(row):
 name,url=row
 try:
  with urlopen(Request(url,headers={'User-Agent':'SkillPath-Link-Audit/1.0'},method='HEAD'),timeout=20) as r:
   return {'title':name,'url':url,'status':r.status,'final_url':r.url,'result':'reachable'}
 except HTTPError as e:
  return {'title':name,'url':url,'status':e.code,'result':'blocked_by_provider' if e.code in (403,429) else 'http_error'}
 except Exception as e:return {'title':name,'url':url,'result':'unverified','error':str(e)}
if __name__=='__main__':
 links=[(v[0],v[1]) for v in CATALOG.values()]+[(v['title'],v['url']) for v in CERTIFICATION_OPTIONS.values()]
 with ThreadPoolExecutor(max_workers=5) as p:rows=list(p.map(check,links))
 out=Path(__file__).resolve().parents[1]/'evidence';out.mkdir(exist_ok=True)
 (out/'link-audit.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
 print(json.dumps(rows,indent=2))

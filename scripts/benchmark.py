"""Small local performance measurement with isolated disposable accounts."""
import concurrent.futures
import json
from pathlib import Path
import statistics
import sys
import tempfile
import threading
import time
from urllib.request import Request,urlopen
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from app import make_server

def measure():
 with tempfile.TemporaryDirectory() as folder:
  server=make_server('127.0.0.1',0,Path(folder)/'perf.db')
  thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
  base='http://127.0.0.1:'+str(server.server_address[1])
  def call(route,data=None,token=None):
   headers={'Content-Type':'application/json'}
   if token:headers['Authorization']='Bearer '+token
   req=Request(base+route,json.dumps(data).encode() if data is not None else None,headers)
   start=time.perf_counter()
   with urlopen(req,timeout=10) as r:result=json.load(r)
   return (time.perf_counter()-start)*1000,result
  try:
   call('/api/register',{'name':'Benchmark','email':'perf@example.com','password':'Benchmark2026!'})
   _,auth=call('/api/login',{'email':'perf@example.com','password':'Benchmark2026!'})
   token=auth['token'];call('/api/profile',{'name':'Benchmark','goal':'Data Scientist','interests':'machine learning statistics'},token)
   samples=[call('/api/dashboard',token=token)[0] for _ in range(30)]
   with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
    parallel_samples=list(pool.map(lambda _:call('/api/dashboard',token=token)[0],range(30)))
   summarize=lambda values:{'requests':len(values),'median_ms':round(statistics.median(values),2),'p95_ms':round(sorted(values)[int(.95*(len(values)-1))],2),'max_ms':round(max(values),2)}
   return {'scenario':'Localhost, one disposable student, seeded small catalog; 30 serial and 30 requests with 5 workers',
           'proposed_target_ms':2000,'serial':summarize(samples),'concurrent_5':summarize(parallel_samples),
           'target_met':max(samples+parallel_samples)<2000,'limits':'Local smoke benchmark, not production capacity certification'}
  finally:server.shutdown();server.server_close();thread.join()
if __name__=='__main__':
 result=measure();out=Path(__file__).resolve().parents[1]/'evidence';out.mkdir(exist_ok=True)
 (out/'performance.json').write_text(json.dumps(result,indent=2),encoding='utf-8');print(json.dumps(result,indent=2))
 if not result['target_met']:raise SystemExit(1)

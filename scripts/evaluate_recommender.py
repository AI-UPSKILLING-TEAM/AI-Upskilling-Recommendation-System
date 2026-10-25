"""Reproducible reference-case evaluation; not a real-student outcome study."""
import json
import math
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from app import CAREER_PATHS
from recommendations import rank_learning

CASES = [
 ('Data Analyst','sql relational databases querying',['SQL']),
 ('Data Analyst','excel spreadsheets budget workbook',['Excel']),
 ('Data Scientist','machine learning artificial intelligence',['Machine Learning']),
 ('Data Scientist','statistics probability data analysis',['Statistics']),
 ('Web Developer','html markup accessible websites',['HTML']),
 ('Web Developer','css styling frontend',['CSS']),
 ('Backend Developer','automated unit testing software quality',['Testing']),
 ('Backend Developer','relational sql databases queries',['SQL']),
 ('Cloud Engineer','linux shell commands operations',['Linux']),
 ('Cloud Engineer','cloud fundamentals computing architecture',['Cloud Fundamentals']),
 ('Cybersecurity Analyst','networking protocols infrastructure',['Networking']),
 ('Cybersecurity Analyst','cybersecurity vulnerability web protection',['Security Fundamentals']),
]

def evaluate():
 rows=[]
 for goal,interests,relevant in CASES:
  candidates=CAREER_PATHS[goal]
  ranked=[r['skill'] for r in rank_learning(candidates,goal,interests)]
  hit=[int(s in relevant) for s in ranked]
  first=next((i+1 for i,v in enumerate(hit) if v),None)
  baseline=next(i+1 for i,s in enumerate(candidates) if s in relevant)
  rows.append({'goal':goal,'interests':interests,'relevant':relevant,'ranking':ranked,
               'reciprocal_rank':1/first if first else 0,'baseline_reciprocal_rank':1/baseline,
               'hit_at_3':int(any(hit[:3]))})
 return {'method':'TF-IDF cosine similarity','dataset':'12 author-defined synthetic reference cases, one relevant topic per case',
         'limitations':'Small, catalog-derived, non-independent reference set. No real-user efficacy or predictive accuracy claim.',
         'cases':rows,'mean_reciprocal_rank':round(sum(r['reciprocal_rank'] for r in rows)/len(rows),4),
         'fixed_order_baseline_mrr':round(sum(r['baseline_reciprocal_rank'] for r in rows)/len(rows),4),
         'hit_rate_at_3':round(sum(r['hit_at_3'] for r in rows)/len(rows),4)}
if __name__=='__main__':
 out=Path(__file__).resolve().parents[1]/'evidence';out.mkdir(exist_ok=True)
 result=evaluate();(out/'recommender-evaluation.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
 print(json.dumps({k:v for k,v in result.items() if k!='cases'},indent=2))

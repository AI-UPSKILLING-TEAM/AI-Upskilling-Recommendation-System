"""Online SQLite backup, with an integrity check. Never commit the result."""
import argparse
from pathlib import Path
import sqlite3
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from app import DB_PATH

def backup(source,destination):
 source=Path(source).resolve();destination=Path(destination).resolve()
 if not source.is_file():raise ValueError('Source database does not exist')
 if source==destination or destination.exists():raise ValueError('Choose a new backup filename')
 destination.parent.mkdir(parents=True,exist_ok=True)
 src=sqlite3.connect(str(source));dst=sqlite3.connect(str(destination))
 try:
  src.backup(dst)
  if dst.execute('PRAGMA integrity_check').fetchone()[0]!='ok':raise RuntimeError('Backup integrity check failed')
 finally:dst.close();src.close()
 return destination
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('destination');parser.add_argument('--source',default=str(DB_PATH));args=parser.parse_args()
 print(backup(args.source,args.destination))

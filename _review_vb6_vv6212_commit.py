"""Stage only this bounded task's files in the two authorized repositories."""
from pathlib import Path
import json,subprocess,sys
W=Path(__file__).resolve().parent;O=Path(json.loads((W/'meta.json').read_text())['repo_dir'])
shared=['README.md','REVIEW.md','SOURCES.md','status.json','validation.json','quality-report.json','source-manifest.json','audit-result.json','annex-coverage.json','preflight-coverage.json','preflight-result.json','review-result.json','review-vb6-vv6212-result.json','review-vb6-vv6212-notes.json','review-vb6-vv6212-unit-evidence.json','sources/verification.json','sources/search-log.json','sources/review-vb6-vv6212-2026-10-20','cases/README.md','cases/bverwg-2009-2-av-4-09.md','cases/olg-muenchen-2021-4-ws-3-21.md','cases/bverwg-2015-2-wdb-1-15.md']
scripts=[p.name for p in W.glob('_review_vb6_vv6212*.py')]
for root,extra in [(W,['commentary/part-13-vv6.md']),(O,['16-vv-teil-6.md'])]:
 paths=[p for p in shared+scripts+extra if (root/p).exists()]
 existing=subprocess.check_output(['git','-C',str(root),'diff','--cached','--name-only'],text=True).splitlines()
 assert all(any(x==p or x.startswith(p+'/') for p in paths) for x in existing),existing
 subprocess.run(['git','-C',str(root),'add','--']+paths,check=True)
 # Keep downloaded evidence byte-exact, including native whitespace. Check authored files only.
 subprocess.run(['git','-C',str(root),'diff','--cached','--check','--','.',':(exclude)sources/**'],check=True)
 staged=subprocess.check_output(['git','-C',str(root),'diff','--cached','--name-only'],text=True).splitlines()
 assert staged
 subprocess.run(['git','-C',str(root),'commit','-q','-m',sys.argv[1]],check=True)
 print(json.dumps(dict(repo=str(root),commit=subprocess.check_output(['git','-C',str(root),'rev-parse','HEAD'],text=True).strip(),files=len(staged))))

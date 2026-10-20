"""Stage only this bounded task's files in the two authorized repositories."""
from pathlib import Path
import json,subprocess,sys
W=Path(__file__).resolve().parent;O=Path(json.loads((W/'meta.json').read_text())['repo_dir'])
shared=['README.md','REVIEW.md','SOURCES.md','status.json','validation.json','quality-report.json','source-manifest.json','audit-result.json','preflight-result.json','review-result.json','review-vv3337-vv3507-result.json','review-vv3337-vv3507-notes.json','review-vv3337-vv3507-unit-evidence.json','sources/verification.json','sources/search-log.json','sources/review-vv3337-vv3507-2026-10-20','cases/README.md','cases/bag-2012-3-azb-22-11.md','cases/bgh-2013-xi-zb-2-13.md','cases/bgh-2024-vi-zb-58-22.md']
scripts=[p.name for p in W.glob('_review_vv3337_vv3507*.py')]
for root,extra in [(W,['commentary/part-08-vv3b.md','commentary/part-09-vv3c.md']),(O,['13-vv-teil-3.md'])]:
 paths=[p for p in shared+scripts+extra if (root/p).exists()]
 subprocess.run(['git','-C',str(root),'add','--']+paths,check=True)
 # Keep downloaded evidence byte-exact, including native whitespace. Check authored files only.
 subprocess.run(['git','-C',str(root),'diff','--cached','--check','--','.',':(exclude)sources/**'],check=True)
 staged=subprocess.check_output(['git','-C',str(root),'diff','--cached','--name-only'],text=True).splitlines()
 assert staged
 subprocess.run(['git','-C',str(root),'commit','-q','-m',sys.argv[1]],check=True)
 print(json.dumps(dict(repo=str(root),commit=subprocess.check_output(['git','-C',str(root),'rev-parse','HEAD'],text=True).strip(),files=len(staged))))

"""Stage only this bounded task's files in the two authorized repositories."""
from pathlib import Path
import json,subprocess,sys
W=Path(__file__).resolve().parent;O=Path(json.loads((W/'meta.json').read_text())['repo_dir'])
shared=['README.md','REVIEW.md','SOURCES.md','status.json','validation.json','quality-report.json','source-manifest.json','audit-result.json','preflight-result.json','review-result.json','review-vv4145-vb5_1-result.json','review-vv4145-vb5_1-notes.json','review-vv4145-vb5_1-unit-evidence.json','sources/verification.json','sources/search-log.json','sources/review-vv4145-vb5_1-2026-10-20','cases/README.md','cases/bgh-2025-3-bgs-440-25.md']
scripts=[p.name for p in W.glob('_review_vv4145_vb5_1*.py')]
for root,extra in [(W,['commentary/part-11-vv4b.md','commentary/part-12-vv5.md']),(O,['14-vv-teil-4.md','15-vv-teil-5.md'])]:
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

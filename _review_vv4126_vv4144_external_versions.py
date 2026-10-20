from pathlib import Path
import urllib.request,hashlib,datetime,json,subprocess,xml.etree.ElementTree as E
W=Path(__file__).resolve().parent;D=W/'sources/review-vv4126-vv4144-2026-10-20';records=[]
for year,num in [(2026,199),(2026,95),(2025,63)]:
 url=f'https://www.recht.bund.de/bgbl/1/{year}/{num}/regelungstext.pdf?__blob=publicationFile&v=2';t=datetime.datetime.now(datetime.timezone.utc).isoformat()
 with urllib.request.urlopen(url,timeout=35) as h:b=h.read();st=h.status;ct=h.headers.get('Content-Type')
 assert b.startswith(b'%PDF-');p=D/f'bgbl-{year}-{num}.pdf';p.write_bytes(b)
 subprocess.run(['pdftotext','-layout',str(p),str(p.with_suffix('.txt'))],check=True);assert p.with_suffix('.txt').stat().st_size>100
 records.append(dict(url=url,accessed_at=t,http_status=st,content_type=ct,local_path=str(p.relative_to(W)),sha256=hashlib.sha256(b).hexdigest(),text_path=str(p.with_suffix('.txt').relative_to(W)),validated_format='Actual PDF signature and successful nonempty text extraction',purpose='Check current external StPO/StrRehaG amendment context, limited to cross-references used in assigned commentary'))
(D/'external-version-requests.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n');p=W/'sources/verification.json';v=json.loads(p.read_text());v['requests']+=records;p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(records,ensure_ascii=False))
# Record actual commencement reading after downloading, not inference from metadata.
p=D/'version-evidence.json';v=json.loads(p.read_text())
v['external_version_preflight']={
 'records':str((D/'external-version-requests.json').relative_to(W)),
 'stpo_stand':'Art. 2(7) G20.3.2026 I Nr95; textually documented Art15(16) G3.7.2026 I Nr199',
 'stpo_actual_amendments_read':[
  {'act':'BGBl.2026 I Nr95','amending_provision':'Art2(7)','affected_sections':['100a','100b','100g','103','111','112a','443'],'commencement':'Art4: day after promulgation on1April2026 =2April2026','assigned_context_affected':False},
  {'act':'BGBl.2026 I Nr199','amending_provision':'Art15(16)','affected_sections':['492(3)sentence4'],'commencement':'Art16(3):1January2027','selection':'Future-dated text not used. Section492 is outside every cross-reference discussed in this batch; operative quoted sections unchanged by this amendment.'}],
 'strrehag_stand':'Art3 G25.2.2025 I Nr63',
 'strrehag_actual_amendment_read':'Art3 read: does not amend §13. Art7(2) makes Art3 effective1July2025.',
 'context_sections_actually_read':['StPO364b','StPO368','StPO369','StPO370','StPO371','StPO372','StPO403','StPO404','StPO411','StrRehaG13'],
 'limitation':'Latest listed external amendments and commencement checked for these sections only; no exhaustive external historical archive.',
 'unresolved_blockers':[]}
p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')

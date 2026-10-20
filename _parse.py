#!/usr/bin/env python3
"""Reproducible GII RVG XML extraction; full annexes plus addressable VV children."""
import json,re,hashlib,shutil
from pathlib import Path
import xml.etree.ElementTree as E
W=Path(__file__).resolve().parent
R=E.parse(W/'sources/rvg.xml').getroot()
def render(e):
 if e is None:return ''
 s=e.text or ''
 for c in e:
  t=c.tag
  x=render(c)
  if t=='noindex':pass
  elif t=='BR':s+='\n'
  elif t=='row':s+='\n\n'+x+'\n\n'
  elif t=='entry':s+=x+' | '
  elif t in ('P','DL','DD','DT','Title','LA'):s+='\n'+x+'\n'
  else:s+=x
  s+=c.tail or ''
 return s
def clean(s):
 s=re.sub(r'[ \t\r\f\v]+',' ',s)
 s=re.sub(r' *\n *','\n',s)
 return re.sub(r'\n{3,}','\n\n',s).strip()
def txt(e):return clean(render(e))
def dump(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
# Preserve the unnumbered statutory header and global official notes as evidence.
# RVG has no separate Eingangsformel in this consolidation; do not invent a unit.
header=R.find('norm')
frontmatter={'source':'sources/rvg.xml','xml_sha256':hashlib.sha256((W/'sources/rvg.xml').read_bytes()).hexdigest(),
 'doknr':header.get('doknr'),'official_title':header.findtext('metadaten/langue'),
 'version_notes':[txt(x) for x in header.findall('metadaten/standangabe/standkommentar')],
 'official_global_notes':[txt(x) for x in header.findall('textdaten/fussnoten/Content')],
 'eingangsformel_disposition':'No separate Eingangsformel/Präambel norm or operative unlabelled Content in the official RVG XML. The introductory enactment/commencement notice is a global official footnote, preserved here.',
 'contents_disposition':'Inhaltsübersicht retained in raw XML as an editorial navigation unit; all its provision references are checked separately against operative norms.'}
dump(W/'sources/rvg-frontmatter.json',frontmatter)
units=[];struct=[];chap=0;chapters=[];expected=[];ann=None
for n in R.findall('norm'):
 m=n.find('metadaten');label=m.findtext('enbez') or '';g=m.find('gliederungseinheit')
 if g is not None:
  chap+=1;h=txt(g.find('gliederungsbez'))+' — '+txt(g.find('gliederungstitel'));struct=[h];chapters.append({'n':chap,'slug':'abschnitt-'+str(chap),'title':h})
 if not (label.startswith('§') or label.startswith('Anlage')):continue
 uid='p'+label[2:].strip() if label.startswith('§') else 'a'+label.split()[-1]
 if uid.startswith('a'):
  ch=10;st=['Anlagen'];ann=n if uid=='a1' else ann
 else:ch=chap;st=list(struct)
 body=txt(n.find('textdaten/text/Content'));notes=[txt(x) for x in n.findall('textdaten/fussnoten/Content')]+[clean(''.join(x.itertext())) for x in n.findall('.//noindex')]
 u={'id':uid,'label':label,'title':txt(m.find('titel')),'chapter':ch,'structure':st,'text':body,'notes':notes,'xml_doknr':n.get('doknr')}
 units.append(u);expected.append(uid)
chapters.append({'n':10,'slug':'anlagen','title':'Anlagen 1 und 2: vollständiger amtlicher Text'})
# Retain entire Anlage 1 above. Index every tariff and operative preliminary remark separately.
extra=[];cur=None;st=[];rawids=[];vbids=[]
for table in ann.findall('.//table'):
 title=txt(table.find('Title'))
 if not title:continue # introductory contents table, retained in a1
 st=[re.sub(r'\s+',' ',title)]
 for row in table.findall('./tgroup/tbody/row'):
  es=row.findall('entry');ss=[txt(e) for e in es];joined=txt(row)
  if not any(ss):continue
  first=ss[0] if ss else ''
  vb=re.match(r'^Vorbemerkung (\d[\d.]*):',first)
  numbered=re.fullmatch(r'\d{4}',first)
  heading=(len(es)==1 and bool(re.match(r'^(?:Abschnitt |Unterabschnitt |Erster Rechtszug$|Zweiter Rechtszug$|Dritter Rechtszug$|Berufung$|Revision$)',re.sub(r'\s+',' ',first))))
  if numbered or vb:
   if cur:extra.append(cur)
   ident='vv'+first if numbered else 'vb'+vb.group(1)
   if numbered:rawids.append(ident)
   else:vbids.append(ident)
   cur={'id':ident,'label':('Nr. '+first+' VV' if numbered else 'Vorbemerkung '+vb.group(1)+' VV'),'title':(ss[1][:160].split('\n')[0] if numbered and len(ss)>1 else ''),'chapter':10+int((first if numbered else vb.group(1))[0]),'structure':list(st),'text':joined,'notes':[],'parent':'a1'}
  elif heading:
   if cur:extra.append(cur);cur=None
   h=re.sub(r'\s+',' ',first)
   if h.startswith('Abschnitt '):st=st[:1]+[h]
   elif h.startswith('Unterabschnitt '):st=[v for v in st if not v.startswith('Unterabschnitt ') and v not in ('Erster Rechtszug','Zweiter Rechtszug','Dritter Rechtszug','Berufung','Revision')]+[h]
   elif h in ('Erster Rechtszug','Zweiter Rechtszug','Dritter Rechtszug','Berufung','Revision'):st=[v for v in st if v not in ('Erster Rechtszug','Zweiter Rechtszug','Dritter Rechtszug','Berufung','Revision')]+[h]
   else:st=st[:1]+[h]
  elif cur:
   # Column header rows never continue a preceding tariff.
   if first in ('Nr.','Gebührentatbestand') or 'Gebührentatbestand' in joined and 'Nr.' in joined:continue
   cur['text']+='\n\n'+joined
 if cur:extra.append(cur);cur=None
units+=extra
for part in range(1,8):chapters.append({'n':10+part,'slug':'vv-teil-'+str(part),'title':'Vergütungsverzeichnis, Teil '+str(part)+' – Einzelkommentierung'})
ids=[u['id'] for u in units];assert len(ids)==len(set(ids)),ids
(W/'units.jsonl').write_text(''.join(json.dumps(u,ensure_ascii=False)+'\n' for u in units))
canonical='# RVG – mechanische Lesefassung aus sources/rvg.xml\n\n'+frontmatter['official_title']+'\n\n'+'\n\n'.join(frontmatter['version_notes']+frontmatter['official_global_notes'])+'\n\n'+'\n\n'.join(u['label']+' '+u['title']+'\n\n'+u['text'] for u in units if not u.get('parent'))+'\n'
# Extra indexed row strings are also present in the full annex; canonical retains exact extraction.
(W/'sources/canonical.md').write_text(canonical)
meta={'cc':'de','lang':'de','repo':'Komentar-DE-RVG-2004','repo_dir':'/Volumes/LaCie/open-commentary/de/Komentar-DE-RVG-2004','title':'Kommentar zum Rechtsanwaltsvergütungsgesetz (RVG)','source_path':str(W/'sources/canonical.md'),'intro_file':'00-einleitung.md','intro_desc':'Systematik, Methode und Quellenstand','labels':{'text':'Wortlaut der Vorschrift','chapter':'Kommentarkapitel','notes':'Amtlicher Quellenhinweis'},'chapters':chapters,'legal_text_date':'2026-10-19','raw_xml_path':str(W/'sources/rvg.xml')}
dump(W/'meta.json',meta)
# Independent expected tariff list from every XML row, regardless of extraction state machine.
xmlvv=['vv'+txt(row.find('entry')) for row in ann.findall('.//row') if re.fullmatch(r'\d{4}',txt(row.find('entry')))];xmlvb=[]
for row in ann.findall('.//row'):
 s=txt(row.find('entry'));v=re.match(r'^Vorbemerkung (\d[\d.]*):',s)
 if v:xmlvb.append('vb'+v.group(1))
all_expected=expected+xmlvv+xmlvb
missing=sorted(set(all_expected)-set(ids));unexpected=sorted(set(ids)-set(all_expected))
report={'xml_sha256':hashlib.sha256((W/'sources/rvg.xml').read_bytes()).hexdigest(),'official_norms':len(expected),'numbered_tariffs':len(xmlvv),'operative_preliminary_remarks':len(xmlvb),'expected_ids':all_expected,'parsed_ids':ids,'missing_ids':missing,'unexpected_ids':unexpected,'duplicate_ids':sorted({i for i in ids if ids.count(i)>1}),'annex_disposition':{'Anlage 1':'Vollständig als a1; zusätzlich sämtliche 231 Tarifnummern und operative Vorbemerkungen einzeln indexiert; nichtnormative Inhaltsgliederung verbleibt im Elterntext.','Anlage 2':'Vollständige Wertgebührentabelle als a2.'},'empty_or_repealed':[u['id'] for u in units if 'weggefallen' in u['text'] and len(u['text'])<250],'structural_headings':'Neun Gesetzesabschnitte, VV-Teile, Abschnitte und Unterabschnitte sind Struktur, keine erfundenen Paragraphen. Fehlende Nummern werden nicht als aufgehoben ergänzt.','ok':not(missing or unexpected) and len(ids)==len(set(ids))}
dump(W/'completeness.json',report)
shutil.copyfile('/Volumes/LaCie/law-intake/eu/de/gesetze/gii-rvg.md',W/'sources/intake-2026-10-02.md')
print(json.dumps({k:report[k] for k in ('official_norms','numbered_tariffs','operative_preliminary_remarks','missing_ids','ok')}))

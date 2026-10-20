#!/usr/bin/env python3
"""Derive RVG identifiers from official XML before consulting parser output.

This script neither imports _parse.py nor uses units.jsonl to generate expected IDs.
The full XML remains the evidence for each annex entry, including unindexed rows.
"""
from pathlib import Path
import collections, datetime, hashlib, json, re, unicodedata
import xml.etree.ElementTree as E

W = Path(__file__).resolve().parent
P = W / 'sources/rvg.xml'
R = E.parse(P).getroot()
HASH = hashlib.sha256(P.read_bytes()).hexdigest()
def dump(name, obj):
    (W/name).write_text(json.dumps(obj, ensure_ascii=False, indent=2)+'\n')
def raw(e):
    if e is None:
        return ''
    out = e.text or ''
    for child in e:
        if child.tag != 'noindex':
            out += raw(child)
        out += child.tail or ''
    return out
def squeeze(s):
    return re.sub(r'[\s|]+', '', unicodedata.normalize('NFKC', s))
def unit_id(label):
    if label.startswith('§ '):
        return 'p'+label[2:].strip()
    if label.startswith('Anlage '):
        return 'a'+label.split()[-1]
    raise ValueError('Unclassified operative label: '+label)

norms = R.findall('norm')
labels = [n.findtext('metadaten/enbez') for n in norms]
expected = []
classified = []
entries = []
details = []
for index, n in enumerate(norms):
    label = n.findtext('metadaten/enbez') or ''
    content = n.find('textdaten/text/Content')
    content_text = raw(content)
    if label == 'Inhaltsübersicht':
        disposition = 'editorial contents list; not a second set of operative provisions'
    elif not label:
        if squeeze(content_text):
            raise ValueError('Unlabelled operative content requires an explicit unit: '+n.get('doknr'))
        disposition = 'global metadata/official footnotes' if index == 0 else 'structural section heading'
    else:
        uid = unit_id(label)
        expected.append(uid)
        disposition = 'operative provision' if uid.startswith('p') else 'operative annex'
        if uid.startswith('a'):
            child_ids, child_evidence, row_details = [], [], []
            for ti, table in enumerate(n.findall('.//table')):
                for ri, row in enumerate(table.findall('.//row')):
                    first = raw(row.find('entry')).strip()
                    text = raw(row)
                    child_id = None
                    if re.fullmatch(r'\d{4}', first):
                        child_id = 'vv'+first
                    elif (match := re.match(r'^Vorbemerkung\s+(\d[\d.]*):', first)):
                        child_id = 'vb'+match.group(1)
                    row_path = f"./norm[{index+1}]/textdaten/text/Content//table[{ti+1}]//row[{ri+1}]"
                    if child_id:
                        child_ids.append(child_id)
                        child_evidence.append({'id':child_id,'first_cell':first,'xml_location':row_path})
                    row_details.append({'table_index':ti,'row_index':ri,'child_id':child_id,
                                        'text_sha256':hashlib.sha256(text.encode()).hexdigest(),
                                        'first_cell':first[:220],
                                        'disposition':'indexed tariff/preliminary remark' if child_id else 'retained in complete parent annex'})
            entries.append({'parent_label':label,'expected_child_ids':child_ids,
                            'evidence_path':str(P),'evidence_sha256':HASH})
            details.append({'parent_label':label,'parent_id':uid,'number_of_tables':len(n.findall('.//table')),
                            'rows':row_details,'independent_child_locations':child_evidence,
                            'disposition': 'All tariff numbers and operative Vorbemerkungen individually indexed; all table headers, contents, structure and continuation rows additionally preserved in the complete a1 text.' if uid=='a1' else 'Complete value/fee table preserved as a2. Value rows have no statutory provision identifiers; no invented child IDs.'})
    classified.append({'index':index,'doknr':n.get('doknr'),'label':label,'disposition':disposition})

# Expected identifiers are fixed above; only now load the manuscript.
us = [json.loads(line) for line in (W/'units.jsonl').read_text().splitlines() if line.strip()]
ids = [u['id'] for u in us]
by_id = {u['id']:u for u in us}
all_expected = expected + [x for entry in entries for x in entry['expected_child_ids']]
missing = sorted(set(all_expected)-set(ids))
extra = sorted(set(ids)-set(all_expected))
duplicates = [k for k,v in collections.Counter(ids).items() if v>1]
duplicate_official_labels = [k for k,v in collections.Counter(x for x in labels if x).items() if v>1]
duplicate_expected = [k for k,v in collections.Counter(all_expected).items() if v>1]
checks = []
child_checks = []
for n in norms:
    label = n.findtext('metadaten/enbez') or ''
    if label.startswith(('§ ', 'Anlage ')):
        uid = unit_id(label)
        a = squeeze(raw(n.find('textdaten/text/Content')))
        b = squeeze(by_id.get(uid,{}).get('text',''))
        checks.append({'id':uid,'complete_character_stream_equal':a==b})
for entry in entries:
    parent = next(n for n in norms if n.findtext('metadaten/enbez')==entry['parent_label'])
    parent_text = squeeze(' '.join(parent.itertext()))
    parent_id = unit_id(entry['parent_label'])
    for uid in entry['expected_child_ids']:
        u = by_id.get(uid,{})
        text = squeeze(u.get('text',''))
        child_checks.append({'id':uid,'parent_correct':u.get('parent')==parent_id,
                             'child_wording_in_official_parent':bool(text) and text in parent_text})
contents = next(n for n in norms if n.findtext('metadaten/enbez')=='Inhaltsübersicht')
toc_ids = ['p'+raw(e).replace('§','').strip() for e in contents.findall('.//LA')
           if re.fullmatch(r'§\s*\d+[a-z]?',raw(e).strip())]
# Different XML contents layouts exist; record textual references independently too.
toc_refs = list(dict.fromkeys('p'+m for m in re.findall(r'§\s*(\d+[a-z]?)',raw(contents))))
toc_missing = sorted(set(x for x in expected if x.startswith('p'))-set(toc_refs))
bad_contents_refs = sorted(set(toc_refs)-set(expected))
ok = not any((missing,extra,duplicates,duplicate_official_labels,duplicate_expected,toc_missing,bad_contents_refs)) and all(x['complete_character_stream_equal'] for x in checks) and all(x['parent_correct'] and x['child_wording_in_official_parent'] for x in child_checks)
dump('annex-coverage.json',{'derivation':'_preflight_coverage.py: direct official XML first-cell labels, before reading units.jsonl','entries':entries})
report={'official_source':{'url':'https://www.gesetze-im-internet.de/rvg/xml.zip','evidence_path':str(P),'sha256':HASH},
        'official_norm_count':len(expected),'expected_ids':all_expected,'parsed_ids':ids,
        'expected_count':len(all_expected),'parsed_count':len(us),'missing_ids':missing,'extra_ids':extra,
        'duplicate_ids':duplicates,'duplicate_expected_ids':duplicate_expected,'duplicate_official_labels':duplicate_official_labels,
        'all_xml_norms_classified':classified,'annex_details':details,'parent_full_content_checks':checks,
        'annex_child_wording_checks':child_checks,'contents_provision_refs':toc_refs,
        'missing_contents_refs':toc_missing,'unmatched_contents_refs':bad_contents_refs,
        'historical_versions':{'operative_duplicates':duplicate_official_labels,'selection':'One current consolidation, 79 single paragraph nodes and two single annex nodes. Historical quotations and transition references within current provisions are retained as content, not appended as old versions.'},
        'eingangsformel':'No separate Eingangsformel or Präambel and no unlabelled operative Content in this official XML. Global enactment/commencement footnote preserved in sources/rvg-frontmatter.json and canonical.md.',
        'limitations':['Algorithmic preflight of sources and extraction only; no independent substantive review of commentary.','Whitespace and inserted table separators are ignored for full-text checks; all other normative characters are compared.'], 'ok':ok}
dump('preflight-coverage.json',report)
print(json.dumps({k:report[k] for k in ['official_norm_count','expected_count','parsed_count','missing_ids','extra_ids','duplicate_official_labels','ok']}))
if not ok:
    raise SystemExit(1)

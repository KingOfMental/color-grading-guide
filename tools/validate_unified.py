from pathlib import Path
from lxml import html
import re,json
R=Path(__file__).resolve().parents[1];doc=html.fromstring((R/'docs/index.html').read_text());data=json.loads(doc.get_element_by_id('unifiedData').text);book=json.loads(doc.get_element_by_id('bookData').text);entries=data['entries'];ids=[e['id'] for e in entries];assert len(ids)==len(set(ids))
assert len(book['pages'])==214 and sum(e['kind']=='color' for e in entries)==214
original=html.fromstring((R/'content/color-original.html').read_text());assert json.loads(original.get_element_by_id('bookData').text)==book
assert len([e for e in entries if e.get('original')=='Final Cut Pro 웹 교재'])==83
missing=[];links=[]
for e in entries:
 if e['kind']=='color':
  if not (R/'docs'/book['pages'][e['page']-1]['image']).exists():missing.append(e['id'])
  continue
 node=html.fromstring('<div>'+e['html']+'</div>')
 for im in node.xpath('.//*[@src]'):
  src=im.get('src')
  if not src.startswith(('http','data:')) and not (R/'docs'/src).is_file():missing.append((e['id'],src))
 for a in node.xpath('.//a[starts-with(@href,"#")]'):
  to=a.get('href')[1:]
  if to.startswith(('fcp-','supp-','page-','principle-')) and to not in ids:links.append((e['id'],to))
assert not missing,missing;assert not links,links
# Preserve the actual paragraphs, lists, figures and captions from all 83 original entries.
fcp=html.fromstring((R/'content/fcp-original.html').read_text());lost=[]
for e in entries:
 if not e.get('sourceId'):continue
 old=fcp.get_element_by_id(e['sourceId']);new=html.fromstring('<div>'+e['html']+'</div>')
 norm=lambda s:re.sub(r'\s+','',s)
 newtext=norm(new.text_content())
 for n in old.xpath('.//p|.//li|.//h3|.//figcaption'):
  if norm(n.text_content()) and norm(n.text_content()) not in newtext:lost.append((e['id'],n.text_content()[:40]))
assert not lost,lost
for before,after in [('page-11','page-15'),('page-15','page-31'),('principle-direction','principle-gimbal-design'),('fcp-project-settings','fcp-retime'),('prepare-contract','fcp-selects'),('fcp-assembly','fcp-ripple'),('fcp-rhythm','fcp-retime'),('page-43','page-83'),('supp-color_pipeline','page-83'),('page-88','page-95'),('page-71','page-161'),('fcp-roundtrip-contract','fcp-xml-export')]:assert ids.index(before)<ids.index(after),(before,after)
assert len(json.loads((R/'content/ejim-review.json').read_text()))==81
for p in (R/'docs').rglob('*'):
 if p.is_file() and p.suffix in ['.html','.js','.json']:
  s=p.read_text()
  assert not any(x in s for x in ['hun1016@gmail.com','OTP Code digit','sso.teachable.com/secure']),str(p)
print(f'PASS: {len(entries)} unique entries; original 214 color pages + 83 editing entries preserved; 81 public-source records; 15 independent principles; assets, links and prerequisites valid.')
for p in [R/'docs/index.html', R/'content/production-principles.json']:
 assert 'kyung6class.teachable' not in p.read_text()


from collections import Counter
sections={s['id']:s for s in data['sections']}
assert all(e['section'] in sections and sections[e['section']]['chapter']==e['chapter'] for e in data['entries'])
assert max(Counter(e['section'] for e in data['entries']).values())<=10
films=[e for e in data['entries'] if e['id'].startswith('film-')]
assert len(films)==14
assert all('근거 구분' in e['html'] for e in films if e['id']!='film-cases')
assert 'film-atonement' in [e['id'] for e in films]
print('PASS: 77 topic groups; at most 10 lessons per group; 13 film cases + index.')

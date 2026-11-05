"""Merge the two existing web guides without dropping their content or assets."""
import json,re,shutil,html as esc
from pathlib import Path
from lxml import html
ROOT=Path(__file__).resolve().parents[1]; DOCS=ROOT/'docs'; FCP=ROOT.parent/'final-cut-pro-guide'/'docs'
source=ROOT/'content/color-original.html'
if not source.exists():source.write_text((DOCS/'index.html').read_text())
base=source.read_text(); book=json.loads(re.search(r'<script[^>]*id="bookData"[^>]*>(.*?)</script>',base,re.S)[1])
fcp_source=ROOT/'content/fcp-original.html'
if FCP.exists():fcp_source.write_text((FCP/'index.html').read_text())
fcp=html.fromstring(fcp_source.read_text()); meta=json.loads(fcp.get_element_by_id('bookMeta').text)
if FCP.exists():
 for p in (FCP/'assets').iterdir():
  if p.is_dir():shutil.copytree(p,DOCS/'assets'/'editing'/p.name,dirs_exist_ok=True)
 shutil.copyfile(FCP/'assets/figures.js',DOCS/'assets/editing-figures.js')
CHAPTERS=[('start','학습 지도와 확인 기준','큰 흐름과 자료를 읽는 기준'),('see','빛·눈·명암·색의 관계','명암 → 색의 속성 → 대비 → 배색'),('shoot','촬영 구성과 기록·라이팅','구도·방향·장면 → 노출·셔터 → 빛·짐벌'),('prepare','소재·프로젝트 준비','파일 위치·백업 → 프로젝트·색공간·프록시'),('edit','샷을 장면으로 조립하기','선별 → 기본 컷·트림 → 장면 → 전체 구조'),('sound','음악·사운드·시간','음악 구조 → 역할·레벨 → 속도 변화'),('grade','색관리에서 샷 매칭까지','입력·보기 → 관리 → 스코프 → 보정·선택·매칭'),('look','룩·합성·전환·사례','배색·질감 → 효과 → 컷 연결 → 작품 사례'),('finish','왕복·출력·수정·보관','전달 계약 → XML·반환 → 수정 → 검수'),('reference','사전·출처·강의 검토 기록','필요한 순간 찾아보는 항목과 근거')]
entries=[]
def add(id,title,chapter,body='',text='',kind='html',**extra):
 entries.append(dict(id=id,title=title,chapter=chapter,html=body,text=text or re.sub('<[^>]+>',' ',body),kind=kind,**extra))
# Prerequisites are explicit, not inferred from keyword sorting.
foundation=[8,9,10,11,12,13,14,15,16,18,19,20,23,24,17,21,22,27,25,26,28,29,30,31,32,33,34,35,36,37]
prepare_color={38,82,134,154,158,160}
finish_color={76,107,121,156}
reference_color=set(range(122,133))|{105,106}
creative_color={72,73,99,100,101,102,103,104,120}|set(range(161,215))
color_groups={p['n']:'see' if p['n'] in foundation else ('start' if p['n']==2 else 'reference') if p['n']<=7 else 'prepare' if p['n'] in prepare_color else 'finish' if p['n'] in finish_color else 'reference' if p['n'] in reference_color else 'look' if p['n'] in creative_color else 'grade' for p in book['pages']}
# Color management and monitoring come before changing pixel values and using masks.
grade_first=[39,40,41,42,43,157,44,133,135,136,45,81,109,83,110,84,111,112,85,88,148,89,137,138,90,91,86,87,139,140,141,46,47,113,48]
grade_rest=[p['n'] for p in book['pages'] if color_groups[p['n']]=='grade' and p['n'] not in grade_first]
color_order=list(range(1,8))+foundation+[n for n in sorted(prepare_color)]+grade_first+grade_rest+sorted(creative_color)+sorted(finish_color)+sorted(reference_color)
assert len(set(color_order))==214,(len(color_order),set(range(1,215))-set(color_order))
for n in color_order:
 p=book['pages'][n-1];add('page-'+str(n),p['title'],color_groups[n],text=p['text'],kind='color',page=n)

supp=json.loads((ROOT/'content/supplements.json').read_text())
for s in supp:
 group={'촬영':'shoot','라이팅':'shoot','색채 관찰':'see','색보정':'grade','편집 연결':'finish','사운드':'sound','전달·출력':'finish'}[s['chapter']]
 body='<p class="lead">'+esc.escape(s['subtitle'])+'</p>'
 for title,text in s['blocks']:body+='<h3>'+esc.escape(title)+'</h3><p>'+esc.escape(text)+'</p>'
 body+='<div class="source"><strong>참고한 설명과 확인 범위</strong><p>제공 자막·설명에 근거한 교육 정리. 원본 시연 프레임·오디오의 전수 검토와 구분합니다.</p><ul>'
 for label,url in s['sources']:body+='<li><a target="_blank" rel="noopener" href="'+esc.escape(url,quote=True)+'">'+esc.escape(label)+'</a></li>'
 body+='</ul></div>';add('supp-'+s['id'],s['title'],group,body)

fcp_ids={x['id'] for x in meta['chapters']}|{'problems','labs','glossary','matrix','checklist','sources'}
prep={'reading','versions','library','ingest','shared-media','project-settings','proxy','storage','backup'}
sound={'beat-detection','markers','audio-roles','audio-edit','audio-mix','muffled','speed','retime','optical-flow'}
finish={'delivery','live-truth','workflow-choice','roundtrip-contract','preflight','xml-export','conform','risk-effects','handles','grade-resolve','return-render','return-finalize','revision','color-difference','mixed-machines','final-exercise'}
def edit_body(node):
 node=html.fromstring(html.tostring(node,encoding='unicode'))
 node.attrib.pop('class',None)
 if node.tag=='article':
  for h in node.xpath('./h2')[:1]:node.remove(h)
  for e in node.xpath('.//div[@class="entry-top"]/span'):e.text='Final Cut Pro · 원리와 조작'
 for e in node.xpath('.//*[@src]'):
  if e.get('src','').startswith('assets/'):e.set('src',e.get('src').replace('assets/','assets/editing/',1))
 for e in node.xpath('.//*[@href]'):
  href=e.get('href','')
  if href.startswith('#') and href[1:] in fcp_ids:e.set('href','#fcp-'+href[1:])
 for e in node.xpath('.//*[@data-read]'):e.set('data-read','fcp-'+e.get('data-read'))
 return ''.join(html.tostring(x,encoding='unicode') for x in node)
for c in meta['chapters']:
 id=c['id'];group='prepare' if id in prep or (c['part']==0 and id not in {'selects'}) else 'sound' if id in sound or c['part']==2 else 'finish' if id in finish or c['part']==7 else 'grade' if id in {'color-management','grade-fcp','match-color'} else 'look' if c['part'] in [3,4,6] else 'edit'
 node=fcp.get_element_by_id(id);add('fcp-'+id,c['title'],group,edit_body(node),text=node.text_content(),original='Final Cut Pro 웹 교재',sourceId=id)
for id,title in [('problems','편집 문제별 색인'),('labs','편집 조작 실험실'),('glossary','FCP 용어·단축키 사전'),('matrix','왕복 전달 표'),('checklist','왕복 체크리스트'),('sources','FCP 자료의 기준과 출처')]:
 node=fcp.get_element_by_id(id);add('fcp-'+id,title,'reference',edit_body(node))

# New integration pages are written independently; private course media is never copied here.
kyung_path=ROOT/'content/production-principles.json'
if kyung_path.exists():
 for r in json.loads(kyung_path.read_text()):add(**r)

ejim=json.loads((ROOT/'content/ejim-review.json').read_text());body='<p class="lead">4개 과정 82항목에서 중복을 제외한 81편. 원본 자막의 주요 논점을 검토한 기록입니다.</p><p>전체 연속 시청·시연 프레임·오디오 청취를 완료한 기록이 아닙니다. 제품 리뷰는 구매 추천으로 옮기지 않고, OS·버전·입력 조건을 확인하도록 정리했습니다.</p><div class="review-grid">'
for i,v in enumerate(ejim):body+='<article><small>'+str(i+1).zfill(2)+' · 자막 주요 구간</small><h3><a href="'+esc.escape(v['url'],quote=True)+'" target="_blank" rel="noopener">'+esc.escape(v['title'])+'</a></h3><p>'+esc.escape(v['note'])+'</p></article>'
body+='</div>';add('ejim-sources','Ejim 81편 · 검토 기록','reference',body)

add('prepare-contract','편집 전에 정할 입력·작업·출력의 약속','prepare','<p class="lead">편집을 시작하기 전에 프레임레이트·색 해석·미디어 위치를 고정합니다.</p><h3>편집 전에 필요한 결정</h3><p>원본의 촬영 FPS와 기록 감마·색역을 확인하고, 프로젝트의 시간 기준과 SDR/HDR 작업 목적을 정합니다. 60p 소재를 24p 타임라인에 놓는 것과 40% 슬로모션으로 해석하는 것은 다릅니다. 혼합 카메라를 모두 같은 로그로 해석하지 않습니다.</p><h3>이후 배울 내용과의 연결</h3><p>상세한 RCM·CST·Camera LUT 조작은 색보정 단원에서 다룹니다. 여기서는 어떤 입력이 들어오고 어떤 출력을 만들 것인지 정해 중간 과정의 이중 변환과 FPS 혼동을 예방합니다.</p><p><a href="#page-82">LOG·RAW·색공간</a> · <a href="#fcp-project-settings">프로젝트 설정</a> · <a href="#supp-color_pipeline">색관리의 책임</a></p>')
add('curriculum-order','전체 학습 순서를 이렇게 바꿨어요','start','<p class="lead">도구 이름의 순서가 아니라, 다음 판단에 필요한 개념이 먼저 등장하도록 재배치했습니다.</p><table><thead><tr><th>먼저 이해할 것</th><th>그다음 볼 것</th><th>순서를 정한 이유</th></tr></thead><tbody><tr><td>빛·눈·큰 명암과 중간톤</td><td>색의 속성·색온도·대비·배색</td><td>같은 색이라도 다르게 보이는 조건을 먼저 읽기</td></tr><tr><td>샷 크기·구도·화면 방향</td><td>짐벌 경로·속도·표현</td><td>움직이는 동안 유지할 화면과 드러낼 정보를 정하기</td></tr><tr><td>기록 형식·프로젝트 FPS·미디어 위치</td><td>컷 선별·장면 조립</td><td>중간에 기준을 바꿔 재작업하는 일을 줄이기</td></tr><tr><td>기본 컷·트림·음악 구조</td><td>속도 램프·고급 전환</td><td>효과보다 먼저 장면의 시간과 정보량을 판단하기</td></tr><tr><td>보기 환경·입력·작업·출력</td><td>노드·스코프·기본 보정</td><td>틀린 변환을 창작 보정으로 덮지 않기</td></tr><tr><td>기본 보정·선택·샷 매칭</td><td>필름 질감·할레이션·공통 룩</td><td>샷의 문제와 스타일 선택을 분리하기</td></tr><tr><td>룩과 편집의 책임</td><td>XML·반환·수정·최종 검수</td><td>속도·마스크·음악·색을 어느 앱에서 끝낼지 먼저 정하기</td></tr></tbody></table><h3>이미 아는 부분은 찾아서 읽기</h3><p>기존 색채 214쪽, 편집 83항목, 사진과 전후 비교는 보존했습니다. 원본 책의 쪽번호는 참조용으로 유지하고 왼쪽 통합 목차와 각 항목의 다음 링크는 새 학습 순서를 따릅니다. 예전 세부 목차와 사전은 마지막 단원에서 다시 찾을 수 있습니다.</p>')
# Place supplemental reasoning next to the concepts it qualifies.
placements={'supp-read_brightness':'page-11','supp-read_edges':'page-13','supp-read_palette':'page-33','supp-read_time':'page-37','supp-color_pipeline':'page-44','supp-color_drt':'page-136','supp-color_lut':'page-84','supp-color_sat':'page-68','supp-color_nr':'page-152','supp-color_group':'page-149','supp-color_reuse':'page-150','supp-color_precision':'page-38','supp-color_detail':'page-153'}
for sid,target in placements.items():
 x=next(v for v in entries if v['id']==sid);entries.remove(x);pos=next(i for i,v in enumerate(entries) if v['id']==target);entries.insert(pos+1,x)
# Native supplementary color precision belongs with recording, not a late grading dictionary.
for x in entries:
 if x['id']=='supp-color_precision':x['chapter']='prepare'
# Semantic progression within preparation / editing / finishing remains stable, independent of the old part numbers.
priorities={'shoot':['principle-shot-scene','principle-direction','principle-depth','principle-coverage','supp-shoot_iso','supp-shoot_ei','supp-shoot_exposure','supp-shoot_shutter','supp-shoot_format','supp-shoot_lens','supp-light_quality','supp-light_book','supp-light_motive','supp-light_wb','supp-light_catch','supp-light_flicker','principle-gimbal-design','principle-gimbal-route','principle-focus'], 'sound':['fcp-rhythm','fcp-music-edit','fcp-beat-detection','fcp-roles','supp-sound_roles','supp-sound_format','supp-sound_levels','supp-sound_dynamics','fcp-mix','fcp-sound-design','fcp-muffled','supp-sound_float','principle-retime','fcp-retime'], 'edit':['fcp-selects','fcp-magnetic','fcp-secondary','fcp-assembly','fcp-ripple','fcp-roll','fcp-slip','fcp-slide','fcp-precision','fcp-split-edit','fcp-story-shots','principle-workflow','principle-flow','fcp-alternatives','fcp-multicam'], 'start':['curriculum-order','page-2'], 'prepare':['fcp-reading','fcp-versions','fcp-library','prepare-contract','principle-files','fcp-ingest','fcp-shared-media','fcp-project-settings','page-82','page-134','page-38','supp-color_precision','principle-media','fcp-proxy','page-158','page-160'], 'grade':['page-39','page-40','page-41','page-42','page-43','page-157','page-44','supp-color_pipeline','page-133','page-135','page-136','supp-color_drt','page-45','page-81','page-109','page-83','page-110','page-84','supp-color_lut','page-111','page-112','page-85','page-88','page-148','page-89','page-137','page-138','principle-color'], 'finish':['supp-edit_bridge','supp-edit_handoff','fcp-live-truth','fcp-workflow-choice','fcp-roundtrip-contract','fcp-preflight','fcp-xml-export','fcp-conform','fcp-risk-effects','fcp-handles','fcp-grade-resolve','fcp-return-render','fcp-return-finalize','fcp-revision','fcp-color-difference','fcp-mixed-machines','fcp-delivery']}
ordered=[]
for key,_,_ in CHAPTERS:
 group=[e for e in entries if e['chapter']==key]; ids=priorities.get(key,[])
 order={v:i for i,v in enumerate(ids)};group.sort(key=lambda x:order.get(x['id'],len(ids)))
 ordered.extend(group)
entries=ordered
assert len({e['id'] for e in entries})==len(entries)
for i,e in enumerate(entries):e['order']=i+1
payload={'chapters':[dict(id=k,title=t,description=d) for k,t,d in CHAPTERS],'entries':entries,'updated':'2026.11.05'}
# Keep original comparison UI, data and images, adding one unified reader and navigation.
root=html.fromstring(base);root.find('head').find('title').text='영상제작 통합 학습서 · 촬영·편집·색보정'
head=root.find('head');link=html.Element('link',rel='stylesheet',href='assets/unified.css');head.append(link)
brand=root.xpath('//*[@class="brand"]')[0];brand.text='영상제작 통합 학습서';[brand.remove(c) for c in list(brand)]
root.xpath('//*[@class="eyebrow"]')[0].text='SEE / SHOOT / EDIT / GRADE / FINISH'
root.xpath('//*[@id="sidebar"]/p')[0].text='촬영·편집·색보정을 한 흐름으로. 전체 목차와 본문을 함께 검색합니다.'
intro=root.xpath('//*[@id="sidebar"]/p')[0]
for child in list(intro):intro.remove(child)
search=root.get_element_by_id('search');search.set('placeholder','예: 빛, 샷, 음악, 노드, XML')
bar=root.xpath('//*[@class="toolbar"]')[0];btn=html.Element('button',id='learnTab',attrib={'class':'tab'});btn.text='학습 지도';bar.insert(1,btn)
main=root.xpath('//*[@class="main"]')[0];pane=html.Element('section',id='lessonPane',attrib={'class':'lesson-pane hidden'});main.append(pane)
home=html.Element('section',id='learnPane',attrib={'class':'learn-pane hidden'});main.append(home)
body=root.find('body')
for script in list(body.xpath('.//script[@src="assets/app.js"]')):script.getparent().remove(script)
data=html.Element('script',id='unifiedData',type='application/json');data.text=json.dumps(payload,ensure_ascii=False).replace('</','<\\/');body.append(data)
for src in ['assets/editing-figures.js','assets/app.js']:body.append(html.Element('script',src=src))
(DOCS/'assets/app.js').write_text((ROOT/'content/color-app-original.js').read_text()+'\n'+(DOCS/'assets/unified.js').read_text())
for e in root.xpath('//*[contains(text(),"페이지 배치는 PDF와 같습니다.")]'):e.text='색채 원본의 쪽번호는 참조용입니다. 통합 목차와 이전·다음 이동은 새 학습 순서를 따릅니다.'
(DOCS/'index.html').write_text('<!doctype html>\n'+html.tostring(root,encoding='unicode'))
(ROOT/'content/unified-outline.json').write_text(json.dumps([dict(id=e['id'],title=e['title'],chapter=e['chapter']) for e in entries],ensure_ascii=False,indent=2))
print(json.dumps({'entries':len(entries),'color':sum(e['kind']=='color' for e in entries),'fcp':len(meta['chapters']),'supplements':len(supp)},ensure_ascii=False))

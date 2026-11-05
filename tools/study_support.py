"""Contextual comparisons, curated exercises and evidence-based coverage inventory."""
import json,re
from pathlib import Path
from lxml import html
R=Path(__file__).resolve().parents[1]

def augment(entries,sections,book,base):
 exercises=json.loads((R/'content/study-exercises.json').read_text());ids={e['id'] for e in entries}
 for e in exercises:
  assert len(e['steps'])==4 and len(e['criteria'])==3,e['id']
  assert set(e['targets'])<=ids,(e['id'],set(e['targets'])-ids)
 root=html.fromstring(base);comparisons=[]
 for node in root.xpath('//*[contains(concat(" ",normalize-space(@class)," ")," comparison-card ")]'):
  stage=node.xpath('.//*[@data-before]')[0]
  comparisons.append(dict(id=node.get('id'),page=int(node.get('data-page')),title=node.get('data-title'),before=stage.get('data-before'),variants=json.loads(stage.get('data-variants')),caption=' '.join(node.xpath('.//*[contains(concat(" ",normalize-space(@class)," ")," caption ")]/text()'))))
 cmp_ids={c['id'] for c in comparisons}
 for e in exercises:assert set(e['comparisons'])<=cmp_ids,e['id']
 audit=[]
 for e in entries:
  targets=[x['id'] for x in exercises if e['id'] in x['targets']]
  pairs=[c['id'] for c in comparisons if c['page']==e.get('page')]
  if not pairs and e['kind']!='color':pairs=list(dict.fromkeys(c for x in exercises if x['id'] in targets for c in x['comparisons']))[:2]
  audit.append(dict(id=e['id'],title=e['title'],chapter=e['chapter'],pageImage=e['kind']=='color',embeddedImage='<img' in e['html'],existingDiagram='data-figure' in e['html'],comparisonIds=pairs,exerciseIds=targets))
  if targets:e['text']+=' 실습 '+' '.join(x['title'] for x in exercises if x['id'] in targets)
 titles={'color':'색채학','shoot':'촬영','fcp':'파이널컷(컷편집)','resolve':'다빈치리졸브(색보정)','other':'기타'}
 for ch,title in titles.items():
  sec={'id':'study-section-'+ch,'chapter':ch,'category':'실습과 복습','title':title+' 실습실'};sections.append(sec)
  selected=[e for e in exercises if e['chapter']==ch]
  body='<p>설명 → 변화 예상 → 비교 → 직접 해보기 → 결과 판단을 연결하는 실습실입니다.</p><ul>'+''.join('<li>'+e['title']+' · 약 '+str(e['minutes'])+'분</li>' for e in selected)+'</ul>'
  entries.append(dict(id='study-'+ch,title=title+' 실습실 · '+str(len(selected))+'개 실습',chapter=ch,section=sec['id'],html=body,text='실습 완료 기준 힌트 '+' '.join(e['title']+' '+e['answer'] for e in selected),kind='html'))
 sec={'id':'study-guide-section','chapter':'other','category':'학습 안내','title':'공부하는 방법'};sections.append(sec)
 entries.append(dict(id='study-guide',title='공부하는 방법 · 실습·비교 길잡이',chapter='other',section=sec['id'],html='<p>읽기·전후 비교·실습·복습을 연결하는 안내입니다.</p>',text='실습 비교 Before After 학습 가이드 노트 완료 기준',kind='html'))
 entries=[e for ch in titles for e in entries if e['chapter']==ch]
 for i,e in enumerate(entries):e['order']=i+1
 summary=[]
 for ch in titles:
  rows=[a for a in audit if a['chapter']==ch]
  summary.append(dict(chapter=ch,reviewedEntries=len(rows),originalPageImages=sum(a['pageImage'] for a in rows),originalEmbeddedImageEntries=sum(a['embeddedImage'] for a in rows),originalDiagramEntries=sum(a['existingDiagram'] for a in rows),contextualComparisonEntries=sum(bool(a['comparisonIds']) for a in rows),curatedPracticeEntries=sum(bool(a['exerciseIds']) for a in rows),newExercises=sum(e['chapter']==ch for e in exercises)))
 report=dict(reviewedOriginalEntries=len(audit),method='원본 368항목의 구조적 보조 자료를 전수 집계하고, 주제별 실습 연결은 직접 선정함. 이미지 수가 곧 학습 품질 점수는 아님.',findings=['기존 비교 62개가 별도 탭에 집중되어 있어 해당 본문에 연결','촬영 보강편은 글 중심이어서 원리 도식과 촬영 실습 추가','기존 FCP 조작 도식과 실제 앱 자료를 유지하고 재료·절차·검수 기준 연결','색관리·마스크·매칭·질감은 한 변수씩 바꾸는 실습과 실패 진단 추가','정답·힌트는 펼쳐 보는 방식, 완료 기준과 메모는 이 브라우저에 저장'],summary=summary,entries=audit)
 (R/'content/study-audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
 return entries,sections,dict(exercises=exercises,comparisons=comparisons,titles={e['id']:e['title'] for e in entries},coverage=summary)

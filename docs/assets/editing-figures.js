/* Original educational diagrams. They are not Final Cut Pro screenshots or output. */
window.GuideFigures=(()=>{
const C={a:'#087f78',b:'#e9b058',c:'#64869c',light:'#e3eeef',ink:'#142b37',pink:'#c4768b'};
const esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const text=(x,y,s,size=15,fill=C.ink)=>`<text x="${x}" y="${y}" font-size="${size}" style="fill:${fill}">${esc(s)}</text>`;
const rect=(x,y,w,h,col=C.light,r=8)=>`<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${r}" fill="${col}"/>`;
const line=(x,y,xx,yy,col=C.c,dash='')=>`<line x1="${x}" y1="${y}" x2="${xx}" y2="${yy}" stroke="${col}" stroke-width="2" ${dash?'stroke-dasharray="'+dash+'"':''}/>`;
const arrow=(x,y,xx,yy)=>line(x,y,xx,yy,C.a)+`<circle cx="${xx}" cy="${yy}" r="4" fill="${C.a}"/>`;
const svg=(s,h=230)=>`<svg viewBox="0 0 800 ${h}" role="img" aria-label="편집 원리 설명 도식">${s}</svg>`;
const box=(x,y,w,title,sub,col=C.light)=>rect(x,y,w,68,col)+text(x+12,y+27,title,16)+text(x+12,y+51,sub,12);
function sequence(labels,subs){let s='';const n=labels.length,w=(740-(n-1)*20)/n;for(let i=0;i<n;i++){let x=30+i*(w+20);s+=box(x,65,w,labels[i],subs[i]);if(i<n-1)s+=arrow(x+w+3,98,x+w+17,98);}return svg(s+text(30,180,'흐름과 책임을 먼저 정한 뒤 도구를 선택합니다.',13));}
const statics={
 story:()=>{let s=text(30,28,'한 공간을 이해하는 정보의 순서',17);const labels=['장소','행동','디테일','반응'],sub=['와이드','미디엄','클로즈업','인물·여운'];for(let i=0;i<4;i++){let x=30+i*192;s+=rect(x,50,170,100,i%2?C.light:'#d2e9e3');if(i===0)s+=line(x+12,115,x+158,115)+`<path d="M${x+20} 105l25-22 25 22 35-34 40 34" fill="none" stroke="${C.c}" stroke-width="3"/>`;else if(i===2)s+=`<circle cx="${x+85}" cy="92" r="31" fill="${C.b}"/>`;else s+=`<circle cx="${x+85}" cy="78" r="15" fill="${C.pink}"/>`+rect(x+57,97,56,35,C.c);s+=text(x,178,labels[i],16)+text(x,200,sub[i],12);}return svg(s);},
 versions:()=>sequence(['11.0 / 11.1','12.0','12.3','12.4'],['마스크·조정 클립','검색·박자 분석','Auto Mask·컷 검출','Cinematic·수정 사항']),
 library:()=>svg(box(30,80,160,'Library','관리 단위')+box(255,25,190,'Event · Source','소재·분류')+box(255,130,190,'Event · Edit','프로젝트·편집안')+box(510,25,235,'Clips / Ranges','원본과 선택 구간')+box(510,130,235,'Project · 60초','타임라인')+arrow(190,110,255,60)+arrow(190,110,255,165)+arrow(445,60,510,60)+arrow(445,165,510,165)),
 media:()=>sequence(['원본','Proxy / Optimized','편집 정보','반환·출력'],['카메라별 보관','작업 미디어','FCPXML · 원본 참조','graded_v002 · 마스터']),
 fps:()=>svg(text(30,30,'프레임은 시간의 격자다',18)+Array.from({length:24},(_,i)=>rect(30+i*30,65,24,40,i%2?C.a:C.c)).join('')+text(30,135,'24fps · 1초 = 24프레임',19)+text(30,175,'23.976 / 24 / 29.97 / 30은 정확히 같은 시간 기준이 아닙니다.',14)),
 selects:()=>svg(text(30,30,'원본 30초 중 의미 있는 범위만 후보로 남긴다',17)+rect(30,65,740,55,C.light)+rect(105,65,80,55,C.a)+rect(350,65,110,55,C.b)+rect(640,65,60,55,C.c)+text(105,150,'문 열기 · 2초',14)+text(350,150,'커피 붓기 · 3초',14)+text(590,190,'키워드: CAFE + DETAIL',13)),
 magnetic:()=>{let s=text(30,28,'시간 기준 + 연결점',18)+rect(70,110,220,55,C.a)+rect(290,110,220,55,C.b)+rect(510,110,220,55,C.c)+text(82,142,'장면 A',16,'white')+text(302,142,'장면 B',16)+text(522,142,'장면 C',16,'white');s+=rect(325,48,135,35,'#d9e8f0')+text(338,73,'B의 타이틀',13)+line(360,83,360,110)+rect(330,190,165,26,'#d6ece5')+text(340,208,'B의 현장음',12)+line(350,165,350,190)+text(65,240,'B를 옮길 때 연결된 타이틀·소리도 함께 움직일 수 있습니다.',13);return svg(s,260);},
 continuity:()=>svg(text(30,28,'동작 단계와 방향을 비교한다',17)+rect(30,55,350,105)+rect(420,55,350,105)+arrow(90,110,220,110)+arrow(480,110,610,110)+text(45,190,'A 끝: 컵을 내려놓는 순간',15)+text(435,190,'B 시작: 내려놓은 컵의 디테일',15)+text(30,225,'손이 다시 올라가면 동작이 되감긴 것처럼 느껴질 수 있다.',13),250),
 sync:()=>svg(text(30,30,'앞·중간·끝에서 동기화를 확인한다',17)+['소니 영상','액션캠','외부 소리'].map((v,i)=>text(20,78+i*55,v,13)+rect(125,50+i*55,625,35,i===0?C.a:i===1?C.b:C.c)).join('')+[220,430,650].map(x=>line(x,42,x,202,C.pink,'5 4')).join('')+text(180,225,'시작',12)+text(410,225,'중간',12)+text(640,225,'끝',12),250),
 audio:()=>svg(text(30,28,'큰 파형이 항상 좋은 소리인 것은 아니다',17)+`<path d="M30 100 ${Array.from({length:100},(_,i)=>'L'+(30+i*7.4).toFixed(1)+' '+(100+Math.sin(i*1.1)*Math.sin(i*.24)*36).toFixed(1)).join(' ')}" fill="none" stroke="${C.a}" stroke-width="3"/>`+line(30,58,770,58,C.pink,'6 4')+text(30,173,'피크 · 순간 최대치',15)+text(300,173,'명료도 · 말이 읽히는가',15)+text(550,173,'거리감 · 화면과 맞는가',15)+text(30,210,'대사 → 음악 → 공간·동작음 순서로 밸런스를 판단합니다.',13)),
 roles:()=>svg(text(30,28,'의미별 역할과 실제 녹음 채널은 다르다',17)+['Dialogue · 대사','Music · 음악','Effects · 효과음'].map((v,i)=>box(30+i*252,60,225,v,i===0?'VO / Interview':i===1?'Main / Filtered':'Water / Foley')).join('')+text(30,180,'컴포넌트: 같은 파일 안의 카메라 마이크 / 라발리에 채널 등',14)),
 crop:()=>svg(text(30,28,'같은 가로 영상의 Fit과 Fill',17)+rect(30,55,335,125,C.light)+rect(395,55,335,125,C.light)+rect(140,55,115,125,'#bfded5')+rect(500,55,115,125,'#bfded5')+rect(144,87,107,60,C.c)+rect(505,55,105,125,C.a)+text(30,215,'Fit: 전체 구도, 빈 공간 가능',15)+text(395,215,'Fill: 화면 채움, 원본 일부 잘림',15),245),
 keyframes:()=>svg(text(30,28,'같은 시작·끝, 다른 가속·감속',17)+line(80,190,750,190)+line(80,190,80,50)+`<path d="M80 190L730 55" stroke="${C.c}" fill="none" stroke-width="3"/><path d="M80 190C410 190 400 55 730 55" stroke="${C.a}" fill="none" stroke-width="4"/>`+text(110,65,'부드러운 변화',14)+text(370,140,'Linear · 일정 변화',14)+text(600,225,'시간 →',13),250),
 mask:()=>svg(text(30,28,'검정 = 제외 · 흰색 = 선택 · 회색 = 점진적 경계',17)+rect(50,55,300,130,C.c)+rect(430,55,300,130,'#172e3b')+`<circle cx="200" cy="98" r="26" fill="${C.pink}"/><path d="M150 185V148Q200 115 250 148V185" fill="${C.b}"/><circle cx="580" cy="98" r="26" fill="white"/><path d="M530 185V148Q580 115 630 148V185" fill="white"/>`+text(50,215,'촬영 장면을 단순화한 그림',13)+text(430,215,'마스크 지도 · 실제 앱 출력 아님',13),245),
 ghost:()=>svg(text(30,28,'현재 배경 위에 과거 인물만 올린다',17)+rect(30,50,740,145,C.light)+line(30,160,770,160)+[190,375,575].map((x,i)=>`<g opacity="${i===2?1:.4}"><circle cx="${x}" cy="91" r="20" fill="${C.pink}"/>${rect(x-22,115,44,60,C.a)}</g>`).join('')+text(120,220,'과거 t−2',14)+text(310,220,'과거 t−1',14)+text(520,220,'현재 t',14),250),
 layers:()=>svg(text(30,28,'적용 순서는 결과를 바꾼다',17)+box(30,55,210,'원본 · 개별 교정','클립별 차이 정리')+box(295,55,210,'공통 룩 / 효과','Adjustment 또는 Resolve')+box(560,55,210,'타이틀 · 최종 합성','구워진 항목 중복 금지')+arrow(240,88,295,88)+arrow(505,88,560,88)+text(30,185,'마스크 = 범위 / 키프레임 = 시간 / 효과 순서 = 계산 순서',14)),
 color:()=>sequence(['실제 입력','작업 공간','교정 · 룩','반환 출력'],['LOG / HDR / SDR','RCM 또는 CST 설계','노출 → 컷 맞추기','Rec.709 등 목적 지정']),
 detection:()=>svg(text(30,28,'컷 검출은 편집 프로젝트 복원이 아니다',17)+rect(30,65,740,55,C.light)+[180,330,510,640].map(x=>line(x,45,x,137,C.pink,'5 4')).join('')+text(30,180,'남는 것: 구워진 픽셀·타이틀·효과',15)+text(30,214,'돌아오지 않는 것: 원본 handles·레이어 구조·효과 파라미터',14),245),
 delivery:()=>sequence(['원본 연결','기술 설정','시험 출력','완성 파일 검수'],['Proxy 전환 확인','FPS·색·오디오','10초 어려운 장면','다시 불러 비교']),
 roundtrip:()=>svg(text(30,28,'두 개의 기준과 두 개의 전달물',18)+box(30,70,225,'Final Cut Pro','컷 · 소리 · 자막')+box(540,70,230,'DaVinci Resolve','입력 · 교정 · 룩')+arrow(255,83,535,83)+text(320,63,'원본 참조 + 새 XML',14)+arrow(540,125,260,125)+text(315,160,'색 적용 미디어 + 반환 XML',14)+text(30,215,'노드 슬라이더와 컷 타임라인은 기본 기능으로 실시간 동기화되지 않습니다.',13),245),
 xml:()=>sequence(['FCP Project','FCPXML','Resolve Timeline'],['구조·미디어 참조','지원 형식·버전 선택','원본 연결 후 검수']),
 conform:()=>svg(text(30,28,'참조 영상과 원본 연결 결과를 대조한다',17)+box(30,70,320,'Reference','정답 편집 · 구워진 화면')+box(430,70,340,'Conformed Timeline','컷 수 · 시작점 · 속도 · 구도')+text(30,190,'총길이 일치 ≠ 모든 컷 일치',18)+text(430,190,'앞뒤 프레임·전환까지 확인',15)),
 revision:()=>sequence(['변경 목록','색 변경','편집 변경','최종 검수'],['Shot ID·버전','새 컷 렌더·교체','새 XML·재conform','앞뒤 컷·음악 확인'])
};
// Transition plates: original examples, not frames from a creator's film.
statics.transition=()=>sequence(['장면 A','연결 조건','장면 B'],['왜 떠나는가','방향 · 시선 · 소리','어디에 도착하는가']);
statics['mask-wipe']=()=>{let s=text(30,25,'전경 경계가 지나가며 A → B가 드러납니다',17);for(let i=0;i<3;i++){let x=30+i*255,w=230,edge=[15,110,220][i];s+=rect(x,65,w,110,C.b)+rect(x+edge,65,w-edge,110,C.a)+rect(x+edge-9,60,18,120,C.ink)+text(x+8,92,'B',14)+text(x+w-24,92,'A',14,'white')+text(x,210,['① B 진입 시작','② 경계 뒤로 B 공개','③ A를 화면 밖으로 종료'][i],13);}return svg(s,245)};
statics.match=()=>{let s=text(30,25,'주된 모양과 시선 위치를 같은 곳에 둡니다',17);for(let i=0;i<2;i++){let x=45+i*390;s+=rect(x,55,320,130,i?C.light:'#f2e8d4')+`<circle cx="${x+160}" cy="120" r="42" fill="${i?C.c:C.a}"/>`+line(x+160,65,x+160,176,C.ink,'4 4')+text(x+80,213,i?'B · 원형 수영장':'A · 커피 컵',14);}return svg(s,245)};
statics.motion=()=>{let s=text(30,25,'방향 · 중심 · 가속 / 감속을 연결합니다',17);s+=box(30,65,220,'A · 관심 지점','정상 → 이동 가속')+box(290,65,220,'컷 경계','최대 흐림 / 공통 중심')+box(550,65,220,'B · 도착 지점','이동 감속 → 정상');s+=arrow(250,99,285,99)+arrow(515,99,546,99)+text(30,190,'정상 화면을 앞뒤에 남겨 장소와 피사체를 읽게 합니다.',14);return svg(s,245)};
statics.intro=()=>{let s=text(30,25,'210초 한 곡 본편 · 독자적인 연습 지도',17),lengths=[18,40,40,32,54,26],labels=['도입','소개','상승','호흡','재상승','귀결'],x=30;lengths.forEach((d,i)=>{let w=d*(740/210);s+=rect(x,70,w-3,62,[C.a,C.c,C.a,C.b,C.c,C.light][i])+text(x+6,96,labels[i],13,i===0||i===1||i===2||i===4?'white':C.ink)+text(x+6,122,d+'초',12,i===0||i===1||i===2||i===4?'white':C.ink);x+=w});s+=text(30,192,'시간은 출발점입니다. 음악 · 행동 · 정보량에 따라 조절합니다.',14);return svg(s,245)};
function mount(container,key){
 const el=container.querySelector('.drawing');if(!el)return;
 if(['trim','beats','speed','filter','handles','jcut'].includes(key))interactive(el,key);else el.innerHTML=(statics[key]||statics.story)();
 container.dataset.mounted='1';
}
function interactive(el,key){
 const num=(name,label,v,min,max,step='1')=>`<label>${label}<br><input data-v="${name}" type="number" value="${v}" min="${min}" max="${max}" step="${step}"></label>`;
 const range=(name,label,min,max,value,step='.1')=>`<label>${label}<input data-v="${name}" type="range" min="${min}" max="${max}" value="${value}" step="${step}"></label>`;
 const select=(name,label,options)=>`<label>${label}<select data-v="${name}">${options.map(([v,t])=>`<option value="${v}">${t}</option>`).join('')}</select></label>`;
 let controls='';
 if(key==='trim')controls=select('mode','트림 방식',[['ripple','Ripple'],['roll','Roll'],['slip','Slip'],['slide','Slide']])+range('d','이동량 −1초 ↔ +1초',-1,1,.5);
 if(key==='beats')controls=num('bpm','BPM · 4/4 고정',120,40,240)+select('level','표시',[['beats','박'],['bars','마디'],['phrase','4마디 구간']]);
 if(key==='speed')controls=num('src','원본 파일 FPS',60,1,240,'0.001')+num('dst','타임라인 FPS',24,1,120,'0.001');
 if(key==='filter')controls=range('log','컷오프 주파수 낮게 ↔ 높게',2.3,4.3,3.2,'.01');
 if(key==='handles')controls=num('fps','FPS · 정상 속도',24,1,120,'.001')+num('frames','한쪽 handles 프레임',24,0,240)+num('length','편집에 사용한 초',3,.1,120,'.1');
 if(key==='jcut')controls=select('type','소리의 흐름',[['j','J-cut · 다음 소리를 먼저'],['l','L-cut · 이전 소리를 남김']])+range('offset','겹치는 시간 · 초',0,1,.5,'.05');
 el.innerHTML=`<div class="canvas"></div><div class="tools">${controls}</div><output class="result" aria-live="polite"></output>`;
 const values=()=>Object.fromEntries([...el.querySelectorAll('[data-v]')].map(e=>[e.dataset.v,e.type==='number'||e.type==='range'?Number(e.value):e.value]));
 function update(){const v=values();let s='',out='';
 if(key==='trim'){
  const d=v.d,mode=v.mode;let len=[3,2,3],start=[0,3,5],total=8,source=10;
  if(mode==='ripple'){len=[3,2+d,3];start=[0,3,5+d];total+=d;}
  if(mode==='roll'){len=[3,2+d,3-d];start=[0,3,5+d];}
  if(mode==='slip')source+=d;
  if(mode==='slide'){len=[3+d,2,3-d];start=[0,3+d,5+d];}
  const row=(y,L,S,color)=>L.map((l,i)=>rect(30+S[i]*75,y,l*75-2,40,color[i])+text(40+S[i]*75,y+26,`${'ABC'[i]} ${l.toFixed(1)}s`,13,i===1?C.ink:'white')).join('');
  s=text(30,25,'변경 전 · 3초 / 2초 / 3초',14)+row(40,[3,2,3],[0,3,5],[C.c,C.b,C.c])+text(30,110,`변경 후 · ${mode.toUpperCase()}`,14)+row(125,len,start,[C.a,C.b,C.c])+line(405,30,405,180,C.pink,'5 5')+text(30,207,`B 원본 구간: ${source.toFixed(1)}~${(source+len[1]).toFixed(1)}초`,14);
  out=`총 길이 ${total.toFixed(1)}초 · B 타임라인 ${start[1].toFixed(1)}~${(start[1]+len[1]).toFixed(1)}초 · ${mode==='slip'?'경계 고정, 원본 내용 변경':mode==='slide'?'B 길이·내용 고정, 자리 이동':mode==='roll'?'B/C 경계 이동, 전체 길이 고정':'B 길이와 뒤쪽 시간 변경'}`;
 }
 if(key==='beats'){
  if(!Number.isFinite(v.bpm)||v.bpm<40||v.bpm>240){out='BPM을 40~240 사이로 입력하세요.';s=text(30,100,out);}
  else{let beat=60/v.bpm;s=text(30,28,'4/4 · 4마디의 상대 위치 (항상 16박)',17)+rect(30,80,740,55,C.light);for(let i=0;i<=16;i++){if(v.level==='phrase'&&i!==0&&i!==16)continue;if(v.level==='bars'&&i%4)continue;let x=30+i*46.25;s+=line(x,65,x,150,i%4===0?C.a:C.c,i%4?'4 5':'')+text(x-5,180,(i*beat).toFixed(1),11);}out=`한 박 ${beat.toFixed(3)}초 · 한 마디 ${(beat*4).toFixed(3)}초 · 4마디 ${(beat*16).toFixed(3)}초. 실제 곡의 템포 변화·분석 결과는 별도 확인.`;}
 }
 if(key==='speed'){
  if(!(v.src>0&&v.dst>0&&v.src<=240&&v.dst<=120)){out='양수인 실제 FPS를 입력하세요.';s=text(30,100,out);}
  else{let percent=v.dst/v.src*100;s=text(30,28,'모든 원본 프레임을 한 번씩 재생할 때',17)+box(30,65,230,`${v.src} fps 원본`,'1초 촬영의 프레임 수')+arrow(265,100,335,100)+box(340,65,200,`${percent.toFixed(2)}%`,'재생 속도')+arrow(545,100,585,100)+box(590,65,180,`${v.dst} fps`,'타임라인');out=`1초 촬영 → ${(v.src/v.dst).toFixed(3)}초 재생 · 속도 = 타임라인 FPS ÷ 원본 파일 FPS × 100. 이미 카메라에서 conform된 슬로 파일은 촬영 FPS와 구분.`;}
 }
 if(key==='filter'){
  const cutoff=Math.pow(10,v.log);s=text(30,25,`단순 1차 low-pass · 컷오프 ${Math.round(cutoff)} Hz`,17)+line(60,55,60,185)+line(60,185,755,185);let path='';for(let i=0;i<=120;i++){let f=20*Math.pow(1000,i/120),db=-10*Math.log10(1+(f/cutoff)**2),x=60+i/120*695,y=55+Math.min(36,-db)/36*130;path+=(i?'L':'M')+x.toFixed(1)+' '+y.toFixed(1);}s+=`<path d="${path}" fill="none" stroke="${C.a}" stroke-width="4"/>`+text(30,60,'0dB',11)+text(18,188,'−36dB',11)+text(60,210,'20Hz',12)+text(700,210,'20kHz',12);out='컷오프를 낮추면 높은 주파수가 더 줄어듭니다. 이 그래프는 설명용 계산이며 FCP EQ 설정·청감의 실제 측정값은 아닙니다.';
 }
 if(key==='handles'){
  if(!(v.fps>0&&v.frames>=0&&v.length>0)){out='FPS·길이는 양수, handles는 0 이상으로 입력하세요.';s=text(30,100,out);}
  else{let h=v.frames/v.fps,total=v.length+2*h,scale=740/total;s=text(30,25,'정상 속도 · 양쪽에 같은 handles',17)+rect(30,75,h*scale,60,C.c)+rect(30+h*scale,75,v.length*scale,60,C.a)+rect(30+(h+v.length)*scale,75,h*scale,60,C.c)+text(30,180,`앞 ${h.toFixed(2)}초`,13)+text(315,180,`편집 사용 ${v.length}초`,13)+text(620,180,`뒤 ${h.toFixed(2)}초`,13);out=`출력 길이 ${total.toFixed(3)}초 = 편집 ${v.length}초 + 양쪽 ${v.frames}프레임. 원본이 부족하면 이 범위가 나오지 않습니다.`;}
 }
 if(key==='jcut'){
  let o=v.offset,cut=3;const x=t=>30+t*120;s=text(30,25,'화면은 3초에서 A → B로 전환',17)+rect(x(0),55,360,42,C.a)+rect(x(3),55,360,42,C.b)+text(x(0)+10,83,'화면 A',14,'white')+text(x(3)+10,83,'화면 B',14)+line(x(cut),42,x(cut),200,C.pink,'5 4');
  if(v.type==='j'){s+=rect(x(0),130,x(cut-o)-30,38,C.c)+rect(x(cut-o),130,750-x(cut-o),38,C.b)+text(x(cut-o)+10,157,'다음 장면 소리 B',13);out=`B의 소리가 화면보다 ${o.toFixed(2)}초 먼저 들어옵니다. 다음 공간을 예고합니다.`;}
  else{s+=rect(x(0),130,x(cut+o)-30,38,C.c)+rect(x(cut+o),130,750-x(cut+o),38,C.b)+text(45,157,'이전 장면 소리 A',13,'white');out=`A의 소리가 화면 전환 뒤 ${o.toFixed(2)}초 남습니다. 이전 경험을 이어갑니다.`;}
  s+=text(30,215,'작은 페이드·장소의 거리감·대사 싱크를 함께 검수합니다.',13);
 }
 el.querySelector('.canvas').innerHTML=svg(s,245);el.querySelector('output').textContent=out;
 }
 el.querySelectorAll('[data-v]').forEach(e=>{e.addEventListener('input',update);e.addEventListener('change',update);});update();
}
return {mount};})();

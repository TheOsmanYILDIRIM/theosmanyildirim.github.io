const $ = (id) => document.getElementById(id);
const DATA = JSON.parse($('experiment-data').textContent);
const LAYOUTS = DATA.layout;
const VOWELS = new Set('aeıioöuü');
const LETTERS = new Set('abcçdefgğhıijklmnoöprsştuüvyz');
const corpusSize = DATA.metadata.train_words + DATA.metadata.test_words;
$('corpus-size').textContent = new Intl.NumberFormat('tr-TR').format(corpusSize);
let activeLayout = 'V29';
let heatHand = 'left';
let calibration = null;
const calEntries = {left:[],right:[]};
const trials = [];
let promptBlock = 0;
let target = '';
let typed = '';
let startedAt = null;
let finishedAt = null;
let sessionClock = null;
let currentEvents = [];
let errors = 0;

function node(tag, cls, text) {
  const result = document.createElement(tag);
  if(cls) result.className = cls;
  if(text !== undefined) result.textContent = text;
  return result;
}
function formatNum(n, places=2) {return Number(n).toLocaleString('tr-TR',{maximumFractionDigits:places,minimumFractionDigits:places});}
function keyHand(el) {
  const parent=el.closest('.keyrow');const rect=el.getBoundingClientRect();
  const outer=parent.getBoundingClientRect();return ((rect.left+rect.width/2-outer.left)/outer.width)<.5?'L':'R';
}
function buildRows(parent, rows, interactive=false, onKey=null) {
  parent.replaceChildren();
  rows.forEach((letters,r)=>{
    const line=node('div','keyrow'); line.dataset.row=r;
    Array.from(letters).forEach((letter,c)=>{
      const key=node(interactive?'button':'div','key'+(VOWELS.has(letter)?' vowel':'')+(!LETTERS.has(letter)?' other':''),letter.toLocaleUpperCase('tr-TR'));
      key.dataset.letter=letter; key.dataset.column=c;
      if(interactive){key.type='button';key.setAttribute('aria-label',`${letter} harfi`);key.addEventListener('pointerdown', e=>{
        if(e.pointerType==='mouse'&&e.button!==0)return;
        e.preventDefault();onKey(letter,key,e);
      });}
      if(c>0 && (c/(letters.length)<.5) && ((c+1)/(letters.length)>=.5))key.classList.add('midline');
      line.appendChild(key);
    }); parent.appendChild(line);
  });
}
function showTab(name) {
  for(const button of document.querySelectorAll('.tab')) {
    const picked=button.dataset.tab===name;
    button.classList.toggle('active',picked);button.setAttribute('aria-selected',String(picked));
    $('panel-'+button.dataset.tab).classList.toggle('hidden',!picked);
  }
  if(name==='calibrate') renderHeat();
  if(name==='typing') setupTypingLayout();
}
for(const b of document.querySelectorAll('.tab')) b.addEventListener('click',()=>showTab(b.dataset.tab));

function renderLayoutPicks() {
  const box=$('layout-picks');box.replaceChildren();
  Object.entries(LAYOUTS).forEach(([id,v])=>{
    const b=node('button','pick'+(id===activeLayout?' selected':''));b.type='button';
    b.append(node('span','code',id),node('strong','',v.title),node('small','',v.rows.map(x=>x.length).join(' · ')+' tuş'));
    b.addEventListener('click',()=>{activeLayout=id;renderLayoutPicks();renderAnalysis();});box.append(b);
  });
}
function metricItem(label,value,note) {
  const box=node('div','metric');box.append(node('strong','',value),node('span','',label),node('div','metric-note',note));return box;
}
function renderAnalysis() {
  const selected=LAYOUTS[activeLayout];const m=selected.holdout;
  $('current-name').textContent=selected.title;$('current-keys').textContent=`${m.keys} harf tuşu`;
  buildRows($('demo-board'),selected.rows);
  const grid=$('metric-grid');grid.replaceChildren(
    metricItem('Model hareket indeksi',formatNum(m.motion_index),'Düşük değer avantajlı'),
    metricItem('Erişim indeksi',formatNum(m.reach_index),'Varsayımsal başparmak bölgesi'),
    metricItem('Bölge değişimi',formatNum(m.alternation_pct,1)+'%','Gerçek başparmak kimliği değil'),
    metricItem('Tek parmak yol uzunluğu',formatNum(m.glide_distance,3),'Ekran genişliğine oranlı')
  );
  const all=Object.entries(LAYOUTS).map(([id,l])=>({id,l,score:l.holdout.motion_index}));
  const max=Math.max(...all.map(x=>x.score))*1.10;
  const bar=$('bar-compare');bar.replaceChildren();
  for(const item of all) {
    const row=node('div','bar-item');
    const track=node('div','bar-track'),fill=node('div','bar-fill');
    fill.style.width=(100*item.score/max)+'%';track.append(fill);
    row.append(node('label','',item.id+' · '+item.l.title),track,node('strong','',formatNum(item.score)));
    bar.append(row);
  }
}
renderLayoutPicks();renderAnalysis();

// Calibration: always 10x3, measured per requested hand, NOT actual finger identity detection.
function seededShuffle(arr, seed) {
  let state=seed>>>0; const next=()=>{state=(Math.imul(1664525,state)+1013904223)>>>0;return state/4294967296;};
  for(let i=arr.length-1;i>0;i--){const j=Math.floor(next()*(i+1));[arr[i],arr[j]]=[arr[j],arr[i]];}
  return arr;
}
function renderCalibrationBoard() {
  const board=$('cal-board');board.replaceChildren();
  for(let r=0;r<3;r++) {
    const line=node('div','keyrow');
    for(let c=0;c<10;c++) {
      const id=r*10+c;
      const btn=node('button','key',String(id+1));btn.type='button';btn.dataset.index=String(id);
      btn.addEventListener('pointerdown',e=>tapCalibration(id,e));
      line.appendChild(btn);
    }
    board.append(line);
  }
  showCalibrationTarget();
}
function showCalibrationTarget() {
  for(const b of $('cal-board').querySelectorAll('.key'))b.classList.remove('target');
  if(!calibration) return;
  const idx=calibration.order[calibration.cursor];
  const el=$('cal-board').querySelector(`[data-index="${idx}"]`);if(el)el.classList.add('target');
  $('cal-progress').textContent=`${calibration.cursor} / 30`;
  $('cal-state').textContent=(calibration.hand==='left'?'Sol':'Sağ')+' başparmak ile dokun';
  calibration.started=performance.now();
}
function startCalibration(hand) {
  if(LAYOUTS.P29){delete LAYOUTS.P29;if(activeLayout==='P29')activeLayout='V29';$('test-layout').querySelector('option[value="P29"]')?.remove();$('make-personal').disabled=true;renderLayoutPicks();renderAnalysis();}
  const order=seededShuffle(Array.from({length:30},(_,i)=>i),hand==='left'?31832:29311);
  calibration={hand,order,cursor:0,started:0};
  $('cal-tip').textContent='Yalnız seçtiğin başparmakla yeşil hedefe bas.';
  showCalibrationTarget();renderHeat();
}
function tapCalibration(actual,e) {
  if(!calibration)return;
  if(e.pointerType==='mouse'&&e.button!==0)return;
  e.preventDefault();
  const now=performance.now();const intended=calibration.order[calibration.cursor];
  const rect=$('cal-board').getBoundingClientRect();
  const hit=actual===intended;
  calEntries[calibration.hand].push({hand:calibration.hand,target:intended,actual,hit,
    latency_ms:Math.round(now-calibration.started),x:Math.round(e.clientX-rect.left),y:Math.round(e.clientY-rect.top),
    width:Math.round(rect.width),height:Math.round(rect.height),pointer:e.pointerType});
  calibration.cursor++;
  if(calibration.cursor>=30){
    $('cal-state').textContent=(calibration.hand==='left'?'Sol':'Sağ')+' ölçümü tamamlandı';
    $('cal-progress').textContent='30 / 30';$('cal-tip').textContent='Diğer başparmağını ölçebilir veya verilerini dışa aktarabilirsin.';
    calibration=null;
  }else showCalibrationTarget();
  renderHeat();
  $('make-personal').disabled=calEntries.left.length<30||calEntries.right.length<30;
}
$('left-hand').addEventListener('click',()=>startCalibration('left'));
$('right-hand').addEventListener('click',()=>startCalibration('right'));
$('heat-left').addEventListener('click',()=>{heatHand='left';renderHeat();});
$('heat-right').addEventListener('click',()=>{heatHand='right';renderHeat();});
function renderHeat(){
  for(const h of ['left','right']){
    $('heat-'+h).classList.toggle('active',heatHand===h);
    $('heat-'+h).setAttribute('aria-pressed',String(heatHand===h));
  }
  const board=$('heat-board');board.replaceChildren();
  const data=calEntries[heatHand];const times=data.map(x=>Math.min(5000,x.latency_ms)).sort((a,b)=>a-b);
  const min=times.length?times[Math.floor(times.length*.1)]:0;
  const max=times.length?times[Math.floor(times.length*.9)]:1;
  for(let idx=0;idx<30;idx++){
    const records=data.filter(x=>x.target===idx);
    const c=node('div','heat-cell');
    if(records.length){
      const mean=records.reduce((s,x)=>s+x.latency_ms,0)/records.length;
      const miss=records.filter(x=>!x.hit).length;
      const t=Math.max(0,Math.min(1,(mean-min)/(Math.max(1,max-min))))*.75+miss/records.length*.25;
      const hue=Math.round(160*(1-t));c.style.background=`hsl(${hue} 38% 37%)`;
      c.textContent=String(Math.round(mean));c.title=`Hücre ${idx+1}: ${Math.round(mean)} ms, ${records.length-miss}/${records.length} isabet`;
    }else{c.textContent='–';c.title='Veri yok';}board.append(c);
  }
  const hits=data.filter(x=>x.hit).length;
  const avg=data.length?Math.round(data.reduce((s,x)=>s+x.latency_ms,0)/data.length):0;
  $('heat-stats').textContent=data.length?`${data.length}/30 hedef · İsabet ${formatNum(100*hits/data.length,1)}% · Ortalama yanıt ${avg} ms · Her hücrede yalnız ${Math.round(data.length/30)} ölçüm (keşifsel)`:'Ölçüm yapılmadı. Her el için 30 hedef var.';
}
renderCalibrationBoard();renderHeat();


// Personalized candidate, shrinkage-regularized against the explicit geometric prior.
function personalPlan(){
  const aggregate=DATA.corpus_aggregates.train;
  const u=aggregate.uni.split('.').map(s=>parseInt(s,36));
  const b=aggregate.bi.split('.').map(s=>parseInt(s,36));
  const alphabet=DATA.corpus_aggregates.alphabet;
  const size=29;const slots=[];
  for(let r=0;r<3;r++){
    const n=r===2?9:10;
    for(let c=0;c<n;c++){
      const x=(c+.5)/n,y=(r+.5)/3,left=x<.5;
      const hand=left?'left':'right';const ideal=left?.22:.78;
      let prior=Math.hypot((x-ideal)/.48,(y-.72)/.68)+((y>.8&&(x<.15||x>.85))?.16:0);
      const records=calEntries[hand];const lengths=records.map(o=>o.latency_ms).sort((a,b)=>a-b);
      const median=lengths[Math.floor(lengths.length/2)]||550;
      const sample=records.filter(t=>t.target===r*10+Math.min(9,Math.floor(x*10)));
      const relative=sample.length?sample.reduce((acc,t)=>acc+
          Math.max(-.5,Math.min(1.5,(t.latency_ms-median)/Math.max(250,median)))+(!t.hit?.5:0),0)/sample.length:0;
      // An individual calibration tap only receives 25% trust.
      prior=Math.max(0,prior+Math.max(-.4,Math.min(.7,relative))*sample.length/(sample.length+3));
      slots.push({x,y,n,hand,cost:prior,width:(n/10)**1.7});
    }
  }
  const pair=slots.map(a=>slots.map(z=>{
    const d=Math.hypot(a.x-z.x,a.y-z.y),w=1/Math.max(a.n,z.n);
    return Math.log2(1+d/w)*(a.hand===z.hand?1:.34);
  }));
  const ut=u.reduce((a,z)=>a+z,0),bt=b.reduce((a,z)=>a+z,0);
  const base=[...'jfövücgzğşpuhaedrkstçoıinlmyb'];
  if(base.length!==size||new Set(base).size!==size)throw new Error('Bad candidate');
  const lookup=new Map([...alphabet].map((x,i)=>[x,i]));
  const index=()=>{const arr=new Array(size);base.forEach((c,s)=>arr[lookup.get(c)]=s);return arr;};
  function objective(){
    const p=index();let reach=0,width=0,motion=0;
    for(let i=0;i<size;i++){reach+=u[i]*slots[p[i]].cost;width+=u[i]*slots[p[i]].width;
      for(let j=0;j<size;j++)motion+=b[i*size+j]*pair[p[i]][p[j]];
    }
    return .64*(motion/bt)+.27*(reach/ut)+.09*(width/ut);
  }
  let rng=20261018>>>0;
  function next(){rng=(Math.imul(rng,1664525)+1013904223)>>>0;return rng/4294967296;}
  let cur=objective(),best=cur,bestChars=base.slice();
  for(let step=0;step<2800;step++){
    const x=Math.floor(next()*29),y=Math.floor(next()*29);
    if(x===y)continue;[base[x],base[y]]=[base[y],base[x]];
    const proposed=objective();const t=.09*Math.pow(.0005/.09,step/2799);
    if(proposed<cur||next()<Math.exp((cur-proposed)/t)){
      cur=proposed;if(cur<best){best=cur;bestChars=base.slice();}
    }else [base[x],base[y]]=[base[y],base[x]];
  }
  const rows=[bestChars.slice(0,10).join(''),bestChars.slice(10,20).join(''),bestChars.slice(20).join('')];
  // Use the exact same geometry-only reporting convention as the other variants,
  // separately from the personal calibration used in searching the layout.
  function evaluateSplit(split){
    const ue=split.uni.split('.').map(s=>parseInt(s,36)),be=split.bi.split('.').map(s=>parseInt(s,36));
    const positions=Object.fromEntries([...rows.join('')].map((c,i)=>[c,slots[i]]));
    let motion=0,reach=0,width=0,glide=0,alternation=0,left=0,ut=0,bt=0;
    for(let i=0;i<29;i++){
      const z=positions[alphabet[i]],ideal=z.hand==='left'?.22:.78;
      const prior=Math.hypot((z.x-ideal)/.48,(z.y-.72)/.68)+((z.y>.8&&(z.x<.15||z.x>.85))?.16:0);
      reach+=ue[i]*prior;width+=ue[i]*z.width;ut+=ue[i];if(z.hand==='left')left+=ue[i];
      for(let j=0;j<29;j++){
        const a=positions[alphabet[j]],num=be[i*29+j];
        const d=Math.hypot(z.x-a.x,z.y-a.y),switches=z.hand!==a.hand;
        motion+=num*Math.log2(1+d*Math.max(z.n,a.n))*(switches?.34:1);
        glide+=num*d;alternation+=num*(switches?1:0);bt+=num;
      }
    }
    const round=n=>Math.round(n*1e6)/1e6;
    return {motion_index:round(motion/bt),reach_index:round(reach/ut),width_index:round(width/ut),glide_distance:round(glide/bt),alternation_pct:round(alternation/bt*1e5)/1000,left_pct:round(left/ut*1e5)/1000,right_pct:round((1-left/ut)*1e5)/1000,keys:29};
  }
  return {rows,train:evaluateSplit(DATA.corpus_aggregates.train),holdout:evaluateSplit(DATA.corpus_aggregates.test),
    title:'Kişisel Başparmak Düzeni',optimized_for:'personal_calibration',calibrated_samples:{left:calEntries.left.length,right:calEntries.right.length}};
}
$('make-personal').addEventListener('click',()=>{
  if(calEntries.left.length<30||calEntries.right.length<30)return;
  const personalized=personalPlan();
  LAYOUTS.P29=personalized;activeLayout='P29';
  const option=node('option','', 'P29 · '+personalized.title);option.value='P29';
  $('test-layout').append(option);$('test-layout').value='P29';
  renderLayoutPicks();renderAnalysis();buildTypingBoard();resetTrial();
  $('personal-info').textContent='P29 oluşturuldu. Ölçümler az olduğu için sonuç keşifseldir; diğer dizilimlerle aynı cümleleri karşılaştır.';
  showTab('analyze');
});

// Typing trials: no autocorrect or OS keyboard; raw taps only. No hidden collection.
function promptText(index) {
  const words=['bir','için','ben','çok','ama','evet','var','değil','şey','hayır','daha','sen','kadar','bana','gibi','bunu','yok','onu','iyi','tamam','beni','seni','benim','her','sana','neden','sadece','zaman','senin','burada','olduğunu','nasıl','hiç','sonra','şimdi','öyle','misin','önce','biraz','hadi','güzel','musun','oldu','yani','ona','böyle','onun','bile','lütfen','bak','eğer','peki','çünkü','artık','gerçekten','geri','biliyorum','istiyorum','kim','başka','olarak','belki','tek','doğru','büyük','olan','biri','bay','buraya','olur','adam','ile','olacak','hey','hiçbir','biz','demek','sanırım','yardım','bilmiyorum','bunun','teşekkürler','tüm','gün','yeni','fazla','ederim','nerede','tanrım','merhaba','efendim','şeyi','orada','gece','son','kötü','şeyler','biliyor','harika','iki','sorun','işte','bütün','tam','gerek','siz','diye','hemen','üzgünüm','küçük','olabilir','olsun','size','bayan','aynı','hakkında','teşekkür','gel','tabii','yüzden'];
  return seededShuffle(words.slice(),19862+index*733).slice(0,10).join(' ');
}
function buildTypingBoard(){
  const id=$('test-layout').value;
  buildRows($('typing-board'),LAYOUTS[id].rows,true,(letter,key,e)=>addTap(letter,keyHand(key),e));
}
function setupTypingLayout(){
  const select=$('test-layout');
  if(!select.options.length){
    Object.entries(LAYOUTS).forEach(([id,x])=>{const option=document.createElement('option');option.value=id;option.textContent=id+' · '+x.title;select.append(option);});
    select.value=activeLayout;
  }
  buildTypingBoard();if(!target)resetTrial();
}
function refreshTyped(){
  $('entry').textContent=typed||'Yazmaya dokunarak başla…';
  $('entry').classList.toggle('error',!target.startsWith(typed));
  $('test-progress').textContent=`${typed.length} / ${target.length} karakter`;
}
function elapsedMs(){return startedAt===null?0:Math.max(0,(finishedAt??performance.now())-startedAt);}
function renderElapsed(){
  const ms=elapsedMs();$('elapsed').textContent=String(Math.floor(ms/60000)).padStart(2,'0')+':'+String(Math.floor((ms%60000)/1000)).padStart(2,'0')+'.'+Math.floor(ms%1000/100);
}
function resetTrial(){
  if(sessionClock){clearInterval(sessionClock);sessionClock=null;}
  typed='';startedAt=null;finishedAt=null;currentEvents=[];errors=0;
  target=promptText(promptBlock);
  $('prompt').textContent=target;
  $('test-status').textContent='İlk harfe dokunduğunda ölçüm başlar.';
  $('typing-metrics').replaceChildren();refreshTyped();renderElapsed();
}
function addTap(key,hand,e){
  if(finishedAt!==null)return;
  const now=performance.now();if(startedAt===null){startedAt=now;sessionClock=setInterval(renderElapsed,100);}
  const expected=target[typed.length]??'';
  if(key==='BACK')typed=typed.slice(0,-1);
  else typed+=key;
  const correct=key==='BACK'||expected===key;
  if(!correct&&key!=='BACK')errors++;
  currentEvents.push({ms:Math.round(now-startedAt),key,region:hand||null,correct,typed_length:typed.length,
    pointer:e?.pointerType??'virtual',x:e&&Number.isFinite(e.clientX)?Math.round(e.clientX):null,y:e&&Number.isFinite(e.clientY)?Math.round(e.clientY):null});
  refreshTyped();
  if(typed===target){finishedAt=performance.now();clearInterval(sessionClock);sessionClock=null;renderElapsed();finishTrial();}
}
function finishTrial(){
  const duration=Math.max(1,elapsedMs())/60000;
  const dig=[];let prev=null;
  for(const ev of currentEvents){
    if(LETTERS.has(ev.key)&&ev.correct){if(prev && prev.region && ev.region){const dt=ev.ms-prev.ms;if(dt>0 && dt<5000)dig.push({dt,change:ev.region!==prev.region});}prev=ev;}
    else prev=null;
  }
  const avg=items=>items.length?Math.round(items.reduce((s,x)=>s+x.dt,0)/items.length):null;
  const same=dig.filter(x=>!x.change),other=dig.filter(x=>x.change);
  const result={layout:$('test-layout').value,mode:$('test-mode').value,block:promptBlock,
    duration_ms:Math.round(elapsedMs()),characters:target.length,presses:currentEvents.length,errors,
    net_wpm:Math.round(target.length/5/duration*100)/100,
    raw_wpm:Math.round(currentEvents.length/5/duration*100)/100,
    kspc:Math.round(currentEvents.length/target.length*1000)/1000,
    same_region_ms:avg(same),different_region_ms:avg(other),
    region_pairs:dig.length,timestamp:new Date().toISOString(),events:currentEvents.map(x=>({...x}))};
  trials.push(result);
  $('test-status').textContent='✓ Deneme tamamlandı. Aynı kelime bloğuyla diğer dizilimi dene.';
  $('typing-metrics').replaceChildren(
    metricItem('Net WPM',formatNum(result.net_wpm),'5 karakter = 1 sözcük'),
    metricItem('KSPC',formatNum(result.kspc,3),'Düzeltmeler dahil / hedef uzunluğu'),
    metricItem('İlk deneme hatası',String(result.errors),'Düzeltmeden önce yanlış dokunuş'),
    metricItem('Bölge değişim ms',result.different_region_ms===null?'—':String(result.different_region_ms),'Bölge içi: '+(result.same_region_ms??'—')+' ms'));
  renderTrialHistory();
}
function renderTrialHistory(){
  const box=$('trial-history');if(!trials.length){box.textContent='Henüz tamamlanan deneme yok.';return;}
  const table=node('table');const headers=['Düzen','Mod','Süre (sn)','Net WPM','KSPC','Hata'];
  const tr=node('tr');headers.forEach(h=>tr.append(node('th','',h)));const thead=node('thead');thead.append(tr);table.append(thead);
  const body=node('tbody');for(const x of trials){const row=node('tr');
    [x.layout,x.mode==='two'?'Çift':'Tek',formatNum(x.duration_ms/1000,1),formatNum(x.net_wpm,1),formatNum(x.kspc,2),String(x.errors)].forEach(v=>row.append(node('td','',v)));
    body.append(row);
  }table.append(body);box.replaceChildren(table);
}
$('test-layout').addEventListener('change',()=>{buildTypingBoard();resetTrial();});
$('test-mode').addEventListener('change',resetTrial);
$('new-prompt').addEventListener('click',()=>{promptBlock++;resetTrial();});
$('reset-trial').addEventListener('click',resetTrial);
$('key-space').addEventListener('pointerdown',e=>{e.preventDefault();addTap(' ',null,e);});
$('key-back').addEventListener('pointerdown',e=>{e.preventDefault();addTap('BACK',null,e);});

function download(name,content,mime){
  const url=URL.createObjectURL(new Blob([content],{type:mime}));
  const a=document.createElement('a');a.href=url;a.download=name;document.body.append(a);a.click();a.remove();
  setTimeout(()=>URL.revokeObjectURL(url),3000);
}
$('export-cal').addEventListener('click',()=>download('thumb_calibration_v1.json',JSON.stringify({version:1,schema:'left/right target-grid reaction and tap error; no finger identity detection',viewport:{width:innerWidth,height:innerHeight,dpr:devicePixelRatio},samples:calEntries},null,2),'application/json'));
$('export-trials-raw').addEventListener('click',()=>{
  download('thumb_typing_trials_raw_v1.json',JSON.stringify({
    version:1,description:'Local tests only; finger identity inferred from screen half, NOT sensed',
    viewport:{width:innerWidth,height:innerHeight,dpr:devicePixelRatio},
    calibration_sample_count:{left:calEntries.left.length,right:calEntries.right.length},
    layout_rows:Object.fromEntries(Object.entries(LAYOUTS).map(([name,l])=>[name,l.rows])),
    trials
  },null,2),'application/json');
});
$('export-trials').addEventListener('click',()=>{
  const fields=['layout','mode','block','duration_ms','characters','presses','errors','net_wpm','raw_wpm','kspc','same_region_ms','different_region_ms','region_pairs','timestamp'];
  const csv=[fields.join(','),...trials.map(x=>fields.map(f=>x[f]??'').join(','))].join('\r\n');
  download('thumb_typing_trials_v1.csv','\ufeff'+csv,'text/csv;charset=utf-8');
});
setupTypingLayout();

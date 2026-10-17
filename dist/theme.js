/* ══ 管理者工作室 設計系統 22.0.0 ══ theme.js
   色系切換（規範 3.8、4.2）與深淺模式（規範 8.8）。由 emit_css.py 產生，THEMES 表取自元件庫。
   用法：
     <html data-style="s1">                         本系統選定的風格（建置時決定，全站只有一套）
     <script src="theme.js"></script>
     DS.applyTheme('c1')                            切換色系；不合法組合退回 c1 並回傳實際套用的 key
     DS.setColorScheme('dark'|'light'|'system')     只有 S6 有深色（DARK_STYLES）；其他風格呼叫無效果
     跟隨系統時會監聽 prefers-color-scheme 的變化並重套品牌色
   色系與深淺偏好以 localStorage 記住（鍵 ds.theme、ds.scheme），網址參數 ?theme=c3 優先。 */
(function(){
const THEMES={
 c1:{"id":"C1","name":"深海藍","acc":"#2B5FB8","accSoft":"#EDF1F9","acc2":"#C2377B","acc2Soft":"#FAEEF4","acc2Deep":"#BA3576","accDeep":"#2B5FB8","acc2Type":"deep","styles":["s1","s2","s3","s4","s5","s6","s7"],"adjust":[],"series":"C"},
 c2:{"id":"C2","name":"深湖青","acc":"#0F5C63","accSoft":"#EBF1F2","acc2":"#C4663A","acc2Soft":"#FAF2EE","acc2Deep":"#A15430","accDeep":"#0F5C63","acc2Type":"deep","styles":["s1","s2","s3","s4","s5","s6","s7"],"adjust":[],"series":"C"},
 c3:{"id":"C3","name":"深靛","acc":"#2C2A72","accSoft":"#EDEDF3","acc2":"#8C7AE6","acc2Soft":"#F5F4FD","acc2Deep":"#6A5DAF","accDeep":"#2C2A72","acc2Type":"deep","styles":["s1","s2","s3","s4","s5","s6","s7"],"adjust":[],"series":"C"},
 c4:{"id":"C4","name":"電光紫","acc":"#6D28D9","accSoft":"#F3EDFC","acc2":"#0F8A99","acc2Soft":"#EBF5F6","acc2Deep":"#0D7481","accDeep":"#6D28D9","acc2Type":"deep","styles":["s1","s2","s3","s4","s5","s6","s7"],"adjust":[],"series":"C"},
 c5:{"id":"C5","name":"森林綠","acc":"#1F5E3D","accSoft":"#ECF1EF","acc2":"#A16207","acc2Soft":"#F7F2EA","acc2Deep":"#975C07","accDeep":"#1F5E3D","acc2Type":"deep","styles":["s1","s2","s3","s4","s5","s6","s7"],"adjust":[],"series":"C"},
 c6:{"id":"C6","name":"胡桃棕","acc":"#6B4A33","accSoft":"#F2F0EE","acc2":"#4A6B55","acc2Soft":"#F0F2F1","acc2Deep":"#4A6B55","accDeep":"#6B4A33","acc2Type":"deep","styles":["s1","s2","s3","s4","s5","s6","s7"],"adjust":[],"series":"C"},
 c7:{"id":"C7","name":"焦糖磚橘","acc":"#A8481F","accSoft":"#F8EFEC","acc2":"#2B2B2B","acc2Soft":"#EDEDED","acc2Deep":"#2B2B2B","accDeep":"#A8481F","acc2Type":"deep","styles":["s1","s2","s3","s4","s5","s6","s7"],"adjust":[],"series":"C"},
 c8:{"id":"C8","name":"暖墨","acc":"#23201E","accSoft":"#ECECEC","acc2":"#D95F1E","acc2Soft":"#FCF1EC","acc2Deep":"#AE4C18","accDeep":"#23201E","acc2Type":"deep","styles":["s1","s2","s3","s4","s5","s6","s7"],"adjust":[],"series":"C"},
 c9:{"id":"C9","name":"唇膏紅","acc":"#9F2436","accSoft":"#F7EDEF","acc2":"#2A5C6A","acc2Soft":"#EEF2F3","acc2Deep":"#2A5C6A","accDeep":"#9F2436","acc2Type":"deep","styles":["s1","s2","s3","s4","s5","s6","s7"],"adjust":[],"series":"C"},
 c10:{"id":"C10","name":"節慶桃紅","acc":"#9E2C6A","accSoft":"#F7EEF3","acc2":"#5C97CB","acc2Soft":"#F2F7FB","acc2Deep":"#336DA0","accDeep":"#9E2C6A","acc2Type":"deep","styles":["s1","s2","s3","s4","s5","s6","s7"],"adjust":[],"series":"C"},
 c11:{"id":"C11","name":"燒橄欖","acc":"#646049","accSoft":"#F3F2F0","acc2":"#C65D52","acc2Soft":"#FAF2F1","acc2Deep":"#B2463B","accDeep":"#646049","acc2Type":"deep","styles":["s1","s2","s3","s4","s5","s6","s7"],"adjust":[],"series":"C"},
 c12:{"id":"C12","name":"玫瑰棕","acc":"#80565B","accSoft":"#F5F1F2","acc2":"#BA797D","acc2Soft":"#F9F4F5","acc2Deep":"#9F5257","accDeep":"#80565B","acc2Type":"deep","styles":["s1","s2","s3","s4","s5","s6","s7"],"adjust":[],"series":"C"},
 sc1:{"id":"SC1","name":"深綠 × 相思黃","acc":"#35463D","accSoft":"#EFF0EF","acc2":"#DACD65","acc2Soft":"#FCFBF3","acc2Deep":"#6F6519","acc2Type":"light","styles":["s1","s3","s5","s6","s7"],"adjust":["s4"],"series":"SC","accDeep":"#35463D"},
 sc2:{"id":"SC2","name":"鈷藍 × 亮橘","acc":"#2449E8","accSoft":"#EEF1FD","acc2":"#FF7A1A","acc2Soft":"#FFF3EA","acc2Deep":"#B0490A","acc2Type":"light","styles":["s1","s3","s5","s6","s7"],"adjust":["s4"],"series":"SC","accDeep":"#2449E8"},
 sc3:{"id":"SC3","name":"石板藍 × 冰川青","acc":"#3D4C5E","accSoft":"#EFF1F3","acc2":"#5FB4C9","acc2Soft":"#F0F8FA","acc2Deep":"#296778","acc2Type":"light","styles":["s1","s3","s4","s5","s6","s7"],"adjust":["s2"],"series":"SC","accDeep":"#3D4C5E"}
};
/* 深色模式的品牌色（規範 8.8：OKLab 只加明度、填色上一律深色字）；目前只有 S6 有深色 */
const DARK={"c1":{"acc":"#629AF8","accSoft":"#262E3E","accDeep":"#629AF8","acc2":"#C2377B","acc2Soft":"#351F2A","acc2Deep":"#F46BA8","onAcc":"#121212","onAcc2":"#121212","acc2Text":"#EDEDED"},"c2":{"acc":"#61A5AC","accSoft":"#253031","accDeep":"#61A5AC","acc2":"#C4663A","acc2Soft":"#35261F","acc2Deep":"#D88561","onAcc":"#121212","onAcc2":"#121212","acc2Text":"#121212"},"c3":{"acc":"#8D94E6","accSoft":"#2C2E3B","accDeep":"#8D94E6","acc2":"#8C7AE6","acc2Soft":"#2C293B","acc2Deep":"#9C90E7","onAcc":"#121212","onAcc2":"#121212","acc2Text":"#121212"},"c4":{"acc":"#A486FF","accSoft":"#302B3F","accDeep":"#A486FF","acc2":"#0F8A99","acc2Soft":"#182C2E","acc2Deep":"#4FA6B4","onAcc":"#121212","onAcc2":"#121212","acc2Text":"#121212"},"c5":{"acc":"#6BA984","accSoft":"#27312B","accDeep":"#6BA984","acc2":"#A16207","acc2Soft":"#302617","acc2Deep":"#CC8E48","onAcc":"#121212","onAcc2":"#121212","acc2Text":"#EDEDED"},"c6":{"acc":"#B9947B","accSoft":"#332E2A","accDeep":"#B9947B","acc2":"#4D6E58","acc2Soft":"#222724","acc2Deep":"#81A48C","onAcc":"#121212","onAcc2":"#121212","acc2Text":"#EDEDED"},"c7":{"acc":"#E57F57","accSoft":"#3A2A24","accDeep":"#E57F57","acc2":"#666666","acc2Soft":"#262626","acc2Deep":"#9B9B9B","onAcc":"#121212","onAcc2":"#121212","acc2Text":"#EDEDED"},"c8":{"acc":"#9F9B98","accSoft":"#2F2F2E","accDeep":"#9F9B98","acc2":"#D95F1E","acc2Soft":"#39251B","acc2Deep":"#E88051","onAcc":"#121212","onAcc2":"#121212","acc2Text":"#121212"},"c9":{"acc":"#F17178","accSoft":"#3C2829","accDeep":"#F17178","acc2":"#3C6D7C","acc2Soft":"#1F272A","acc2Deep":"#71A3B3","onAcc":"#121212","onAcc2":"#121212","acc2Text":"#EDEDED"},"c10":{"acc":"#E972AC","accSoft":"#3B2831","accDeep":"#E972AC","acc2":"#5C97CB","acc2Soft":"#252E36","acc2Deep":"#659FD5","onAcc":"#121212","onAcc2":"#121212","acc2Text":"#121212"},"c11":{"acc":"#A19D84","accSoft":"#302F2B","accDeep":"#A19D84","acc2":"#C65D52","acc2Soft":"#362523","acc2Deep":"#ED7B6C","onAcc":"#121212","onAcc2":"#121212","acc2Text":"#121212"},"c12":{"acc":"#BD8F94","accSoft":"#342D2E","accDeep":"#BD8F94","acc2":"#BA797D","acc2Soft":"#34292A","acc2Deep":"#D78588","onAcc":"#121212","onAcc2":"#121212","acc2Text":"#121212"},"sc1":{"acc":"#8CA095","accSoft":"#2C2F2E","accDeep":"#8CA095","acc2":"#DACD65","acc2Soft":"#393726","acc2Deep":"#A69C55","onAcc":"#121212","onAcc2":"#121212","acc2Text":"#121212"},"sc2":{"acc":"#6D96FF","accSoft":"#272E3F","accDeep":"#6D96FF","acc2":"#FF7A1A","acc2Soft":"#3F291A","acc2Deep":"#EA7E4B","onAcc":"#121212","onAcc2":"#121212","acc2Text":"#121212"},"sc3":{"acc":"#8C9DB2","accSoft":"#2C2F32","accDeep":"#8C9DB2","acc2":"#5FB4C9","acc2Soft":"#253336","acc2Deep":"#68A5B7","onAcc":"#121212","onAcc2":"#121212","acc2Text":"#121212"}};
const DARK_STYLES=['s6'];
const root=document.documentElement;
const STYLE=(root.dataset.style||'s1').toLowerCase();
const mq=window.matchMedia?window.matchMedia('(prefers-color-scheme: dark)'):null;
function isDark(){
  if(!DARK_STYLES.includes(STYLE)) return false;
  const a=root.getAttribute('data-theme');
  if(a==='dark') return true; if(a==='light') return false;
  return !!(mq&&mq.matches);
}
function allowed(k){const t=THEMES[k];return !!t&&(t.styles.includes(STYLE)||(t.adjust||[]).includes(STYLE));}
function applyTheme(k){
  let t=THEMES[k];
  if(!t||!allowed(k)){ if(typeof DS.onFallback==='function') DS.onFallback(k,'c1'); k='c1'; t=THEMES.c1; }
  const dark=isDark();
  if(dark&&DARK[k]) t=Object.assign({},t,DARK[k]);
  const r=root.style;
  r.setProperty('--acc',t.acc); r.setProperty('--acc-soft',t.accSoft); r.setProperty('--accsoft',t.accSoft); r.setProperty('--acc-deep',t.accDeep);
  r.setProperty('--acc2',t.acc2); r.setProperty('--acc2-soft',t.acc2Soft); r.setProperty('--acc2soft',t.acc2Soft); r.setProperty('--acc2-deep',t.acc2Deep);
  const ink=(getComputedStyle(root).getPropertyValue('--ink')||'#26292E').trim();
  if(dark){ r.setProperty('--acc2-text',t.acc2Text); r.setProperty('--on-acc',t.onAcc); r.setProperty('--on-acc2',t.onAcc2); }
  else { r.setProperty('--acc2-text', t.acc2Type==='light' ? ink : '#FFFFFF'); r.removeProperty('--on-acc'); r.removeProperty('--on-acc2'); }
  root.classList.toggle('sc-light', t.acc2Type==='light');
  root.classList.toggle('sc-adjust', !!(t.adjust&&t.adjust.includes(STYLE)));
  root.dataset.theme_id=t.id;
  try{ localStorage.setItem('ds.theme',k); }catch(_){}
  return k;
}
if(mq&&mq.addEventListener) mq.addEventListener('change',()=>{ const k=root.dataset.theme_key; if(k) applyTheme(k); });
function setColorScheme(mode){
  if(mode==='system'){ root.removeAttribute('data-theme'); }
  else { root.setAttribute('data-theme', mode==='dark'?'dark':'light'); }
  try{ localStorage.setItem('ds.scheme',mode); }catch(_){}
  /* 深型／淺型副色的字色跟著 --ink 走，換模式後重算 */
  const k=root.dataset.theme_key; if(k) applyTheme(k);
}
function init(){
  let k=null, mode=null;
  try{ k=new URLSearchParams(location.search).get('theme'); }catch(_){}
  try{ k=k||localStorage.getItem('ds.theme'); mode=localStorage.getItem('ds.scheme'); }catch(_){}
  if(mode&&mode!=='system') root.setAttribute('data-theme',mode);
  root.dataset.theme_key=applyTheme(k||'c1');
}
window.DS={THEMES,STYLE,allowed,applyTheme:function(k){root.dataset.theme_key=k;return applyTheme(k);},setColorScheme,init};
init();
})();

(function(){
const C=window.QADMORA||{},$=s=>document.querySelector(s),$$=s=>[...document.querySelectorAll(s)];
const wa=t=>`https://wa.me/${C.whatsapp}?text=${encodeURIComponent(t)}`;
$$('[data-wa]').forEach(a=>a.href=wa(a.dataset.wa));
const A=C.ads||{};
if(A.top&&A.top.text&&$('#adTop')){const e=$('#adTop');e.hidden=false;e.textContent=A.top.text+' ';const a=document.createElement('a');a.href=A.top.link;a.textContent=A.top.label;e.append(a)}
if(A.middle&&A.middle.title&&$('#adMid')){const m=A.middle;$('#adMid').hidden=false;const b=$('#bannerBox'),h=document.createElement('h3');h.textContent=m.title;b.append(h);
 if(m.image){const i=document.createElement('img');i.src=m.image;i.alt='';b.append(i)}const a=document.createElement('a');a.className='btn';a.href=m.link;a.textContent=m.label;b.append(a)}
const S=C.social||{},so=$('#soc');if(so)for(const k in S)if(S[k]){const a=document.createElement('a');a.href=S[k];a.rel='noopener';a.target='_blank';a.textContent=k[0].toUpperCase()+k.slice(1);so.append(a)}
function season(v){$$('.card[data-season]').forEach(c=>c.hidden=!(v==='all'||c.dataset.season===v||c.dataset.season==='All'));
 $$('#seasonChips .chip').forEach(b=>b.setAttribute('aria-pressed',b.dataset.s===v))}
if(C.useSeasons===false){$$('#seasonChips,#seasons,#navSeason').forEach(e=>e.remove())}
else{const sc=$('#seasonChips');if(sc)sc.addEventListener('click',e=>{const b=e.target.closest('.chip');if(b)season(b.dataset.s)});
 $$('.season').forEach(b=>b.addEventListener('click',()=>{season(b.dataset.s);$('#shop').scrollIntoView({behavior:'smooth'})}))}
const dr=$('#drawer'),ov=$('#overlay'),bg=$('#burger');
function menu(o){dr.classList.toggle('open',o);ov.hidden=!o;bg.setAttribute('aria-expanded',o);(o?dr.querySelector('a'):bg).focus({preventScroll:true})}
bg.onclick=()=>menu(true);ov.onclick=()=>menu(false);dr.addEventListener('click',e=>{if(e.target.closest('a'))menu(false)});
document.addEventListener('keydown',e=>{if(e.key==='Escape'&&dr.classList.contains('open'))menu(false)});
const th=$('#thumbs');if(th){const m=$('#main');const set=b=>{m.innerHTML=b.innerHTML;$$('.th').forEach(x=>x.setAttribute('aria-current',x===b))};
 th.addEventListener('click',e=>{const b=e.target.closest('.th');if(b)set(b)});set($('.th'))}
const o=$('[data-order]');if(o){const sel={};$$('[data-opt]').forEach(g=>{const on=g.querySelector('[aria-pressed=true]');if(on)sel[g.dataset.opt]=on.textContent;
 g.addEventListener('click',e=>{const b=e.target.closest('.opt');if(!b)return;g.querySelectorAll('.opt').forEach(x=>x.setAttribute('aria-pressed',x===b));sel[g.dataset.opt]=b.textContent})});
 o.addEventListener('click',e=>{e.preventDefault();const m=$('#pmsg');if(!sel.size){m.textContent='Please choose a size first.';return}m.textContent='';
 window.open(wa(`Assalam o Alaikum, I want to order ${o.dataset.name} (SKU ${o.dataset.sku}). Size: EU ${sel.size}. Colour: ${sel.colour||'any'}.`),'_blank','noopener')})}
const f=$('#form');if(f)f.addEventListener('submit',e=>{e.preventDefault();const d=new FormData(f);window.open(wa(`Name: ${d.get('n')}\nPhone: ${d.get('p')}\n${d.get('m')}`),'_blank','noopener')});
})();
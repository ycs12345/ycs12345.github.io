(() => {
 'use strict';
 const $ = (selector, root=document) => root.querySelector(selector);
 const $$ = (selector, root=document) => [...root.querySelectorAll(selector)];
 const key = 'liubai-theme';
 let theme = 'light';
 try { theme = localStorage.getItem(key) === 'dark' ? 'dark' : 'light'; } catch (_) {}
 function setTheme(next) {
  document.documentElement.dataset.theme = next;
  const btn = $('#theme-btn');
  if(btn) btn.setAttribute('aria-label',next==='dark'?'切换浅色模式':'切换深色模式');
  try {localStorage.setItem(key,next)}catch(_){}
 }
 setTheme(theme);
 $('#theme-btn')?.addEventListener('click',() => setTheme(document.documentElement.dataset.theme==='dark'?'light':'dark'));
 const menuBtn=$('#menu-btn'), menu=$('#main-nav');
 menuBtn?.addEventListener('click',()=>{
   const open=menu?.classList.toggle('open')||false;
   menuBtn.setAttribute('aria-expanded',String(open));
 });
 $$('#main-nav a').forEach(a=>a.addEventListener('click',()=>{
   menu?.classList.remove('open');menuBtn?.setAttribute('aria-expanded','false');
 }));
 let category='全部文章'; let query='';
 function updateFilters(){
   const list=$$('.entry-card,.archive-row');
   let count=0;
   for(const card of list){
     const matchCat=category==='全部文章'||card.dataset.category===category;
     const matchSearch=!query||(card.dataset.search||'').toLowerCase().includes(query);
     const visible=matchCat&&matchSearch;
     card.hidden=!visible;
     if(visible)count++;
   }
   const empty=$('#no-results');if(empty)empty.hidden=!(list.length>0&&count===0);
 }
 $$('[data-filter]').forEach(btn=>btn.addEventListener('click',()=>{
   category=btn.dataset.filter;
   $$('[data-filter]').forEach(b=>{const a=b===btn;b.classList.toggle('active',a);b.setAttribute('aria-pressed',String(a))});
   updateFilters();
   if(btn.classList.contains('category-painting')){
     const target=$('#journal');
     if(target) target.scrollIntoView({behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth',block:'start'});
   }
 }));
 $$('.post-search').forEach(input=>input.addEventListener('input',()=>{
   query=input.value.trim().toLowerCase(); updateFilters();
 }));
 const progress=$('#reading-progress');
 if(document.body.classList.contains('page-article')&&progress){
   const update=()=>{const max=document.documentElement.scrollHeight-innerHeight; progress.style.width=(max>0?Math.min(100,Math.max(0,100*scrollY/max)):100)+'%'};
   addEventListener('scroll',update,{passive:true});addEventListener('resize',update,{passive:true});update();
 }
 let toastTimer;
 function notify(msg){const t=$('#toast');if(!t)return;t.textContent=msg;t.classList.add('show');clearTimeout(toastTimer);toastTimer=setTimeout(()=>t.classList.remove('show'),2500)}
 $('#share-post')?.addEventListener('click',async()=>{
   const url=location.href;
   if(navigator.share){try{await navigator.share({url,title:document.title});return}catch(_){}}
   try{await navigator.clipboard.writeText(url);notify('文章链接已复制')}
   catch(_){notify('可以从地址栏复制文章链接')}
 });
})();

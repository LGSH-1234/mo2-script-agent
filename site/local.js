/* Local reconstruction interactions. All model actions live in /storyboard. */
function dialog(title,description,img){
 const d=document.createElement('dialog');d.className='local-dialog';
 if(img){const image=document.createElement('img');image.src=img;image.alt=title;d.append(image)}
 const h=document.createElement('h2');h.textContent=title;d.append(h);
 const p=document.createElement('p');p.textContent=description;d.append(p);
 const actions=document.createElement('div');actions.className='local-dialog-actions';d.append(actions);
 const close=document.createElement('button');close.textContent='关闭';close.onclick=()=>d.close();actions.append(close);
 d.addEventListener('close',()=>d.remove());d.addEventListener('click',e=>{if(e.target===d&&e.offsetX<0)d.close()});document.body.append(d);d.showModal();return{d,actions};
}
document.querySelectorAll('[class*="__templateUse"]').forEach(button=>{
 button.addEventListener('click',()=>{
  const card=button.closest('[class*="__templateCard"]');
  const title=card.querySelector('h3').textContent;
  const description=card.querySelector('p').textContent;
  const {actions}=dialog(title,description,card.querySelector('img').src);
  const start=document.createElement('a');start.textContent='以此灵感创作分镜';start.href='/storyboard?new=1&brief='+encodeURIComponent('创作方向：'+title+'。'+description+'。请创作一个有开端、转折和结尾的短故事。');actions.append(start);
 });
});
document.querySelectorAll('button[aria-label="语言"]').forEach(b=>{b.onclick=()=>{dialog('语言','本地演示使用简体中文。')}});
document.querySelectorAll('button[aria-label="主导航"]').forEach(b=>{b.onclick=()=>{
 const {d,actions}=dialog('MO² 工作室','');const nav=document.createElement('nav');nav.className='local-mobile-nav';
 for(const [text,href] of [['首页','/'],['我的项目','/series'],['关于我们','/about'],['Agent','https://ai.momostudio.top/'],['分镜','/storyboard'],['价格方案','/pricing']]){const a=document.createElement('a');a.textContent=text;a.href=href;nav.append(a)}d.insertBefore(nav,actions);
}});
document.querySelectorAll('button[class*="about-module"][class*="__play"]').forEach(b=>{b.textContent='前往观看';b.disabled=false;b.onclick=()=>b.closest('article')?.querySelector('a')?.click()});
document.querySelector('button[aria-label="关闭"]')?.addEventListener('click',()=>location.assign('/'));
document.querySelector('#pricing-tab-seats')?.addEventListener('click',()=>{const {actions}=dialog('席位方案','团队席位的实时方案请查看 MO² 官网。');const a=document.createElement('a');a.textContent='查看官网方案';a.href='https://app.momostudio.top/pricing';a.target='_blank';a.rel='noopener';actions.append(a)});
if(document.querySelector('[data-official-pricing]')){const note=document.createElement('p');note.className='local-pricing-note';note.textContent='本地价格展示 · 购买将在 MO² 官网进行';document.querySelector('[role="tabpanel"]')?.prepend(note)}

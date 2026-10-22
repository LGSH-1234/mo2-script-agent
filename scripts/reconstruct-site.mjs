// Rebuild local public pages from the retained REA DOM evidence. No upstream JS runs.
import fs from 'node:fs/promises';
import path from 'node:path';
import crypto from 'node:crypto';
const root=path.resolve(import.meta.dirname,'..');
const evidence=JSON.parse(await fs.readFile(process.argv[2]||'/tmp/mo2-site-zh-evidence.json','utf8'));
const out=path.join(root,'web/public/site');
await fs.mkdir(path.join(out,'assets'),{recursive:true});
const origin='https://app.momostudio.top';
const assets=new Map();
const failures=[];
function url(s,base=origin){return new URL(s.replaceAll('&amp;','&'),base).href}
async function asset(input,base=origin){
 const source=url(input,base);
 if(assets.has(source))return assets.get(source);
 const ext=path.extname(new URL(source).pathname)||'.bin';
 const name=crypto.createHash('sha256').update(source).digest('hex').slice(0,16)+ext;
 const local='/media/site/assets/'+name;
 assets.set(source,local);
 try{
  let content;
  try{content=await fs.readFile(path.join(out,'assets',name))}catch{
   const res=await fetch(source,{signal:AbortSignal.timeout(25000)});
   if(!res.ok)throw new Error('HTTP '+res.status);
   content=Buffer.from(await res.arrayBuffer());
  }
  if(ext==='.css'){
   let css=content.toString().replaceAll('https://app.momostudio.top/_next/static/chunks/%23n','#n');
   const refs=[...new Set([...css.matchAll(/url\(["']?([^)'"\s]+)["']?\)/g)].map(m=>m[1]))];
   for(const ref of refs){if(!ref.startsWith('#')&&!ref.startsWith('data:')&&!ref.startsWith('/media/'))css=css.replaceAll(ref,await asset(ref,source));}
   content=Buffer.from(css);
  }
  await fs.writeFile(path.join(out,'assets',name),content);
  return local;
 }catch(e){assets.set(source,source);failures.push({source,error:e.message});return source;}
}
for(const [step,name] of [['home-zh','index'],['about-zh','about'],['pricing-zh','pricing']]){
 let html=evidence.data.normalized_result.steps.find(s=>s.step_id===step).artifacts.dom.value.text;
 html=html.replace(/<script\b[^>]*>[\s\S]*?<\/script>/gi,'').replace(/<link\b[^>]*as="script"[^>]*>/gi,'').replace(/\son\w+="[^"]*"/g,'').replace(/<!--[^]*?-->/g,'');
 // Public captured assets are copied locally; large demo films retain observed source URLs.
 const urls=new Set();
 for(const m of html.matchAll(/<(img|link|video)\b[^>]*>/g)){
  for(const a of m[0].matchAll(/\b(src|href|poster)="([^"]+)"/g)){
   if(!/\.mp4(?:\?|$)/.test(a[2])&&!a[2].startsWith('data:'))urls.add(a[2]);
  }
 }
 const items=[...urls];
 for(let i=0;i<items.length;i+=6)await Promise.all(items.slice(i,i+6).map(async ref=>{const local=await asset(ref);html=html.replaceAll(ref,local)}));
 html=html.replace(/(<a\b[^>]*>Agent<\/a>)/,'$1<a class="landing-module__ACF0Ka__navItem" href="/storyboard">分镜</a>');
 html=html.replace(/(<a\b[^>]*class="[^"]*navSecondary[^"]*"[^>]*href=")\/login("[^>]*>)/g,'$1/series$2');
 html=html.replace(/(<a\b[^>]*class="[^"]*loginEntry[^"]*"[^>]*href=")\/login("[^>]*>)登录<\/a>/g,'$1/series$2本地演示</a>');
 html=html.replaceAll('href="/login"','href="/storyboard?new=1"');
 html=html.replace(/(<a\b[^>]*class="[^"]*campaignCard[^"]*"[^>]*href=")\/storyboard\?new=1("[^>]*>)/g,'$1https://app.momostudio.top/login$2');
 html=html.replaceAll('href="/login?callbackUrl=%2Fpricing"','href="https://app.momostudio.top/pricing" target="_blank" rel="noopener" data-official-pricing="true"');
 for(const policy of ['terms','privacy','refund-policy','delivery-policy','legal'])html=html.replaceAll(`href="/${policy}"`,`href="${origin}/${policy}" target="_blank" rel="noopener"`);
 html=html.replaceAll('cover-video-module__vXrvbq__pending','');
 html=html.replace('</head>','<link rel="stylesheet" href="/media/site/local.css"></head>');
 html=html.replace('</body>','<script src="/media/site/local.js" defer></script></body>');
 await fs.writeFile(path.join(out,name+'.html'),html);
 console.log(name+' generated');
}
await fs.writeFile(path.join(out,'asset-manifest.json'),JSON.stringify({source:origin,evidence_id:evidence.data.evidence_id,assets:Object.fromEntries(assets),failures},null,2));
console.log(JSON.stringify({assets:assets.size,failures}));

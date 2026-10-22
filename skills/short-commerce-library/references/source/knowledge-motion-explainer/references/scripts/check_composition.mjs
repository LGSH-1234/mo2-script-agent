
#!/usr/bin/env node
// 检查已启动的本地合成页面；不安装依赖、不启动渲染、不修改项目。
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import {createRequire} from 'node:module';

const help = `Usage:
  node check_composition.mjs --url http://127.0.0.1:3000/ \\
    --browser-module /absolute/path/to/puppeteer-core \\
    --executable /absolute/path/to/chromium --output runtime-check.json

Required: --url, --browser-module (已安装 puppeteer/puppeteer-core/playwright 模块路径), --executable
Optional: --composition ID, --fps N, --duration N, --timeout-ms N (默认 30000),
          --pixel-check, --times 0,1.5,8 (附加像素检查时间), --output FILE
          --layout-check, --layout-inset-ratio N (默认 .04), --layout-gap N (逻辑px；默认 12*H/1080)

逐帧 seek 使用 window.__timelines[compositionId].seek(t, true)。检查全部帧的
同步异常、pageerror、资源加载失败以及时间轴定位；samples=0 不能通过。
--pixel-check 额外比较关键帧顺序/逆序/打乱 seek 后的 PNG hash；精确差异会报错，
需要检查是否有状态残留或浏览器栅格差异，不自动降低门槛。
--layout-check 每帧测量可见DOM/SVG文字及LayoutAudit.fillText包装的Canvas文字；
越界、裁剪、保守AABB碰撞或测量缺口都导致失败。碰撞需人工复核，不自动改布局。
这不验证科学事实、美观、音频同步或最终 MP4 的实际字幕；这些仍需单独检查。
Exit: 0 passed, 1 failed, 2 capability/input unavailable. 不会自动安装任何依赖。
`;
let args = {};
const report = {ok:false, status:'not_run', samples:0, frameErrors:[], frameErrorCount:0,
  pageErrors:[], resourceErrors:[], pixelChecks:[], scope:'Full timeline runtime execution; optional deterministic pixel checks. Not an aesthetic, speech, caption coverage, or final MP4 verdict.'};
let browser;
let exitCode=2;
function safeURL(value){try{const u=new URL(value);return `${u.origin}${u.pathname}`}catch{return String(value).split('?')[0]}}
function fail(message){throw new Error(message)}
function numberArg(name, fallback){const n=args[name]===undefined?fallback:Number(args[name]);if(!Number.isFinite(n)||n<=0)fail(`Invalid --${name}`);return n}
try {
  for(let i=2;i<process.argv.length;i++){
    const k=process.argv[i];
    if(k==='--help'||k==='-h'){console.log(help);process.exit(0)}
    if(k==='--pixel-check'||k==='--layout-check'){args[k.slice(2)]=true;continue}
    if(!['--url','--browser-module','--executable','--composition','--fps','--duration','--timeout-ms','--times','--output','--layout-inset-ratio','--layout-gap'].includes(k))fail(`Unknown argument ${k}`);
    if(!process.argv[i+1]||process.argv[i+1].startsWith('--'))fail(`Missing value for ${k}`);
    args[k.slice(2)]=process.argv[++i];
  }
  for(const k of ['url','browser-module','executable'])if(!args[k])fail(`Required --${k}; use --help`);
  const url=new URL(args.url);
  if(!['http:','https:'].includes(url.protocol)||!['localhost','127.0.0.1','[::1]'].includes(url.hostname))fail('--url must be a started local HTTP(S) project URL');
  if(!path.isAbsolute(args['browser-module'])||!path.isAbsolute(args.executable))fail('Browser module and executable paths must be absolute');
  if(!fs.existsSync(args.executable))fail('Browser executable not found');
  const timeout=numberArg('timeout-ms',30000);
  let api;
  try{api=createRequire(import.meta.url)(args['browser-module'])}catch(e){fail(`Browser module unavailable: ${e.code||e.message}. Use an installed module; do not treat this as a successful check.`)}
  api=api.default||api;
  const playwright=Boolean(api.chromium?.launch);
  const launcher=playwright?api.chromium:api;
  if(typeof launcher.launch!=='function')fail('Module must expose Puppeteer launch or Playwright chromium.launch');
  browser=await launcher.launch({headless:true,executablePath:args.executable,args:['--no-sandbox']});
  const page=await browser.newPage();
  if(args['layout-check']){
    const content=fs.readFileSync(new URL('./layout_audit.js',import.meta.url),'utf8');
    if(playwright)await page.addInitScript({content});else await page.evaluateOnNewDocument(content);
  }
  const seenResource=new Set();
  function resourceError(kind, address, detail){const item={kind,url:safeURL(address),detail};const key=JSON.stringify(item);if(!seenResource.has(key)){seenResource.add(key);report.resourceErrors.push(item)}}
  page.on('pageerror',e=>report.pageErrors.push({message:e.message}));
  page.on('requestfailed',r=>resourceError('request_failed',r.url(),r.failure()?.errorText||'request failed'));
  page.on('response',r=>{if(r.status()>=400)resourceError('http_status',r.url(),String(r.status()))});
  const waitFor=fn=>playwright?page.waitForFunction(fn,null,{timeout}):page.waitForFunction(fn,{timeout});
  await page.goto(args.url,{waitUntil:'load',timeout});
  const composition=await page.evaluate(id=>{
    const roots=[...document.querySelectorAll('[data-composition-id]')];
    const root=id?roots.find(e=>e.dataset.compositionId===id):roots[0];
    if(!root)throw new Error('No matching data-composition-id root');
    if(!id&&roots.length!==1)throw new Error('Multiple compositions: pass --composition');
    return {id:root.dataset.compositionId,width:Number(root.dataset.width),height:Number(root.dataset.height),duration:Number(root.dataset.duration),fps:Number(root.dataset.fps)};
  },args.composition||null);
  const width=composition.width,height=composition.height;
  if(!Number.isInteger(width)||!Number.isInteger(height)||width<1||height<1)fail('Composition must declare valid data-width and data-height');
  if(playwright)await page.setViewportSize({width,height});else await page.setViewport({width,height,deviceScaleFactor:1});
  await page.evaluate(async timeout=>{
    let timer;
    try{await Promise.race([
      (async()=>{
        await document.fonts.ready;
        const fontErrors=[...document.fonts].filter(f=>f.status==='error');
        if(fontErrors.length)throw new Error(`Font loading failed: ${fontErrors.map(f=>f.family).join(', ')}`);
        await Promise.all([...document.images].map(async img=>{
          if(!img.complete)await new Promise((resolve,reject)=>{img.addEventListener('load',resolve,{once:true});img.addEventListener('error',()=>reject(new Error('Image load failed')),{once:true})});
          if(!img.naturalWidth)throw new Error('Image has no decoded pixels');
          if(img.decode)await img.decode();
        }));
      })(),
      new Promise((_,reject)=>{timer=setTimeout(()=>reject(new Error('Fonts/images readiness timeout')),timeout)})
    ])}finally{clearTimeout(timer)}
  },timeout);
  await page.evaluate(id=>{window.__compositionCheckId=id},composition.id);
  await waitFor(()=>Boolean(window.__timelines?.[window.__compositionCheckId]?.seek));
  const fps=numberArg('fps',composition.fps),duration=numberArg('duration',composition.duration);
  const totalFrames=Math.ceil(duration*fps);
  if(!Number.isSafeInteger(totalFrames)||totalFrames<1||totalFrames>500000)fail('Invalid or excessive frame count');
  const timelineDuration=await page.evaluate(id=>window.__timelines[id].duration(),composition.id);
  if(timelineDuration+1/fps<duration)fail(`Timeline (${timelineDuration}s) is shorter than declared duration (${duration}s)`);
  report.composition={...composition,fps,duration,totalFrames,timelineDuration};
  const layoutConfig={width,height,insetRatio:Number(args['layout-inset-ratio']??.04),gap:Number(args['layout-gap']??12*height/1080)};
  if(!Number.isFinite(layoutConfig.insetRatio)||layoutConfig.insetRatio<0||layoutConfig.insetRatio>.25||!Number.isFinite(layoutConfig.gap)||layoutConfig.gap<0)fail('Invalid layout inset ratio (0..0.25) or gap (>=0)');
  const layoutIssues=new Map();
  if(args['layout-check'])report.layout={ok:false,samples:0,config:layoutConfig,issueCount:0,issues:[],measuredExamples:[],
    coverage:{textFrames:0,domBoxes:0,svgBoxes:0,canvasBoxes:0,visibleCanvases:0,trackedCanvases:0},
    scope:'Measured text geometry only; conservative AABBs. Does not cover final burned captions, image-contained text, artwork occlusion or aesthetics.'};
  report.status='running';exitCode=1;
  for(let first=0;first<totalFrames;first+=100){
    const batch=await page.evaluate(({id,first,last,fps,layoutConfig,layoutEnabled})=>{
      const tl=window.__timelines[id];let errors=[],layouts=[];
      const root=[...document.querySelectorAll('[data-composition-id]')].find(e=>e.dataset.compositionId===id);
      for(let frame=first;frame<last;frame++){
        const t=frame/fps;
        try{
          if(layoutEnabled)window.LayoutAudit.beginFrame();
          tl.seek(t,true);if(Math.abs(tl.time()-t)>1e-5)throw new Error(`Timeline did not reach requested time: ${tl.time()}`);
          if(layoutEnabled)layouts.push({frame,time:t,...window.LayoutAudit.collect(root,layoutConfig)});
        }
        catch(e){errors.push({frame,time:t,name:e.name,message:e.message})}
      }
      return {samples:last-first,errors,layouts};
    },{id:composition.id,first,last:Math.min(first+100,totalFrames),fps,layoutConfig,layoutEnabled:!!args['layout-check']});
    report.samples+=batch.samples;report.frameErrorCount+=batch.errors.length;
    report.frameErrors.push(...batch.errors.slice(0,Math.max(0,50-report.frameErrors.length)));
    for(const sample of batch.layouts){
      const layout=report.layout;layout.samples++;
      if(sample.boxes.length)layout.coverage.textFrames++;
      for(const key of Object.keys(sample.coverage))layout.coverage[key]+=sample.coverage[key];
      if(layout.measuredExamples.length<12&&sample.boxes.length)layout.measuredExamples.push({frame:sample.frame,time:sample.time,boxes:sample.boxes.slice(0,20)});
      for(const item of sample.issues){
        layout.issueCount++;
        const key=JSON.stringify([item.type,item.ids,item.detail]);
        let aggregate=layoutIssues.get(key);
        if(!aggregate){aggregate={...item,firstTime:sample.time,lastTime:sample.time,count:0,examples:[]};layoutIssues.set(key,aggregate);}
        aggregate.lastTime=sample.time;aggregate.lastText=item.text;aggregate.count++;
        if(aggregate.examples.length<3)aggregate.examples.push({frame:sample.frame,time:sample.time,text:item.text,boxes:item.boxes});
      }
    }
  }
  // 让已排队的页面错误/重绘到达；不使用猜测的固定等待时长。
  await page.evaluate(()=>new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve))));
  if(args['pixel-check']){
    const supplied=args.times?args.times.split(',').map(Number):[];
    if(supplied.some(t=>!Number.isFinite(t)||t<0||t>=duration))fail('--times must be within [0, duration)');
    const times=[...new Set([0,duration*.25,duration*.5,duration*.75,(totalFrames-1)/fps,...supplied])].sort((a,b)=>a-b);
    const sample=async time=>{
      await page.evaluate(({id,time})=>{window.__timelines[id].seek(time,true)}, {id:composition.id,time});
      await page.evaluate(()=>new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve))));
      return crypto.createHash('sha256').update(await page.screenshot({type:'png'})).digest('hex');
    };
    const hashes=new Map();for(const t of times)hashes.set(t,await sample(t));
    const shuffled=[...times.filter((_,i)=>i%2===1),...times.filter((_,i)=>i%2===0)];
    for(const [order,sequence] of [['reverse',[...times].reverse()],['shuffled',shuffled]]){
      for(const time of sequence){const actual=await sample(time);report.pixelChecks.push({order,time,ok:actual===hashes.get(time),expectedHash:hashes.get(time),actualHash:actual})}
    }
  }
  if(report.layout){
    if(!report.layout.coverage.textFrames)layoutIssues.set('no_text_measured',{type:'no_text_measured',ids:[],text:[],boxes:[],firstTime:0,lastTime:(totalFrames-1)/fps,count:totalFrames,detail:'No visible text was measured; this is not proof of safe text layout.',examples:[]});
    report.layout.issues=[...layoutIssues.values()];
    report.layout.ok=report.layout.samples===totalFrames&&report.layout.coverage.textFrames>0&&report.layout.issues.length===0;
  }
  report.ok=report.samples===totalFrames&&report.samples>0&&report.frameErrorCount===0&&report.pageErrors.length===0&&report.resourceErrors.length===0&&report.pixelChecks.every(x=>x.ok)&&(!report.layout||report.layout.ok);
  report.status=report.ok?'passed':'failed';exitCode=report.ok?0:1;
}catch(e){report.error=e.message;report.status=report.samples?'failed':'unavailable';report.ok=false;if(report.samples)exitCode=1}
finally{
  if(browser)await browser.close();
  const output=JSON.stringify(report,null,2)+'\n';
  if(args.output){fs.mkdirSync(path.dirname(path.resolve(args.output)),{recursive:true});fs.writeFileSync(args.output,output)}
  process.stdout.write(output);process.exitCode=exitCode;
}
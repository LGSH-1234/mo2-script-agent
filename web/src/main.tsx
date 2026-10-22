import React, {useEffect, useState} from 'react';
import {createRoot} from 'react-dom/client';
import {ArrowUp, ArrowRight, Plus, Check, Film, FileText, LayoutList, Play, ChevronRight, X, History, Download, Sparkles, LoaderCircle, Scissors, Merge, Trash2, ArrowDown, Settings2, ImagePlus, RotateCcw, Folder, Clapperboard, PanelRightClose} from 'lucide-react';
import type {Project, Shot, Script, Job, Proposal, Health} from './types';
import './style.css';
import {SiteHeader} from './SiteHeader';
import {ProjectsPage} from './ProjectsPage';
import {ScriptImports} from './ScriptImports';
import './site.css';

async function api<T>(path:string, method='GET', body?:unknown):Promise<T>{
 const res=await fetch('/api'+path,{method,headers:body?{'Content-Type':'application/json'}:undefined,body:body?JSON.stringify(body):undefined});
 if(!res.ok){const error=await res.json().catch(()=>({detail:'请求失败'}));throw new Error(typeof error.detail==='string'?error.detail:'请检查输入字段，内容尚未保存。')}
 return res.json();
}
async function apiForm<T>(path:string, form:FormData):Promise<T>{
 const res=await fetch('/api'+path,{method:'POST',body:form});
 if(!res.ok){const error=await res.json().catch(()=>({detail:'请求失败'}));throw new Error(typeof error.detail==='string'?error.detail:'请检查输入字段，内容尚未保存。')}
 return res.json();
}
const exampleBrief='雨夜，一位年轻摄影师来到即将关闭的老照相馆。老人递给她一封母亲留下的信。她打开信，发现一张童年合照，最后回头看向门口。30 秒，克制温暖，无旁白。';
const label:Record<string,string>={queued:'排队中',running:'生成中',succeeded:'已完成',failed:'失败'};
const fields:[keyof Shot,string][]=[['title','镜头名称'],['framing','景别'],['camera','运镜'],['duration','时长（秒）'],['action','画面内容'],['dialogue','对白 / 声音'],['start_state','起始状态'],['end_state','结束状态'],['prompt','视频提示词']];

function App(){
 const [scriptFiles,setScriptFiles]=useState<File[]>([]); const [importSkipped,setImportSkipped]=useState(false);
 const [health,setHealth]=useState<Health>(); const [projects,setProjects]=useState<Project[]>([]); const [p,setP]=useState<Project|null>(null);
 const [tab,setTab]=useState('script'); const [brief,setBrief]=useState(''); const [ratio,setRatio]=useState('16:9'); const [duration,setDuration]=useState(30);
 const [busy,setBusy]=useState(''); const [error,setError]=useState(''); const [notice,setNotice]=useState(''); const [selected,setSelected]=useState<string|null>(null);
 const [edit,setEdit]=useState<Shot|null>(null); const [scriptEdit,setScriptEdit]=useState<Script|null>(null); const [chat,setChat]=useState('');
 const [messages,setMessages]=useState<{role:string;text:string}[]>([]); const [proposal,setProposal]=useState<Proposal|null>(null);
 const [jobs,setJobs]=useState<Job[]>([]); const [modal,setModal]=useState<string|null>(null); const [history,setHistory]=useState<Project[]>([]);
 const [videoShot,setVideoShot]=useState<Shot|null>(null); const [fail,setFail]=useState(false); const [viewVersion,setViewVersion]=useState<Project|null>(null);
 const [stepOverride,setStepOverride]=useState<number|null>(null);
 const shown=viewVersion||p; const approved=!!p&&p.approved_version===p.version; const shownApproved=!!shown&&shown.approved_version===shown.version; const shot=p?.shots.find(s=>s.id===selected);
 const dirty=!!(edit&&shot&&JSON.stringify(edit)!==JSON.stringify(shot));
 const stages=['拆解分镜','确认版本','生成视频'] as const;
 const autoStage=!p||!p.shots.length?0:!approved?0:jobs.some(j=>j.version===p.version)?2:1;
 const stageIndex=stepOverride===null?autoStage:Math.min(stepOverride,autoStage);
 function goBackStep(){
  if(tab==='results'){setSelected(null);setTab('board');setStepOverride(approved?1:0);return}
  if(tab==='board'){setSelected(null);setTab('script');setStepOverride(0);return}
 }
 async function refreshList(){setProjects(await api<Project[]>('/projects'))}
 function adopt(next:Project){if(p&&p.id!==next.id)setScriptFiles([]);setP(next);setViewVersion(null);localStorage.setItem('mo2-project',next.id);window.history.replaceState({},'',storyboardUrl({project:next.id}));void refreshList()}
 async function work(name:string,fn:()=>Promise<void>){setBusy(name);setError('');try{await fn()}catch(e){setError((e as Error).message)}finally{setBusy('')}}
 useEffect(()=>{
  const restore=()=>void work('载入项目',async()=>{
   setHealth(await api('/health'));const list=await api<Project[]>('/projects');setProjects(list);
   const query=new URLSearchParams(window.location.search), requested=query.get('project');
   const id=query.get('new')==='1'?null:requested||localStorage.getItem('mo2-project');
   const last=list.find(x=>x.id===id);
   setSelected(null);setProposal(null);setViewVersion(null);setMessages([]);setJobs([]);setModal(null);setScriptFiles([]);
   if(last){setP(last);setTab(last.shots.length?'board':'script');localStorage.setItem('mo2-project',last.id);window.history.replaceState({},'',storyboardUrl({project:last.id}))}
   else{setP(null);setBrief(query.get('brief')?.slice(0,8000)||'');setTab('script');if(requested)throw new Error('这个项目不存在或已被移除。请前往「我的项目」选择项目，或新建一个故事。');if(query.get('new')==='1')localStorage.removeItem('mo2-project')}
  });
  restore();window.addEventListener('popstate',restore);return()=>window.removeEventListener('popstate',restore)
 },[]);
 useEffect(()=>{if(!p)return;let alive=true;const load=()=>api<Job[]>(`/projects/${p.id}/jobs`).then(j=>{if(alive)setJobs(j)}).catch(()=>{});void load();const timer=setInterval(load,1500);return()=>{alive=false;clearInterval(timer)}},[p?.id]);
 useEffect(()=>{setEdit(shot?structuredClone(shot):null)},[shot]);
 useEffect(()=>{setScriptEdit(p?.script?structuredClone(p.script):null)},[p?.script]);
 useEffect(()=>{if(!notice)return;const t=setTimeout(()=>setNotice(''),3500);return()=>clearTimeout(t)},[notice]);
 function reset(){setImportSkipped(false);setStepOverride(null);setP(null);setSelected(null);setProposal(null);setViewVersion(null);setMessages([]);setBrief('');setTab('script');setJobs([]);setError('');setModal(null);setScriptFiles([]);localStorage.removeItem('mo2-project');window.history.pushState({},'',storyboardUrl({new:'1'}))}
 async function saveShots(shots:Shot[]){if(!p)return;adopt(await api<Project>(`/projects/${p.id}/board`,'PUT',{version:p.version,shots}));setProposal(null);setNotice('已保存新版本，请重新确认分镜表')}
 async function createAndWrite(){await work('正在编写脚本',async()=>{const created=await api<Project>('/projects','POST',{title:brief.slice(0,16)||'新项目',brief,duration,ratio});adopt(created);setTab('script');const result=await api<Project>(`/projects/${created.id}/script/generate`,'POST',{version:created.version});adopt(result);setMessages([{role:'agent',text:'脚本已生成。你可以直接编辑，准备好后点击「拆解分镜」。'}])})}
 async function createFromScript(){await work('正在读取脚本文件',async()=>{
  if(!scriptFiles.length)throw new Error('请先导入脚本文件');
  const form=new FormData();form.append('duration',String(duration));form.append('ratio',ratio);form.append('notes',brief);for(const file of scriptFiles)form.append('files',file);
  const imported=await apiForm<Project>('/projects/from-script',form);adopt(imported);setScriptFiles([]);setImportSkipped(true);setStepOverride(null);setTab('board');setSelected(null);
  setBusy('正在按原文生成分镜');
  const result=await api<Project>(`/projects/${imported.id}/board/generate`,'POST',{version:imported.version});adopt(result);
  setNotice('已跳过脚本编写，直接生成分镜');setMessages([{role:'agent',text:`已跳过「写脚本」：按导入稿直接生成 ${result.shots.length} 个镜头。可编辑分镜；回看或改中间稿请切到「脚本」页。`}]);
 })}
 async function startFromWelcome(){if(!scriptFiles.length){setError('请先导入脚本文件');return}return createFromScript()}
 async function loadExample(){await work('载入演示案例',async()=>{adopt(await api<Project>('/examples','POST'));setScriptFiles([]);setTab('board');setSelected(null);setMessages([{role:'agent',text:'已载入「雨夜来信」预置案例：2 场戏、6 个镜头。可以编辑分镜、确认版本，再体验单镜视频模拟。'}])})}
 async function revise(){if(!p||!chat.trim())return;const match=chat.match(/第\s*(\d+)\s*镜/);const target=match?p.shots[Number(match[1])-1]:shot;if(!target){setError('请选择一个镜头，或在指令中指定“第 2 镜”。');return}const instruction=chat;setChat('');setMessages(m=>[...m,{role:'user',text:instruction}]);await work('正在生成修改建议',async()=>{setSelected(target.id);const result=await api<Proposal>(`/projects/${p.id}/revisions`,'POST',{version:p.version,shot_id:target.id,instruction});setProposal(result);setMessages(m=>[...m,{role:'agent',text:`「${target.title}」的修改建议已准备好。查看差异后应用，其他镜头保持不变。`}])})}
 async function action(kind:string){if(!p||!shot)return;const rows=structuredClone(p.shots),i=rows.findIndex(s=>s.id===shot.id);if(kind==='delete'){if(rows.length===1){setError('至少保留一个镜头');return}rows.splice(i,1);setSelected(null)}
 if(kind==='up'&&i>0)[rows[i-1],rows[i]]=[rows[i],rows[i-1]];
 if(kind==='down'&&i<rows.length-1)[rows[i+1],rows[i]]=[rows[i],rows[i+1]];
 if(kind==='split'){if(shot.duration<2){setError('拆分前镜头时长至少为 2 秒');return}const a={...shot,duration:shot.duration/2,title:shot.title+' · A',prompt:''};const b={...shot,id:crypto.randomUUID(),duration:shot.duration/2,title:shot.title+' · B',prompt:''};rows.splice(i,1,a,b)}
 if(kind==='merge'){if(i===rows.length-1){setError('请选择非最后一个镜头，与下一镜合并');return}const next=rows[i+1];if(next.source_scene!==shot.source_scene){setError('仅支持合并同一场景的相邻镜头');return}if(shot.duration+next.duration>30){setError('合并后时长不能超过 30 秒');return}rows.splice(i,2,{...shot,title:shot.title+' / '+next.title,duration:shot.duration+next.duration,action:shot.action+' '+next.action,dialogue:[shot.dialogue,next.dialogue].filter(Boolean).join('\n'),end_state:next.end_state,prompt:'',reference_ids:[...new Set([...shot.reference_ids,...next.reference_ids])]})}
 await work('保存镜头',()=>saveShots(rows))}
 function latest(s:Shot){return jobs.find(j=>j.shot_id===s.id&&j.version===shown?.version)}
 function download(format:string){if(p){const anchor=document.createElement('a');anchor.href=`/api/projects/${p.id}/export?format=${format}`;anchor.download=`storyboard.${format}`;document.body.appendChild(anchor);anchor.click();anchor.remove()}}

 return <div className="app">
  <nav className="rail"><button className="logo" onClick={reset} aria-label="MO² 首页"><img src="/mo2-logo.svg"/></button><button className="rail-active" aria-label="脚本分镜 Agent"><Clapperboard/></button><button onClick={()=>setModal('projects')} aria-label="项目列表"><Folder/></button><div className="rail-bottom"><span className="avatar">导</span><span className="vertical-label">LOCAL DEMO</span></div></nav>
  <div className="shell"><header><div className="breadcrumb"><span>创作空间</span><ChevronRight size={14}/><strong>脚本分镜 Agent</strong>{p&&<><ChevronRight size={14}/><span>{p.title}</span></>}</div><div className="header-right"><span className={'status-dot '+(health?.model_configured?'on':'')}/><button className="text-button" onClick={()=>setModal('model')}>{health?.model||'DeepSeek'} · {health?.model_configured?'已配置':'待配置'}</button><span className="pill">本地演示</span><button className="icon-button" onClick={reset} aria-label="新建项目"><Plus size={18}/></button></div></header>
  {p&&<div className="stagebar"><div className="stagebar-steps">{stages.map((x,i)=><React.Fragment key={x}><div className={'step '+(i===stageIndex?'current':i<stageIndex?'done':'')}><span>{i<stageIndex?<Check size={12}/>:i+1}</span>{x}</div>{i<stages.length-1&&<div className="step-line"/>}</React.Fragment>)}</div></div>}
  {error&&<div className="error" role="alert">{error}<button onClick={()=>setError('')} aria-label="关闭提示"><X size={15}/></button></div>}
  {notice&&<div className="toast" role="status"><Check size={16}/>{notice}</div>}
  {p?.imported_files?.length&&!p.shots.length?<div className="version-banner"><span>{busy?'正在根据导入原文生成分镜…':'导入原文已保存，可以继续生成分镜。'}</span><button disabled={!!busy} onClick={()=>void work('正在生成分镜',async()=>{adopt(await api<Project>(`/projects/${p.id}/board/generate`,'POST',{version:p.version}));setTab('board')})}>生成分镜</button></div>:null}
  {p&&scriptFiles.length>0&&<div className="workspace-imports"><ScriptImports files={scriptFiles} onChange={setScriptFiles} disabled={!!busy} compact/></div>}
  {!p?<main className="welcome">
   <div className="eyebrow"><span/> FROM SCRIPT TO SHOTS</div>
   <h1>导入已有脚本，<br/><em>直接生成分镜。</em></h1>
   <p className="intro">本阶段只走导入路径：上传 Word / TXT 等脚本 → 开始写分镜 → 直接进入分镜表。</p>
   <ScriptImports files={scriptFiles} onChange={setScriptFiles} disabled={!!busy}/>
   <div className="brief-box">
    <textarea aria-label="补充要求（可选）" placeholder="补充风格、节奏等要求（可选），留空即可按上传脚本生成分镜…" value={brief} onChange={e=>setBrief(e.target.value)}/>
    <div className="brief-bottom">
     <label>时长<select aria-label="目标时长" value={duration} onChange={e=>setDuration(Number(e.target.value))}>{[15,30,60,90,120].map(n=><option key={n} value={n}>{n} 秒</option>)}</select></label>
     <label>画幅<select aria-label="画幅" value={ratio} onChange={e=>setRatio(e.target.value)}>{['16:9','9:16','1:1'].map(r=><option key={r}>{r}</option>)}</select></label>
     <button className="primary" disabled={!scriptFiles.length||!!busy} onClick={()=>void startFromWelcome()}>{busy?<LoaderCircle className="spin" size={16}/>:<Sparkles size={16}/>}开始写分镜<ArrowRight size={16}/></button>
    </div>
   </div>
   <footer>导入脚本 <span>／</span> 直接分镜 <span>／</span> 确认后再生成</footer>
  </main>:<div className="workspace">
   <aside className="agent"><div className="agent-title"><span className="agent-symbol"><Sparkles size={19}/></span><div><strong>你的分镜搭档</strong><small>想法、修改，都从这里开始</small></div></div><div className="conversation"><div className="message user"><span>导演输入</span><p>{p.brief}</p></div><div className="message agent-message"><span><Sparkles size={12}/> Agent</span><p>{p.shots.length?`已整理为 ${p.shots.length} 个镜头，总时长 ${p.shots.reduce((n,s)=>n+s.duration,0)} 秒。点击分镜行查看详情，或告诉我想修改哪一镜。`:'先完成脚本，再进入分镜。你可以直接编辑脚本内容。'}</p><div className="mini-progress"><Check size={13}/>{p.script?'脚本已就绪':'等待脚本生成'}<span>{p.shots.length?`${p.shots.length} 镜`:'准备中'}</span></div></div>{p.origin==='preset'&&<div className="sample-note">当前内容来自预置案例。对话修改使用真实 DeepSeek。</div>}{messages.map((m,i)=><div key={i} className={'message '+(m.role==='user'?'user':'agent-message')}><span>{m.role==='user'?'你':'Agent'}</span><p>{m.text}</p></div>)}{busy&&<div className="thinking"><LoaderCircle size={14} className="spin"/>{busy}</div>}</div><div className="chat-compose">{selected&&<div className="selection-chip">正在修改 · 第 {(p.shots.findIndex(s=>s.id===selected)+1).toString().padStart(2,'0')} 镜<button onClick={()=>setSelected(null)} aria-label="取消镜头选择"><X size={12}/></button></div>}<textarea aria-label="修改指令" value={chat} onChange={e=>setChat(e.target.value)} placeholder="例如：只改第 2 镜，让递信的动作更迟疑" onKeyDown={e=>{if(e.key==='Enter'&&(e.metaKey||e.ctrlKey))void revise()}}/><div><span>先看差异，再应用</span><button className="send" onClick={revise} disabled={!chat.trim()||!!busy||!p.shots.length} aria-label="发送修改指令"><ArrowUp size={18}/></button></div></div></aside>
   <main className="work"><div className="work-heading"><div><div className="eyebrow">PROJECT / {p.id.slice(-6).toUpperCase()}</div><h2>{shown?.script?.title||p.title}<span className="version">V{shown?.version}</span></h2></div><div className="heading-actions"><button className="icon-button" aria-label="版本历史" onClick={()=>void work('读取版本',async()=>{setHistory(await api(`/projects/${p.id}/versions`));setModal('history')})}><History size={18}/></button><button className="secondary compact" onClick={()=>download('csv')} disabled={!p.shots.length||!!viewVersion}><Download size={15}/>导出</button></div></div>
   <div className="tabs"><button className={tab==='script'?'active':''} onClick={()=>{setTab('script');setSelected(null)}}><FileText size={16}/>脚本</button><button className={tab==='board'?'active':''} onClick={()=>{setTab('board');if(approved)setStepOverride(1);else setStepOverride(0)}}><LayoutList size={16}/>分镜表 <small>{shown?.shots.length||0}</small></button><button className={tab==='results'?'active':''} onClick={()=>{setTab('results');setSelected(null);setStepOverride(null)}}><Film size={16}/>视频结果 <small>{jobs.filter(j=>j.status==='succeeded').length}</small></button><div className="tab-spacer"/><span className="subtle">{p.ratio} <b>·</b> {p.duration}s 目标</span></div>
   {importSkipped&&!viewVersion&&<div className="version-banner import-skip-banner" role="status">已跳过脚本编写，直接生成分镜<button type="button" onClick={()=>{setTab('script');setSelected(null)}}>查看 / 改脚本</button><button type="button" className="banner-dismiss" aria-label="关闭提示" onClick={()=>setImportSkipped(false)}><X size={14}/></button></div>}{viewVersion&&<div className="version-banner">查看历史 V{viewVersion.version} · 只读<button onClick={()=>setViewVersion(null)}>返回当前版本</button></div>}
   {tab==='script'&&<div className="script-pane">{!p.script?<div className="empty-state"><FileText size={34}/><h3>让想法成为脚本</h3><p>{p.brief}</p><button className="primary" disabled={!!busy} onClick={()=>void work('正在编写脚本',async()=>adopt(await api(`/projects/${p.id}/script/generate`,'POST',{version:p.version})))}>生成脚本<ArrowRight size={16}/></button></div>:<><div className="script-toolbar"><span>{shown?.script?.scenes.length} 场戏 · {p.origin==='preset'?'预置示例':'创作草稿'}</span>{!viewVersion&&<div><button className="secondary" disabled={!!busy||JSON.stringify(scriptEdit)===JSON.stringify(p.script)} onClick={()=>void work('保存脚本',async()=>{adopt(await api(`/projects/${p.id}/script`,'PUT',{version:p.version,script:scriptEdit}));setNotice('脚本已更新，请重新拆解分镜')} )}>保存脚本</button><button className="primary" disabled={!!busy||JSON.stringify(scriptEdit)!==JSON.stringify(p.script)} onClick={()=>void work('正在拆解分镜与提示词',async()=>{adopt(await api(`/projects/${p.id}/board/generate`,'POST',{version:p.version}));setTab('board')})}>拆解分镜<ArrowRight size={16}/></button></div>}</div><div className="script-document"><span className="eyebrow">SCREENPLAY</span><h2>{shown?.script?.title}</h2><p className="synopsis">{shown?.script?.synopsis}</p>{(viewVersion?.script||scriptEdit)?.scenes.map((s,i)=><section key={s.id}><div className="scene-title"><span>{s.id}</span><h3>{s.location}</h3></div><label>动作<textarea disabled={!!viewVersion} aria-label={`${s.id} 动作`} value={s.action} onChange={e=>setScriptEdit(old=>old?{...old,scenes:old.scenes.map((x,j)=>j===i?{...x,action:e.target.value}:x)}:old)}/></label><label>对白<textarea disabled={!!viewVersion} aria-label={`${s.id} 对白`} value={s.dialogue} placeholder="无对白" onChange={e=>setScriptEdit(old=>old?{...old,scenes:old.scenes.map((x,j)=>j===i?{...x,dialogue:e.target.value}:x)}:old)}/></label></section>)}<div className="document-end">END OF SCRIPT</div></div></>}</div>}
   {tab==='board'&&<div className="board-pane">{!shown?.shots.length?<div className="empty-state"><LayoutList size={34}/><h3>分镜从脚本开始</h3><p>先在脚本页完成内容，再拆解为镜头。</p><button className="secondary" onClick={()=>setTab('script')}>查看脚本</button></div>:<><div className="board-toolbar"><div><span className={'approval '+(shownApproved?'approved':'')}>{shownApproved?<Check size={13}/>:<span className="dot"/>}{shownApproved?`V${shown?.version} 已确认`:'等待确认'}</span><span className="subtle">{shown.shots.length} 镜 <b>·</b> {shown.shots.reduce((n,s)=>n+s.duration,0)} 秒</span></div>{!viewVersion&&<div className="toolbar-actions">{tab==='board'&&<button type="button" className="secondary compact" disabled={!!busy} onClick={goBackStep}>返回</button>}<button className={approved?'secondary compact':'primary compact'} disabled={!!busy||approved||dirty} onClick={()=>setModal('approve')}>{approved?<Check size={15}/>:null}{approved?'已确认此版':'确认此版分镜表'}</button></div>}</div><div className="table-scroll"><table><thead><tr><th>镜号</th><th>镜头 / 画面内容</th><th>景别 · 运镜</th><th>时长</th><th>状态</th></tr></thead><tbody>{shown.shots.map((s,i)=>{const job=latest(s);return <tr key={s.id} className={selected===s.id?'selected':''} onClick={()=>{if(dirty){setError('请先保存或取消当前镜头修改');return}if(!viewVersion)setSelected(s.id)}} tabIndex={0} onKeyDown={e=>{if(e.key==='Enter'&&!viewVersion&&!dirty)setSelected(s.id)}} aria-label={`第 ${i+1} 镜 ${s.title}`}><td><span className="shot-number">{String(i+1).padStart(2,'0')}</span></td><td><strong>{s.title}</strong><p>{s.action}</p><small>{s.source_scene} · {s.dialogue?'有对白':'无对白'}</small></td><td><span>{s.framing}</span><small>{s.camera}</small></td><td className="duration">{s.duration}<small>s</small></td><td><span className={'job-label '+(job?.status||'')}>{job?label[job.status]:!s.prompt?'待补提示词':shownApproved?'可生成':'待确认'}</span><ChevronRight size={14}/></td></tr>})}</tbody></table></div>{!viewVersion&&<button className="add-shot" disabled={!!busy||dirty} onClick={()=>void work('新增镜头',async()=>{const id=crypto.randomUUID();await saveShots([...p.shots,{id,source_scene:p.script!.scenes[0].id,title:'新镜头',framing:'中景',camera:'固定',duration:5,action:'请填写画面内容',dialogue:'',start_state:'请填写起始状态',end_state:'请填写结束状态',prompt:'',reference_ids:[]}]);setSelected(id)})}><Plus size={15}/>增加镜头</button>}<div className="board-footnote"><span>每一镜都可以独立修改。</span><span>确认只锁定版本，不会自动生成视频。</span></div></>}</div>}
   {tab==='results'&&<div className="results-pane"><div className="results-head"><h3>镜头视频</h3><div className="toolbar-actions"><button type="button" className="secondary compact" disabled={!!busy} onClick={goBackStep}>返回</button><span className="pill">视频模拟 · 不产生费用</span></div></div>{!jobs.length?<div className="empty-state"><Film size={34}/><h3>等待第一支镜头</h3><p>确认分镜表后，在镜头详情中手动生成。</p><button className="secondary" onClick={goBackStep}>返回</button></div>:<div className="result-grid">{jobs.map(j=><article className="result-card" key={j.id}><div className="result-preview">{j.status==='succeeded'?<video controls preload="metadata" src={j.video_url}/>:<div>{j.status==='running'?<LoaderCircle className="spin" size={26}/>:<Film size={26}/>}<span>{label[j.status]}</span></div>}<span className="sample-badge">模拟样例</span></div><div className="result-description"><strong>{p.shots.find(s=>s.id===j.shot_id)?.title||'历史镜头'}</strong><span>V{j.version} · 第 {j.attempt} 次</span><div><span className={'job-label '+j.status}>{label[j.status]}</span>{j.status==='failed'&&<button onClick={()=>void work('重新提交',async()=>{await api(`/projects/${p.id}/jobs/${j.id}/retry`,'POST',{});setJobs(await api(`/projects/${p.id}/jobs`))})}>手动重试</button>}</div></div></article>)}</div>}</div>}
   </main>
   {tab==='board'&&edit&&!viewVersion&&<aside className="detail"><div className="detail-heading"><div><span className="eyebrow">SHOT {String(p.shots.findIndex(s=>s.id===edit.id)+1).padStart(2,'0')}</span><h3>镜头详情</h3></div><button className="icon-button" onClick={()=>{if(dirty){setError('请先保存或取消修改');return}setSelected(null)}} aria-label="关闭镜头详情"><PanelRightClose size={19}/></button></div><div className="detail-content"><div className="detail-tools">{[[Scissors,'split','拆分'],[Merge,'merge','合并下一镜'],[ArrowUp,'up','上移'],[ArrowDown,'down','下移'],[Trash2,'delete','删除']] .map(([Icon,kind,title])=>{const I=Icon as typeof Scissors;return <button key={String(kind)} aria-label={String(title)} title={String(title)} disabled={!!busy||dirty} onClick={()=>void action(String(kind))}><I size={16}/></button>})}</div><label>来源场景<select value={edit.source_scene} onChange={e=>setEdit({...edit,source_scene:e.target.value})}>{p.script?.scenes.map(s=><option key={s.id} value={s.id}>{s.id} · {s.location}</option>)}</select></label>{fields.map(([key,title])=><label key={key}>{title}{['action','dialogue','start_state','end_state','prompt'].includes(key)?<textarea aria-label={title} className={key==='prompt'?'prompt-field':''} value={String(edit[key])} onChange={e=>setEdit({...edit,[key]:e.target.value})}/>:<input aria-label={title} type={key==='duration'?'number':'text'} min={1} max={30} value={String(edit[key])} onChange={e=>setEdit({...edit,[key]:key==='duration'?Number(e.target.value):e.target.value})}/>}</label>)}<label>参考图片（可选）</label><div className="references">{p.references.map(r=><label className="reference-option" key={r.id}><input type="checkbox" checked={edit.reference_ids.includes(r.id)} onChange={e=>setEdit({...edit,reference_ids:e.target.checked?[...edit.reference_ids,r.id]:edit.reference_ids.filter(id=>id!==r.id)})}/><img src={r.url}/>{r.name}</label>)}<label className="upload"><ImagePlus size={15}/>上传参考图<input type="file" accept="image/png,image/jpeg,image/webp" disabled={dirty||!!busy} onChange={e=>{const file=e.target.files?.[0];if(file)void work('上传参考图',async()=>{const form=new FormData();form.append('file',file);const res=await fetch(`/api/projects/${p.id}/references?version=${p.version}`,{method:'POST',body:form});const data=await res.json();if(!res.ok)throw new Error(data.detail);adopt(data)})}}/></label></div>{dirty&&<div className="edit-notice">保存将产生新版本，需要重新确认。</div>}</div><div className="detail-footer">{dirty?<><button className="secondary" onClick={()=>setEdit(structuredClone(shot!))}>取消修改</button><button className="primary" disabled={!!busy} onClick={()=>void work('保存镜头',()=>saveShots(p.shots.map(s=>s.id===edit.id?edit:s)))}>保存镜头</button></>:<button className="primary full" disabled={!approved||!!busy||!!latest(edit)} onClick={()=>{setVideoShot(edit);setFail(false);setModal('video')}}><Play size={16}/>{latest(edit)?label[latest(edit)!.status]:approved?'生成视频（模拟）':'确认分镜后可生成'}</button>}</div></aside>}
  </div>}
  </div>
  {proposal&&<div className="overlay"><div className="dialog diff-dialog"><div className="dialog-heading"><div><span className="eyebrow">REVIEW CHANGES</span><h2>只改这一镜，其余保持不变</h2></div><button className="icon-button" onClick={()=>setProposal(null)} aria-label="关闭修改建议"><X/></button></div><p>{proposal.instruction}</p><div className="diff-columns"><div><h4>修改前</h4>{fields.filter(([key])=>proposal.before[key]!==proposal.after[key]).map(([key,title])=><section key={key}><label>{title}</label><p>{String(proposal.before[key])||'无'}</p></section>)}</div><div><h4>修改后</h4>{fields.filter(([key])=>proposal.before[key]!==proposal.after[key]).map(([key,title])=><section key={key}><label>{title}</label><p>{String(proposal.after[key])||'无'}</p></section>)}</div></div><div className="dialog-actions"><button className="secondary" onClick={()=>setProposal(null)}>保留原版</button><button className="primary" disabled={!!busy} onClick={()=>void work('应用修改',async()=>{adopt(await api(`/projects/${p!.id}/revisions/apply`,'POST',{version:p!.version,proposal_id:proposal.id}));setProposal(null);setNotice('修改已应用，其他镜头未改变')})}>应用修改<Check size={16}/></button></div></div></div>}
  {modal&&<div className="overlay"><div className={'dialog '+(modal==='history'?'history-dialog':'')}><div className="dialog-heading"><h2>{{approve:'确认这版分镜',video:'生成单镜视频',model:'模型连接',projects:'项目列表',history:'版本历史'}[modal]}</h2><button className="icon-button" onClick={()=>setModal(null)} aria-label="关闭窗口"><X size={20}/></button></div>
  {modal==='approve'&&p&&<><p>确认 V{p.version} 的 {p.shots.length} 个镜头与视频提示词。</p><div className="summary-box"><span>总时长 <strong>{p.shots.reduce((n,s)=>n+s.duration,0)} 秒</strong></span><span>画幅 <strong>{p.ratio}</strong></span></div><p className="subtle">确认后可逐镜生成。此操作不会自动提交视频任务。</p><div className="dialog-actions"><button className="secondary" onClick={()=>setModal(null)}>继续编辑</button><button className="primary" disabled={!!busy} onClick={()=>void work('确认版本',async()=>{adopt(await api(`/projects/${p.id}/approve`,'POST',{version:p.version}));setModal(null);setStepOverride(null);setNotice('已确认。选择镜头即可生成模拟视频。')})}>确认此版本<Check size={16}/></button></div></>}
  {modal==='video'&&p&&videoShot&&<><div className="video-intent"><span className="pill">模拟任务</span><h3>{videoShot.title}</h3><p>{videoShot.duration}s · {p.ratio} · V{p.version}</p><p>{videoShot.action}</p></div><p className="subtle">演示排队、任务状态和样例播放。不会调用视频模型，也不会产生费用。</p><label className="checkbox"><input type="checkbox" checked={fail} onChange={e=>setFail(e.target.checked)}/>演示失败与手动重试</label><div className="dialog-actions"><button className="secondary" onClick={()=>setModal(null)}>取消</button><button className="primary" disabled={!!busy} onClick={()=>void work('提交视频模拟',async()=>{await api(`/projects/${p.id}/jobs`,'POST',{version:p.version,shot_id:videoShot.id,simulate_failure:fail});setModal(null);setTab('results');setSelected(null);setJobs(await api(`/projects/${p.id}/jobs`))})}>提交生成<Play size={16}/></button></div></>}
  {modal==='model'&&<><div className="model-icon"><Settings2 size={28}/></div><p>文本模型：<strong>{health?.model}</strong></p><p>{health?.model_configured?'服务端密钥已配置。':'服务端尚未配置 DeepSeek 密钥。'}</p><p className="subtle">在项目目录复制 .env.example 为 .env，填写 DEEPSEEK_API_KEY 后重启。密钥仅保存在本机服务端。</p><p className="subtle">预置案例可体验编辑和视频模拟；真实脚本、分镜、对话修改需要连接模型。</p><button className="secondary full" onClick={()=>void work('检查连接',async()=>{setHealth(await api('/health'));setNotice('已刷新模型配置状态')})}><RotateCcw size={15}/>刷新连接状态</button></>}
  {modal==='projects'&&<div className="project-list">{projects.length?projects.map(x=><button key={x.id} onClick={()=>{adopt(x);setSelected(null);setProposal(null);setMessages([]);setTab(x.shots.length?'board':'script');setModal(null)}}><div><strong>{x.script?.title||x.title}</strong><span>{x.shots.length} 镜 · V{x.version}</span></div><ChevronRight size={16}/></button>):<p>还没有项目，先写下第一个故事。</p>}</div>}
  {modal==='history'&&<div className="project-list">{history.map(x=><button key={x.version} onClick={()=>{setViewVersion(x);setTab(x.shots.length?'board':'script');setSelected(null);setModal(null)}}><div><strong>V{x.version}{x.version===p?.version?' · 当前版本':''}</strong><span>{x.shots.length} 镜 · {x.approved_version===x.version?'已确认':'草稿'}</span></div><span>查看<ChevronRight size={14}/></span></button>)}</div>}
  </div></div>}
 </div>
}

const BASE=(import.meta.env.BASE_URL||'/').replace(/\/$/,'');
function withBase(path:string){
 const clean=path.startsWith('/')?path:`/${path}`;
 return `${BASE}${clean}`||clean;
}
function isEmbed(){
 return new URLSearchParams(window.location.search).get('embed')==='1';
}
function appPath(){
 let path=window.location.pathname.replace(/\/$/,'')||'/';
 if(BASE && (path===BASE || path.startsWith(BASE+'/'))) path=path.slice(BASE.length)||'/';
 return path||'/';
}
function storyboardUrl(extra:Record<string,string>={}){
 const q=new URLSearchParams();
 if(isEmbed()) q.set('embed','1');
 for(const [k,v] of Object.entries(extra)){
  if(v) q.set(k,v);
 }
 const s=q.toString();
 return `${withBase('/storyboard')}${s?`?${s}`:''}`;
}
function SiteApp(){
 const path=appPath();
 const embed=isEmbed();
 return <>{!embed&&<SiteHeader active={path}/>}{path==='/series'?<ProjectsPage/>:path==='/storyboard'?<div className="storyboard-site"><App/></div>:<main className="site-not-found"><h1>页面未找到</h1><a href={withBase('/')}>返回首页</a></main>}</>
}
createRoot(document.getElementById('root')!).render(<SiteApp/>);

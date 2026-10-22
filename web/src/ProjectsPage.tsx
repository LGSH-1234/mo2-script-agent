import {useEffect,useState} from 'react';
import {ArrowRight,Clapperboard,FolderOpen,LoaderCircle,Plus,Search} from 'lucide-react';
import type {Project} from './types';

export function ProjectsPage(){
 const [projects,setProjects]=useState<Project[]>([]),[query,setQuery]=useState(''),[loading,setLoading]=useState(true),[error,setError]=useState('');
 async function load(){setLoading(true);setError('');try{const response=await fetch('/api/projects');if(!response.ok)throw new Error('项目暂时无法载入，请重试。');setProjects(await response.json())}catch(e){setError(e instanceof Error?e.message:'无法连接项目服务。')}finally{setLoading(false)}}
 useEffect(()=>{void load()},[]);
 const filtered=projects.filter(p=>`${p.script?.title||p.title} ${p.brief}`.toLocaleLowerCase().includes(query.trim().toLocaleLowerCase()));
 return <main className="mo2-projects-page">
  <div className="mo2-projects-heading"><div><h1>我的项目</h1><p>让每一个想法，成为下一部作品。</p></div><a className="mo2-new-project" href="/storyboard?new=1"><Plus size={18}/>新建分镜项目</a></div>
  <div className="mo2-projects-toolbar"><div className="mo2-projects-tab">分镜项目 <span>{projects.length}</span></div><label className="mo2-project-search"><Search size={17}/><input aria-label="搜索项目" placeholder="搜索项目" value={query} onChange={e=>setQuery(e.target.value)}/></label></div>
  {loading?<div className="mo2-projects-empty"><LoaderCircle size={28} className="spin"/><p>正在载入项目…</p></div>:error?<div className="mo2-projects-empty" role="alert"><p>{error}</p><button className="secondary" onClick={()=>void load()}>重新载入</button></div>:filtered.length?<div className="mo2-project-grid">{filtered.map(p=><a className="mo2-project-card" href={`/storyboard?project=${encodeURIComponent(p.id)}`} key={p.id}>
   <div className="mo2-project-cover"><span className="mo2-project-cover-mark"><Clapperboard size={36}/></span><span className="mo2-project-ratio">{p.ratio}</span><span className="mo2-project-cover-title">{p.script?.title||p.title}</span><span className="mo2-project-open"><ArrowRight size={20}/></span></div>
   <div className="mo2-project-card-body"><h2>{p.script?.title||p.title}</h2><p>{p.brief}</p><div><span>{p.shots.length} 镜 · {p.duration} 秒</span><span>V{p.version} · {p.approved_version===p.version?'已确认':p.shots.length?'待确认':p.script?'脚本草稿':'待写脚本'}</span></div></div>
  </a>)}</div>:<div className="mo2-projects-empty"><FolderOpen size={38}/><h2>{query?'没有找到匹配的项目':'从第一个故事开始'}</h2><p>{query?'试试其他关键词。':'输入导演文本，和 Agent 一起完成脚本与分镜。'}</p>{query?<button className="secondary" onClick={()=>setQuery('')}>清空搜索</button>:<a className="mo2-new-project" href="/storyboard?new=1"><Plus size={17}/>创建分镜项目</a>}</div>}
 </main>
}

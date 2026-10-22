const links=[
 {label:'首页',href:'/'},
 {label:'我的项目',href:'/series'},
 {label:'关于我们',href:'/about'},
 {label:'Agent',href:'https://ai.momostudio.top/'},
 {label:'分镜',href:'/storyboard'},
];

export function SiteHeader({active}:{active:string}){
 return <header className="mo2-site-header">
  <a href="/" className="mo2-site-logo" aria-label="MO² 首页"><img src="/media/site/assets/1b4c791608bb24b4.svg" alt="MO²"/></a>
  <nav className="mo2-site-nav" aria-label="主导航">{links.map(link=><a key={link.label} href={link.href} className={active===link.href?'is-active':''} aria-current={active===link.href?'page':undefined}>{link.label}</a>)}</nav>
  <div className="mo2-site-account"><a href="/pricing" className={active==='/pricing'?'is-active':''}>价格方案</a><span className="mo2-local-label">本地演示</span><span className="mo2-site-avatar" aria-label="本地导演账号">导</span></div>
 </header>
}

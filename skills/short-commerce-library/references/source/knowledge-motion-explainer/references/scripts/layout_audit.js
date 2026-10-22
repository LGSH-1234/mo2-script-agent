
/* 文字几何审阅：只测实际文字，不把 Canvas 或标题容器当文字框。 */
(() => {
  if (window.LayoutAudit?.version === 1) return;
  const states = new Map();
  const native = CanvasRenderingContext2D.prototype;
  const fillText = native.fillText;
  const state = ctx => {
    if (!states.has(ctx.canvas)) states.set(ctx.canvas, {rows: [], raw: [], gaps: [], clips: [], clipped: false});
    return states.get(ctx.canvas);
  };
  const reset = ctx => { states.delete(ctx.canvas); state(ctx); };
  const rgbaAlpha = value => {
    const m = typeof value === 'string' && value.match(/^rgba\([^,]+,[^,]+,[^,]+,\s*([\d.]+)\)$/);
    return m ? Number(m[1]) : 1;
  };
  const painted = (ctx,operation='fillText') => ctx.globalAlpha * rgbaAlpha(operation==='strokeText'?ctx.strokeStyle:ctx.fillStyle) > .001;
  function textPaint(el,cs) {
    if(el instanceof SVGElement)return {
      fill:cs.fill!=='none'&&rgbaAlpha(cs.fill)*Number(cs.fillOpacity)>.001,
      stroke:cs.stroke!=='none'&&parseFloat(cs.strokeWidth)>0&&rgbaAlpha(cs.stroke)*Number(cs.strokeOpacity)>.001
    };
    return {fill:rgbaAlpha(cs.webkitTextFillColor||cs.color)>.001,
      stroke:parseFloat(cs.webkitTextStrokeWidth)>0&&rgbaAlpha(cs.webkitTextStrokeColor)>.001};
  }
  const bounds = points => ({left: Math.min(...points.map(p => p.x)), top: Math.min(...points.map(p => p.y)),
    right: Math.max(...points.map(p => p.x)), bottom: Math.max(...points.map(p => p.y))});
  const transformBox = (m, b) => bounds([[b.left,b.top],[b.right,b.top],[b.right,b.bottom],[b.left,b.bottom]]
    .map(([x,y]) => ({x:m.a*x+m.c*y+m.e,y:m.b*x+m.d*y+m.f})));
  const intersects = (a,b,epsilon=0) => Math.min(a.right,b.right)-Math.max(a.left,b.left)>epsilon && Math.min(a.bottom,b.bottom)-Math.max(a.top,b.top)>epsilon;
  const contains = (a,b,epsilon=0) => b.left>=a.left-epsilon && b.top>=a.top-epsilon && b.right<=a.right+epsilon && b.bottom<=a.bottom+epsilon;
  const snippet = text => String(text).replace(/\s+/g,' ').slice(0,100);
  const identity = el => el.id || el.getAttribute('data-layout-id') || (() => {
    const parts=[]; for(let e=el;e&&parts.length<5;e=e.parentElement) {
      parts.unshift(`${e.tagName.toLowerCase()}:nth-child(${[...e.parentElement?.children||[]].indexOf(e)+1})`);
    } return parts.join('>');
  })();
  function visible(el) {
    if(!el.isConnected || getComputedStyle(el).visibility!=='visible') return false;
    let alpha=1;
    for(let e=el;e;e=e.parentElement) {const s=getComputedStyle(e);if(s.display==='none')return false;alpha*=Number(s.opacity);}
    return alpha>.001;
  }
  function axisCSS(el) {
    for(let e=el;e;e=e.parentElement) {
      const s=getComputedStyle(e); if(s.perspective!=='none')return false;
      if(s.transform!=='none') {const m=new DOMMatrix(s.transform);if(!m.is2D||Math.abs(m.b)>1e-8||Math.abs(m.c)>1e-8||m.a<=0||m.d<=0)return false;}
    } return true;
  }
  const getContext=HTMLCanvasElement.prototype.getContext;
  HTMLCanvasElement.prototype.getContext=function(...args) {const ctx=getContext.apply(this,args);if(args[0]==='2d'&&ctx)state(ctx);return ctx;};
  for(const name of ['width','height']) {
    const d=Object.getOwnPropertyDescriptor(HTMLCanvasElement.prototype,name);
    Object.defineProperty(HTMLCanvasElement.prototype,name,{...d,set(value){d.set.call(this,value);states.delete(this);}});
  }
  for(const name of ['fillText','strokeText']) {
    const original=native[name];
    native[name]=function(text,...args) {
      const result=original.call(this,text,...args);
      if(String(text).trim()&&painted(this,name))state(this).raw.push({text:snippet(text),operation:name});
      return result;
    };
  }
  for(const name of ['reset','save','restore','clip']) {
    const original=native[name];if(!original)continue;
    native[name]=function(...args) {
      const result=original.apply(this,args),s=state(this);
      if(name==='reset')reset(this);
      else if(name==='save')s.clips.push(s.clipped);
      else if(name==='restore'){if(s.clips.length)s.clipped=s.clips.pop();}
      else s.clipped=true;
      return result;
    };
  }
  const clearRect=native.clearRect;
  native.clearRect=function(x,y,w,h) {
    const result=clearRect.call(this,x,y,w,h),m=this.getTransform(),s=state(this);
    const b=transformBox(m,{left:x,top:y,right:x+w,bottom:y+h});
    if(!s.clipped&&Math.abs(m.b)<1e-8&&Math.abs(m.c)<1e-8) {
      if(contains(b,{left:0,top:0,right:this.canvas.width,bottom:this.canvas.height})) {s.rows=[];s.raw=[];s.gaps=[];}
      else {s.rows=s.rows.filter(row=>!contains(b,row.box));if(s.rows.some(row=>intersects(b,row.box)))s.gaps.push('partial_clear_over_text');}
    } else if(s.rows.length)s.gaps.push('unmeasured_clear_clip');
    return result;
  };
  function drawText(ctx,text,x,y,options={}) {
    const result=options.maxWidth===undefined?fillText.call(ctx,text,x,y):fillText.call(ctx,text,x,y,options.maxWidth);
    if(!String(text).trim()||!painted(ctx))return result;
    const s=state(ctx),id=options.id;
    if(typeof id!=='string'||!id.trim()){s.raw.push({text:snippet(text),operation:'missing_text_id'});return result;}
    const m=ctx.measureText(text),scale=options.maxWidth===undefined?1:Math.min(1,Number(options.maxWidth)/m.width);
    const values=[m.actualBoundingBoxLeft,m.actualBoundingBoxRight,m.actualBoundingBoxAscent,m.actualBoundingBoxDescent,scale];
    if(values.some(n=>!Number.isFinite(n))||scale<=0){s.gaps.push(`text_metrics:${id}`);return result;}
    if(s.clipped)s.gaps.push(`canvas_clip:${id}`);
    if(!document.fonts.check(ctx.font,String(text)))s.gaps.push(`canvas_font_not_ready:${id}`);
    if(ctx.globalCompositeOperation!=='source-over')s.gaps.push(`canvas_composite:${id}`);
    const box=transformBox(ctx.getTransform(),{left:x-m.actualBoundingBoxLeft*scale,right:x+m.actualBoundingBoxRight*scale,
      top:y-m.actualBoundingBoxAscent,bottom:y+m.actualBoundingBoxDescent});
    const row={id,group:options.group||id,text:snippet(text),box,kind:'canvas'};
    const key=JSON.stringify(row);if(!s.rows.some(r=>r.key===key))s.rows.push({...row,key});
    if(s.rows.length>2000){s.rows=s.rows.slice(-2000);s.gaps.push('canvas_record_limit');}
    return result;
  }
  function collect(root,{width,height,insetRatio=.04,gap=12*height/1080}={}) {
    const issues=[],rows=[],coverage={domBoxes:0,svgBoxes:0,canvasBoxes:0,visibleCanvases:0,trackedCanvases:0};
    const rootRect=root.getBoundingClientRect(),sx=rootRect.width/width,sy=rootRect.height/height;
    const issue=(type,items,detail)=>issues.push({type,ids:items.map(x=>x.id),text:items.map(x=>x.text),boxes:items.map(x=>x.box),detail});
    const fromScreen=b=>({left:(b.left-rootRect.left)/sx,top:(b.top-rootRect.top)/sy,right:(b.right-rootRect.left)/sx,bottom:(b.bottom-rootRect.top)/sy});
    const rootItem={id:identity(root),text:'',box:{left:0,top:0,right:rootRect.width,bottom:rootRect.height}};
    if(root.clientWidth!==width||root.clientHeight!==height||!Number.isFinite(sx)||!Number.isFinite(sy)||sx<=0||sy<=0||!axisCSS(root)) {
      issue('root_dimensions',[rootItem],`Declared ${width}x${height}; actual client ${root.clientWidth}x${root.clientHeight}; CSS rotation/perspective unsupported`);
      return {issues,coverage,boxes:[]};
    }
    if(document.fonts.status!=='loaded')issue('font_coverage_gap',[rootItem],'Fonts changed or started loading during the sampled frame');
    const rootStyle=getComputedStyle(root);
    if(rootStyle.clipPath!=='none'||rootStyle.maskImage!=='none')issue('unsupported_clip',[rootItem],'Root clip-path/mask is not measured');
    function append(row,element,screenBox) {
      if(![row.box.left,row.box.right,row.box.top,row.box.bottom].every(Number.isFinite)) {issue('unmeasurable_text',[row],'Invalid coordinates');return;}
      if(row.box.right-row.box.left<=0||row.box.bottom-row.box.top<=0)return;
      const safe={left:width*insetRatio,top:height*insetRatio,right:width*(1-insetRatio),bottom:height*(1-insetRatio)};
      if(!contains(safe,row.box,.5))issue('text_out_of_bounds',[row],'Text exceeds the declared safe area');
      let clipped={left:screenBox.left,top:screenBox.top,right:screenBox.right,bottom:screenBox.bottom};
      for(let e=element;e&&e!==root;e=e.parentElement) {
        const cs=getComputedStyle(e),r=e.getBoundingClientRect();
        if(cs.clipPath!=='none'||cs.maskImage!=='none')issue('unsupported_clip',[row],identity(e));
        if(['hidden','clip','scroll','auto'].includes(cs.overflowX)){clipped.left=Math.max(clipped.left,r.left);clipped.right=Math.min(clipped.right,r.right);}
        if(['hidden','clip','scroll','auto'].includes(cs.overflowY)){clipped.top=Math.max(clipped.top,r.top);clipped.bottom=Math.min(clipped.bottom,r.bottom);}
      }
      if(!contains(clipped,screenBox,.5))issue('text_clipped',[row],'An ancestor clips this text');
      rows.push({...row,visibleBox:fromScreen(clipped)});
      coverage[row.kind==='canvas'?'canvasBoxes':row.kind==='svg'?'svgBoxes':'domBoxes']++;
    }
    const walker=document.createTreeWalker(root,NodeFilter.SHOW_TEXT);
    for(let node=walker.nextNode();node;node=walker.nextNode()) {
      const el=node.parentElement;if(!el||!node.textContent.trim()||el.closest('script,style,canvas,defs,symbol,clipPath,mask,pattern')||!visible(el))continue;
      const paint=textPaint(el,getComputedStyle(el));if(!paint.fill&&!paint.stroke)continue;
      let owner=el.closest('[data-layout-group]');
      if(!owner){owner=el;while(owner.parentElement!==root&&getComputedStyle(owner).display==='inline')owner=owner.parentElement;}
      const group=owner.getAttribute('data-layout-group')||identity(owner);
      const range=document.createRange();range.selectNodeContents(node);
      let n=0;
      for(const r of range.getClientRects()) {
        const row={id:`${identity(el)}:text${[...el.childNodes].indexOf(node)}:line${n++}`,group,text:snippet(node.textContent),box:fromScreen(r),kind:el instanceof SVGElement?'svg':'dom'};
        if(paint.stroke)issue('text_stroke_unmeasured',[row],'Stroke extents require pixel review');
        append(row,el,r);
      }
    }
    for(const canvas of root.querySelectorAll('canvas')) {
      if(!visible(canvas))continue;
      const r=canvas.getBoundingClientRect();if(!r.width||!r.height)continue;
      coverage.visibleCanvases++;
      const s=states.get(canvas),base={id:identity(canvas),text:'',box:fromScreen(r)};
      if(!s){issue('canvas_coverage_gap',[base],'Canvas context/text was not observed by the installed helper');continue;}
      coverage.trackedCanvases++;
      if(!axisCSS(canvas)){issue('canvas_coverage_gap',[base],'CSS rotation/perspective is not measured');continue;}
      for(const raw of s.raw)issue('canvas_untracked_text',[{...base,text:raw.text}],raw.operation);
      for(const detail of new Set(s.gaps))issue('canvas_coverage_gap',[base],detail);
      const cs=getComputedStyle(canvas),cx=r.width/canvas.offsetWidth,cy=r.height/canvas.offsetHeight;
      const left=r.left+(parseFloat(cs.borderLeftWidth)+parseFloat(cs.paddingLeft))*cx;
      const top=r.top+(parseFloat(cs.borderTopWidth)+parseFloat(cs.paddingTop))*cy;
      const contentWidth=canvas.clientWidth-parseFloat(cs.paddingLeft)-parseFloat(cs.paddingRight);
      const contentHeight=canvas.clientHeight-parseFloat(cs.paddingTop)-parseFloat(cs.paddingBottom);
      for(const row of s.rows) {
        const b=row.box,screen={left:left+b.left*contentWidth*cx/canvas.width,right:left+b.right*contentWidth*cx/canvas.width,
          top:top+b.top*contentHeight*cy/canvas.height,bottom:top+b.bottom*contentHeight*cy/canvas.height};
        if(!contains({left:0,top:0,right:canvas.width,bottom:canvas.height},b,.5))issue('canvas_bitmap_clip',[{...row,id:`${identity(canvas)}/${row.id}`,box:fromScreen(screen)}],'Text extends beyond the Canvas backing bitmap');
        append({...row,id:`${identity(canvas)}/${row.id}`,group:`${identity(canvas)}/${row.group}`,box:fromScreen(screen)},canvas,screen);
      }
    }
    for(let i=0;i<rows.length;i++)for(let j=i+1;j<rows.length;j++) {
      const a=rows[i],b=rows[j],same=a.group===b.group;
      if(intersects(a.visibleBox,b.visibleBox,1))issue('text_overlap',[a,b],'Conservative AABB overlap; inspect the identified text');
      else if(!same&&gap>0&&intersects({left:a.visibleBox.left-gap,top:a.visibleBox.top-gap,right:a.visibleBox.right+gap,bottom:a.visibleBox.bottom+gap},b.visibleBox))issue('text_gap',[a,b],`Less than ${gap.toFixed(2)} logical px between text groups`);
    }
    return {issues,coverage,boxes:rows.map(({id,group,text,box,kind})=>({id,group,text,box,kind}))};
  }
  window.LayoutAudit={version:1,fillText:drawText,beginFrame(){/* 保留未重绘 Canvas 的当前像素记录；清屏由原生操作同步。 */},collect};
})();
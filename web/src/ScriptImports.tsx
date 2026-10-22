import {useRef, useState} from 'react';
import {FileText, Paperclip, X} from 'lucide-react';
import './script-imports.css';

const selectable = ['pdf', 'doc', 'docx', 'txt', 'md', 'rtf'];
const parseable = selectable;
const extension = (file: File) => file.name.split('.').pop()?.toLowerCase() || '';
const identity = (file: File) => `${file.name}:${file.size}:${file.lastModified}`;
function sizeLabel(bytes: number) {
 if (bytes < 1024) return `${bytes} B`;
 if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
 return `${(bytes / 1024 / 1024).toFixed(1)} MB`;
}

export function ScriptImports({files, onChange, disabled=false, compact=false}: {
 files: File[]; onChange: (files: File[]) => void; disabled?: boolean; compact?: boolean;
}) {
 const input = useRef<HTMLInputElement>(null);
 const [error, setError] = useState('');
 function select(selected: FileList | null) {
  if (!selected) return;
  const incoming = [...selected];
  const tooLarge = incoming.filter(file => file.size > 20 * 1024 * 1024);
  const unsupported = incoming.filter(file => !selectable.includes(extension(file)));
  const accepted = incoming.filter(file => parseable.includes(extension(file)) && file.size <= 20 * 1024 * 1024);
  const combined = [...new Map([...files, ...accepted].map(file => [identity(file), file])).values()];
  if(combined.length <= 5)onChange(combined);
  const messages: string[] = [];
  if (tooLarge.length) messages.push('单个文件不能超过 20 MB');
  if (combined.length > 5) messages.push('一次最多导入 5 个文件');
  if (unsupported.length) {
   messages.push(`不支持 ${unsupported.map(file => file.name).join('、')}，请选择 PDF、Word、TXT、Markdown 或 RTF`);
  }
  setError(messages.join('。') || '');
  if (input.current) input.current.value = '';
 }
 return <section className={`script-imports${compact ? ' is-compact' : ''}`} aria-label="脚本附件">
  <div className="script-import-toolbar">
   <button type="button" className="script-import-button" onClick={() => input.current?.click()} disabled={disabled}><Paperclip size={15}/>导入脚本</button>
   <span>PDF / Word / TXT / Markdown / RTF</span>
   <input ref={input} type="file" aria-label="导入脚本文件" accept={selectable.map(ext => `.${ext}`).join(',')} multiple hidden onChange={event => select(event.target.files)}/>
  </div>
  {files.length > 0 && <>
   <div className="script-file-list" aria-live="polite">
    {files.map(file => <div className="script-file-card" key={identity(file)}>
     <div className={`script-file-icon is-${extension(file)}`}><FileText size={20}/></div>
     <div className="script-file-info"><strong title={file.name}>{file.name}</strong><small>{extension(file).toUpperCase()} · {sizeLabel(file.size)}</small></div>
     <button type="button" disabled={disabled} aria-label={`移除 ${file.name}`} onClick={() => onChange(files.filter(item => identity(item) !== identity(file)))}><X size={14}/></button>
    </div>)}
   </div>
   <p className="script-import-note">已导入脚本文件。点击「开始写分镜」将解析内容并直接生成分镜，无需再写脚本。</p>
  </>}
  {error && <p className="script-import-error" role="alert">{error}</p>}
 </section>;
}

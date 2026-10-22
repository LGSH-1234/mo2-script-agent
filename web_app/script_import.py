"""Extract plain text from uploaded script files (stdlib only)."""
from __future__ import annotations

import re
import subprocess
import sys
import tempfile
from pathlib import Path
from pypdf import PdfReader
from striprtf.striprtf import rtf_to_text
import zipfile
from io import BytesIO
from xml.etree import ElementTree as ET

SUPPORTED = {"pdf", "doc", "docx", "txt", "md", "rtf"}


def ext_of(name: str) -> str:
    return (name.rsplit(".", 1)[-1] if "." in name else "").lower()


def extract_text(name: str, data: bytes) -> str:
    ext = ext_of(name)
    if ext not in SUPPORTED:
        raise ValueError(f"不支持的文件类型：{name}")
    if ext in {"txt", "md"}:
        return _decode(data)
    if ext == "rtf":
        return _rtf_to_text(_decode(data))
    if ext == "docx":
        return _docx_to_text(data)
    if ext == "doc":
        if sys.platform != 'darwin':
            raise ValueError(f"{name} 是旧版 Word（.doc），请另存为 .docx 后再上传")
        try:
            with tempfile.TemporaryDirectory(prefix='mo2-import-') as folder:
                source = Path(folder) / 'script.doc'
                source.write_bytes(data)
                result = subprocess.run(['/usr/bin/textutil', '-convert', 'txt', '-stdout', str(source)], capture_output=True, timeout=20, check=True)
                return result.stdout.decode('utf-8')
        except Exception:
            raise ValueError('无法读取 DOC，请另存为 DOCX 后导入') from None
    if ext == "pdf":
        try:
            reader = PdfReader(BytesIO(data))
            if reader.is_encrypted:
                raise ValueError('请先解除 PDF 密码保护后导入')
            if len(reader.pages) > 200:
                raise ValueError('PDF 最多支持 200 页，请拆分后导入')
            text = '\n\n'.join(page.extract_text() or '' for page in reader.pages).strip()
            if not text:
                raise ValueError('未读取到文字；扫描版 PDF 请先转为可复制的文字')
            return text
        except ValueError:
            raise
        except Exception:
            raise ValueError('PDF 无法读取，请检查文件是否损坏') from None
    raise ValueError(f"不支持的文件类型：{name}")


def _decode(data: bytes) -> str:
    for enc in ("utf-8-sig", "utf-16" if data.startswith((b'\xff\xfe', b'\xfe\xff')) else "gb18030"):
        try:
            return data.decode(enc)
        except UnicodeDecodeError:
            continue
    raise ValueError('文本编码无法识别，请另存为 UTF-8 后导入')


def _docx_to_text(data: bytes) -> str:
    try:
        with zipfile.ZipFile(BytesIO(data)) as zf:
            if zf.getinfo('word/document.xml').file_size > 10 * 1024 * 1024:
                raise ValueError('Word 正文过大，请拆分后导入')
            xml = zf.read("word/document.xml")
    except KeyError as e:
        raise ValueError("无法读取 Word 文档内容") from e
    except zipfile.BadZipFile as e:
        raise ValueError("Word 文件损坏或不是有效的 .docx") from e
    try:
        root = ET.fromstring(xml)
    except ET.ParseError:
        raise ValueError('Word 正文损坏，请另存为 DOCX 后导入') from None
    parts: list[str] = []
    for node in root.iter():
        tag = node.tag.rsplit("}", 1)[-1]
        if tag == "t" and node.text:
            parts.append(node.text)
        elif tag == "tab":
            parts.append("\t")
        elif tag in {"br", "cr"}:
            parts.append("\n")
        elif tag == "p":
            parts.append("\n")
    text = re.sub(r"\n{3,}", "\n\n", "".join(parts)).strip()
    if not text:
        raise ValueError("Word 文档里没有可读文字")
    return text


def _rtf_to_text(raw: str) -> str:
    return rtf_to_text(raw).strip()


def combine_files(files: list[tuple[str, bytes]]) -> str:
    chunks: list[str] = []
    for name, data in files:
        body = extract_text(name, data).strip()
        if not body:
            raise ValueError(f"{name} 没有可读文字")
        chunks.append(f"【来源：{name}】\n{body}")
    return "\n\n".join(chunks).strip()

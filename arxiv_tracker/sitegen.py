# -*- coding: utf-8 -*-
import os, datetime, html
from typing import Dict, List, Any, Optional

import re
try:
    from markdown import markdown as _md
except Exception:
    _md = None

def _esc(x):  # 保留你的实现
    import html
    return html.escape(x or "", quote=True)

def _md2html(md: str) -> str:
    if not md: return ""
    if _md:
        return _md(md, extensions=["extra", "sane_lists", "tables"])
    return "<pre class='mono'>" + _esc(md) + "</pre>"

# --- 语言/内容判断 & 文本处理 ---
_CJK_RE = re.compile(r"[\u4e00-\u9fff]")
def _has_cjk(s: str) -> bool:
    return bool(_CJK_RE.search(s or ""))

def _first_sentence(text: str) -> str:
    if not text: return ""
    t = re.sub(r"\s+", " ", text.strip())
    parts = re.split(r"(?<=[。！？.!?])\s+", t)
    return parts[0] if parts else t

def _strip_format(md: str) -> str:
    """
    去掉冗余行：**Method Card...**, **Discussion...**, **Links**...
    """
    if not md: return ""
    out = []
    for line in md.splitlines():
        L = line.strip().lower()
        if L.startswith("**method card") or L.startswith("**discussion"):
            continue
        if L.startswith("- **links**"):
            continue
        out.append(line)
    return "\n".join(out)

def _localize_md_to_zh(md: str) -> str:
    """
    仅把标签本地化，内容不硬翻译（避免引入错误）。英文值保留。
    """
    repl = {
        "**Task / Problem**:": "**任务 / 问题**：",
        "**Core Idea**:": "**核心思路**：",
        "**Data / Benchmarks**:": "**数据 / 基准**：",
        "**Venue**:": "**会议 / 期刊**：",
    }
    s = md
    for k, v in repl.items():
        s = s.replace(k, v)
    return s
    
try:
    # 用于把 full_md 渲染成真正的 HTML 列表/加粗等
    from markdown import markdown as _md
except Exception:
    _md = None

def _esc(x: Optional[str]) -> str:
    return html.escape(x or "", quote=True)

def _md2html(md: str) -> str:
    if not md: return ""
    if _md:
        return _md(md, extensions=["extra", "sane_lists", "tables"])
    # 兜底（没有 markdown 包时，退化为等宽块）
    return "<pre class='mono'>" + _esc(md) + "</pre>"

def _strip_redundant_links(md: str) -> str:
    out = []
    for line in (md or "").splitlines():
        if line.strip().lower().startswith("- **links**"):
            continue
        out.append(line)
    return "\n".join(out)

def _css(accent: str = "#2563eb") -> str:
    return f"""
:root {{
  --bg0:#f1f4f9;
  --bg1:#e4eaf3;
  --card:#ffffff;
  --text:#0b1220;
  --text2:#334155;
  --muted:#64748b;
  --line:rgba(15,23,42,.08);
  --acc:{accent};
  --acc-faint: color-mix(in srgb, {accent} 14%, transparent);
  --acc-ghost: color-mix(in srgb, {accent} 6%, #ffffff);
  --shadow: 0 1px 0 rgba(255,255,255,.7) inset, 0 4px 20px rgba(15,23,42,.06);
  --shadow-h: 0 12px 32px rgba(15,23,42,.1);
  --r: 18px;
  --r-sm: 10px;
  --font: "Plus Jakarta Sans", system-ui, -apple-system, "Segoe UI", sans-serif;
  --font-t: "Outfit", var(--font);
}}
:root[data-theme="dark"] {{
  --bg0: #0b0d12;
  --bg1: #12151d;
  --card: #161a24;
  --text: #e8ecf4;
  --text2: #a8b3c9;
  --muted: #8892a4;
  --line: rgba(232,236,244,.1);
  --acc-faint: color-mix(in srgb, {accent} 22%, transparent);
  --acc-ghost: color-mix(in srgb, {accent} 8%, #161a24);
  --shadow: 0 1px 0 rgba(255,255,255,.04) inset, 0 4px 24px rgba(0,0,0,.35);
  --shadow-h: 0 16px 40px rgba(0,0,0,.45);
}}
* {{ box-sizing: border-box; }}
html {{ -webkit-font-smoothing: antialiased; }}
body {{
  margin: 0;
  min-height: 100vh;
  color: var(--text);
  font-family: var(--font);
  font-size: 15px;
  line-height: 1.65;
  background: fixed linear-gradient(168deg, var(--bg0) 0%, var(--bg1) 48%, var(--bg0) 100%), var(--bg0);
  letter-spacing: 0.01em;
}}
.container {{ max-width: 52rem; margin: 0 auto; padding: 28px 20px 40px; }}
.app-header {{
  display: flex;
  gap: 1rem;
  align-items: flex-start;
  justify-content: space-between;
  flex-wrap: wrap;
  margin-bottom: 0.5rem;
  padding-bottom: 1.25rem;
  border-bottom: 1px solid var(--line);
}}
h1 {{
  font-family: var(--font-t);
  font-size: clamp(1.25rem, 1.1rem + 1vw, 1.6rem);
  font-weight: 600;
  letter-spacing: -0.03em;
  line-height: 1.25;
  margin: 0;
  max-width: 20ch;
  color: var(--text);
}}
.badge-time {{
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  color: var(--text2);
  background: var(--acc-ghost);
  border: 1px solid var(--acc-faint);
  padding: 6px 12px;
  border-radius: 999px;
  white-space: nowrap;
}}
.lead-row {{
  margin: 1.25rem 0 1.5rem;
}}
.page-sub {{
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  font-size: 0.8rem;
  font-weight: 500;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  color: var(--muted);
}}
.page-sub::before {{
  content: "";
  display: block;
  width: 0.5rem;
  height: 0.5rem;
  border-radius: 2px;
  background: var(--acc);
  opacity: 0.9;
}}
.toolbar {{ display: flex; flex-wrap: wrap; gap: 8px; align-items: center; }}
.btn {{
  font-family: var(--font);
  font-size: 0.8rem;
  font-weight: 500;
  border: 1px solid var(--line);
  background: var(--card);
  color: var(--text2);
  padding: 7px 12px;
  border-radius: 999px;
  cursor: pointer;
  box-shadow: var(--shadow);
  transition: color .15s, border-color .15s, background .15s, transform .12s;
}}
.btn:hover {{
  color: var(--text);
  border-color: var(--acc-faint);
  background: var(--acc-ghost);
}}
.btn:active {{ transform: scale(0.98); }}
#theme-label {{ font-size: 0.72rem; letter-spacing: 0.04em; opacity: 0.9; }}
.row {{ display: flex; flex-direction: column; gap: 1.1rem; }}
.paper {{
  position: relative;
  background: var(--card);
  border: 1px solid var(--line);
  border-radius: var(--r);
  padding: 1.1rem 1.15rem 1.1rem 1.35rem;
  box-shadow: var(--shadow);
  transition: box-shadow .2s, transform .18s, border-color .2s;
}}
.paper::before {{
  content: "";
  position: absolute;
  left: 0; top: 0.6rem; bottom: 0.6rem; width: 3px; border-radius: 3px;
  background: var(--acc);
  opacity: 0.9;
}}
.paper:hover {{
  box-shadow: var(--shadow-h);
  border-color: var(--acc-faint);
  transform: translateY(-2px);
}}
.title {{
  font-family: var(--font-t);
  font-size: 1.08rem;
  font-weight: 600;
  letter-spacing: -0.02em;
  line-height: 1.45;
  margin: 0 0 0.5rem 0;
  color: var(--text);
}}
.meta-line {{
  color: var(--muted);
  font-size: 0.82rem;
  line-height: 1.45;
  margin: 0.2rem 0 0.15rem;
}}
.meta-line b {{ color: var(--text2); font-weight: 600; }}
.doc-links {{ margin-top: 0.65rem; line-height: 1.6; display: flex; flex-wrap: wrap; gap: 0.4rem 0.65rem; }}
.doc-links a {{
  display: inline-flex;
  align-items: center;
  font-size: 0.8rem;
  font-weight: 500;
  color: var(--acc);
  text-decoration: none;
  padding: 3px 0;
  border-bottom: 1px solid transparent;
  transition: border-color .15s, color .15s;
}}
.doc-links a:hover {{ border-bottom-color: var(--acc); }}
.prose-blk details.detail {{
  margin-top: 0.75rem;
  border: 1px solid var(--line);
  border-radius: var(--r-sm);
  background: var(--acc-ghost);
  overflow: hidden;
}}
.prose-blk .detail summary {{
  cursor: pointer;
  list-style: none;
  display: flex;
  align-items: center;
  gap: 0.4rem;
  font-size: 0.78rem;
  font-weight: 600;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  color: var(--text2);
  padding: 0.55rem 0.7rem;
  user-select: none;
}}
.prose-blk .detail summary::-webkit-details-marker {{ display: none; }}
.prose-blk .detail summary::before {{
  content: "▸";
  font-size: 0.65rem;
  color: var(--acc);
  transition: transform .2s;
}}
.prose-blk .detail[open] summary::before {{ transform: rotate(90deg); }}
.prose-blk .detail .mono, .prose-blk .detail > :not(summary) {{ margin: 0; border: 0; border-top: 1px solid var(--line); background: var(--card); border-radius: 0; padding: 0.75rem 0.8rem; }}
.mono {{
  white-space: pre-wrap;
  font-size: 0.86rem;
  line-height: 1.6;
  color: var(--text2);
  word-break: break-word;
}}
.history-block {{
  margin-top: 1.75rem;
  padding: 0.2rem 0 0.5rem;
  border-top: 1px solid var(--line);
}}
.history-block details.detail {{
  border: 1px solid var(--line);
  border-radius: var(--r);
  background: var(--acc-ghost);
  overflow: hidden;
}}
.history-block .detail summary {{ padding: 0.65rem 0.9rem; font-size: 0.78rem; font-weight: 600; letter-spacing: 0.04em; text-transform: uppercase; color: var(--text2); cursor: pointer; list-style: none; }}
.history-block .history-list {{ padding: 0.4rem 0.55rem 0.55rem; background: var(--card); max-height: 12rem; overflow-y: auto; display: flex; flex-direction: column; gap: 2px; }}
.history-list a {{
  display: block;
  color: var(--text2);
  text-decoration: none;
  font-size: 0.8rem;
  padding: 0.45rem 0.55rem;
  border-radius: 6px;
  transition: background .12s, color .12s;
}}
.history-list a:hover {{
  color: var(--acc);
  background: var(--acc-ghost);
}}
.footer {{
  color: var(--muted);
  font-size: 0.78rem;
  margin: 2rem 0 0.5rem;
  padding-top: 1.25rem;
  border-top: 1px solid var(--line);
  letter-spacing: 0.02em;
}}
"""

def _join_links(it: Dict[str, Any]) -> str:
    parts = []
    if it.get("html_url"): parts.append(f'<a href="{_esc(it["html_url"])}">Abs</a>')
    if it.get("pdf_url"):  parts.append(f'<a href="{_esc(it["pdf_url"])}">PDF</a>')
    if it.get("code_urls"):
        for i,u in enumerate(it["code_urls"][:3]): parts.append(f'<a href="{_esc(u)}">Code{i+1}</a>')
    if it.get("project_urls"):
        for i,u in enumerate(it["project_urls"][:2]): parts.append(f'<a href="{_esc(u)}">Project{i+1}</a>')
    return " · ".join(parts)

def _card(it: Dict[str, Any],
          trans_zh: Optional[Dict[str,str]],
          sum_zh: Optional[Dict[str,str]],
          sum_en: Optional[Dict[str,str]]) -> str:
    t = it.get("title") or ""
    au = ", ".join(it.get("authors") or [])
    venue = it.get("venue_inferred") or (it.get("journal_ref") or "")
    pub = it.get("published") or "—"
    upd = it.get("updated") or "—"
    comm = it.get("comments") or ""
    absu = it.get("summary") or ""

    zh_title = (trans_zh or {}).get("title_zh")
    zh_abs   = (trans_zh or {}).get("summary_zh")

    # 新的双语总结（来自 summarizer）
    digest_en = (sum_en or {}).get("digest_en") or (sum_zh or {}).get("digest_en") or ""
    digest_zh = (sum_zh or {}).get("digest_zh") or (sum_en or {}).get("digest_zh") or ""

    parts = [f'<article class="paper">', f'<h2 class="title">{_esc(t)}</h2>']

    # 元信息分行
    parts.append(f'<div class="meta-line"><b>Authors</b> · {_esc(au)}</div>')
    if venue:
        parts.append(f'<div class="meta-line"><b>Venue</b> · {_esc(venue)}</div>')
    parts.append(f'<div class="meta-line"><b>First</b> {_esc(pub)} · <b>Latest</b> {_esc(upd)}</div>')
    if comm:
        parts.append(f'<div class="meta-line"><b>Comments</b> · {_esc(comm)}</div>')

    # 链接
    links = _join_links(it)
    if links:
        parts.append(f'<div class="doc-links">{links}</div>')

    has_body = bool(absu or zh_abs or zh_title or digest_en or digest_zh)
    if has_body:
        parts.append('<div class="prose-blk">')

    # 摘要（英文原文，可折叠）
    if absu:
        parts.append('<details class="detail"><summary>Abstract</summary>')
        parts.append(f'<div class="mono">{_esc(absu)}</div></details>')

    # 中文标题/摘要（可选）
    if zh_abs or zh_title:
        parts.append('<details class="detail"><summary>中文标题/摘要</summary>')
        if zh_title:
            parts.append(f'<div class="mono"><b>标题</b> {_esc(zh_title)}</div>')
        if zh_abs:
            parts.append(f'<div class="mono" style="margin-top:6px">{_esc(zh_abs)}</div>')
        parts.append('</details>')

    # 双语总结
    if digest_en or digest_zh:
        parts.append('<details class="detail"><summary>Summary / 总结</summary>')
        if digest_en:
            parts.append(f'<div class="mono">{_esc(digest_en)}</div>')
        if digest_zh:
            parts.append(f'<div class="mono" style="margin-top:6px">{_esc(digest_zh)}</div>')
        parts.append('</details>')

    if has_body:
        parts.append('</div>')

    parts.append('</article>')
    return "\n".join(parts)


def _write(path: str, text: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f: f.write(text)

def _build_page(title: str, sub: str, cards_html: str, history_html: str,
                theme_mode: str, accent: str) -> str:
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    js = f"""
<script>
(function() {{
  const root = document.documentElement;
  function apply(t) {{
    if (t==='dark') root.setAttribute('data-theme','dark');
    else if (t==='light') root.removeAttribute('data-theme');
    else {{
      if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches)
        root.setAttribute('data-theme','dark');
      else root.removeAttribute('data-theme');
    }}
  }}
  let t = localStorage.getItem('theme') || '{theme_mode}';
  if (!['light','dark','auto'].includes(t)) t='light';
  apply(t);
  window.__toggleTheme = function() {{
    let cur = localStorage.getItem('theme') || '{theme_mode}';
    if (cur==='light') cur='dark';
    else if (cur==='dark') cur='auto';
    else cur='light';
    localStorage.setItem('theme', cur);
    apply(cur);
    const el=document.getElementById('theme-label');
    if(el) el.textContent = cur.toUpperCase();
  }}
  window.__expandAll = function(open) {{
    document.querySelectorAll('details').forEach(d => d.open = !!open);
  }}
}})();
</script>
"""
    font_links = """
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@500;600;700&family=Plus+Jakarta+Sans:wght@400;500;600&display=swap" rel="stylesheet" />
"""
    controls = """
<div class="toolbar" role="toolbar" aria-label="View options">
  <button type="button" class="btn" onclick="__toggleTheme()">Theme <span id="theme-label" style="margin-left:4px">AUTO</span></button>
  <button type="button" class="btn" onclick="__expandAll(true)">Expand all</button>
  <button type="button" class="btn" onclick="__expandAll(false)">Collapse all</button>
</div>
"""
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8" /><meta name="viewport" content="width=device-width,initial-scale=1" />
<title>{_esc(title)}</title>{font_links}<style>{_css(accent)}</style>{js}</head>
<body>
  <div class="container">
    <header class="app-header">
      <h1>{_esc(title)}</h1>
      <div style="display:flex;flex-wrap:wrap;gap:10px;align-items:center;justify-content:flex-end">
        {controls}
        <time class="badge-time" datetime="{_esc(now)}">{_esc(now)}</time>
      </div>
    </header>
    <div class="lead-row">
      <p class="page-sub">{_esc(sub)}</p>
    </div>
    <div class="row" role="feed" aria-label="Papers">{cards_html}</div>
    <div class="history-block">
    <details class="detail"><summary>Archive / history</summary>
      <nav class="history-list" aria-label="Past digests">{history_html}</nav>
    </details>
    </div>
    <div class="footer">Generated by arxiv-tracker</div>
  </div>
</body></html>
"""

def _history_list(archive_dir: str, keep: int) -> List[str]:
    if not os.path.isdir(archive_dir):
        return []
    files = [f for f in os.listdir(archive_dir) if f.endswith(".html")]
    files.sort(reverse=True)
    files = files[:keep]
    links = []
    for f in files:
        date = f.replace(".html","")
        links.append(f'<a href="archive/{_esc(f)}">{_esc(date)}</a>')
    return links

def generate_site(items: List[Dict[str,Any]],
                  summaries_zh: Dict[str,Dict[str,str]],
                  summaries_en: Dict[str,Dict[str,str]],
                  translations: Dict[str,Dict[str,str]],
                  site_dir: str, site_title: str = "arXiv Results",
                  keep_runs: int = 60,
                  theme: str = "light",
                  accent: Optional[str] = None) -> Dict[str,str]:
    stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M")
    archive_dir = os.path.join(site_dir, "archive")
    os.makedirs(archive_dir, exist_ok=True)
    open(os.path.join(site_dir, ".nojekyll"), "w").close()

    cards = []
    for it in items:
        sid = it.get("id") or ""
        cards.append(_card(it, translations.get(sid), summaries_zh.get(sid), summaries_en.get(sid)))
    cards_html = "\n".join(cards)
    hist_html = "\n".join(_history_list(archive_dir, keep_runs))

    acc = (accent or "#2563eb").strip()

    arch_html = _build_page(site_title, f"Snapshot: {stamp}", cards_html, history_html=hist_html,
                            theme_mode=theme, accent=acc)
    arch_path = os.path.join(archive_dir, f"{stamp}.html")
    _write(arch_path, arch_html)

    index_html = _build_page(site_title, "Latest digest", cards_html, history_html=hist_html,
                             theme_mode=theme, accent=acc)
    index_path = os.path.join(site_dir, "index.html")
    _write(index_path, index_html)

    return {"index_path": index_path, "archive_path": arch_path, "stamp": stamp}

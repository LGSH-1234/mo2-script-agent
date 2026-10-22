---
name: "ugc-geo-zhen-duan"
display_name: "GEO诊断"
short_description: 诊断网站能否被AI搜索引用，输出评分与可执行修复清单
default_prompt: 帮我做一次 GEO 诊断，网站是 https://example.com
version: 1.1.0-platform
description: "诊断网站能否被AI搜索引用，输出评分与可执行修复清单。"
tools: [ sandbox_generate_image, render_video, sandbox_generate_video, sandbox_process_video ]
---

# geo-audit

Diagnose and improve content visibility across AI search systems.
Traditional SEO gets you ranked. GEO gets you **cited**.

This is a self-contained diagnostic skill: every check is performed by
fetching a small, fixed set of URLs directly and analysing the response
yourself. No external scripts or executables are required or bundled —
follow the parsing rules in `references/technical-checks.md` exactly as
written; they replicate a deterministic checker line for line.

## Security Boundaries

Before running any check:

- Only fetch publicly accessible URLs provided by the user
- Do not fetch localhost, private IPs (10.x, 192.168.x, 172.16–31.x), or .local / .internal domains
- Do not bypass authentication or scrape paywalled content
- Only fetch the specific paths listed in Phase 1 (robots.txt, llms.txt, llms-full.txt, sitemap.xml and at most 3 sub-sitemaps, the homepage, and up to 3 spot-check pages) — never crawl links beyond that fixed list
- For third-party presence checks, ask the user to supply evidence; do not scrape competitor or review sites

## Phase 0 — Start Immediately

**Run the audit now. Do not ask questions first.**

1. Extract the URL from the user's message. If no URL was given, ask for one — that is the only required input.
2. Check if the user already mentioned a brand name in their message. If yes, use it in the report header. If not, use the domain name.
3. If the current environment can access a project file system and `.agents/geo-audit-context.md` exists there, read it for additional context (brand, industry, market, platforms, queries, competitors). If the environment has no file access, skip this step silently.
4. Run the audit (see Phase 1). Do **not** ask the user to fill in industry, platforms, queries, competitors, or market before running.

After the audit is complete and results are shown, you may briefly note (in one sentence) that providing brand/industry/market context up front improves presence scoring — but only if presence was marked unknown.

## Phase 1 — Technical Checks (fetch + parse yourself)

Run these checks in sequence. Each is one or two HTTP GET requests. Apply the
exact parsing rules in `references/technical-checks.md` — do not eyeball the
HTML; follow the field definitions and scoring inputs literally so results
are reproducible.

**Step 1 — robots.txt** — fetch `{url}/robots.txt`.
Classify each AI crawler in the bot table (`references/technical-checks.md` §1)
as `allowed` / `blocked` / `not-mentioned` / `unknown` using the longest-match
rule described there. Also collect any `Sitemap:` directives.

**Step 2 — llms.txt and llms-full.txt** — fetch `{url}/llms.txt` and
`{url}/llms-full.txt`. Check for title (`# `), description (`> `), sections
(`## `), and links (`- [`) per §2. Absence never reduces the score — bonus signal only.

**Step 3 — sitemap.xml** — try the `Sitemap:` URLs from Step 1 first, then
`{url}/sitemap.xml`, then `{url}/sitemap_index.xml` (§3). Extract total page
count, blog-post count, most recent `<lastmod>`, and pick up to 3 sample URLs
spanning about/team, a blog post, and a product/tool page — these become your
spot-check targets in Step 5.

**Step 4 — homepage inspection** — fetch `{url}/` and apply §4: extract
JSON-LD + microdata schema types, compare against the recommended set for a
homepage (`Organization`, `WebSite`), check required attributes (e.g.
`Organization.sameAs`, `Organization.logo`), and extract meta title/description/canonical
and heading hierarchy.

**Step 5 — spot-check 2–3 pages** using the sample URLs from Step 3 (one from
each category: about/team, blog post, product/tool page). For each, repeat
the §4 schema/meta/heading checks plus the §5 content-structure heuristic
(extractable block types, quotable passages, confidence level).

Record every finding — these populate the "关键证据" section of the report.

## Phase 2 — Three-Pillar Evaluation

After the technical checks, evaluate the three GEO pillars using the reference modules:

- **Structure** → `references/structure.md` — content extractability
- **Authority** → `references/authority.md` — credibility signals
- **Presence** → `references/presence.md` — third-party footprint (evidence-based, see note below)

**Presence note:** These checks cannot be automated by fetching the user's own
site — Zhihu, Wikipedia, Baidu Baike, G2, and media coverage live elsewhere.
Ask the user to confirm or search for:
- Does the brand have a Zhihu topic or answers? (知乎)
- Is it listed on Wikipedia or Baidu Baike (百度百科)?
- Any review platform listings (G2, Capterra, Trustpilot, 36Kr, etc.)?
- Media / industry blog mentions in the past 12 months?
- Competitor comparison articles that include the brand?

Score this dimension only from confirmed evidence. Mark as `unknown` if evidence is not provided.

## Phase 2b — Citation Evidence (Optional, Evidence-Based)

If the user has tested AI platforms manually, ask for their findings using this structure:

> "Have you searched for [top queries] on ChatGPT, Perplexity, or Chinese platforms? If so, did [Brand] appear? Was the official URL cited?"

Record results using the citation matrix in `references/citation.md`. Use confirmed citations to:
- Adjust presence scoring (social/media/review counts)
- Identify which failure taxonomy codes apply (T-ACCESS, C-MATCH, A-AUTH, etc.)
- Prioritise recommendations (fix what is causing the specific failure)

If the user has no citation evidence yet, skip this phase and note in the report that presence scoring is `unknown`.

## Phase 3 — Score and Report

Scoring model (100 points total). Compute every sub-signal by hand using the
tables in `references/scoring.md` — there is no separate scoring tool, the
formulas are the specification:

| Dimension | Weight | Notes |
|-----------|--------|-------|
| Structure extractability | 30 | From Phase 1 Steps 4–5 |
| Authority / credibility | 25 | From Phase 1 + user evidence |
| Third-party presence | 25 | Evidence-based; `unknown` if not provided |
| Technical accessibility | 20 | From Phase 1 Steps 1–4 |

See `references/scoring.md` for the full breakdown, the veto gate
(`V-ACCESS`: caps the score at 40 when an AI crawler is blocked at high risk,
or the page is unreachable), and the verdict (🟢 可引用 / 🟡 需修复 / 🔴 被阻断).

**Maturity levels:**

| Level | Score | Description |
|-------|-------|-------------|
| 1 | 0–20 | AI crawlers blocked or unreachable |
| 2 | 21–40 | Reachable but rarely cited |
| 3 | 41–60 | Occasionally cited |
| 4 | 61–80 | Regularly cited |
| 5 | 81–100 | High-frequency citation, strong authority |

## Phase 4 — Platform-Specific Guidance

After scoring, provide targeted recommendations for the user's selected AI platforms. Each platform has different citation patterns and optimisation levers. See `references/platforms.md` for platform-by-platform guidance with confidence levels (`confirmed`, `likely`, `hypothesis`).

If the user specified target platforms in their message or context file, focus recommendations on those. Otherwise, default to the top global platforms (ChatGPT, Perplexity, Google AI Overviews) plus the top China platforms (DeepSeek, Doubao, ERNIE Bot) when market context suggests China.

## Phase 4b — Apply Fixes (audit → fix closure)

If this environment can write files into the user's own project (and the
audited site's source is there — check config files, `package.json`
homepage, CNAME, or ask the user), **offer to implement the P0 fixes
directly** instead of only listing them:

1. **llms.txt** — draft a pre-filled version using the template in
   `references/technical-checks.md` §6, filled with real data from the audit
   (site name, description, key pages). Review any placeholder before writing.
2. **JSON-LD** — insert the Organization / Article / Product / FAQPage schema
   snippets from `references/technical-checks.md` §6 into the site's layout
   or template files, filled with real site data from the audit.
3. **canonical / meta** — add missing tags to the HTML head template.

This closes the loop: diagnose → fix in one session. Never write into the
skill's own files; only write into the user's own project after confirming
file paths with them.

If the environment cannot write files, or the site source isn't available,
output the generated llms.txt content and code snippets directly in the
conversation for the user to copy.

## Phase 5 — Monitoring

Provide a monitoring plan using `references/monitor.md`. Include:
- Recommended tools for the user's market (global vs. China)
- Monthly audit cadence
- KPIs to track

## Output Format

Write the report directly in the conversation — this is the full analysis, not a raw data dump.

```
## GEO 诊断报告 — {Brand}（{Date}）
**目标网站**: {URL}
**行业/市场**: {industry / market if known}
**诊断方法**: robots.txt、llms.txt、Schema、内容结构（首页检测）+ sitemap 概览 + {N} 个页面抽查

### 总体结论

[2–3 句话：当前 GEO 状态 + 最大短板 + 优先方向。不要只罗列发现，要给出判断。
例："站内内容主题集中，但首页缺少机器可读的实体信号（Organization schema、canonical），
文章页无作者/日期 schema，使 AI 系统难以判断权威性，这是当前被引用率低的核心原因。"]

### GEO 得分

| 维度 | 得分 | 判断 |
|------|-----:|------|
| 技术可访问性 | XX/20 | [一句话] |
| 内容可摘取性 | XX/30 | [一句话] |
| 实体与权威信号 | XX/25 | [一句话] |
| 第三方存在感 | XX/25 或 unknown | [一句话] |
| **总分** | **XX/100** | **Level X：[描述]** |

### 关键证据

列出每个检查点的具体发现（有 URL 就带 URL）：

- `robots.txt` — [是否允许主流 AI 爬虫]
- `/llms.txt` — [存在/404/内容质量]
- `/sitemap.xml` — [共 N 个页面，M 篇博客，最近更新 YYYY-MM-DD]
- `/`（首页）— [发现哪些 schema，缺哪些，是否有 canonical]
- `/{about-page}` — [抽查结果：有无 Person/Organization schema]
- `/{blog-post}` — [抽查结果：有无 BlogPosting/Article、作者、日期]
- `/{tool-or-product-page}` — [抽查结果：有无 WebApplication/Product schema]

### P0：本周做

[最高优先级，1–3 项，每项必须包含可直接复制的代码示例]

**1. 上线 /llms.txt**（如果缺失）

给出完整的 llms.txt 内容模板，填入该站点的实际信息：
```txt
# {domain}

> {一句话站点定位}

## Key pages
- Home: {url}/
- {页面名}: {url}/{path}
...

## Core topics
- {主题 1}
- {主题 2}
```

**2. 首页补 canonical + Organization JSON-LD**（如果缺失）

给出完整代码，用实际品牌名/URL/描述填充占位符。

**3. FAQ / FAQPage JSON-LD**（如果首页有 FAQ 文案但无 schema）

给出完整代码示例。

### P1：本月做

[中优先级，2–4 项，可以只给指导方向，不强制要代码]

**4. 博客模板补 BlogPosting JSON-LD + 作者 + 日期**
**5. 每篇核心文章加可引用摘要（40–80 字，开头给结论）**
**6. 建立核心主题 Hub 页**

### P2：持续做

**7. 建立第三方存在感**（知乎、GitHub、小红书/公众号、工具目录、Wikipedia/百度百科）
**8. 文章增加数据与外部引用**

### 推荐监控

每月人工测试以下查询，记录 ChatGPT、Perplexity、Google AI Overviews、DeepSeek、豆包是否引用本站：

- {根据站点主题生成 7–10 个具体查询，不要写通用占位符，要是真实的搜索问题}
```

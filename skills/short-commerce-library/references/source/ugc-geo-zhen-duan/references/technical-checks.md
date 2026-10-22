# Technical Checks Reference

Exact parsing rules for Phase 1. These replicate a deterministic checker —
follow them literally rather than eyeballing pages, so two runs of the same
site produce the same result.

---

## §1 — robots.txt (AI crawler access)

Fetch `{url}/robots.txt`. If the request fails or returns a non-200 status,
mark every crawler below as `unknown` and note the page as unreachable
(this triggers the `V-ACCESS` veto — see `scoring.md`).

**Bot table:**

| Crawler UA | Platform | Confidence | Role |
|---|---|---|---|
| `GPTBot` | ChatGPT | confirmed | training |
| `OAI-SearchBot` | ChatGPT Search | confirmed | search |
| `ClaudeBot` | Claude (Anthropic) | confirmed | general |
| `anthropic-ai` | Claude (alternate UA) | confirmed | general |
| `PerplexityBot` | Perplexity | confirmed | search |
| `Bytespider` | Doubao / ByteDance (豆包) | confirmed | indexing |
| `Baiduspider` | ERNIE Bot / Baidu (文心一言) | confirmed | indexing |
| `Googlebot` | Google AI Overviews | confirmed | search |
| `Bingbot` | Copilot / Bing AI | confirmed | search |
| `meta-externalagent` | Meta AI | likely | general |

**Classification algorithm** (four states: `allowed` / `blocked` /
`not-mentioned` / `unknown`):

1. Parse the file into `User-agent:` blocks. A new `User-agent:` line right
   after a block of `Allow:`/`Disallow:` rules starts a fresh block; consecutive
   `User-agent:` lines with no rules between them belong to the same block
   (rules apply to all of them).
2. For the target crawler's path (the audited URL's path, default `/`):
   - If the crawler is named explicitly in any block, use only that block's rules.
   - Otherwise, fall back to the `*` (wildcard) block's rules, and the result
     can only be `not-mentioned` (not `blocked`) — a wildcard disallow does not
     count as an explicit block of a named crawler, it just means the crawler
     was never addressed.
3. Among the applicable rules, find the **longest matching path** (wildcard
   `*` and trailing `$` don't count toward length; ties go to `Allow`).
4. If no rule matches, or the best rule is `Allow`, or the crawler wasn't
   named at all → the fallback-only branch is `not-mentioned`; the
   named-crawler branch with no matching rule is `allowed`.
5. If the best matching rule for a named crawler is `Disallow` with a
   non-empty path → `blocked`.

**citationRisk** (drives the veto gate):
- `blocked` + role `search`/`indexing`/`general` → **high**
- `blocked` + role `training` → **medium**
- `not-mentioned` + role `search`/`indexing` → **low**
- anything else → **none**

Also collect any `Sitemap:` directive lines — feed these into §3 as
candidate sitemap URLs before trying the default paths.

---

## §2 — llms.txt / llms-full.txt

Fetch `{url}/llms.txt` and `{url}/llms-full.txt` separately (both are checked;
neither missing file reduces the score — bonus signal only).

For each that returns 200, check for these markers (multiline, start-of-line):

| Field | Marker | Required |
|---|---|---|
| Title | `# ` | yes |
| Description | `> ` | yes |
| Sections | `## ` | no |
| Links | `- [` | no |

`requiredMet` = title AND description both present. Report completeness as
`N/4` fields found. A 404 means "not present" — never treat as a deduction.

---

## §3 — sitemap.xml

Try, in order, until one returns 200 and contains `<loc>`:
1. Each `Sitemap:` URL collected from robots.txt (§1)
2. `{origin}/sitemap.xml`
3. `{origin}/sitemap_index.xml`

Parse all `<loc>…</loc>` values. If every value ends in `.xml` and there are
no non-`.xml` page URLs, this is a sitemap **index** — follow up to 3 of the
sub-sitemaps and union their `<loc>` values as the page list (don't go deeper
than one level).

From the final page-URL list:
- `totalUrls` = count of non-`.xml` URLs
- Classify into buckets by path pattern: blog (`/blog/`, `/post/`, `/article/`, `/news/`), tools/product (`/tool`, `/product`, `/service`), about (`/about`, `/team`, `/contact`)
- `blogCount` / `pageCount` = blogCount vs. everything else
- `lastmod` = the last `<lastmod>` value found in the sitemap body (most recently listed, not necessarily max — matches how the file lists it)
- Sample URLs for spot-checking (Phase 1 Step 5): first about URL + first tool URL + the middle blog URL (`blogUrls[floor(len/2)]`), capped at 3 total

If no sitemap is found after all three attempts, report it as missing (not an error) and skip Step 5's sitemap-derived samples — ask the user for 2–3 representative URLs instead, or use the homepage plus any URLs visible in top navigation.

---

## §4 — Page inspection (schema, meta, headings)

Fetch the page HTML directly (no JS rendering — inspect the raw response
body, which is what most AI crawlers see too).

**Schema extraction:**
- JSON-LD: every `<script type="application/ld+json">…</script>` block, JSON-parsed. If a block has `@graph`, walk its array too. Collect the `@type` value(s) (can be a string or array) from every item.
- Microdata: every `itemtype="https://schema.org/X"` (or `http://`) attribute, collect `X`.
- Union both sources into one `schemaTypes` set.

**Page-type detection** (schema-first, then URL fallback):
1. If `schemaTypes` includes `BlogPosting`/`Article`/`NewsArticle` → `article`
2. Else if it includes `Product`/`WebApplication`/`SoftwareApplication` → `product`
3. Else if it includes `FAQPage` → `faq`
4. Else if it includes both `ItemList` and `Product` → `comparison`
5. Else fall back to URL path: `/` → `homepage`; `/blog|/post|/article|/news` → `article`; `/about|/team|/company` → `about`; `/product|/tool|/app|/service` → `product`; `/faq|/help` → `faq`; `/vs-|/compare|/alternative` → `comparison`; `/pricing` → `pricing`; else `general`

**Recommended schema by page type** — flag anything missing:

| Page type | Recommended types |
|---|---|
| homepage | Organization, WebSite |
| article | Article, BreadcrumbList |
| product | Product, AggregateRating |
| about | Person, Organization |
| faq | FAQPage |
| comparison | ItemList, FAQPage |
| pricing | Product |
| general | WebPage |

**Required attributes per found type** — for every schema type actually
present, check whether these properties exist on the JSON-LD object; list any
missing as `{Type}.{property}` (this is the "Schema attribute gaps" evidence):

| Type | Required properties |
|---|---|
| Organization | name, url, description, sameAs, logo |
| WebSite | name, url |
| Article | headline, author, datePublished, publisher |
| BlogPosting | headline, author, datePublished, dateModified, publisher |
| NewsArticle | headline, author, datePublished, publisher |
| Product | name, description, offers |
| WebApplication | name, description, offers, applicationCategory |
| SoftwareApplication | name, description, offers, applicationCategory |
| FAQPage | mainEntity |
| Person | name, jobTitle, sameAs |

**Meta:** `<title>`, `<meta name="description">`, `<link rel="canonical">` — presence and content.

**Headings:** strip `<nav>`, `<footer>`, `<aside>` first (avoid counting site
chrome). Count H1/H2/H3. `hasProperHierarchy` = exactly one H1 AND at least one H2.

**Author/date signals:**
- `hasAuthor`: an element/class/id containing "author" or "byline", OR a JSON-LD `"author":` field, OR `rel="author"`
- `hasPublishDate`: a `<time datetime>` attribute, OR JSON-LD `"datePublished":`, OR text like "published_at"/"publish-date"/"post_date"
- `hasModifiedDate`: JSON-LD `"dateModified":`, OR text like "modified_at"/"updated_at"/"last-modified"

**External links:** count distinct hostnames in `href="https?://…"` attributes that differ from the page's own hostname.

---

## §5 — Content structure heuristic (confidence: low/medium — not semantic understanding)

Run on the plain text extracted from the page (strip `<script>`, `<style>`,
`<nav>`, `<footer>`, then strip remaining tags and collapse whitespace).

Split into sentences on `. ! ? 。！？`. For each sentence, test:

| Signal | Pattern (EN) | Pattern (ZH) |
|---|---|---|
| Question | `what/how/why/when/where/who/which/is/are/can/does/do/will/should/was/were` as a word | `是什么/怎么/为什么/如何/哪些/什么是/怎样/有哪些` after a CJK char |
| Definition | `is / refers to / means / defined as / is a / is an` | `是指/即/指的是/是一种/是一个` after a CJK char |
| Statistic | a `%` figure, or a number followed by 万/百万/亿/billion/million/thousand | (shared pattern) |
| Source citation | `来源：/数据来自/Source:/according to/cited from/引用自` | (shared pattern) |

Count sentences matching each. Also count `<ol>` list items and test each for
a step prefix (`step N`, `第N步`, `一、二、三…`, `N. `) OR check whether the URL
or any H1/H2 contains how-to/guide/tutorial/steps/步骤/教程/方法/指南/操作/安装/部署/配置 context.

**Extractable block flags** (each true/false):
- `hasFirstScreenDefinition`: a definition pattern matches within the first 300 characters of text
- `hasStepBlocks`: ≥2 `<ol>` items AND (a step-prefixed item OR how-to context in URL/headings)
- `hasStatistics`: ≥2 statistic sentences
- `hasCitations`: ≥1 source-citation sentence
- `hasDefinitionBlocks`: ≥2 definition sentences
- FAQ present: `FAQPage` JSON-LD or a `class`/`id` containing "faq"

`extractableBlockCount` = count of true flags above (0–6).

**Quotable blocks** (candidates the report can quote verbatim): up to 2
definition sentences (30–200 chars), up to 2 statistic sentences (20–200
chars), and 1 question→answer sentence pair (question ≤100 chars, followed by
an answer sentence 20–200 chars). Missing block types = whichever of
`definition / statistic / step / citation / faq / qa` produced zero
candidates — list these explicitly in the report as "缺失的可引用内容类型".

**Paragraph metrics:** paragraph count (`<p>` tags), average words per
paragraph = word count ÷ paragraph count.

**Confidence:** count how many of these hold: sentence count > 10, paragraph
count > 3, structural-element count (tables+lists+details) > 0, heading depth
(how many of H1/H2/H3 are non-empty) ≥ 2. If ≥3 hold → `medium`, else `low`.
Always state the confidence level next to any content-structure finding —
never present it as certain.

**Interpretation flags:**
- `likelyExtractable`: extractableBlockCount ≥ 2, OR structural elements ≥ 2, OR heading depth ≥ 2, OR FAQ schema present
- `selfContainedParagraphs`: avg words/paragraph between 40 and 200
- `richInQA`: ≥3 question sentences

---

## §6 — Fix templates (Phase 4b)

**llms.txt skeleton:**

```
# {Site Name}
> {One or two sentences describing what this site is and who it's for.}

## {Section: e.g. Docs, Blog, API, Products}
- [{Page Title}]({https://example.com/page}): {One-line description}
- [{Page Title}]({https://example.com/page-2}): {One-line description}

## About
- [{About Us}]({https://example.com/about}): {Company background and mission}
```
Keep descriptions factual and concise — AI systems parse these literally.
Place at the domain root: `https://yourdomain.com/llms.txt`.

**FAQPage JSON-LD:**

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "What is {Your Product/Service}?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "{A clear, self-contained answer AI systems can extract directly.}"
      }
    }
  ]
}
```

**Article JSON-LD:**

```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "{Article Title — under 110 characters}",
  "description": "{One-sentence summary}",
  "image": "{https://example.com/images/article-image.jpg}",
  "datePublished": "{YYYY-MM-DD}",
  "dateModified": "{YYYY-MM-DD}",
  "author": { "@type": "Person", "name": "{Author Full Name}", "url": "{https://example.com/authors/name}", "jobTitle": "{Job Title}" },
  "publisher": { "@type": "Organization", "name": "{Publisher Name}", "logo": { "@type": "ImageObject", "url": "{https://example.com/logo.png}" } },
  "mainEntityOfPage": { "@type": "WebPage", "@id": "{https://example.com/article-url}" }
}
```

**Product JSON-LD:**

```json
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "{Product Name}",
  "description": "{What it does, who it's for, key benefits}",
  "image": "{https://example.com/images/product.jpg}",
  "brand": { "@type": "Brand", "name": "{Brand Name}" },
  "offers": { "@type": "Offer", "priceCurrency": "{USD|CNY}", "price": "{0.00}", "availability": "https://schema.org/InStock", "url": "{https://example.com/product}" }
}
```

**robots.txt AI-crawler allow block** (append to the existing file):

```
User-agent: GPTBot
Allow: /

User-agent: OAI-SearchBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: anthropic-ai
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Bytespider
Allow: /

User-agent: Baiduspider
Allow: /

User-agent: meta-externalagent
Allow: /
```

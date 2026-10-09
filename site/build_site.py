"""AXblog 포털 생성기.

- site/catalog.json 의 카테고리·질문 목록을 읽고,
- 각 질문 폴더(<카테고리>/<질문>/article_rN.html)에서 아티클을 찾아
- site/dist/ 에 포털(index.html)과 회차별 아티클 페이지를 만든다.

새 질문·새 회차 아티클이 생기면 이 스크립트만 다시 돌리면 포털에 붙는다.
catalog.json 에 없는 질문 폴더도 아티클이 있으면 자동으로 포함한다.
"""
import html, json, re, shutil, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
DIST = SITE / "dist"
E = html.escape

cat = json.loads((SITE / "catalog.json").read_text(encoding="utf-8"))

def text_of(fragment):
    fragment = re.sub(r'<a class="rid"[^>]*>.*?</a>', "", fragment, flags=re.S)
    return html.unescape(re.sub(r"<[^>]+>", "", fragment)).strip()

def parse_article(path):
    s = path.read_text(encoding="utf-8")
    def grab(pat):
        m = re.search(pat, s, re.S)
        return text_of(m.group(1)) if m else ""
    question = re.sub(r"^고정 질문 v[\d.]+ — ", "", grab(r'<p class="question">(.*?)</p>'))
    qver = (re.search(r"고정 질문 (v[\d.]+)", s) or [None, ""])[1]
    date = (re.search(r"R\d+ [^<]*?· (\d{4}-\d{2}-\d{2})", s) or [None, ""])[1]
    nrec = (re.search(r"4유형 기록 (\d+)건", s) or [None, ""])[1]
    return {"html": s, "title": grab(r"<h1>(.*?)</h1>"), "question": question, "qver": qver,
            "answer": grab(r'<p class="answer[^"]*">(.*?)</p>'), "date": date, "records": nrec}

def rounds_of(qdir):
    out = []
    for p in qdir.glob("article_r*.html"):
        m = re.match(r"article_r(\d+)\.html$", p.name)
        if m:
            out.append((int(m.group(1)), p))
    return sorted(out)

SITEBAR_CSS = """
.sitebar { position: sticky; top: env(safe-area-inset-top, 0px); z-index: 10; background: var(--paper); border-bottom: 1px solid var(--rule);
  margin: 0 -20px; padding: 10px 20px; display: flex; gap: 14px; align-items: center; flex-wrap: wrap; font: 500 13px/1.4 var(--mono); }
.sitebar a { color: var(--ink); text-decoration: none; }
.sitebar a:hover, .sitebar a:focus-visible { text-decoration: underline; }
.sitebar .crumb { color: var(--muted); }
.sitebar .rounds { margin-left: auto; display: flex; gap: 8px; }
.sitebar .rounds a[aria-current="page"] { color: var(--accent); }
"""

def wrap_article(art, crumbs, rounds_html, depth):
    head, body = art["html"].split("<main>", 1)
    up = "../" * depth
    bar = f'<nav class="sitebar" aria-label="사이트"><a href="{up}index.html">AXblog</a><span class="crumb">{crumbs}</span><span class="rounds">{rounds_html}</span></nav>'
    return (f'<!doctype html>\n<html lang="ko"><head><meta charset="utf-8">'
            f'<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">'
            f'{head}<style>{SITEBAR_CSS}</style></head><body>{bar}<main>{body}</body></html>')

# ---------------------------------------------------------------- 수집
if DIST.exists():
    shutil.rmtree(DIST)
DIST.mkdir(parents=True)

pages = []           # (published path, file)
sections = []
latest = []
for c in cat["categories"]:
    cdir = ROOT / c["id"]
    qs = list(c.get("questions", []))
    known = {q["id"] for q in qs}
    if cdir.exists():  # catalog에 없는 질문 폴더 자동 포함
        for d in sorted(p for p in cdir.iterdir() if p.is_dir() and re.fullmatch(r"[a-z]\d+", p.name)):
            if d.name not in known and rounds_of(d):
                qs.append({"id": d.name, "no": d.name.upper(), "area": ""})
    items = []
    for q in qs:
        rs = rounds_of(cdir / q["id"])
        if not rs:
            items.append({"q": q, "status": "planned"})
            continue
        arts = []
        for n, p in rs:
            a = parse_article(p); a["n"] = n
            a["path"] = f'{c["id"]}/{q["id"]}/r{n}.html'
            arts.append(a)
        for a in arts:
            links = " ".join(f'<a href="r{b["n"]}.html"{" aria-current=page" if b["n"]==a["n"] else ""}>R{b["n"]}</a>' for b in arts)
            crumbs = f'/ {E(c["name"])} / {E(q["no"])}'
            out = DIST / a["path"]
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(wrap_article(a, crumbs, links, 2), encoding="utf-8")
            pages.append(a["path"])
        cur = arts[-1]
        items.append({"q": q, "status": "live", "cur": cur, "arts": arts})
        latest.append((cur["date"], c, q, cur))
    sections.append((c, items))

# ---------------------------------------------------------------- 포털
def q_row(c, it):
    q = it["q"]
    if it["status"] == "planned":
        return f"""<li class="qrow planned"><div class="qno"><b>{E(q['no'])}</b><span>{E(q.get('area',''))}</span></div>
  <div class="qbody"><p class="qq">{E(q.get('question','고정 질문 설계 예정'))}</p><p class="qmeta"><span class="pill">준비 중</span></p></div></li>"""
    a = it["cur"]
    older = "".join(f'<a href="{E(b["path"])}">R{b["n"]}</a>' for b in it["arts"][:-1])
    older_html = f' · 이전 회차 {older}' if older else ""
    return f"""<li class="qrow"><div class="qno"><b>{E(q['no'])}</b><span>{E(q.get('area',''))}</span></div>
  <div class="qbody"><h3><a href="{E(a['path'])}">{E(a['title'])}</a></h3>
  <p class="qq">{E(a['question'])}</p>
  <p class="qa">{E(a['answer'])}</p>
  <p class="qmeta"><span class="pill live">R{a['n']}</span><time>{E(a['date'])}</time><span>기록 {E(a['records'])}건</span><span>질문 {E(a['qver'])}</span>{older_html}</p></div></li>"""

sec_html = ""
nav_html = ""
for c, items in sections:
    live = sum(1 for i in items if i["status"] == "live")
    nav_html += f'<a href="#{E(c["id"])}"><b>{c["no"]:02d}</b> {E(c["name"])} <span>{live}/{len(items)}</span></a>'
    if items:
        body = f'<ol class="qlist">{"".join(q_row(c, it) for it in items)}</ol>'
    else:
        body = '<p class="empty">고정 질문을 설계하는 중입니다. 질문이 확정되면 첫 회차 아티클이 이곳에 올라옵니다.</p>'
    sec_html += f"""<section class="cat" id="{E(c['id'])}"><header class="cathead"><span class="catno">{c['no']:02d}</span>
  <div><h2>{E(c['name'])}</h2><p>{E(c['desc'])}</p></div><span class="catcount">아티클 {live}개 · 질문 {len(items)}개</span></header>{body}</section>"""

latest.sort(key=lambda x: x[0], reverse=True)
total_q = sum(len(i) for _, i in sections)
total_live = sum(1 for _, its in sections for i in its if i["status"] == "live")
total_rec = sum(int(i["cur"]["records"] or 0) for _, its in sections for i in its if i["status"] == "live")
last_date = latest[0][0] if latest else "—"

CSS = (ROOT / "customer-lab" / "lib" / "article.css").read_text(encoding="utf-8").split("/* 한 줄 답 */")[0]
PORTAL_CSS = """
/* Layout: 신문 목차 — 카테고리 번호를 큰 숫자로, 질문은 번호 열 + 본문 열의 2단 목록 */
.portal { max-width: 1080px; }
.masthead { display: grid; gap: 14px; padding-bottom: 28px; border-bottom: 2px solid var(--ink); }
.masthead h1 { font: 800 clamp(40px, 7vw, 72px)/1 var(--display); letter-spacing: -0.01em; }
.masthead .tag { font-size: 17px; max-width: 60ch; margin: 0; }
.stats { display: flex; gap: 22px; flex-wrap: wrap; font: 500 13px var(--mono); color: var(--muted); }
.stats b { color: var(--ink); font-weight: 600; font-variant-numeric: tabular-nums; }
.method { font-size: 14px; color: var(--muted); margin: 0; max-width: 72ch; }
.catnav { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 0; border-bottom: 1px solid var(--rule); }
.catnav a { padding: 12px 14px 12px 0; text-decoration: none; color: var(--ink); font-size: 14px; display: grid; gap: 2px; border-right: 1px solid var(--rule); padding-left: 14px; }
.catnav a:first-child { padding-left: 0; }
.catnav a:last-child { border-right: 0; }
.catnav b { font: 600 12px var(--mono); color: var(--accent); }
.catnav span { font: 400 12px var(--mono); color: var(--muted); }
.catnav a:hover b, .catnav a:focus-visible b { text-decoration: underline; }
.cat { display: grid; gap: 0; scroll-margin-top: 20px; }
.cathead { display: grid; grid-template-columns: auto 1fr auto; gap: 18px; align-items: end; padding-bottom: 14px; border-bottom: 1px solid var(--ink); }
.catno { font: 800 56px/0.9 var(--display); color: var(--accent); }
.cathead h2 { font: 600 24px/1.2 var(--display); }
.cathead p { margin: 4px 0 0; color: var(--muted); font-size: 14px; }
.catcount { font: 500 12px var(--mono); color: var(--muted); white-space: nowrap; }
.qlist { list-style: none; margin: 0; padding: 0; }
.qrow { display: grid; grid-template-columns: 170px minmax(0, 1fr); gap: 20px; padding: 20px 0; border-bottom: 1px solid var(--rule); }
.qno b { display: block; font: 600 22px/1.1 var(--mono); }
.qno span { font: 400 12px var(--mono); color: var(--muted); }
.qbody { display: grid; gap: 8px; min-width: 0; }
.qbody h3 { font: 600 20px/1.35 var(--display); }
.qbody h3 a { color: var(--ink); text-decoration: none; background-image: linear-gradient(var(--accent), var(--accent)); background-size: 0 2px; background-repeat: no-repeat; background-position: 0 100%; transition: background-size .2s; }
.qbody h3 a:hover, .qbody h3 a:focus-visible { background-size: 100% 2px; }
.qq { margin: 0; color: var(--muted); font-size: 14px; }
.qa { margin: 0; font-size: 15px; border-left: 2px solid var(--accent); padding-left: 12px; max-width: 75ch; }
.qmeta { margin: 0; display: flex; gap: 12px; flex-wrap: wrap; align-items: center; font: 400 12px var(--mono); color: var(--muted); }
.pill { font: 500 11px var(--mono); padding: 2px 7px; border-radius: 2px; border: 1px solid var(--rule); color: var(--muted); }
.pill.live { border-color: var(--accent); color: var(--accent); }
.qrow.planned .qno b { color: var(--muted); }
.qrow.planned .qq { font-size: 15px; }
.empty { margin: 0; padding: 20px 0; color: var(--muted); font-size: 14px; border-bottom: 1px solid var(--rule); }
footer { font-size: 13px; color: var(--muted); border-top: 1px solid var(--rule); padding-top: 18px; }
@media (prefers-reduced-motion: reduce) { .qbody h3 a { transition: none; } }
@media (max-width: 760px) {
  .catnav { grid-template-columns: 1fr 1fr; }
  .catnav a { border-right: 0; padding-left: 0; }
  .cathead { grid-template-columns: auto 1fr; }
  .catcount { grid-column: 1 / -1; }
  .qrow { grid-template-columns: 1fr; gap: 8px; }
}
"""

portal = f"""<!doctype html>
<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>AXblog</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans+KR:wght@400;500;600&family=Noto+Serif+KR:wght@600;800&display=swap">
<style>{CSS}{PORTAL_CSS}</style></head>
<body><main class="portal">
  <header class="masthead">
    <h1>{E(cat['site']['title'])}</h1>
    <p class="tag">{E(cat['site']['tagline'])}</p>
    <div class="stats"><span>카테고리 <b>{len(sections)}</b></span><span>질문 <b>{total_q}</b></span><span>발행 아티클 <b>{total_live}</b></span><span>근거 기록 <b>{total_rec}</b>건</span><span>최근 업데이트 <b>{E(last_date)}</b></span></div>
    <p class="method">각 질문은 정해진 문장 그대로 매달 다시 조사합니다. 조사 결과는 지표·사건·해석·전망 기록으로 쪼개 저장하고, 아티클은 그 기록에서만 만들어집니다. 글 속 번호를 누르면 근거 기록과 원문 출처로 이동합니다.</p>
  </header>
  <nav class="catnav" aria-label="카테고리">{nav_html}</nav>
  {sec_html}
  <footer><span>AXblog · 원본 기록과 생성 스크립트는 GitHub skykelly/AXblog 저장소에 있습니다.</span></footer>
</main></body></html>
"""
(DIST / "index.html").write_text(portal, encoding="utf-8")
# Claude 아티팩트 게시용 진입 페이지: 게시 시 문서 골격이 자동으로 씌워지므로 doctype·head·body 태그를 뺀다
entry = re.sub(r'^<!doctype html>\s*<html[^>]*><head><meta charset="utf-8"><meta name="viewport"[^>]*>', "", portal)
entry = entry.replace("</head>\n<body>", "").replace("</body></html>", "")
(DIST / "artifact_index.html").write_text(entry, encoding="utf-8")

# ---------------------------------------------------------------- 점검
bad = []
for p in [DIST / "index.html"] + [DIST / x for x in pages]:
    s = p.read_text(encoding="utf-8")
    for href in re.findall(r'href="([^"#:]+\.html)"', s):
        if not (p.parent / href).resolve().exists():
            bad.append(f"{p.relative_to(DIST)} → {href}")
(DIST / "manifest.json").write_text(json.dumps({"pages": pages}, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"포털 생성: 카테고리 {len(sections)}, 질문 {total_q}, 아티클 페이지 {len(pages)}")
print("페이지:", pages)
print("깨진 내부 링크:", bad or "없음")
sys.exit(1 if bad else 0)

"""records.jsonl → 기준 아티클 HTML (C3 R1).
순서: 한 줄 답 → 해석 → 주요 사건 → 전망 → 정보 유형별 지도 → 핵심 지표 → 미확인·경고
"""
import json, html, re, sys
from pathlib import Path

ROOT = Path(__file__).parent
recs = [json.loads(l) for l in (ROOT / "records.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
by = {r["id"]: r for r in recs}
E = html.escape
CSS = (ROOT.parent.parent / "lib" / "article.css").read_text(encoding="utf-8")

def tags(ids):
    return "".join(f'<a class="rid" href="#{E(i)}" title="{E(by[i]["statement"])}">{E(i)}</a>' for i in ids)
def para(text, ids): return f"<p>{E(text)} {tags(ids)}</p>"
def src_links(r):
    return " · ".join(f'<a href="{E(s["url"])}" target="_blank" rel="noopener">{E(s["publisher"])}</a><span class="grade g{E(s["grade"])}">{E(s["grade"])}</span>' for s in r.get("sources", []))

TITLE = "AI가 만든 정보, 소비자는 믿는가"
QUESTION = "소비자가 구매 판단에 쓰는 정보의 원천은 사람이 만든 것에서 AI가 만든 것으로 어디까지 옮겨갔고, 소비자는 그것을 믿는가?"

# 1. 한 줄 답 ----------------------------------------------------------
ONE_LINE = ("2026년 10월 현재 웹에 새로 올라오는 글의 절반은 AI가 쓰고, 소비자는 그 정보를 원문 대신 AI 요약으로 받아본다. 그러나 믿음은 따라오지 않았다. "
            "AI가 전해준 뉴스를 믿는 사람은 5명 중 1명이고, 정작 AI는 브랜드 사이트보다 Reddit·YouTube 같은 사람의 경험담을 가장 많이 인용한다.")
ONE_LINE_BASIS = ["C3-I-001", "C3-I-002", "C3-I-003", "C3-I-004"]
ANSWER_ROWS = [
    ("만드는 쪽", "신규 영문 웹 글의 50.9%가 AI 글이다. AI 생성 의심 Amazon 리뷰는 2022년 대비 약 400% 늘었고, 광고 임원의 83%가 제작에 AI를 쓴다.", ["C3-M-001", "C3-M-002", "C3-M-009"]),
    ("전달 경로", "AI 챗봇에서 원문을 자주 누르는 사람은 4%(검색엔진 19%)다. 퍼블리셔로 가는 Google 검색 유입은 1년 새 40% 줄었다.", ["C3-M-005", "C3-M-006"]),
    ("믿는가", "AI 챗봇 뉴스를 믿는다는 응답은 전체 20%, 이용자 44%다. 젊은 층의 AI 광고 호감은 45%로, 광고주 기대(82%)와 37%p 벌어졌다.", ["C3-M-004", "C3-M-008"]),
    ("AI가 기대는 원천", "AI 검색이 가장 많이 인용하는 곳은 Reddit, YouTube, LinkedIn, Wikipedia 순이다. 사람이 남긴 경험담이 AI 답변의 재료다.", ["C3-M-007"]),
    ("한국", "허위·편향 정보 우려가 64%로 글로벌(52%)보다 높다. AI 기본법(1월)과 공정위 리뷰·가상인물 광고 지침(7월)이 생겼지만, 이용자 리뷰의 AI 사용은 플랫폼마다 대응이 다르다.", ["C3-M-010", "C3-E-001", "C3-E-002", "C3-E-003"]),
]
answer_rows = "".join(f'<div class="arow"><dt>{E(k)}</dt><dd>{E(v)} {tags(ids)}</dd></div>' for k, v, ids in ANSWER_ROWS)

# 2. 해석 --------------------------------------------------------------
NARRATIVE = [
    ("정보를 만드는 일은 이미 절반이 AI로 넘어갔다. Graphite가 Common Crawl에서 뽑은 영문 글 55,400건을 탐지기 3종으로 판정한 결과, 2025년 말 신규 글의 50.9%가 주로 AI가 쓴 글이었다. "
     "ChatGPT 출시 1년 뒤 35.9%, 2년 뒤 48%로 올라간 뒤 2025년 초부터는 절반 안팎에서 멈춰 있다.",
     ["C3-M-001", "C3-I-001"]),
    ("소비자는 그 정보를 원문이 아니라 AI 요약으로 받는다. AI 챗봇으로 매주 뉴스를 보는 사람은 10%(18~24세 17%)로 늘었지만, 챗봇에서 원문을 자주 누르는 사람은 4%뿐이다. "
     "같은 기간 퍼블리셔로 가는 Google 검색 유입은 40.2% 줄었고, AI 챗봇이 보내주는 유입은 전체의 0.01%에 그쳤다. 정보를 만든 원천이 독자를 잃고 있다.",
     ["C3-M-003", "C3-M-005", "C3-M-006", "C3-I-002"]),
    ("이용은 늘었지만 신뢰는 따라오지 않았다. AI 챗봇이 전한 뉴스를 믿는다는 사람은 전체의 20%다. 챗봇 이용자는 44%로 높지만 비이용자는 17%에 그친다. "
     "광고도 같다. 광고 임원의 83%가 AI로 광고를 만들지만, 이를 반기는 젊은 소비자는 45%이고 광고주 기대와의 격차는 37%p로 더 벌어졌다.",
     ["C3-M-004", "C3-M-009", "C3-M-008", "C3-I-003"]),
    ("역설적으로 AI 답변의 재료는 사람의 경험담이다. 미국 AI 검색의 인용 3천만 건을 보면 Reddit과 YouTube가 1·2위다. 반면 리뷰는 AI가 빠르게 파고들어, "
     "AI 생성 의심 Amazon 리뷰가 2022년 대비 약 400% 늘었고 특히 1점·5점 같은 극단 평점에 몰린다.",
     ["C3-M-007", "C3-M-002", "C3-I-004", "C3-I-005"]),
    ("한국은 규제가 먼저 움직였다. 1월 AI 기본법 시행으로 생성형 AI 결과물 표시 의무가 생겼지만 대상은 AI 사업자이고 과태료는 1년 이상 유예됐다. "
     "7월에는 쇼핑몰 리뷰 운영 기준 공개와 AI 가상인물 광고 표시가 도입됐다. 이용자가 AI로 쓰는 리뷰는 무신사처럼 막는 곳과 쿠팡처럼 허용하는 곳으로 갈린다. "
     "한국 소비자의 허위·편향 정보 우려는 64%로 글로벌보다 높다.",
     ["C3-E-001", "C3-E-002", "C3-E-003", "C3-M-010", "C3-I-006"]),
]
narrative_html = "".join(para(t, ids) for t, ids in NARRATIVE)
DIR = {"강화": "up", "약화": "down", "중립": "flat"}
irows = "".join(f"""<tr id="{E(r['id'])}"><td><span class="dir {DIR[r['direction']]}">{E(r['direction'])}</span></td>
  <td class="tgt">{E(r['target'])}</td><td>{E(r['statement'])}</td><td>{tags(r['basis'])}</td><td class="idc"><code>{E(r['id'])}</code></td></tr>"""
  for r in recs if r["type"] == "해석")

# 3. 주요 사건 (최신순) ------------------------------------------------
EVENTS_LEAD = ("이번 회차의 사건은 모두 한국의 신뢰 장치에 관한 것이다. 정부(AI 기본법)와 공정위(리뷰·가상인물 광고)가 표시 규칙을 만들었고, "
               "규칙이 닿지 않는 이용자 리뷰는 플랫폼이 각자 정하고 있다.")
events = sorted([r for r in recs if r["type"] == "사건" and r.get("verified")], key=lambda r: r["date"], reverse=True)
erows = "".join(f"""<li id="{E(r['id'])}"><time>{E(r['date'])}</time><div><b>{E(r['actor'])}</b> {E(r['statement'])}
  <div class="src">{src_links(r)} <code>{E(r['id'])}</code></div></div></li>""" for r in events)

# 4. 전망 --------------------------------------------------------------
FORECAST_LEAD = ("소비자 정보 생태계 관점에서 2027년 말을 기준으로 두 시나리오를 세웠다. 갈림길은 신뢰 장치(표시 의무 집행, 플랫폼의 AI 리뷰 정책, 출처 표시)가 "
                 "AI 정보의 확산 속도를 따라잡느냐다.")
scen = sorted([r for r in recs if r["type"] == "전망" and r.get("scenario")], key=lambda r: 0 if r["scenario"] == "낙관" else 1)
scen_html = ""
for r in scen:
    cls = "opt" if r["scenario"] == "낙관" else "pes"
    ms = "".join(f'<li><time>{E(m["by"])}</time><span>{E(m["text"])}</span></li>' for m in r["milestones"])
    scen_html += f"""<article class="scen {cls}" id="{E(r['id'])}"><header><span class="sk">{E(r['scenario'])} · {'Optimistic' if cls=='opt' else 'Pessimistic'}</span><code>{E(r['id'])}</code></header>
  <p class="sstmt">{E(r['statement'])}</p><ol class="ms">{ms}</ol>
  <dl class="sdl"><div><dt>판정 시점</dt><dd>{E(r['due'])}</dd></div><div><dt>판정 방법</dt><dd>{E(r['method'])}</dd></div>
  <div><dt>전제</dt><dd>{E(r['condition'])}</dd></div><div><dt>근거</dt><dd>{tags(r['basis'])}</dd></div></dl></article>"""
sign = {}
for r in scen:
    for sp in r["signposts"]:
        d = sign.setdefault(sp["id"], {"hit": set(), "miss": set()})
        if "on_hit" in sp: d["hit"].add(sp["on_hit"])
        if "on_miss" in sp: d["miss"].add(sp["on_miss"])
def side(s): return "".join(f'<span class="side {"opt" if x=="낙관" else "pes"}">{E(x)}</span>' for x in sorted(s)) or '<span class="muted">—</span>'
details = sorted([r for r in recs if r["type"] == "전망" and not r.get("scenario")], key=lambda r: r["due"])
frows = "".join(f"""<tr id="{E(r['id'])}"><td class="stmt">{E(r['statement'])}<small>확인 방법: {E(r['method'])}</small></td>
  <td class="asof">{E(r['due'])}</td><td>{side(sign.get(r['id'],{}).get('hit',set()))}</td><td>{side(sign.get(r['id'],{}).get('miss',set()))}</td>
  <td><span class="fstat">{E(r['forecast_status'])}</span></td><td>{tags(r['basis'])}</td></tr>""" for r in details)

# 5. 정보 유형별 지도 -----------------------------------------------
LEVELS = ["실험", "얼리어답터", "확산", "주류"]
TRUST = {"측정 없음": "contest", "낮음": "agent", "약화": "agent", "사람 경험담 우위": "brand"}
MAP_LEAD = "AI가 만드는 쪽(정보 글·광고)은 이미 주류이고, AI를 거쳐 받는 쪽은 얼리어답터 단계다. 신뢰는 어느 유형에서도 오르지 않았고, AI가 기대는 원천은 여전히 사람의 경험담이다."
MAP = [
    ("정보 글", "Articles", "주류", "측정 없음", "신규 영문 웹 글의 50.9%가 AI 글. 2025년 초부터 정체.", ["C3-M-001"]),
    ("광고", "Ads", "주류", "약화", "광고 임원 83%가 AI로 제작, 젊은 층 호감 45%로 기대와 격차 확대.", ["C3-M-009", "C3-M-008"]),
    ("상품 리뷰", "Reviews", "얼리어답터", "약화", "AI 의심 리뷰 2022년 대비 약 400% 증가. 플랫폼 대응은 금지·허용으로 갈림.", ["C3-M-002", "C3-E-003"]),
    ("뉴스·정보 받는 경로", "Delivery", "얼리어답터", "낮음", "매주 AI 챗봇으로 뉴스 10%, 신뢰 20%, 원문 클릭 4%.", ["C3-M-003", "C3-M-004", "C3-M-005"]),
    ("AI 답변의 인용 원천", "Citations", "실험", "사람 경험담 우위", "Reddit·YouTube가 인용 1·2위. 원천은 아직 사람.", ["C3-M-007"]),
]
def lvl(level):
    i = LEVELS.index(level)
    return "".join(f'<span class="pip{" on" if k <= i else ""}"></span>' for k in range(4)) + f'<span class="lv">{E(level)}</span>'
def trust(t): return f'<span class="own {TRUST[t]}">{E(t)}</span>'
map_rows = "".join(f"""<div class="rung"><div class="stage"><b>{E(ko)}</b><span>{E(en)}</span></div>
  <div class="lvcell"><span class="region">AI 생성·경유 정도</span><span class="pips">{lvl(l)}</span></div>
  <div class="lvcell"><span class="region">소비자 신뢰</span>{trust(t)}</div>
  <p class="why">{E(w)} {tags(ids)}</p></div>""" for ko, en, l, t, w, ids in MAP)

# 6. 핵심 지표 ---------------------------------------------------------
INDICATOR_NAMES = {"C3-K1": "신규 웹 글 AI 생성 비중", "C3-K2": "상품 리뷰의 AI 생성 추세", "C3-K3": "AI 경유 정보 신뢰도",
                   "C3-K4": "원천 매체로의 유입", "C3-K5": "AI 답변의 인용 원천", "C3-K6": "AI 광고에 대한 소비자 태도",
                   "C3-K7": "AI 콘텐츠 표시 규제", "C3-K8": "한국 소비자의 AI 정보 신뢰"}
metrics = sorted([r for r in recs if r["type"] == "지표"], key=lambda r: (r["indicator"], -r["importance"]))
filled = {r["indicator"] for r in metrics if r.get("verified")}
empty_ind = [f"{k} {v}" for k, v in INDICATOR_NAMES.items() if k not in filled]
METRICS_LEAD = (f"추적 지표 8개 중 {len(filled)}개의 값을 원문으로 확인했다. {', '.join(empty_ind)}은 이번 회차에 수치를 찾지 못했다. "
                "표시 규제는 수치 대신 주요 사건(AI 기본법, 공정위 지침)으로 추적한다. 측정치 상당수가 탐지 업체·업계 단체 조사라 방법론 주의 표시를 달았다.")
def fmt_val(r):
    v, u = r.get("value"), r.get("unit", "")
    s = f"{v:g}" if isinstance(v, (int, float)) else str(v)
    return f"{s}{'' if u.startswith('%') else ' '}{u}"
mrows = "".join(f"""<tr id="{E(r['id'])}"><td class="ind">{E(r['indicator'])}<small>{E(INDICATOR_NAMES[r['indicator']])}</small></td>
  <td class="stmt">{E(r['statement'])} {'<span class="warn">충돌·주의</span>' if r.get('check_flags') else ''}<div class="src">{src_links(r)}</div></td>
  <td class="num">{E(fmt_val(r))}</td><td class="asof">{E(r['as_of'])}<small>{E(r['region'])}</small></td><td class="idc"><code>{E(r['id'])}</code></td></tr>""" for r in metrics)

# 7. 미확인·경고 -------------------------------------------------------
warns = [(r, "원문 미확인" if r["type"] in ("지표", "사건") and not r.get("verified") else "주의") for r in recs
         if (r["type"] in ("지표", "사건") and not r.get("verified")) or r.get("check_flags")]
wrows = "".join(f"""<tr><td><code>{E(r['id'])}</code></td><td><span class="wk">{E(k)}</span></td><td>{E(r['statement'])}</td><td class="muted">{E('; '.join(r.get('check_flags', [])))}</td></tr>""" for r, k in warns)
counts = {t: sum(1 for r in recs if r["type"] == t) for t in ("지표", "사건", "해석", "전망")}

page = f"""<title>C3 정보 원천과 신뢰 R1</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans+KR:wght@400;500;600&family=Noto+Serif+KR:wght@600;800&display=swap">
<style>{CSS}</style>
<main>
  <header class="narrow">
    <div class="eyebrow"><span>AI Future Customer Lab</span><span>C3 · Content, Information &amp; Trust</span><span>R1 기준 회차 · 2026-10-09</span></div>
    <h1>{E(TITLE)}</h1>
    <p class="question">고정 질문 v1.0 — {E(QUESTION)}</p>
  </header>
  <section class="answer-box"><h2>한 줄 답</h2>
    <p class="answer narrow">{E(ONE_LINE)} {tags(ONE_LINE_BASIS)}</p><dl class="arows">{answer_rows}</dl></section>
  <section><h2>해석</h2><div class="narrative">{narrative_html}</div>
    <div class="tablewrap"><table><thead><tr><th>방향</th><th>대상</th><th>해석</th><th>근거</th><th>기록</th></tr></thead><tbody>{irows}</tbody></table></div></section>
  <section><h2>주요 사건 <small>최신순 · 원문 확인된 것만</small></h2><p class="lead">{E(EVENTS_LEAD)}</p><ul class="timeline">{erows}</ul></section>
  <section><h2>전망 <small>2027년 말까지, 소비자는 AI가 만든 정보를 믿게 될까</small></h2><p class="lead">{E(FORECAST_LEAD)}</p>
    <div class="scens">{scen_html}</div>
    <h3 class="subhead">세부 판정 근거</h3>
    <p class="lead muted">각 세부 전망이 적중하거나 빗나갔을 때 어느 시나리오 쪽 신호인지 표시했다. 확인 시점이 오면 확인 방법대로 판정한다.</p>
    <div class="tablewrap"><table><thead><tr><th>세부 전망</th><th>확인 시점</th><th>적중 시</th><th>빗나갈 시</th><th>상태</th><th>근거</th></tr></thead><tbody>{frows}</tbody></table></div></section>
  <section><h2>정보 유형별 지도 <small>AI 생성·경유 정도 · 소비자 신뢰</small></h2><p class="lead">{E(MAP_LEAD)}</p>
    <div class="ladder mapgrid">{map_rows}</div></section>
  <section><h2>핵심 지표 <small>추적 지표 {len(filled)}/8개 값 확보</small></h2><p class="lead">{E(METRICS_LEAD)}</p>
    <div class="tablewrap"><table><thead><tr><th>추적 지표</th><th>내용 · 출처</th><th style="text-align:right">현재값</th><th>기준 시점</th><th>기록</th></tr></thead><tbody>{mrows}</tbody></table></div></section>
  <section><h2>미확인·경고 <small>본문 판단에서 빼거나 주의해서 쓴 기록</small></h2>
    <div class="tablewrap"><table><thead><tr><th>기록</th><th>구분</th><th>진술</th><th>사유</th></tr></thead><tbody>{wrows}</tbody></table></div></section>
  <footer>
    <span>이 글은 4유형 기록 {len(recs)}건(지표 {counts['지표']} · 사건 {counts['사건']} · 해석 {counts['해석']} · 전망 {counts['전망']})에서 생성했습니다. 문장 옆 번호를 누르면 해당 기록으로 이동합니다.</span>
        <span>출처 등급 A = 1차 조사·공식 발표, B = 주요 언론·2차 보도, C = 블로그·출처 불명(원문 확인 전까지 판단에 쓰지 않음).</span>
  </footer>
</main>
"""
(ROOT / "article_r1.html").write_text(page, encoding="utf-8")
anchors = set(re.findall(r'id="(C3-[A-Z]-\d{3})"', page))
bad = sorted({i for i in re.findall(r'href="#(C3-[A-Z]-\d{3})"', page) if i not in anchors})
order = [page.index(f"<h2>{h}") for h in ("한 줄 답", "해석", "주요 사건", "전망", "정보 유형별 지도", "핵심 지표")]
print("article_r1.html 생성,", len(page), "bytes; 앵커 없는 근거 링크:", bad or "없음", "; 섹션 순서 정상:", order == sorted(order))
sys.exit(1 if bad or order != sorted(order) else 0)

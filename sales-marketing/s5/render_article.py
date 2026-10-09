"""records.jsonl → 기준 아티클 HTML (S5 R1).
순서: 한 줄 답 → 해석 → 주요 사건 → 전망 → 영역별 주도 기업과 조건 순위 → 핵심 지표 → 미확인·경고
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

TITLE = "영업·마케팅 AI 예산은 누가 가져가고, 무엇이 도입을 가르나"
QUESTION = "어떤 기업과 제품이 영업·마케팅 예산과 고객 접점을 확보하고 있으며, 도입 확대와 수익성을 결정하는 조건은 무엇인가?"

# 1. 한 줄 답 ----------------------------------------------------------
ONE_LINE = ("2026년 10월 현재 영업·마케팅 AI 예산과 고객 접점을 가장 크게 확보한 곳은 광고 플랫폼이다. Meta Advantage+ 하나가 연환산 750억 달러로 Salesforce Agentforce(15억 달러)의 50배다. "
            "CRM 기존 강자는 AI 매출을 빠르게 키우지만 아직 전체 매출의 3% 수준이고, 고객 서비스 AI에서는 Sierra 같은 신생 기업이 기업가치 150억 달러로 빠르게 치고 올라온다. "
            "도입 확대를 가르는 조건은 성과 증명이며, 그래서 과금이 좌석에서 해결·성과당으로 옮겨가고 있다.")
ONE_LINE_BASIS = ["S5-I-001", "S5-I-002", "S5-I-003", "S5-I-004", "S5-I-006"]
ANSWER_ROWS = [
    ("광고·미디어 AI", "Meta·Google이 굳혔다. Advantage+ 연환산 750억 달러, AI Max 광고주 50만 곳. 한국은 네이버(광고 성장의 60% 이상이 AI 덕).", ["S5-M-001", "S5-M-009"]),
    ("CRM·영업", "Salesforce·HubSpot이 AI 매출을 키우는 중. Agentforce 연환산 15억 달러(AI·데이터 합계 약 40억 달러), HubSpot 에이전트 8,000~10,000곳 도입.", ["S5-M-002", "S5-M-005"]),
    ("고객 서비스 AI", "신생 기업이 경합. Sierra 기업가치 150억 달러·Fortune 50의 40% 이상, Decagon 45억 달러.", ["S5-M-003"]),
    ("과금", "좌석 → 사용량 → 성과. HubSpot 해결 대화당 0.5달러, Sierra 해결당 약 1.5달러, Salesforce 해결당 과금 출시.", ["S5-M-004", "S5-E-006"]),
    ("수익성 위협", "좌석 과금 약화 우려로 소프트웨어 시가총액 약 2조 달러 감소(집계). 실적은 아직 버티는 중.", ["S5-M-006", "S5-E-008"]),
]
answer_rows = "".join(f'<div class="arow"><dt>{E(k)}</dt><dd>{E(v)} {tags(ids)}</dd></div>' for k, v, ids in ANSWER_ROWS)

# 2. 해석 --------------------------------------------------------------
NARRATIVE = [
    ("영업·마케팅 AI의 돈은 광고 플랫폼으로 가장 많이 간다. Meta의 AI 광고 묶음 Advantage+는 연환산 750억 달러, 구글 AI Max는 광고주 50만 곳이다. AI가 광고 상품 안에 들어 있어 기업이 따로 'AI 도구'를 살 필요 없이 퍼진다. "
     "한국도 같다. 네이버는 광고 성장의 60% 이상을 AI 최적화 덕으로 돌렸다.",
     ["S5-M-001", "S5-M-009", "S5-I-001", "S5-I-008"]),
    ("CRM 기존 강자는 AI를 데이터와 묶어 판다. Salesforce Agentforce의 연환산 매출은 15억 달러로 연 매출의 약 3%지만, AI·데이터를 합치면 40억 달러에 가깝다. 한 분기에 실제 운영 유료 고객 2,000곳을 더했다. "
     "HubSpot도 고객 응대 에이전트 8,000곳, 영업 에이전트 1만 곳 넘게 켜졌다.",
     ["S5-M-002", "S5-M-005", "S5-E-008", "S5-I-002"]),
    ("고객 서비스 AI는 신생 기업이 가장 빠르게 자리를 넓히는 영역이다. Sierra는 2026년 5월 기업가치 150억 달러를 넘어 1년 반 새 세 배가 됐고, Fortune 50의 40% 이상을 고객으로 확보했다. Decagon도 45억 달러를 인정받았다. "
     "AI 검색 노출 측정처럼 새로 생긴 영역에서도 Profound가 유니콘이 됐다.",
     ["S5-M-003", "S5-E-005", "S5-E-001", "S5-E-003", "S5-I-003"]),
    ("과금 방식이 경쟁의 축이 됐다. HubSpot은 4월 고객 응대 에이전트를 해결 대화당 0.5달러로, 영업 에이전트를 추천 리드당 1달러로 바꿨고, Salesforce도 해결당 과금을 냈다. Sierra는 처음부터 해결당 약 1.5달러를 받는다. "
     "효과가 증명되지 않은 상황에서 구매자의 위험을 공급자가 나눠 지는 방식이다.",
     ["S5-M-004", "S5-E-004", "S5-E-006", "S5-I-004", "S5-I-006"]),
    ("시장은 기존 SaaS의 수익성 약화를 먼저 가격에 반영했다. AI 에이전트가 좌석 수요를 줄일 것이라는 우려로 소프트웨어 시가총액 약 2조 달러가 줄었다는 집계가 나왔고, HubSpot은 고점 대비 70~80% 빠졌다. "
     "그러나 Salesforce 실적에서는 좌석이 늘고 이탈이 최저였으며, Adobe의 AI 중심 매출은 150% 넘게 늘었다. 실적과 시장 평가 사이의 괴리가 크다. 마케팅 예산은 매출의 7.8%로 그대로라, AI 예산은 기존 지출을 대체하며 자란다.",
     ["S5-M-006", "S5-M-007", "S5-M-008", "S5-E-002", "S5-I-005", "S5-I-007"]),
]
narrative_html = "".join(para(t, ids) for t, ids in NARRATIVE)
DIR = {"강화": "up", "약화": "down", "중립": "flat"}
irows = "".join(f"""<tr id="{E(r['id'])}"><td><span class="dir {DIR[r['direction']]}">{E(r['direction'])}</span></td>
  <td class="tgt">{E(r['target'])}</td><td>{E(r['statement'])}</td><td>{tags(r['basis'])}</td><td class="idc"><code>{E(r['id'])}</code></td></tr>"""
  for r in recs if r["type"] == "해석")

# 3. 주요 사건 (최신순) ------------------------------------------------
EVENTS_LEAD = ("올해는 두 흐름이 동시에 움직였다. 2월 소프트웨어 주식 급락으로 좌석 과금의 미래가 의심받는 사이, 4~6월 HubSpot·Salesforce가 해결당 과금으로 돌아섰고 Sierra는 기업가치를 세 배로 키웠다. "
               "여름 실적 시즌에는 Meta Advantage+ 750억 달러, Agentforce 15억 달러, Adobe AI 중심 매출 150% 성장이 발표됐다.")
events = sorted([r for r in recs if r["type"] == "사건" and r.get("verified")], key=lambda r: r["date"], reverse=True)
erows = "".join(f"""<li id="{E(r['id'])}"><time>{E(r['date'])}</time><div><b>{E(r['actor'])}</b> {E(r['statement'])}
  <div class="src">{src_links(r)} <code>{E(r['id'])}</code></div></div></li>""" for r in events)

# 4. 전망 --------------------------------------------------------------
FORECAST_LEAD = ("2027년 말을 기준으로 두 시나리오를 세웠다. 갈림길은 성과당 과금이 도입 문턱을 낮춰 기존 CRM과 AI 신생 기업이 함께 크는지, "
                 "아니면 광고 플랫폼이 예산을 흡수하고 독립 SaaS의 수익성이 깎이는지다. 가장 이른 신호는 12월 Salesforce·Adobe 실적이다.")
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

# 5. 영역별 주도 기업과 조건 순위 -----------------------------------
MAP_LEAD = ("영업·마케팅 AI를 다섯 영역으로 나누고, 영역마다 지금 예산과 고객 접점을 가장 많이 확보한 기업·제품과 그 자리의 방향(굳어짐·경합·흔들림)을 판정했다.")
OWN = {"굳어짐": "brand", "경합": "contest", "흔들림": "agent"}
MAP = [
    ("광고·미디어 AI", "Meta·Google (한국: 네이버)", "굳어짐", "Advantage+ 연환산 750억 달러, AI Max 광고주 50만 곳, 네이버 광고 성장의 60% 이상이 AI 덕", ["S5-M-001", "S5-M-009"]),
    ("CRM·영업", "Salesforce·HubSpot", "경합", "Agentforce 15억 달러(AI·데이터 약 40억 달러), HubSpot 에이전트 1만 곳 이상. 주가는 좌석 과금 우려로 급락", ["S5-M-002", "S5-M-005", "S5-M-006"]),
    ("고객 서비스 AI", "Sierra 등 신생 기업 vs CRM", "경합", "Sierra 150억 달러·Fortune 50의 40% 이상, Decagon 45억 달러, Salesforce·HubSpot 해결당 과금으로 대응", ["S5-M-003", "S5-M-004"]),
    ("마케팅 콘텐츠", "Adobe vs 광고 플랫폼 내장 도구", "흔들림", "Adobe AI 중심 매출 +150%지만 전체 +13%, 주가 연초 대비 -26~38%. Meta AI 제작 도구 소상공인 900만 곳", ["S5-M-007", "S5-M-006", "S5-M-001"]),
    ("AI 검색 노출 측정", "Profound 등 신생 기업", "경합", "새로 생긴 영역. Profound 기업가치 10억 달러, 고객 700곳 이상", ["S5-E-003"]),
]
map_rows = "".join(f"""<div class="rung"><div class="stage"><b>{E(k)}</b></div><div class="lvcell">{E(who)}</div>
  <div class="lvcell"><span class="own {OWN[d]}">{E(d)}</span></div><p class="why">{E(w)} {tags(ids)}</p></div>""" for k, who, d, w, ids in MAP)
FACTOR_LEAD = ("도입 확대와 공급자 수익성을 가르는 조건을 영향 크기 순으로 놓았다. 순위는 여러 영역에 걸치는지와 이미 수치로 나타났는지를 기준으로 매겼다.")
FCLS = {"제약": "agent", "촉진": "brand", "중립": "contest"}
FACTORS = [
    (1, "제약", "성과 증명", "마케팅 예산 그대로(매출의 7.8%), AI 준비된 조직 30%. 증분 효과가 엇갈려 구매자가 확신하지 못함", ["S5-M-008", "S5-I-006"]),
    (2, "촉진", "성과당 과금", "HubSpot 해결당 0.5달러·리드당 1달러, Sierra 해결당 약 1.5달러, Salesforce 해결당 과금. 구매자의 위험을 낮춤", ["S5-M-004", "S5-E-004", "S5-E-006"]),
    (3, "촉진", "기존 상품에 내장", "광고 플랫폼 AI는 별도 구매 없이 확산(Advantage+ 750억 달러). CRM도 데이터 기반과 묶어 판매(AI·데이터 약 40억 달러)", ["S5-M-001", "S5-M-002"]),
    (4, "제약", "좌석 과금 약화", "에이전트가 사람 사용자를 대신하면 좌석 매출이 줄 수 있다는 우려로 소프트웨어 시가총액 약 2조 달러 감소(집계)", ["S5-M-006", "S5-E-002"]),
    (5, "중립", "신생 기업의 속도", "고객 서비스 AI 신생 기업이 대형 고객을 빠르게 확보. 기존 강자에는 위협, 시장 전체로는 도입 촉진", ["S5-M-003", "S5-E-005"]),
]
factor_rows = "".join(f"""<tr><td class="num">{n}</td><td><span class="own {FCLS[k]}">{E(k)}</span></td><td class="tgt">{E(f)}</td><td>{E(w)} {tags(ids)}</td></tr>""" for n, k, f, w, ids in FACTORS)

# 6. 핵심 지표 ---------------------------------------------------------
INDICATOR_NAMES = {"S5-T1": "광고 플랫폼 AI 매출", "S5-T2": "CRM AI 매출", "S5-T3": "AI 네이티브 가치·매출",
                   "S5-T4": "과금 방식", "S5-T5": "도입 고객 수", "S5-T6": "기존 SaaS 성장·가치",
                   "S5-T7": "마케팅 예산 중 AI", "S5-T8": "한국 영업·마케팅 AI 시장"}
metrics = sorted([r for r in recs if r["type"] == "지표"], key=lambda r: (r["indicator"], -r["importance"]))
filled = {r["indicator"] for r in metrics if r.get("verified")}
empty_ind = [f"{k} {v}" for k, v in INDICATOR_NAMES.items() if k not in filled]
METRICS_LEAD = (f"추적 지표 8개 중 {len(filled)}개의 값을 원문으로 확인했다. "
                "비상장사 기업가치·매출은 투자 보도 기준이고, 소프트웨어 시가총액 감소는 2차 정리 기사의 집계라 원자료 확인 표시를 달았다.")
def fmt_val(r):
    v, u = r.get("value"), r.get("unit", "")
    if v is None: return "—"
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

page = f"""<title>S5 영업·마케팅 AI 시장 R1</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans+KR:wght@400;500;600&family=Noto+Serif+KR:wght@600;800&display=swap">
<style>{CSS}</style>
<main>
  <header class="narrow">
    <div class="eyebrow"><span>AI Sales &amp; Marketing</span><span>S5 · Market, Competition &amp; Economics</span><span>R1 기준 회차 · 2026-10-09</span></div>
    <h1>{E(TITLE)}</h1>
    <p class="question">고정 질문 v1.0 — {E(QUESTION)}</p>
  </header>
  <section class="answer-box"><h2>한 줄 답</h2>
    <p class="answer narrow">{E(ONE_LINE)} {tags(ONE_LINE_BASIS)}</p><dl class="arows">{answer_rows}</dl></section>
  <section><h2>해석</h2><div class="narrative">{narrative_html}</div>
    <div class="tablewrap"><table><thead><tr><th>방향</th><th>대상</th><th>해석</th><th>근거</th><th>기록</th></tr></thead><tbody>{irows}</tbody></table></div></section>
  <section><h2>주요 사건 <small>최신순 · 원문 확인된 것만</small></h2><p class="lead">{E(EVENTS_LEAD)}</p><ul class="timeline">{erows}</ul></section>
  <section><h2>전망 <small>2027년 말까지, 누가 예산을 가져갈까</small></h2><p class="lead">{E(FORECAST_LEAD)}</p>
    <div class="scens">{scen_html}</div>
    <h3 class="subhead">세부 판정 근거</h3>
    <p class="lead muted">각 세부 전망이 적중하거나 빗나갔을 때 어느 시나리오 쪽 신호인지 표시했다. 확인 시점이 오면 확인 방법대로 판정한다.</p>
    <div class="tablewrap"><table><thead><tr><th>세부 전망</th><th>확인 시점</th><th>적중 시</th><th>빗나갈 시</th><th>상태</th><th>근거</th></tr></thead><tbody>{frows}</tbody></table></div></section>
  <section><h2>영역별 주도 기업과 조건 순위 <small>누가 예산을 가져가나 · 무엇이 도입을 가르나</small></h2><p class="lead">{E(MAP_LEAD)}</p>
    <div class="ladder mapgrid layers">{map_rows}</div>
    <h3 class="subhead">도입 확대·수익성 조건 순위</h3><p class="lead">{E(FACTOR_LEAD)}</p>
    <div class="tablewrap"><table><thead><tr><th style="white-space:nowrap">순위</th><th>방향</th><th>조건</th><th>근거</th></tr></thead><tbody>{factor_rows}</tbody></table></div></section>
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
anchors = set(re.findall(r'id="(S5-[A-Z]-\d{3})"', page))
bad = sorted({i for i in re.findall(r'href="#(S5-[A-Z]-\d{3})"', page) if i not in anchors})
order = [page.index(f"<h2>{h}") for h in ("한 줄 답", "해석", "주요 사건", "전망", "영역별 주도 기업과 조건 순위", "핵심 지표")]
print("article_r1.html 생성,", len(page), "bytes; 앵커 없는 근거 링크:", bad or "없음", "; 섹션 순서 정상:", order == sorted(order))
sys.exit(1 if bad or order != sorted(order) else 0)

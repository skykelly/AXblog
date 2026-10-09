"""records.jsonl → 기준 아티클 HTML (T2 R1).
순서: 한 줄 답 → 해석 → 주요 사건 → 전망 → 상용화 단계 → 핵심 지표 → 미확인·경고
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

TITLE = "AI 제품은 어디까지 실제로 쓰이고 있나"
QUESTION = "AI 제품은 어느 영역에서 시범을 넘어 실제 운영 단계에 들어섰는가?"

# 1. 한 줄 답 ----------------------------------------------------------
ONE_LINE = ("2026년 10월 현재 시범을 넘어 ‘대규모 운영’에 들어선 AI 제품은 세 가지다. 대화형 Assistant(ChatGPT 주 9억 명), Coding Agent(Claude Code 연환산 매출 25억 달러 이상), 로보택시(Waymo 주 50만 회)다. "
            "몇 시간짜리 일을 맡기는 업무형 Agent는 정식 출시됐지만 운영 성과가 공개되지 않았고, 휴머노이드는 고객 현장 파일럿 단계다.")
ONE_LINE_BASIS = ["T2-I-001", "T2-I-002", "T2-I-003", "T2-I-004"]
ANSWER_ROWS = [
    ("대규모 운영", "대화형 Assistant(ChatGPT 주간 9억 명, 유료 5천만 명), Coding Agent(Claude Code 연환산 25억 달러 이상, Uber 커밋 코드 70%를 AI가 작성), 로보택시(Waymo 주 50만 회, 11개 도시).", ["T2-M-001", "T2-M-002", "T2-M-003", "T2-M-004"]),
    ("정식 출시, 성과 미공개", "업무형 Agent. ChatGPT Work가 7월 출시됐지만 이용량은 공개되지 않았다. 기업 54%가 에이전트를 운영·시범 중이지만 성과를 지표로 재는 곳은 25%다.", ["T2-E-004", "T2-M-007"]),
    ("파일럿·초기 상용", "휴머노이드. Agility Digit이 9개 고객 시설에서 6만 5천 시간, Figure가 BMW 공장 파일럿. 출하 대수는 중국 Unitree(2025년 약 5,500대)가 앞선다.", ["T2-M-005", "T2-M-006"]),
    ("반복되는 실패", "권한을 받은 코딩 에이전트가 운영 데이터를 지운 공개 사고가 1년여 동안 9건. 승인 단계를 우회하거나 지시를 무시한 사례가 많다.", ["T2-M-008", "T2-E-005"]),
    ("한국", "자율주행 택시는 강남 심야(평일 밤 10시~새벽 5시)로 묶어 시작했고, 휴머노이드는 현대차가 2028년 미국 공장 투입 계획을 내놓은 단계다.", ["T2-E-002", "T2-E-001"]),
]
answer_rows = "".join(f'<div class="arow"><dt>{E(k)}</dt><dd>{E(v)} {tags(ids)}</dd></div>' for k, v, ids in ANSWER_ROWS)

# 2. 해석 --------------------------------------------------------------
NARRATIVE = [
    ("이용량과 매출을 공개할 만큼 자리 잡은 소프트웨어 제품은 두 가지다. ChatGPT는 2월 주간 이용자 9억 명, 유료 구독자 5천만 명을 발표했다. "
     "Coding Agent는 더 빠르다. Claude Code는 2월 연환산 매출 25억 달러를 넘었고, Uber에서는 엔지니어의 84%가 매달 쓰며 커밋 코드의 70%를 AI가 썼다.",
     ["T2-M-001", "T2-M-002", "T2-M-003", "T2-I-001"]),
    ("물리 세계에서 대규모 운영에 들어선 것은 로보택시, 그중에서도 Waymo 하나다. 차량 약 3,500대로 11개 도시를 돌며 주간 유료 탑승 약 50만 회를 기록했고, 7월에는 라스베이거스에서 완전 무인 운행을 시작했다. "
     "Tesla는 오스틴에서 안전요원 없이 운행하는 것으로 보인다는 보도가 나왔지만 회사가 공식 확인하지 않았다.",
     ["T2-M-004", "T2-E-003", "T2-E-006", "T2-I-002"]),
    ("업무형 Agent는 ‘써 보는 단계’와 ‘운영 단계’ 사이에 있다. OpenAI는 7월 몇 시간짜리 프로젝트를 수행하는 ChatGPT Work를 냈지만 이용량은 밝히지 않았다. "
     "미국 기업의 54%가 에이전트를 운영하거나 시범 운영하지만, 성과를 명확한 지표로 재는 곳은 25%, 회사 차원의 사용 정책이 있는 곳은 24%다.",
     ["T2-E-004", "T2-M-007", "T2-I-003"]),
    ("운영 확산의 가장 직접적인 걸림돌은 사고다. 2025년 6월부터 2026년 7월까지 코딩 에이전트가 운영 데이터베이스나 사용자 파일을 지운 공개 사고가 9건 집계됐고, 상당수는 복구되지 못했다. "
     "7월에도 최신 모델로 작업하던 개발자의 운영 데이터베이스가 초기화됐다. 사람의 승인 단계를 우회하거나 ‘실행하지 말라’는 지시를 무시한 경우가 많다.",
     ["T2-M-008", "T2-E-005", "T2-I-005"]),
    ("휴머노이드는 고객 현장 파일럿과 초기 상용 단계다. Agility의 Digit은 9개 고객 시설에서 6만 5천 시간 넘게 일했고, Figure는 BMW 공장에서 11개월 파일럿을 마쳤다. "
     "출하 대수는 중국 Unitree가 2025년 약 5,500대로 앞서고, Tesla Optimus는 아직 외부 판매가 없다. 한국은 현대차그룹이 2028년 미국 공장 투입 계획을 내놓았고, 자율주행 택시는 3월 강남 심야 운행을 시작했다.",
     ["T2-M-005", "T2-M-006", "T2-E-001", "T2-E-002", "T2-I-004", "T2-I-006"]),
]
narrative_html = "".join(para(t, ids) for t, ids in NARRATIVE)
DIR = {"강화": "up", "약화": "down", "중립": "flat"}
irows = "".join(f"""<tr id="{E(r['id'])}"><td><span class="dir {DIR[r['direction']]}">{E(r['direction'])}</span></td>
  <td class="tgt">{E(r['target'])}</td><td>{E(r['statement'])}</td><td>{tags(r['basis'])}</td><td class="idc"><code>{E(r['id'])}</code></td></tr>"""
  for r in recs if r["type"] == "해석")

# 3. 주요 사건 (최신순) ------------------------------------------------
EVENTS_LEAD = ("7월이 분기점이었다. Waymo가 완전 무인 지역을 넓히고 OpenAI가 업무형 Agent를 정식 출시한 같은 달, 최신 모델로 작업하던 운영 데이터베이스가 초기화되는 사고도 보고됐다. "
               "한국은 연초 현대차의 휴머노이드 투입 계획과 3월 강남 자율주행 택시가 주요 사건이다.")
events = sorted([r for r in recs if r["type"] == "사건" and r.get("verified")], key=lambda r: r["date"], reverse=True)
erows = "".join(f"""<li id="{E(r['id'])}"><time>{E(r['date'])}</time><div><b>{E(r['actor'])}</b> {E(r['statement'])}
  <div class="src">{src_links(r)} <code>{E(r['id'])}</code></div></div></li>""" for r in events)

# 4. 전망 --------------------------------------------------------------
FORECAST_LEAD = ("2027년 말을 기준으로 두 시나리오를 세웠다. 갈림길은 업무형 Agent가 사고와 성과 측정 문제를 넘어 운영 성과를 공개하는지, "
                 "그리고 로보택시와 휴머노이드에서 Waymo 다음의 대규모 운영 사례가 나오는지다.")
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

# 5. 상용화 단계 -----------------------------------------------
SG = ["발표", "베타", "정식 출시", "대규모 운영"]
STAGE_LEAD = ("제품 영역마다 발표 → 베타(제한 이용) → 정식 출시 → 대규모 운영(이용량·성과·매출 공개) 중 어디에 있는지 판정했다. "
              "출시 발표만으로는 정식 출시까지만 인정한다. 한국은 국내 서비스 기준이며, 자료가 없으면 비워 두었다.")
STAGES = [
    ("대화형 Assistant", "대규모 운영", None, "주간 9억 명, 유료 5천만 명", ["T2-M-001"]),
    ("Coding Agent", "대규모 운영", None, "연환산 25억 달러 이상, 대형 고객 커밋 코드 70%", ["T2-M-002", "T2-M-003"]),
    ("로보택시", "대규모 운영", "베타", "Waymo 주 50만 회·11개 도시 / 서울 강남 심야 제한 운행", ["T2-M-004", "T2-E-002"]),
    ("업무형 Agent", "정식 출시", None, "ChatGPT Work 출시, 이용량 미공개", ["T2-E-004"]),
    ("기업 내 Agent 도입", "베타", None, "54% 운영·시범, 성과 측정 25%", ["T2-M-007"]),
    ("휴머노이드", "베타", "발표", "Agility 9개 시설·Figure BMW 파일럿 / 현대차 2028 투입 계획", ["T2-M-005", "T2-E-001"]),
]
def sg4(v):
    if v is None:
        return '<span class="lv muted">자료 없음</span>'
    i = SG.index(v)
    return "".join(f'<span class="pip{" on" if k <= i else ""}"></span>' for k in range(4)) + f'<span class="lv">{E(v)}</span>'
stage_rows = "".join(f"""<div class="rung"><div class="stage"><b>{E(d)}</b></div>
  <div class="lvcell"><span class="region">글로벌</span><span class="pips">{sg4(g)}</span></div>
  <div class="lvcell"><span class="region">한국</span><span class="pips">{sg4(k)}</span></div>
  <p class="why">{E(w)} {tags(ids)}</p></div>""" for d, g, k, w, ids in STAGES)

# 6. 핵심 지표 ---------------------------------------------------------
INDICATOR_NAMES = {"T2-K1": "AI Assistant 이용 규모", "T2-K2": "Coding Agent 매출·이용", "T2-K3": "업무형 Agent 이용량",
                   "T2-K4": "로보택시 운행 규모", "T2-K5": "휴머노이드 배치", "T2-K6": "기업 Agent 운영 비율",
                   "T2-K7": "Agent 운영 사고", "T2-K8": "한국 상용화 현황"}
metrics = sorted([r for r in recs if r["type"] == "지표"], key=lambda r: (r["indicator"], -r["importance"]))
filled = {r["indicator"] for r in metrics if r.get("verified")}
empty_ind = [f"{k} {v}" for k, v in INDICATOR_NAMES.items() if k not in filled]
METRICS_LEAD = (f"추적 지표 8개 중 {len(filled)}개의 값을 원문으로 확인했다. {', '.join(empty_ind)}은 이번 회차에 수치를 찾지 못했다. "
                "업무형 Agent는 이용량이 공개되지 않아 값을 비워 두었고, 한국 상용화는 수치 대신 주요 사건으로 추적한다. 기업 자체 발표와 보안 업체 집계에는 주의 표시를 달았다.")
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

page = f"""<title>T2 AI 제품 상용화 R1</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans+KR:wght@400;500;600&family=Noto+Serif+KR:wght@600;800&display=swap">
<style>{CSS}</style>
<main>
  <header class="narrow">
    <div class="eyebrow"><span>AI Industry Trend</span><span>T2 · AI Products &amp; Applications</span><span>R1 기준 회차 · 2026-10-09</span></div>
    <h1>{E(TITLE)}</h1>
    <p class="question">고정 질문 v1.0 — {E(QUESTION)}</p>
  </header>
  <section class="answer-box"><h2>한 줄 답</h2>
    <p class="answer narrow">{E(ONE_LINE)} {tags(ONE_LINE_BASIS)}</p><dl class="arows">{answer_rows}</dl></section>
  <section><h2>해석</h2><div class="narrative">{narrative_html}</div>
    <div class="tablewrap"><table><thead><tr><th>방향</th><th>대상</th><th>해석</th><th>근거</th><th>기록</th></tr></thead><tbody>{irows}</tbody></table></div></section>
  <section><h2>주요 사건 <small>최신순 · 원문 확인된 것만</small></h2><p class="lead">{E(EVENTS_LEAD)}</p><ul class="timeline">{erows}</ul></section>
  <section><h2>전망 <small>2027년 말까지, 무엇이 대규모 운영에 들어설까</small></h2><p class="lead">{E(FORECAST_LEAD)}</p>
    <div class="scens">{scen_html}</div>
    <h3 class="subhead">세부 판정 근거</h3>
    <p class="lead muted">각 세부 전망이 적중하거나 빗나갔을 때 어느 시나리오 쪽 신호인지 표시했다. 확인 시점이 오면 확인 방법대로 판정한다.</p>
    <div class="tablewrap"><table><thead><tr><th>세부 전망</th><th>확인 시점</th><th>적중 시</th><th>빗나갈 시</th><th>상태</th><th>근거</th></tr></thead><tbody>{frows}</tbody></table></div></section>
  <section><h2>상용화 단계 <small>제품 영역별 · 글로벌과 한국</small></h2><p class="lead">{E(STAGE_LEAD)}</p>
    <div class="ladder mapgrid auto">{stage_rows}</div></section>
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
anchors = set(re.findall(r'id="(T2-[A-Z]-\d{3})"', page))
bad = sorted({i for i in re.findall(r'href="#(T2-[A-Z]-\d{3})"', page) if i not in anchors})
order = [page.index(f"<h2>{h}") for h in ("한 줄 답", "해석", "주요 사건", "전망", "상용화 단계", "핵심 지표")]
print("article_r1.html 생성,", len(page), "bytes; 앵커 없는 근거 링크:", bad or "없음", "; 섹션 순서 정상:", order == sorted(order))
sys.exit(1 if bad or order != sorted(order) else 0)

"""records.jsonl → 기준 아티클 HTML (L1 R1).
순서: 한 줄 답 → 해석 → 주요 사건 → 전망 → 수요 확보 단계와 계약 원장 → 핵심 지표 → 미확인·경고
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

TITLE = "LG는 AI 데이터센터 수요를 어디까지 계약과 매출로 잡았나"
QUESTION = "LG는 AI 데이터센터의 냉각·전력·구축·운영 수요를 어떤 제품과 계약으로 확보하고 있으며, 그 수요는 계약·매출로 어디까지 확인되는가?"

# 1. 한 줄 답 ----------------------------------------------------------
ONE_LINE = ("2026년 10월 현재 LG는 냉각·전력·구축·운영 네 제품군 모두에서 AI 데이터센터 수요를 '계약' 단계까지 확보했다. LG전자 북미 5GW 칠러 장기 계약과 냉각 수주 6,000억 원 이상, LG에너지솔루션 ESS 수주 3조 원(하이퍼스케일러 AI 데이터센터 포함), LG CNS DBO 수주 1조 원 이상, 네이버클라우드 6,034억 원 입주 계약이다. "
            "그러나 AI 데이터센터 매출로 따로 확인된 것은 아직 없다. 냉각·ESS 매출은 기존 사업에 섞여 있고, 파주 AIDC는 2027년 가동이다.")
ONE_LINE_BASIS = ["L1-I-001", "L1-I-002", "L1-I-003", "L1-I-004", "L1-I-005"]
ANSWER_ROWS = [
    ("냉각 (LG전자)", "계약·고객 공개. Air Control Concept 5GW 장기 공급, 상반기 수주 6,000억 원 이상. CDU는 NVIDIA향 일부 모델 인증, 공급 계약은 미공개.", ["L1-M-001", "L1-E-010", "L1-E-011"]),
    ("전력·ESS (LG에너지솔루션)", "계약·고객 비공개. 상반기 ESS 수주 3조 원 이상에 하이퍼스케일러 AI 데이터센터 포함. 800V DC는 NVIDIA와 개발 중.", ["L1-M-003", "L1-E-007"]),
    ("구축 (LG CNS)", "수주 확인. 상반기 DBO 수주 1조 원 이상, 자카르타 데이터센터 인프라. AI Box는 자체 캠퍼스 계획.", ["L1-M-005", "L1-E-003"]),
    ("운영 (LG CNS·LG유플러스)", "계약, 매출은 2027년부터. 네이버클라우드 9년 6,034억 원, 파주 AIDC 첫 동 고객 확보(비공개).", ["L1-M-006", "L1-M-007"]),
    ("협의 단계", "Microsoft와는 9월 사장단 파트너십으로 냉각·전력·IT 공급 기회를 함께 찾기로 함(주문·금액 미공개). NVIDIA DSX Ready에 LG CDU·ESS 포함.", ["L1-E-012", "L1-E-013"]),
]
answer_rows = "".join(f'<div class="arow"><dt>{E(k)}</dt><dd>{E(v)} {tags(ids)}</dd></div>' for k, v, ids in ANSWER_ROWS)

# 2. 해석 --------------------------------------------------------------
NARRATIVE = [
    ("냉각은 LG가 가장 앞서 나간 영역이다. LG전자의 AI 데이터센터 냉각 수주는 2026년 상반기 6,000억 원을 넘었고, 10월에는 북미 데이터센터 인프라 기업 Air Control Concept과 총 5GW 규모의 칠러 장기 공급 계약을 맺었다. 건별 입찰이 아니라 물량이 보장되는 방식이다. "
     "다만 AI 데이터센터 냉각 매출은 ES사업본부(2분기 매출 2조 7,261억 원) 안에 섞여 있고, 액체냉각의 핵심인 CDU는 NVIDIA향 일부 모델 인증을 마쳤지만 공급 계약은 아직 공개되지 않았다.",
     ["L1-M-001", "L1-E-010", "L1-M-002", "L1-E-011", "L1-I-001"]),
    ("전력과 구축은 수주로 확인되지만 고객이 다 드러나지는 않았다. LG에너지솔루션의 상반기 ESS 수주 3조 원 이상에는 하이퍼스케일러의 AI 데이터센터 프로젝트가 들어 있고, ESS 매출은 1년 새 4.6배가 됐다. "
     "LG CNS는 상반기 데이터센터 설계·구축·운영 수주 1조 원 이상을 확보했고, 자카르타 데이터센터에서 냉각·전력·통신 인프라를 맡았다. 모듈형 AI Box는 부산 자체 캠퍼스로 시작한다.",
     ["L1-M-003", "L1-M-004", "L1-M-005", "L1-E-003", "L1-I-002", "L1-I-003"]),
    ("운영은 계약이 있지만 매출은 2027년부터다. LG CNS는 네이버클라우드와 2035년까지 6,034억 원 규모의 입주 계약을 맺었지만, AI 전용 여부는 명시되지 않았다. "
     "LG유플러스 파주 AIDC는 200MW(Blackwell GPU 약 7만 장 수용)로 시작해 600MW까지 늘릴 계획이며, 첫 동 50MW의 고객을 확보했지만 이름은 밝히지 않았다. 가동은 2027년, 향후 5년간 수주 매출 5조 원이 목표다.",
     ["L1-M-006", "L1-M-007", "L1-M-008", "L1-I-004"]),
    ("네 제품군 모두 '계약' 칸에 와 있지만, AI 데이터센터 매출로 따로 확인된 것은 없다. 2027년이 매출 전환을 확인하는 해다. "
     "계열사 역할은 6월 NVIDIA M.A.P. 협력에서 정식으로 나뉘었다(U+ 운영, CNS 설계·구축, 전자 냉각, 엔솔 800V DC 전력). 실제로 묶어 판 사례는 아직 그룹 안(파주 AIDC에 LG전자 냉각 적용)에 머문다.",
     ["L1-I-005", "L1-E-007", "L1-E-006", "L1-I-006"]),
    ("Microsoft와의 냉각 협력은 조심해서 읽어야 한다. 2025년 4월 일부 AI 데이터센터에 LG 냉각 설비를 쓸 계획이 알려졌고, 12월 시연을 거쳐 2026년 9월 사장단이 냉각·전력·IT 공급 기회를 함께 찾기로 했지만 주문·물량·금액은 공개되지 않았다. 같은 날 LG전자 CDU와 LG에너지솔루션 ESS는 NVIDIA 'DSX Ready' 제품에 포함됐다. "
     "글로벌 경쟁사와 견주면 규모 차이도 크다. Vertiv의 분기 매출은 약 33억 달러(+24%)로 LG전자 ES사업본부 전체보다 크고, 직접 칩 냉각 기업을 인수해 포트폴리오를 넓히고 있다.",
     ["L1-E-001", "L1-E-002", "L1-E-012", "L1-E-013", "L1-M-009", "L1-I-007", "L1-I-008"]),
]
narrative_html = "".join(para(t, ids) for t, ids in NARRATIVE)
DIR = {"강화": "up", "약화": "down", "중립": "flat"}
irows = "".join(f"""<tr id="{E(r['id'])}"><td><span class="dir {DIR[r['direction']]}">{E(r['direction'])}</span></td>
  <td class="tgt">{E(r['target'])}</td><td>{E(r['statement'])}</td><td>{tags(r['basis'])}</td><td class="idc"><code>{E(r['id'])}</code></td></tr>"""
  for r in recs if r["type"] == "해석")

# 3. 주요 사건 (최신순) ------------------------------------------------
EVENTS_LEAD = ("10월 LG전자의 북미 5GW 칠러 장기 계약이 가장 최근의 큰 사건이다. 그 앞에는 6월 NVIDIA M.A.P. 협력과 파주 AIDC 첫 동 고객 확보, 4월 네이버클라우드 입주 계약 공시가 있다. "
               "9월에는 Microsoft와 사장단 파트너십(공급 기회 탐색)을 맺고, LG전자 CDU와 엔솔 ESS가 NVIDIA DSX Ready에 들어갔다.")
events = sorted([r for r in recs if r["type"] == "사건" and r.get("verified")], key=lambda r: r["date"], reverse=True)
erows = "".join(f"""<li id="{E(r['id'])}"><time>{E(r['date'])}</time><div><b>{E(r['actor'])}</b> {E(r['statement'])}
  <div class="src">{src_links(r)} <code>{E(r['id'])}</code></div></div></li>""" for r in events)

# 4. 전망 --------------------------------------------------------------
FORECAST_LEAD = ("2027년 말을 기준으로 두 시나리오를 세웠다. 갈림길은 계약이 매출로 확인되는지(냉각 매출 1조 원, 파주 AIDC 가동과 고객 확보), "
                 "그리고 계열사가 함께 들어간 해외 패키지 수주가 나오는지다. 가장 이른 신호는 연말 CDU 공급 계약 공개다(NVIDIA향 일부 모델은 7월 인증 완료).")
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

# 5. 제품군별 수요 확보 단계와 계약 원장 ----------------------------
SG = ["발표·전시", "실증·협의", "계약", "공급·매출"]
STAGE_LEAD = ("제품군마다 발표·전시 → 실증·협의 → 계약 → 공급·매출(AI 데이터센터 매출이 따로 확인됨) 중 어디에 있는지 판정했다. 오른쪽 표시는 계약 고객이 공개됐는지다.")
CUST = {"고객 공개": "brand", "고객 일부 공개": "platform", "고객 비공개": "agent", "해당 없음": "contest"}
STAGES = [
    ("냉각 (LG전자)", "계약", "고객 공개", "Air Control Concept 5GW 장기 공급, 상반기 수주 6,000억 원+. CDU는 NVIDIA향 일부 인증, 냉각 매출 미분리", ["L1-M-001", "L1-E-010", "L1-E-011"]),
    ("전력·ESS (LG에너지솔루션)", "계약", "고객 비공개", "ESS 수주 3조 원+에 하이퍼스케일러 AI 데이터센터 포함. 800V DC는 NVIDIA와 개발", ["L1-M-003", "L1-E-007"]),
    ("구축·DBO (LG CNS)", "계약", "고객 일부 공개", "상반기 DBO 수주 1조 원+, 자카르타 인프라. AI Box는 부산 자체 캠퍼스", ["L1-M-005", "L1-E-003"]),
    ("운영·코로케이션 (LG CNS·U+)", "계약", "고객 일부 공개", "네이버클라우드 6,034억 원(2035년까지), 파주 첫 동 고객 확보(비공개). 가동 2027년", ["L1-M-006", "L1-M-007"]),
    ("GPU 클라우드 (LG CNS·U+)", "실증·협의", "해당 없음", "CNS GPU 투자 3,814억 원(Vera Rubin 포함), U+ Rubin 기반 인프라 계획. 외부 고객 계약 미확인", ["L1-M-008", "L1-E-007"]),
]
def sg4(v):
    i = SG.index(v)
    return "".join(f'<span class="pip{" on" if k <= i else ""}"></span>' for k in range(4)) + f'<span class="lv">{E(v)}</span>'
stage_rows = "".join(f"""<div class="rung"><div class="stage"><b>{E(d)}</b></div>
  <div class="lvcell"><span class="pips">{sg4(st)}</span></div>
  <div class="lvcell"><span class="own {CUST[c]}">{E(c)}</span></div>
  <p class="why">{E(w)} {tags(ids)}</p></div>""" for d, st, c, w, ids in STAGES)
LEDGER_LEAD = "확인된 계약을 한 줄씩 기록했다. 규모·기간이 공개되지 않은 항목은 비워 두고, 계획·협의 단계는 따로 표시했다."
LEDGER = [
    ("LG전자", "Air Control Concept (북미)", "칠러 장기 공급 (CDU 협의 중)", "총 5GW", "2026-10 체결, 금액·기간 미공개", ["L1-E-010"]),
    ("LG CNS", "네이버클라우드", "삼송 데이터센터 입주", "6,034억 원", "2026-07 ~ 2035-05", ["L1-E-004"]),
    ("LG CNS", "인도네시아 자카르타 데이터센터", "냉각·전력·통신 인프라", "약 1,000억 원 (30MW → 220MW)", "진행 중", ["L1-M-005"]),
    ("LG에너지솔루션", "하이퍼스케일러 (비공개)", "AI 데이터센터 ESS", "미공개 (상반기 ESS 수주 3조 원+에 포함)", "2026 상반기 수주", ["L1-M-003"]),
    ("LG유플러스", "비공개", "파주 AIDC 첫 동 50MW", "미공개", "2027 가동 예정", ["L1-M-007"]),
    ("LG 계열사", "Microsoft", "냉각·전력·IT 인프라 공급 기회 탐색", "미공개", "2026-09 사장단 파트너십, 공급 계약 미확인", ["L1-E-001", "L1-E-012"]),
]
ledger_rows = "".join(f"""<tr><td class="tgt">{E(a)}</td><td>{E(b)}</td><td>{E(c)}</td><td>{E(d)}</td><td>{E(e)}</td><td>{tags(ids)}</td></tr>""" for a, b, c, d, e, ids in LEDGER)
STAGE_NOTE = "판정: 네 제품군 모두 '계약' 단계, AI 데이터센터 매출로 따로 확인된 제품군은 아직 없다 (R1 기준)."

# 6. 핵심 지표 ---------------------------------------------------------
INDICATOR_NAMES = {"L1-T1": "냉각 수주", "L1-T2": "냉각 사업 규모", "L1-T3": "전력·ESS 수주",
                   "L1-T4": "ESS 매출·생산능력", "L1-T5": "구축(DBO) 수주", "L1-T6": "운영·임대 계약",
                   "L1-T7": "AIDC 용량·GPU", "L1-T8": "글로벌 경쟁사 비교"}
metrics = sorted([r for r in recs if r["type"] == "지표"], key=lambda r: (r["indicator"], -r["importance"]))
filled = {r["indicator"] for r in metrics if r.get("verified")}
empty_ind = [f"{k} {v}" for k, v in INDICATOR_NAMES.items() if k not in filled]
METRICS_LEAD = (f"추적 지표 8개 중 {len(filled)}개의 값을 원문으로 확인했다. "
                "회사 목표·전망(수주 5조 원, 칠러 매출 1조 원 등)은 실적과 구분해 표시했고, 금액·고객이 공개되지 않은 계약에는 주의 표시를 달았다.")
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

page = f"""<title>L1 LG AI 데이터센터 R1</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans+KR:wght@400;500;600&family=Noto+Serif+KR:wght@600;800&display=swap">
<style>{CSS}</style>
<main>
  <header class="narrow">
    <div class="eyebrow"><span>LG Group AI</span><span>L1 · AI Data Center / Infra</span><span>R1 기준 회차 · 2026-10-09</span></div>
    <h1>{E(TITLE)}</h1>
    <p class="question">고정 질문 v1.0 — {E(QUESTION)}</p>
  </header>
  <section class="answer-box"><h2>한 줄 답</h2>
    <p class="answer narrow">{E(ONE_LINE)} {tags(ONE_LINE_BASIS)}</p><dl class="arows">{answer_rows}</dl></section>
  <section><h2>해석</h2><div class="narrative">{narrative_html}</div>
    <div class="tablewrap"><table><thead><tr><th>방향</th><th>대상</th><th>해석</th><th>근거</th><th>기록</th></tr></thead><tbody>{irows}</tbody></table></div></section>
  <section><h2>주요 사건 <small>최신순 · 원문 확인된 것만</small></h2><p class="lead">{E(EVENTS_LEAD)}</p><ul class="timeline">{erows}</ul></section>
  <section><h2>전망 <small>2027년 말까지, 계약이 매출이 될까</small></h2><p class="lead">{E(FORECAST_LEAD)}</p>
    <div class="scens">{scen_html}</div>
    <h3 class="subhead">세부 판정 근거</h3>
    <p class="lead muted">각 세부 전망이 적중하거나 빗나갔을 때 어느 시나리오 쪽 신호인지 표시했다. 확인 시점이 오면 확인 방법대로 판정한다.</p>
    <div class="tablewrap"><table><thead><tr><th>세부 전망</th><th>확인 시점</th><th>적중 시</th><th>빗나갈 시</th><th>상태</th><th>근거</th></tr></thead><tbody>{frows}</tbody></table></div></section>
  <section><h2>수요 확보 단계와 계약 원장 <small>제품군별 · 계약 단위</small></h2><p class="lead">{E(STAGE_LEAD)}</p>
    <div class="ladder mapgrid auto">{stage_rows}</div><p class="gapnote">{E(STAGE_NOTE)}</p>
    <h3 class="subhead">계약 원장</h3><p class="lead">{E(LEDGER_LEAD)}</p>
    <div class="tablewrap"><table><thead><tr><th>계열사</th><th>상대</th><th>내용</th><th>규모</th><th>기간·상태</th><th>기록</th></tr></thead><tbody>{ledger_rows}</tbody></table></div></section>
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
anchors = set(re.findall(r'id="(L1-[A-Z]-\d{3})"', page))
bad = sorted({i for i in re.findall(r'href="#(L1-[A-Z]-\d{3})"', page) if i not in anchors})
order = [page.index(f"<h2>{h}") for h in ("한 줄 답", "해석", "주요 사건", "전망", "수요 확보 단계와 계약 원장", "핵심 지표")]
print("article_r1.html 생성,", len(page), "bytes; 앵커 없는 근거 링크:", bad or "없음", "; 섹션 순서 정상:", order == sorted(order))
# ---------- 포털 신호: 판정 칩과 게이지를 판정 데이터에서 계산해 내보낸다
SIGNAL_CHIP = '4개 제품군 계약 단계'
SIGNAL_GAUGE = '제품군 5개 중 계약 이상'
SIGNAL_FRONTIER = '계약 → 공급·매출'
signal = {"question": 'L1', "round": 1, "chip": SIGNAL_CHIP, "gauge": SIGNAL_GAUGE, "frontier": SIGNAL_FRONTIER,
          "on": sum(1 for r in STAGES if SG.index(r[1]) >= SG.index("계약")), "of": len(STAGES)}
(ROOT / "signal_r1.json").write_text(json.dumps(signal, ensure_ascii=False, indent=1), encoding="utf-8")
print("signal_r1.json:", signal["chip"], f'{signal["on"]}/{signal["of"]}')
sys.exit(1 if bad or order != sorted(order) else 0)

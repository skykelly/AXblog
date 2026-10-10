"""records.jsonl → 기준 아티클 HTML (L6 R1).
순서: 한 줄 답 → 해석 → 주요 사건 → 전망 → 파트너별 협력 단계 → 핵심 지표 → 미확인·경고
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

TITLE = "LG의 AI 동맹은 무엇을 바꾸고 있나"
QUESTION = "LG는 자체 AI 역량과 외부 파트너를 어떻게 결합하며, 협력이 기술·고객·공급망·시장 접근에 어떤 변화를 만드는가?"

# 1. 한 줄 답 ----------------------------------------------------------
ONE_LINE = ("2026년 10월 현재 LG의 AI 동맹 가운데 상용 계약까지 간 것은 LG가 '고객'인 협력이다. Palantir(그룹 PoC → 본 계약)와 Anthropic(그룹 통합 Claude 계약)이 그렇다. "
            "LG가 '공급자'가 되는 협력은 공급망 입구에 섰다. NVIDIA와는 세 분야·여섯 계열사가 공동개발 중이고 LG전자 CDU와 엔솔 ESS가 DSX Ready에 들어갔으며, Microsoft와는 9월 냉각·전력·IT 공급 기회를 함께 찾기로 했다. 다만 의사결정(Palantir)·로봇 두뇌(Skild·GR00T)·컴퓨팅(NVIDIA) 같은 핵심층은 외부에 기대고 있다.")
ONE_LINE_BASIS = ["L6-I-001", "L6-I-002", "L6-I-003", "L6-I-004"]
ANSWER_ROWS = [
    ("상용 계약 (LG가 고객)", "Palantir: 계열사 PoC 뒤 본 계약, FDE 조직. Anthropic: 그룹 통합 Claude Enterprise(2023년부터 지분 보유).", ["L6-E-002", "L6-E-006"]),
    ("공급망 입구 (LG가 공급자)", "NVIDIA: M.A.P. 세 분야·여섯 계열사, CDU·ESS가 DSX Ready에 포함. Microsoft: 냉각·전력·IT 공급 기회 탐색(금액 미공개).", ["L6-M-001", "L6-M-002", "L6-M-003"]),
    ("공동개발·투자", "Skild AI(RFM, 지분 투자), Dexmate(투자 3개월 뒤 물류 실증), D&D Pharmatech·LabGenius(신약), Aeva(라이다), CuspAI(소재).", ["L6-E-001", "L6-E-007", "L6-E-008", "L6-E-010"]),
    ("재판매", "LG CNS가 ChatGPT Enterprise 약 10곳, Palantir·CuspAI를 외부 고객에 공급.", ["L6-M-007", "L6-I-006"]),
    ("종속 위험", "의사결정·로봇 두뇌·컴퓨팅은 외부. LG가 쥔 축은 EXAONE, PhysicalWorks, 현장 데이터.", ["L6-I-004"]),
]
answer_rows = "".join(f'<div class="arow"><dt>{E(k)}</dt><dd>{E(v)} {tags(ids)}</dd></div>' for k, v, ids in ANSWER_ROWS)

# 2. 해석 --------------------------------------------------------------
NARRATIVE = [
    ("상용 계약까지 간 협력은 LG가 고객인 쪽이다. LG CNS는 3월 Palantir와 전략적 파트너십을 맺었는데, LG 계열사 품질 관리 PoC를 거쳐 본 계약이 됐다. 6월에는 Anthropic과 그룹 전 계열사에 적용할 수 있는 Claude Enterprise 통합 계약을 맺었다. "
     "LG테크놀로지벤처스가 2023년부터 지분을 가진 회사다. 반면 LG가 공급자가 되는 협력은 아직 계약 이전이다.",
     ["L6-E-002", "L6-E-006", "L6-I-001"]),
    ("NVIDIA는 가장 넓은 축이다. 6월 구광모 회장과 젠슨 황 CEO가 모빌리티·AI 인프라·피지컬 AI의 M.A.P. 협력과 레퍼런스 로봇 공동 개발에 합의했고, 여섯 계열사가 참여한다. 2주 뒤 30여 명의 워킹그룹이 NVIDIA 본사를 찾았다. "
     "9월에는 LG전자의 대용량 CDU와 LG에너지솔루션의 ESS가 NVIDIA의 AI 팩토리 프로그램 'DSX Ready' 제품에 들어가, NVIDIA 기반 데이터센터의 공급망 입구에 섰다.",
     ["L6-E-005", "L6-M-001", "L6-E-009", "L6-M-002", "L6-I-002"]),
    ("Microsoft와는 LG가 고객이자 공급자 후보인 양면 관계다. 9월 LG그룹 사장단이 Microsoft 본사에서 AI 데이터센터·AX·피지컬 AI 세 분야의 전략적 파트너십을 맺었다. LG는 사무직에 Copilot 등을 도입하고, Microsoft 데이터센터에 냉각·전력·IT를 공급할 기회를 함께 찾는다. "
     "공급 쪽은 금액·물량이 공개되지 않은 탐색 단계다.",
     ["L6-E-011", "L6-M-003", "L6-I-003"]),
    ("CVC 투자는 협력과 실증으로 이어지는 옵션이다. 확인된 AI·로봇 지분 투자는 Anthropic, Skild AI, Dexmate, 스마트레이더시스템 네 건이다. 가장 빠른 전환은 Dexmate로, 3월 투자 뒤 6월 LX판토스 물류 실증에 투입됐다. "
     "파트너 기술은 LG CNS의 외부 사업으로도 흐른다. ChatGPT Enterprise를 약 10곳에 팔았고, CuspAI 소재 AI 협력체(48개 기관)에서는 국내 공급 파트너를 맡았다.",
     ["L6-M-004", "L6-E-007", "L6-M-007", "L6-E-010", "L6-I-005", "L6-I-006"]),
    ("빠른 속도의 이면에는 종속 위험이 있다. 구광모 회장이 4월 실리콘밸리(Palantir·Skild), 6월 젠슨 황, 9월 사티아 나델라를 직접 만나며 협력을 끌어올렸지만, 의사결정·온톨로지는 Palantir, 로봇 두뇌는 Skild AI와 NVIDIA GR00T, 컴퓨팅은 NVIDIA에 기댄다. "
     "LG가 직접 쥔 축은 EXAONE, PhysicalWorks 같은 운영 플랫폼, 그리고 공장·배터리·차량의 현장 데이터다.",
     ["L6-E-003", "L6-E-005", "L6-E-011", "L6-I-004", "L6-I-007"]),
]
narrative_html = "".join(para(t, ids) for t, ids in NARRATIVE)
DIR = {"강화": "up", "약화": "down", "중립": "flat"}
irows = "".join(f"""<tr id="{E(r['id'])}"><td><span class="dir {DIR[r['direction']]}">{E(r['direction'])}</span></td>
  <td class="tgt">{E(r['target'])}</td><td>{E(r['statement'])}</td><td>{tags(r['basis'])}</td><td class="idc"><code>{E(r['id'])}</code></td></tr>"""
  for r in recs if r["type"] == "해석")

# 3. 주요 사건 (최신순) ------------------------------------------------
EVENTS_LEAD = ("9월 Microsoft 사장단 파트너십과 NVIDIA DSX Ready 포함이 가장 최근의 큰 사건이다. 6월에는 NVIDIA M.A.P.·Claude Enterprise·신약 협력이 몰렸고, 3월 Palantir 본 계약과 4월 구광모 회장의 실리콘밸리 방문이 그 앞에 있다.")
events = sorted([r for r in recs if r["type"] == "사건" and r.get("verified")], key=lambda r: r["date"], reverse=True)
erows = "".join(f"""<li id="{E(r['id'])}"><time>{E(r['date'])}</time><div><b>{E(r['actor'])}</b> {E(r['statement'])}
  <div class="src">{src_links(r)} <code>{E(r['id'])}</code></div></div></li>""" for r in events)

# 4. 전망 --------------------------------------------------------------
FORECAST_LEAD = ("2027년 말을 기준으로 두 시나리오를 세웠다. 갈림길은 협력이 LG의 공급 계약(NVIDIA·Microsoft)과 현장 성과(외부 로봇 파운데이션 모델)로 이어지는지, "
                 "아니면 회동·MOU·프로그램 참여에 머물며 외부 의존만 깊어지는지다.")
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

# 5. 파트너별 협력 단계와 종속 위험 ----------------------------------
SG = ["발표·MOU", "공동개발·투자", "실증", "상용 계약·고객", "매출·시장 접근"]
STAGE_LEAD = ("파트너마다 발표·MOU → 공동개발·투자 → 실증 → 상용 계약·고객 → 매출·시장 접근 중 어디에 있는지 판정했다. 오른쪽 표시는 그 파트너가 LG 사업의 핵심층(의사결정·로봇 두뇌·컴퓨팅)을 쥐는 정도다. 개별 제품·계약 성과는 L1~L5에 기록한다.")
CUST = {"종속 높음": "agent", "종속 중간": "platform", "종속 낮음": "brand"}
STAGES = [
    ("Palantir (LG CNS)", "상용 계약·고객", "종속 높음", "계열사 품질 PoC → 본 계약, FDE 조직. 의사결정·온톨로지층", ["L6-E-002"]),
    ("Anthropic (LG CNS·그룹)", "상용 계약·고객", "종속 중간", "Claude Enterprise 그룹 통합 계약, 2023년 지분 투자. OpenAI·EXAONE과 병행", ["L6-E-006"]),
    ("OpenAI (LG CNS 재판매)", "상용 계약·고객", "종속 낮음", "ChatGPT Enterprise 외부 고객 약 10곳", ["L6-M-007"]),
    ("NVIDIA (6개 계열사)", "실증", "종속 높음", "M.A.P. 공동개발, CDU 인증·DSX Ready 포함, 레퍼런스 로봇 공동 개발. 컴퓨팅·로봇 모델층", ["L6-M-001", "L6-M-002"]),
    ("Microsoft (그룹)", "발표·MOU", "종속 중간", "사장단 파트너십: 공급 기회 탐색·Copilot 도입·모델 학습 인프라. 금액 미공개", ["L6-M-003"]),
    ("Skild AI (LG CNS·LGTV)", "공동개발·투자", "종속 높음", "로봇 파운데이션 모델 협력·지분 투자. 현장 실증 결과 미공개. 로봇 두뇌층", ["L6-E-001", "L6-E-003"]),
    ("Dexmate (LG CNS)", "실증", "종속 낮음", "3월 투자 → 6월 LX판토스 물류 실증", ["L6-E-007"]),
    ("D&D Pharmatech · LabGenius", "공동개발·투자", "종속 낮음", "AI 신약 공동개발, LabGenius 라이선스 옵션", ["L6-E-008"]),
    ("CuspAI (LG CNS)", "발표·MOU", "종속 중간", "소재 AI 협력체 창립 멤버, 국내 공급 파트너", ["L6-E-010"]),
    ("SDVerse (LG에너지솔루션)", "발표·MOU", "종속 낮음", "배터리 SW 5종 등록, 고객 미공개", ["L6-M-006"]),
]
def sg5(v):
    i = SG.index(v)
    return "".join(f'<span class="pip{" on" if k <= i else ""}"></span>' for k in range(5)) + f'<span class="lv">{E(v)}</span>'
stage_rows = "".join(f"""<div class="rung"><div class="stage"><b>{E(d)}</b></div>
  <div class="lvcell"><span class="pips">{sg5(st)}</span></div>
  <div class="lvcell"><span class="own {CUST[c]}">{E(c)}</span></div>
  <p class="why">{E(w)} {tags(ids)}</p></div>""" for d, st, c, w, ids in STAGES)
LEDGER_LEAD = "LG 사업의 핵심층마다 외부 파트너와 LG가 직접 쥔 자산을 나란히 놓았다. 다음 회차부터 오른쪽 칸이 두꺼워지는지(내재화)를 본다."
LEDGER = [
    ("의사결정·온톨로지", "Palantir Foundry·AIP", "LG CNS FDE 조직, 그룹 업무 데이터", "높음", "PoC → 본 계약", ["L6-E-002"]),
    ("업무 AI 모델", "Anthropic Claude, OpenAI", "EXAONE (LG AI연구원)", "중간", "그룹 통합 계약", ["L6-E-006", "L6-M-007"]),
    ("로봇 두뇌", "Skild AI RFM, NVIDIA GR00T", "PhysicalWorks(학습·운영), 현장 데이터", "높음", "공동개발", ["L6-E-001", "L6-E-005"]),
    ("컴퓨팅·AI 팩토리", "NVIDIA GPU·DSX", "LG 냉각(CDU)·전력(ESS)이 공급망에 진입", "높음", "DSX Ready 포함", ["L6-M-002"]),
    ("클라우드·사무 AI", "Microsoft Azure·Copilot", "LG 냉각·전력·IT 공급 후보", "중간", "공급 기회 탐색", ["L6-M-003"]),
]
ledger_rows = "".join(f"""<tr><td class="tgt">{E(a)}</td><td>{E(b)}</td><td>{E(c)}</td><td>{E(d)}</td><td>{E(e)}</td><td>{tags(ids)}</td></tr>""" for a, b, c, d, e, ids in LEDGER)
STAGE_NOTE = "판정: 상용 계약은 LG가 고객인 협력(Palantir·Anthropic·OpenAI)에서, LG가 공급자인 협력(NVIDIA·Microsoft)은 실증·탐색 단계. 핵심층 다섯 중 셋의 종속이 높다 (R1 기준)."

# 6. 핵심 지표 ---------------------------------------------------------
INDICATOR_NAMES = {"L6-T1": "NVIDIA 협력 범위", "L6-T2": "파트너 공급망 진입", "L6-T3": "그룹이 고객인 플랫폼 계약",
                   "L6-T4": "Microsoft 협력 범위", "L6-T5": "CVC·전략 투자", "L6-T6": "연구 협력체",
                   "L6-T7": "모빌리티 SW 채널", "L6-T8": "파트너 기술 재판매"}
metrics = sorted([r for r in recs if r["type"] == "지표"], key=lambda r: (r["indicator"], -r["importance"]))
filled = {r["indicator"] for r in metrics if r.get("verified")}
empty_ind = [f"{k} {v}" for k, v in INDICATOR_NAMES.items() if k not in filled]
METRICS_LEAD = (f"추적 지표 8개 중 {len(filled)}개의 값을 원문으로 확인했다. "
                "T3 그룹이 고객인 플랫폼 계약(Palantir·Anthropic)은 사건으로 추적한다. 회동·MOU는 계약과 구분했고, 금액이 공개되지 않은 협력에는 주의 표시를 달았다.")
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

page = f"""<title>L6 LG 글로벌 AI 동맹 R1</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans+KR:wght@400;500;600&family=Noto+Serif+KR:wght@600;800&display=swap">
<style>{CSS}</style>
<main>
  <header class="narrow">
    <div class="eyebrow"><span>LG Group AI</span><span>L6 · Global AI Alliance / Open Innovation</span><span>R1 기준 회차 · 2026-10-09</span></div>
    <h1>{E(TITLE)}</h1>
    <p class="question">고정 질문 v1.0 — {E(QUESTION)}</p>
  </header>
  <section class="answer-box"><h2>한 줄 답</h2>
    <p class="answer narrow">{E(ONE_LINE)} {tags(ONE_LINE_BASIS)}</p><dl class="arows">{answer_rows}</dl></section>
  <section><h2>해석</h2><div class="narrative">{narrative_html}</div>
    <div class="tablewrap"><table><thead><tr><th>방향</th><th>대상</th><th>해석</th><th>근거</th><th>기록</th></tr></thead><tbody>{irows}</tbody></table></div></section>
  <section><h2>주요 사건 <small>최신순 · 원문 확인된 것만</small></h2><p class="lead">{E(EVENTS_LEAD)}</p><ul class="timeline">{erows}</ul></section>
  <section><h2>전망 <small>2027년 말까지, 동맹이 공급 계약이 될까</small></h2><p class="lead">{E(FORECAST_LEAD)}</p>
    <div class="scens">{scen_html}</div>
    <h3 class="subhead">세부 판정 근거</h3>
    <p class="lead muted">각 세부 전망이 적중하거나 빗나갔을 때 어느 시나리오 쪽 신호인지 표시했다. 확인 시점이 오면 확인 방법대로 판정한다.</p>
    <div class="tablewrap"><table><thead><tr><th>세부 전망</th><th>확인 시점</th><th>적중 시</th><th>빗나갈 시</th><th>상태</th><th>근거</th></tr></thead><tbody>{frows}</tbody></table></div></section>
  <section><h2>파트너별 협력 단계 <small>단계 판정 · 핵심층 종속 지도</small></h2><p class="lead">{E(STAGE_LEAD)}</p>
    <div class="ladder mapgrid auto">{stage_rows}</div><p class="gapnote">{E(STAGE_NOTE)}</p>
    <h3 class="subhead">핵심층 종속 지도</h3><p class="lead">{E(LEDGER_LEAD)}</p>
    <div class="tablewrap"><table><thead><tr><th>핵심층</th><th>외부 파트너</th><th>LG가 쥔 자산</th><th>종속</th><th>현재 단계</th><th>기록</th></tr></thead><tbody>{ledger_rows}</tbody></table></div></section>
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
anchors = set(re.findall(r'id="(L6-[A-Z]-\d{3})"', page))
bad = sorted({i for i in re.findall(r'href="#(L6-[A-Z]-\d{3})"', page) if i not in anchors})
order = [page.index(f"<h2>{h}") for h in ("한 줄 답", "해석", "주요 사건", "전망", "파트너별 협력 단계", "핵심 지표")]
print("article_r1.html 생성,", len(page), "bytes; 앵커 없는 근거 링크:", bad or "없음", "; 섹션 순서 정상:", order == sorted(order))
# ---------- 포털 신호: 판정 칩과 게이지를 판정 데이터에서 계산해 내보낸다
SIGNAL_CHIP = '상용 계약 3곳, 모두 LG가 고객'
SIGNAL_GAUGE = '파트너 10곳 중 상용 계약 이상'
SIGNAL_FRONTIER = 'NVIDIA 실증 → 계약'
signal = {"question": 'L6', "round": 1, "chip": SIGNAL_CHIP, "gauge": SIGNAL_GAUGE, "frontier": SIGNAL_FRONTIER,
          "on": sum(1 for r in STAGES if SG.index(r[1]) >= SG.index("상용 계약·고객")), "of": len(STAGES)}
(ROOT / "signal_r1.json").write_text(json.dumps(signal, ensure_ascii=False, indent=1), encoding="utf-8")
print("signal_r1.json:", signal["chip"], f'{signal["on"]}/{signal["of"]}')
sys.exit(1 if bad or order != sorted(order) else 0)

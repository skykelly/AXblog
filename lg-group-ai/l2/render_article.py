"""records.jsonl → 기준 아티클 HTML (L2 R1).
순서: 한 줄 답 → 해석 → 주요 사건 → 전망 → 적용 영역별 증거 수준 → 핵심 지표 → 미확인·경고
"""
import json, html, re, sys
from pathlib import Path

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT.parent.parent / "lib"))
from judge import gauge, chip, criteria_panel
L_RULE = "단계를 올리려면 회사 공식 발표, 공시, 고객사 발표 중 하나가 필요하다. 출처를 밝히지 않은 언론 보도만 있으면 잠정으로 둔다."
recs = [json.loads(l) for l in (ROOT / "records.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
by = {r["id"]: r for r in recs}
E = html.escape
CSS = (ROOT.parent.parent / "lib" / "article.css").read_text(encoding="utf-8")

def tags(ids):
    return "".join(f'<a class="rid" href="#{E(i)}" title="{E(by[i]["statement"])}">{E(i)}</a>' for i in ids)
def para(text, ids): return f"<p>{E(text)} {tags(ids)}</p>"
def src_links(r):
    return " · ".join(f'<a href="{E(s["url"])}" target="_blank" rel="noopener">{E(s["publisher"])}</a><span class="grade g{E(s["grade"])}">{E(s["grade"])}</span>' for s in r.get("sources", []))

TITLE = "LG의 피지컬 AI는 현장에서 어디까지 성과를 냈나"
QUESTION = "LG는 AI를 공장·물류·로봇·가전의 물리적 작동에 어떻게 적용하며, 실제 성능과 사업 성과는 어디까지 확인되는가?"

# 1. 한 줄 답 ----------------------------------------------------------
ONE_LINE = ("2026년 10월 현재 LG의 피지컬 AI가 사업 성과로 확인된 곳은 공장이다. LG전자 스마트팩토리 외부 수주가 2년 새 약 5,000억 원이 됐고, LG CNS 공장 운영 AI는 설비 10만 개 이상에 적용돼 한 배터리 공장에서 한 달 만에 합격품 비중 90% 이상을 냈다. "
            "물류 휴머노이드는 컬리·LX판토스와의 외부 실증 단계이고, 가전에서는 홈 허브(씽큐 온)가 출시됐지만 홈 로봇 CLOiD는 아직 실험실 안이다. 공개된 성능 수치의 대부분은 자사 공장 측정이거나 회사가 기대하는 값이다.")
ONE_LINE_BASIS = ["L2-I-001", "L2-I-002", "L2-I-003", "L2-I-004", "L2-I-005"]
ANSWER_ROWS = [
    ("상용 계약·성과", "공장. 스마트팩토리 외부 수주 약 5,000억 원(2년), Factova Control 설비 10만 개+·배터리 공장 합격품 90%+·전자 공장 생산성 +20%.", ["L2-M-001", "L2-M-003"]),
    ("외부 실증", "물류 휴머노이드. 컬리 PoC, LX판토스 청라 물류센터(Dexmate 바퀴형 휴머노이드), PhysicalWorks 실증 고객 20곳+.", ["L2-E-005", "L2-E-007", "L2-M-004"]),
    ("상용 출시 / 내부 실증", "가전. 씽큐 온은 상황 판단 자동화로 출시, CLOiD는 '내년 현장 투입' 계획.", ["L2-E-001", "L2-E-003"]),
    ("증거의 질", "자사 공장 수치(창원 생산성 +17%, 품질 비용 -70%)와 기대 효과(로봇 생산성 +15%, 운영비 -18%)가 대부분. 외부 고객 실측은 고객명 비공개 사례뿐.", ["L2-M-002", "L2-M-004", "L2-I-005"]),
    ("빈자리", "로봇 파운데이션 모델은 외부 협력 필요. 하드웨어·부품·센서·배터리·통합은 계열사 분업.", ["L2-E-003", "L2-I-006"]),
]
answer_rows = "".join(f'<div class="arow"><dt>{E(k)}</dt><dd>{E(v)} {tags(ids)}</dd></div>' for k, v, ids in ANSWER_ROWS)

# 2. 해석 --------------------------------------------------------------
NARRATIVE = [
    ("공장은 LG 피지컬 AI 가운데 사업 성과가 가장 분명한 영역이다. LG전자 스마트팩토리 솔루션의 외부 수주는 2024년 전담 조직을 만든 뒤 2년 만에 약 5,000억 원이 됐고, 2030년 외부 매출을 조 단위로 키우는 것이 목표다. "
     "LG CNS의 공장 운영 AI Factova Control은 국내외 설비 10만 개 이상에 적용됐고, 한 배터리 공장에서는 한 달 만에 합격품 비중 90% 이상·불량 반품 비용 약 70% 감소, 한 전자 공장에서는 생산성 약 20% 향상을 냈다.",
     ["L2-M-001", "L2-M-003", "L2-I-001", "L2-I-002"]),
    ("물류 로봇과 휴머노이드는 외부 실증 단계다. LG CNS는 5월 로봇 학습·운영 플랫폼 PhysicalWorks를 공개하고 20곳 넘는 고객과 실증 중이며, 컬리 물류센터 휴머노이드 PoC와 LX판토스 청라 물류센터 휴머노이드 투입 협약을 맺었다. "
     "LX판토스 현장에는 LG CNS가 투자한 미국 Dexmate의 바퀴형 휴머노이드가 들어간다. 상용 계약과 실측 성과는 아직 없고, 공개된 생산성 15%·운영비 18% 개선은 회사의 기대치다.",
     ["L2-E-004", "L2-M-004", "L2-E-005", "L2-E-007", "L2-I-003"]),
    ("가전에서는 홈 허브와 홈 로봇의 단계가 다르다. 생성형 AI 홈 허브 씽큐 온은 상황을 판단해 기기를 스스로 작동시키는 기능으로 출시됐다. 반면 CES 2026에서 공개한 홈 로봇 CLOiD는 가격·출시일이 없고, CEO는 '내년에 실험실에서 나와 현장에 투입'하겠다고 했다.",
     ["L2-E-001", "L2-E-002", "L2-E-003", "L2-I-004"]),
    ("성능 증거의 질은 아직 약하다. 자주 인용되는 창원 등대공장의 생산성 17%·품질 비용 70% 개선은 자사 공장 수치이고, 로봇 플랫폼 효과는 기대치다. 외부 고객 현장 실측은 고객명이 비공개인 Factova 사례 정도다. "
     "다음 회차부터는 외부 고객의 실측 수치가 나오는지가 핵심 판정 기준이다.",
     ["L2-M-002", "L2-M-004", "L2-M-003", "L2-I-005"]),
    ("LG는 로봇 밸류체인을 계열사로 나눠 맡는 구조를 만들고 있다. LG전자는 하드웨어와 액추에이터 '악시움', 산업용 로보스타·상업용 베어로보틱스 자회사를, LG이노텍은 센서, LG에너지솔루션은 배터리, LG CNS는 학습·운영 플랫폼과 통합을 맡는다. "
     "비어 있는 자리는 로봇 파운데이션 모델로 외부 협력에 기대고 있다. 7월에는 스마트팩토리 센터를 전무급으로 올리고 로보틱스사업센터를 새로 만들었다.",
     ["L2-E-003", "L2-E-008", "L2-M-005", "L2-I-006", "L2-I-007"]),
]
narrative_html = "".join(para(t, ids) for t, ids in NARRATIVE)
DIR = {"강화": "up", "약화": "down", "중립": "flat"}
irows = "".join(f"""<tr id="{E(r['id'])}"><td><span class="dir {DIR[r['direction']]}">{E(r['direction'])}</span></td>
  <td class="tgt">{E(r['target'])}</td><td>{E(r['statement'])}</td><td>{tags(r['basis'])}</td><td class="idc"><code>{E(r['id'])}</code></td></tr>"""
  for r in recs if r["type"] == "해석")

# 3. 주요 사건 (최신순) ------------------------------------------------
EVENTS_LEAD = ("5~6월에 LG CNS의 로봇 사건이 몰렸다. PhysicalWorks 공개, 컬리 휴머노이드 PoC, Factova 북미 진출, LX판토스 휴머노이드 협약이다. "
               "LG전자는 연초 CES에서 CLOiD와 로봇 사업 체계를 내놓고, 7월 스마트팩토리·로보틱스 조직을 키웠다.")
events = sorted([r for r in recs if r["type"] == "사건" and r.get("verified")], key=lambda r: r["date"], reverse=True)
erows = "".join(f"""<li id="{E(r['id'])}"><time>{E(r['date'])}</time><div><b>{E(r['actor'])}</b> {E(r['statement'])}
  <div class="src">{src_links(r)} <code>{E(r['id'])}</code></div></div></li>""" for r in events)

# 4. 전망 --------------------------------------------------------------
FORECAST_LEAD = ("2027년 말을 기준으로 두 시나리오를 세웠다. 갈림길은 로봇·휴머노이드가 실증을 넘어 상용 계약과 외부 고객 실측 성과로 이어지는지, "
                 "아니면 성과가 계속 자사 공장 수치와 기대 효과에 머무는지다.")
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

# 5. 적용 영역별 증거 수준과 성능 수치 원장 -------------------------
SG = ["내부 실증", "외부 실증", "상용 계약", "사업 성과"]
SG_DEF = {
    "내부 실증": "자사 공장·시설에 적용했다.",
    "외부 실증": "외부 고객 현장에서 PoC·실증을 한다 (고객이나 현장 공개).",
    "상용 계약": "외부 고객과의 유료 계약이나 정식 판매가 확인됐다.",
    "사업 성과": "외부 수주·매출 금액이 공개됐다.",
}
STAGE_LEAD = ("공장 쪽이 가장 앞서 있다. LG전자 외부 스마트팩토리는 수주 금액이 보도돼 사업 성과 단계지만 회사가 직접 밝힌 수치는 아니고, 성능 수치도 자사 공장 기준이다. "
              "LG CNS 공장 운영 AI는 외부 고객 실측 수치까지 나왔다. 물류 로봇·휴머노이드는 외부 실증, 홈 로봇은 내부 실증 단계다.")
CUST = {"외부 고객 실측": "brand", "자사 공장": "platform", "회사 기대치": "agent", "수치 없음": "contest"}
CUST_DEF = {"외부 고객 실측": "외부 고객 현장에서 잰 수치다.", "자사 공장": "LG 자체 공장에서 잰 수치다.",
            "회사 기대치": "실측이 아닌 목표·예상치다.", "수치 없음": "공개된 성능 수치가 없다."}
# (영역, 단계, 잠정, 성능 수치 출처, 근거, 기록)
STAGES = [
    ("공장 — 외부 스마트팩토리 (LG전자)", "사업 성과", True, "자사 공장", "외부 수주 약 5,000억 원(2년, 언론 보도), 로지스밸리 적용 보도. 성과 수치는 창원 등대공장 기준", ["L2-M-001", "L2-M-002", "L2-E-008"]),
    ("공장 — 운영 AI (LG CNS Factova)", "상용 계약", False, "외부 고객 실측", "설비 10만 개+, 배터리 공장 합격품 90%+·전자 공장 생산성 +20% (고객명 비공개)", ["L2-M-003"]),
    ("물류 로봇·휴머노이드 (LG CNS)", "외부 실증", False, "회사 기대치", "컬리 PoC, LX판토스 청라 협약, Forge 실증 20곳+", ["L2-E-005", "L2-E-007", "L2-M-004"]),
    ("가전 — 홈 허브 (씽큐 온)", "상용 계약", False, "수치 없음", "상황 판단 자동화 기능으로 정식 출시. 이용·성과 수치 미공개", ["L2-E-001"]),
    ("가전 — 홈 로봇 (CLOiD)", "내부 실증", False, "수치 없음", "CES 공개, 가격·출시일 없음, '내년 현장 투입' 계획", ["L2-E-002", "L2-E-003"]),
]
def tip_sg(v):
    return f"{v} — {SG_DEF[v]}"
def side(c, pv=False):
    return chip(c, CUST[c], f"{c} — {CUST_DEF[c]}", pv)
stage_rows = "".join(f"""<div class="rung"><div class="stage"><b>{E(d)}</b></div>
  <div class="lvcell">{gauge(SG, st, tip_sg(st), pv)}</div>
  <div class="lvcell">{side(c)}</div>
  <p class="why">{E(w)} {tags(ids)}</p></div>""" for d, st, pv, c, w, ids in STAGES)
criteria_html = criteria_panel([
    ("판정 단계: 증거 수준", ["단계", "기준"], [[gauge(SG, k), E(v)] for k, v in SG_DEF.items()]),
    ("옆 표시: 성능 수치의 출처 (강한 순)", ["판정", "정의"], [[side(k), E(v)] for k, v in CUST_DEF.items()]),
], extra_rules=[L_RULE])
LEDGER_LEAD = "공개된 성능 수치를 한 줄씩 기록하고, 측정 주체와 근거 종류를 표시했다. 다음 회차부터 '외부 고객 실측' 줄이 늘어나는지를 본다."
LEDGER = [
    ("생산성 +17%, 품질 비용 -70%, 에너지 효율 +30%", "LG전자 창원 등대공장", "LG전자", "2024 발표", "자사 공장", ["L2-M-002"]),
    ("합격품 비중 90%+ (1개월), 불량 반품 비용 -70%", "배터리 공장 (고객명 비공개)", "LG CNS", "2026-05", "외부 고객 실측", ["L2-M-003"]),
    ("작업 생산성 +20%, 공정 데이터 90%+ 자동 수집", "전자 공장 (고객명 비공개)", "LG CNS", "2026-05", "외부 고객 실측", ["L2-M-003"]),
    ("로봇 투입 기간 수개월 → 1~2개월", "PhysicalWorks Forge", "LG CNS", "2026-05", "회사 기대치", ["L2-M-004"]),
    ("생산성 +15% 이상, 운영비 최대 -18%", "로봇 100대 운영 (Baton)", "LG CNS", "2026-05", "회사 기대치", ["L2-M-004"]),
]
ledger_rows = "".join(f"""<tr><td class="tgt">{E(a)}</td><td>{E(b)}</td><td>{E(c)}</td><td>{E(d)}</td><td>{E(e)}</td><td>{tags(ids)}</td></tr>""" for a, b, c, d, e, ids in LEDGER)
STAGE_NOTE = "판정: 공장은 사업 성과까지 왔지만 성능 증거는 자사 공장 중심이고, 로봇·휴머노이드는 외부 실증, 홈 로봇은 내부 실증 단계다."

# 6. 핵심 지표 ---------------------------------------------------------
INDICATOR_NAMES = {"L2-T1": "스마트팩토리 외부 수주", "L2-T2": "자사 공장 성과", "L2-T3": "공장 운영 AI 적용·성과",
                   "L2-T4": "로봇 운영 플랫폼", "L2-T5": "물류 휴머노이드 실증", "L2-T6": "로봇 사업 체계",
                   "L2-T7": "가전 피지컬 AI", "L2-T8": "조직·투자"}
metrics = sorted([r for r in recs if r["type"] == "지표"], key=lambda r: (r["indicator"], -r["importance"]))
filled = {r["indicator"] for r in metrics if r.get("verified")}
empty_ind = [f"{k} {v}" for k, v in INDICATOR_NAMES.items() if k not in filled]
METRICS_LEAD = (f"추적 지표 8개 중 {len(filled)}개의 값을 원문으로 확인했다. "
                "T5 물류 휴머노이드 실증, T6 로봇 사업 체계, T7 가전 피지컬 AI는 수치 대신 사건으로 추적한다. 자사 공장 수치와 회사 기대치는 외부 고객 성과와 구분해 표시했다. 글로벌 경쟁사(Siemens·Rockwell) 비교 지표는 다음 회차에 확보한다.")
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

page = f"""<title>L2 LG 피지컬 AI R1</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans+KR:wght@400;500;600&family=Noto+Serif+KR:wght@600;800&display=swap">
<style>{CSS}</style>
<main>
  <header class="narrow">
    <div class="eyebrow"><span>LG Group AI</span><span>L2 · Physical AI / Smart Manufacturing</span><span>R1 기준 회차 · 2026-10-09</span></div>
    <h1>{E(TITLE)}</h1>
    <p class="question">고정 질문 v1.0 — {E(QUESTION)}</p>
  </header>
  <section class="answer-box"><h2>한 줄 답</h2>
    <p class="answer narrow">{E(ONE_LINE)} {tags(ONE_LINE_BASIS)}</p><dl class="arows">{answer_rows}</dl></section>
  <section><h2>해석</h2><div class="narrative">{narrative_html}</div>
    <div class="tablewrap"><table><thead><tr><th>방향</th><th>대상</th><th>해석</th><th>근거</th><th>기록</th></tr></thead><tbody>{irows}</tbody></table></div></section>
  <section><h2>주요 사건 <small>최신순 · 원문 확인된 것만</small></h2><p class="lead">{E(EVENTS_LEAD)}</p><ul class="timeline">{erows}</ul></section>
  <section><h2>전망 <small>2027년 말까지, 실증이 성과가 될까</small></h2><p class="lead">{E(FORECAST_LEAD)}</p>
    <div class="scens">{scen_html}</div>
    <h3 class="subhead">세부 판정 근거</h3>
    <p class="lead muted">각 세부 전망이 적중하거나 빗나갔을 때 어느 시나리오 쪽 신호인지 표시했다. 확인 시점이 오면 확인 방법대로 판정한다.</p>
    <div class="tablewrap"><table><thead><tr><th>세부 전망</th><th>확인 시점</th><th>적중 시</th><th>빗나갈 시</th><th>상태</th><th>근거</th></tr></thead><tbody>{frows}</tbody></table></div></section>
  <section><h2>적용 영역별 증거 수준 <small>영역별 · 성능 수치 원장</small></h2><p class="lead">{E(STAGE_LEAD)}</p>
    {criteria_html}
    <div class="ladder mapgrid auto">{stage_rows}</div><p class="gapnote">{E(STAGE_NOTE)}</p>
    <h3 class="subhead">성능 수치 원장</h3><p class="lead">{E(LEDGER_LEAD)}</p>
    <div class="tablewrap"><table><thead><tr><th>수치</th><th>대상</th><th>측정 주체</th><th>시점</th><th>근거 종류</th><th>기록</th></tr></thead><tbody>{ledger_rows}</tbody></table></div></section>
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
anchors = set(re.findall(r'id="(L2-[A-Z]-\d{3})"', page))
bad = sorted({i for i in re.findall(r'href="#(L2-[A-Z]-\d{3})"', page) if i not in anchors})
order = [page.index(f"<h2>{h}") for h in ("한 줄 답", "해석", "주요 사건", "전망", "적용 영역별 증거 수준", "핵심 지표")]
print("article_r1.html 생성,", len(page), "bytes; 앵커 없는 근거 링크:", bad or "없음", "; 섹션 순서 정상:", order == sorted(order))
# ---------- 포털 신호: 판정 칩과 게이지를 판정 데이터에서 계산해 내보낸다
SIGNAL_CHIP = '공장만 사업 성과'
SIGNAL_GAUGE = '적용 영역 5개 중 사업 성과'
SIGNAL_FRONTIER = '물류 로봇 외부 실증'
signal = {"question": 'L2', "round": 1, "chip": SIGNAL_CHIP, "gauge": SIGNAL_GAUGE, "frontier": SIGNAL_FRONTIER,
          "on": sum(1 for r in STAGES if r[1] == "사업 성과"), "of": len(STAGES)}
# 포털 띠: 항목마다 단계(0~3)와 잠정 여부
signal["kind"] = "band"
signal["levels"] = list(SG)
signal["items"] = [[r[0], SG.index(r[1]), bool(r[2])] for r in STAGES if True]
(ROOT / "signal_r1.json").write_text(json.dumps(signal, ensure_ascii=False, indent=1), encoding="utf-8")
print("signal_r1.json:", signal["chip"], f'{signal["on"]}/{signal["of"]}')
sys.exit(1 if bad or order != sorted(order) else 0)

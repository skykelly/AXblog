"""records.jsonl → 기준 아티클 HTML (L3 R1).
순서: 한 줄 답 → 해석 → 주요 사건 → 전망 → 제품군별 공급 단계 → 핵심 지표 → 미확인·경고
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

TITLE = "LG의 차량용 AI는 어느 고객·차종까지 들어갔나"
QUESTION = "LG의 차량용 AI·소프트웨어·부품은 어떤 고객과 차종에 적용되며, 공급 범위와 수익 기회는 어떻게 확대되는가?"

# 1. 한 줄 답 ----------------------------------------------------------
ONE_LINE = ("2026년 10월 현재 고객과 차종을 밝힌 LG의 AI·SDV 수주는 르노 'New Trafic E-Tech Electric'(유럽 첫 상용 SDV)의 통합 콕핏 한 건이다. 부품 공급사에서 통합 솔루션 공급사로 넓어지는 첫 공개 사례다. "
            "양산 적용 단계에 있는 것은 텔레매틱스(점유율 23%, 1위)와 차량용 OLED(15.9%, 2위) 같은 기존 강점이고, AI 캐빈·ADAS·라이다는 콘셉트이거나 고객명 없는 수주 단계다. 수익 기회는 이익률에서 먼저 보인다. VS 영업이익률 6~7%는 보쉬 모빌리티의 3배가 넘는다.")
ONE_LINE_BASIS = ["L3-I-001", "L3-I-002", "L3-I-003", "L3-I-004"]
ANSWER_ROWS = [
    ("고객·차종 공개", "르노 New Trafic E-Tech Electric: 계기판·인포테인먼트 통합 콕핏 (규모 비공개).", ["L3-E-006"]),
    ("양산 적용", "텔레매틱스 점유율 23%(1위), 차량용 OLED 15.9%(2위)·완성차 10여 곳. 고객명은 대부분 비공개.", ["L3-M-003", "L3-M-005"]),
    ("콘셉트·개발", "AI 캐빈 플랫폼(몇 년 안 상용화), DRIVE Hyperion 기반 ADAS 개발, 이노텍 라이다 2028년 탑재 목표, 엔솔 배터리 SW 5종 마켓 등록.", ["L3-E-001", "L3-E-004", "L3-M-004", "L3-M-006"]),
    ("수익", "VS 2분기 매출 3조 259억 원(+6.2%), 영업이익률 6.3%. 1분기 6.9%로 보쉬(1.8%)의 3배 이상.", ["L3-M-001", "L3-M-002"]),
    ("역풍", "전기차 수요 정체로 완성차 수요 회복 제한, VS 매출 전 분기 대비 -1.3%.", ["L3-M-001", "L3-I-007"]),
]
answer_rows = "".join(f'<div class="arow"><dt>{E(k)}</dt><dd>{E(v)} {tags(ids)}</dd></div>' for k, v, ids in ANSWER_ROWS)

# 2. 해석 --------------------------------------------------------------
NARRATIVE = [
    ("고객과 차종을 밝힌 LG의 AI·SDV 수주는 아직 한 건이다. LG전자는 10월 르노그룹이 '유럽 첫 상용 SDV'로 소개한 New Trafic E-Tech Electric에 계기판과 인포테인먼트를 하나로 통합 제어하는 콕핏을 공급한다고 발표했다. "
     "물량과 금액은 공개되지 않았지만, 개별 부품을 넘어 통합 솔루션을 맡는 첫 공개 사례라는 점에서 공급 범위가 넓어지는 신호다.",
     ["L3-E-006", "L3-I-001"]),
    ("양산 단계에 있는 것은 AI 이전부터의 강점이다. LG전자는 글로벌 텔레매틱스 점유율 23%로 1위이고, LG디스플레이는 차량용 OLED 점유율 15.9%로 2위이며 완성차 10여 곳에 패널을 공급한다. "
     "AI 기능은 이 기반 위에 얹히는 구조이고, 고객명은 대부분 공개되지 않는다.",
     ["L3-M-003", "L3-M-005", "L3-I-003"]),
    ("AI 고유 영역은 아직 콘셉트와 개발 단계다. LG전자는 CES 2026에서 투명 OLED 앞유리·시선 분석 비전 AI·온디바이스 AI 캐빈 플랫폼을 내놓고 '몇 년 안 상용화'를 말했다. LG이노텍은 자율주행 부품 16종을 공개했고, Aeva와 만드는 라이다는 2028년 탑재가 목표다. "
     "6월 NVIDIA 협력에서는 LG전자가 인포테인먼트에 DRIVE Hyperion을 결합한 ADAS를 개발하기로 해, 인포테인먼트에서 ADAS로 공급 범위를 넓힐 통로를 만들었다.",
     ["L3-E-001", "L3-E-002", "L3-M-004", "L3-E-004", "L3-I-004", "L3-I-006"]),
    ("수익 기회는 매출보다 이익률에서 먼저 보인다. VS사업본부의 2분기 매출은 3조 259억 원으로 6.2% 늘었지만, 영업이익은 2분기 기준 최대인 1,912억 원이었다. 1분기 영업이익률 6.9%는 보쉬 모빌리티(1.8%)의 3배, 콘티넨탈(3.9%)보다 높다. "
     "다만 전기차 수요 정체로 회사도 완성차 수요 회복이 제한적이라고 봤다.",
     ["L3-M-001", "L3-M-002", "L3-E-005", "L3-I-002", "L3-I-007"]),
    ("배터리 소프트웨어는 판매 채널부터 확보했다. LG에너지솔루션은 GM·Magna·Wipro가 세운 차량 SW 마켓 SDVerse에 배터리 기업 최초로 합류해 배터리 SW 5종을 올렸지만, 고객과 수익 모델은 아직 공개되지 않았다.",
     ["L3-M-006", "L3-E-003", "L3-I-005"]),
]
narrative_html = "".join(para(t, ids) for t, ids in NARRATIVE)
DIR = {"강화": "up", "약화": "down", "중립": "flat"}
irows = "".join(f"""<tr id="{E(r['id'])}"><td><span class="dir {DIR[r['direction']]}">{E(r['direction'])}</span></td>
  <td class="tgt">{E(r['target'])}</td><td>{E(r['statement'])}</td><td>{tags(r['basis'])}</td><td class="idc"><code>{E(r['id'])}</code></td></tr>"""
  for r in recs if r["type"] == "해석")

# 3. 주요 사건 (최신순) ------------------------------------------------
EVENTS_LEAD = ("10월 르노 통합 콕핏 공급 발표가 가장 최근의 큰 사건이다. 그 앞에는 6월 NVIDIA M.A.P. 협력(ADAS·센싱), 4월 LG에너지솔루션의 SDVerse 합류, 연초 CES의 AI 캐빈·자율주행 부품 공개가 있다.")
events = sorted([r for r in recs if r["type"] == "사건" and r.get("verified")], key=lambda r: r["date"], reverse=True)
erows = "".join(f"""<li id="{E(r['id'])}"><time>{E(r['date'])}</time><div><b>{E(r['actor'])}</b> {E(r['statement'])}
  <div class="src">{src_links(r)} <code>{E(r['id'])}</code></div></div></li>""" for r in events)

# 4. 전망 --------------------------------------------------------------
FORECAST_LEAD = ("2027년 말을 기준으로 두 시나리오를 세웠다. 갈림길은 르노에 이은 통합 콕핏 수주와 ADAS·라이다 수주가 고객명과 함께 나오는지, "
                 "그리고 전기차 수요 정체 속에서 VS 이익률을 지키는지다.")
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

# 5. 제품군별 공급 단계 ---------------------------------------------
SG = ["콘셉트", "수주(고객 비공개)", "수주(고객·차종 공개)", "양산 적용"]
SG_DEF = {
    "콘셉트": "전시·개발 착수·협력 발표 단계다.",
    "수주(고객 비공개)": "수주가 공식 확인됐지만 고객이 비공개다.",
    "수주(고객·차종 공개)": "고객과 차종이 공개된 수주다.",
    "양산 적용": "양산 차량에 탑재돼 출하됐다.",
}
STAGE_LEAD = ("양산 단계에 있는 것은 AI 이전부터의 강점인 텔레매틱스와 차량용 OLED다. AI 신영역 다섯 가운데 고객·차종이 공개된 수주는 르노 통합 콕핏 한 건이고, "
              "라이다는 2028년 탑재 목표만 보도됐으며, AI 캐빈·ADAS·배터리 SW는 콘셉트 단계다.")
CUST = {"기존 강점": "platform", "AI 신영역": "brand"}
CUST_DEF = {"기존 강점": "AI 이전부터 매출이 있던 제품군이다.", "AI 신영역": "SDV·센싱·AI 캐빈처럼 AI로 새로 여는 제품군이다."}
# (제품군, 단계, 잠정, 구분, 근거, 기록)
STAGES = [
    ("텔레매틱스 (LG전자)", "양산 적용", False, "기존 강점", "점유율 23%, 1위", ["L3-M-003"]),
    ("차량용 OLED (LG디스플레이)", "양산 적용", False, "기존 강점", "점유율 15.9%(2위), 완성차 10여 곳 공급, 고객명 비공개", ["L3-M-005"]),
    ("통합 콕핏·SDV (LG전자)", "수주(고객·차종 공개)", False, "AI 신영역", "르노 New Trafic E-Tech Electric 공급 발표, 규모·출하 시점 비공개", ["L3-E-006"]),
    ("AI 캐빈 (LG전자)", "콘셉트", False, "AI 신영역", "온디바이스 AI 캐빈 플랫폼, 인캐빈 센싱 양산 논의 중", ["L3-E-001"]),
    ("ADAS (LG전자)", "콘셉트", False, "AI 신영역", "DRIVE Hyperion 기반 개발 착수", ["L3-E-004"]),
    ("라이다·센싱 (LG이노텍)", "수주(고객 비공개)", True, "AI 신영역", "Aeva 공동 라이다, 2028년 '글로벌 완성차' 탑재 목표(언론 보도, 회사는 고객·수주 미공개)", ["L3-M-004", "L3-E-002"]),
    ("배터리 SW (LG에너지솔루션)", "콘셉트", False, "AI 신영역", "SDVerse에 5종 등록, 고객·수익 모델 미공개", ["L3-M-006"]),
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
    ("판정 단계: 공급 단계", ["단계", "기준"], [[gauge(SG, k), E(v)] for k, v in SG_DEF.items()]),
    ("옆 표시: 제품군 구분", ["구분", "정의"], [[side(k), E(v)] for k, v in CUST_DEF.items()]),
], extra_rules=[L_RULE, "포털 게이지는 AI 신영역만 센다. 기존 강점은 비교 기준으로 남긴다."])
LEDGER_LEAD = "수익을 판단할 수 있는 수치를 정리했다. 수주잔고는 회사가 금액을 공개하지 않아 다음 회차에 확인한다."
LEDGER = [
    ("VS 2분기 매출", "3조 259억 원 (+6.2%)", "LG전자 IR", "2026-Q2", "실적", ["L3-M-001"]),
    ("VS 2분기 영업이익률", "6.3% (영업이익 1,912억 원, 2분기 최대)", "LG전자 IR", "2026-Q2", "실적", ["L3-M-001"]),
    ("VS 1분기 영업이익률 vs Tier 1", "6.9% vs 보쉬 1.8%·콘티넨탈 3.9%", "분기보고서·언론", "2026-Q1", "실적", ["L3-M-002"]),
    ("LG이노텍 센싱 매출", "2030년 약 2조 원 (모빌리티 전체 약 5조 원)", "LG이노텍", "2026-04", "목표", ["L3-M-004"]),
]
ledger_rows = "".join(f"""<tr><td class="tgt">{E(a)}</td><td>{E(b)}</td><td>{E(c)}</td><td>{E(d)}</td><td>{E(e)}</td><td>{tags(ids)}</td></tr>""" for a, b, c, d, e, ids in LEDGER)
STAGE_NOTE = "판정: 양산 단계는 기존 강점(텔레매틱스·OLED), AI 신영역 중 고객·차종이 공개된 것은 르노 통합 콕핏 한 건이다."

# 6. 핵심 지표 ---------------------------------------------------------
INDICATOR_NAMES = {"L3-T1": "VS 매출·이익", "L3-T2": "글로벌 Tier 1 대비 수익성", "L3-T3": "텔레매틱스·인포테인먼트 점유율",
                   "L3-T4": "통합 콕핏·SDV 수주", "L3-T5": "센싱 사업", "L3-T6": "차량용 디스플레이",
                   "L3-T7": "배터리 SW", "L3-T8": "AI 기능 양산"}
metrics = sorted([r for r in recs if r["type"] == "지표"], key=lambda r: (r["indicator"], -r["importance"]))
filled = {r["indicator"] for r in metrics if r.get("verified")}
empty_ind = [f"{k} {v}" for k, v in INDICATOR_NAMES.items() if k not in filled]
METRICS_LEAD = (f"추적 지표 8개 중 {len(filled)}개의 값을 원문으로 확인했다. "
                "T4 통합 콕핏·SDV 수주와 T8 AI 기능 양산은 수치 대신 사건으로 추적한다(현재 르노 1건, AI 기능 양산 0건). 2030 목표치와 고객 비공개 항목에는 주의 표시를 달았다.")
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

page = f"""<title>L3 LG AI 모빌리티 R1</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans+KR:wght@400;500;600&family=Noto+Serif+KR:wght@600;800&display=swap">
<style>{CSS}</style>
<main>
  <header class="narrow">
    <div class="eyebrow"><span>LG Group AI</span><span>L3 · AI Mobility / SDV·AIDV</span><span>R1 기준 회차 · 2026-10-09</span></div>
    <h1>{E(TITLE)}</h1>
    <p class="question">고정 질문 v1.0 — {E(QUESTION)}</p>
  </header>
  <section class="answer-box"><h2>한 줄 답</h2>
    <p class="answer narrow">{E(ONE_LINE)} {tags(ONE_LINE_BASIS)}</p><dl class="arows">{answer_rows}</dl></section>
  <section><h2>해석</h2><div class="narrative">{narrative_html}</div>
    <div class="tablewrap"><table><thead><tr><th>방향</th><th>대상</th><th>해석</th><th>근거</th><th>기록</th></tr></thead><tbody>{irows}</tbody></table></div></section>
  <section><h2>주요 사건 <small>최신순 · 원문 확인된 것만</small></h2><p class="lead">{E(EVENTS_LEAD)}</p><ul class="timeline">{erows}</ul></section>
  <section><h2>전망 <small>2027년 말까지, 공급 범위가 넓어질까</small></h2><p class="lead">{E(FORECAST_LEAD)}</p>
    <div class="scens">{scen_html}</div>
    <h3 class="subhead">세부 판정 근거</h3>
    <p class="lead muted">각 세부 전망이 적중하거나 빗나갔을 때 어느 시나리오 쪽 신호인지 표시했다. 확인 시점이 오면 확인 방법대로 판정한다.</p>
    <div class="tablewrap"><table><thead><tr><th>세부 전망</th><th>확인 시점</th><th>적중 시</th><th>빗나갈 시</th><th>상태</th><th>근거</th></tr></thead><tbody>{frows}</tbody></table></div></section>
  <section><h2>제품군별 공급 단계 <small>기존 강점과 AI 신영역 · 수익 수치</small></h2><p class="lead">{E(STAGE_LEAD)}</p>
    {criteria_html}
    <div class="ladder mapgrid auto">{stage_rows}</div><p class="gapnote">{E(STAGE_NOTE)}</p>
    <h3 class="subhead">수익 수치</h3><p class="lead">{E(LEDGER_LEAD)}</p>
    <div class="tablewrap"><table><thead><tr><th>항목</th><th>값</th><th>출처</th><th>시점</th><th>종류</th><th>기록</th></tr></thead><tbody>{ledger_rows}</tbody></table></div></section>
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
anchors = set(re.findall(r'id="(L3-[A-Z]-\d{3})"', page))
bad = sorted({i for i in re.findall(r'href="#(L3-[A-Z]-\d{3})"', page) if i not in anchors})
order = [page.index(f"<h2>{h}") for h in ("한 줄 답", "해석", "주요 사건", "전망", "제품군별 공급 단계", "핵심 지표")]
print("article_r1.html 생성,", len(page), "bytes; 앵커 없는 근거 링크:", bad or "없음", "; 섹션 순서 정상:", order == sorted(order))
# ---------- 포털 신호: 판정 칩과 게이지를 판정 데이터에서 계산해 내보낸다
SIGNAL_CHIP = 'AI 신영역 공개 수주 1건'
SIGNAL_GAUGE = 'AI 신영역 5개 중 고객 공개 수주 이상'
SIGNAL_FRONTIER = '통합 콕핏·라이다'
signal = {"question": 'L3', "round": 1, "chip": SIGNAL_CHIP, "gauge": SIGNAL_GAUGE, "frontier": SIGNAL_FRONTIER,
          "on": sum(1 for r in STAGES if r[3] == "AI 신영역" and SG.index(r[1]) >= 2), "of": sum(1 for r in STAGES if r[3] == "AI 신영역")}
# 포털 띠: 항목마다 단계(0~3)와 잠정 여부
signal["kind"] = "band"
signal["levels"] = list(SG)
signal["items"] = [[r[0], SG.index(r[1]), bool(r[2])] for r in STAGES if r[3] == "AI 신영역"]
(ROOT / "signal_r1.json").write_text(json.dumps(signal, ensure_ascii=False, indent=1), encoding="utf-8")
print("signal_r1.json:", signal["chip"], f'{signal["on"]}/{signal["of"]}')
sys.exit(1 if bad or order != sorted(order) else 0)

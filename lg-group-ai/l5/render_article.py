"""records.jsonl → 기준 아티클 HTML (L5 R1).
순서: 한 줄 답 → 해석 → 주요 사건 → 전망 → 분야별 연구 단계 → 핵심 지표 → 미확인·경고
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

TITLE = "AI가 찾은 소재·신약은 어디까지 제품이 됐나"
QUESTION = "AI가 소재·배터리·신약의 탐색과 개발을 얼마나 개선하며, 연구 결과는 실험·제품·사업화로 어디까지 이어지는가?"

# 1. 한 줄 답 ----------------------------------------------------------
ONE_LINE = ("2026년 10월 현재 AI는 LG의 탐색 단계를 크게 줄였다. 화장품 소재 4,000만 건 검토가 22개월에서 하루로, 탈모 소재 후보 42만 개 선별이 하루로 줄었다(회사 발표). "
            "그러나 AI로 찾은 물질 가운데 제품·임상까지 간 것은 아직 없다. 가장 앞선 탈모 소재 '람시딜'은 학회에서 효과를 발표하고 제품화를 준비 중이고, 신약(펩타이드·항체)은 발견 단계, 배터리는 자동 실험 루프를 만든 단계다.")
ONE_LINE_BASIS = ["L5-I-001", "L5-I-002", "L5-I-003"]
ANSWER_ROWS = [
    ("개선 폭 (결과)", "탐색: 4,000만 건 22개월 → 1일, 42만 후보 → 1일. 모두 회사 발표 수치.", ["L5-M-001", "L5-M-002"]),
    ("개선 폭 (목표)", "개발 기간: LG화학 항체 발굴 5년+ → 절반, LG에너지솔루션 배터리 개발 → 절반. 결과치 미공개.", ["L5-M-003", "L5-M-004"]),
    ("가장 앞선 것", "화장품 원료 람시딜: 실험 검증(세계모발학회 발표), 제품화 준비.", ["L5-M-002"]),
    ("발견 단계", "신약: D&D Pharmatech 경구 펩타이드, LabGenius 다중항체(옵션 계약), Galux 항암 단백질.", ["L5-E-002", "L5-E-003"]),
    ("연구 역량", "소재 생성 벤치마크 종합 2위, 특허 출원 838건, EXAONE Discovery '길목 특허' 등록.", ["L5-M-006", "L5-M-005", "L5-E-001"]),
]
answer_rows = "".join(f'<div class="arow"><dt>{E(k)}</dt><dd>{E(v)} {tags(ids)}</dd></div>' for k, v, ids in ANSWER_ROWS)

# 2. 해석 --------------------------------------------------------------
NARRATIVE = [
    ("AI는 후보를 찾는 시간을 크게 줄였다. LG AI연구원은 EXAONE Discovery로 화장품 소재 4,000만 건 이상의 물성·합성 용이성·안전성 검토를 22개월에서 하루로 줄였다고 밝혔고, LG생활건강과 함께 42만 개 넘는 후보에서 탈모 관리 소재 '람시딜'을 하루 만에 골라냈다. "
     "다만 이 수치는 모두 회사 발표이며 독립 검증은 없다.",
     ["L5-M-001", "L5-M-002", "L5-I-001"]),
    ("탐색에서 제품까지의 거리는 아직 멀다. AI로 찾은 물질 가운데 제품이 되거나 임상에 들어간 것은 없다. 가장 앞선 람시딜은 스테로이드 유래 성분 없이 탈모 방지 효과를 보였다는 결과를 세계모발학회에서 발표하고 제품화를 준비 중이다. "
     "신약은 LG AI연구원과 D&D Pharmatech의 경구 펩타이드, LG화학과 LabGenius의 다중항체 항암 후보 모두 발견 단계다.",
     ["L5-M-002", "L5-E-002", "L5-E-003", "L5-I-002"]),
    ("AI 제안과 실험을 잇는 폐쇄 루프가 만들어지고 있다. D&D Pharmatech은 합성·실험 결과를 LG의 모델에 되먹이고, LabGenius는 AI 설계와 로봇 실험을 반복한다. LG에너지솔루션은 AI가 좁힌 전해질 후보를 자동 설비가 만들어 시험하고, 초기 충방전 데이터만으로 수명을 예측한다. "
     "탐색 속도가 실험 속도에 막히지 않게 하려는 구조다.",
     ["L5-E-002", "L5-E-003", "L5-E-005", "L5-I-003"]),
    ("개발 기간 단축은 아직 목표다. LG화학은 통상 5년 넘게 걸리는 항체 후보 발굴을 절반으로, LG에너지솔루션은 배터리 개발 기간 또는 자원을 절반으로 줄이는 것이 목표지만 측정된 결과는 공개되지 않았다. "
     "자체 플랫폼과 외부 협력도 함께 쓴다. 소재·화장품은 EXAONE Discovery, 신약은 외부 바이오텍, 외부 소재 기업 지원은 LG CNS가 창립 멤버로 합류한 CuspAI 협력체(48개 기관)를 통한다.",
     ["L5-M-003", "L5-M-004", "L5-E-006", "L5-I-004", "L5-I-005"]),
    ("연구 역량 자체는 글로벌 수준이다. 신소재 생성 벤치마크 LeMat-GenBench 종합 2위, 특허 출원 838건, 주요 학회 논문 363편이고, EXAONE Discovery는 우회하기 어려운 '길목 특허'로 등록됐다. "
     "GS칼텍스와 만든 AI 데이터센터용 액침 냉각유 소재처럼, AI for Science가 다른 테마의 소재가 되는 연결도 생기고 있다.",
     ["L5-M-006", "L5-M-005", "L5-E-001", "L5-E-004", "L5-I-006", "L5-I-007"]),
]
narrative_html = "".join(para(t, ids) for t, ids in NARRATIVE)
DIR = {"강화": "up", "약화": "down", "중립": "flat"}
irows = "".join(f"""<tr id="{E(r['id'])}"><td><span class="dir {DIR[r['direction']]}">{E(r['direction'])}</span></td>
  <td class="tgt">{E(r['target'])}</td><td>{E(r['statement'])}</td><td>{tags(r['basis'])}</td><td class="idc"><code>{E(r['id'])}</code></td></tr>"""
  for r in recs if r["type"] == "해석")

# 3. 주요 사건 (최신순) ------------------------------------------------
EVENTS_LEAD = ("6~7월에 사건이 몰렸다. D&D Pharmatech·LabGenius와의 신약 협력, ICML의 람시딜·액침 냉각유 공개, LG에너지솔루션의 자동 실험 R&D, LG CNS의 CuspAI 협력체 합류다. 그 앞에는 2월 EXAONE Discovery 특허 등록이 있다.")
events = sorted([r for r in recs if r["type"] == "사건" and r.get("verified")], key=lambda r: r["date"], reverse=True)
erows = "".join(f"""<li id="{E(r['id'])}"><time>{E(r['date'])}</time><div><b>{E(r['actor'])}</b> {E(r['statement'])}
  <div class="src">{src_links(r)} <code>{E(r['id'])}</code></div></div></li>""" for r in events)

# 4. 전망 --------------------------------------------------------------
FORECAST_LEAD = ("2027년 말을 기준으로 두 시나리오를 세웠다. 갈림길은 AI가 찾은 물질이 제품(람시딜)·전임상(신약)·양산 계획(배터리 소재)으로 넘어가는지, "
                 "아니면 탐색 속도 발표와 협력 계약에 머무는지다.")
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

# 5. 분야별 연구 단계 --------------------------------------------------
SG = ["가상 탐색", "실험 검증", "제품·임상 진입", "사업화"]
STAGE_LEAD = ("분야마다 가상 탐색 → 실험 검증 → 제품·임상 진입 → 사업화 중 어디에 있는지 판정했다. 오른쪽 표시는 그 분야를 자체 플랫폼으로 하는지 외부 협력으로 하는지다.")
CUST = {"자체 플랫폼": "brand", "외부 협력": "platform", "자체+외부": "contest"}
STAGES = [
    ("화장품 원료 (LG생활건강)", "실험 검증", "자체 플랫폼", "람시딜: 42만 후보 → 하루, 세계모발학회 효과 발표, 제품화 준비", ["L5-M-002"]),
    ("기타 소재 (액침 냉각유 등)", "실험 검증", "자체+외부", "GS칼텍스와 공동 개발한 AI 데이터센터용 액침 냉각유 실물 전시", ["L5-E-004"]),
    ("배터리 소재 (LG에너지솔루션)", "가상 탐색", "자체 플랫폼", "AI 에이전트 + 자동 실험 루프 구축, 결과 미공개", ["L5-E-005", "L5-M-004"]),
    ("신약 — 펩타이드 (LG AI연구원)", "가상 탐색", "외부 협력", "D&D Pharmatech과 경구 펩타이드, 발견 단계", ["L5-E-002"]),
    ("신약 — 항체 (LG화학)", "가상 탐색", "외부 협력", "LabGenius 다중항체 옵션 계약, Galux 항암 단백질, 자체 MediX", ["L5-E-003"]),
]
def sg4(v):
    i = SG.index(v)
    return "".join(f'<span class="pip{" on" if k <= i else ""}"></span>' for k in range(4)) + f'<span class="lv">{E(v)}</span>'
stage_rows = "".join(f"""<div class="rung"><div class="stage"><b>{E(d)}</b></div>
  <div class="lvcell"><span class="pips">{sg4(st)}</span></div>
  <div class="lvcell"><span class="own {CUST[c]}">{E(c)}</span></div>
  <p class="why">{E(w)} {tags(ids)}</p></div>""" for d, st, c, w, ids in STAGES)
LEDGER_LEAD = "AI가 줄였다고 밝힌 기간과, 줄이겠다는 목표를 나눠 적었다. 다음 회차부터 목표 줄이 결과 줄로 바뀌는지를 본다."
LEDGER = [
    ("화장품 소재 4,000만 건 검토", "약 22개월", "1일", "결과 (회사 발표)", "2026-02", ["L5-M-001"]),
    ("탈모 소재 후보 42만 개 선별", "—", "1일", "결과 (회사 발표)", "2026-07", ["L5-M-002"]),
    ("항체 신약 후보 발굴", "5년 이상", "절반 목표", "목표", "2026-06", ["L5-M-003"]),
    ("배터리 개발 기간·자원", "—", "절반 목표", "목표", "2026-07", ["L5-M-004"]),
]
ledger_rows = "".join(f"""<tr><td class="tgt">{E(a)}</td><td>{E(b)}</td><td>{E(c)}</td><td>{E(d)}</td><td>{E(e)}</td><td>{tags(ids)}</td></tr>""" for a, b, c, d, e, ids in LEDGER)
STAGE_NOTE = "판정: 가장 앞선 분야는 화장품 원료(실험 검증), 신약·배터리 소재는 가상 탐색 단계. 제품·임상에 들어간 AI 발굴 물질은 아직 없다 (R1 기준)."

# 6. 핵심 지표 ---------------------------------------------------------
INDICATOR_NAMES = {"L5-T1": "탐색 속도", "L5-T2": "실험 검증 결과", "L5-T3": "제품·임상 진입",
                   "L5-T4": "외부 연구 협력", "L5-T5": "개발 기간 단축", "L5-T6": "특허·논문",
                   "L5-T7": "소재 생성 AI 성능", "L5-T8": "외부 플랫폼 사업"}
metrics = sorted([r for r in recs if r["type"] == "지표"], key=lambda r: (r["indicator"], -r["importance"]))
filled = {r["indicator"] for r in metrics if r.get("verified")}
empty_ind = [f"{k} {v}" for k, v in INDICATOR_NAMES.items() if k not in filled]
METRICS_LEAD = (f"추적 지표 8개 중 {len(filled)}개의 값을 원문으로 확인했다. "
                "T3 제품·임상 진입(현재 0건)과 T4 외부 연구 협력은 사건으로 추적한다. 탐색 속도는 회사 발표 수치이고, 개발 기간 단축은 목표치라 주의 표시를 달았다.")
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

page = f"""<title>L5 LG AI for Science R1</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans+KR:wght@400;500;600&family=Noto+Serif+KR:wght@600;800&display=swap">
<style>{CSS}</style>
<main>
  <header class="narrow">
    <div class="eyebrow"><span>LG Group AI</span><span>L5 · AI for Science / Bio / Materials / Battery</span><span>R1 기준 회차 · 2026-10-09</span></div>
    <h1>{E(TITLE)}</h1>
    <p class="question">고정 질문 v1.0 — {E(QUESTION)}</p>
  </header>
  <section class="answer-box"><h2>한 줄 답</h2>
    <p class="answer narrow">{E(ONE_LINE)} {tags(ONE_LINE_BASIS)}</p><dl class="arows">{answer_rows}</dl></section>
  <section><h2>해석</h2><div class="narrative">{narrative_html}</div>
    <div class="tablewrap"><table><thead><tr><th>방향</th><th>대상</th><th>해석</th><th>근거</th><th>기록</th></tr></thead><tbody>{irows}</tbody></table></div></section>
  <section><h2>주요 사건 <small>최신순 · 원문 확인된 것만</small></h2><p class="lead">{E(EVENTS_LEAD)}</p><ul class="timeline">{erows}</ul></section>
  <section><h2>전망 <small>2027년 말까지, 탐색이 제품이 될까</small></h2><p class="lead">{E(FORECAST_LEAD)}</p>
    <div class="scens">{scen_html}</div>
    <h3 class="subhead">세부 판정 근거</h3>
    <p class="lead muted">각 세부 전망이 적중하거나 빗나갔을 때 어느 시나리오 쪽 신호인지 표시했다. 확인 시점이 오면 확인 방법대로 판정한다.</p>
    <div class="tablewrap"><table><thead><tr><th>세부 전망</th><th>확인 시점</th><th>적중 시</th><th>빗나갈 시</th><th>상태</th><th>근거</th></tr></thead><tbody>{frows}</tbody></table></div></section>
  <section><h2>분야별 연구 단계 <small>단계 판정 · 기간 단축 원장</small></h2><p class="lead">{E(STAGE_LEAD)}</p>
    <div class="ladder mapgrid auto">{stage_rows}</div><p class="gapnote">{E(STAGE_NOTE)}</p>
    <h3 class="subhead">기간 단축 원장</h3><p class="lead">{E(LEDGER_LEAD)}</p>
    <div class="tablewrap"><table><thead><tr><th>작업</th><th>기존</th><th>AI 적용</th><th>종류</th><th>시점</th><th>기록</th></tr></thead><tbody>{ledger_rows}</tbody></table></div></section>
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
anchors = set(re.findall(r'id="(L5-[A-Z]-\d{3})"', page))
bad = sorted({i for i in re.findall(r'href="#(L5-[A-Z]-\d{3})"', page) if i not in anchors})
order = [page.index(f"<h2>{h}") for h in ("한 줄 답", "해석", "주요 사건", "전망", "분야별 연구 단계", "핵심 지표")]
print("article_r1.html 생성,", len(page), "bytes; 앵커 없는 근거 링크:", bad or "없음", "; 섹션 순서 정상:", order == sorted(order))
sys.exit(1 if bad or order != sorted(order) else 0)

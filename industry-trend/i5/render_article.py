"""records.jsonl → 기준 아티클 HTML (I5 R1).
순서: 한 줄 답 → 해석 → 주요 사건 → 전망 → 판정(직무별 영향 단계) → 핵심 지표 → 다른 질문에서 인용한 기록 → 미확인·경고
"""
import json, html, re, sys
from pathlib import Path

ROOT = Path(__file__).parent
REPO = ROOT.parent.parent
sys.path.insert(0, str(REPO / "lib"))
from judge import gauge, criteria_panel
recs = [json.loads(l) for l in (ROOT / "records.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
by = {r["id"]: r for r in recs}
E = html.escape
CSS = (REPO / "lib" / "article.css").read_text(encoding="utf-8")
Q = "I5"

# 다른 질문 기록 (교차 인용)
CAT_DIR = {"C": "customer-lab", "I": "industry-trend", "S": "sales-marketing", "L": "lg-group-ai"}
def other(rid):
    q = rid.split("-")[0]
    f = REPO / CAT_DIR[q[0]] / q.lower() / "records.jsonl"
    for l in f.read_text(encoding="utf-8").splitlines():
        if l.strip():
            r = json.loads(l)
            if r["id"] == rid: return r
    raise SystemExit(f"교차 인용 기록 없음: {rid}")
def other_href(rid):
    q = rid.split("-")[0]
    pre = "../" if CAT_DIR[q[0]] == "industry-trend" else f"../../{CAT_DIR[q[0]]}/"
    return f"{pre}{q.lower()}/r1.html#{rid}"

def tags(ids):
    out = []
    for i in ids:
        if i in by: out.append(f'<a class="rid" href="#{E(i)}" title="{E(by[i]["statement"])}">{E(i)}</a>')
        else: out.append(f'<a class="rid" href="{E(other_href(i))}" title="{E(other(i)["statement"])}">{E(i)}</a>')
    return "".join(out)
def para(text, ids): return f"<p>{E(text)} {tags(ids)}</p>"
def src_links(r):
    return " · ".join(f'<a href="{E(s["url"])}" target="_blank" rel="noopener">{E(s["publisher"])}</a><span class="grade g{E(s["grade"])}">{E(s["grade"])}</span>' for s in r.get("sources", []))

TITLE = "AI는 어떤 일을 줄이고, 어떤 일을 만드나"
QUESTION = "AI는 어떤 직무의 채용과 고용을 실제로 줄이고 있고, 대신 어떤 새 직무와 업종이 생겨나고 있는가?"

# 1. 한 줄 답 ----------------------------------------------------------
ONE_LINE = ("2026년 10월 현재 AI의 고용 영향은 해고보다 신입 채용 축소로 나타나며, 미국과 한국 통계 모두에서 AI 노출 직무의 경력 초기 고용 감소가 확인된다(미국 22~25세 격차 19%, 한국 청년 일자리 감소의 약 94%가 AI 노출 업종). "
            "인과는 확정되지 않았고 경제 전체로는 아직 큰 충격이 보이지 않는다. 새 직무는 AI 엔지니어·컨설턴트와 비개발 AI 직무를 중심으로 채용공고에서 빠르게 늘지만(잡코리아 AI 전문 직무 +128%) 공식 직업분류에는 거의 반영되지 않았다.")
ONE_LINE_BASIS = ["I5-I-001", "I5-I-002", "I5-I-006", "I5-E-011"]
ANSWER_ROWS = [
    ("신입·청년 사무직", "통계로 확인. 미국 AI 노출 직무 22~25세 고용이 기대보다 19% 낮고(2025년 7월 자료 15%), 경력자에게는 격차가 없다. 한국은 2022~2026년 청년 일자리 감소의 약 94%가 AI 노출 업종이다. 한국은행은 AI를 주원인이 아닌 가속 요인으로 본다.", ["I5-M-001", "I5-M-002", "I5-E-015"]),
    ("고객응대·상담", "국지적 신호. Salesforce 지원 인력 9,000→5,000명, KB국민은행 상담사 264명 감소. 반면 Klarna는 사람 상담원을 다시 뽑았고 신한은행 상담 인력은 늘었다. 직무 전체 통계는 없다.", ["I5-E-004", "I5-M-016", "I5-E-002"]),
    ("소프트웨어 개발", "국지적 신호(한국은 통계로 확인, 잠정). 미국 개발 공고는 1년 반 새 15% 늘었지만 2020년보다 27.5% 적고 순증의 71%가 시니어다. 한국은 AI가 아닌 개발 공고 -6.6%, 프로그래밍 업종 청년 고용 -16.6%.", ["I5-M-007", "I5-M-012", "I5-M-002"]),
    ("새 직무·업종", "채용공고에서 통계로 확인(잠정). LinkedIn 떠오르는 직업 상위 5개 중 4개가 AI 직무, 잡코리아 AI 전문 직무 +128%·비개발 AI 직무 +325%. 공식 분류는 미국 SOC 2028 개정 전, 한국직업사전 AI 신규 직업 1개 확인.", ["I5-M-011", "I5-M-012", "I5-M-013", "I5-M-014"]),
    ("AI 사유 감원", "미국 2026년 1~9월 12만 136명(전체의 21%), 3~7월 사유 1위였다가 9월 5위. 기업이 밝힌 사유의 집계라 실제 대체 규모로 읽지 않는다.", ["I5-M-004", "I5-M-005", "I5-I-003"]),
]
answer_rows = "".join(f'<div class="arow"><dt>{E(k)}</dt><dd>{E(v)} {tags(ids)}</dd></div>' for k, v, ids in ANSWER_ROWS)

# 2. 해석 --------------------------------------------------------------
NARRATIVE = [
    ("AI의 고용 영향은 사람을 내보내는 쪽보다 새로 뽑지 않는 쪽으로 먼저 나타났다. 뉴욕 연준 조사에서 AI 때문에 해고한 서비스 기업은 1%였지만 채용을 줄인 곳은 12%였고, 줄어든 채용은 대졸 직무에 몰렸다. "
     "Stanford 연구진의 급여 자료 분석에서도 AI 노출이 큰 직무의 22~25세 고용은 기대보다 19% 낮지만 같은 직무의 경력자에게는 격차가 없다. 격차는 2025년 7월 자료의 15%에서 커졌다.",
     ["I5-M-008", "I5-M-001", "I5-E-014", "I5-I-002"]),
    ("한국도 같은 모양이다. 한국은행은 2022~2026년 청년 일자리 감소의 약 94%가 AI 노출 업종에서 나왔고, 같은 업종에서 50대 일자리는 늘었다고 분석했다. 업종별로는 정보서비스(-31.4%), 출판(-27.4%), 컴퓨터 프로그래밍(-16.6%)의 청년 고용이 크게 줄었다. "
     "9월 청년 취업자는 47개월 연속 감소했지만 사무종사자 전체는 24만 7천 명 늘었다. 다만 한국은행은 청년 고용 감소의 주원인을 AI로 보지 않고 경력직 선호 같은 기존 변화를 AI가 키운 것으로 봤다.",
     ["I5-M-002", "I5-M-003", "I5-M-015", "I5-E-015", "I5-I-001", "I5-I-008"]),
    ("기업이 AI를 감원 사유로 드는 일은 늘었다. 미국에서 AI를 사유로 든 감원은 2025년 1~11월 약 5만 5천 명(4.5%)에서 2026년 1~9월 12만 명(21%)으로 늘었고, 3~7월에는 다섯 달 연속 사유 1위였다. 그러나 8~9월에는 월 4천 명 아래로 내려갔다. "
     "Amazon은 2025년 10월 이후 3만 명 넘게 줄였지만 사유를 관료주의 축소로 설명했고, Oxford Economics는 일부 기업이 감원을 포장하려고 AI를 든다고 봤다. Yale Budget Lab은 경제 전체로는 안정에 가깝다고 평가했다.",
     ["I5-M-004", "I5-M-005", "I5-M-006", "I5-E-010", "I5-E-011", "I5-I-003"]),
    ("직무별로 보면 고객 상담과 소프트웨어 개발의 방향이 다르다. 상담은 Salesforce(지원 인력 약 4,000명 감축)와 KB국민은행(상담사 264명 감소)처럼 기업 단위 감축이 있지만, Klarna는 사람 상담원을 다시 뽑았고 신한은행은 AICC 도입 뒤에도 인력이 늘었다. "
     "개발은 수요가 사라지기보다 경력과 AI 쪽으로 옮겨 간다. 미국 개발 공고는 2025년 2월 이후 15% 늘었지만 순증의 71%가 시니어이고, 한국은 AI가 아닌 개발 공고가 6.6% 줄었다.",
     ["I5-E-004", "I5-M-016", "I5-E-002", "I5-M-007", "I5-M-012", "I5-I-004", "I5-I-005"]),
    ("새 일은 채용공고에서 먼저 보인다. LinkedIn의 2026년 미국 떠오르는 직업 상위 5개 중 4개가 AI 엔지니어·AI 컨설턴트·데이터 라벨러·AI 연구원이고, 잡코리아의 AI 전문 직무 공고는 1년 새 128%, AI 콘텐츠 크리에이터·AI 기획 같은 비개발 AI 직무는 325% 늘었다. "
     "공식 분류는 따라가지 못했다. 미국 표준직업분류는 2028년 적용을 목표로 아직 의견 검토 중이고, 한국직업사전에서 확인된 AI 신규 직업은 '인공지능서비스운영관리자' 하나다. 정부는 2030년까지 100만 명 AI 훈련과 함께 한국형 AI 노출지수·카나리아 대시보드를 만들어 감지 체계를 갖추기로 했다.",
     ["I5-M-011", "I5-M-012", "I5-M-013", "I5-M-014", "I5-M-017", "I5-I-006", "I5-I-007"]),
]
narrative_html = "".join(para(t, ids) for t, ids in NARRATIVE)
DIR = {"강화": "up", "약화": "down", "중립": "flat"}
irows = "".join(f"""<tr id="{E(r['id'])}"><td><span class="dir {DIR[r['direction']]}">{E(r['direction'])}</span></td>
  <td class="tgt">{E(r['target'])}</td><td>{E(r['statement'])}</td><td>{tags(r['basis'])}</td><td class="idc"><code>{E(r['id'])}</code></td></tr>"""
  for r in recs if r["type"] == "해석")

# 3. 주요 사건 (최신순) ------------------------------------------------
EVENTS_LEAD = ("2025년에는 개별 기업의 감축 발표(Salesforce·Accenture·Amazon)와 반대 사례(Klarna)가 이어졌다. 2026년에는 통계 분석이 쌓였다. Stanford 연구진은 신입 격차가 커졌다고 밝혔고, 한국은행은 두 차례 보고서로 한국의 같은 패턴을 확인했다. "
               "AI 사유 감원은 여름까지 1위를 지키다 9월 5위로 내려갔고, 정부는 7월 산업전환 고용안정 기본계획을 내놨다.")
events = sorted([r for r in recs if r["type"] == "사건" and r.get("verified")], key=lambda r: r["date"], reverse=True)
erows = "".join(f"""<li id="{E(r['id'])}"><time>{E(r['date'])}</time><div><b>{E(r['actor'])}</b> {E(r['statement'])}
  <div class="src">{src_links(r)} <code>{E(r['id'])}</code></div></div></li>""" for r in events)

# 4. 전망 --------------------------------------------------------------
FORECAST_LEAD = ("2027년 말을 기준으로 두 시나리오를 세웠다. 갈림길은 신입 채용 축소가 경력 초기 전반으로 번지는지, 그리고 새 AI 직무와 개발 공고 회복이 그 빈자리를 메우는지다.")
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
frows = "".join(f"""<tr id="{E(r['id'])}"><td class="stmt">{E(r['statement'])}<small>확인 방법: {E(r['method'])}</small>
  <small>예측 근거: {E(r.get('reasoning',''))}</small><small>틀릴 수 있는 이유: {E(r.get('counter',''))}</small></td>
  <td class="asof">{E(r['due'])}</td><td>{side(sign.get(r['id'],{}).get('hit',set()))}</td><td>{side(sign.get(r['id'],{}).get('miss',set()))}</td>
  <td><span class="fstat">{E(r['forecast_status'])}</span></td><td>{tags(r['basis'])}</td></tr>""" for r in details)

# 5. 판정: 직무별 영향 단계 --------------------------------------------
SG = ["신호 없음", "국지적 신호", "통계로 확인", "구조적 변화"]
SG_DEF = {
    "신호 없음": ("감소·증가를 보여 주는 발표나 통계가 없다", "—"),
    "국지적 신호": ("개별 기업의 감원·채용 발표, 사례 보도", "기업 발표, 언론 보도"),
    "통계로 확인": ("공식 통계 또는 대규모 연구·채용 자료에서 감소·증가가 보인다", "정부 통계, 급여·채용공고 자료 분석"),
    "구조적 변화": ("여러 나라·업종에서 2년 이상 지속되고 전체 고용 수준에서 확인된다", "복수 국가 공식 통계"),
}
STAGE_LEAD = ("직무 네 개를 미국(글로벌 선행)과 한국으로 나눠 판정했다. 신입·청년 사무직은 두 나라 모두 통계로 확인 단계이고, 구조적 변화로 올리려면 인과가 더 분명해지고 전체 고용 수준에서 확인돼야 한다. "
              "새 직무는 채용 플랫폼 자료뿐이라 잠정이다.")
# (항목, 글로벌, 글로벌 잠정, 한국, 한국 잠정, 근거, 기록)
STAGES = [
    ("신입·청년 사무직", "통계로 확인", False, "통계로 확인", False, "미국 22~25세 격차 19%(급여 자료) / 한국 청년 일자리 감소의 약 94%가 AI 노출 업종(한국은행)", ["I5-M-001", "I5-M-002", "I5-M-003"]),
    ("고객응대·상담", "국지적 신호", False, "국지적 신호", False, "Salesforce 9,000→5,000명, Klarna 재채용 / KB국민은행 상담사 -264명, 신한은행 증가", ["I5-E-004", "I5-E-002", "I5-M-016"]),
    ("소프트웨어 개발", "국지적 신호", False, "통계로 확인", True, "미국 개발 공고 회복(+15%)이나 시니어 중심 / 한국 프로그래밍 업종 청년 고용 -16.6%, AI 외 개발 공고 -6.6%(한 플랫폼)", ["I5-M-007", "I5-M-002", "I5-M-012"]),
    ("새 직무·업종", "통계로 확인", True, "통계로 확인", True, "LinkedIn 상위 5개 중 4개 AI 직무 / 잡코리아 AI 전문 직무 +128%. 공식 분류 미반영", ["I5-M-011", "I5-M-012", "I5-M-014"]),
]
def tip_sg(v):
    th, ev = SG_DEF[v]
    return f"{v} — 기준: {th}. 근거: {ev}."
def cell(v, pv):
    if v is None:
        return '<span class="pips"><span class="lv muted">자료 없음</span></span>'
    return gauge(SG, v, tip_sg(v), pv)
criteria_html = criteria_panel([
    ("판정 단계: 직무별 영향", ["단계", "기준", "인정하는 근거"], [[gauge(SG, k), E(v[0]), E(v[1])] for k, v in SG_DEF.items()]),
], rules=[
    "기업이 감원 사유로 AI를 든 발표는 회사 주장으로 보고 국지적 신호까지만 인정한다.",
    "AI 노출 직무와 비노출 직무를 비교한 통계여야 통계로 확인으로 올린다. 전체 고용 증감만으로는 올리지 않는다.",
    "한 채용 플랫폼 자료로 판정한 칸은 잠정으로 둔다.",
    "인과를 확인하지 않은 통계는 그 점을 본문에 병기한다.",
    "기준을 직접 재는 수치가 없어 간접 근거로 판정한 칸은 '잠정'이며, 게이지의 점선 테두리와 빗금으로 표시한다.",
])
stage_rows = "".join(f"""<div class="rung"><div class="stage"><b>{E(d)}</b></div>
  <div class="lvcell"><span class="region">글로벌</span>{cell(g, gp)}</div>
  <div class="lvcell"><span class="region">한국</span>{cell(k, kp)}</div>
  <p class="why">{E(w)} {tags(ids)}</p></div>""" for d, g, gp, k, kp, w, ids in STAGES)
NEW_LEAD = ("이번 회차에 확인된 새 직무와 업종이다. 채용공고 규모와 공식 분류 반영 여부를 함께 적었다.")
NEWJOBS = [
    ("AI 엔지니어", "미국 떠오르는 직업 1위", "미반영", ["I5-M-011"]),
    ("AI 컨설턴트·전략가", "미국 떠오르는 직업 2위", "미반영", ["I5-M-011"]),
    ("데이터 라벨러", "미국 떠오르는 직업 4위", "미반영", ["I5-M-011"]),
    ("AI 콘텐츠 크리에이터·AI 기획·AI 사업전략", "잡코리아 공고 +405%·+363%·+313%", "미반영(생성형 AI 콘텐츠 직업 미등재)", ["I5-M-012", "I5-M-013"]),
    ("인공지능서비스운영관리자", "공고 규모 미확인", "한국직업사전 2025 등재", ["I5-M-013"]),
]
new_rows = "".join(f"""<tr><td class="tgt">{E(a)}</td><td>{E(b)}</td><td>{E(c)}</td><td>{tags(ids)}</td></tr>""" for a, b, c, ids in NEWJOBS)

# 6. 핵심 지표 ---------------------------------------------------------
INDICATOR_NAMES = {"I5-T1": "AI 노출 직무 연령대별 고용", "I5-T2": "AI 사유 감원", "I5-T3": "직무별 채용·채용 계획",
                   "I5-T4": "AI 업무 활용 분포", "I5-T5": "새 직무 공고 규모", "I5-T6": "공식 직업분류 신설",
                   "I5-T7": "한국 청년·사무직 고용", "I5-T8": "재교육·고용 정책"}
metrics = sorted([r for r in recs if r["type"] == "지표"], key=lambda r: (r["indicator"], -r["importance"]))
filled = {r["indicator"] for r in metrics if r.get("verified")}
METRICS_LEAD = (f"추적 지표 8개 중 {len(filled)}개의 값을 확인했다. Indeed·Anthropic·시카고 연준 값은 원문 대신 주요 언론 인용으로 확인해 표시를 달았고, AI 사유 감원은 기업이 밝힌 사유의 집계다.")
def fmt_val(r):
    v, u = r.get("value"), r.get("unit", "")
    s = f"{v:,.10g}" if isinstance(v, (int, float)) else str(v)
    return f"{s}{'' if u.startswith('%') else ' '}{u}"
mrows = "".join(f"""<tr id="{E(r['id'])}"><td class="ind">{E(r['indicator'])}<small>{E(INDICATOR_NAMES[r['indicator']])}</small></td>
  <td class="stmt">{E(r['statement'])} {'<span class="warn">충돌·주의</span>' if r.get('check_flags') else ''}<div class="src">{src_links(r)}</div></td>
  <td class="num">{E(fmt_val(r))}</td><td class="asof">{E(r['as_of'])}<small>{E(r['region'])}</small></td><td class="idc"><code>{E(r['id'])}</code></td></tr>""" for r in metrics)

# 7. 다른 질문에서 인용한 기록 -----------------------------------------
xrefs = []
for r in recs:
    for x in r.get("xref", []):
        if x not in [a for a, _ in xrefs]: xrefs.append((x, r["id"]))
xrows = "".join(f"""<tr><td><a class="rid" href="{E(other_href(x))}">{E(x)}</a></td><td>{E(other(x)['statement'])}</td><td>{tags([mine])}</td></tr>""" for x, mine in xrefs)

# 8. 미확인·경고 -------------------------------------------------------
warns = [(r, "원문 미확인" if r["type"] in ("지표", "사건") and not r.get("verified") else "주의") for r in recs
         if (r["type"] in ("지표", "사건") and not r.get("verified")) or r.get("check_flags")]
wrows = "".join(f"""<tr{' id="' + E(r['id']) + '"' if k == "원문 미확인" else ''}><td><code>{E(r['id'])}</code></td><td><span class="wk">{E(k)}</span></td><td>{E(r['statement'])}</td><td class="muted">{E('; '.join(r.get('check_flags', [])))}</td></tr>""" for r, k in warns)
counts = {t: sum(1 for r in recs if r["type"] == t) for t in ("지표", "사건", "해석", "전망")}

page = f"""<title>I5 AI와 일자리 R1</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans+KR:wght@400;500;600&family=Noto+Serif+KR:wght@600;800&display=swap">
<style>{CSS}</style>
<main>
  <header class="narrow">
    <div class="eyebrow"><span>AI Industry Trend · 산업 내 AI 자동화</span><span>I5 · AI &amp; Work</span><span>R1 기준 회차 · 2026-10-29</span><span><a href="../../changes.html#I5">변경 이력</a></span></div>
    <h1>{E(TITLE)}</h1>
    <p class="question">고정 질문 v1.0 — {E(QUESTION)}</p>
  </header>
  <section class="answer-box"><h2>한 줄 답</h2>
    <p class="answer narrow">{E(ONE_LINE)} {tags(ONE_LINE_BASIS)}</p><dl class="arows">{answer_rows}</dl></section>
  <section><h2>해석</h2><div class="narrative">{narrative_html}</div>
    <div class="tablewrap"><table><thead><tr><th>방향</th><th>대상</th><th>해석</th><th>근거</th><th>기록</th></tr></thead><tbody>{irows}</tbody></table></div></section>
  <section><h2>주요 사건 <small>최신순 · 원문 확인된 것만</small></h2><p class="lead">{E(EVENTS_LEAD)}</p><ul class="timeline">{erows}</ul></section>
  <section><h2>전망 <small>2027년 말까지, 신입 감소는 번질까</small></h2><p class="lead">{E(FORECAST_LEAD)}</p>
    <div class="scens">{scen_html}</div>
    <h3 class="subhead">세부 판정 근거</h3>
    <p class="lead muted">각 세부 전망이 적중하거나 빗나갔을 때 어느 시나리오 쪽 신호인지 표시했다. 확인 시점이 오면 확인 방법대로 판정한다.</p>
    <div class="tablewrap"><table><thead><tr><th>세부 전망</th><th>확인 시점</th><th>적중 시</th><th>빗나갈 시</th><th>상태</th><th>근거</th></tr></thead><tbody>{frows}</tbody></table></div></section>
  <section><h2>직무별 영향 단계 <small>줄어드는 일과 생기는 일</small></h2><p class="lead">{E(STAGE_LEAD)}</p>
    {criteria_html}
    <div class="ladder mapgrid auto">{stage_rows}</div>
    <h3 class="subhead">새 직무·업종</h3><p class="lead">{E(NEW_LEAD)}</p>
    <div class="tablewrap"><table><thead><tr><th>직무·업종</th><th>채용 규모</th><th>공식 분류</th><th>근거</th></tr></thead><tbody>{new_rows}</tbody></table></div></section>
  <section><h2>핵심 지표 <small>추적 지표 {len(filled)}/8개 값 확보</small></h2><p class="lead">{E(METRICS_LEAD)}</p>
    <div class="tablewrap"><table><thead><tr><th>추적 지표</th><th>내용 · 출처</th><th style="text-align:right">현재값</th><th>기준 시점</th><th>기록</th></tr></thead><tbody>{mrows}</tbody></table></div></section>
  <section><h2>다른 질문에서 인용한 기록 <small>같은 사실을 다룬 다른 질문</small></h2>
    <div class="tablewrap"><table><thead><tr><th>기록</th><th>진술</th><th>이 질문의 관련 기록</th></tr></thead><tbody>{xrows}</tbody></table></div></section>
  <section><h2>미확인·경고 <small>본문 판단에서 빼거나 주의해서 쓴 기록</small></h2>
    <div class="tablewrap"><table><thead><tr><th>기록</th><th>구분</th><th>진술</th><th>사유</th></tr></thead><tbody>{wrows}</tbody></table></div></section>
  <footer>
    <span>이 글은 4유형 기록 {len(recs)}건(지표 {counts['지표']} · 사건 {counts['사건']} · 해석 {counts['해석']} · 전망 {counts['전망']})에서 생성했습니다. 문장 옆 번호를 누르면 해당 기록으로 이동합니다.</span>
        <span>출처 등급 A = 1차 조사·공식 발표, B = 주요 언론·2차 보도, C = 블로그·출처 불명(원문 확인 전까지 판단에 쓰지 않음).</span>
  </footer>
</main>
"""
(ROOT / "article_r1.html").write_text(page, encoding="utf-8")
anchors = set(re.findall(rf'id="({Q}-[A-Z]-\d{{3}})"', page))
bad = sorted({i for i in re.findall(rf'href="#({Q}-[A-Z]-\d{{3}})"', page) if i not in anchors})
order = [page.index(f"<h2>{h}") for h in ("한 줄 답", "해석", "주요 사건", "전망", "직무별 영향 단계", "핵심 지표", "다른 질문에서 인용한 기록", "미확인·경고")]
print("article_r1.html 생성,", len(page), "bytes; 앵커 없는 근거 링크:", bad or "없음", "; 섹션 순서 정상:", order == sorted(order))
# ---------- 포털 신호
signal = {"question": Q, "round": 1, "chip": "신입 감소 통계로 확인, 새 직무는 공고로", "gauge": "직무 4개 중 통계로 확인 이상(글로벌)",
          "frontier": "신입·청년 사무직", "on": sum(1 for r in STAGES if r[1] in ("통계로 확인", "구조적 변화")), "of": len(STAGES),
          "kind": "band", "levels": list(SG), "items": [[r[0], SG.index(r[1]), bool(r[2])] for r in STAGES if r[1] is not None]}
(ROOT / "signal_r1.json").write_text(json.dumps(signal, ensure_ascii=False, indent=1), encoding="utf-8")
print("signal_r1.json:", signal["chip"], f'{signal["on"]}/{signal["of"]}')
sys.exit(1 if bad or order != sorted(order) else 0)

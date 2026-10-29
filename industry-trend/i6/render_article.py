"""records.jsonl → 기준 아티클 HTML (I6 R1).
순서: 한 줄 답 → 해석 → 주요 사건 → 전망 → 판정(영역별 상용화 단계) → 핵심 지표 → 다른 질문에서 인용한 기록 → 미확인·경고
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
Q = "I6"

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

TITLE = "사람 없이 돌아가는 공장·창고·도로는 어디까지 왔나"
QUESTION = "사람 없이 돌아가는 생산·물류·이동은 어디까지 진행되고 있는가?"

# 1. 한 줄 답 ----------------------------------------------------------
ONE_LINE = ("2026년 10월 현재 사람 없이 돌아가는 영역 중 대규모 상용에 들어선 것은 로보택시뿐이다(Waymo 미국 11개 대도시권·주 50만 건 유료 운행, Baidu 28개 도시). "
            "공장은 로봇이 연 60만 대씩 늘지만 완전 무인 공장은 검증된 사례가 드물고, 물류·드론 배송·무인 트럭은 제한 상용, 휴머노이드는 시범 운영 단계다. 확산을 가장 크게 막는 것은 안전 검증과 사람 감독 요구다.")
ONE_LINE_BASIS = ["I6-I-001", "I6-I-003", "I6-I-005", "I6-I-007"]
ANSWER_ROWS = [
    ("로보택시", "대규모 상용(글로벌) / 시범 운영(한국). Waymo 약 3,500대·주 50만 건(2026년 상반기), Baidu 28개 도시, Pony.ai 1,975대. Tesla 무감독은 4~8대 추정. 서울은 11월 상암에서 안전관리자 탑승으로 시작.", ["I6-M-010", "I6-M-011", "I6-M-012", "I6-M-013", "I6-M-015"]),
    ("제조 무인화", "제한 상용(잠정). 2025년 산업용 로봇 설치 60만 대 이상(중국 59%), 가동 500만 대. 등대 공장 238곳·중국 선진급 스마트공장 7천 곳은 무인 기준이 아니고, 샤오미는 회사 발표 자동화율 81%.", ["I6-M-002", "I6-M-005", "I6-M-006", "I6-M-007"]),
    ("물류·배송", "제한 상용. Amazon 로봇 100만 대, 내부 문서상 2033년까지 채용 60만 명 대체 목표. Walmart 드론 배송 누적 100만 건(40%가 한 분기), Aurora 무인 트럭 10대.", ["I6-M-017", "I6-M-016", "I6-M-018"]),
    ("휴머노이드", "시범 운영. 2025년 출하 약 1만 8천 대(+508%)지만 용도는 연구·오락·데이터 수집 중심. Figure 02는 BMW에서 11개월 적재 후 퇴역, 현대차 아틀라스는 2028년 안전 검증부터.", ["I6-M-008", "I6-E-003", "I6-E-013"]),
    ("최대 제약", "안전 검증과 사람 감독 요구. Waymo 스쿨버스 사례 리콜, 한국 로보택시 안전관리자 탑승, Aurora 무인 트럭 대부분 관찰자 탑승.", ["I6-M-014", "I6-M-015", "I6-M-018", "I6-I-007"]),
]
answer_rows = "".join(f'<div class="arow"><dt>{E(k)}</dt><dd>{E(v)} {tags(ids)}</dd></div>' for k, v, ids in ANSWER_ROWS)

# 2. 해석 --------------------------------------------------------------
NARRATIVE = [
    ("사람이 아예 빠진 운영이 대규모로 굴러가는 곳은 도로다. Waymo는 2026년 상반기 약 3,500대로 미국 10개 시장에서 주당 약 50만 건 유료 운행을 했고, 7월 라스베이거스에서 완전 무인 운행을 시작했다. "
     "Baidu Apollo Go는 28개 도시에서 완전 무인 주행 2억 4천만 km를 넘겼고, Pony.ai는 6월 말 1,975대다. 반면 Tesla의 차 안 안전요원 없는 차량은 3월 기준 4~8대로 추정돼, 대규모 상용은 소수 사업자에 몰려 있다.",
     ["I6-M-010", "I6-E-012", "I6-M-011", "I6-M-012", "I6-M-013", "I6-I-001", "I6-I-002"]),
    ("공장은 로봇 대수로는 빠르게 무인화되고 있다. 2025년 세계 산업용 로봇 설치는 60만 대를 넘어 11% 늘었고 가동 대수는 500만 대가 됐다. 중국이 설치의 59%를 차지하고, 선진급 스마트공장도 7천 곳을 넘었다. "
     "그러나 '사람 없이 24시간 돌아가는 라인'은 검증된 사례가 드물다. 등대 공장(238곳)과 중국 스마트공장 등급은 무인 가동을 기준으로 삼지 않고, 대표 사례인 샤오미 창핑 공장도 회사 발표 자동화율 81%에 감독·유지보수 인력이 남아 있다.",
     ["I6-M-002", "I6-M-006", "I6-M-005", "I6-M-007", "I6-I-003", "I6-I-004"]),
    ("물류와 배송은 무인 운영이 빠르게 늘고, 그 영향은 해고보다 채용 회피로 나타난다. Amazon은 로봇 100만 대를 배치했고, 뉴욕타임스가 보도한 내부 문서에는 2033년까지 미국 채용 60만 명 이상을 로봇으로 대신한다는 목표가 담겼다(회사는 일부 팀의 시각이라고 반박). "
     "Walmart 드론 배송은 누적 100만 건 중 40%가 한 분기에 나왔고, Aurora는 트럭 30대 중 10대를 운전자 없이 운행한다.",
     ["I6-M-017", "I6-E-002", "I6-M-016", "I6-M-018", "I6-I-008"]),
    ("휴머노이드는 출하가 늘었지만 현장 운영은 시범 단계다. 2025년 출하는 약 1만 8천 대로 다섯 배 넘게 늘었고 Unitree 한 곳이 5,500대를 넘겼지만, 용도는 연구·오락·데이터 수집이 중심이다. "
     "공장 투입 사례인 Figure 02는 BMW에서 11개월 동안 부품 9만 개를 적재하고 퇴역했고, 현대차는 아틀라스를 2028년 미국 메타플랜트에서 안전 검증한 뒤 2030년부터 조립 공정으로 넓힌다.",
     ["I6-M-008", "I6-M-009", "I6-E-003", "I6-E-013", "I6-I-005"]),
    ("가장 큰 제약은 안전 검증과 사람 감독 요구다. 선두 Waymo도 스쿨버스를 지나친 사례 19건으로 NHTSA 조사를 받고 소프트웨어를 리콜했고, Aurora 무인 트럭 대부분에는 제조사 요구로 관찰자가 탄다. "
     "한국은 로봇 밀도가 근로자 1만 명당 1,220대로 세계 1위지만 설치는 3만 대 안팎에서 줄었고, 로보택시는 11월 상암에서 안전관리자가 조수석에 탄 채 시작한다. 국토교통부는 시범운행지구 지정 권한 이양과 무인 차량 안전 지침을 추진 중이다.",
     ["I6-M-014", "I6-M-018", "I6-M-001", "I6-M-003", "I6-M-015", "I6-E-008", "I6-I-006", "I6-I-007"]),
]
narrative_html = "".join(para(t, ids) for t, ids in NARRATIVE)
DIR = {"강화": "up", "약화": "down", "중립": "flat"}
irows = "".join(f"""<tr id="{E(r['id'])}"><td><span class="dir {DIR[r['direction']]}">{E(r['direction'])}</span></td>
  <td class="tgt">{E(r['target'])}</td><td>{E(r['statement'])}</td><td>{tags(r['basis'])}</td><td class="idc"><code>{E(r['id'])}</code></td></tr>"""
  for r in recs if r["type"] == "해석")

# 3. 주요 사건 (최신순) ------------------------------------------------
EVENTS_LEAD = ("2025년 말에는 Amazon 자동화 문서 보도, Figure 02 퇴역, Waymo 리콜이 이어졌다. 2026년에는 로보택시 확장(Waymo 라스베이거스 무인, Baidu 28개 도시, Pony.ai 2천 대 근접)과 로봇 통계 발표(IFR 500만 대)가 중심이었고, "
               "한국은 국토교통부 제도 정비와 서울시 11월 로보택시 계획이 나왔다.")
events = sorted([r for r in recs if r["type"] == "사건" and r.get("verified")], key=lambda r: r["date"], reverse=True)
erows = "".join(f"""<li id="{E(r['id'])}"><time>{E(r['date'])}</time><div><b>{E(r['actor'])}</b> {E(r['statement'])}
  <div class="src">{src_links(r)} <code>{E(r['id'])}</code></div></div></li>""" for r in events)

# 4. 전망 --------------------------------------------------------------
FORECAST_LEAD = ("2027년 말을 기준으로 두 시나리오를 세웠다. 갈림길은 로보택시가 소수 사업자 밖으로 넓어지는지, 휴머노이드가 시범을 넘어 공정에 정규 투입되는지다.")
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

# 5. 판정: 영역별 상용화 단계 ------------------------------------------
SG = ["시연", "시범 운영", "제한 상용", "대규모 상용"]
SG_DEF = {
    "시연": ("공개 시연·발표만 있다", "기업 발표, 시연"),
    "시범 운영": ("제한된 구역·현장에서 운영, 무료이거나 안전요원·관찰자가 탄다", "운영 발표, 규제기관 허가"),
    "제한 상용": ("일부 도시·공장·매장에서 유료 또는 실제 생산·배송", "사업자 운영 수치, 공시"),
    "대규모 상용": ("여러 지역에서 사람 없이 일상 운영하고 운영 규모가 공개된다", "공시·규제기관 기록의 운영 규모"),
}
STAGE_LEAD = ("영역 여섯 개를 글로벌과 한국으로 나눠 판정했다. 대규모 상용은 로보택시 하나이고, 제조 무인화는 '완전 무인'의 정의와 검증이 부족해 잠정이다. 한국은 로보택시와 배송 로봇이 시범 단계이고, 공장 무인화는 판단할 자료가 없다.")
STAGES = [
    ("로보택시", "대규모 상용", False, "시범 운영", False, "Waymo 약 3,500대·주 50만 건, Baidu 28개 도시 / 서울 상암 11월 시작, 안전관리자 탑승", ["I6-M-010", "I6-M-011", "I6-M-015"]),
    ("제조 무인화", "제한 상용", True, None, False, "로봇 설치 60만 대, 샤오미 자동화율 81%(회사 발표). 완전 무인 라인 검증 사례 부족 / 한국은 로봇 밀도 1위지만 무인 라인 자료 없음", ["I6-M-002", "I6-M-007", "I6-M-001"]),
    ("물류 자동화", "제한 상용", False, None, False, "Amazon 로봇 100만 대, 운영 75% 자동화 목표(내부 문서)", ["I6-M-017"]),
    ("드론·배송 로봇", "제한 상용", False, "시범 운영", True, "Walmart 드론 배송 누적 100만 건·66개 매장 / 한국 실외이동로봇은 운행안전인증 의무, 운영 규모 미확인", ["I6-M-016", "I6-E-009"]),
    ("무인 화물 트럭", "제한 상용", False, None, False, "Aurora 30대 중 10대 무인, 무인 25만 마일. 대부분 관찰자 탑승", ["I6-M-018"]),
    ("휴머노이드", "시범 운영", False, "시연", False, "출하 1만 8천 대(연구·오락 중심), Figure 02 BMW 11개월 / 현대차 아틀라스 2028년 안전 검증", ["I6-M-008", "I6-E-003", "I6-E-013"]),
]
def tip_sg(v):
    th, ev = SG_DEF[v]
    return f"{v} — 기준: {th}. 근거: {ev}."
def cell(v, pv):
    if v is None:
        return '<span class="pips"><span class="lv muted">자료 없음</span></span>'
    return gauge(SG, v, tip_sg(v), pv)
criteria_html = criteria_panel([
    ("판정 단계: 영역별 상용화", ["단계", "기준", "인정하는 근거"], [[gauge(SG, k), E(v[0]), E(v[1])] for k, v in SG_DEF.items()]),
], rules=[
    "'무인'은 차·라인·현장 안에 사람이 없는 운영만 인정한다. 원격 감독은 허용하되 그 점을 병기한다.",
    "로봇 대수·자동화율만으로는 제조 무인화를 대규모 상용으로 올리지 않는다.",
    "사업자가 밝힌 운행 대수·횟수는 자사 집계로 표시한다.",
    "기준을 직접 재는 수치가 없어 간접 근거로 판정한 칸은 '잠정'이며, 게이지의 점선 테두리와 빗금으로 표시한다.",
])
stage_rows = "".join(f"""<div class="rung"><div class="stage"><b>{E(d)}</b></div>
  <div class="lvcell"><span class="region">글로벌</span>{cell(g, gp)}</div>
  <div class="lvcell"><span class="region">한국</span>{cell(k, kp)}</div>
  <p class="why">{E(w)} {tags(ids)}</p></div>""" for d, g, gp, k, kp, w, ids in STAGES)
NEW_LEAD = ("이번 달 확산에 영향을 준 요인을 크기 순으로 놓았다. 순위는 영향 범위(여러 영역인지 한 영역인지)와 이미 운영 중단·지연으로 나타났는지를 기준으로 매겼다.")
FCLS = {"제약": "agent", "촉진": "brand", "중립": "contest"}
FACTORS = [
    (1, "제약", "안전 검증·사람 감독 요구", "Waymo 스쿨버스 사례 리콜, 한국 로보택시 안전관리자 탑승, Aurora 트럭 관찰자 탑승.", ["I6-M-014", "I6-M-015", "I6-M-018"]),
    (2, "촉진", "중국의 설비 확산", "로봇 설치의 59%, 선진급 스마트공장 7천 곳, 휴머노이드 출하 주도.", ["I6-M-002", "I6-M-006", "I6-M-009"]),
    (3, "촉진", "선두 사업자의 도시 확장", "Waymo 라스베이거스 무인 개시와 3개 도시 추가 발표, Baidu 28개 도시.", ["I6-E-012", "I6-M-011"]),
    (4, "제약", "기술·운영 성숙도", "Tesla 무감독 차량 4~8대, 휴머노이드 공장 투입은 단일 공정 시범.", ["I6-M-013", "I6-E-003"]),
    (5, "중립", "제도 정비(한국)", "시범운행지구 지정 권한 이양, 무인 차량 안전 지침·운전석 없는 차량 특례 추진.", ["I6-E-008", "I6-M-015"]),
]
new_rows = "".join(f"""<tr><td class="num">{n}</td><td><span class="own {FCLS[k]}">{E(k)}</span></td><td class="tgt">{E(f)}</td><td>{E(w)} {tags(ids)}</td></tr>""" for n, k, f, w, ids in FACTORS)

# 6. 핵심 지표 ---------------------------------------------------------
INDICATOR_NAMES = {"I6-T1": "국가별 로봇 밀도", "I6-T2": "산업용 로봇 설치", "I6-T3": "무인·등대 공장·물류 사례",
                   "I6-T4": "휴머노이드 출하·투입", "I6-T5": "로보택시 운행 규모", "I6-T6": "자율주행 사고·리콜",
                   "I6-T7": "한국 자율주행 제도", "I6-T8": "배송·무인 화물 상용 운영"}
metrics = sorted([r for r in recs if r["type"] == "지표"], key=lambda r: (r["indicator"], -r["importance"]))
filled = {r["indicator"] for r in metrics if r.get("verified")}
METRICS_LEAD = (f"추적 지표 8개 중 {len(filled)}개의 값을 확인했다. 로보택시·드론 배송·물류 로봇 수치는 사업자 발표(자사 집계)이고, 휴머노이드 출하는 조사사마다 정의가 달라 표시를 달았다.")
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

page = f"""<title>I6 무인화 R1</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans+KR:wght@400;500;600&family=Noto+Serif+KR:wght@600;800&display=swap">
<style>{CSS}</style>
<main>
  <header class="narrow">
    <div class="eyebrow"><span>AI Industry Trend · 산업 내 AI 자동화</span><span>I6 · Autonomous Operations</span><span>R1 기준 회차 · 2026-10-29</span><span><a href="../../changes.html#I6">변경 이력</a></span></div>
    <h1>{E(TITLE)}</h1>
    <p class="question">고정 질문 v1.0 — {E(QUESTION)}</p>
  </header>
  <section class="answer-box"><h2>한 줄 답</h2>
    <p class="answer narrow">{E(ONE_LINE)} {tags(ONE_LINE_BASIS)}</p><dl class="arows">{answer_rows}</dl></section>
  <section><h2>해석</h2><div class="narrative">{narrative_html}</div>
    <div class="tablewrap"><table><thead><tr><th>방향</th><th>대상</th><th>해석</th><th>근거</th><th>기록</th></tr></thead><tbody>{irows}</tbody></table></div></section>
  <section><h2>주요 사건 <small>최신순 · 원문 확인된 것만</small></h2><p class="lead">{E(EVENTS_LEAD)}</p><ul class="timeline">{erows}</ul></section>
  <section><h2>전망 <small>2027년 말까지, 무인화는 소수 사업자 밖으로 넓어질까</small></h2><p class="lead">{E(FORECAST_LEAD)}</p>
    <div class="scens">{scen_html}</div>
    <h3 class="subhead">세부 판정 근거</h3>
    <p class="lead muted">각 세부 전망이 적중하거나 빗나갔을 때 어느 시나리오 쪽 신호인지 표시했다. 확인 시점이 오면 확인 방법대로 판정한다.</p>
    <div class="tablewrap"><table><thead><tr><th>세부 전망</th><th>확인 시점</th><th>적중 시</th><th>빗나갈 시</th><th>상태</th><th>근거</th></tr></thead><tbody>{frows}</tbody></table></div></section>
  <section><h2>영역별 상용화 단계 <small>생산·물류·이동</small></h2><p class="lead">{E(STAGE_LEAD)}</p>
    {criteria_html}
    <div class="ladder mapgrid auto">{stage_rows}</div>
    <h3 class="subhead">확산을 밀고 막는 요인 순위</h3><p class="lead">{E(NEW_LEAD)}</p>
    <div class="tablewrap"><table><thead><tr><th style="white-space:nowrap">순위</th><th>방향</th><th>요인</th><th>근거</th></tr></thead><tbody>{new_rows}</tbody></table></div></section>
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
order = [page.index(f"<h2>{h}") for h in ("한 줄 답", "해석", "주요 사건", "전망", "영역별 상용화 단계", "핵심 지표", "다른 질문에서 인용한 기록", "미확인·경고")]
print("article_r1.html 생성,", len(page), "bytes; 앵커 없는 근거 링크:", bad or "없음", "; 섹션 순서 정상:", order == sorted(order))
# ---------- 포털 신호
signal = {"question": Q, "round": 1, "chip": "대규모 상용은 로보택시뿐", "gauge": "영역 6개 중 제한 상용 이상(글로벌)",
          "frontier": "로보택시", "on": sum(1 for r in STAGES if r[1] in ("제한 상용", "대규모 상용")), "of": len(STAGES),
          "kind": "band", "levels": list(SG), "items": [[r[0], SG.index(r[1]), bool(r[2])] for r in STAGES if r[1] is not None]}
(ROOT / "signal_r1.json").write_text(json.dumps(signal, ensure_ascii=False, indent=1), encoding="utf-8")
print("signal_r1.json:", signal["chip"], f'{signal["on"]}/{signal["of"]}')
sys.exit(1 if bad or order != sorted(order) else 0)

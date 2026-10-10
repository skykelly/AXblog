"""records.jsonl → 기준 아티클 HTML (S3 R1).
순서: 한 줄 답 → 해석 → 주요 사건 → 전망 → 기능별 변화 단계와 성과 근거 → 핵심 지표 → 미확인·경고
"""
import json, html, re, sys
from pathlib import Path

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT.parent.parent / "lib"))
from judge import gauge, chip, criteria_panel
recs = [json.loads(l) for l in (ROOT / "records.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
by = {r["id"]: r for r in recs}
E = html.escape
CSS = (ROOT.parent.parent / "lib" / "article.css").read_text(encoding="utf-8")

def tags(ids):
    return "".join(f'<a class="rid" href="#{E(i)}" title="{E(by[i]["statement"])}">{E(i)}</a>' for i in ids)
def para(text, ids): return f"<p>{E(text)} {tags(ids)}</p>"
def src_links(r):
    return " · ".join(f'<a href="{E(s["url"])}" target="_blank" rel="noopener">{E(s["publisher"])}</a><span class="grade g{E(s["grade"])}">{E(s["grade"])}</span>' for s in r.get("sources", []))

TITLE = "AI는 마케팅을 어디까지 바꿨고, 무엇이 매출로 이어졌나"
QUESTION = "AI는 고객 이해·타기팅·콘텐츠·광고·CRM의 일하는 방식을 어디까지 바꿨으며, 그중 어떤 방식이 실제 매출과 고객 가치 증가로 이어지고 있는가?"

# 1. 한 줄 답 ----------------------------------------------------------
ONE_LINE = ("2026년 10월 현재 AI가 일하는 방식을 가장 깊이 바꾼 곳은 광고 집행과 타기팅이다. 플랫폼 AI가 스스로 운영하는 단계(Meta Advantage+ 연환산 750억 달러)에 들어섰다. 콘텐츠는 AI가 만들고 사람이 고르는 방식이 표준이 됐고(마케터 74% 사용), 고객 이해와 CRM은 아직 보조~생성 단계다. "
            "매출 효과는 광고 AI에서 가장 많이 측정됐지만 결과가 엇갈린다. 플랫폼은 전환 15% 증가를 말하지만, 독립 실험에서는 전환당 비용이 16% 오르거나 증분 수익률이 수동 캠페인보다 12% 낮았다.")
ONE_LINE_BASIS = ["S3-I-001", "S3-I-002", "S3-I-003", "S3-I-004"]
ANSWER_ROWS = [
    ("AI 운영", "광고 집행·타기팅. Advantage+ 연환산 750억 달러, AI Max 광고주 50만 곳. 마케터는 목표와 예산만 정한다.", ["S3-M-004", "S3-M-005"]),
    ("AI 생성", "콘텐츠. 마케터 74%가 콘텐츠 제작에 AI를 쓰고, AI 광고는 사람 제작 광고만큼 클릭된다. 개인화(65%)도 생성 단계.", ["S3-M-001", "S3-M-009"]),
    ("AI 보조", "고객 이해. 고객 예측 분석 42%, 세분화 36%로 가장 덜 쓰인다.", ["S3-M-001"]),
    ("매출로 이어진 근거", "광고 AI는 증분 실험이 있지만 엇갈림(플랫폼 +15% 전환 vs 독립 분석 전환당 비용 +16%, 홀드아웃 실험 증분 수익률 -12%). CRM 개인화는 벤더 의뢰 사례(갱신율 70%→84%), 콘텐츠는 클릭까지만 검증.", ["S3-M-005", "S3-M-006", "S3-M-007", "S3-M-008", "S3-M-009"]),
    ("한국", "네이버 광고 성장의 60% 이상이 AI 최적화·타기팅 덕, AI 브리핑 광고 구매 전환율 검색 광고의 3배(회사 발표).", ["S3-M-010"]),
]
answer_rows = "".join(f'<div class="arow"><dt>{E(k)}</dt><dd>{E(v)} {tags(ids)}</dd></div>' for k, v, ids in ANSWER_ROWS)

# 2. 해석 --------------------------------------------------------------
NARRATIVE = [
    ("AI는 마케팅 전체보다 몇몇 업무를 깊게 바꿨다. 미국 기업 마케팅 활동 중 AI 비중은 2026년 24.2%로 2년 새 두 배 가까이 됐다. 하지만 용도는 콘텐츠 제작(73.9%)과 개인화(65.4%)에 몰려 있고, 고객 예측 분석(41.5%)과 세분화(35.6%)는 상대적으로 덜 쓰인다.",
     ["S3-M-001", "S3-I-002"]),
    ("가장 깊이 바뀐 곳은 광고 집행과 타기팅이다. Meta의 AI 광고 묶음 Advantage+는 연환산 매출 750억 달러에 이르렀고, 구글 AI Max는 베타를 마치고 광고주 50만 곳이 쓴다. 입찰·지면·대상 선정을 플랫폼 AI가 운영하고, 마케터는 목표와 예산을 정하는 쪽으로 물러났다. "
     "네이버도 광고 성장의 60% 이상을 AI 최적화·타기팅 덕으로 돌렸다.",
     ["S3-M-004", "S3-M-005", "S3-E-004", "S3-E-005", "S3-M-010", "S3-I-001", "S3-I-008"]),
    ("그러나 광고 AI가 매출을 '더' 만드는지는 엇갈린다. 구글은 AI Max와 Performance Max를 함께 쓴 캠페인이 비슷한 수익률에서 전환을 15% 더 냈다고 밝혔다. 반면 리테일 캠페인 250여 개를 본 독립 분석에서는 매출이 13% 늘었지만 전환당 비용이 16% 올랐다. "
     "Meta 광고 증분 실험 640건에서는 자동 캠페인의 증분 수익률이 수동보다 12% 낮았고, 브랜드의 58%가 수동 쪽이 나았다. AI 자동화는 양을 늘리지만 효율은 보장하지 않으며, 플랫폼 보고와 독립 실험이 다르게 나오는 만큼 측정 주도권이 핵심이 된다.",
     ["S3-M-005", "S3-M-006", "S3-M-007", "S3-I-003", "S3-I-007"]),
    ("콘텐츠와 CRM은 근거의 수준이 다르다. 실제 광고 수십만 건을 비교한 연구에서 AI 생성 광고는 사람 제작 광고만큼 클릭됐고, AI 티가 나지 않을 때 가장 잘 됐다. 다만 매출 효과는 측정되지 않았다. "
     "CRM의 1:1 개인화 AI는 구독 갱신율 70%→84% 같은 큰 효과를 보고하지만, 벤더가 의뢰한 사례 연구다.",
     ["S3-M-009", "S3-M-008", "S3-I-004", "S3-I-005"]),
    ("마케터가 체감하는 성과는 커졌지만 돈은 늘지 않았다. AI로 인한 매출 생산성 개선은 1년 새 8.6%에서 14.1%로 커졌고 간접비는 14.6% 줄었다. 그러나 마케팅 예산은 매출의 7.8%로 그대로이고, AI 예산(15.3%)은 기존 예산 안에서 옮겨진 것이다. AI를 키울 준비가 된 조직은 30%뿐이다.",
     ["S3-M-002", "S3-M-003", "S3-E-002", "S3-I-006"]),
]
narrative_html = "".join(para(t, ids) for t, ids in NARRATIVE)
DIR = {"강화": "up", "약화": "down", "중립": "flat"}
irows = "".join(f"""<tr id="{E(r['id'])}"><td><span class="dir {DIR[r['direction']]}">{E(r['direction'])}</span></td>
  <td class="tgt">{E(r['target'])}</td><td>{E(r['statement'])}</td><td>{tags(r['basis'])}</td><td class="idc"><code>{E(r['id'])}</code></td></tr>"""
  for r in recs if r["type"] == "해석")

# 3. 주요 사건 (최신순) ------------------------------------------------
EVENTS_LEAD = ("여름 실적 시즌에 광고 플랫폼의 AI 규모가 드러났다. Meta Advantage+ 연환산 750억 달러, 구글 AI Max 광고주 50만 곳, 네이버 AI 브리핑 광고 정식 출시가 7월에 몰렸다. "
               "그 앞에는 AI 광고 크리에이티브를 검증한 학술 연구(1월)와, 예산 정체 속 AI 성과 압박을 짚은 Gartner 조사(5월)가 있다.")
events = sorted([r for r in recs if r["type"] == "사건" and r.get("verified")], key=lambda r: r["date"], reverse=True)
erows = "".join(f"""<li id="{E(r['id'])}"><time>{E(r['date'])}</time><div><b>{E(r['actor'])}</b> {E(r['statement'])}
  <div class="src">{src_links(r)} <code>{E(r['id'])}</code></div></div></li>""" for r in events)

# 4. 전망 --------------------------------------------------------------
FORECAST_LEAD = ("2027년 말을 기준으로 두 시나리오를 세웠다. 갈림길은 AI가 광고 밖(CRM·콘텐츠·고객 이해)까지 '운영' 단계로 들어가고 매출 효과가 마케터 조사에서도 뚜렷해지는지, "
                 "아니면 플랫폼 안 자동화와 제작 비용 절감에 머무는지다. 핵심 판정 자료는 2027년 봄의 CMO Survey와 Gartner 예산 조사다.")
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

# 5. 기능별 변화 단계와 성과 근거 -----------------------------------
SG = ["AI 보조", "AI 생성", "AI 운영", "자율 운영"]
SG_DEF = {
    "AI 보조": "사람이 하고, AI는 분석·초안을 돕는다.",
    "AI 생성": "AI가 결과물(소재·세그먼트·문구)을 만들고, 사람이 골라 집행한다.",
    "AI 운영": "AI가 집행·최적화를 돌리고, 사람은 목표·예산·가드레일만 정한다.",
    "자율 운영": "AI가 목표·예산 배분까지 정해 실행하고, 사람은 사후에 점검한다. 과반이면서 사람 운영 업무가 줄어든 것이 확인돼야 한다.",
}
EV_DEF = {
    "업체 주장": "벤더·플랫폼의 발표",
    "기업 사례": "광고주·기업이 밝힌 결과 (벤더가 의뢰한 연구 포함)",
    "증분 검증": "홀드아웃·지역 실험 같은 통제 실험, 또는 독립 분석. 결과 방향(긍정·엇갈림·부정)이나 범위를 괄호로 함께 적는다",
}
FUNC_LEAD = ("타기팅과 광고 집행은 AI 운영 단계로, Meta 광고 매출의 약 3분의 1(연환산 기준)이 AI 자동 캠페인에서 나온다. 콘텐츠와 CRM은 AI 생성, 고객 이해는 AI 보조 단계다. "
             "목표와 예산까지 AI가 정하는 자율 운영에 이른 기능은 없다.")
EV = {"업체 주장": "contest", "기업 사례": "platform", "증분 검증 (엇갈림)": "agent", "증분 검증 (클릭 한정)": "agent", "증분 검증": "brand"}
# (기능, 변화 단계, 잠정, 성과 근거, 근거, 기록)
FUNCS = [
    ("고객 이해", "AI 보조", True, "업체 주장", "AI 사용처 중 고객 예측 분석 41.5%, 세분화로 가장 덜 쓰임. 합성 응답자 같은 방식은 정확도 근거가 공개되지 않음", ["S3-M-001"]),
    ("타기팅", "AI 운영", False, "증분 검증 (엇갈림)", "Advantage+ 연환산 750억 달러(Meta 광고 매출의 약 3분의 1), 네이버 광고 성장의 60% 이상. 홀드아웃 실험에서 자동 캠페인 증분 수익률은 수동보다 -12%", ["S3-M-004", "S3-M-010", "S3-M-007"]),
    ("광고 집행·입찰", "AI 운영", False, "증분 검증 (엇갈림)", "AI Max 광고주 50만 곳. 플랫폼 보고 전환 +15%(같은 수익률) vs 독립 분석 매출 +13%·전환당 비용 +16%", ["S3-M-005", "S3-M-006", "S3-M-004"]),
    ("콘텐츠", "AI 생성", True, "증분 검증 (클릭 한정)", "AI를 쓰는 마케터의 73.9%가 콘텐츠 제작에 사용(사용 여부), Meta AI 도구 소상공인 900만 곳. AI 광고 클릭률은 사람 제작과 비슷하거나 약간 높음, 매출 미측정", ["S3-M-001", "S3-M-004", "S3-M-009"]),
    ("CRM·개인화", "AI 생성", True, "기업 사례", "AI 사용처 중 개인화 65.4%, 자동화 48.9%(사용 여부). 1:1 의사결정 AI로 갱신율 70%→84%(벤더 의뢰 연구)", ["S3-M-001", "S3-M-008"]),
]
def tip_sg(v):
    return f"{v} — {SG_DEF[v]}"
def tip_ev(v):
    base = v.split(" (")[0]
    return f"{v} — {EV_DEF[base]}"
criteria_html = criteria_panel([
    ("축 1. AI가 일하는 방식", ["단계", "정의"], [[gauge(SG, k), E(v)] for k, v in SG_DEF.items()]),
    ("축 2. 성과 근거", ["판정", "정의"], [[f'<span class="own {EV[k]}">{E(k)}</span>', E(v)] for k, v in EV_DEF.items()]),
], extra_rules=["변화 단계는 그 기능 업무의 25% 이상이 해당 방식으로 돌아가는 최고 단계로 정한다.",
                "'마케터의 N%가 AI를 쓴다' 같은 사용 여부 수치만 있으면 잠정으로 둔다."])
func_rows = "".join(f"""<div class="rung"><div class="stage"><b>{E(f)}</b></div>
  <div class="lvcell"><span class="region">변화 단계</span>{gauge(SG, st, tip_sg(st), pv)}</div>
  <div class="lvcell"><span class="region">성과 근거</span><span class="own {EV[ev]}" tabindex="0" data-tip="{E(tip_ev(ev))}">{E(ev)}</span></div>
  <p class="why">{E(w)} {tags(ids)}</p></div>""" for f, st, pv, ev, w, ids in FUNCS)
FUNC_NOTE = "판정: 변화가 깊을수록(광고·타기팅) 증분 검증도 많지만 결과가 엇갈리고, 변화가 얕은 곳(고객 이해·CRM)은 아직 업체 주장과 사례에 머문다."

# 6. 핵심 지표 ---------------------------------------------------------
INDICATOR_NAMES = {"S3-T1": "마케팅 AI 활용 비중", "S3-T2": "AI 성과 체감", "S3-T3": "마케팅 예산 중 AI",
                   "S3-T4": "AI 광고 운영 규모", "S3-T5": "플랫폼 보고 성과", "S3-T6": "독립·사례 증분 성과",
                   "S3-T7": "AI 콘텐츠 성과", "S3-T8": "한국 AI 마케팅"}
metrics = sorted([r for r in recs if r["type"] == "지표"], key=lambda r: (r["indicator"], -r["importance"]))
filled = {r["indicator"] for r in metrics if r.get("verified")}
empty_ind = [f"{k} {v}" for k, v in INDICATOR_NAMES.items() if k not in filled]
METRICS_LEAD = (f"추적 지표 8개 중 {len(filled)}개의 값을 원문으로 확인했다. "
                "플랫폼 자체 보고 성과는 '업체 주장', 벤더 의뢰 연구는 '기업 사례'로만 인정했고, 마케터 설문의 성과는 자기 평가라 주의 표시를 달았다.")
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

page = f"""<title>S3 AI 마케팅 R1</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans+KR:wght@400;500;600&family=Noto+Serif+KR:wght@600;800&display=swap">
<style>{CSS}</style>
<main>
  <header class="narrow">
    <div class="eyebrow"><span>AI Sales &amp; Marketing</span><span>S3 · AI Marketing</span><span>R1 기준 회차 · 2026-10-09</span></div>
    <h1>{E(TITLE)}</h1>
    <p class="question">고정 질문 v1.0 — {E(QUESTION)}</p>
  </header>
  <section class="answer-box"><h2>한 줄 답</h2>
    <p class="answer narrow">{E(ONE_LINE)} {tags(ONE_LINE_BASIS)}</p><dl class="arows">{answer_rows}</dl></section>
  <section><h2>해석</h2><div class="narrative">{narrative_html}</div>
    <div class="tablewrap"><table><thead><tr><th>방향</th><th>대상</th><th>해석</th><th>근거</th><th>기록</th></tr></thead><tbody>{irows}</tbody></table></div></section>
  <section><h2>주요 사건 <small>최신순 · 원문 확인된 것만</small></h2><p class="lead">{E(EVENTS_LEAD)}</p><ul class="timeline">{erows}</ul></section>
  <section><h2>전망 <small>2027년 말까지, AI는 광고 밖까지 운영할까</small></h2><p class="lead">{E(FORECAST_LEAD)}</p>
    <div class="scens">{scen_html}</div>
    <h3 class="subhead">세부 판정 근거</h3>
    <p class="lead muted">각 세부 전망이 적중하거나 빗나갔을 때 어느 시나리오 쪽 신호인지 표시했다. 확인 시점이 오면 확인 방법대로 판정한다.</p>
    <div class="tablewrap"><table><thead><tr><th>세부 전망</th><th>확인 시점</th><th>적중 시</th><th>빗나갈 시</th><th>상태</th><th>근거</th></tr></thead><tbody>{frows}</tbody></table></div></section>
  <section><h2>기능별 변화 단계와 성과 근거 <small>마케팅 기능 다섯 개</small></h2><p class="lead">{E(FUNC_LEAD)}</p>
    {criteria_html}
    <div class="ladder mapgrid auto">{func_rows}</div><p class="gapnote">{E(FUNC_NOTE)}</p></section>
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
anchors = set(re.findall(r'id="(S3-[A-Z]-\d{3})"', page))
bad = sorted({i for i in re.findall(r'href="#(S3-[A-Z]-\d{3})"', page) if i not in anchors})
order = [page.index(f"<h2>{h}") for h in ("한 줄 답", "해석", "주요 사건", "전망", "기능별 변화 단계와 성과 근거", "핵심 지표")]
print("article_r1.html 생성,", len(page), "bytes; 앵커 없는 근거 링크:", bad or "없음", "; 섹션 순서 정상:", order == sorted(order))
# ---------- 포털 신호: 판정 칩과 게이지를 판정 데이터에서 계산해 내보낸다
SIGNAL_CHIP = '깊은 변화일수록 성과 엇갈림'
SIGNAL_GAUGE = '마케팅 기능 5개 중 AI 운영 이상'
SIGNAL_FRONTIER = '콘텐츠·CRM'
signal = {"question": 'S3', "round": 1, "chip": SIGNAL_CHIP, "gauge": SIGNAL_GAUGE, "frontier": SIGNAL_FRONTIER,
          "on": sum(1 for r in FUNCS if SG.index(r[1]) >= SG.index("AI 운영")), "of": len(FUNCS)}
(ROOT / "signal_r1.json").write_text(json.dumps(signal, ensure_ascii=False, indent=1), encoding="utf-8")
print("signal_r1.json:", signal["chip"], f'{signal["on"]}/{signal["of"]}')
sys.exit(1 if bad or order != sorted(order) else 0)

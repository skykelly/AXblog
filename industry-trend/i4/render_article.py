"""records.jsonl → 기준 아티클 HTML (I4 R1).
순서: 한 줄 답 → 해석 → 주요 사건 → 전망 → 확산 단계와 요인 순위 → 핵심 지표 → 미확인·경고
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

TITLE = "AI는 어느 산업까지 들어갔고, 무엇이 밀고 막나"
QUESTION = "AI는 어느 산업·업무까지 실제 운영에 들어갔고, 확산을 가장 크게 밀거나 막는 요인은 무엇인가?"

# 1. 한 줄 답 ----------------------------------------------------------
ONE_LINE = ("2026년 10월 현재 AI가 실제 운영에 들어선 곳은 정보·금융 산업(미국 기업 사용률 34~40%)과 IT·소프트웨어 개발 업무다. 소매·제조는 아직 초기 확산(14~24%)이고, 미국 기업 전체 사용률은 반년째 20% 안팎에 멈췄다. "
            "확산을 가장 크게 막는 것은 규제가 아니라 전력(올해 데이터센터 계획의 30~50% 지연)이고, 가장 크게 미는 것은 규제 완화(EU 고위험 의무 연기, 미국 학습 공정 이용 지지)와 대기업의 전사 확장(44%)이다.")
ONE_LINE_BASIS = ["I4-I-001", "I4-I-002", "I4-I-003", "I4-I-005"]
ANSWER_ROWS = [
    ("운영 단계", "정보 산업 39.7%, 금융·보험 33.9%. 업무로는 IT·지식관리·소프트웨어 개발에서 Agent 확장이 가장 많다.", ["I4-M-002", "I4-M-004"]),
    ("초기 확산", "소매 약 14%, 제조(한국 23.8%). 미국 기업 전체 19.8%로 반년째 17~20%에 머무른다.", ["I4-M-001", "I4-M-002", "I4-M-009"]),
    ("가장 큰 제약", "전력·데이터센터 건설. 올해 완공 예정 용량의 30~50%가 지연·취소. 다음은 Agent 보안(간접 프롬프트 주입이 실제 공격 단계)과 성과 증명(EBIT 효과 37%로 정체).", ["I4-M-005", "I4-M-007", "I4-M-004"]),
    ("가장 큰 촉진", "규제 완화와 대기업 확장. EU 고위험 의무 2027년 12월로 연기, 미국 법무부의 학습 공정 이용 지지, 대기업 40%가 Agent 확장.", ["I4-E-007", "I4-E-010", "I4-M-004"]),
    ("한국", "국민 AI 사용률 30% 이상(세계 18위, 증가율 80%), AI 기본법 시행, 정부 GPU 1만 3천 장. 기업 도입 공식 통계는 2024년(30.6%) 이후 갱신되지 않았다.", ["I4-M-008", "I4-E-004", "I4-M-010", "I4-M-009"]),
]
answer_rows = "".join(f'<div class="arow"><dt>{E(k)}</dt><dd>{E(v)} {tags(ids)}</dd></div>' for k, v, ids in ANSWER_ROWS)

# 2. 해석 --------------------------------------------------------------
NARRATIVE = [
    ("AI 확산은 넓이보다 깊이로 진행되고 있다. 미국 인구조사국 조사에서 AI를 쓰는 기업은 2026년 5월 19.8%로, 2025년 12월부터 17~20%에 머물렀다. "
     "그러나 직원 250명 이상 기업은 37%가 쓰고, McKinsey 조사에서는 AI를 전사로 확장하는 기업이 44%(1년 전 38%), Agent를 확장하는 대기업이 40%였다. 쓰는 기업은 더 깊이 쓰고, 안 쓰는 작은 기업은 그대로다.",
     ["I4-M-001", "I4-M-003", "I4-M-004", "I4-I-001"]),
    ("산업으로 보면 정보(39.7%)와 금융·보험(33.9%)이 확산 단계에 들어섰고, 소매(약 14%)가 가장 낮다. 업무로는 IT·지식관리·소프트웨어 개발에서 Agent가 가장 많이 확장됐다. "
     "한국도 2024년 조사에서 서비스업(53.0%, 금융 57.1%)과 제조업(23.8%)의 격차가 컸다.",
     ["I4-M-002", "I4-M-004", "I4-M-009", "I4-I-002"]),
    ("규제는 확산을 미는 쪽으로 움직였다. EU는 고위험 AI 의무를 2026년 8월에서 2027년 12월로 미뤘고, 미국은 대통령 행정명령으로 주 법을 압박해 콜로라도가 AI법을 크게 줄였다. "
     "저작권은 '막는 요인'에서 '비용'으로 바뀌는 중이다. Anthropic 합의로 저작물당 약 3,100달러라는 가격이 매겨졌고, 법무부는 학습 단계의 공정 이용을 지지했다.",
     ["I4-E-007", "I4-E-002", "I4-E-005", "I4-M-006", "I4-E-010", "I4-I-003", "I4-I-004"]),
    ("가장 큰 제약은 물리적이다. 올해 완공 예정이던 미국 데이터센터의 30~50%가 늦어지거나 취소됐고, 병목은 GPU보다 전력망 연결이다. "
     "Agent 보안도 새 제약이다. 웹 페이지에 숨긴 지시로 에이전트를 조종하는 공격이 실제로 쓰이지만, 1~4월 주요 사고 8건 중 CVE가 붙은 것은 1건뿐이다.",
     ["I4-M-005", "I4-M-007", "I4-I-005", "I4-I-006"]),
    ("미국과 중국 시장은 갈라지고 있다. 미국이 수익의 25%를 받는 조건으로 H200 판매를 허용했지만 중국이 수입을 억제해, NVIDIA는 중국 매출을 전망에서 뺐다. "
     "한국은 국민 사용률이 30%를 넘어 빠르게 늘고, AI 기본법 시행과 정부 GPU 확보로 제도·인프라가 갖춰지고 있다. 다만 기업 운영 단계를 판정할 최신 통계가 없다.",
     ["I4-E-001", "I4-E-003", "I4-E-009", "I4-M-008", "I4-M-010", "I4-I-007", "I4-I-008"]),
]
narrative_html = "".join(para(t, ids) for t, ids in NARRATIVE)
DIR = {"강화": "up", "약화": "down", "중립": "flat"}
irows = "".join(f"""<tr id="{E(r['id'])}"><td><span class="dir {DIR[r['direction']]}">{E(r['direction'])}</span></td>
  <td class="tgt">{E(r['target'])}</td><td>{E(r['statement'])}</td><td>{tags(r['basis'])}</td><td class="idc"><code>{E(r['id'])}</code></td></tr>"""
  for r in recs if r["type"] == "해석")

# 3. 주요 사건 (최신순) ------------------------------------------------
EVENTS_LEAD = ("여름 이후 규제 쪽 사건이 확산을 미는 방향으로 이어졌다. EU가 고위험 의무를 미뤘고(7월), Anthropic 합의가 확정됐으며(7월), 미국 법무부가 학습의 공정 이용을 지지했다(9월). "
               "수출 통제는 반대로 미국·중국 시장을 갈랐고, 한국은 1월 AI 기본법 시행과 5월 행동계획 점검이 주요 사건이다.")
events = sorted([r for r in recs if r["type"] == "사건" and r.get("verified")], key=lambda r: r["date"], reverse=True)
erows = "".join(f"""<li id="{E(r['id'])}"><time>{E(r['date'])}</time><div><b>{E(r['actor'])}</b> {E(r['statement'])}
  <div class="src">{src_links(r)} <code>{E(r['id'])}</code></div></div></li>""" for r in events)

# 4. 전망 --------------------------------------------------------------
FORECAST_LEAD = ("2027년 말을 기준으로 두 시나리오를 세웠다. 갈림길은 AI가 정보·금융을 넘어 소매·제조로 넓어지는지, 그리고 전력 병목이 풀리는지다. "
                 "규제는 당분간 미는 쪽이라, 시나리오를 가르는 변수는 인프라와 기업 성과다.")
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

# 5. 확산 단계와 요인 순위 -----------------------------------------
SG = ["시험", "초기 확산", "확산", "주류"]
STAGE_LEAD = ("산업·업무마다 시험(사용률 10% 미만) → 초기 확산(10~25%) → 확산(25~50%) → 주류(50% 이상) 중 어디에 있는지 판정했다. "
              "글로벌은 미국 인구조사국 업종별 현재 사용률, 업무 기능은 McKinsey의 Agent 확장 보고를 기준으로 했다. 한국은 2024년 기업 조사라 참고값이다.")
STAGES = [
    ("정보·소프트웨어", "확산", None, "미국 39.7%, Agent는 소프트웨어 개발에서 가장 많이 확장", ["I4-M-002", "I4-M-004"]),
    ("금융·보험", "확산", "주류", "미국 33.9% / 한국 금융 57.1%(2024)", ["I4-M-002", "I4-M-009"]),
    ("서비스 전반", None, "주류", "한국 서비스업 53.0%(2024)", ["I4-M-009"]),
    ("제조", None, "초기 확산", "Agent는 공급망·재고 업무에서 시험 / 한국 23.8%(2024)", ["I4-M-004", "I4-M-009"]),
    ("소매", "초기 확산", None, "미국 약 14%로 업종 중 최저", ["I4-M-002"]),
    ("기업 전체", "초기 확산", "확산", "미국 19.8%(반년째 정체), 250명 이상 37% / 한국 30.6%(2024)", ["I4-M-001", "I4-M-003", "I4-M-009"]),
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
FACTOR_LEAD = ("이번 달 확산에 영향을 준 요인을 크기 순으로 놓았다. 순위는 영향 범위(산업 전체인지 일부인지)와 이미 수치로 나타났는지를 기준으로 매겼다.")
FCLS = {"제약": "agent", "촉진": "brand", "중립": "contest"}
FACTORS = [
    (1, "제약", "전력·데이터센터 건설", "올해 완공 예정 용량의 30~50% 지연·취소. 돈이 있어도 연산 능력이 제때 들어서지 못한다.", ["I4-M-005", "I4-I-005"]),
    (2, "촉진", "규제 완화·연기", "EU 고위험 의무 2027년 12월로 연기, 미국 연방의 주 법 압박과 콜로라도 축소.", ["I4-E-007", "I4-E-002", "I4-E-005"]),
    (3, "촉진", "대기업의 전사 확장", "전사 확장 44%(+6%p), 대기업 Agent 확장 40%.", ["I4-M-004", "I4-M-003"]),
    (4, "제약", "성과 증명", "EBIT 효과 37%로 1년째 정체, 소기업 사용률 변화 없음.", ["I4-M-004", "I4-M-003"]),
    (5, "제약", "Agent 보안", "간접 프롬프트 주입이 실제 공격 단계, 주요 사고 8건 중 CVE 1건.", ["I4-M-007"]),
    (6, "중립", "저작권", "합의로 비용이 정해지고(저작물당 약 3,100달러) 학습은 공정 이용 쪽으로 기울어 불확실성이 줄었다.", ["I4-M-006", "I4-E-010"]),
    (7, "중립", "수출 통제", "미국·중국 시장 분리. 중국 밖 확산에는 영향이 작다.", ["I4-E-009", "I4-E-003"]),
]
factor_rows = "".join(f"""<tr><td class="num">{n}</td><td><span class="own {FCLS[k]}">{E(k)}</span></td><td class="tgt">{E(f)}</td><td>{E(w)} {tags(ids)}</td></tr>""" for n, k, f, w, ids in FACTORS)

# 6. 핵심 지표 ---------------------------------------------------------
INDICATOR_NAMES = {"I4-T1": "기업 AI 사용률", "I4-T2": "산업별 사용률", "I4-T3": "기업 규모별 격차",
                   "I4-T4": "기업 확장·성과", "I4-T5": "인프라 병목", "I4-T6": "저작권 비용·판결",
                   "I4-T7": "Agent 보안 사고", "I4-T8": "한국 확산·정책"}
metrics = sorted([r for r in recs if r["type"] == "지표"], key=lambda r: (r["indicator"], -r["importance"]))
filled = {r["indicator"] for r in metrics if r.get("verified")}
empty_ind = [f"{k} {v}" for k, v in INDICATOR_NAMES.items() if k not in filled]
METRICS_LEAD = (f"추적 지표 8개 중 {len(filled)}개의 값을 원문으로 확인했다. "
                "데이터센터 지연 비율은 2차 정리 기사라 원자료 확인 표시를, 한국 기업 도입률은 2024년 조사라 갱신 필요 표시를 달았다.")
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

page = f"""<title>I4 AI 확산·정책 R1</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans+KR:wght@400;500;600&family=Noto+Serif+KR:wght@600;800&display=swap">
<style>{CSS}</style>
<main>
  <header class="narrow">
    <div class="eyebrow"><span>AI Industry Trend</span><span>I4 · AI Adoption, Governance &amp; Geopolitics</span><span>R1 기준 회차 · 2026-10-09</span></div>
    <h1>{E(TITLE)}</h1>
    <p class="question">고정 질문 v1.0 — {E(QUESTION)}</p>
  </header>
  <section class="answer-box"><h2>한 줄 답</h2>
    <p class="answer narrow">{E(ONE_LINE)} {tags(ONE_LINE_BASIS)}</p><dl class="arows">{answer_rows}</dl></section>
  <section><h2>해석</h2><div class="narrative">{narrative_html}</div>
    <div class="tablewrap"><table><thead><tr><th>방향</th><th>대상</th><th>해석</th><th>근거</th><th>기록</th></tr></thead><tbody>{irows}</tbody></table></div></section>
  <section><h2>주요 사건 <small>최신순 · 원문 확인된 것만</small></h2><p class="lead">{E(EVENTS_LEAD)}</p><ul class="timeline">{erows}</ul></section>
  <section><h2>전망 <small>2027년 말까지, AI는 소매·제조로 넓어질까</small></h2><p class="lead">{E(FORECAST_LEAD)}</p>
    <div class="scens">{scen_html}</div>
    <h3 class="subhead">세부 판정 근거</h3>
    <p class="lead muted">각 세부 전망이 적중하거나 빗나갔을 때 어느 시나리오 쪽 신호인지 표시했다. 확인 시점이 오면 확인 방법대로 판정한다.</p>
    <div class="tablewrap"><table><thead><tr><th>세부 전망</th><th>확인 시점</th><th>적중 시</th><th>빗나갈 시</th><th>상태</th><th>근거</th></tr></thead><tbody>{frows}</tbody></table></div></section>
  <section><h2>확산 단계와 요인 순위 <small>산업·업무별 · 촉진과 제약</small></h2><p class="lead">{E(STAGE_LEAD)}</p>
    <div class="ladder mapgrid auto">{stage_rows}</div>
    <h3 class="subhead">확산을 밀고 막는 요인 순위</h3><p class="lead">{E(FACTOR_LEAD)}</p>
    <div class="tablewrap"><table><thead><tr><th style="white-space:nowrap">순위</th><th>방향</th><th>요인</th><th>근거</th></tr></thead><tbody>{factor_rows}</tbody></table></div></section>
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
anchors = set(re.findall(r'id="(I4-[A-Z]-\d{3})"', page))
bad = sorted({i for i in re.findall(r'href="#(I4-[A-Z]-\d{3})"', page) if i not in anchors})
order = [page.index(f"<h2>{h}") for h in ("한 줄 답", "해석", "주요 사건", "전망", "확산 단계와 요인 순위", "핵심 지표")]
print("article_r1.html 생성,", len(page), "bytes; 앵커 없는 근거 링크:", bad or "없음", "; 섹션 순서 정상:", order == sorted(order))
# ---------- 포털 신호: 판정 칩과 게이지를 판정 데이터에서 계산해 내보낸다
SIGNAL_CHIP = '1위 제약 전력·데이터센터'
SIGNAL_GAUGE = '산업·업무 6개 중 확산 이상(글로벌)'
SIGNAL_FRONTIER = '기업 전체 초기 확산'
signal = {"question": 'I4', "round": 1, "chip": SIGNAL_CHIP, "gauge": SIGNAL_GAUGE, "frontier": SIGNAL_FRONTIER,
          "on": sum(1 for r in STAGES if r[1] in ("확산", "주류")), "of": len(STAGES)}
(ROOT / "signal_r1.json").write_text(json.dumps(signal, ensure_ascii=False, indent=1), encoding="utf-8")
print("signal_r1.json:", signal["chip"], f'{signal["on"]}/{signal["of"]}')
sys.exit(1 if bad or order != sorted(order) else 0)

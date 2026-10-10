"""records.jsonl → 기준 아티클 HTML (L4 R1).
순서: 한 줄 답 → 해석 → 주요 사건 → 전망 → 계열사별 AX 단계 → 핵심 지표 → 미확인·경고
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

TITLE = "LG의 AX는 목표에서 결과로 얼마나 넘어왔나"
QUESTION = "LG는 내부 업무와 외부 고객 사업에서 AI를 어떻게 실행 체계로 전환하며, 사용·품질·생산성·매출 성과는 무엇인가?"

# 1. 한 줄 답 ----------------------------------------------------------
ONE_LINE = ("2026년 10월 현재 LG의 AX는 계열사마다 단계가 다르다. LG CNS는 외부 사업화(상반기 AI·클라우드 매출 1조 6,714억 원, 전체의 59%)까지 왔고, LG디스플레이·LG에너지솔루션은 업무 단위 성과(설계 한 달→8시간, 리튬 가격 예측 정확도 90%+)를 공개했으며, LG전자는 업무 적용(LGenie 월 3만 명), LG화학은 교육 단계(3,000명)다. "
            "목표는 전사 단위(엔솔 2028년 생산성 50%, LGD 30%)인데 공개된 결과는 업무 단위에 머물고, LG전자가 만든 업무 에이전트는 절반 이상(96개 중 50개)이 사라졌다.")
ONE_LINE_BASIS = ["L4-I-001", "L4-I-002", "L4-I-003", "L4-I-004"]
ANSWER_ROWS = [
    ("외부 사업화", "LG CNS. AI·클라우드 매출 59%, Palantir(그룹 PoC → 본 계약), Claude Enterprise 그룹 통합 계약, ChatGPT Enterprise 고객 약 10곳.", ["L4-M-007", "L4-E-002", "L4-E-007", "L4-M-008"]),
    ("성과 공개", "LG디스플레이(설계 30일→8시간, 품질 3주→2일, 연 2,000억 원), LG에너지솔루션(리튬 가격 예측 90%+, ESS 셀 100만 개 학습).", ["L4-M-004", "L4-M-005"]),
    ("업무 적용", "LG전자. LGenie 월 3만 명, 에이전트 96개 중 46개 생존.", ["L4-M-001", "L4-M-002"]),
    ("교육·도구 배포", "LG화학. AX 교육 3,000명(사무직 절반), 1인 1에이전트.", ["L4-M-006"]),
    ("목표 vs 결과", "전사 생산성 목표(엔솔 50%·LGD 30%)에 대응하는 전사 결과치는 아직 공개되지 않음.", ["L4-M-003", "L4-I-002"]),
]
answer_rows = "".join(f'<div class="arow"><dt>{E(k)}</dt><dd>{E(v)} {tags(ids)}</dd></div>' for k, v, ids in ANSWER_ROWS)

# 2. 해석 --------------------------------------------------------------
NARRATIVE = [
    ("계열사마다 AX의 단계가 다르다. LG CNS는 상반기 AI·클라우드 매출 1조 6,714억 원으로 전체의 약 59%를 차지해 외부 사업화 단계에 있다. LG디스플레이와 LG에너지솔루션은 업무 단위 성과를 숫자로 공개했고, "
     "LG전자는 사내 플랫폼 LGenie를 월 3만 명이 쓰는 업무 적용 단계, LG화학은 반년 만에 사무직 절반(3,000명)이 교육을 마친 교육·도구 배포 단계다.",
     ["L4-M-007", "L4-M-004", "L4-M-005", "L4-M-001", "L4-M-006", "L4-I-001"]),
    ("목표는 전사 단위인데 결과는 업무 단위다. LG에너지솔루션은 2028년까지 전사 생산성 50% 개선을, LG디스플레이는 3년 내 30% 향상을 내걸었다. 공개된 결과는 LG디스플레이의 설계 기간 한 달→8시간, 품질 개선 3주→2일, 연 2,000억 원 원가 효과, "
     "LG에너지솔루션의 리튬 가격 예측 정확도 90% 이상처럼 개별 업무의 개선이다. 전사 결과치를 공개한 계열사는 아직 없다.",
     ["L4-M-003", "L4-M-004", "L4-M-005", "L4-I-002", "L4-I-006"]),
    ("업무 에이전트의 절반은 살아남지 못한다. LG전자가 5월 AX Fair에서 공개한 바로는 지난해 만든 에이전트 96개 중 46개만 쓰이고 있다. OCR·비전 AI 같은 기술에서 출발해 쓸 곳을 찾은 에이전트는 사라졌고, 현업의 반복 비효율에서 출발한 에이전트가 남았다. "
     "실행 체계의 초점이 '많이 만들기'에서 '문제부터 정의하기'로 옮겨가고 있다.",
     ["L4-M-002", "L4-E-005", "L4-I-003"]),
    ("그룹 내부는 외부 AX 사업의 시험장이다. LG CNS의 Palantir 협력은 LG 계열사 품질 관리 PoC를 거쳐 본 계약이 됐고, 전방배치 엔지니어링 조직을 만들어 그룹부터 적용한 뒤 외부로 넓힌다. "
     "6월 Anthropic과 맺은 Claude Enterprise 계약도 그룹 전 계열사에 적용할 수 있는 통합 계약이며, 외부 기업 도입까지 지원한다.",
     ["L4-E-002", "L4-E-007", "L4-I-004"]),
    ("LG의 AX는 여러 외부 플랫폼을 조합한다. 데이터 통합과 의사결정은 Palantir, 그룹 업무 AI는 Claude, 외부 재판매는 ChatGPT Enterprise(1분기 고객 약 10곳)를 쓴다. 자체 모델 EXAONE을 포함한 역할 분담은 공개되지 않았다. "
     "LG에너지솔루션은 CEO가 매월 AI 거버넌스 위원회를 주재하며 도입·보안·변화관리를 점검한다.",
     ["L4-E-002", "L4-E-007", "L4-M-008", "L4-E-003", "L4-I-005", "L4-I-007"]),
]
narrative_html = "".join(para(t, ids) for t, ids in NARRATIVE)
DIR = {"강화": "up", "약화": "down", "중립": "flat"}
irows = "".join(f"""<tr id="{E(r['id'])}"><td><span class="dir {DIR[r['direction']]}">{E(r['direction'])}</span></td>
  <td class="tgt">{E(r['target'])}</td><td>{E(r['statement'])}</td><td>{tags(r['basis'])}</td><td class="idc"><code>{E(r['id'])}</code></td></tr>"""
  for r in recs if r["type"] == "해석")

# 3. 주요 사건 (최신순) ------------------------------------------------
EVENTS_LEAD = ("3월 Palantir, 6월 Anthropic과의 계약이 LG AX의 외부 플랫폼 축을 만들었다. 그 사이 LG에너지솔루션은 2028년 생산성 50% 목표를, LG전자는 에이전트 생존율 48%라는 내부 교훈을, LG화학은 교육 3,000명 돌파를 밝혔다.")
events = sorted([r for r in recs if r["type"] == "사건" and r.get("verified")], key=lambda r: r["date"], reverse=True)
erows = "".join(f"""<li id="{E(r['id'])}"><time>{E(r['date'])}</time><div><b>{E(r['actor'])}</b> {E(r['statement'])}
  <div class="src">{src_links(r)} <code>{E(r['id'])}</code></div></div></li>""" for r in events)

# 4. 전망 --------------------------------------------------------------
FORECAST_LEAD = ("2027년 말을 기준으로 두 시나리오를 세웠다. 갈림길은 계열사가 전사 생산성 결과치를 공개하는지, 그리고 LG CNS가 그룹에서 검증한 AX를 외부 고객에 파는지다.")
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

# 5. 계열사별 AX 단계와 목표·결과 ---------------------------------
SG = ["교육·도구 배포", "업무 적용", "성과 공개", "외부 사업화"]
STAGE_LEAD = ("계열사마다 교육·도구 배포 → 업무 적용 → 성과 공개(사용·품질·생산성 결과치) → 외부 사업화(매출) 중 어디에 있는지 판정했다. 오른쪽 표시는 공개된 수치가 결과치인지 목표치인지다.")
CUST = {"결과치 공개": "brand", "목표치만": "agent", "사용 지표만": "platform", "매출 공개": "brand"}
STAGES = [
    ("LG CNS", "외부 사업화", "매출 공개", "AI·클라우드 매출 1조 6,714억 원(59%), Palantir·Claude·ChatGPT Enterprise", ["L4-M-007", "L4-E-002", "L4-E-007"]),
    ("LG디스플레이", "성과 공개", "결과치 공개", "설계 30일→8시간, 품질 3주→2일, 연 2,000억 원, Hi-D +10% (2025년 발표)", ["L4-M-004"]),
    ("LG에너지솔루션", "성과 공개", "결과치 공개", "리튬 가격 예측 90%+, ESS 셀 100만 개 학습. 2028년 생산성 50%는 목표", ["L4-M-005", "L4-M-003"]),
    ("LG전자", "업무 적용", "사용 지표만", "LGenie 월 3만 명, 에이전트 96개 중 46개 생존", ["L4-M-001", "L4-M-002"]),
    ("LG화학", "교육·도구 배포", "사용 지표만", "AX 교육 3,000명, 1인 1에이전트, 결과치 미공개", ["L4-M-006"]),
]
def sg4(v):
    i = SG.index(v)
    return "".join(f'<span class="pip{" on" if k <= i else ""}"></span>' for k in range(4)) + f'<span class="lv">{E(v)}</span>'
stage_rows = "".join(f"""<div class="rung"><div class="stage"><b>{E(d)}</b></div>
  <div class="lvcell"><span class="pips">{sg4(st)}</span></div>
  <div class="lvcell"><span class="own {CUST[c]}">{E(c)}</span></div>
  <p class="why">{E(w)} {tags(ids)}</p></div>""" for d, st, c, w, ids in STAGES)
LEDGER_LEAD = "계열사가 밝힌 목표와 공개된 결과를 나란히 놓았다. 전사 목표에 대응하는 전사 결과가 나오는지가 다음 회차의 판정 기준이다."
LEDGER = [
    ("LG에너지솔루션", "2028년까지 전사 생산성 50% 개선", "리튬 가격 예측 정확도 90%+, ESS 안전진단(셀 100만 개)", "업무 단위", "2026-04", ["L4-M-003", "L4-M-005"]),
    ("LG디스플레이", "3년 내 업무 생산성 30% 이상", "설계 30일→8시간, 품질 3주→2일, 연 2,000억 원, Hi-D +10%", "업무 단위", "2025-08", ["L4-M-003", "L4-M-004"]),
    ("LG전자", "공개 목표 확인 안 됨 (R1)", "LGenie 월 3만 명, 에이전트 생존 46/96", "사용 지표", "2026-05", ["L4-M-001", "L4-M-002"]),
    ("LG화학", "1인 1에이전트", "교육 3,000명 (사무직 절반)", "사용 지표", "2026-05", ["L4-M-006"]),
    ("LG CNS", "그룹 → 외부 AX 사업 확대", "AI·클라우드 매출 59%, ChatGPT Enterprise 고객 약 10곳", "매출", "2026-H1", ["L4-M-007", "L4-M-008"]),
]
ledger_rows = "".join(f"""<tr><td class="tgt">{E(a)}</td><td>{E(b)}</td><td>{E(c)}</td><td>{E(d)}</td><td>{E(e)}</td><td>{tags(ids)}</td></tr>""" for a, b, c, d, e, ids in LEDGER)
STAGE_NOTE = "판정: 외부 사업화는 LG CNS, 성과 공개는 LGD·엔솔(업무 단위), 업무 적용은 LG전자, 교육은 LG화학. 전사 결과치를 공개한 계열사는 아직 없다 (R1 기준)."

# 6. 핵심 지표 ---------------------------------------------------------
INDICATOR_NAMES = {"L4-T1": "사내 AI 플랫폼 사용", "L4-T2": "에이전트 생존율", "L4-T3": "생산성 목표",
                   "L4-T4": "생산성 결과", "L4-T5": "품질·의사결정 결과", "L4-T6": "교육·확산",
                   "L4-T7": "외부 AX 매출", "L4-T8": "외부 플랫폼 계약"}
metrics = sorted([r for r in recs if r["type"] == "지표"], key=lambda r: (r["indicator"], -r["importance"]))
filled = {r["indicator"] for r in metrics if r.get("verified")}
empty_ind = [f"{k} {v}" for k, v in INDICATOR_NAMES.items() if k not in filled]
METRICS_LEAD = (f"추적 지표 8개 중 {len(filled)}개의 값을 원문으로 확인했다. "
                "목표치는 결과치와 구분해 표시했고, AX 행사에서 발표된 수치와 기간 이전 발표(LG디스플레이)는 주의 표시를 달았다. 비교 렌즈(Palantir 도입 기업 등)는 다음 회차에 확보한다.")
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

page = f"""<title>L4 LG 엔터프라이즈 AX R1</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans+KR:wght@400;500;600&family=Noto+Serif+KR:wght@600;800&display=swap">
<style>{CSS}</style>
<main>
  <header class="narrow">
    <div class="eyebrow"><span>LG Group AI</span><span>L4 · Enterprise AX / Agentic Operating Model</span><span>R1 기준 회차 · 2026-10-09</span></div>
    <h1>{E(TITLE)}</h1>
    <p class="question">고정 질문 v1.0 — {E(QUESTION)}</p>
  </header>
  <section class="answer-box"><h2>한 줄 답</h2>
    <p class="answer narrow">{E(ONE_LINE)} {tags(ONE_LINE_BASIS)}</p><dl class="arows">{answer_rows}</dl></section>
  <section><h2>해석</h2><div class="narrative">{narrative_html}</div>
    <div class="tablewrap"><table><thead><tr><th>방향</th><th>대상</th><th>해석</th><th>근거</th><th>기록</th></tr></thead><tbody>{irows}</tbody></table></div></section>
  <section><h2>주요 사건 <small>최신순 · 원문 확인된 것만</small></h2><p class="lead">{E(EVENTS_LEAD)}</p><ul class="timeline">{erows}</ul></section>
  <section><h2>전망 <small>2027년 말까지, 목표가 결과가 될까</small></h2><p class="lead">{E(FORECAST_LEAD)}</p>
    <div class="scens">{scen_html}</div>
    <h3 class="subhead">세부 판정 근거</h3>
    <p class="lead muted">각 세부 전망이 적중하거나 빗나갔을 때 어느 시나리오 쪽 신호인지 표시했다. 확인 시점이 오면 확인 방법대로 판정한다.</p>
    <div class="tablewrap"><table><thead><tr><th>세부 전망</th><th>확인 시점</th><th>적중 시</th><th>빗나갈 시</th><th>상태</th><th>근거</th></tr></thead><tbody>{frows}</tbody></table></div></section>
  <section><h2>계열사별 AX 단계 <small>단계 판정 · 목표와 결과</small></h2><p class="lead">{E(STAGE_LEAD)}</p>
    <div class="ladder mapgrid auto">{stage_rows}</div><p class="gapnote">{E(STAGE_NOTE)}</p>
    <h3 class="subhead">목표치와 결과치</h3><p class="lead">{E(LEDGER_LEAD)}</p>
    <div class="tablewrap"><table><thead><tr><th>계열사</th><th>목표</th><th>공개된 결과</th><th>결과의 단위</th><th>시점</th><th>기록</th></tr></thead><tbody>{ledger_rows}</tbody></table></div></section>
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
anchors = set(re.findall(r'id="(L4-[A-Z]-\d{3})"', page))
bad = sorted({i for i in re.findall(r'href="#(L4-[A-Z]-\d{3})"', page) if i not in anchors})
order = [page.index(f"<h2>{h}") for h in ("한 줄 답", "해석", "주요 사건", "전망", "계열사별 AX 단계", "핵심 지표")]
print("article_r1.html 생성,", len(page), "bytes; 앵커 없는 근거 링크:", bad or "없음", "; 섹션 순서 정상:", order == sorted(order))
# ---------- 포털 신호: 판정 칩과 게이지를 판정 데이터에서 계산해 내보낸다
SIGNAL_CHIP = '성과 공개 3곳, 전사 결과 0'
SIGNAL_GAUGE = '계열사 5곳 중 성과 공개 이상'
SIGNAL_FRONTIER = '전사 결과치'
signal = {"question": 'L4', "round": 1, "chip": SIGNAL_CHIP, "gauge": SIGNAL_GAUGE, "frontier": SIGNAL_FRONTIER,
          "on": sum(1 for r in STAGES if SG.index(r[1]) >= SG.index("성과 공개")), "of": len(STAGES)}
(ROOT / "signal_r1.json").write_text(json.dumps(signal, ensure_ascii=False, indent=1), encoding="utf-8")
print("signal_r1.json:", signal["chip"], f'{signal["on"]}/{signal["of"]}')
sys.exit(1 if bad or order != sorted(order) else 0)

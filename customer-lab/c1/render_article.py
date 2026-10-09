"""records.jsonl → 기준 아티클 HTML (C1 R1).
아티클은 기록에서만 만든다. 서술형 요약과 판정도 근거 기록 번호를 함께 가진다.
순서: 한 줄 답 → 해석 → 주요 사건 → 전망 → 단계별 판정 → 핵심 지표 → 미확인·경고
"""
import json, html, re, sys
from pathlib import Path

ROOT = Path(__file__).parent
recs = [json.loads(l) for l in (ROOT / "records.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
by = {r["id"]: r for r in recs}
E = html.escape

def tags(ids):
    return "".join(f'<a class="rid" href="#{E(i)}" title="{E(by[i]["statement"])}">{E(i)}</a>' for i in ids)

def para(text, ids):
    return f"<p>{E(text)} {tags(ids)}</p>"

def src_links(r):
    return " · ".join(
        f'<a href="{E(s["url"])}" target="_blank" rel="noopener">{E(s["publisher"])}</a><span class="grade g{E(s["grade"])}">{E(s["grade"])}</span>'
        for s in r.get("sources", []))

# =====================================================================
# 1. 한 줄 답
# =====================================================================
QUESTION = "소비자는 탐색 → 답변 → 추천 → 결정 → 위임 중 어느 단계까지 AI에 맡기고 있으며, 검색엔진·브랜드 사이트의 역할은 얼마나 줄었는가?"
ONE_LINE = "2026년 10월 현재 AI가 대신하는 일은 ‘찾아보고 후보를 추려주는 것’까지다. 무엇을 살지 정하고 결제하는 일은 소비자가 직접 하며, 결제까지 AI에 맡기겠다는 소비자는 9%에 그친다."
ONE_LINE_BASIS = ["C1-I-002", "C1-I-003", "C1-M-011"]
ANSWER_ROWS = [
    ("AI가 대신하는 것", "검색·비교·추천. 미국 구글 검색의 68%가 클릭 없이 끝나고, AI를 거쳐 쇼핑몰에 들어온 방문은 일반 방문보다 60% 더 구매로 이어진다.",
     ["C1-M-003", "C1-M-006"]),
    ("아직 못 하는 것", "최종 선택과 결제. ChatGPT의 대화 안 결제는 출시 6개월이 안 된 2026년 3월에 철회됐고, 미국·영국 소비자 55%는 AI의 대리 구매가 불편하다고 답했다.",
     ["C1-E-002", "C1-M-012"]),
    ("한국", "AI를 주 쇼핑 수단으로 쓰는 소비자는 7%로 6개국 평균(14%)의 절반이다. 대신 네이버 AI탭·쇼핑 에이전트처럼 기존 플랫폼 안의 AI가 탐색을 흡수하고 있다.",
     ["C1-M-008", "C1-E-009", "C1-M-015"]),
    ("검색엔진·브랜드 사이트", "검색엔진은 정보 탐색에서 클릭을 잃고 있다. 브랜드·리테일러 사이트는 방문 수 대신 ‘최종 확인과 결제’ 장소로서 무게가 커지고 있다.",
     ["C1-M-004", "C1-I-001", "C1-I-002"]),
]
answer_rows = "".join(
    f'<div class="arow"><dt>{E(k)}</dt><dd>{E(v)} {tags(ids)}</dd></div>' for k, v, ids in ANSWER_ROWS)

# =====================================================================
# 2. 해석 — 서술형 요약 + 해석 기록
# =====================================================================
NARRATIVE = [
    ("미국에서는 정보를 찾는 단계가 이미 AI로 넘어갔다. 구글 검색 열 번 중 일곱 번(68%)이 클릭 없이 끝나고, AI 요약이 뜨면 일반 결과 클릭이 15%에서 8%로 줄어든다. "
     "다만 전용 AI 검색인 AI Mode로 넘어간 검색은 0.34%뿐이다. 변화는 별도 AI 서비스보다 기존 검색 화면 안에서 먼저 일어나고 있다.",
     ["C1-M-003", "C1-M-004", "C1-M-005", "C1-I-001"]),
    ("추천 단계도 AI가 실질적으로 맡기 시작했다. AI를 거쳐 쇼핑몰에 들어온 방문은 1년 전에는 일반 방문보다 전환율이 38% 낮았지만, 2026년 7월에는 60% 높아졌다. "
     "소비자가 AI와 대화하며 후보를 좁힌 뒤 사이트에 들어오기 때문이다. 유입 증가율은 1분기 393%에서 7월 62%로 낮아져, 성장의 무게가 양에서 질로 옮겨가고 있다.",
     ["C1-M-007", "C1-M-006", "C1-I-002", "C1-I-006"]),
    ("결정과 결제는 아직 사람 몫이다. 16개국 소비자 32%는 예산·브랜드 범위 안에서 AI가 고르게 하겠다고 했지만, 결제까지 맡기겠다는 응답은 9%였다. "
     "공급 쪽도 같은 방향이다. OpenAI는 대화 안 결제를 접고 구매를 리테일러 앱과 사이트로 넘겼다.",
     ["C1-M-011", "C1-M-012", "C1-E-001", "C1-E-002", "C1-I-003"]),
    ("한국은 경로가 다르다. 생성형 AI 경험률은 44.5%까지 올랐지만 AI를 주 쇼핑 수단으로 쓰는 소비자는 7%이고, 탐색은 여전히 마켓플레이스(59%)에서 시작한다. "
     "대신 네이버가 검색창에 AI탭을 넣고 쇼핑 에이전트를 붙이면서, AI가 기존 플랫폼 안에서 쓰이는 방식으로 퍼지고 있다. 쇼핑 에이전트 경유 거래액은 3개월 만에 2.7배가 됐다.",
     ["C1-M-001", "C1-M-008", "C1-M-009", "C1-E-009", "C1-M-015", "C1-I-004"]),
    ("한국 소비자는 AI 쇼핑에서 허위·편향 정보를 우려하는 비율(64%)이 글로벌 평균(52%)보다 높다. AI는 비교·검증 보조로 쓰고 최종 판단은 직접 하는 모습이다.",
     ["C1-M-013", "C1-I-005"]),
]
narrative_html = "".join(para(t, ids) for t, ids in NARRATIVE)

DIR = {"강화": "up", "약화": "down", "중립": "flat"}
interps = [r for r in recs if r["type"] == "해석"]
irows = "".join(f"""<tr id="{E(r['id'])}"><td><span class="dir {DIR[r['direction']]}">{E(r['direction'])}</span></td>
  <td class="tgt">{E(r['target'])}</td><td>{E(r['statement'])}</td><td>{tags(r['basis'])}</td><td class="idc"><code>{E(r['id'])}</code></td></tr>""" for r in interps)

# =====================================================================
# 3. 주요 사건 — 최신순
# =====================================================================
EVENTS_LEAD = ("사건의 흐름은 ‘AI가 결제까지 직접 쥐는 시도’에서 ‘기존 플랫폼과 리테일러 안에 AI를 넣는 방식’으로 옮겨가고 있다. "
               "글로벌에서는 OpenAI가 대화 안 결제를 접었고, 한국에서는 네이버가 검색(AI탭)과 쇼핑(쇼핑 AI 에이전트) 두 접점에 AI를 정식 적용했다.")
events = sorted([r for r in recs if r["type"] == "사건" and r.get("verified")], key=lambda r: r["date"], reverse=True)
erows = "".join(f"""<li id="{E(r['id'])}"><time>{E(r['date'])}</time><div><b>{E(r['actor'])}</b> {E(r['statement'])}
  <div class="src">{src_links(r)} <code>{E(r['id'])}</code></div></div></li>""" for r in events)

# =====================================================================
# 4. 전망 — 메인 질문 시나리오 + 세부 판정 신호
# =====================================================================
FORECAST_LEAD = ("핵심은 지금의 경계선(추천 → 결정)이 2027년 말까지 한 칸 앞으로 가느냐다. 낙관·비관 두 시나리오를 세우고, "
                 "확인 시점이 정해진 세부 전망들의 판정 결과를 어느 쪽에 가까운지 보여주는 신호로 쓴다.")
scen = [r for r in recs if r["type"] == "전망" and r.get("scenario")]
scen.sort(key=lambda r: 0 if r["scenario"] == "낙관" else 1)
scen_html = ""
for r in scen:
    ms = "".join(f'<li><time>{E(m["by"])}</time><span>{E(m["text"])}</span></li>' for m in r["milestones"])
    cls = "opt" if r["scenario"] == "낙관" else "pes"
    en = "Optimistic" if cls == "opt" else "Pessimistic"
    scen_html += f"""<article class="scen {cls}" id="{E(r['id'])}">
  <header><span class="sk">{E(r['scenario'])} · {en}</span><code>{E(r['id'])}</code></header>
  <p class="sstmt">{E(r['statement'])}</p>
  <ol class="ms">{ms}</ol>
  <dl class="sdl"><div><dt>판정 시점</dt><dd>{E(r['due'])}</dd></div><div><dt>판정 방법</dt><dd>{E(r['method'])}</dd></div>
  <div><dt>전제</dt><dd>{E(r['condition'])}</dd></div><div><dt>근거</dt><dd>{tags(r['basis'])}</dd></div></dl>
</article>"""

sign = {}
for r in scen:
    for sp in r["signposts"]:
        d = sign.setdefault(sp["id"], {"hit": set(), "miss": set()})
        if "on_hit" in sp: d["hit"].add(sp["on_hit"])
        if "on_miss" in sp: d["miss"].add(sp["on_miss"])
def side(s):
    return "".join(f'<span class="side {"opt" if x=="낙관" else "pes"}">{E(x)}</span>' for x in sorted(s)) or '<span class="muted">—</span>'
details = sorted([r for r in recs if r["type"] == "전망" and not r.get("scenario")], key=lambda r: r["due"])
frows = "".join(f"""<tr id="{E(r['id'])}"><td class="stmt">{E(r['statement'])}<small>확인 방법: {E(r['method'])}</small></td>
  <td class="asof">{E(r['due'])}</td><td>{side(sign.get(r['id'],{}).get('hit',set()))}</td><td>{side(sign.get(r['id'],{}).get('miss',set()))}</td>
  <td><span class="fstat">{E(r['forecast_status'])}</span></td><td>{tags(r['basis'])}</td></tr>""" for r in details)

# =====================================================================
# 5. 단계별 판정
# =====================================================================
LEVELS = ["실험", "얼리어답터", "확산", "주류"]
LADDER_LEAD = "탐색·답변은 주류, 추천은 확산, 결정은 얼리어답터, 위임은 실험 단계다. 한국은 답변 단계만 한 칸 뒤에 있다."
LADDER = [
    ("탐색", "Search", "주류", "주류", "미국 구글 검색 68%가 클릭 없이 끝남. 한국은 생성형 AI 경험률 44.5%.", ["C1-M-003", "C1-M-001", "C1-I-001"]),
    ("답변", "Answer", "주류", "확산", "AI 요약이 뜨면 클릭이 절반으로 줄어듦. 한국은 네이버 AI탭이 6월 전면 적용.", ["C1-M-004", "C1-E-009", "C1-M-014"]),
    ("추천", "Recommendation", "확산", "확산", "AI 유입 방문의 전환율이 일반 유입을 60% 앞섬. 한국 AI 이용자 절반이 AI 추천 제품 구매.", ["C1-M-006", "C1-M-010", "C1-I-002"]),
    ("결정", "Decision", "얼리어답터", "얼리어답터", "범위 안에서 AI가 고르게 하겠다 32%. 한국은 AI를 주 쇼핑 수단으로 쓰는 비율 7%.", ["C1-M-011", "C1-M-008", "C1-I-005"]),
    ("위임", "Delegation", "실험", "실험", "결제까지 맡기겠다 9%. 대표 사례였던 ChatGPT 대화 안 결제는 2026년 3월 철회.", ["C1-M-011", "C1-E-002", "C1-I-003"]),
]
def cell(level):
    i = LEVELS.index(level)
    return "".join(f'<span class="pip{" on" if k <= i else ""}"></span>' for k in range(4)) + f'<span class="lv">{E(level)}</span>'
ladder_rows = "".join(f"""<div class="rung" data-frontier="{'y' if ko in ('추천','결정') else 'n'}">
  <div class="stage"><b>{E(ko)}</b><span>{E(en)}</span></div>
  <div class="lvcell"><span class="region">글로벌·미국</span><span class="pips">{cell(g)}</span></div>
  <div class="lvcell"><span class="region">한국</span><span class="pips">{cell(k)}</span></div>
  <p class="why">{E(w)} {tags(ids)}</p></div>""" for ko, en, g, k, w, ids in LADDER)

# =====================================================================
# 6. 핵심 지표
# =====================================================================
INDICATOR_NAMES = {
    "C1-T1": "생성형 AI 이용률 (한국)", "C1-T2": "생성형 AI 이용률 (미국·글로벌)", "C1-T3": "Zero-click·AI 요약 클릭률",
    "C1-T4": "리테일 AI 유입 트래픽", "C1-T5": "쇼핑에 AI를 쓰는 소비자", "C1-T6": "구매 위임 의향·우려",
    "C1-T7": "에이전트 결제 상용 사례 수", "C1-T8": "한국 AI 검색·쇼핑 에이전트",
}
metrics = sorted([r for r in recs if r["type"] == "지표" and r.get("status") == "유효"], key=lambda r: (r["indicator"], -r["importance"]))
filled = {r["indicator"] for r in metrics}
empty_ind = [f"{k} {v}" for k, v in INDICATOR_NAMES.items() if k not in filled]
METRICS_LEAD = (f"추적 지표 8개 중 {len(filled)}개의 값을 확보했다. 미국은 검색·트래픽 관측치(SparkToro, Adobe), 한국은 설문(과기정통부, Criteo)과 "
                f"네이버 발표 수치가 중심이다. {', '.join(empty_ind)}은 다음 간단 조사에서 우선 채운다.")
def fmt_val(r):
    v, u = r.get("value"), r.get("unit", "")
    s = f"{v:g}" if isinstance(v, (int, float)) else str(v)
    return f"{s}{'' if u.startswith('%') else ' '}{u}"
mrows = []
for r in metrics:
    prev = r.get("prev_value")
    prev_s = "—" if prev is None else (f"{prev:g}%" if r.get("unit", "").startswith("%") else str(prev))
    flag = '<span class="warn">충돌·주의</span>' if r.get("check_flags") else ""
    mrows.append(f"""<tr id="{E(r['id'])}"><td class="ind">{E(r['indicator'])}<small>{E(INDICATOR_NAMES[r['indicator']])}</small></td>
      <td class="stmt">{E(r['statement'])} {flag}<div class="src">{src_links(r)}</div></td>
      <td class="num">{E(fmt_val(r))}</td><td class="num muted">{E(prev_s)}</td>
      <td class="asof">{E(r['as_of'])}<small>{E(r['region'])}</small></td><td class="idc"><code>{E(r['id'])}</code></td></tr>""")

# =====================================================================
# 7. 미확인·경고
# =====================================================================
warns = []
for r in recs:
    if r["type"] in ("지표", "사건") and not r.get("verified"):
        warns.append((r, "원문 미확인"))
    elif r.get("check_flags"):
        warns.append((r, "주의"))
wrows = "".join(f"""<tr{' id="'+E(r['id'])+'"' if r['type']=='사건' and not r.get('verified') else ''}><td><code>{E(r['id'])}</code></td>
  <td><span class="wk">{E(k)}</span></td><td>{E(r['statement'])}</td><td class="muted">{E('; '.join(r.get('check_flags', [])))}</td></tr>""" for r, k in warns)

counts = {t: sum(1 for r in recs if r["type"] == t) for t in ("지표", "사건", "해석", "전망")}

CSS = (ROOT.parent.parent / "lib" / "article.css").read_text(encoding="utf-8")

page = f"""<title>C1 소비자 의사결정 R1</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans+KR:wght@400;500;600&family=Noto+Serif+KR:wght@600;800&display=swap">
<style>{CSS}</style>
<main>
  <header class="narrow">
    <div class="eyebrow"><span>AI Future Customer Lab</span><span>C1 · Consumer Decision Making</span><span>R1 기준 회차 · 2026-10-09</span></div>
    <h1>AI는 고객의 쇼핑을 어디까지 대신하고 있나</h1>
    <p class="question">고정 질문 v1.0 — {E(QUESTION)}</p>
  </header>

  <section class="answer-box">
    <h2>한 줄 답</h2>
    <p class="answer narrow">{E(ONE_LINE)} {tags(ONE_LINE_BASIS)}</p>
    <dl class="arows">{answer_rows}</dl>
  </section>

  <section>
    <h2>해석</h2>
    <div class="narrative">{narrative_html}</div>
    <div class="tablewrap"><table>
      <thead><tr><th>방향</th><th>대상</th><th>해석</th><th>근거</th><th>기록</th></tr></thead>
      <tbody>{irows}</tbody></table></div>
  </section>

  <section>
    <h2>주요 사건 <small>최신순 · 원문 확인된 것만</small></h2>
    <p class="lead">{E(EVENTS_LEAD)}</p>
    <ul class="timeline">{erows}</ul>
  </section>

  <section>
    <h2>전망 <small>2027년 말까지, AI는 쇼핑을 어디까지 대신할까</small></h2>
    <p class="lead">{E(FORECAST_LEAD)}</p>
    <div class="scens">{scen_html}</div>
    <h3 class="subhead">세부 판정 근거</h3>
    <p class="lead muted">각 세부 전망이 적중하거나 빗나갔을 때 어느 시나리오 쪽 신호인지 표시했다. 확인 시점이 오면 확인 방법대로 판정한다.</p>
    <div class="tablewrap"><table>
      <thead><tr><th>세부 전망</th><th>확인 시점</th><th>적중 시</th><th>빗나갈 시</th><th>상태</th><th>근거</th></tr></thead>
      <tbody>{frows}</tbody></table></div>
  </section>

  <section>
    <h2>단계별 판정 <small>실험 · 얼리어답터 · 확산 · 주류 4단계</small></h2>
    <p class="lead">{E(LADDER_LEAD)}</p>
    <div class="ladder">{ladder_rows}</div>
    <p class="frontier-note">음영 = 현재 경계선 (추천 → 결정)</p>
  </section>

  <section>
    <h2>핵심 지표 <small>추적 지표 {len(filled)}/8개 값 확보</small></h2>
    <p class="lead">{E(METRICS_LEAD)}</p>
    <div class="tablewrap"><table>
      <thead><tr><th>추적 지표</th><th>내용 · 출처</th><th style="text-align:right">현재값</th><th style="text-align:right">이전값</th><th>기준 시점</th><th>기록</th></tr></thead>
      <tbody>{''.join(mrows)}</tbody></table></div>
  </section>

  <section>
    <h2>미확인·경고 <small>본문 판단에서 빼거나 주의해서 쓴 기록</small></h2>
    <div class="tablewrap"><table>
      <thead><tr><th>기록</th><th>구분</th><th>진술</th><th>사유</th></tr></thead>
      <tbody>{wrows}</tbody></table></div>
  </section>

  <footer>
    <span>이 글은 4유형 기록 {len(recs)}건(지표 {counts['지표']} · 사건 {counts['사건']} · 해석 {counts['해석']} · 전망 {counts['전망']})에서 생성했습니다. 문장 옆 번호를 누르면 해당 기록으로 이동합니다.</span>
    <span>출처 등급 A = 1차 조사·공식 발표, B = 주요 언론·2차 보도, C = 블로그·출처 불명(원문 확인 전까지 판단에 쓰지 않음).</span>
    <span>다음 회차: 딥리서치 R2는 2026년 11월, 그 사이 매주 간단 조사로 지표·사건만 갱신합니다.</span>
  </footer>
</main>
"""
(ROOT / "article_r1.html").write_text(page, encoding="utf-8")
anchors = set(re.findall(r'id="(C1-[A-Z]-\d{3})"', page))
bad = sorted({i for i in re.findall(r'href="#(C1-[A-Z]-\d{3})"', page) if i not in by or i not in anchors})
order = [page.index(f"<h2>{h}") for h in ("한 줄 답", "해석", "주요 사건", "전망", "단계별 판정", "핵심 지표")]
print("article_r1.html 생성,", len(page), "bytes; 깨진 근거 링크:", bad or "없음", "; 섹션 순서 정상:", order == sorted(order))
sys.exit(1 if bad or order != sorted(order) else 0)

"""records.jsonl → 기준 아티클 HTML (Q5 R1).
순서: 한 줄 답 → 해석 → 주요 사건 → 전망 → 수요를 만드는 변화 순위 → 핵심 지표 → 미확인·경고
"""
import json, html, re, sys
from pathlib import Path

ROOT = Path(__file__).parent
recs = [json.loads(l) for l in (ROOT / "records.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
by = {r["id"]: r for r in recs}
E = html.escape
CSS = (ROOT.parent / "lib" / "article.css").read_text(encoding="utf-8")

def tags(ids):
    return "".join(f'<a class="rid" href="#{E(i)}" title="{E(by[i]["statement"])}">{E(i)}</a>' for i in ids)
def para(text, ids): return f"<p>{E(text)} {tags(ids)}</p>"
def src_links(r):
    return " · ".join(f'<a href="{E(s["url"])}" target="_blank" rel="noopener">{E(s["publisher"])}</a><span class="grade g{E(s["grade"])}">{E(s["grade"])}</span>' for s in r.get("sources", []))

TITLE = "어떤 삶의 변화가 수요를 만드는가"
QUESTION = "어떤 가구 변화와 생활 사건이 새로운 수요를 만들고 있는가?"

# 1. 한 줄 답 ----------------------------------------------------------
ONE_LINE = ("2026년 10월 현재 수요를 가장 빠르게 만드는 변화는 출생·혼인 반등이다(1~7월 출생아 14.7% 증가, 2025년 혼인 7년 만에 최다). "
            "가장 큰 기반은 고령 가구(전체의 28.8%)와 1인 가구(36.6%)다. 반대로 이사와 입주는 각각 51년, 13년 만의 최저여서 가전·가구 교체를 일으키던 계기가 줄고 있다.")
ONE_LINE_BASIS = ["Q5-I-001", "Q5-I-002", "Q5-I-003", "Q5-I-004"]
ANSWER_ROWS = [
    ("가장 빠르게 커지는 수요", "신혼·육아. 2025년 혼인 24만 건(+8.1%), 2026년 1~7월 출생아 17만 명(+14.7%). 백화점 신생아 상품 매출은 28.6% 늘었다.", ["Q5-M-006", "Q5-M-004", "Q5-M-011"]),
    ("가장 큰 수요 기반", "고령 가구 650만 7천 가구(28.8%). 65세 이상 인구는 21.6%이고, 고령 가구는 2038년 1천만을 넘는다.", ["Q5-M-003"]),
    ("작아지는 가구", "1인 가구 36.6%(+0.6%p), 4인 이상 가구는 1년 새 4.6% 감소.", ["Q5-M-001", "Q5-M-002"]),
    ("줄어드는 계기", "이사 611만 8천 명으로 1974년 이후 최저, 주택 사유 이동이 가장 크게 줄었다. 올해 아파트 입주는 18만 3천 가구로 2013년 이후 최저다.", ["Q5-M-008", "Q5-M-009"]),
    ("아직 확인할 것", "1분기 소비지출은 5.3% 늘었지만 자동차(+29.6%)가 이끌었다. 생활 사건 증가가 가구·가전 지출로 번졌는지는 아직 통계로 확인되지 않았다.", ["Q5-M-010"]),
]
answer_rows = "".join(f'<div class="arow"><dt>{E(k)}</dt><dd>{E(v)} {tags(ids)}</dd></div>' for k, v, ids in ANSWER_ROWS)

# 2. 해석 --------------------------------------------------------------
NARRATIVE = [
    ("지금 가장 빠르게 움직이는 것은 혼인과 출생이다. 2025년 혼인은 24만 건으로 8.1% 늘어 2018년 이후 가장 많았고, 출생아는 2024년 7월부터 매달 전년보다 늘었다. "
     "2026년 1~7월 출생아는 17만 79명으로 14.7% 늘었고, 증가율은 통계 작성 이래 최대다. 유통 현장도 이를 보여준다. 1~5월 신세계백화점 신생아 상품 매출은 28.6%, 현대백화점 유아 상품은 25.2% 늘었다.",
     ["Q5-M-006", "Q5-M-005", "Q5-M-004", "Q5-M-011", "Q5-I-001"]),
    ("규모로 보면 고령 가구가 가장 큰 기반이다. 65세 이상이 가구주인 가구는 650만 7천 가구로 전체의 28.8%이고, 2038년에는 1천만 가구를 넘는다. "
     "가구는 동시에 작아지고 있다. 1인 가구는 36.6%로 늘었고, 4인 이상 가구는 1년 새 16만 3천 가구가 줄었다.",
     ["Q5-M-003", "Q5-M-001", "Q5-M-002", "Q5-I-002", "Q5-I-003"]),
    ("반대 방향의 변화도 크다. 2025년 국내 이동자는 611만 8천 명으로 1974년 이후 가장 적었고, 주택 때문에 옮긴 사람이 가장 크게 줄었다. "
     "2026년 아파트 입주 물량은 18만 3천 가구로 2013년 이후 최저이고 서울은 전년의 절반 수준이다. 이사와 입주는 가전·가구를 새로 들이는 대표적인 계기였는데, 그 계기가 줄고 있다.",
     ["Q5-M-008", "Q5-M-009", "Q5-E-001", "Q5-I-004"]),
    ("반등 신호도 있지만 아직 약하다. 6월 이동자는 주택 매매 증가로 6월 기준 5년 만에 가장 많았지만 증가율은 0.6%였다. 혼인은 5월에 6.4% 줄었다가 7월에 9.3% 늘었다. "
     "가계 소비는 1분기 5.3% 늘었지만 자동차와 여행이 이끌었고, 생활 사건 증가가 가구·가전 지출로 번졌는지는 아직 확인되지 않았다.",
     ["Q5-E-003", "Q5-M-007", "Q5-M-010", "Q5-I-005", "Q5-I-006"]),
]
narrative_html = "".join(para(t, ids) for t, ids in NARRATIVE)
DIR = {"강화": "up", "약화": "down", "중립": "flat"}
irows = "".join(f"""<tr id="{E(r['id'])}"><td><span class="dir {DIR[r['direction']]}">{E(r['direction'])}</span></td>
  <td class="tgt">{E(r['target'])}</td><td>{E(r['statement'])}</td><td>{tags(r['basis'])}</td><td class="idc"><code>{E(r['id'])}</code></td></tr>"""
  for r in recs if r["type"] == "해석")

# 3. 주요 사건 (최신순) ------------------------------------------------
EVENTS_LEAD = ("Q5는 공식 통계가 중심이라 사건은 적다. 기록한 사건은 이사·입주 흐름을 바꿀 수 있는 것들로, 입주 물량 저점 전망, 6월 이동 반등, "
               "그리고 일부 지역의 전입을 늘린 농어촌 기본소득 시범사업이다.")
events = sorted([r for r in recs if r["type"] == "사건" and r.get("verified")], key=lambda r: r["date"], reverse=True)
erows = "".join(f"""<li id="{E(r['id'])}"><time>{E(r['date'])}</time><div><b>{E(r['actor'])}</b> {E(r['statement'])}
  <div class="src">{src_links(r)} <code>{E(r['id'])}</code></div></div></li>""" for r in events)

# 4. 전망 --------------------------------------------------------------
FORECAST_LEAD = ("2027년 말을 기준으로 두 시나리오를 세웠다. 갈림길은 출생·혼인 반등이 기저효과를 넘어 이어지는지, "
                 "그리고 이사·주택 거래가 살아나 교체 수요가 돌아오는지다.")
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

# 5. 수요를 만드는 변화 순위 -----------------------------------------------
SPEED = {"가속": "brand", "지속": "platform", "축소": "agent"}
RANK_LEAD = ("속도와 규모를 함께 보고 순위를 매겼다. 1위는 가장 빠르게 늘고 있는 변화, 2·3위는 규모가 크고 꾸준한 변화다. "
             "4위는 수요를 줄이는 방향의 변화로, 다른 변화가 만든 수요를 일부 상쇄한다.")
RANK = [
    (1, "출생·혼인 반등", "출생 +14.7% (1~7월) · 혼인 24만 건", "가속", "신혼 가전·가구, 육아용품·육아 가전, 돌봄 서비스", ["Q5-M-004", "Q5-M-006", "Q5-M-011"]),
    (2, "고령 가구 확대", "650.7만 가구 · 28.8%", "지속", "돌봄·안전·건강, 쉬운 조작, 방문 서비스", ["Q5-M-003"]),
    (3, "1인·소형 가구", "1인 36.6% · 4인 이상 −4.6%", "지속", "소형·개인화 제품, 구독·렌털", ["Q5-M-001", "Q5-M-002"]),
    (4, "이사·입주 감소", "이동 611.8만 명(51년 최저) · 입주 18.3만 가구(13년 최저)", "축소", "이사·입주 계기의 교체 수요 감소", ["Q5-M-008", "Q5-M-009"]),
]
rank_rows = "".join(f"""<tr><td class="num">{n}</td><td class="tgt">{E(ch)}</td><td class="num" style="text-align:left">{E(sz)}</td>
  <td><span class="own {SPEED[sp]}">{E(sp)}</span></td><td>{E(dm)}</td><td>{tags(ids)}</td></tr>""" for n, ch, sz, sp, dm, ids in RANK)

# 6. 핵심 지표 ---------------------------------------------------------
INDICATOR_NAMES = {"Q5-I1": "1인 가구 비중", "Q5-I2": "고령 가구 비중", "Q5-I3": "출생아 수·합계출산율",
                   "Q5-I4": "혼인 건수", "Q5-I5": "인구이동(이사)", "Q5-I6": "아파트 입주 물량",
                   "Q5-I7": "가계 내구재 지출", "Q5-I8": "생활 사건 연계 소비"}
metrics = sorted([r for r in recs if r["type"] == "지표"], key=lambda r: (r["indicator"], -r["importance"]))
filled = {r["indicator"] for r in metrics if r.get("verified")}
empty_ind = [f"{k} {v}" for k, v in INDICATOR_NAMES.items() if k not in filled]
METRICS_LEAD = (f"추적 지표 8개 중 {len(filled)}개의 값을 원문으로 확인했다. {', '.join(empty_ind)}은 이번 회차에 수치를 찾지 못했다. "
                "모든 수치는 국가데이터처 공식 통계를 인용한 보도에서 가져왔고, 원 통계표 대조는 다음 간단 조사에서 한다. 가구·가전 지출 항목은 가계동향 원자료로 채울 예정이다.")
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

page = f"""<title>Q5 가구 변화와 생활 사건 R1</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans+KR:wght@400;500;600&family=Noto+Serif+KR:wght@600;800&display=swap">
<style>{CSS}</style>
<main>
  <header class="narrow">
    <div class="eyebrow"><span>AI Future Customer Lab</span><span>Q5 · Household &amp; Life Events</span><span>R1 기준 회차 · 2026-10-09</span></div>
    <h1>{E(TITLE)}</h1>
    <p class="question">고정 질문 v1.0 — {E(QUESTION)}</p>
  </header>
  <section class="answer-box"><h2>한 줄 답</h2>
    <p class="answer narrow">{E(ONE_LINE)} {tags(ONE_LINE_BASIS)}</p><dl class="arows">{answer_rows}</dl></section>
  <section><h2>해석</h2><div class="narrative">{narrative_html}</div>
    <div class="tablewrap"><table><thead><tr><th>방향</th><th>대상</th><th>해석</th><th>근거</th><th>기록</th></tr></thead><tbody>{irows}</tbody></table></div></section>
  <section><h2>주요 사건 <small>최신순 · 원문 확인된 것만</small></h2><p class="lead">{E(EVENTS_LEAD)}</p><ul class="timeline">{erows}</ul></section>
  <section><h2>전망 <small>2027년 말까지, 삶의 변화는 수요를 늘릴까 줄일까</small></h2><p class="lead">{E(FORECAST_LEAD)}</p>
    <div class="scens">{scen_html}</div>
    <h3 class="subhead">세부 판정 근거</h3>
    <p class="lead muted">각 세부 전망이 적중하거나 빗나갔을 때 어느 시나리오 쪽 신호인지 표시했다. 확인 시점이 오면 확인 방법대로 판정한다.</p>
    <div class="tablewrap"><table><thead><tr><th>세부 전망</th><th>확인 시점</th><th>적중 시</th><th>빗나갈 시</th><th>상태</th><th>근거</th></tr></thead><tbody>{frows}</tbody></table></div></section>
  <section><h2>수요를 만드는 변화 순위 <small>규모 · 속도 · 수요 영역</small></h2><p class="lead">{E(RANK_LEAD)}</p>
    <div class="tablewrap"><table><thead><tr><th>순위</th><th>변화</th><th>규모</th><th>속도</th><th>만드는 수요</th><th>근거</th></tr></thead><tbody>{rank_rows}</tbody></table></div></section>
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
anchors = set(re.findall(r'id="(Q5-[A-Z]-\d{3})"', page))
bad = sorted({i for i in re.findall(r'href="#(Q5-[A-Z]-\d{3})"', page) if i not in anchors})
order = [page.index(f"<h2>{h}") for h in ("한 줄 답", "해석", "주요 사건", "전망", "수요를 만드는 변화 순위", "핵심 지표")]
print("article_r1.html 생성,", len(page), "bytes; 앵커 없는 근거 링크:", bad or "없음", "; 섹션 순서 정상:", order == sorted(order))
sys.exit(1 if bad or order != sorted(order) else 0)

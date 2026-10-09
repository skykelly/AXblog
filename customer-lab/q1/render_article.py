"""records.jsonl → 기준 아티클 HTML (Q1 R1).
아티클은 기록에서만 만든다. 판정(단계 사다리)도 근거 기록 번호를 함께 가진다.
"""
import json, html, sys
from pathlib import Path

ROOT = Path(__file__).parent
recs = [json.loads(l) for l in (ROOT / "records.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
by = {r["id"]: r for r in recs}
E = html.escape

QUESTION = "소비자는 탐색 → 답변 → 추천 → 결정 → 위임 중 어느 단계까지 AI에 맡기고 있으며, 검색엔진·브랜드 사이트의 역할은 얼마나 줄었는가?"
ONE_LINE = "AI는 ‘찾고 좁혀주는’ 데까지 들어왔고, ‘고르고 결제하는’ 일은 아직 사람이 쥐고 있다. 지금의 경계선은 추천과 결정 사이다."
ONE_LINE_BASIS = ["Q1-I-001", "Q1-I-002", "Q1-I-003", "Q1-I-005"]
SITE_ROLE = ("검색엔진은 정보형 검색에서 클릭을 잃고 있지만, 브랜드·리테일러 사이트는 사라지지 않고 ‘최종 확인과 결제’ 장소로 역할이 좁아지고 있다. "
             "한국에서는 그 자리를 범용 AI가 아니라 네이버 같은 기존 플랫폼 안의 AI가 먼저 차지하고 있다.")
SITE_ROLE_BASIS = ["Q1-M-003", "Q1-M-006", "Q1-E-002", "Q1-I-004"]

LEVELS = ["실험", "얼리어답터", "확산", "주류"]
LADDER = [
    ("탐색", "Search", "주류", "주류", "미국 구글 검색 68%가 클릭 없이 끝남. 한국은 생성형 AI 경험률 44.5%.", ["Q1-M-003", "Q1-M-001", "Q1-I-001"]),
    ("답변", "Answer", "주류", "확산", "AI 요약이 뜨면 클릭이 절반으로 줄어듦. 한국은 네이버 AI탭이 6월 전면 적용.", ["Q1-M-004", "Q1-E-009", "Q1-M-014"]),
    ("추천", "Recommendation", "확산", "확산", "AI 유입 방문의 전환율이 일반 유입을 60% 앞섬. 한국 AI 이용자 절반이 AI 추천 제품 구매.", ["Q1-M-006", "Q1-M-010", "Q1-I-002"]),
    ("결정", "Decision", "얼리어답터", "얼리어답터", "범위 안에서 AI가 고르게 하겠다 32%. 한국은 AI를 주 쇼핑 수단으로 쓰는 비율 7%.", ["Q1-M-011", "Q1-M-008", "Q1-I-005"]),
    ("위임", "Delegation", "실험", "실험", "결제까지 맡기겠다 9%. 대표 사례였던 ChatGPT 인챗 결제는 2026년 3월 철회.", ["Q1-M-011", "Q1-E-002", "Q1-I-003"]),
]

def tags(ids):
    return "".join(f'<a class="rid" href="#{E(i)}" title="{E(by[i]["statement"])}">{E(i)}</a>' for i in ids)

def src_links(r):
    out = []
    for s in r.get("sources", []):
        out.append(f'<a href="{E(s["url"])}" target="_blank" rel="noopener">{E(s["publisher"])}</a><span class="grade g{E(s["grade"])}">{E(s["grade"])}</span>')
    return " · ".join(out)

def fmt_val(r):
    v = r.get("value"); u = r.get("unit", "")
    s = f"{v:g}" if isinstance(v, (int, float)) else str(v)
    return f"{s}{'' if u.startswith('%') else ' '}{u}"

# ---------- 사다리 ----------
def cell(level):
    i = LEVELS.index(level)
    return "".join(f'<span class="pip{" on" if k <= i else ""}"></span>' for k in range(4)) + f'<span class="lv">{E(level)}</span>'

ladder_rows = []
for ko, en, glob, kr, why, ids in LADDER:
    ladder_rows.append(f"""
    <div class="rung" data-frontier="{'y' if ko in ('추천','결정') else 'n'}">
      <div class="stage"><b>{E(ko)}</b><span>{E(en)}</span></div>
      <div class="lvcell"><span class="region">글로벌·미국</span><span class="pips">{cell(glob)}</span></div>
      <div class="lvcell"><span class="region">한국</span><span class="pips">{cell(kr)}</span></div>
      <p class="why">{E(why)} {tags(ids)}</p>
    </div>""")

# ---------- 지표 ----------
metrics = [r for r in recs if r["type"] == "지표" and r.get("status") == "유효"]
metrics.sort(key=lambda r: (r["indicator"], -r["importance"]))
INDICATOR_NAMES = {
    "Q1-I1": "생성형 AI 이용률 (한국)", "Q1-I2": "생성형 AI 이용률 (미국·글로벌)", "Q1-I3": "Zero-click·AI 요약 클릭률",
    "Q1-I4": "리테일 AI 유입 트래픽", "Q1-I5": "쇼핑에 AI를 쓰는 소비자", "Q1-I6": "구매 위임 의향·우려",
    "Q1-I7": "에이전트 결제 상용 사례 수", "Q1-I8": "한국 AI 검색·쇼핑 에이전트",
}
filled = {r["indicator"] for r in metrics}
mrows = []
for r in metrics:
    prev = r.get("prev_value")
    prev_s = f"{prev:g}%" if prev is not None and r.get("unit", "").startswith("%") else ("—" if prev is None else str(prev))
    flag = '<span class="warn">충돌·주의</span>' if r.get("check_flags") else ""
    mrows.append(f"""<tr id="{E(r['id'])}">
      <td class="ind">{E(r['indicator'])}<small>{E(INDICATOR_NAMES[r['indicator']])}</small></td>
      <td class="stmt">{E(r['statement'])} {flag}<div class="src">{src_links(r)}</div></td>
      <td class="num">{E(fmt_val(r))}</td><td class="num muted">{E(prev_s)}</td>
      <td class="asof">{E(r['as_of'])}<small>{E(r['region'])}</small></td>
      <td class="idc"><code>{E(r['id'])}</code></td></tr>""")
empty_ind = [f"{k} {v}" for k, v in INDICATOR_NAMES.items() if k not in filled]

# ---------- 사건 ----------
events = sorted([r for r in recs if r["type"] == "사건" and r.get("verified")], key=lambda r: r["date"])
erows = "".join(f"""<li id="{E(r['id'])}"><time>{E(r['date'])}</time><div><b>{E(r['actor'])}</b> {E(r['statement'])}
  <div class="src">{src_links(r)} <code>{E(r['id'])}</code></div></div></li>""" for r in events)

# ---------- 해석 ----------
DIR = {"강화": "up", "약화": "down", "중립": "flat"}
interps = [r for r in recs if r["type"] == "해석"]
irows = "".join(f"""<article class="interp" id="{E(r['id'])}">
  <header><span class="dir {DIR[r['direction']]}">{E(r['direction'])}</span><h3>{E(r['target'])}</h3><code>{E(r['id'])}</code></header>
  <p>{E(r['statement'])}</p><div class="basis">근거 {tags(r['basis'])}</div></article>""" for r in interps)

# ---------- 전망 ----------
fcs = sorted([r for r in recs if r["type"] == "전망"], key=lambda r: r["due"])
frows = "".join(f"""<tr id="{E(r['id'])}"><td class="stmt">{E(r['statement'])}<small>조건: {E(r['condition'])}</small></td>
  <td class="asof">{E(r['due'])}</td><td class="method">{E(r['method'])}</td><td><span class="fstat">{E(r['forecast_status'])}</span></td>
  <td>{tags(r['basis'])}</td></tr>""" for r in fcs)

# ---------- 미확인·경고 ----------
warns = []
for r in recs:
    if r["type"] in ("지표", "사건") and not r.get("verified"):
        warns.append((r["id"], "원문 미확인", r["statement"], "; ".join(r.get("check_flags", []))))
    elif r.get("check_flags"):
        warns.append((r["id"], "주의", r["statement"], "; ".join(r["check_flags"])))
wrows = "".join(f"""<tr id="{E(i) if by[i]['type']=='사건' and not by[i].get('verified') else ''}"><td><code>{E(i)}</code></td><td><span class="wk">{E(k)}</span></td><td>{E(s)}</td><td class="muted">{E(n)}</td></tr>""" for i, k, s, n in warns)

counts = {t: sum(1 for r in recs if r["type"] == t) for t in ("지표", "사건", "해석", "전망")}

page = f"""<title>Q1 소비자 의사결정 R1</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans+KR:wght@400;500;600&family=Noto+Serif+KR:wght@600;800&display=swap">
<style>
/* Layout: 연구 노트 한 단(68ch) — 사다리 판정 → 표 → 근거 연결. 기록 번호가 본문 곳곳의 각주 역할 */
:root {{
  --paper: #f6f7f9; --ink: #16202b; --muted: #5d6875; --rule: #d6dbe2; --panel: #ffffff;
  --accent: #1f5f8b; --accent-soft: #e2edf5; --amber: #b4690e; --amber-soft: #f7ead7;
  --up: #1f7a4d; --down: #b3412f; --flat: #6a7380;
  --display: "Noto Serif KR", "Apple SD Gothic Neo", serif;
  --body: "IBM Plex Sans KR", "Apple SD Gothic Neo", "Malgun Gothic", system-ui, sans-serif;
  --mono: "IBM Plex Mono", ui-monospace, Menlo, monospace;
}}
@media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) {{
  --paper: #11161c; --ink: #e6ebf1; --muted: #9aa5b1; --rule: #2b333d; --panel: #171e26;
  --accent: #7fb6dc; --accent-soft: #1b2c3a; --amber: #e2a457; --amber-soft: #33271a;
  --up: #5fc493; --down: #ec8a78; --flat: #98a2ae; color-scheme: dark; }} }}
:root[data-theme="dark"] {{
  --paper: #11161c; --ink: #e6ebf1; --muted: #9aa5b1; --rule: #2b333d; --panel: #171e26;
  --accent: #7fb6dc; --accent-soft: #1b2c3a; --amber: #e2a457; --amber-soft: #33271a;
  --up: #5fc493; --down: #ec8a78; --flat: #98a2ae; color-scheme: dark; }}
* {{ box-sizing: border-box; }}
body {{ background: var(--paper); color: var(--ink); font: 400 16px/1.7 var(--body); padding: 0 20px; }}
main {{ max-width: 980px; margin: 0 auto; padding-block: 40px 72px; display: grid; gap: 56px; }}
.narrow {{ max-width: 68ch; }}
a {{ color: var(--accent); }}
code, .rid {{ font: 500 12px/1 var(--mono); }}
h1, h2, h3 {{ text-wrap: balance; margin: 0; }}
.eyebrow {{ font: 500 12px/1.4 var(--mono); letter-spacing: .06em; text-transform: uppercase; color: var(--muted); display: flex; gap: 14px; flex-wrap: wrap; }}
h1 {{ font: 800 clamp(26px, 4.4vw, 40px)/1.25 var(--display); margin-top: 14px; }}
.question {{ margin: 16px 0 0; color: var(--muted); font-size: 15px; border-left: 2px solid var(--rule); padding-left: 14px; }}
.answer {{ font: 600 clamp(20px, 2.8vw, 25px)/1.55 var(--display); margin: 0; }}
.answer-wrap {{ display: grid; gap: 14px; }}
.answer-wrap p.sub {{ margin: 0; }}
h2 {{ font: 600 22px/1.3 var(--display); display: flex; align-items: baseline; gap: 12px; flex-wrap: wrap; }}
h2 small {{ font: 400 13px var(--body); color: var(--muted); }}
section {{ display: grid; gap: 18px; min-width: 0; }}
.rid {{ display: inline-block; padding: 3px 5px; margin: 2px 2px 0 0; border-radius: 3px; background: var(--accent-soft); color: var(--accent); text-decoration: none; vertical-align: 1px; }}
.rid:hover, .rid:focus-visible {{ outline: 1px solid var(--accent); }}
/* 사다리 */
.ladder {{ border-top: 1px solid var(--ink); }}
.rung {{ display: grid; grid-template-columns: 150px 170px 170px 1fr; gap: 16px; align-items: center; padding: 14px 0; border-bottom: 1px solid var(--rule); }}
.rung[data-frontier="y"] {{ background: linear-gradient(90deg, var(--amber-soft), transparent 70%); }}
.stage b {{ display: block; font: 600 18px/1.2 var(--display); }}
.stage span {{ font: 400 12px var(--mono); color: var(--muted); }}
.region {{ display: block; font: 500 11px var(--mono); color: var(--muted); letter-spacing: .04em; margin-bottom: 4px; }}
.pips {{ display: flex; align-items: center; gap: 4px; }}
.pip {{ width: 16px; height: 8px; border: 1px solid var(--accent); border-radius: 1px; }}
.pip.on {{ background: var(--accent); }}
.lv {{ margin-left: 8px; font-size: 14px; font-weight: 500; }}
.why {{ margin: 0; font-size: 14px; color: var(--muted); min-width: 0; }}
.frontier-note {{ font-size: 13px; color: var(--amber); font-family: var(--mono); }}
/* 표 */
.tablewrap {{ overflow-x: auto; border-top: 1px solid var(--ink); }}
table {{ border-collapse: collapse; width: 100%; min-width: 760px; font-size: 14px; }}
th {{ text-align: left; font: 500 11px var(--mono); letter-spacing: .05em; color: var(--muted); padding: 10px 8px; border-bottom: 1px solid var(--rule); }}
td {{ padding: 12px 8px; border-bottom: 1px solid var(--rule); vertical-align: top; }}
td small {{ display: block; color: var(--muted); font-size: 12px; margin-top: 3px; }}
.num {{ font: 500 15px var(--mono); font-variant-numeric: tabular-nums; white-space: nowrap; text-align: right; }}
.muted {{ color: var(--muted); }}
.ind {{ font: 500 12px var(--mono); width: 150px; }}
.ind small {{ font-family: var(--body); }}
.asof {{ font: 400 13px var(--mono); white-space: nowrap; }}
.idc code {{ color: var(--muted); }}
.src {{ font-size: 12px; color: var(--muted); margin-top: 6px; }}
.src a {{ color: var(--muted); }}
.grade {{ font: 500 10px var(--mono); margin-left: 4px; padding: 1px 4px; border: 1px solid currentColor; border-radius: 2px; }}
.gC {{ color: var(--amber); }}
.warn, .wk {{ font: 500 11px var(--mono); color: var(--amber); background: var(--amber-soft); padding: 2px 6px; border-radius: 2px; white-space: nowrap; }}
.gap {{ font-size: 13px; color: var(--muted); margin: 0; }}
/* 사건 */
.timeline {{ list-style: none; margin: 0; padding: 0; border-top: 1px solid var(--ink); }}
.timeline li {{ display: grid; grid-template-columns: 110px 1fr; gap: 16px; padding: 12px 0; border-bottom: 1px solid var(--rule); }}
.timeline time {{ font: 500 13px var(--mono); color: var(--muted); padding-top: 2px; }}
.timeline li > div {{ min-width: 0; }}
/* 해석 */
.interps {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 0 28px; border-top: 1px solid var(--ink); }}
.interp {{ padding: 16px 0; border-bottom: 1px solid var(--rule); display: grid; gap: 8px; align-content: start; }}
.interp header {{ display: flex; align-items: center; gap: 10px; flex-wrap: wrap; }}
.interp h3 {{ font: 600 16px/1.3 var(--body); flex: 1; }}
.interp header code {{ color: var(--muted); }}
.interp p {{ margin: 0; font-size: 15px; }}
.basis {{ font-size: 12px; color: var(--muted); }}
.dir {{ font: 500 11px var(--mono); padding: 2px 7px; border-radius: 2px; color: var(--panel); }}
.dir.up {{ background: var(--up); }} .dir.down {{ background: var(--down); }} .dir.flat {{ background: var(--flat); }}
.method {{ font-size: 13px; color: var(--muted); }}
.fstat {{ font: 500 11px var(--mono); border: 1px solid var(--accent); color: var(--accent); padding: 2px 6px; border-radius: 2px; white-space: nowrap; }}
footer {{ font-size: 13px; color: var(--muted); border-top: 1px solid var(--rule); padding-top: 18px; display: grid; gap: 6px; }}
:target {{ background: var(--accent-soft); }}
@media (max-width: 760px) {{
  .rung {{ grid-template-columns: 1fr 1fr; }}
  .rung .stage, .rung .why {{ grid-column: 1 / -1; }}
  .interps {{ grid-template-columns: 1fr; }}
  .timeline li {{ grid-template-columns: 1fr; gap: 4px; }}
}}
</style>
<main>
  <header class="narrow">
    <div class="eyebrow"><span>AI Future Customer Lab</span><span>Q1 · Consumer Decision Making</span><span>R1 기준 회차 · 2026-10-09</span></div>
    <h1>AI는 고객의 쇼핑을 어디까지 대신하고 있나</h1>
    <p class="question">고정 질문 v1.0 — {E(QUESTION)}</p>
  </header>

  <section class="answer-wrap narrow">
    <h2>한 줄 답</h2>
    <p class="answer">{E(ONE_LINE)}</p>
    <p class="sub">{E(SITE_ROLE)} {tags(SITE_ROLE_BASIS)}</p>
    <div>{tags(ONE_LINE_BASIS)}</div>
  </section>

  <section>
    <h2>단계별 판정 <small>실험 · 얼리어답터 · 확산 · 주류 4단계</small></h2>
    <div class="ladder">{''.join(ladder_rows)}</div>
    <p class="frontier-note">음영 = 현재 경계선 (추천 → 결정)</p>
  </section>

  <section>
    <h2>핵심 지표 <small>추적 지표 {len(filled)}/8개 값 확보</small></h2>
    <div class="tablewrap"><table>
      <thead><tr><th>추적 지표</th><th>내용 · 출처</th><th style="text-align:right">현재값</th><th style="text-align:right">이전값</th><th>기준 시점</th><th>기록</th></tr></thead>
      <tbody>{''.join(mrows)}</tbody></table></div>
    <p class="gap">이번 회차에 값을 채우지 못한 지표: {E(', '.join(empty_ind))}. 다음 간단 조사에서 우선 확인합니다.</p>
  </section>

  <section>
    <h2>주요 사건 <small>원문 확인된 것만</small></h2>
    <ul class="timeline">{erows}</ul>
  </section>

  <section>
    <h2>해석</h2>
    <div class="interps">{irows}</div>
  </section>

  <section>
    <h2>전망 <small>시점이 오면 확인 방법대로 판정합니다</small></h2>
    <div class="tablewrap"><table>
      <thead><tr><th>전망</th><th>확인 시점</th><th>확인 방법</th><th>상태</th><th>근거</th></tr></thead>
      <tbody>{frows}</tbody></table></div>
  </section>

  <section>
    <h2>미확인·경고 <small>Diff와 본문 판단에서 제외하거나 주의해서 쓴 기록</small></h2>
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
# 근거 번호 무결성
import re
bad = [i for i in re.findall(r'href="#(Q1-[A-Z]-\d{3})"', page) if i not in by]
print("article_r1.html 생성,", len(page), "bytes; 깨진 근거 링크:", bad or "없음")
sys.exit(1 if bad else 0)

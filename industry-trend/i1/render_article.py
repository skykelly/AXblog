"""records.jsonl → 기준 아티클 HTML (I1 R1).
순서: 한 줄 답 → 해석 → 주요 사건 → 전망 → 역량 원장 → 핵심 지표 → 미확인·경고
"""
import json, html, re, sys
from pathlib import Path

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT.parent.parent / "lib"))
from judge import gauge, criteria_panel, E as _E
recs = [json.loads(l) for l in (ROOT / "records.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
by = {r["id"]: r for r in recs}
E = html.escape
CSS = (ROOT.parent.parent / "lib" / "article.css").read_text(encoding="utf-8")

def tags(ids):
    return "".join(f'<a class="rid" href="#{E(i)}" title="{E(by[i]["statement"])}">{E(i)}</a>' for i in ids)
def para(text, ids): return f"<p>{E(text)} {tags(ids)}</p>"
def src_links(r):
    return " · ".join(f'<a href="{E(s["url"])}" target="_blank" rel="noopener">{E(s["publisher"])}</a><span class="grade g{E(s["grade"])}">{E(s["grade"])}</span>' for s in r.get("sources", []))

TITLE = "AI 기술의 경계는 어디까지 넓어졌나"
QUESTION = "AI가 새롭게 할 수 있게 된 일은 무엇이고, 기술의 경계는 어느 축에서 얼마나 넓어졌는가?"

# 1. 한 줄 답 ----------------------------------------------------------
ONE_LINE = ("2026년 10월 현재 AI는 사람이 반나절에서 하루 걸리는 소프트웨어 작업을 절반의 확률로 해내고(METR 기준 12~16시간 이상), 이 능력은 몇 시간짜리 업무를 끝까지 수행하는 에이전트로 이미 제품이 됐다. "
            "한계선은 ‘처음 보는 환경에서 스스로 규칙을 배우는 추론’(ARC-AGI-3 최고 30%)과 월드 모델·AI 과학 발견으로 옮겨갔고, 이 영역은 아직 시연·연구 단계다.")
ONE_LINE_BASIS = ["I1-I-001", "I1-I-002", "I1-I-005"]
ANSWER_ROWS = [
    ("새로 할 수 있게 된 일", "몇 시간짜리 일을 끝까지 맡기기. METR 작업 길이 최고치는 16시간 이상이고, OpenAI는 7월 시간 단위 프로젝트 에이전트 ChatGPT Work를 내놓았다.", ["I1-M-001", "I1-E-004"]),
    ("포화된 영역", "정형 추론 퍼즐(ARC-AGI-2 90.4%)과 100만 토큰 문맥은 프런티어 모델의 기본이 됐다.", ["I1-M-004", "I1-M-007"]),
    ("새 한계선", "처음 보는 상호작용 환경에서의 추론(ARC-AGI-3 30.2%), 1분으로 제한된 월드 모델, 검증을 기다리는 AI 수학 증명.", ["I1-M-003", "I1-E-001", "I1-E-007"]),
    ("경쟁 구도", "오픈 웨이트가 2.8조 파라미터(Kimi K3)로 바짝 추격하고, 9월 신모델은 성능만큼 가격 인하(Opus 5.5 −40%, GPT-6 Sol 반값)를 내세웠다.", ["I1-M-008", "I1-E-009"]),
    ("한국", "정부 프로젝트 평가에서 국가별 3위권(AAII 40점 이상 구간). LG K-엑사원 2.0(7,500억 파라미터)은 SKT·업스테이지와 함께 3차 단계로 올라갔다.", ["I1-M-010", "I1-E-008"]),
]
answer_rows = "".join(f'<div class="arow"><dt>{E(k)}</dt><dd>{E(v)} {tags(ids)}</dd></div>' for k, v, ids in ANSWER_ROWS)

# 2. 해석 --------------------------------------------------------------
NARRATIVE = [
    ("올해 가장 크게 움직인 축은 ‘얼마나 긴 일을 맡길 수 있나’다. METR 측정에서 Claude Opus 4.6은 사람 기준 약 12시간 걸리는 소프트웨어 작업을 절반의 확률로 해냈고, 4월 Mythos Preview는 최소 16시간으로 측정됐다. "
     "이 길이는 2023년 이후 약 131일마다 두 배가 되고 있다. 제품도 같은 방향이다. OpenAI는 7월 GPT-5.6과 함께, 앱과 파일을 넘나들며 몇 시간짜리 프로젝트를 수행하는 ChatGPT Work를 내놓았다.",
     ["I1-M-001", "I1-M-002", "I1-E-004", "I1-I-001"]),
    ("추론의 한계선은 다른 곳으로 옮겨갔다. Claude Opus 5는 정형 추론 퍼즐인 ARC-AGI-2에서 90.4%를 기록해 이 영역을 사실상 포화시켰다. "
     "반면 처음 보는 상호작용 환경에서 규칙을 스스로 익혀야 하는 ARC-AGI-3에서는 최고 점수가 30.2%다. 지금의 한계선은 ‘아는 문제를 푸는 능력’이 아니라 ‘새 환경에 적응하는 능력’에 있다.",
     ["I1-M-004", "I1-M-003", "I1-E-006", "I1-I-002"]),
    ("측정 도구가 모델을 따라가지 못하고 있다. METR는 16시간 이상은 현재 과제로 신뢰하기 어렵다고 밝혔고, 코딩 지수에서는 과적합 논란이 나왔다. "
     "같은 코딩 평가에서도 지표에 따라 1위가 바뀐다(SWE-Bench Pro에서는 Fable 5 80%, GPT-5.6 Sol 64.6%). 단일 벤치마크 순위로 기술 수준을 판정하기 어려워졌다.",
     ["I1-M-001", "I1-M-006", "I1-I-003"]),
    ("성능 우위는 짧아지고 있다. 중국 Moonshot은 2.8조 파라미터의 Kimi K3를 가중치까지 공개했고, 100만 토큰 문맥은 모든 프런티어 모델의 기본이 됐다. "
     "9월 Anthropic과 OpenAI의 신모델은 성능과 함께 가격 인하를 앞세웠다. 반면 Google은 Gemini 3 Pro 이후 1년 가까이 Pro급 신모델이 없고, Gemini 4를 준비 중이다.",
     ["I1-M-008", "I1-M-007", "I1-E-009", "I1-E-010", "I1-I-004"]),
    ("월드 모델과 AI 과학은 시연 단계다. Google의 Project Genie는 실시간으로 걸어 다닐 수 있는 세계를 만들지만 한 번에 60초까지이고, OpenAI가 발표한 에르되시 문제 3건의 진전은 독립 검증을 기다린다. "
     "하드웨어에서는 차세대 가속기용 HBM4(대역폭 2.8TB/s 이상)가 양산에 들어갔다. 한국은 정부 프로젝트 평가에서 국가별 3위권으로 평가됐다.",
     ["I1-E-001", "I1-E-007", "I1-M-009", "I1-M-010", "I1-I-005", "I1-I-006", "I1-I-007"]),
]
narrative_html = "".join(para(t, ids) for t, ids in NARRATIVE)
DIR = {"강화": "up", "약화": "down", "중립": "flat"}
irows = "".join(f"""<tr id="{E(r['id'])}"><td><span class="dir {DIR[r['direction']]}">{E(r['direction'])}</span></td>
  <td class="tgt">{E(r['target'])}</td><td>{E(r['statement'])}</td><td>{tags(r['basis'])}</td><td class="idc"><code>{E(r['id'])}</code></td></tr>"""
  for r in recs if r["type"] == "해석")

# 3. 주요 사건 (최신순) ------------------------------------------------
EVENTS_LEAD = ("6월부터 9월까지 석 달 사이에 Anthropic(Fable 5·Opus 5·Opus 5.5)과 OpenAI(GPT-5.6·GPT-6)가 각각 두세 번씩 프런티어 모델을 바꿨다. "
               "그 사이 오픈 웨이트(Kimi K3)가 추격했고, 프런티어 모델이 수출 통제 대상이 되는 첫 사례가 나왔다.")
events = sorted([r for r in recs if r["type"] == "사건" and r.get("verified")], key=lambda r: r["date"], reverse=True)
erows = "".join(f"""<li id="{E(r['id'])}"><time>{E(r['date'])}</time><div><b>{E(r['actor'])}</b> {E(r['statement'])}
  <div class="src">{src_links(r)} <code>{E(r['id'])}</code></div></div></li>""" for r in events)

# 4. 전망 --------------------------------------------------------------
FORECAST_LEAD = ("2027년 말을 기준으로 두 시나리오를 세웠다. 갈림길은 작업 길이의 배가 추세가 이어지는지, 그리고 새 한계선(새 환경 추론, 월드 모델, AI 과학)이 "
                 "시연을 넘어 제품과 검증된 성과로 들어서는지다.")
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

# 5. 역량 원장 -----------------------------------------------
ST = ["연구", "시연", "제품 출시", "일상 사용"]
ST_DEF = {
    "연구": ("논문·내부 결과로만 확인된다.", "공개 논문, 회사 발표(외부 접근 없음)"),
    "시연": ("공개 데모나 제한 접근(초대·대기자·연구 프리뷰·상위 요금제 한정)으로 확인된다.", "공개 데모, 제한 프리뷰"),
    "제품 출시": ("일반 사용자·개발자 누구나 쓸 수 있다. Compute는 양산 출하.", "가격·문서가 공개된 정식 제품"),
    "일상 사용": ("그 능력이 대규모 업무·서비스에 실제로 쓰이는 것이 확인된다. Compute는 데이터센터 주력 세대.", "이용량·매출·업무 비중 같은 사용 수치"),
}
LEDGER_LEAD = ("가장 앞선 축은 Agent·장시간 작업과 Reasoning으로, 일상 사용 단계에 들어섰다. Computer use, 장문 맥락, Compute는 제품 출시 단계이고, "
               "World Model은 시연, AI for Science는 연구 단계다. 다음 한계선은 그 축에서 아직 한 단계 아래에 있는 능력이다.")
# (축, 현재 위치, 잠정, 근거, 다음 한계선, 기록)
LEDGER = [
    ("Agent·장시간 작업", "일상 사용", True, "코딩 에이전트가 실무에 쓰임(Claude Code 연환산 25억 달러, Uber 커밋 코드 70% — I2). AI가 끝내는 작업 길이 12~16시간.",
     "하루 이상 걸리는 일을 끝까지 맡기기 (METR 16시간 이상은 측정 한계)", ["I1-M-001", "I1-M-002", "I1-E-004"]),
    ("Reasoning", "일상 사용", True, "추론 모델이 주력 대화형 서비스의 기본값(ChatGPT 주간 9억 명 — I2). 정형 추론 퍼즐 ARC-AGI-2 90.4%로 포화.",
     "처음 보는 환경에서 규칙 학습 — ARC-AGI-3 최고 30.2%", ["I1-M-004", "I1-M-003"]),
    ("Multimodal·Computer use", "제품 출시", False, "컴퓨터 조작 기능이 정식 제품으로 제공됨. 실제 업무 이용량은 공개되지 않음.",
     "사람 수준의 컴퓨터 조작 신뢰성 (OSWorld-Verified 83%, 자체 발표)", ["I1-M-005"]),
    ("Long context·Memory", "제품 출시", False, "100만 토큰 입력이 프런티어 모델의 표준 사양.",
     "세션을 넘는 장기 기억 — 아직 제한적", ["I1-M-007"]),
    ("World Model", "시연", False, "Project Genie가 미국 최상위 요금제 구독자에게만 열림, 한 번에 60초.",
     "60초 제한을 넘는 실시간 세계 생성·물리 일관성", ["I1-E-001"]),
    ("AI for Science", "연구", False, "에르되시 문제 진전은 미공개 내부 모델의 회사 발표이고 독립 검증 전.",
     "AI가 낸 수학·과학 결과의 독립 검증", ["I1-E-007"]),
    ("Compute", "제품 출시", False, "Vera Rubin용 HBM4 대량 생산·출하 시작. 데이터센터 주력 세대 전환은 진행 중.",
     "HBM4·차세대 가속기가 데이터센터 주력으로", ["I1-M-009", "I1-E-002"]),
]
def tip_st(v):
    d, ev = ST_DEF[v]
    return f"{v} — {d} 근거: {ev}."
criteria_html = criteria_panel([
    ("판정 단계: 기술 축의 성숙도", ["단계", "상태", "인정하는 근거"], [[gauge(ST, k), E(v[0]), E(v[1])] for k, v in ST_DEF.items()]),
], extra_rules=["다음 한계선은 그 축에서 현재 단계보다 아래(연구·시연)에 있는 능력이며, 한계선이 제품으로 나오면 원장에 새 한계선을 적는다."])
ledger_rows = "".join(f"""<div class="rung"><div class="stage"><b>{E(ax)}</b></div>
  <div class="lvcell"><span class="region">현재 위치</span>{gauge(ST, v, tip_st(v), pv)}</div>
  <p class="why">{E(why)}<br><b>다음 한계선</b> · {E(nx)} {tags(ids)}</p></div>""" for ax, v, pv, why, nx, ids in LEDGER)

# 6. 핵심 지표 ---------------------------------------------------------
INDICATOR_NAMES = {"I1-T1": "AI 작업 길이", "I1-T2": "새 환경 추론", "I1-T3": "코딩·컴퓨터 사용",
                   "I1-T4": "문맥 길이·기억", "I1-T5": "오픈 웨이트 수준", "I1-T6": "AI for Science 검증 성과",
                   "I1-T7": "AI 메모리·칩", "I1-T8": "한국 모델 수준"}
metrics = sorted([r for r in recs if r["type"] == "지표"], key=lambda r: (r["indicator"], -r["importance"]))
filled = {r["indicator"] for r in metrics if r.get("verified")}
empty_ind = [f"{k} {v}" for k, v in INDICATOR_NAMES.items() if k not in filled]
METRICS_LEAD = (f"추적 지표 8개 중 {len(filled)}개의 값을 원문으로 확인했다. {', '.join(empty_ind)}은 이번 회차에 수치를 찾지 못했다. "
                "벤치마크는 포화와 과적합이 빨라, 분기마다 지표를 점검하고 바꿀 때는 버전을 올린다. 기업 자체 발표 수치에는 주의 표시를 달았다. AI for Science는 독립 검증된 결과가 아직 없어 값을 비워 두었다.")
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

page = f"""<title>I1 AI 기술의 경계 R1</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans+KR:wght@400;500;600&family=Noto+Serif+KR:wght@600;800&display=swap">
<style>{CSS}</style>
<main>
  <header class="narrow">
    <div class="eyebrow"><span>AI Industry Trend</span><span>I1 · AI Technology &amp; Research</span><span>R1 기준 회차 · 2026-10-09</span></div>
    <h1>{E(TITLE)}</h1>
    <p class="question">고정 질문 v1.0 — {E(QUESTION)}</p>
  </header>
  <section class="answer-box"><h2>한 줄 답</h2>
    <p class="answer narrow">{E(ONE_LINE)} {tags(ONE_LINE_BASIS)}</p><dl class="arows">{answer_rows}</dl></section>
  <section><h2>해석</h2><div class="narrative">{narrative_html}</div>
    <div class="tablewrap"><table><thead><tr><th>방향</th><th>대상</th><th>해석</th><th>근거</th><th>기록</th></tr></thead><tbody>{irows}</tbody></table></div></section>
  <section><h2>주요 사건 <small>최신순 · 원문 확인된 것만</small></h2><p class="lead">{E(EVENTS_LEAD)}</p><ul class="timeline">{erows}</ul></section>
  <section><h2>전망 <small>2027년 말까지, 기술의 경계는 어디까지 넓어질까</small></h2><p class="lead">{E(FORECAST_LEAD)}</p>
    <div class="scens">{scen_html}</div>
    <h3 class="subhead">세부 판정 근거</h3>
    <p class="lead muted">각 세부 전망이 적중하거나 빗나갔을 때 어느 시나리오 쪽 신호인지 표시했다. 확인 시점이 오면 확인 방법대로 판정한다.</p>
    <div class="tablewrap"><table><thead><tr><th>세부 전망</th><th>확인 시점</th><th>적중 시</th><th>빗나갈 시</th><th>상태</th><th>근거</th></tr></thead><tbody>{frows}</tbody></table></div></section>
  <section><h2>역량 원장 <small>기술 축별 현재 위치와 다음 한계선</small></h2><p class="lead">{E(LEDGER_LEAD)}</p>
    {criteria_html}
    <div class="ladder mapgrid ledger">{ledger_rows}</div></section>
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
anchors = set(re.findall(r'id="(I1-[A-Z]-\d{3})"', page))
bad = sorted({i for i in re.findall(r'href="#(I1-[A-Z]-\d{3})"', page) if i not in anchors})
order = [page.index(f"<h2>{h}") for h in ("한 줄 답", "해석", "주요 사건", "전망", "역량 원장", "핵심 지표")]
print("article_r1.html 생성,", len(page), "bytes; 앵커 없는 근거 링크:", bad or "없음", "; 섹션 순서 정상:", order == sorted(order))
# ---------- 포털 신호: 판정 칩과 게이지를 판정 데이터에서 계산해 내보낸다
SIGNAL_CHIP = '2개 축 일상 사용, 5개 축 제품 이상'
SIGNAL_GAUGE = '기술 축 7개 중 제품 출시 이상'
SIGNAL_FRONTIER = '장기 기억·World Model'
signal = {"question": 'I1', "round": 1, "chip": SIGNAL_CHIP, "gauge": SIGNAL_GAUGE, "frontier": SIGNAL_FRONTIER,
          "on": sum(1 for r in LEDGER if ST.index(r[1]) >= ST.index("제품 출시")), "of": len(LEDGER)}
(ROOT / "signal_r1.json").write_text(json.dumps(signal, ensure_ascii=False, indent=1), encoding="utf-8")
print("signal_r1.json:", signal["chip"], f'{signal["on"]}/{signal["of"]}')
sys.exit(1 if bad or order != sorted(order) else 0)

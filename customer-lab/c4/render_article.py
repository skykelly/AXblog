"""records.jsonl → 기준 아티클 HTML (C4 R1).
순서: 한 줄 답 → 해석 → 주요 사건 → 전망 → 생활 영역별 자율 수준 → 핵심 지표 → 미확인·경고
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

TITLE = "집 안의 AI는 어디까지 스스로 하나"
QUESTION = "집 안에서 AI가 스스로 판단·실행하는 범위는 어디까지 왔으며, 고객은 어느 수준의 자율을 받아들이는가?"

# 1. 한 줄 답 ----------------------------------------------------------
ONE_LINE = ("2026년 10월 현재 집 안 AI는 ‘정해준 조건대로 알아서 하는 것(L2)’까지 제품이 됐고, 생성형 AI 허브가 상황을 판단해 여러 기기를 엮는 L3로 막 넘어가는 중이다. "
            "고객 수용은 한 칸 뒤에 있다. 한국에서는 AI 가전에 신중한 소비자(45.7%)가 처음으로 긍정 소비자(36.3%)를 넘었다.")
ONE_LINE_BASIS = ["C4-I-001", "C4-I-003", "C4-M-001"]
ANSWER_ROWS = [
    ("AI가 스스로 하는 것", "정해준 조건에 따른 자동 실행(L2). 씽큐 온은 습도가 높으면 제습기를 스스로 켜고, 로봇청소기는 부재 중 움직임을 감지해 사진을 보낸다.", ["C4-E-001", "C4-E-007"]),
    ("막 시작된 것", "상황 판단 실행(L3). 지난 1년 사이 Alexa+(미국 전체, 프라임 무료), Gemini for Home, 씽큐 온이 생성형 AI 허브로 나왔다. Amazon은 기존 기기 97%를 Alexa+로 바꿀 수 있다.", ["C4-E-005", "C4-E-002", "C4-M-008"]),
    ("아직 못 하는 것", "물리 작업 위임(L4). 1X NEO가 2만 달러에 첫해 물량 1만 대를 선판매했지만, LG CLOiD는 시연 단계이고 삼성 Ballie는 사실상 보류됐다.", ["C4-M-006", "C4-E-003", "C4-E-004"]),
    ("고객이 받아들이는 것", "사람이 조건을 정하거나 결과를 바로 확인하는 자율까지. 한국 소비자의 개인정보 우려는 58.2%로 가격 걱정과 같아졌고, 'AI가 스스로 판단해 불편하다'는 응답도 15.8%로 늘었다.", ["C4-M-002", "C4-M-003", "C4-I-005"]),
]
answer_rows = "".join(f'<div class="arow"><dt>{E(k)}</dt><dd>{E(v)} {tags(ids)}</dd></div>' for k, v, ids in ANSWER_ROWS)

# 2. 해석 --------------------------------------------------------------
NARRATIVE = [
    ("기술은 지난 1년 사이 한 단계 올라섰다. LG전자는 2025년 10월 생성형 AI 홈 허브 ‘씽큐 온’을 내놓았다. 여러 기기에 걸친 명령을 순서대로 실행하고, 센서로 습도가 높으면 제습기를 스스로 켠다. "
     "Google은 Gemini for Home을 미국부터 배포했고, Amazon은 2026년 2월 Alexa+를 미국 전체에 출시했다. 집 안 AI의 표준이 ‘앱 원격 조작’에서 ‘조건 자동화’로, 다시 ‘상황 판단 실행’의 입구로 옮겨가고 있다.",
     ["C4-E-001", "C4-E-002", "C4-E-005", "C4-I-001"]),
    ("허브 경쟁은 이미 깔린 기기 수에서 갈린다. Amazon은 그동안 판매한 Alexa 기기 6억 대 이상 가운데 97%가 Alexa+를 돌릴 수 있다고 밝혔고, 프라임 회원에게 무료로 풀었다. "
     "가전사 허브는 자사 가전을 깊게 제어하는 것이 강점이지만, 설치 기반은 따로 쌓아야 한다.",
     ["C4-M-008", "C4-E-005", "C4-I-006"]),
    ("물리 작업까지 맡기는 단계는 아직 시연과 선판매 사이에 있다. 1X는 가정용 휴머노이드 NEO의 첫해 물량 1만 대 이상을 예약 5일 만에 팔았고 4월 공장을 가동했다. "
     "반면 LG전자는 CES에서 냉장고에서 우유를 꺼내고 빨래를 개는 CLOiD를 보여줬을 뿐 가격과 출시일은 밝히지 않았고, 삼성전자는 Ballie를 내부 혁신 플랫폼으로 돌렸다.",
     ["C4-M-006", "C4-E-006", "C4-E-003", "C4-E-004", "C4-I-002"]),
    ("한국 소비자의 수용은 오히려 한 걸음 물러섰다. 오픈서베이 조사에서 AI 가전에 신중한 수용자가 45.7%로 긍정 수용자(36.3%)를 처음 넘었다. "
     "AI 기능을 써 본 사람은 생활가전 51%로 늘었지만, 직접 써 본 사람일수록 기대(88%)와 함께 우려(55.4%)도 커졌다.",
     ["C4-M-001", "C4-M-004", "C4-M-005", "C4-I-003"]),
    ("자율을 막는 것은 기술보다 데이터와 통제감이다. 개인정보 유출 우려는 58.2%로 1년 새 6.9%p 올라 가격 걱정(58.3%)과 같아졌고, ‘AI가 스스로 판단해 불편하다’는 응답도 15.8%로 늘었다. "
     "가전사가 부재 중 보안 알림처럼 ‘AI가 하고 사람이 확인하는’ 기능을 앞세우는 것도 이 때문이다.",
     ["C4-M-002", "C4-M-003", "C4-E-007", "C4-I-004", "C4-I-005"]),
]
narrative_html = "".join(para(t, ids) for t, ids in NARRATIVE)
DIR = {"강화": "up", "약화": "down", "중립": "flat"}
irows = "".join(f"""<tr id="{E(r['id'])}"><td><span class="dir {DIR[r['direction']]}">{E(r['direction'])}</span></td>
  <td class="tgt">{E(r['target'])}</td><td>{E(r['statement'])}</td><td>{tags(r['basis'])}</td><td class="idc"><code>{E(r['id'])}</code></td></tr>"""
  for r in recs if r["type"] == "해석")

# 3. 주요 사건 (최신순) ------------------------------------------------
EVENTS_LEAD = ("지난 1년의 사건은 두 갈래다. 생성형 AI 홈 허브는 한국(씽큐 온)과 미국(Gemini for Home, Alexa+)에서 실제로 출시됐다. "
               "홈 로봇은 스타트업(1X)이 생산에 들어간 반면, 국내 대형 가전사는 시연(LG CLOiD)과 보류(삼성 Ballie)로 갈렸다.")
events = sorted([r for r in recs if r["type"] == "사건" and r.get("verified")], key=lambda r: r["date"], reverse=True)
erows = "".join(f"""<li id="{E(r['id'])}"><time>{E(r['date'])}</time><div><b>{E(r['actor'])}</b> {E(r['statement'])}
  <div class="src">{src_links(r)} <code>{E(r['id'])}</code></div></div></li>""" for r in events)

# 4. 전망 --------------------------------------------------------------
FORECAST_LEAD = ("2027년 말을 기준으로 두 시나리오를 세웠다. 갈림길은 기술이 L3로 올라가는 속도에 고객 수용이 따라붙느냐, "
                 "그리고 홈 로봇이 시연을 넘어 일반 가정에 들어가느냐다.")
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

# 5. 생활 영역별 자율 수준 -----------------------------------------------
AL = ["L0", "L1", "L2", "L3", "L4"]
AL_NAME = {"L0": "수동", "L1": "제안", "L2": "조건 자동화", "L3": "상황 판단 실행", "L4": "위임"}
MAP_LEAD = ("모든 생활 영역에서 출시된 기술이 고객 수용보다 한 칸 앞서 있다. 장보기는 C1에서 본 것처럼 결제 위임이 막혀 있고, "
            "물리 작업은 L4 제품이 선판매 단계라 대부분의 가정은 로봇청소기 같은 L2에 머문다.")
MAP = [
    ("환경 제어", "Climate · Light", "L3", "L2", "생성형 허브가 복합 명령·센서 조건 실행. 고객은 조건 자동화까지 쓰고, AI 자체 판단에는 거부감 증가.", ["C4-E-001", "C4-E-005", "C4-M-003"]),
    ("보안·돌봄", "Security · Care", "L2", "L2", "움직임 감지 시 촬영·알림, 부재 중 자동화 루틴. 사람이 결과를 확인하는 형태라 수용이 쉬움.", ["C4-E-007"]),
    ("가사 물리 작업", "Chores", "L4", "L2", "휴머노이드 NEO 선판매·생산 시작, CLOiD 시연. 대부분의 가정은 로봇청소기 수준.", ["C4-M-006", "C4-E-003"]),
    ("장보기·소모품", "Replenishment", "L3", "L1", "설정 가격 자동 구매·반복 주문 기능은 있으나 결제 위임 수용은 낮음(C1 참조).", ["C4-M-009"]),
]
def lvl5(v):
    i = AL.index(v)
    return "".join(f'<span class="pip{" on" if k <= i else ""}"></span>' for k in range(5)) + f'<span class="lv">{E(v)} {E(AL_NAME[v])}</span>'
map_rows = "".join(f"""<div class="rung"><div class="stage"><b>{E(ko)}</b><span>{E(en)}</span></div>
  <div class="lvcell"><span class="region">출시된 기술</span><span class="pips">{lvl5(t)}</span></div>
  <div class="lvcell"><span class="region">고객 수용</span><span class="pips">{lvl5(c)}</span></div>
  <p class="why">{E(w)} {tags(ids)}</p></div>""" for ko, en, t, c, w, ids in MAP)
LEVEL_TABLE = "".join(f"<tr><td><code>{k}</code></td><td>{E(AL_NAME[k])}</td><td>{E(d)}</td></tr>" for k, d in [
    ("L0", "사람이 직접 또는 앱으로 원격 조작"), ("L1", "AI가 상태를 알리고 추천, 실행은 사람"), ("L2", "사람이 정한 조건·루틴대로 AI가 실행"),
    ("L3", "AI가 상황을 판단해 여러 기기를 엮어 실행, 사람은 사후 확인"), ("L4", "목표만 주면 물리 작업까지 스스로 수행")])

# 6. 핵심 지표 ---------------------------------------------------------
INDICATOR_NAMES = {"C4-K1": "생성형 AI 홈 허브 출시·보급", "C4-K2": "AI 허브가 닿는 설치 기반", "C4-K3": "홈 로봇 출시·판매",
                   "C4-K4": "AI 가전 기능 경험률", "C4-K5": "AI 자율에 대한 수용 태도", "C4-K6": "개인정보·통제 우려",
                   "C4-K7": "연결 표준 기기 수", "C4-K8": "AI 가전 판매 비중"}
metrics = sorted([r for r in recs if r["type"] == "지표"], key=lambda r: (r["indicator"], -r["importance"]))
filled = {r["indicator"] for r in metrics if r.get("verified")}
empty_ind = [f"{k} {v}" for k, v in INDICATOR_NAMES.items() if k not in filled]
METRICS_LEAD = (f"추적 지표 8개 중 {len(filled)}개의 값을 원문으로 확인했다. {', '.join(empty_ind)}은 이번 회차에 수치를 찾지 못했다. "
                "홈 허브 출시는 주요 사건으로 추적한다. AI 가전 판매 비중과 미국 스마트홈 AI 지불 의향은 조사 기간 밖 수치라 기준선으로만 쓴다.")
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

page = f"""<title>C4 집 안 AI 자율 수준 R1</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans+KR:wght@400;500;600&family=Noto+Serif+KR:wght@600;800&display=swap">
<style>{CSS}</style>
<main>
  <header class="narrow">
    <div class="eyebrow"><span>AI Future Customer Lab</span><span>C4 · Physical AI, Products &amp; Living</span><span>R1 기준 회차 · 2026-10-09</span></div>
    <h1>{E(TITLE)}</h1>
    <p class="question">고정 질문 v1.0 — {E(QUESTION)}</p>
  </header>
  <section class="answer-box"><h2>한 줄 답</h2>
    <p class="answer narrow">{E(ONE_LINE)} {tags(ONE_LINE_BASIS)}</p><dl class="arows">{answer_rows}</dl></section>
  <section><h2>해석</h2><div class="narrative">{narrative_html}</div>
    <div class="tablewrap"><table><thead><tr><th>방향</th><th>대상</th><th>해석</th><th>근거</th><th>기록</th></tr></thead><tbody>{irows}</tbody></table></div></section>
  <section><h2>주요 사건 <small>최신순 · 원문 확인된 것만</small></h2><p class="lead">{E(EVENTS_LEAD)}</p><ul class="timeline">{erows}</ul></section>
  <section><h2>전망 <small>2027년 말까지, 집 안 AI는 어디까지 스스로 하게 될까</small></h2><p class="lead">{E(FORECAST_LEAD)}</p>
    <div class="scens">{scen_html}</div>
    <h3 class="subhead">세부 판정 근거</h3>
    <p class="lead muted">각 세부 전망이 적중하거나 빗나갔을 때 어느 시나리오 쪽 신호인지 표시했다. 확인 시점이 오면 확인 방법대로 판정한다.</p>
    <div class="tablewrap"><table><thead><tr><th>세부 전망</th><th>확인 시점</th><th>적중 시</th><th>빗나갈 시</th><th>상태</th><th>근거</th></tr></thead><tbody>{frows}</tbody></table></div></section>
  <section><h2>생활 영역별 자율 수준 <small>출시된 기술 · 고객 수용 (L0~L4)</small></h2><p class="lead">{E(MAP_LEAD)}</p>
    <div class="ladder mapgrid auto">{map_rows}</div>
    <div class="tablewrap"><table class="levels"><thead><tr><th>수준</th><th>이름</th><th>뜻</th></tr></thead><tbody>{LEVEL_TABLE}</tbody></table></div></section>
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
anchors = set(re.findall(r'id="(C4-[A-Z]-\d{3})"', page))
bad = sorted({i for i in re.findall(r'href="#(C4-[A-Z]-\d{3})"', page) if i not in anchors})
order = [page.index(f"<h2>{h}") for h in ("한 줄 답", "해석", "주요 사건", "전망", "생활 영역별 자율 수준", "핵심 지표")]
print("article_r1.html 생성,", len(page), "bytes; 앵커 없는 근거 링크:", bad or "없음", "; 섹션 순서 정상:", order == sorted(order))
sys.exit(1 if bad or order != sorted(order) else 0)

"""records.jsonl → 기준 아티클 HTML (I3 R1).
순서: 한 줄 답 → 해석 → 주요 사건 → 전망 → 두 곡선과 층별 주도권 → 핵심 지표 → 미확인·경고
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

TITLE = "AI에 쏟아진 돈은 어디로 가고, 돌아오고 있나"
QUESTION = "AI 산업의 돈은 어디로 흐르고, 그 돈은 수익으로 돌아오고 있는가?"

# 1. 한 줄 답 ----------------------------------------------------------
ONE_LINE = ("2026년 10월 현재 AI에 들어가는 돈(빅테크 설비투자 연 7천억 달러 이상)은 아직 확인되는 AI 매출보다 몇 배 크지만, 매출이 투자보다 빨리 늘면서 간격이 좁혀지기 시작했다. "
            "지금 돈을 가장 확실하게 버는 곳은 칩·메모리(NVIDIA 매출총이익률 75%, SK하이닉스 영업이익률 76%)이고, 모델 층은 Anthropic이 흑자로 돌아선 반면 OpenAI는 큰 손실이 이어진다.")
ONE_LINE_BASIS = ["I3-I-001", "I3-I-002", "I3-I-003", "I3-I-004"]
ANSWER_ROWS = [
    ("돈이 들어가는 곳", "데이터센터와 칩. 빅테크 4사의 분기 설비투자가 1년 새 두 배 가까이 늘었고 Meta는 연간 계획을 1,450억 달러까지 올렸다.", ["I3-M-001", "I3-E-003"]),
    ("돈을 버는 곳", "칩·메모리. NVIDIA 데이터센터 매출 분기 890억 달러(+117%), SK하이닉스 분기 영업이익 60조 원.", ["I3-M-002", "I3-M-003"]),
    ("돌아오는 속도", "Anthropic 연환산 매출 650억 달러(1년 반 새 수십 배), Microsoft AI 매출 +123%, Google Cloud 수주 잔고 4,600억 달러.", ["I3-M-004", "I3-M-006"]),
    ("남은 위험", "OpenAI 2026년 손실 약 140억 달러, 모델 가격이 세대마다 40~50% 하락, 칩 회사가 고객에게 투자하는 순환 구조.", ["I3-M-005", "I3-M-007", "I3-I-006"]),
    ("한국", "메모리 호황의 최대 수혜국이자 GPU 26만 장 확보. 다만 이익은 메모리 공급에 몰려 있고 국내 모델·서비스 매출은 아직 보이지 않는다.", ["I3-M-003", "I3-M-008"]),
]
answer_rows = "".join(f'<div class="arow"><dt>{E(k)}</dt><dd>{E(v)} {tags(ids)}</dd></div>' for k, v, ids in ANSWER_ROWS)

# 2. 해석 --------------------------------------------------------------
NARRATIVE = [
    ("투자 곡선은 꺾이지 않았다. 2026년 1분기 설비투자는 Amazon 442억 달러, Alphabet 357억 달러, Microsoft 309억 달러로 1년 전보다 두 배 가까이 늘었고, "
     "Meta는 부품값 상승을 이유로 연간 계획을 1,250억~1,450억 달러로 올렸다. 4사의 올해 계획은 합쳐서 7천억 달러를 넘는다는 집계가 나온다.",
     ["I3-M-001", "I3-E-003", "I3-I-001"]),
    ("그 돈을 가장 먼저 이익으로 바꾼 곳은 칩과 메모리다. NVIDIA는 5~7월 분기 데이터센터 매출 890억 달러, 매출총이익률 75%를 냈고 다음 분기 1,080억 달러를 전망했다. "
     "SK하이닉스는 2분기 영업이익률 76.3%로 NVIDIA보다 높았고 HBM4 양산 출하를 시작했다. 공급이 수요를 따라가지 못하는 층이 가장 큰 몫을 가져간다.",
     ["I3-M-002", "I3-M-003", "I3-E-004", "I3-E-005", "I3-I-002"]),
    ("수익 곡선도 빠르게 올라온다. Anthropic의 연환산 매출은 2025년 초 약 10억 달러에서 2026년 7월 약 650억 달러로, OpenAI는 8월 약 400억 달러로 늘었다. "
     "Microsoft AI 매출은 연환산 370억 달러를 넘어 123% 늘었다. 매출 증가 속도가 투자 증가 속도보다 빨라 간격이 좁혀지기 시작했지만, 절대 규모는 아직 투자가 몇 배 크다.",
     ["I3-M-004", "I3-M-006", "I3-I-003"]),
    ("모델 층의 수익성은 갈렸다. Anthropic은 2분기 조정 영업이익 흑자로 돌아섰지만 OpenAI는 2026년 약 140억 달러 손실이 예상된다. "
     "9월 신모델은 이전 세대보다 40~50% 싸게 나와, 이용량은 늘리지만 모델 판매의 마진은 압박한다.",
     ["I3-M-005", "I3-M-007", "I3-E-007", "I3-I-004", "I3-I-005"]),
    ("돈의 흐름은 서로 얽히고 있다. NVIDIA는 OpenAI의 1,100억 달러 투자 유치에 300억 달러를 넣었고 Hugging Face를 약 130억 달러에 사들였다. 공급자가 고객의 수요를 자금으로 받치는 구조라, 수요가 독립적인지 따져 봐야 한다. "
     "한국은 SK하이닉스를 통해 이 흐름의 가장 큰 수혜를 받고 있고, NVIDIA GPU 26만 장으로 수요자 쪽 기반도 마련했다.",
     ["I3-E-002", "I3-E-006", "I3-M-008", "I3-I-006", "I3-I-007"]),
]
narrative_html = "".join(para(t, ids) for t, ids in NARRATIVE)
DIR = {"강화": "up", "약화": "down", "중립": "flat"}
irows = "".join(f"""<tr id="{E(r['id'])}"><td><span class="dir {DIR[r['direction']]}">{E(r['direction'])}</span></td>
  <td class="tgt">{E(r['target'])}</td><td>{E(r['statement'])}</td><td>{tags(r['basis'])}</td><td class="idc"><code>{E(r['id'])}</code></td></tr>"""
  for r in recs if r["type"] == "해석")

# 3. 주요 사건 (최신순) ------------------------------------------------
EVENTS_LEAD = ("8~9월에 흐름이 한꺼번에 드러났다. NVIDIA가 분기 매출 962억 달러를 발표한 직후 Hugging Face 인수를 밝혔고, 같은 달 Anthropic과 OpenAI는 이전보다 40~50% 싼 신모델을 냈다. "
               "그 앞에는 OpenAI의 1,100억 달러 투자 유치(2월)와 SK하이닉스의 사상 최대 실적(7월)이 있다.")
events = sorted([r for r in recs if r["type"] == "사건" and r.get("verified")], key=lambda r: r["date"], reverse=True)
erows = "".join(f"""<li id="{E(r['id'])}"><time>{E(r['date'])}</time><div><b>{E(r['actor'])}</b> {E(r['statement'])}
  <div class="src">{src_links(r)} <code>{E(r['id'])}</code></div></div></li>""" for r in events)

# 4. 전망 --------------------------------------------------------------
FORECAST_LEAD = ("2027년 말을 기준으로 두 시나리오를 세웠다. 갈림길은 모델 기업의 매출이 손실과 가격 인하를 이기고 계속 늘어나는지, "
                 "그리고 빅테크가 2027년에도 투자를 늘리는지다. 세부 전망 가운데 가장 이른 판정은 10~11월 SK하이닉스·NVIDIA 실적이다.")
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

# 5. 판정: 두 곡선과 층별 주도권 ----------------------------------
CURVE_LEAD = ("두 곡선을 같은 단위(연 달러)로 놓았다. 투자 곡선은 빅테크 4사의 2026년 설비투자 계획, 수익 곡선은 원문으로 확인된 AI 서비스 연환산 매출의 합이다. "
              "수익 쪽은 Microsoft AI 매출에 OpenAI 매출 일부가 겹칠 수 있어 상한값으로 읽어야 한다.")
CURVES = [
    ("inv", "투자 곡선", "빅테크 4사 설비투자", 7000, "7,000억 달러 이상 / 연", "1분기 전년 대비 +84~100% 이상", ["I3-M-001"]),
    ("rev", "수익 곡선", "Anthropic+OpenAI+MS AI 연환산", 1420, "약 1,420억 달러 / 연", "Anthropic 1년 반 새 수십 배, MS AI +123%", ["I3-M-004", "I3-M-006"]),
]
curve_html = "".join(f"""<div class="curve {c}"><div class="cl">{E(n)}<small>{E(s)}</small></div>
  <div><div class="bar"><span style="width:{max(v/70,18):.0f}%">{E(lbl)}</span></div><p class="why">증가 속도: {E(sp)} {tags(ids)}</p></div></div>""" for c, n, s, v, lbl, sp, ids in CURVES)
GAP_NOTE = "판정: 규모는 투자가 약 5배 크지만, 수익이 더 빨리 늘어 간격은 좁혀지기 시작했다 (R1 기준값)."
LAYER_LEAD = ("가치사슬 층마다 지금 돈을 가장 많이 가져가는 쪽과 그 자리가 굳어지는지 흔들리는지를 판정했다. 앱 층은 매출이 확인된 독립 앱 기업이 아직 없어 이번 회차에서는 비워 두었다.")
OWN = {"굳어짐": "brand", "경합": "contest", "흔들림": "agent", "자료 부족": "contest"}
LAYERS = [
    ("칩", "NVIDIA", "굳어짐", "데이터센터 매출 분기 890억 달러, 매출총이익률 75%, Vera Rubin 전면 양산", ["I3-M-002", "I3-E-005"]),
    ("메모리", "SK하이닉스·Micron", "굳어짐", "영업이익률 76~80%, HBM4 양산 출하, 2027년 물량 협상 순조", ["I3-M-003", "I3-E-004"]),
    ("클라우드·데이터센터", "Microsoft·AWS·Google", "경합", "모두 투자를 늘리는 중. MS AI +123%, AWS +28%, Google 수주 잔고 4,600억 달러", ["I3-M-006", "I3-M-001"]),
    ("모델", "Anthropic이 매출 선두", "흔들림", "Anthropic 650억 달러·흑자 vs OpenAI 400억 달러·손실, 가격은 세대마다 40~50% 하락", ["I3-M-004", "I3-M-005", "I3-M-007"]),
    ("도구·생태계", "NVIDIA의 수직 확장", "경합", "Hugging Face 인수로 칩 회사가 개발자 생태계로 내려옴", ["I3-E-006"]),
    ("앱", "—", "자료 부족", "독립 AI 앱 기업의 매출·이익 원문 미확보", []),
]
layer_rows = "".join(f"""<div class="rung"><div class="stage"><b>{E(l)}</b></div><div class="lvcell">{E(lead)}</div>
  <div class="lvcell"><span class="own {OWN[st]}">{E(st)}</span></div><p class="why">{E(w)} {tags(ids)}</p></div>""" for l, lead, st, w, ids in LAYERS)

# 6. 핵심 지표 ---------------------------------------------------------
INDICATOR_NAMES = {"I3-T1": "빅테크 AI 설비투자", "I3-T2": "데이터센터 가속기 매출", "I3-T3": "메모리 수익성",
                   "I3-T4": "프런티어 연구소 매출", "I3-T5": "프런티어 연구소 수익성", "I3-T6": "클라우드 AI 매출",
                   "I3-T7": "모델 가격", "I3-T8": "한국 AI 공급망·인프라"}
metrics = sorted([r for r in recs if r["type"] == "지표"], key=lambda r: (r["indicator"], -r["importance"]))
filled = {r["indicator"] for r in metrics if r.get("verified")}
empty_ind = [f"{k} {v}" for k, v in INDICATOR_NAMES.items() if k not in filled]
METRICS_LEAD = (f"추적 지표 8개 중 {len(filled)}개의 값을 원문으로 확인했다. "
                "상장사 실적은 공시 기준이고, OpenAI·Anthropic 같은 비상장사의 매출과 손익은 투자자 대상 잠정치를 보도한 것이라 주의 표시를 달았다. 빅테크 설비투자 합계는 집계 기관마다 차이가 있다.")
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

page = f"""<title>I3 AI 산업 돈의 흐름 R1</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans+KR:wght@400;500;600&family=Noto+Serif+KR:wght@600;800&display=swap">
<style>{CSS}</style>
<main>
  <header class="narrow">
    <div class="eyebrow"><span>AI Industry Trend</span><span>I3 · AI Industry &amp; Economics</span><span>R1 기준 회차 · 2026-10-09</span></div>
    <h1>{E(TITLE)}</h1>
    <p class="question">고정 질문 v1.0 — {E(QUESTION)}</p>
  </header>
  <section class="answer-box"><h2>한 줄 답</h2>
    <p class="answer narrow">{E(ONE_LINE)} {tags(ONE_LINE_BASIS)}</p><dl class="arows">{answer_rows}</dl></section>
  <section><h2>해석</h2><div class="narrative">{narrative_html}</div>
    <div class="tablewrap"><table><thead><tr><th>방향</th><th>대상</th><th>해석</th><th>근거</th><th>기록</th></tr></thead><tbody>{irows}</tbody></table></div></section>
  <section><h2>주요 사건 <small>최신순 · 원문 확인된 것만</small></h2><p class="lead">{E(EVENTS_LEAD)}</p><ul class="timeline">{erows}</ul></section>
  <section><h2>전망 <small>2027년 말까지, 수익이 투자를 따라잡을까</small></h2><p class="lead">{E(FORECAST_LEAD)}</p>
    <div class="scens">{scen_html}</div>
    <h3 class="subhead">세부 판정 근거</h3>
    <p class="lead muted">각 세부 전망이 적중하거나 빗나갔을 때 어느 시나리오 쪽 신호인지 표시했다. 확인 시점이 오면 확인 방법대로 판정한다.</p>
    <div class="tablewrap"><table><thead><tr><th>세부 전망</th><th>확인 시점</th><th>적중 시</th><th>빗나갈 시</th><th>상태</th><th>근거</th></tr></thead><tbody>{frows}</tbody></table></div></section>
  <section><h2>두 곡선과 층별 주도권 <small>투자 vs 수익 · 가치사슬 층별</small></h2><p class="lead">{E(CURVE_LEAD)}</p>
    <div class="curves">{curve_html}</div><p class="gapnote">{E(GAP_NOTE)}</p>
    <h3 class="subhead">가치사슬 층별 주도권</h3><p class="lead">{E(LAYER_LEAD)}</p>
    <div class="ladder mapgrid layers">{layer_rows}</div></section>
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
anchors = set(re.findall(r'id="(I3-[A-Z]-\d{3})"', page))
bad = sorted({i for i in re.findall(r'href="#(I3-[A-Z]-\d{3})"', page) if i not in anchors})
order = [page.index(f"<h2>{h}") for h in ("한 줄 답", "해석", "주요 사건", "전망", "두 곡선과 층별 주도권", "핵심 지표")]
print("article_r1.html 생성,", len(page), "bytes; 앵커 없는 근거 링크:", bad or "없음", "; 섹션 순서 정상:", order == sorted(order))
# ---------- 포털 신호: 판정 칩과 게이지를 판정 데이터에서 계산해 내보낸다
SIGNAL_CHIP = '투자 5배, 간격은 좁혀지는 중'
SIGNAL_GAUGE = '가치사슬 6개 층 중 주도권이 굳어진 층'
SIGNAL_FRONTIER = '모델 층'
signal = {"question": 'I3', "round": 1, "chip": SIGNAL_CHIP, "gauge": SIGNAL_GAUGE, "frontier": SIGNAL_FRONTIER,
          "on": sum(1 for r in LAYERS if r[2] == "굳어짐"), "of": len(LAYERS)}
(ROOT / "signal_r1.json").write_text(json.dumps(signal, ensure_ascii=False, indent=1), encoding="utf-8")
print("signal_r1.json:", signal["chip"], f'{signal["on"]}/{signal["of"]}')
sys.exit(1 if bad or order != sorted(order) else 0)

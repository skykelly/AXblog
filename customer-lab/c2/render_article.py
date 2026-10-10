"""records.jsonl → 기준 아티클 HTML (C2 R1).
순서: 한 줄 답 → 해석 → 주요 사건 → 전망 → 접점별 주도권 지도 → 핵심 지표 → 미확인·경고
"""
import json, html, re, sys
from pathlib import Path

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT.parent.parent / "lib"))
from judge import ADOPTION, adoption_tip, adoption_block, gauge, chip, criteria_panel
recs = [json.loads(l) for l in (ROOT / "records.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
by = {r["id"]: r for r in recs}
E = html.escape
CSS = (ROOT.parent.parent / "lib" / "article.css").read_text(encoding="utf-8")

def tags(ids):
    return "".join(f'<a class="rid" href="#{E(i)}" title="{E(by[i]["statement"])}">{E(i)}</a>' for i in ids)
def para(text, ids): return f"<p>{E(text)} {tags(ids)}</p>"
def src_links(r):
    return " · ".join(f'<a href="{E(s["url"])}" target="_blank" rel="noopener">{E(s["publisher"])}</a><span class="grade g{E(s["grade"])}">{E(s["grade"])}</span>' for s in r.get("sources", []))

TITLE = "AI 시대, 고객 접점의 주인은 누구인가"
QUESTION = "고객 여정(발견·상담·판매·관계) 중 어느 접점이 AI Agent로 넘어가고 있으며, 그 접점의 주도권은 브랜드·플랫폼·고객 Agent 중 누구에게 있는가?"

# 1. 한 줄 답 ----------------------------------------------------------
ONE_LINE = ("2026년 10월 현재 AI로 가장 많이 넘어간 접점은 발견과 상담이다. 발견은 플랫폼이 광고로 팔고, 상담은 고객이 직접 쓰는 범용 AI로 옮겨가 두 곳 모두 브랜드 손을 떠나고 있다. "
            "결제는 플랫폼·리테일러·고객 Agent가 다투는 중이고, 재구매·멤버십 같은 관계 접점만 아직 브랜드에 남아 있다.")
ONE_LINE_BASIS = ["C2-I-001", "C2-I-002", "C2-I-003"]
ANSWER_ROWS = [
    ("발견 → 플랫폼", "AI 답변 아래에 광고가 붙기 시작했다. ChatGPT는 1월 광고 시험을 발표했고, Amazon은 Rufus 안에 브랜드 스폰서 질문을 넣었다(누른 사람의 약 20%가 대화를 이어감).", ["C2-E-002", "C2-M-005"]),
    ("상담 → 고객 Agent", "고객은 기업 챗봇보다 ChatGPT·Gemini 같은 범용 AI를 약 3배 더 많이 쓴다. 다만 87%는 사람 상담원 연결을 필수로 본다.", ["C2-M-007", "C2-M-008"]),
    ("판매 → 경합", "Google은 AI Mode·Gemini 안 결제를 열었고, OpenAI는 결제를 리테일러에게 돌려줬다. Amazon과 Perplexity는 고객 Agent의 쇼핑 접근권을 놓고 소송 중이며, 8월 항소심은 Agent 쪽 손을 들었다.", ["C2-E-001", "C2-E-004", "C2-E-010"]),
    ("관계 → 브랜드 (잠정)", "주문·반품·멤버십은 아직 브랜드·리테일러 몫이다. 그러나 Rufus의 반복 구매 설정, 네이버의 멤버십 혜택 추천 계획처럼 플랫폼이 이 영역에도 들어오고 있다.", ["C2-E-011", "C2-E-008"]),
    ("한국", "네이버(검색·쇼핑)와 카카오(카톡·선물하기)가 발견부터 결제까지 자사 안에 묶고 있다. 브랜드는 두 플랫폼에 입점하는 방식으로 Agent 채널에 들어가게 된다.", ["C2-E-006", "C2-M-013", "C2-I-005"]),
]
answer_rows = "".join(f'<div class="arow"><dt>{E(k)}</dt><dd>{E(v)} {tags(ids)}</dd></div>' for k, v, ids in ANSWER_ROWS)

# 2. 해석 --------------------------------------------------------------
NARRATIVE = [
    ("발견 접점은 AI 답변 안으로 옮겨가고, 그 지면을 플랫폼이 광고로 팔기 시작했다. OpenAI는 1월 미국 무료·Go 요금제에서 답변 아래 ‘스폰서’ 카드 광고 시험을 발표했다. "
     "Amazon은 쇼핑 Agent Rufus 안에 브랜드 스폰서 질문을 넣었고, 광고 매출은 1분기 172억 달러로 24% 늘었다. 네이버도 4분기 AI탭 광고를 추진한다. "
     "브랜드가 AI 답변에 노출되려면 플랫폼에 비용을 내는 구조가 생기고 있다.",
     ["C2-E-002", "C2-M-005", "C2-M-004", "C2-E-007", "C2-I-001"]),
    ("상담 접점은 브랜드 밖으로 빠져나가고 있다. Gartner가 3,566명을 조사한 결과, 고객은 최근 서비스 상황에서 기업 챗봇보다 범용 AI를 약 3배 더 많이 썼고, "
     "생성형 AI 이용자의 58%는 AI에게 대신 일을 처리시킨 적이 있었다. 반면 87%는 사람 상담원 연결을 필수로 봤다. 브랜드 상담의 역할은 ‘AI 안내 후 사람 연결’로 좁혀지고 있다.",
     ["C2-M-007", "C2-M-009", "C2-M-008", "C2-I-002"]),
    ("판매 접점은 아직 주인이 정해지지 않았다. Google은 1월 Universal Commerce Protocol로 AI Mode와 Gemini 안 결제를 열었고, Shopify·Walmart·Target 등 20곳 이상이 참여했다. "
     "OpenAI는 3월 대화 안 결제를 접고 구매를 리테일러에게 돌려줬다. Amazon은 3월 Perplexity 쇼핑 Agent를 막는 가처분을 받아냈지만, 8월 항소심은 Agent가 사용자 지시로 움직인다며 이를 뒤집었다.",
     ["C2-E-001", "C2-M-010", "C2-E-004", "C2-E-003", "C2-E-010", "C2-I-003"]),
    ("지금 가장 앞선 쇼핑 Agent는 외부 범용 AI가 아니라 플랫폼 자체 Agent다. Amazon Rufus는 2025년 고객 3억 명이 썼고 연환산 약 120억 달러의 증분 매출을 냈다. "
     "2026년 1분기 월간 이용자는 115% 늘었고, Rufus 사용자는 구매를 끝낼 가능성이 60% 높다.",
     ["C2-M-001", "C2-M-002", "C2-M-003", "C2-I-004"]),
    ("한국은 대형 플랫폼이 Agent를 자사 안에 키우는 길로 가고 있다. 네이버 쇼핑 AI 에이전트 경유 거래액은 3개월 만에 2.7배가 됐고, 카카오는 카톡 안 검색·추천·결제 Agent를 하반기에 내겠다고 했다(연말 이용 가능자 3,100만 명 예상). "
     "결제 인프라는 아직 준비 단계로, 한국 카드사 6곳이 Visa의 Agent 결제 시험 프로그램에 들어갔지만 일반 소비자 상용 거래는 없다.",
     ["C2-M-013", "C2-E-006", "C2-M-012", "C2-M-011", "C2-I-005", "C2-I-006"]),
]
narrative_html = "".join(para(t, ids) for t, ids in NARRATIVE)
DIR = {"강화": "up", "약화": "down", "중립": "flat"}
irows = "".join(f"""<tr id="{E(r['id'])}"><td><span class="dir {DIR[r['direction']]}">{E(r['direction'])}</span></td>
  <td class="tgt">{E(r['target'])}</td><td>{E(r['statement'])}</td><td>{tags(r['basis'])}</td><td class="idc"><code>{E(r['id'])}</code></td></tr>"""
  for r in recs if r["type"] == "해석")

# 3. 주요 사건 (최신순) ------------------------------------------------
EVENTS_LEAD = ("1월에 플랫폼들이 AI 화면 안 결제(Google)와 광고(OpenAI)를 함께 열었다. 3월 이후에는 결제와 고객 접근권을 누가 쥐느냐를 두고 후퇴(OpenAI)와 법적 공방(Amazon·Perplexity)이 이어졌다. "
               "한국에서는 5~6월 카카오와 네이버가 자사 안 Agent 계획을 내놓았다.")
events = sorted([r for r in recs if r["type"] == "사건" and r.get("verified")], key=lambda r: r["date"], reverse=True)
erows = "".join(f"""<li id="{E(r['id'])}"><time>{E(r['date'])}</time><div><b>{E(r['actor'])}</b> {E(r['statement'])}
  <div class="src">{src_links(r)} <code>{E(r['id'])}</code></div></div></li>""" for r in events)

# 4. 전망 --------------------------------------------------------------
FORECAST_LEAD = ("브랜드 입장에서 2027년 말을 기준으로 두 시나리오를 세웠다. 갈림길은 두 가지다. 고객 Agent의 쇼핑 접근권이 법적으로 유지되는가, "
                 "그리고 한국 메신저·포털 Agent가 외부 브랜드몰에 결제를 열어주는가.")
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

# 5. 접점별 주도권 지도 -----------------------------------------------
LEVELS = ADOPTION
OWN = {"브랜드": "brand", "플랫폼": "platform", "고객 Agent": "agent", "경합": "contest"}
MAP_LEAD = ("AI로 가장 많이 넘어간 접점은 발견과 상담으로, 둘 다 얼리어답터 단계다. 판매와 관계는 실험 단계다. "
            "상담은 고객이 직접 쓰는 범용 AI가 기업 챗봇보다 3배 더 쓰여 고객 Agent 쪽으로 넘어갔고, 발견은 플랫폼이 쥐고 있다. "
            "판매는 주인을 다투는 중이고, 관계만 브랜드에 남아 있다. 한국은 판매까지 플랫폼 쪽으로 기울어 있다.")
# (접점, 영문, AI 이전 정도, 잠정, 주도권 글로벌, 한국, (글로벌 잠정, 한국 잠정), 근거 설명, 기록)
MAP = [
    ("발견", "Discovery", "얼리어답터", True, "플랫폼", "플랫폼", (True, True),
     "AI를 주 쇼핑 수단으로 쓰는 소비자는 6개국 평균 14%(C1). Rufus 이용 고객 3억 명, 답변 안 스폰서 질문. 한국은 네이버 쇼핑 에이전트 경유 거래액 3개월 새 2.7배.", ["C2-M-001", "C2-M-005", "C2-M-013", "C2-E-002"]),
    ("상담", "Consultation", "얼리어답터", True, "고객 Agent", "브랜드", (False, True),
     "고객 서비스 상황에서 범용 AI 이용이 기업 챗봇의 약 3배. AI에게 일을 대신 시켜 본 고객 58%(경험). 한국은 기업 AICC 중심으로 보이나 이용 데이터 없음.", ["C2-M-007", "C2-M-009", "C2-E-009"]),
    ("판매", "Commerce", "실험", True, "경합", "플랫폼", (True, True),
     "Google은 AI 안 결제 표준(UCP), OpenAI는 대화 안 결제를 접고 리테일러로, Amazon은 외부 Agent와 소송. AI 안 결제 거래 비중은 공개되지 않음. 한국은 네이버·카카오 자사 결제.", ["C2-E-001", "C2-E-004", "C2-E-010", "C2-E-006", "C2-M-010"]),
    ("관계", "Relationship", "실험", True, "브랜드", "브랜드", (True, True),
     "주문·반품·멤버십은 브랜드 몫. Rufus 반복 구매, 네이버 멤버십 혜택 추천이 진입 중이나 이용 규모는 공개되지 않음.", ["C2-E-011", "C2-E-008"]),
]
TOUCH_DEF = {
    "발견": ("살 만한 제품·브랜드를 처음 알게 되는 일", "제품을 처음 알게 된 경로 중 AI 답변·추천의 비율"),
    "상담": ("구매 전 질문·비교·확인", "구매 전 문의 가운데 직원·콜센터·브랜드 사이트 대신 AI가 답한 비율"),
    "판매": ("주문·결제", "AI 대화나 에이전트 안에서 주문·결제된 거래의 비중"),
    "관계": ("배송 조회·반품·A/S·멤버십·재구매", "구매 후 문의와 재구매 가운데 AI가 처리한 비율"),
}
OWN_DEF = {
    "브랜드": "브랜드 자체 AI·채널에서 처리된다.",
    "플랫폼": "검색·마켓플레이스·메신저(구글·아마존·네이버·카카오)의 AI에서 처리된다.",
    "고객 Agent": "고객이 쓰는 범용 AI(ChatGPT 등)가 브랜드·플랫폼을 대신 상대한다.",
    "경합": "가장 큰 쪽이 과반이 아니거나, 두 쪽이 비슷한 규모로 확인된다.",
}
def tip_touch(t):
    d, m = TOUCH_DEF[t]
    return f"{t} — AI로 넘어가는 일: {d}. 측정: {m}."
def own(o, prov):
    return chip(o, OWN[o], f"{o} — {OWN_DEF[o]}", prov)
criteria_html = criteria_panel([
    ("판정 항목: 네 접점", ["접점", "AI로 넘어가는 일", "측정하는 것"], [[f"<b>{E(k)}</b>", E(v[0]), E(v[1])] for k, v in TOUCH_DEF.items()]),
    adoption_block("축 1. AI 이전 정도"),
    ("축 2. 주도권: 그 접점의 AI 상호작용을 누가 가져가는가", ["판정", "정의"], [[own(k, False), E(v)] for k, v in OWN_DEF.items()]),
], extra_rules=["주도권은 이용량·거래액 같은 규모 근거로 가장 큰 쪽을 정한다. 출시 발표만 있으면 잠정으로 표시한다."])
map_rows = "".join(f"""<div class="rung"><div class="stage"><b tabindex="0" data-tip="{E(tip_touch(ko))}">{E(ko)}</b><span>{E(en)}</span></div>
  <div class="lvcell"><span class="region">AI 이전 정도</span>{gauge(LEVELS, l, adoption_tip(l), lp)}</div>
  <div class="lvcell"><span class="region">주도권 · 글로벌</span>{own(g, op[0])}</div>
  <div class="lvcell"><span class="region">주도권 · 한국</span>{own(k, op[1])}</div>
  <p class="why">{E(w)} {tags(ids)}</p></div>""" for ko, en, l, lp, g, k, op, w, ids in MAP)

# 6. 핵심 지표 ---------------------------------------------------------
INDICATOR_NAMES = {"C2-T1": "플랫폼 자체 쇼핑 Agent 규모", "C2-T2": "AI 답변 내 광고", "C2-T3": "Agent 거래 프로토콜·결제망",
                   "C2-T4": "상담 접점의 AI 이용 구조", "C2-T5": "브랜드 자체 AI Agent 도입", "C2-T6": "외부 Agent 차단·허용",
                   "C2-T7": "한국 메신저·포털 커머스 Agent", "C2-T8": "리테일 미디어 매출"}
metrics = sorted([r for r in recs if r["type"] == "지표"], key=lambda r: (r["indicator"], -r["importance"]))
filled = {r["indicator"] for r in metrics if r.get("verified")}
empty_ind = [f"{k} {v}" for k, v in INDICATOR_NAMES.items() if k not in filled]
METRICS_LEAD = (f"추적 지표 8개 중 {len(filled)}개의 값을 원문으로 확인했다. {', '.join(empty_ind)}은 이번 회차에 수치를 찾지 못했다. "
                "외부 Agent 차단·허용은 주요 사건(Amazon·Perplexity 소송)으로 추적하고, 브랜드 자체 Agent 도입 건수는 다음 간단 조사에서 집계한다.")
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

page = f"""<title>C2 고객 접점 주도권 R1</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans+KR:wght@400;500;600&family=Noto+Serif+KR:wght@600;800&display=swap">
<style>{CSS}</style>
<main>
  <header class="narrow">
    <div class="eyebrow"><span>AI Future Customer Lab</span><span>C2 · Customer Experience &amp; Commerce</span><span>R1 기준 회차 · 2026-10-09</span></div>
    <h1>{E(TITLE)}</h1>
    <p class="question">고정 질문 v1.0 — {E(QUESTION)}</p>
  </header>
  <section class="answer-box"><h2>한 줄 답</h2>
    <p class="answer narrow">{E(ONE_LINE)} {tags(ONE_LINE_BASIS)}</p><dl class="arows">{answer_rows}</dl></section>
  <section><h2>해석</h2><div class="narrative">{narrative_html}</div>
    <div class="tablewrap"><table><thead><tr><th>방향</th><th>대상</th><th>해석</th><th>근거</th><th>기록</th></tr></thead><tbody>{irows}</tbody></table></div></section>
  <section><h2>주요 사건 <small>최신순 · 원문 확인된 것만</small></h2><p class="lead">{E(EVENTS_LEAD)}</p><ul class="timeline">{erows}</ul></section>
  <section><h2>전망 <small>2027년 말까지, 고객 접점의 주인은 누가 될까</small></h2><p class="lead">{E(FORECAST_LEAD)}</p>
    <div class="scens">{scen_html}</div>
    <h3 class="subhead">세부 판정 근거</h3>
    <p class="lead muted">각 세부 전망이 적중하거나 빗나갔을 때 어느 시나리오 쪽 신호인지 표시했다. 확인 시점이 오면 확인 방법대로 판정한다.</p>
    <div class="tablewrap"><table><thead><tr><th>세부 전망</th><th>확인 시점</th><th>적중 시</th><th>빗나갈 시</th><th>상태</th><th>근거</th></tr></thead><tbody>{frows}</tbody></table></div></section>
  <section><h2>접점별 주도권 지도 <small>AI 이전 정도 · 누가 쥐고 있나</small></h2><p class="lead">{E(MAP_LEAD)}</p>
    {criteria_html}
    <div class="ladder mapgrid">{map_rows}</div>
    <p class="frontier-note">접점 이름과 판정에 마우스를 올리거나 누르면 기준이 보입니다</p></section>
  <section><h2>핵심 지표 <small>추적 지표 {len(filled)}/8개 값 확보</small></h2><p class="lead">{E(METRICS_LEAD)}</p>
    <div class="tablewrap"><table><thead><tr><th>추적 지표</th><th>내용 · 출처</th><th style="text-align:right">현재값</th><th>기준 시점</th><th>기록</th></tr></thead><tbody>{mrows}</tbody></table></div></section>
  <section><h2>미확인·경고 <small>본문 판단에서 빼거나 주의해서 쓴 기록</small></h2>
    <div class="tablewrap"><table><thead><tr><th>기록</th><th>구분</th><th>진술</th><th>사유</th></tr></thead><tbody>{wrows}</tbody></table></div></section>
  <footer>
    <span>이 글은 4유형 기록 {len(recs)}건(지표 {counts['지표']} · 사건 {counts['사건']} · 해석 {counts['해석']} · 전망 {counts['전망']})에서 생성했습니다. 문장 옆 번호를 누르면 해당 기록으로 이동합니다.</span>
    <span>주도권 구분: 브랜드 = 제조사·리테일러 자체 채널, 플랫폼 = 검색·AI 서비스·마켓플레이스·메신저, 고객 Agent = 고객이 직접 고르는 범용 AI·브라우저 Agent.</span>
    <span>출처 등급 A = 1차 조사·공식 발표, B = 주요 언론·2차 보도, C = 블로그·출처 불명(원문 확인 전까지 판단에 쓰지 않음).</span>
  </footer>
</main>
"""
(ROOT / "article_r1.html").write_text(page, encoding="utf-8")
anchors = set(re.findall(r'id="(C2-[A-Z]-\d{3})"', page))
bad = sorted({i for i in re.findall(r'href="#(C2-[A-Z]-\d{3})"', page) if i not in anchors})
order = [page.index(f"<h2>{h}") for h in ("한 줄 답", "해석", "주요 사건", "전망", "접점별 주도권 지도", "핵심 지표")]
print("article_r1.html 생성,", len(page), "bytes; 앵커 없는 근거 링크:", bad or "없음", "; 섹션 순서 정상:", order == sorted(order))
# ---------- 포털 신호: 판정 칩과 게이지를 판정 데이터에서 계산해 내보낸다
SIGNAL_CHIP = '상담은 고객 Agent, 발견은 플랫폼'
SIGNAL_GAUGE = '고객 접점 4곳 중 AI 이전이 얼리어답터 이상'
SIGNAL_FRONTIER = '상담 → 판매'
signal = {"question": 'C2', "round": 1, "chip": SIGNAL_CHIP, "gauge": SIGNAL_GAUGE, "frontier": SIGNAL_FRONTIER,
          "on": sum(1 for r in MAP if r[2] != "실험"), "of": len(MAP)}
# 포털 띠: 항목마다 단계(0~3)와 잠정 여부
signal["kind"] = "band"
signal["levels"] = list(LEVELS)
signal["items"] = [[r[0], LEVELS.index(r[2]), bool(r[3])] for r in MAP if True]
(ROOT / "signal_r1.json").write_text(json.dumps(signal, ensure_ascii=False, indent=1), encoding="utf-8")
print("signal_r1.json:", signal["chip"], f'{signal["on"]}/{signal["of"]}')
sys.exit(1 if bad or order != sorted(order) else 0)

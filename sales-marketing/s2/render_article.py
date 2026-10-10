"""records.jsonl → 기준 아티클 HTML (S2 R1).
순서: 한 줄 답 → 해석 → 주요 사건 → 전망 → 커머스 단계와 수익 배분 지도 → 핵심 지표 → 미확인·경고
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

TITLE = "AI는 어디까지 대신 사고, 그 돈은 누구에게 가나"
QUESTION = "에이전트 구매는 어느 단계까지 실제 거래가 됐고, 거래 한 건의 수익(수수료·광고·데이터)은 누구에게 가는가?"

# 1. 한 줄 답 ----------------------------------------------------------
ONE_LINE = ("2026년 10월 현재 에이전트 구매가 실제 거래로 자리 잡은 단계는 '탐색·비교'까지다. 유통사 에이전트가 이를 대규모로 운영하지만(Amazon Rufus 3억 명·증분 매출 120억 달러), ChatGPT 안 결제는 전환율이 사이트의 3분의 1에 그쳐 6개월 만에 접혔다. "
            "그래서 돈은 결제 수수료(4%)보다 에이전트 안 광고로 흐르고, 고객 관계와 데이터는 유통사가 지킨다. 한국은 네이버·카카오가 자기 플랫폼 안에서 결제 단계에 먼저 다가가고 있다.")
ONE_LINE_BASIS = ["S2-I-001", "S2-I-002", "S2-I-003", "S2-I-004", "S2-I-007"]
ANSWER_ROWS = [
    ("대규모 운영", "탐색·비교. Amazon Rufus 3억 명, Walmart 앱 이용자 절반이 Sparky 사용(주문액 +35%), Shopify AI 경유 주문 3배.", ["S2-M-001", "S2-M-002", "S2-M-003"]),
    ("시험·후퇴", "외부 AI 안 결제. ChatGPT Instant Checkout은 전환율이 사이트 이동의 3분의 1에 그쳐 2026년 3월 종료. 카드망 에이전트 결제는 수백 건 시험.", ["S2-M-004", "S2-E-004", "S2-M-005"]),
    ("수익", "AI 플랫폼의 결제 수수료 4% 시도는 외부 AI 결제가 접히며 후퇴했다. 대신 Rufus 안 광고·구글 AI Mode 할인 광고·네이버 AI탭 광고처럼 AI 지면 광고가 열리고 있다.", ["S2-M-007", "S2-E-006", "S2-E-002", "S2-E-009"]),
    ("고객·데이터", "유통사가 판매 당사자로 남고(구글 UCP), Walmart는 자기 에이전트를 ChatGPT 안에 넣어 장바구니를 묶었다.", ["S2-E-002", "S2-E-005"]),
    ("한국", "네이버 쇼핑 에이전트 거래액 3개월 새 2.7배, 하반기 장바구니·배송 추가. 카카오는 카톡 안 쿠팡이츠 주문·결제 에이전트 준비.", ["S2-M-010", "S2-E-008", "S2-E-011"]),
]
answer_rows = "".join(f'<div class="arow"><dt>{E(k)}</dt><dd>{E(v)} {tags(ids)}</dd></div>' for k, v, ids in ANSWER_ROWS)

# 2. 해석 --------------------------------------------------------------
NARRATIVE = [
    ("AI가 실제로 대신하는 일은 '고르기'까지다. Amazon Rufus는 2025년 고객 3억 명이 썼고 연환산 약 120억 달러의 증분 매출을 만들었다. Walmart 앱 이용자의 절반이 Sparky를 썼고, Sparky 이용자는 주문당 35% 더 쓴다. "
     "Shopify 상점의 AI 경유 주문은 1년 새 3배가 됐고, AI 유입의 절반이 상품 페이지로 바로 들어온다. 탐색과 비교는 이미 에이전트가 대규모로 하고 있다.",
     ["S2-M-001", "S2-M-002", "S2-M-003", "S2-I-001"]),
    ("결제 단계에서는 후퇴가 일어났다. OpenAI는 2025년 9월 ChatGPT 안에서 결제까지 끝내는 Instant Checkout을 냈지만, Walmart 기준 전환율이 사이트로 넘어가 사는 경우의 3분의 1에 그쳤고 상품 데이터도 부정확했다. 2026년 3월 기능은 접혔다. "
     "카드망의 에이전트 결제도 Visa 시범 수백 건, Mastercard 통제 환경 1건 수준이다. 대규모 실거래는 자기 앱 안에서 결제를 묶은 중국 Alipay(1억 2천만 건)에서만 나왔다.",
     ["S2-E-001", "S2-M-004", "S2-E-004", "S2-M-005", "S2-I-002", "S2-I-005"]),
    ("고객 관계와 데이터는 유통사가 지키는 쪽으로 정리되고 있다. 구글의 개방형 표준 UCP에서도 유통사가 판매 당사자로 남는다. Walmart는 외부 AI에 자리를 내주는 대신 자기 에이전트 Sparky를 ChatGPT와 Gemini 안에 넣고 장바구니를 자기 시스템과 동기화했다. "
     "외부 에이전트의 접근권은 법정으로 갔다. Amazon이 Perplexity 쇼핑 에이전트를 막는 가처분을 얻었지만, 항소심은 '에이전트는 사용자의 대리인'이라며 이를 뒤집었다.",
     ["S2-E-002", "S2-E-005", "S2-E-003", "S2-E-010", "S2-I-003", "S2-I-006"]),
    ("돈은 결제 수수료보다 광고로 흐른다. OpenAI가 매긴 4% 수수료는 마켓플레이스(8~15%)보다 낮았지만 결제가 접히며 기반이 약해졌다. 반대로 Amazon은 Rufus 대화 안 광고를 정식화했고(광고 매출 1분기 172억 달러, +24%), "
     "구글은 AI Mode 안 할인 광고를 시범 운영하며, 네이버는 4분기 AI탭 광고를 추진한다.",
     ["S2-M-007", "S2-M-008", "S2-E-006", "S2-E-002", "S2-E-009", "S2-I-004"]),
    ("한국은 외부 AI가 아니라 플랫폼 안에서 에이전트 커머스가 자란다. 네이버 쇼핑 에이전트는 6월 정식 출시 후 거래액이 3월 대비 2.7배가 됐고, 하반기 장바구니·배송을 더한다. "
     "카카오는 카톡 안에서 쿠팡이츠 주문·결제까지 끝내는 에이전트를 준비하고, 연말 이용 가능자를 3,100만 명으로 본다. 결제를 이미 가진 플랫폼이라 미국보다 먼저 결제 단계에 닿을 수 있다. 국내 카드사 5곳은 Visa 에이전트 결제 준비에 참여했다.",
     ["S2-M-010", "S2-E-008", "S2-E-011", "S2-M-011", "S2-E-007", "S2-I-007"]),
]
narrative_html = "".join(para(t, ids) for t, ids in NARRATIVE)
DIR = {"강화": "up", "약화": "down", "중립": "flat"}
irows = "".join(f"""<tr id="{E(r['id'])}"><td><span class="dir {DIR[r['direction']]}">{E(r['direction'])}</span></td>
  <td class="tgt">{E(r['target'])}</td><td>{E(r['statement'])}</td><td>{tags(r['basis'])}</td><td class="idc"><code>{E(r['id'])}</code></td></tr>"""
  for r in recs if r["type"] == "해석")

# 3. 주요 사건 (최신순) ------------------------------------------------
EVENTS_LEAD = ("3월이 분기점이었다. OpenAI가 ChatGPT 안 결제를 접은 같은 달, Walmart는 자기 에이전트를 ChatGPT 안에 넣었고 Amazon은 Rufus 안 광고를 정식화했다. "
               "여름에는 외부 에이전트의 접근권을 두고 항소심이 사용자 편을 들었고, 한국에서는 네이버·카카오가 플랫폼 안 에이전트로 결제 단계에 다가갔다.")
events = sorted([r for r in recs if r["type"] == "사건" and r.get("verified")], key=lambda r: r["date"], reverse=True)
erows = "".join(f"""<li id="{E(r['id'])}"><time>{E(r['date'])}</time><div><b>{E(r['actor'])}</b> {E(r['statement'])}
  <div class="src">{src_links(r)} <code>{E(r['id'])}</code></div></div></li>""" for r in events)

# 4. 전망 --------------------------------------------------------------
FORECAST_LEAD = ("2027년 말을 기준으로 두 시나리오를 세웠다. 갈림길은 에이전트가 결제 단계까지 실거래를 만드는지, 아니면 '고르기'에 머물고 수익이 광고로만 흐르는지다. "
                 "가장 이른 신호는 연말 카카오·네이버의 결제 연동 출시와 2027년 초 구글 AI Mode 결제의 해외 확대다.")
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

# 5. 커머스 단계와 수익 배분 지도 ----------------------------------
NA = '<span class="pips"><span class="lv muted">자료 없음</span></span>'
SG = ["계획", "시험", "정식 운영", "대규모 운영"]
SG_DEF = {
    "계획": "발표·로드맵만 있다.",
    "시험": "제한 지역·일부 이용자·파일럿으로 운영한다.",
    "정식 운영": "누구나 쓸 수 있다 (지역 한정이면 그 지역 기준).",
    "대규모 운영": "이용량·거래액이 공개되고, 그 단계 AI 기능 이용자 1억 명 또는 연 거래액 100억 달러 이상이다 (한국은 10분의 1).",
}
STEP_DEF = {
    "탐색·비교": "AI가 상품을 찾아 비교해 준다.",
    "장바구니·선택": "AI가 고른 상품을 장바구니에 담거나 옵션을 정한다.",
    "결제 (유통사 앱 안)": "유통사 자체 AI 안에서 주문·결제까지 끝난다.",
    "결제 (외부 AI 안)": "ChatGPT·Gemini 같은 외부 AI 화면 안에서 결제까지 끝난다.",
    "사후관리": "재주문·배송·반품·가격 추적을 AI가 맡는다.",
}
STAGE_LEAD = ("글로벌에서 대규모 운영에 이른 단계는 탐색·비교 하나다. 장바구니와 유통사 앱 안 결제는 정식 운영, 외부 AI 안 결제와 사후관리는 시험 단계다. "
              "한국은 탐색·비교가 정식 운영이고, 장바구니와 결제는 계획 단계다.")
# (단계, 글로벌, 글로벌 잠정, 한국, 한국 잠정, 근거, 기록)
STAGES = [
    ("탐색·비교", "대규모 운영", False, "정식 운영", False, "Rufus 이용 고객 3억 명·Shopify AI 경유 주문 3배 / 네이버 쇼핑 에이전트 정식 출시, 거래액 3개월 새 2.7배(절대 규모 미공개)", ["S2-M-001", "S2-M-003", "S2-M-010"]),
    ("장바구니·선택", "정식 운영", False, "계획", False, "Walmart Sparky가 ChatGPT 안에서 장바구니 동기화, Walmart 앱 이용자 절반이 Sparky 사용 경험 / 네이버 하반기 장바구니 추가 계획", ["S2-E-005", "S2-M-002", "S2-E-008"]),
    ("결제 (유통사 앱 안)", "정식 운영", False, "계획", False, "Rufus 설정 가격 자동 구매 / 카카오 쿠팡이츠 주문·결제 준비", ["S2-M-001", "S2-E-011"]),
    ("결제 (외부 AI 안)", "시험", False, None, False, "ChatGPT 대화 안 결제 종료, 구글 UCP 미국 한정, 카드망 에이전트 결제는 수백 건 규모", ["S2-E-004", "S2-E-002", "S2-M-005"]),
    ("사후관리", "시험", True, None, False, "Rufus 재주문·신제품 추적 설정, UCP가 사후관리까지 표준에 포함. 이용 규모 미공개", ["S2-M-001", "S2-E-002"]),
]
def tip_sg(v):
    return f"{v} — {SG_DEF[v]}"
def cell(v, pv):
    return NA if v is None else gauge(SG, v, tip_sg(v), pv)
stage_rows = "".join(f"""<div class="rung"><div class="stage"><b tabindex="0" data-tip="{E(d)} — {E(STEP_DEF[d])}">{E(d)}</b></div>
  <div class="lvcell"><span class="region">글로벌</span>{cell(g, gp)}</div>
  <div class="lvcell"><span class="region">한국</span>{cell(k, kp)}</div>
  <p class="why">{E(w)} {tags(ids)}</p></div>""" for d, g, gp, k, kp, w, ids in STAGES)
MAP_LEAD = ("거래 한 건에서 생기는 수익과 자산을 네 갈래로 나눴다. 광고만 AI 지면으로 일부 넘어가기 시작했고(Split), 거래 수수료·결제·고객 관계는 기존 주자가 그대로 가져간다(Hold). "
            "기존 주자의 몫이 줄어 AI 쪽으로 넘어간(Shift) 갈래는 아직 없다.")
FLOW = {"Hold": "brand", "Split": "agent", "Shift": "platform"}
FLOW_DEF = {
    "Hold": ("기존 주자 유지", "AI 쪽 몫이 공개되지 않았거나 그 수익의 5% 미만이고, 기존 주자 몫의 감소가 없다."),
    "Split": ("AI와 분할", "AI 쪽 몫이 5% 이상으로 확인되거나, AI 쪽 상품이 정식 운영 중이고 매출이 공개됐다. 기존 주자 몫의 감소는 아직 확인되지 않았다."),
    "Shift": ("AI로 이동", "기존 주자의 점유율·수수료율·매출 비중이 줄어든 것이 수치로 확인되고, 그 몫이 AI 쪽으로 간 근거가 있다."),
}
def flow(v, pv):
    k, d = FLOW_DEF[v]
    return chip(v, FLOW[v], f"{v} ({k}) — {d}", pv)
# (갈래, 지금 가져가는 쪽, 판정, 잠정, 근거, 기록)
MAP = [
    ("거래 수수료", "유통사·마켓플레이스", "Hold", False, "AI 플랫폼이 4% 수수료로 진입을 시도했지만 외부 AI 결제가 접히며 후퇴. 마켓플레이스 수수료(8~15%)는 유지", ["S2-M-007", "S2-E-004"]),
    ("광고", "유통사·AI 플랫폼", "Split", True, "Amazon Rufus 안 광고 정식 상품화, 구글 AI Mode 할인 광고 시범, 네이버 AI탭 광고 추진. AI 지면 광고 매출은 따로 공개되지 않음", ["S2-E-006", "S2-M-008", "S2-E-002", "S2-E-009"]),
    ("결제", "기존 카드망·간편결제", "Hold", False, "Visa·Mastercard가 에이전트 결제 표준을 선점, 실거래는 아직 소량. 중국은 Alipay가 자기 앱 안에서 대규모", ["S2-M-005", "S2-E-007"]),
    ("고객 관계·데이터", "유통사", "Hold", False, "UCP에서도 유통사가 판매 당사자, Walmart는 자기 에이전트로 장바구니 유지. 외부 에이전트 접근권은 소송 중", ["S2-E-002", "S2-E-005", "S2-E-010"]),
]
map_rows = "".join(f"""<div class="rung"><div class="stage"><b>{E(k)}</b></div><div class="lvcell">{E(who)}</div>
  <div class="lvcell">{flow(d, pv)}</div><p class="why">{E(w)} {tags(ids)}</p></div>""" for k, who, d, pv, w, ids in MAP)
criteria_html = criteria_panel([
    ("구매 단계", ["단계", "AI가 맡는 일"], [[f"<b>{E(k)}</b>", E(v)] for k, v in STEP_DEF.items()]),
    ("판정 단계: 커머스 운영", ["단계", "기준"], [[gauge(SG, k), E(v)] for k, v in SG_DEF.items()]),
    ("수익 배분: 수익이 AI 쪽으로 얼마나 넘어갔나", ["판정", "뜻", "확인 기준"], [[flow(k, False), E(v[0]), E(v[1])] for k, v in FLOW_DEF.items()]),
], extra_rules=["AI 쪽은 AI 대화·답변·에이전트 지면과 그 운영자다. 누가 운영하든 AI 지면에서 생긴 수익이면 AI 쪽으로 본다.",
                "글로벌은 유통사 자체 에이전트와 외부 AI 가운데 더 앞선 쪽을 기준으로 하고, 외부 AI 안 결제는 따로 한 줄로 둔다."])
# 6. 핵심 지표 ---------------------------------------------------------
INDICATOR_NAMES = {"S2-T1": "쇼핑 에이전트 이용 규모", "S2-T2": "AI 경유 주문·거래", "S2-T3": "에이전트 안 결제 전환",
                   "S2-T4": "에이전트 결제 거래 수", "S2-T5": "거래 수수료", "S2-T6": "AI 쇼핑 광고",
                   "S2-T7": "시장 규모 전망", "S2-T8": "한국 에이전트 커머스"}
metrics = sorted([r for r in recs if r["type"] == "지표"], key=lambda r: (r["indicator"], -r["importance"]))
filled = {r["indicator"] for r in metrics if r.get("verified")}
empty_ind = [f"{k} {v}" for k, v in INDICATOR_NAMES.items() if k not in filled]
METRICS_LEAD = (f"추적 지표 8개 중 {len(filled)}개의 값을 원문으로 확인했다. "
                "유통사 이용·증분 매출은 회사 자체 발표이고, Walmart 전환율은 한 기업의 수치이며, 2030년 시장 규모는 전망치라 주의 표시를 달았다.")
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

page = f"""<title>S2 AI 커머스 R1</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans+KR:wght@400;500;600&family=Noto+Serif+KR:wght@600;800&display=swap">
<style>{CSS}</style>
<main>
  <header class="narrow">
    <div class="eyebrow"><span>AI Sales &amp; Marketing</span><span>S2 · AI Commerce</span><span>R1 기준 회차 · 2026-10-09</span></div>
    <h1>{E(TITLE)}</h1>
    <p class="question">고정 질문 v1.0 — {E(QUESTION)}</p>
  </header>
  <section class="answer-box"><h2>한 줄 답</h2>
    <p class="answer narrow">{E(ONE_LINE)} {tags(ONE_LINE_BASIS)}</p><dl class="arows">{answer_rows}</dl></section>
  <section><h2>해석</h2><div class="narrative">{narrative_html}</div>
    <div class="tablewrap"><table><thead><tr><th>방향</th><th>대상</th><th>해석</th><th>근거</th><th>기록</th></tr></thead><tbody>{irows}</tbody></table></div></section>
  <section><h2>주요 사건 <small>최신순 · 원문 확인된 것만</small></h2><p class="lead">{E(EVENTS_LEAD)}</p><ul class="timeline">{erows}</ul></section>
  <section><h2>전망 <small>2027년 말까지, 에이전트가 결제까지 할까</small></h2><p class="lead">{E(FORECAST_LEAD)}</p>
    <div class="scens">{scen_html}</div>
    <h3 class="subhead">세부 판정 근거</h3>
    <p class="lead muted">각 세부 전망이 적중하거나 빗나갔을 때 어느 시나리오 쪽 신호인지 표시했다. 확인 시점이 오면 확인 방법대로 판정한다.</p>
    <div class="tablewrap"><table><thead><tr><th>세부 전망</th><th>확인 시점</th><th>적중 시</th><th>빗나갈 시</th><th>상태</th><th>근거</th></tr></thead><tbody>{frows}</tbody></table></div></section>
  <section><h2>커머스 단계와 수익 배분 지도 <small>글로벌과 한국 · 누가 가져가나</small></h2><p class="lead">{E(STAGE_LEAD)}</p>
    {criteria_html}
    <div class="ladder mapgrid auto">{stage_rows}</div>
    <h3 class="subhead">수익 배분 지도</h3><p class="lead">{E(MAP_LEAD)}</p>
    <div class="ladder mapgrid layers">{map_rows}</div></section>
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
anchors = set(re.findall(r'id="(S2-[A-Z]-\d{3})"', page))
bad = sorted({i for i in re.findall(r'href="#(S2-[A-Z]-\d{3})"', page) if i not in anchors})
order = [page.index(f"<h2>{h}") for h in ("한 줄 답", "해석", "주요 사건", "전망", "커머스 단계와 수익 배분 지도", "핵심 지표")]
print("article_r1.html 생성,", len(page), "bytes; 앵커 없는 근거 링크:", bad or "없음", "; 섹션 순서 정상:", order == sorted(order))
# ---------- 포털 신호: 판정 칩과 게이지를 판정 데이터에서 계산해 내보낸다
SIGNAL_CHIP = '탐색만 대규모, 결제는 시험'
SIGNAL_GAUGE = '커머스 5단계 중 대규모 운영(글로벌)'
SIGNAL_FRONTIER = '장바구니·결제'
signal = {"question": 'S2', "round": 1, "chip": SIGNAL_CHIP, "gauge": SIGNAL_GAUGE, "frontier": SIGNAL_FRONTIER,
          "on": sum(1 for r in STAGES if r[1] == "대규모 운영"), "of": len(STAGES)}
(ROOT / "signal_r1.json").write_text(json.dumps(signal, ensure_ascii=False, indent=1), encoding="utf-8")
print("signal_r1.json:", signal["chip"], f'{signal["on"]}/{signal["of"]}')
sys.exit(1 if bad or order != sorted(order) else 0)

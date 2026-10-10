"""records.jsonl → 기준 아티클 HTML (S4 R1).
순서: 한 줄 답 → 해석 → 주요 사건 → 전망 → 업무 단계별 역할 분담 → 핵심 지표 → 미확인·경고
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

TITLE = "AI는 영업과 고객 응대에서 무엇을 맡고, 사람은 무엇을 하나"
QUESTION = "AI는 리드 발굴·상담·제안·협상·고객 서비스 중 무엇을 수행하며, 사람과의 역할 분담은 어떻게 달라지는가?"

# 1. 한 줄 답 ----------------------------------------------------------
ONE_LINE = ("2026년 10월 현재 AI는 영업 과정의 양 끝을 맡는다. 앞단의 리드 발굴(셀러 54%가 AI 에이전트 사용)과 뒷단의 고객 서비스(Salesforce 문의 70%를 AI 단독 해결)는 AI가 주도하고, 가운데의 구매 상담·제안·협상은 사람이 주도한다. "
            "사람의 역할은 '정보 전달'에서 '검증과 예외 처리'로 바뀌고 있다. B2B 구매자의 69%가 AI 정보를 영업 담당자에게 확인받고 싶어 하고, 고객의 87%는 AI 응대에도 사람 연결을 요구한다.")
ONE_LINE_BASIS = ["S4-I-001", "S4-I-002", "S4-I-003"]
ANSWER_ROWS = [
    ("AI 주도", "리드 발굴(셀러 54% 에이전트 사용, B2B 팀 44% AI SDR)과 고객 서비스(Salesforce 70%, 토스뱅크 약 70% AI 처리).", ["S4-M-001", "S4-M-003", "S4-M-005", "S4-M-008"]),
    ("사람 주도·AI 보조", "B2B 구매 상담과 제안. 구매자 67%가 영업 없는 구매를 선호하지만 69%는 AI 정보를 사람에게 확인받고 싶어 한다.", ["S4-M-004"]),
    ("사람 단독", "판매 측 협상. AI 협상은 구매(조달) 측에서 먼저 자리 잡았다(Walmart 공급사 68% 타결, 2023년).", ["S4-M-007"]),
    ("성과와 긴장", "AI 해결률은 높지만 만족도는 사람의 절반(토스뱅크 36% vs 72%), 콜드 메일 회신율은 5.1%→3.4%로 하락.", ["S4-M-008", "S4-M-003"]),
    ("한국", "은행 콜센터 AI 처리율 20%대~70%로 편차, 국민은행 상담 인력 1,133명→869명.", ["S4-M-008", "S4-M-009"]),
]
answer_rows = "".join(f'<div class="arow"><dt>{E(k)}</dt><dd>{E(v)} {tags(ids)}</dd></div>' for k, v, ids in ANSWER_ROWS)

# 2. 해석 --------------------------------------------------------------
NARRATIVE = [
    ("AI는 영업 과정의 양 끝부터 맡고 있다. 영업 인력 4,050명 조사에서 54%가 AI 에이전트를 써 봤고, 그중 92%가 잠재 고객 발굴에 도움이 된다고 답했다. B2B 영업팀의 44%는 첫 연락을 맡는 AI SDR을 들였다. "
     "뒷단의 고객 서비스에서는 Salesforce 고객 지원 AI가 문의 430만 건의 70%를 사람 없이 해결했다.",
     ["S4-M-001", "S4-M-003", "S4-M-005", "S4-I-001"]),
    ("가운데는 여전히 사람의 몫이다. B2B 구매자의 67%가 영업 담당자 없는 구매를 선호하고 45%가 구매에 생성형 AI를 썼지만, 69%는 AI가 준 정보를 영업 담당자에게 확인받고 싶어 한다. "
     "AI와 영업 담당자 모두 오정보를 줄 수 있다고 보는 비율도 비슷하다(51% vs 49%). 영업 담당자의 역할은 정보를 전하는 사람에서 구매 결정을 검증하고 확신을 주는 사람으로 옮겨간다.",
     ["S4-M-004", "S4-E-004", "S4-I-003"]),
    ("AI가 맡은 양 끝에서는 성과와 품질 사이의 긴장이 보인다. 고객의 87%는 AI 응대에도 사람 연결이 필수라고 답했고, AI 덕에 응대가 쉬워졌다는 응답은 50%였다. "
     "리드 발굴에서는 AI가 발송량을 늘렸지만 콜드 메일 회신율은 5.1%에서 3.4%로 떨어졌다. AI의 첫 효과는 셀러의 행정 시간(근무 시간의 60%)을 덜어 판매 시간을 돌려주는 쪽이다.",
     ["S4-M-006", "S4-M-003", "S4-M-002", "S4-I-002", "S4-I-004", "S4-I-008"]),
    ("과금 방식도 역할 분담을 따라 바뀐다. Salesforce는 AI가 혼자 해결한 문의에만 돈을 받고 고객이 사람을 찾으면 과금하지 않는 '해결당 과금'을 7월 정식 출시했다. 해결률이 곧 공급자의 매출이 되는 구조다. "
     "협상은 판매 측에서는 아직 사람의 일이지만, 구매 측에서는 Walmart가 공급사 68%와 AI로 협상을 타결한 선례가 있다.",
     ["S4-E-005", "S4-M-007", "S4-I-005", "S4-I-007"]),
    ("한국 은행 콜센터는 AI 도입 수준의 편차가 크다. 농협은행 AI 처리율은 20%대에서 정체했지만, 국민은행은 41.3%로 올라서며 상담 인력이 1,133명에서 869명으로 줄었다. "
     "토스뱅크는 AI가 상담 10건 중 7건을 처리하지만 만족도는 36%로 기존 콜센터(72%)의 절반이다. 비용 절감과 서비스 품질 사이의 긴장이 가장 분명하게 드러나는 곳이다.",
     ["S4-M-008", "S4-M-009", "S4-E-003", "S4-I-006"]),
]
narrative_html = "".join(para(t, ids) for t, ids in NARRATIVE)
DIR = {"강화": "up", "약화": "down", "중립": "flat"}
irows = "".join(f"""<tr id="{E(r['id'])}"><td><span class="dir {DIR[r['direction']]}">{E(r['direction'])}</span></td>
  <td class="tgt">{E(r['target'])}</td><td>{E(r['statement'])}</td><td>{tags(r['basis'])}</td><td class="idc"><code>{E(r['id'])}</code></td></tr>"""
  for r in recs if r["type"] == "해석")

# 3. 주요 사건 (최신순) ------------------------------------------------
EVENTS_LEAD = ("올해 사건은 역할 분담의 양쪽을 보여 준다. Salesforce는 셀러 절반이 AI 에이전트를 쓴다고 밝히고 해결당 과금 응대 에이전트를 냈다. "
               "반대편에서 Gartner 조사들은 구매자와 고객이 여전히 사람을 원한다는 것을 보여 줬고, 한국에서는 은행 콜센터의 인력 감축과 만족도 하락이 국회 자료로 드러났다.")
events = sorted([r for r in recs if r["type"] == "사건" and r.get("verified")], key=lambda r: r["date"], reverse=True)
erows = "".join(f"""<li id="{E(r['id'])}"><time>{E(r['date'])}</time><div><b>{E(r['actor'])}</b> {E(r['statement'])}
  <div class="src">{src_links(r)} <code>{E(r['id'])}</code></div></div></li>""" for r in events)

# 4. 전망 --------------------------------------------------------------
FORECAST_LEAD = ("2027년 말을 기준으로 두 시나리오를 세웠다. 갈림길은 AI가 양 끝을 넘어 구매 상담·제안까지 주도하면서 품질도 사람에 가까워지는지, "
                 "아니면 단순 응대와 대량 발송의 비용 절감에 머물며 품질 불만이 쌓이는지다.")
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

# 5. 업무 단계별 역할 분담 지도 -------------------------------------
NA = '<span class="pips"><span class="lv muted">자료 없음</span></span>'
SG = ["사람 단독", "사람 주도·AI 보조", "AI 주도·사람 승인", "AI 단독"]
SG_DEF = {
    "사람 단독": "아래 기준에 모두 못 미친다.",
    "사람 주도·AI 보조": "해당 업무 담당자의 25% 이상이 AI 도구를 실제 업무에 쓴다.",
    "AI 주도·사람 승인": "해당 업무 건의 25% 이상을 AI가 먼저 처리하고, 사람이 승인·수정한다.",
    "AI 단독": "과반 건을 AI가 사람 승인 없이 끝내고, 사람이 처리하는 비중이 줄어든 것이 확인된다.",
}
STAGE_LEAD = ("AI가 가장 깊이 들어간 업무는 고객 서비스다. B2B는 AI가 문의 70%를 사람 없이 끝내는 사례가 나와 AI 단독(잠정)이고, B2C는 AI 주도·사람 승인 단계다. "
              "리드 발굴도 AI가 먼저 움직이지만, 구매 상담·제안·협상 같은 가운데 단계는 사람이 주도한다. 오른쪽에는 그 단계에서 사람이 새로 맡는 역할을 적었다.")
# (업무, B2B, B2B 잠정, B2C, B2C 잠정, 근거, 기록)
STAGES = [
    ("리드 발굴", "AI 주도·사람 승인", True, None, False, "B2B 영업팀 44%가 AI SDR 도입, 셀러 54%가 AI 에이전트 사용 경험(도입률이라 처리 비중은 미확인). 사람 → 대상 선정·메시지 승인, 반응 하락 관리", ["S4-M-001", "S4-M-003", "S4-E-001"]),
    ("구매 상담", "사람 주도·AI 보조", False, "AI 주도·사람 승인", True, "B2B 구매자 69%가 AI 정보를 영업 담당자에게 검증받기 원함 / B2C는 쇼핑 에이전트·외부 AI가 상담을 대신하기 시작(처리 비중 미공개). 사람 → 검증·확신 제공", ["S4-M-004", "S4-M-006"]),
    ("제안·견적", "사람 주도·AI 보조", True, None, False, "에이전트가 견적·이메일 작성을 도움(작성 시간 -36% 기대). 사람 → 맞춤 설계·내부 조율", ["S4-M-001"]),
    ("협상", "사람 단독", True, None, False, "판매 측 AI 협상 자료 없음. 구매 측은 AI 협상 선례(Walmart 공급사 68% 타결). 사람 → AI 구매 에이전트와의 협상 대비", ["S4-M-007"]),
    ("고객 서비스", "AI 단독", True, "AI 주도·사람 승인", False, "Salesforce 고객 지원 문의 430만 건 중 70%를 AI가 사람 없이 해결(한 기업 발표) / 국민은행 AI 처리율 41.3%·상담 인력 1,133명→869명, 토스뱅크 약 70%, 농협 21.7%로 정체. 사람 → 예외·복잡·감정 응대", ["S4-M-005", "S4-M-008", "S4-M-009", "S4-M-006"]),
]
def tip_sg(v):
    return f"{v} — {SG_DEF[v]}"
def cell(v, pv):
    return NA if v is None else gauge(SG, v, tip_sg(v), pv)
criteria_html = criteria_panel([
    ("판정 단계: 사람과 AI의 역할 분담", ["단계", "기준"], [[gauge(SG, k), E(v)] for k, v in SG_DEF.items()]),
], extra_rules=["고객 서비스에서 사람에게 넘기는 길이 열려 있어도 AI 단독을 막지 않는다. 기준은 개별 건마다 사람이 승인하는가다.",
                "AI 단독은 사람 처리 비중 감소가 필수다. 상담 인력 감소(기업 공시·고용 통계·업계 지표)까지 확인되면 확정하고, 한 기업의 발표뿐이면 잠정으로 둔다.",
                "AI 도구 도입률만 있으면 처리 비중을 알 수 없어 잠정으로 둔다."])
stage_rows = "".join(f"""<div class="rung"><div class="stage"><b>{E(d)}</b></div>
  <div class="lvcell"><span class="region">B2B</span>{cell(g, gp)}</div>
  <div class="lvcell"><span class="region">B2C</span>{cell(k, kp)}</div>
  <p class="why">{E(w)} {tags(ids)}</p></div>""" for d, g, gp, k, kp, w, ids in STAGES)
STAGE_NOTE = "판정: AI는 양 끝(리드 발굴·고객 서비스)을 주도하고, 가운데(상담·제안·협상)는 사람이 주도한다. 사람의 역할은 검증·예외·관계로 좁혀지며 깊어진다."

# 6. 핵심 지표 ---------------------------------------------------------
INDICATOR_NAMES = {"S4-T1": "영업 AI 에이전트 사용", "S4-T2": "AI SDR 도입·아웃바운드 반응", "S4-T3": "영업 시간 구조",
                   "S4-T4": "B2B 구매자의 선택", "S4-T5": "AI 응대 해결률", "S4-T6": "서비스 품질·사람 접근",
                   "S4-T7": "협상 AI", "S4-T8": "한국 AI 컨택센터"}
metrics = sorted([r for r in recs if r["type"] == "지표"], key=lambda r: (r["indicator"], -r["importance"]))
filled = {r["indicator"] for r in metrics if r.get("verified")}
empty_ind = [f"{k} {v}" for k, v in INDICATOR_NAMES.items() if k not in filled]
METRICS_LEAD = (f"추적 지표 8개 중 {len(filled)}개의 값을 원문으로 확인했다. "
                "업체 자체 해결률과 CRM 업체 조사는 주의 표시를, AI SDR 수치는 2차 인용 표시를, 협상 AI는 조사 기간 이전 기준선 표시를 달았다.")
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

page = f"""<title>S4 AI 영업·고객 응대 R1</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans+KR:wght@400;500;600&family=Noto+Serif+KR:wght@600;800&display=swap">
<style>{CSS}</style>
<main>
  <header class="narrow">
    <div class="eyebrow"><span>AI Sales &amp; Marketing</span><span>S4 · AI Sales &amp; Customer Service</span><span>R1 기준 회차 · 2026-10-09</span></div>
    <h1>{E(TITLE)}</h1>
    <p class="question">고정 질문 v1.0 — {E(QUESTION)}</p>
  </header>
  <section class="answer-box"><h2>한 줄 답</h2>
    <p class="answer narrow">{E(ONE_LINE)} {tags(ONE_LINE_BASIS)}</p><dl class="arows">{answer_rows}</dl></section>
  <section><h2>해석</h2><div class="narrative">{narrative_html}</div>
    <div class="tablewrap"><table><thead><tr><th>방향</th><th>대상</th><th>해석</th><th>근거</th><th>기록</th></tr></thead><tbody>{irows}</tbody></table></div></section>
  <section><h2>주요 사건 <small>최신순 · 원문 확인된 것만</small></h2><p class="lead">{E(EVENTS_LEAD)}</p><ul class="timeline">{erows}</ul></section>
  <section><h2>전망 <small>2027년 말까지, AI는 가운데까지 맡을까</small></h2><p class="lead">{E(FORECAST_LEAD)}</p>
    <div class="scens">{scen_html}</div>
    <h3 class="subhead">세부 판정 근거</h3>
    <p class="lead muted">각 세부 전망이 적중하거나 빗나갔을 때 어느 시나리오 쪽 신호인지 표시했다. 확인 시점이 오면 확인 방법대로 판정한다.</p>
    <div class="tablewrap"><table><thead><tr><th>세부 전망</th><th>확인 시점</th><th>적중 시</th><th>빗나갈 시</th><th>상태</th><th>근거</th></tr></thead><tbody>{frows}</tbody></table></div></section>
  <section><h2>업무 단계별 역할 분담 <small>B2B와 B2C · 사람의 새 역할</small></h2><p class="lead">{E(STAGE_LEAD)}</p>
    {criteria_html}
    <div class="ladder mapgrid auto">{stage_rows}</div><p class="gapnote">{E(STAGE_NOTE)}</p></section>
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
anchors = set(re.findall(r'id="(S4-[A-Z]-\d{3})"', page))
bad = sorted({i for i in re.findall(r'href="#(S4-[A-Z]-\d{3})"', page) if i not in anchors})
order = [page.index(f"<h2>{h}") for h in ("한 줄 답", "해석", "주요 사건", "전망", "업무 단계별 역할 분담", "핵심 지표")]
print("article_r1.html 생성,", len(page), "bytes; 앵커 없는 근거 링크:", bad or "없음", "; 섹션 순서 정상:", order == sorted(order))
# ---------- 포털 신호: 판정 칩과 게이지를 판정 데이터에서 계산해 내보낸다
SIGNAL_CHIP = '고객 서비스는 AI 단독, 가운데는 사람'
SIGNAL_GAUGE = '업무 단계 5개 중 AI 주도(B2B)'
SIGNAL_FRONTIER = '구매 상담·제안'
signal = {"question": 'S4', "round": 1, "chip": SIGNAL_CHIP, "gauge": SIGNAL_GAUGE, "frontier": SIGNAL_FRONTIER,
          "on": sum(1 for r in STAGES if r[1] in ("AI 주도·사람 승인", "AI 단독")), "of": len(STAGES)}
# 포털 띠: 항목마다 단계(0~3)와 잠정 여부
signal["kind"] = "band"
signal["levels"] = list(SG)
signal["items"] = [[r[0], SG.index(r[1]), bool(r[2])] for r in STAGES if r[1] is not None]
(ROOT / "signal_r1.json").write_text(json.dumps(signal, ensure_ascii=False, indent=1), encoding="utf-8")
print("signal_r1.json:", signal["chip"], f'{signal["on"]}/{signal["of"]}')
sys.exit(1 if bad or order != sorted(order) else 0)

"""records.jsonl → 기준 아티클 HTML (S1 R1).
순서: 한 줄 답 → 해석 → 주요 사건 → 전망 → 유입 저울과 인용 신호 순위 → 핵심 지표 → 미확인·경고
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

TITLE = "AI 답변 속 브랜드는 어떻게 보이고, 무엇이 노출을 가르나"
QUESTION = "AI 답변에서 브랜드는 얼마나 노출·인용되고, AI 유입은 검색 유입을 얼마나 대신하고 있으며, 노출을 가르는 신호는 무엇인가?"

# 1. 한 줄 답 ----------------------------------------------------------
ONE_LINE = ("2026년 10월 현재 AI 유입은 브랜드 사이트 방문의 1% 안팎으로, 검색에서 잃는 클릭(구글 검색의 68%가 클릭 없이 끝남)을 메우지 못한다. 다만 AI 유입의 전환율은 비AI보다 60% 높다. "
            "AI 답변 노출을 가르는 1순위 신호는 브랜드가 직접 쓴 글이 아니라 웹·커뮤니티의 제3자 언급이며, 기존 검색 순위가 그 기반이고, 구매 직전 질문에서는 상품 페이지가 인용의 약 40%를 차지한다.")
ONE_LINE_BASIS = ["S1-I-001", "S1-I-002", "S1-I-004", "S1-I-006"]
ANSWER_ROWS = [
    ("노출", "검색의 무대가 AI 답변으로 옮겨가는 중. 구글 검색의 약 25%에 AI 요약, AI Mode 월 10억 명. 다만 AI Mode가 검색에서 차지하는 비중은 0.34%.", ["S1-M-007", "S1-M-008", "S1-M-009"]),
    ("유입", "AI 유입은 전체 방문의 1.08%(ChatGPT가 87~92%). 19개월 새 9.9배로 늘었지만, 퍼블리셔의 구글 검색 유입은 1년 새 40% 줄었다.", ["S1-M-001", "S1-M-002", "S1-M-006"]),
    ("전환", "리테일 AI 유입의 전환율은 비AI보다 60% 높다. 1년 전에는 38% 낮았다.", ["S1-M-003"]),
    ("노출을 가르는 신호", "① 제3자 언급(상관 0.664, Reddit·YouTube 최다 인용) ② 검색 순위(구글 1페이지 0.65) ③ 질문 단계별 형식(비교 글·상품 페이지). 백링크·광고비는 약하다.", ["S1-M-012", "S1-M-013", "S1-M-010"]),
    ("한국", "네이버 AI 브리핑이 통합검색의 20%에 적용되고 연말까지 두 배 확대. 네이버 점유율은 64%로 8년 만의 최고.", ["S1-M-014", "S1-M-015"]),
]
answer_rows = "".join(f'<div class="arow"><dt>{E(k)}</dt><dd>{E(v)} {tags(ids)}</dd></div>' for k, v, ids in ANSWER_ROWS)

# 2. 해석 --------------------------------------------------------------
NARRATIVE = [
    ("브랜드가 보여야 하는 무대가 검색 결과 목록에서 AI 답변 안으로 옮겨가고 있다. 구글 검색의 약 4분의 1에 AI 요약이 뜨고(헬스케어는 절반), AI Mode 월간 이용자는 10억 명을 넘었다. "
     "다만 이용자 수와 실제 검색 비중은 다르다. 미국 구글 검색 중 AI Mode로 넘어간 비율은 0.34%로, 대부분의 AI 노출은 여전히 일반 검색 위에 얹힌 AI 요약에서 일어난다.",
     ["S1-M-007", "S1-M-008", "S1-M-009", "S1-I-003"]),
    ("유입의 저울은 아직 손실 쪽으로 기울어 있다. 구글 검색의 68%가 클릭 없이 끝나고, AI 요약이 뜨면 클릭률은 절반(15% → 8%)으로 떨어진다. 뉴스 퍼블리셔의 구글 검색 유입은 1년 새 40% 줄었다. "
     "반면 AI 유입은 기업 사이트 방문의 1.08%다. 19개월 새 9.9배로 빠르게 늘고 있지만, 잃는 클릭을 메우기에는 규모가 작다.",
     ["S1-M-004", "S1-M-005", "S1-M-006", "S1-M-001", "S1-M-002", "S1-I-001"]),
    ("AI 유입은 양보다 질이다. 미국 리테일 사이트에서 AI 유입의 전환율은 1년 전 비AI보다 38% 낮았지만 2026년 3월 42% 높아졌고, 7월에는 60% 높았다. "
     "AI 답변에서 비교를 마치고 들어오는 방문이라, 브랜드 사이트는 탐색의 첫 관문이 아니라 결정을 확인하는 마지막 관문이 된다.",
     ["S1-M-003", "S1-I-002"]),
    ("AI 답변 노출을 가르는 가장 강한 신호는 남이 브랜드를 말하는 것이다. 브랜드 7만 5천 개 분석에서 웹상의 브랜드 언급은 노출과 0.664로 연결됐지만, 백링크(0.218)와 광고비(0.215)는 약했다. "
     "AI 검색이 가장 많이 인용하는 도메인은 Reddit·YouTube이고, 전문 서비스 분야에서는 리스트형 비교 글 인용의 81%가 제3자 글이다. 그 아래 기반은 여전히 검색 순위다. 구글 1페이지 순위가 AI 답변의 브랜드 언급과 0.65로 연결됐다.",
     ["S1-M-012", "S1-M-011", "S1-M-010", "S1-M-013", "S1-I-004", "S1-I-005"]),
    ("질문 단계마다 인용되는 형식이 다르고, 노출을 돈으로 사는 길도 열리고 있다. 비교·검토 질문에서는 리스트형 글이 41%, 구매 직전에는 상품·카테고리 페이지가 약 40%를 차지한다. "
     "구글은 AI Mode 답변 속 광고를, OpenAI는 ChatGPT 답변 아래 광고를 시험 중이다. 한국은 네이버가 무대다. AI 브리핑이 검색의 20%에 적용되며 네이버 점유율이 64%로 올라섰고, 6월에는 대화형 AI탭이 정식 출시됐다.",
     ["S1-M-010", "S1-E-004", "S1-E-001", "S1-M-014", "S1-M-015", "S1-E-005", "S1-I-006", "S1-I-007", "S1-I-008"]),
]
narrative_html = "".join(para(t, ids) for t, ids in NARRATIVE)
DIR = {"강화": "up", "약화": "down", "중립": "flat"}
irows = "".join(f"""<tr id="{E(r['id'])}"><td><span class="dir {DIR[r['direction']]}">{E(r['direction'])}</span></td>
  <td class="tgt">{E(r['target'])}</td><td>{E(r['statement'])}</td><td>{tags(r['basis'])}</td><td class="idc"><code>{E(r['id'])}</code></td></tr>"""
  for r in recs if r["type"] == "해석")

# 3. 주요 사건 (최신순) ------------------------------------------------
EVENTS_LEAD = ("올해 사건은 두 갈래다. 구글(AI Mode 월 10억 명, 답변 속 광고 공개)과 OpenAI(ChatGPT 광고 시험)가 AI 답변을 광고 지면으로 만들고 있고, "
               "그 사이에 노출을 재는 측정 시장(Profound 유니콘)이 커졌다. 한국은 네이버가 AI 브리핑 확대와 AI탭 출시로 같은 흐름을 자기 생태계 안에서 만들고 있다.")
events = sorted([r for r in recs if r["type"] == "사건" and r.get("verified")], key=lambda r: r["date"], reverse=True)
erows = "".join(f"""<li id="{E(r['id'])}"><time>{E(r['date'])}</time><div><b>{E(r['actor'])}</b> {E(r['statement'])}
  <div class="src">{src_links(r)} <code>{E(r['id'])}</code></div></div></li>""" for r in events)

# 4. 전망 --------------------------------------------------------------
FORECAST_LEAD = ("브랜드 관점에서 2027년 말을 기준으로 두 시나리오를 세웠다. 갈림길은 AI 유입이 검색 손실을 일부라도 메우는 규모(3%)로 커지는지, "
                 "그리고 AI 답변 속 노출이 측정·광고로 관리 가능한 채널이 되는지, 아니면 플랫폼 안에서 닫혀 버리는지다.")
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

# 5. 유입 저울과 인용 신호 순위 ------------------------------------
SCALE_LEAD = ("브랜드 사이트 기준으로 검색에서 잃는 것과 AI에서 얻는 것을 나란히 놓았다. 출처마다 표본(검색 전체·퍼블리셔·리테일)이 달라 단순 합산은 하지 않았다.")
LOSE = [("구글 검색의 68%가 클릭 없이 끝남 (2년 새 +7.6%p)", ["S1-M-004"]),
        ("AI 요약이 뜨면 클릭률 15% → 8%", ["S1-M-005"]),
        ("퍼블리셔 구글 검색 유입 1년 새 -40.2%", ["S1-M-006"])]
GAIN = [("AI 유입 = 전체 방문의 1.08%", ["S1-M-001"]),
        ("AI 유입 19개월 새 9.9배 (이커머스 37배)", ["S1-M-002"]),
        ("리테일 AI 유입 전환율 비AI보다 +60%", ["S1-M-003"])]
def li(items): return "".join(f"<li>{E(t)} {tags(ids)}</li>" for t, ids in items)
scale_html = f"""<div class="balance"><div class="pan lose"><h4>검색에서 잃는 것</h4><ul>{li(LOSE)}</ul></div>
  <div class="pan gain"><h4>AI에서 얻는 것</h4><ul>{li(GAIN)}</ul></div></div>"""
SCALE_NOTE = "판정: 양은 손실이 크고, 질은 AI 유입이 높다. 저울은 아직 손실 쪽으로 기울어 있다 (R1 기준)."
SIGNAL_LEAD = ("AI 답변 노출과 인용에 영향이 큰 신호를 근거 강도 순으로 놓았다. 상관 연구는 인과를 뜻하지 않으며, 대부분 GEO·SEO 업체 연구라 주의 표시를 달았다. "
               "'브랜드 통제'는 브랜드가 직접 바꿀 수 있는 정도다.")
STR = {"강함": "brand", "중간": "platform", "약함": "contest"}
SIGNALS = [
    (1, "제3자 언급·평판", "강함", "간접", "브랜드 언급 상관 0.664, 최다 인용은 Reddit·YouTube, 전문 서비스 리스트형 인용의 81%가 제3자 글", ["S1-M-012", "S1-M-011", "S1-M-010"]),
    (2, "기존 검색 순위", "강함", "직접", "구글 1페이지 순위 상관 약 0.65, 빙 0.5~0.6", ["S1-M-013"]),
    (3, "질문 단계에 맞는 형식", "중간", "직접", "비교 질문은 리스트형 글 41%, 구매 직전은 상품·카테고리 페이지 약 40%", ["S1-M-010"]),
    (4, "브랜드 검색 수요", "중간", "간접", "브랜드 검색량 상관 0.392, 브랜드 앵커 0.527", ["S1-M-012"]),
    (5, "도메인 권위·백링크", "약함", "직접", "도메인 등급 0.326, 백링크 수 0.218", ["S1-M-012", "S1-M-013"]),
    (6, "광고비", "약함", "직접", "광고비 상관 0.215. 단, AI 답변 속 광고가 생기면 별도의 유료 경로가 된다", ["S1-M-012", "S1-E-004"]),
]
signal_rows = "".join(f"""<tr><td class="num">{n}</td><td class="tgt">{E(s)}</td><td><span class="own {STR[st]}">{E(st)}</span></td><td>{E(ctl)}</td><td>{E(w)} {tags(ids)}</td></tr>""" for n, s, st, ctl, w, ids in SIGNALS)

# 6. 핵심 지표 ---------------------------------------------------------
INDICATOR_NAMES = {"S1-T1": "AI 유입 비중", "S1-T2": "AI 유입 성장·플랫폼 점유", "S1-T3": "AI 유입 전환율",
                   "S1-T4": "검색 클릭 감소", "S1-T5": "AI 답변 노출 면적", "S1-T6": "인용 원천·형식·신호",
                   "S1-T7": "AI 검색 광고", "S1-T8": "한국 AI 검색"}
metrics = sorted([r for r in recs if r["type"] == "지표"], key=lambda r: (r["indicator"], -r["importance"]))
filled = {r["indicator"] for r in metrics if r.get("verified")}
empty_ind = [f"{k} {v}" for k, v in INDICATOR_NAMES.items() if k not in filled]
METRICS_LEAD = (f"추적 지표 8개 중 {len(filled)}개의 값을 원문으로 확인했다. S1-T7 AI 검색 광고는 수치 대신 사건(구글·OpenAI 발표)으로 추적한다. "
                "GEO·SEO 업체 연구는 이해관계자 자료로, 조사 기간 이전 연구(Ahrefs·Seer·Pew)는 기준선으로 표시했다.")
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

page = f"""<title>S1 AI 검색과 GEO R1</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans+KR:wght@400;500;600&family=Noto+Serif+KR:wght@600;800&display=swap">
<style>{CSS}</style>
<main>
  <header class="narrow">
    <div class="eyebrow"><span>AI Sales &amp; Marketing</span><span>S1 · AI Search &amp; GEO</span><span>R1 기준 회차 · 2026-10-09</span></div>
    <h1>{E(TITLE)}</h1>
    <p class="question">고정 질문 v1.0 — {E(QUESTION)}</p>
  </header>
  <section class="answer-box"><h2>한 줄 답</h2>
    <p class="answer narrow">{E(ONE_LINE)} {tags(ONE_LINE_BASIS)}</p><dl class="arows">{answer_rows}</dl></section>
  <section><h2>해석</h2><div class="narrative">{narrative_html}</div>
    <div class="tablewrap"><table><thead><tr><th>방향</th><th>대상</th><th>해석</th><th>근거</th><th>기록</th></tr></thead><tbody>{irows}</tbody></table></div></section>
  <section><h2>주요 사건 <small>최신순 · 원문 확인된 것만</small></h2><p class="lead">{E(EVENTS_LEAD)}</p><ul class="timeline">{erows}</ul></section>
  <section><h2>전망 <small>2027년 말까지, AI 유입은 검색 손실을 메울까</small></h2><p class="lead">{E(FORECAST_LEAD)}</p>
    <div class="scens">{scen_html}</div>
    <h3 class="subhead">세부 판정 근거</h3>
    <p class="lead muted">각 세부 전망이 적중하거나 빗나갔을 때 어느 시나리오 쪽 신호인지 표시했다. 확인 시점이 오면 확인 방법대로 판정한다.</p>
    <div class="tablewrap"><table><thead><tr><th>세부 전망</th><th>확인 시점</th><th>적중 시</th><th>빗나갈 시</th><th>상태</th><th>근거</th></tr></thead><tbody>{frows}</tbody></table></div></section>
  <section><h2>유입 저울과 인용 신호 순위 <small>브랜드 사이트 기준</small></h2><p class="lead">{E(SCALE_LEAD)}</p>
    {scale_html}<p class="gapnote">{E(SCALE_NOTE)}</p>
    <h3 class="subhead">AI 답변 노출을 가르는 신호 순위</h3><p class="lead">{E(SIGNAL_LEAD)}</p>
    <div class="tablewrap"><table><thead><tr><th style="white-space:nowrap">순위</th><th>신호</th><th style="white-space:nowrap">근거 강도</th><th style="white-space:nowrap">브랜드 통제</th><th>근거</th></tr></thead><tbody>{signal_rows}</tbody></table></div></section>
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
anchors = set(re.findall(r'id="(S1-[A-Z]-\d{3})"', page))
bad = sorted({i for i in re.findall(r'href="#(S1-[A-Z]-\d{3})"', page) if i not in anchors})
order = [page.index(f"<h2>{h}") for h in ("한 줄 답", "해석", "주요 사건", "전망", "유입 저울과 인용 신호 순위", "핵심 지표")]
print("article_r1.html 생성,", len(page), "bytes; 앵커 없는 근거 링크:", bad or "없음", "; 섹션 순서 정상:", order == sorted(order))
# ---------- 포털 신호: 판정 칩과 게이지를 판정 데이터에서 계산해 내보낸다
SIGNAL_CHIP = '저울은 손실 쪽'
SIGNAL_GAUGE = 'AI 노출 신호 6개 중 근거 강함'
SIGNAL_FRONTIER = 'AI 유입 1%대'
signal = {"question": 'S1', "round": 1, "chip": SIGNAL_CHIP, "gauge": SIGNAL_GAUGE, "frontier": SIGNAL_FRONTIER,
          "on": sum(1 for r in SIGNALS if r[2] == "강함"), "of": len(SIGNALS)}
# 포털 띠 대신 글자
signal["kind"] = "text"
signal["text"] = f"1위 신호 {SIGNALS[0][1]}"
(ROOT / "signal_r1.json").write_text(json.dumps(signal, ensure_ascii=False, indent=1), encoding="utf-8")
print("signal_r1.json:", signal["chip"], f'{signal["on"]}/{signal["of"]}')
sys.exit(1 if bad or order != sorted(order) else 0)

"""C3 R1 4유형 기록 생성 + 규칙 검증.
출력: q3/records.jsonl
"""
import json, sys
from pathlib import Path
from collections import Counter

R = "R1"
SRC = {
 "axios_graphite": {"url": "https://axios.com/2026/05/15/human-vs-ai-written-articles", "publisher": "Axios (Graphite 연구)", "date": "2026-05-15", "grade": "B"},
 "orig_amazon": {"url": "https://originality.ai/blog/amazon-ai-generated-reviews", "publisher": "Originality.ai 연구", "date": "2025-11-17", "grade": "B"},
 "decoder_dnr": {"url": "https://the-decoder.com/more-people-get-news-from-ai-chatbots-but-trust-remains-low/", "publisher": "The Decoder (Reuters Institute DNR 2026)", "date": "2026-06", "grade": "B"},
 "chartbeat": {"url": "https://www.relevantaudience.com/seo/chartbeat-google-search-publisher-traffic-down-40-percent/", "publisher": "Relevant Audience (Chartbeat 보고서 인용)", "date": "2026-09-25", "grade": "B"},
 "peec": {"url": "https://docs.peec.ai/research/most-cited-domains-in-ai-search", "publisher": "Peec 연구", "date": "2026-03", "grade": "B"},
 "iab": {"url": "https://www.iab.com/insights/the-ai-ad-gap-widens/", "publisher": "IAB·Sonata Insights", "date": "2026-01-15", "grade": "A"},
 "newsis_aiact": {"url": "https://www.newsis.com/view/NISX20260121_0003484769", "publisher": "뉴시스", "date": "2026-01-21", "grade": "B"},
 "newsis_ftc_kr": {"url": "https://mobile.newsis.com/view/NISX20260629_0003688360", "publisher": "뉴시스 (2026 하반기 달라지는 것)", "date": "2026-06-29", "grade": "B"},
 "mtn_reviews": {"url": "https://news.mtn.co.kr/news-detail/2026073016430716651", "publisher": "MTN", "date": "2026-07-30", "grade": "B"},
 "criteo_kr": {"url": "https://www.criteo.com/kr/wp-content/uploads/sites/7/2026/06/보도자료_크리테오-2026-커머스와-AI-트렌드-리포트-공개-for-Web.pdf", "publisher": "Criteo 보도자료", "date": "2026-06-10", "grade": "A"},
}
def src(*keys): return [dict(SRC[k], key=k) for k in keys]

base = dict(question="C3", question_version="v1.0", first_seen=R, last_seen=R, status="유효", replaces=None, check_flags=[])
records = []
def add(**kw):
    r = dict(base); r.update(kw); records.append(r)

# ---------- 지표 (M) ----------
add(id="C3-M-001", type="지표", indicator="C3-K1", importance=3, statement="2025년 말 새로 발행된 영문 웹 글의 50.9%가 주로 AI가 쓴 글로 판정됐다. 이 비중은 2025년 초부터 50% 안팎에서 멈춰 있다.",
    value=50.9, unit="%", as_of="2025-H2", region="GLOBAL(영문)", definition="Graphite, Common Crawl 55,400개 URL을 AI 탐지기 3종으로 판정", extra={"ai_share_1y_after_chatgpt": "35.9%", "ai_share_2y_after": "48%"},
    sources=src("axios_graphite"), verified=True, check_flags=["AI 탐지기 판정치 — 오탐 가능성"])
add(id="C3-M-002", type="지표", indicator="C3-K2", importance=2, statement="AI 생성 의심 Amazon 리뷰의 비중은 2022년 대비 약 400% 늘었고, 별점 1점·5점 리뷰가 2~4점 리뷰보다 AI로 판정될 가능성이 약 1.3배 높았다.",
    value=400, unit="% 증가(2022 대비)", as_of="2025-11", region="US", definition="Originality.ai, Amazon 리뷰 표본 약 2,000건 AI 탐지", sources=src("orig_amazon"), verified=True,
    check_flags=["탐지 업체 자체 연구 — 절대 비중은 미공개"])
add(id="C3-M-003", type="지표", indicator="C3-K3", importance=3, statement="AI 챗봇으로 매주 뉴스를 보는 사람은 7%에서 10%로 늘었고, 18~24세는 17%였다.",
    value=10, unit="%", as_of="2026", region="GLOBAL(45개 시장)", definition="Reuters Institute DNR 2026, 주간 AI 챗봇 뉴스 이용", prev_value=7, sources=src("decoder_dnr"), verified=True)
add(id="C3-M-004", type="지표", indicator="C3-K3", importance=3, statement="AI 챗봇이 전한 뉴스를 믿는다는 응답은 전체 20%였다. 챗봇 이용자는 44%, 비이용자는 17%였다.",
    value=20, unit="%", as_of="2026", region="GLOBAL", definition="Reuters Institute DNR 2026, AI 생성 뉴스 신뢰", extra={"users": "44%", "non_users": "17%"}, sources=src("decoder_dnr"), verified=True)
add(id="C3-M-005", type="지표", indicator="C3-K4", importance=3, statement="AI 챗봇에서 원문 출처를 자주 누른다는 응답은 4%로, 검색엔진(19%)·소셜미디어(17%)보다 크게 낮았다.",
    value=4, unit="%", as_of="2026", region="GLOBAL(27개 시장)", definition="Reuters Institute DNR 2026, 원문을 항상·자주 클릭", sources=src("decoder_dnr"), verified=True)
add(id="C3-M-006", type="지표", indicator="C3-K4", importance=3, statement="뉴스 퍼블리셔로 가는 Google 검색 유입은 2025년 7월~2026년 7월 사이 40.2% 줄었다(전년 감소폭 21.9%). AI 챗봇 유입은 전체 트래픽의 0.01%였다.",
    value=-40.2, unit="% YoY", as_of="2026-07", region="GLOBAL", definition="Chartbeat 퍼블리셔 네트워크, Google 검색 유입 변화", prev_value=-21.9, sources=src("chartbeat"), verified=True,
    check_flags=["Chartbeat 원보고서 미대조(2차 보도)"])
add(id="C3-M-007", type="지표", indicator="C3-K5", importance=3, statement="미국 AI 검색(ChatGPT·AI Mode·Gemini·Perplexity·AI Overviews)이 가장 많이 인용한 도메인은 Reddit, YouTube, LinkedIn, Wikipedia 순이었다.",
    value=1, unit="위(Reddit)", as_of="2026-03", region="US", definition="Peec, 인용 출처 3천만 건 분석", sources=src("peec"), verified=True)
add(id="C3-M-008", type="지표", indicator="C3-K6", importance=3, statement="AI로 만든 광고에 호감을 느끼는 미국 Gen Z·밀레니얼은 45%였지만, 광고주는 82%가 소비자가 호감을 느낄 것이라 봤다. 격차는 2024년 32%p에서 37%p로 벌어졌다.",
    value=45, unit="%", as_of="2025-10~2026-01", region="US", definition="IAB·Sonata Insights, 소비자 505명·광고 임원 104명", extra={"advertiser_belief": "82%", "gap_pp": 37, "gap_2024_pp": 32},
    sources=src("iab"), verified=True)
add(id="C3-M-009", type="지표", indicator="C3-K6", importance=2, statement="광고 임원의 83%가 제작에 AI를 쓴다고 답했고(2024년 60%), 소비자의 71%는 AI로 만든 광고를 본 적 있다고 생각했다(2024년 54%).",
    value=83, unit="%", as_of="2025-10~2026-01", region="US", definition="IAB, 광고 제작 AI 사용 기업 비율", prev_value=60, sources=src("iab"), verified=True)
add(id="C3-M-010", type="지표", indicator="C3-K8", importance=3, statement="AI 쇼핑에서 허위·편향 정보에 노출될까 우려하는 한국 소비자는 64%로 6개국 평균(52%)보다 높았다.",
    value=64, unit="%", as_of="2026-01~02", region="KR", definition="Criteo 6개국 설문(한국 1,107명)", sources=src("criteo_kr"), verified=True)

# ---------- 사건 (E) ----------
add(id="C3-E-001", type="사건", importance=3, statement="한국 AI 기본법이 시행됐다. 생성형 AI 결과물 표시 의무는 AI 사업자에게만 있고 일반 이용자는 대상이 아니며, 과태료(최대 3천만 원)는 최소 1년 유예된다.",
    date="2026-01-22", actor="정부(과기정통부)", sources=src("newsis_aiact"), verified=True)
add(id="C3-E-002", type="사건", importance=3, statement="공정위 개정 지침에 따라 온라인 쇼핑몰은 리뷰 작성 자격·게시 기간·평점·삭제 기준을 공개해야 하고, AI 가상인물을 쓴 추천·보증 광고에는 '가상인물' 표시가 필요해졌다.",
    date="2026-07-21", actor="공정거래위원회", sources=src("newsis_ftc_kr"), verified=True, check_flags=["가상인물 표시 시행일은 '하반기'로만 보도"])
add(id="C3-E-003", type="사건", importance=2, statement="무신사가 리뷰에 AI 생성 이미지 첨부를 금지하고 해당 적립금을 회수할 수 있게 약관을 바꿨다. 쿠팡은 가짜 리뷰는 제재하지만 AI 도움을 받은 리뷰는 막지 않는다.",
    date="2026-07", actor="무신사·쿠팡", sources=src("mtn_reviews"), verified=True)

# ---------- 해석 (I) ----------
add(id="C3-I-001", type="해석", importance=3, target="정보 생산", direction="강화",
    statement="정보 글의 생산은 이미 절반이 AI로 넘어갔고 그 수준에서 멈춰 있다. AI 글이 흔해질수록 사람의 실제 경험이 담긴 글이 상대적으로 귀해진다.",
    basis=["C3-M-001", "C3-M-007"])
add(id="C3-I-002", type="해석", importance=3, target="정보 전달 경로", direction="강화",
    statement="소비자는 원문 대신 AI 요약을 읽고, 원문으로 거의 넘어가지 않는다. 그 결과 정보를 만든 원천(언론·블로그·브랜드 사이트)으로 가는 유입이 빠르게 줄고 있다.",
    basis=["C3-M-003", "C3-M-005", "C3-M-006"])
add(id="C3-I-003", type="해석", importance=3, target="소비자 신뢰", direction="약화",
    statement="AI를 거친 정보의 이용은 늘지만 신뢰는 따라오지 않았다. AI 뉴스를 믿는 사람은 이용자 안에서만 절반 가까이이고 전체로는 5명 중 1명이며, AI 광고에 대한 젊은 층의 호감은 오히려 떨어졌다.",
    basis=["C3-M-004", "C3-M-008", "C3-M-009"])
add(id="C3-I-004", type="해석", importance=3, target="AI가 기대는 원천", direction="강화",
    statement="AI 답변은 브랜드 자체 콘텐츠보다 Reddit·YouTube 같은 사람의 경험담을 가장 많이 인용한다. AI 시대에도 구매 판단의 근거는 '다른 사람의 실제 경험'에 있다.",
    basis=["C3-M-007"])
add(id="C3-I-005", type="해석", importance=2, target="상품 리뷰", direction="약화",
    statement="AI가 쓴 리뷰가 빠르게 늘고, 특히 극단적인 별점에 몰린다. 플랫폼 대응은 금지(무신사)와 허용(쿠팡)으로 갈려 리뷰의 신뢰 기준이 흔들리고 있다.",
    basis=["C3-M-002", "C3-E-003"])
add(id="C3-I-006", type="해석", importance=2, target="한국 신뢰 장치", direction="중립",
    statement="한국은 표시 규제를 먼저 만들었지만 대상이 AI 사업자와 광고주에 한정되고 과태료도 유예됐다. 이용자가 쓰는 리뷰의 AI 사용은 플랫폼 자율에 맡겨져 있고, 소비자의 허위 정보 우려는 글로벌보다 높다.",
    basis=["C3-E-001", "C3-E-002", "C3-E-003", "C3-M-010"])

# ---------- 세부 전망 (F) ----------
add(id="C3-F-001", type="전망", importance=3, status="유효", forecast_status="진행 중",
    statement="Reuters Institute 2027 보고서에서 AI 챗봇이 전한 뉴스를 믿는다는 응답(전체)은 25%를 넘지 못할 것이다.", due="2027-06-30", condition="같은 문항이 반복될 경우",
    method="Reuters Institute Digital News Report 2027의 AI 뉴스 신뢰 수치 확인", basis=["C3-M-004"], result=None)
add(id="C3-F-002", type="전망", importance=3, status="유효", forecast_status="진행 중",
    statement="다음 Chartbeat 연간 집계에서도 퍼블리셔의 Google 검색 유입은 전년 대비 20% 이상 줄어 있을 것이다.", due="2027-09-30", condition="Chartbeat가 같은 지표를 공개할 경우",
    method="Chartbeat 2027 보고서의 Google 검색 유입 YoY 확인", basis=["C3-M-006"], result=None)
add(id="C3-F-003", type="전망", importance=2, status="유효", forecast_status="진행 중",
    statement="정부는 AI 기본법 표시 의무의 과태료 유예를 2027년 1월 22일 이후로 연장할 것이다.", due="2027-01-31", condition="없음",
    method="과기정통부 발표·시행령에서 과태료 유예 연장 여부 확인", basis=["C3-E-001"], result=None)
add(id="C3-F-004", type="전망", importance=2, status="유효", forecast_status="진행 중",
    statement="2027년 6월 말까지 쿠팡·네이버 중 1곳 이상이 AI 생성 리뷰를 표시하거나 제한하는 정책을 도입할 것이다.", due="2027-06-30", condition="없음",
    method="쿠팡·네이버 약관·공지·보도에서 AI 생성 리뷰 표시·제한 정책 확인", basis=["C3-E-003", "C3-E-002"], result=None)
add(id="C3-F-005", type="전망", importance=2, status="유효", forecast_status="진행 중",
    statement="IAB의 다음 조사에서 AI 광고에 호감을 느끼는 Gen Z·밀레니얼 비율은 45% 아래로 내려갈 것이다.", due="2027-03-31", condition="같은 조사가 반복될 경우",
    method="IAB AI 광고 인식 조사 차기 발표 확인", basis=["C3-M-008"], result=None)
add(id="C3-F-006", type="전망", importance=2, status="유효", forecast_status="진행 중",
    statement="Graphite의 다음 측정에서도 신규 영문 웹 글 중 AI 생성 비중은 60% 미만에 머물 것이다.", due="2027-06-30", condition="같은 방법으로 측정할 경우",
    method="Graphite 후속 연구의 AI 생성 비중 확인", basis=["C3-M-001"], result=None)

# ---------- 메인 질문 시나리오 (소비자 정보 생태계 관점) ----------
add(id="C3-F-101", type="전망", importance=3, status="유효", forecast_status="진행 중", scenario="낙관",
    statement="2027년 말까지 AI가 주된 정보 창구가 되면서도 신뢰 장치가 자리 잡는다. 표시 의무가 실제로 집행되고, 주요 쇼핑 플랫폼이 AI 리뷰를 표시·제한하며, AI 답변이 사람의 경험담을 출처와 함께 보여준다. AI가 전한 정보를 믿는 사람이 4명 중 1명을 넘는다.",
    milestones=[
        {"by": "2027-01", "text": "AI 기본법 표시 의무 과태료 유예 종료, 집행 시작"},
        {"by": "2027-06", "text": "쿠팡·네이버 중 1곳 이상 AI 리뷰 표시·제한 도입"},
        {"by": "2027-06", "text": "AI 뉴스 신뢰(전체) 25% 이상"}],
    due="2027-12-31", condition="AI 생성 허위 정보가 대형 소비자 피해로 번지지 않을 경우",
    method="세 가지 중 두 가지 이상 충족 시 적중: (1) Reuters Institute 보고서의 AI 뉴스 신뢰(전체) 25% 이상 (2) 국내 주요 쇼핑 플랫폼의 AI 리뷰 표시·제한 정책 도입 (3) AI 기본법 표시 의무의 과태료 집행 시작",
    basis=["C3-M-004", "C3-E-001", "C3-E-002", "C3-E-003"],
    signposts=[{"id": "C3-F-001", "on_miss": "낙관", "on_hit": "비관"}, {"id": "C3-F-003", "on_miss": "낙관", "on_hit": "비관"}, {"id": "C3-F-004", "on_hit": "낙관", "on_miss": "비관"},
               {"id": "C3-F-006", "on_hit": "낙관"}], result=None)
add(id="C3-F-102", type="전망", importance=3, status="유효", forecast_status="진행 중", scenario="비관",
    statement="2027년 말까지 AI 콘텐츠가 리뷰와 광고까지 뒤덮지만 신뢰 장치는 늦어진다. 원천 매체로 가는 유입이 계속 줄어 사람이 쓴 정보의 공급이 마르고, 소비자는 AI 답변을 쓰되 믿지 않아 지인·커뮤니티·매장 체험으로 다시 확인한다.",
    milestones=[
        {"by": "2027-01", "text": "AI 기본법 과태료 유예 연장"},
        {"by": "2027-03", "text": "젊은 층의 AI 광고 호감 45% 아래로 하락"},
        {"by": "2027-09", "text": "퍼블리셔 Google 검색 유입 감소가 연 20% 이상 지속"}],
    due="2027-12-31", condition="없음",
    method="낙관 시나리오의 판정 조건 세 가지 중 하나 이하만 충족 시 적중",
    basis=["C3-M-006", "C3-M-005", "C3-M-008", "C3-M-002", "C3-M-010"],
    signposts=[{"id": "C3-F-002", "on_hit": "비관"}, {"id": "C3-F-005", "on_hit": "비관"}], result=None)

# ---------- 검증 ----------
ids = {r["id"] for r in records}
_t = {r["id"]: r["type"] for r in records}
_v = {r["id"]: r.get("verified") for r in records}
facts = {i for i, t in _t.items() if t in ("지표", "사건")}
errs = []
for r in records:
    if r["type"] in ("지표", "사건") and (not r.get("sources") or not all(s.get("url") for s in r["sources"])):
        errs.append(f"{r['id']}: 원문 링크 없음")
    if r["type"] == "해석":
        if not set(r.get("basis", [])) & facts: errs.append(f"{r['id']}: 사실 기록 연결 없음")
        if r.get("direction") not in ("강화", "약화", "중립"): errs.append(f"{r['id']}: 방향 값 오류")
    if r["type"] == "전망":
        for f in ("due", "method", "basis"):
            if not r.get(f): errs.append(f"{r['id']}: {f} 없음")
        if not set(r["basis"]) & facts: errs.append(f"{r['id']}: 해석에만 기대는 전망")
    for sp in r.get("signposts", []):
        if _t.get(sp["id"]) != "전망": errs.append(f"{r['id']}: 판정 신호 {sp['id']}가 세부 전망이 아님")
    if r.get("scenario") and r["scenario"] not in ("낙관", "비관"): errs.append(f"{r['id']}: 시나리오 값 오류")
    for b in r.get("basis", []):
        if b not in ids: errs.append(f"{r['id']}: 존재하지 않는 근거 {b}")
        elif r["type"] in ("해석", "전망") and b in facts and not _v[b]: errs.append(f"{r['id']}: 원문 미확인 기록 {b}을 근거로 씀")
if len(ids) != len(records): errs.append("중복 ID")

with open(Path(__file__).parent / "records.jsonl", "w", encoding="utf-8") as f:
    for r in records: f.write(json.dumps(r, ensure_ascii=False) + "\n")

print("기록 수:", len(records), dict(Counter(r["type"] for r in records)))
print("원문 미확인 사실:", [r["id"] for r in records if r["type"] in ("지표", "사건") and not r.get("verified")])
inds = {r.get("indicator") for r in records if r["type"] == "지표" and r.get("verified")}
print("값 채워진 추적 지표:", sorted(inds), f"{len(inds)}/8")
print("검증 오류:", errs or "없음")
sys.exit(1 if errs else 0)

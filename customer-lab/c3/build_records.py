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
add(id="C3-M-001", type="지표", indicator="C3-T1", importance=3, statement="2025년 말 새로 발행된 영문 웹 글의 50.9%가 주로 AI가 쓴 글로 판정됐다. 이 비중은 2025년 초부터 50% 안팎에서 멈춰 있다.",
    value=50.9, unit="%", as_of="2025-H2", region="GLOBAL(영문)", definition="Graphite, Common Crawl 55,400개 URL을 AI 탐지기 3종으로 판정", extra={"ai_share_1y_after_chatgpt": "35.9%", "ai_share_2y_after": "48%"},
    sources=src("axios_graphite"), verified=True, check_flags=["AI 탐지기 판정치 — 오탐 가능성"])
add(id="C3-M-002", type="지표", indicator="C3-T2", importance=2, statement="AI 생성 의심 Amazon 리뷰의 비중은 2022년 대비 약 400% 늘었고, 별점 1점·5점 리뷰가 2~4점 리뷰보다 AI로 판정될 가능성이 약 1.3배 높았다.",
    value=400, unit="% 증가(2022 대비)", as_of="2025-11", region="US", definition="Originality.ai, Amazon 리뷰 표본 약 2,000건 AI 탐지", sources=src("orig_amazon"), verified=True,
    check_flags=["탐지 업체 자체 연구 — 절대 비중은 미공개"])
add(id="C3-M-003", type="지표", indicator="C3-T3", importance=3, statement="AI 챗봇으로 매주 뉴스를 보는 사람은 7%에서 10%로 늘었고, 18~24세는 17%였다.",
    value=10, unit="%", as_of="2026", region="GLOBAL(45개 시장)", definition="Reuters Institute DNR 2026, 주간 AI 챗봇 뉴스 이용", prev_value=7, sources=src("decoder_dnr"), verified=True)
add(id="C3-M-004", type="지표", indicator="C3-T3", importance=3, statement="AI 챗봇이 전한 뉴스를 믿는다는 응답은 전체 20%였다. 챗봇 이용자는 44%, 비이용자는 17%였다.",
    value=20, unit="%", as_of="2026", region="GLOBAL", definition="Reuters Institute DNR 2026, AI 생성 뉴스 신뢰", extra={"users": "44%", "non_users": "17%"}, sources=src("decoder_dnr"), verified=True)
add(id="C3-M-005", type="지표", indicator="C3-T4", importance=3, statement="AI 챗봇에서 원문 출처를 자주 누른다는 응답은 4%로, 검색엔진(19%)·소셜미디어(17%)보다 크게 낮았다.",
    value=4, unit="%", as_of="2026", region="GLOBAL(27개 시장)", definition="Reuters Institute DNR 2026, 원문을 항상·자주 클릭", sources=src("decoder_dnr"), verified=True)
add(id="C3-M-006", type="지표", indicator="C3-T4", importance=3, statement="뉴스 퍼블리셔로 가는 Google 검색 유입은 2025년 7월~2026년 7월 사이 40.2% 줄었다(전년 감소폭 21.9%). AI 챗봇 유입은 전체 트래픽의 0.01%였다.",
    value=-40.2, unit="% YoY", as_of="2026-07", region="GLOBAL", definition="Chartbeat 퍼블리셔 네트워크, Google 검색 유입 변화", prev_value=-21.9, sources=src("chartbeat"), verified=True,
    check_flags=["Chartbeat 원보고서 미대조(2차 보도)"])
add(id="C3-M-007", type="지표", indicator="C3-T5", importance=3, statement="미국 AI 검색(ChatGPT·AI Mode·Gemini·Perplexity·AI Overviews)이 가장 많이 인용한 도메인은 Reddit, YouTube, LinkedIn, Wikipedia 순이었다.",
    value=1, unit="위(Reddit)", as_of="2026-03", region="US", definition="Peec, 인용 출처 3천만 건 분석", sources=src("peec"), verified=True)
add(id="C3-M-008", type="지표", indicator="C3-T6", importance=3, statement="AI로 만든 광고에 호감을 느끼는 미국 Gen Z·밀레니얼은 45%였지만, 광고주는 82%가 소비자가 호감을 느낄 것이라 봤다. 격차는 2024년 32%p에서 37%p로 벌어졌다.",
    value=45, unit="%", as_of="2025-10~2026-01", region="US", definition="IAB·Sonata Insights, 소비자 505명·광고 임원 104명", extra={"advertiser_belief": "82%", "gap_pp": 37, "gap_2024_pp": 32},
    sources=src("iab"), verified=True)
add(id="C3-M-009", type="지표", indicator="C3-T6", importance=2, statement="광고 임원의 83%가 제작에 AI를 쓴다고 답했고(2024년 60%), 소비자의 71%는 AI로 만든 광고를 본 적 있다고 생각했다(2024년 54%).",
    value=83, unit="%", as_of="2025-10~2026-01", region="US", definition="IAB, 광고 제작 AI 사용 기업 비율", prev_value=60, sources=src("iab"), verified=True)
add(id="C3-M-010", type="지표", indicator="C3-T8", importance=3, statement="AI 쇼핑에서 허위·편향 정보에 노출될까 우려하는 한국 소비자는 64%로 6개국 평균(52%)보다 높았다.",
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
    statement="AI 요약으로 정보를 받는 소비자는 원문으로 거의 넘어가지 않는다. 그 결과 정보를 만든 원천(언론·블로그·브랜드 사이트)으로 가는 유입이 빠르게 줄고 있다.",
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


# ---------- 정정·추가 (2026-10-11 검증 반영, probe_20261011/verification_report.md) ----------
CHG = "2026-10-11"
SRC.update({
 "graphite_now": {"url": "https://graphite.io/five-percent/research/ai-now-writes-as-many-online-articles-as-humans-do", "publisher": "Graphite (AI now writes as many online articles as humans do)", "date": "2026-05-15", "grade": "A"},
 "graphite_search": {"url": "https://graphite.io/five-percent/ai-content-in-search-and-llms", "publisher": "Graphite (AI content in search and LLMs)", "date": "2025-10-14", "grade": "A"},
 "dnr_es": {"url": "https://reutersinstitute.politics.ox.ac.uk/digital-news-report/2026/dnr-executive-summary", "publisher": "Reuters Institute (DNR 2026 요약)", "date": "2026-06-16", "grade": "A"},
 "edelman_dnr": {"url": "https://www.edelman.com/newsroom/richard-edelmans-6am-blog/reuters-institute-digital-news-report-2026", "publisher": "Edelman (DNR 2026 요약)", "date": "2026-06", "grade": "B"},
 "sej": {"url": "https://www.searchenginejournal.com/google-search-decline-publishers-chartbeat/590681/", "publisher": "Search Engine Journal (Chartbeat 보고서 해설)", "date": "2026-09", "grade": "B"},
 "pangram": {"url": "https://www.pangram.com/blog/ai-amazon-reviews", "publisher": "Pangram (Amazon 리뷰 연구)", "date": "2026-05-04", "grade": "A"},
 "ahrefs_am": {"url": "https://ahrefs.com/blog/most-cited-domains-ai-mode/", "publisher": "Ahrefs (AI Mode 인용 도메인)", "date": "2026-09", "grade": "B"},
 "criteo_pr": {"url": "https://www.criteo.com/kr/news/press-releases/2026/06/criteo-releases-2026-commerce-and-ai-trends-report/", "publisher": "Criteo 보도자료", "date": "2026-06-10", "grade": "A"},
 "shinkim": {"url": "https://shinkim.com/kor/media/newsletter/3350", "publisher": "법무법인 세종·김앤장 계열 뉴스레터(Shin & Kim)", "date": "2026-06-29", "grade": "B"},
 "bkl": {"url": "https://www.bkl.co.kr/law/insight/newsletter/6557", "publisher": "법무법인 BKL 뉴스레터", "date": "2026", "grade": "B"},
 "khan_aiact": {"url": "https://www.khan.co.kr/article/202607210908001/", "publisher": "경향신문", "date": "2026-07-21", "grade": "B"},
 "mtn_label": {"url": "https://news.mtn.co.kr/news-detail/2026093017122478426", "publisher": "MTN (방미통위 AI 생성물 표시)", "date": "2026-09-30", "grade": "B"},
 "mtn_naver1": {"url": "https://news.mtn.co.kr/news-detail/2026072115515062394", "publisher": "MTN (네이버 AI 표시)", "date": "2026-07-22", "grade": "B"},
 "mtn_naver2": {"url": "https://news.mtn.co.kr/news-detail/2026072417015682342", "publisher": "MTN (네이버 스마트스토어 AI 표시)", "date": "2026-07-25", "grade": "B"},
 "paulweiss": {"url": "https://www.paulweiss.com/insights/client-memos/eu-finalises-transparency-rules-for-ai-generated-content", "publisher": "Paul Weiss (EU AI Act 제50조)", "date": "2026-08", "grade": "B"},
 "newsis_dnr_kr": {"url": "https://www.newsis.com/view/NISX20260616_0003671612", "publisher": "뉴시스 (한국 DNR 2026)", "date": "2026-06-16", "grade": "B"},
 "kookie_dnr": {"url": "https://v.daum.net/v/20260626060325750", "publisher": "쿠키뉴스 (DNR 2026)", "date": "2026-06-26", "grade": "B"},
})
def _get(i): return next(r for r in records if r["id"] == i)
def revise(i, kind, why, **ch):
    r = _get(i)
    r.setdefault("revisions", []).append({"on": CHG, "kind": kind, "before": r.get("statement") if "statement" in ch else None, "why": why})
    r.update(ch)
def _more(i, *keys): return _get(i)["sources"] + src(*keys)

# --- 지표 ---
revise("C3-M-001", "갱신", "Graphite 갱신 연구(2026-05-15)에서 2026년 1분기 값 49.9%가 나왔다. 50%를 넘은 분기는 2025년 4분기뿐이고 최신 분기는 다시 50% 아래이며, 방법도 탐지기 3종 평균으로 바뀌었다.",
    statement="신규 영문 웹 글 중 AI가 쓴 글의 비중은 2026년 1분기 49.9%다(2025년 1분기 49.6%, 2025년 4분기 50.9%). 50%를 넘은 분기는 2025년 4분기 하나뿐이고 최신 분기는 다시 50% 아래다.",
    value=49.9, as_of="2026-Q1", prev_value=50.9, definition="Graphite, 신규 영문 글을 AI 탐지기 3종 평균으로 판정(2025-10 연구의 탐지기 1종 대비 평균 3.3%p 낮음)",
    check_flags=["AI 탐지기 판정치 — 오탐 가능성", "연구가 탐지기 1종에서 3종 평균으로 방법을 바꿔 2025년 값과 이어 읽을 때 주의"],
    sources=src("graphite_now", "axios_graphite"))
revise("C3-M-002", "상충", "Originality.ai 연구에는 지역 표기가 없고, 400%는 2022년 연평균 0.02에서의 증가이며 1.3배는 1·5점(극단) 대 2~4점 비교다.",
    statement="AI 생성 의심 Amazon 리뷰(AI 50% 이상 포함)의 비중은 2022년 대비 약 400% 늘었다. 별점 1점·5점 리뷰는 2~4점 리뷰보다 AI로 탐지될 가능성이 약 1.3배 높았다(극단 별점 합산 대 중간 별점 비교).",
    region="Amazon(마켓플레이스 미표기)", check_flags=["탐지 업체 자체 연구 — 절대 비중은 미공개", "400%는 2022년 연평균 0.02에서의 증가라 비중 수준은 확정 불가"])
revise("C3-M-003", "갱신", "DNR 2026은 48개 시장이고(기록의 45개는 용도별 문항 기준), 한국 14%(1년 새 두 배)가 요약에서 확인된다.",
    statement="AI 챗봇으로 매주 뉴스를 보는 사람은 7%에서 10%로 늘었고, 35세 미만은 16%(18~24세는 17%)였다. 한국은 14%로 1년 새 두 배가 됐고(ChatGPT 7%·Gemini 5%) 영국은 4%로 가장 낮다.",
    region="GLOBAL(48개 시장)", extra={"korea": "14% (ChatGPT 7%·Gemini 5%)"}, check_flags=["97,520명·48개 시장은 쿠키뉴스·Edelman 기준, 요약 페이지에는 시장 수가 없음 — 확인 필요", "한국 14%가 전체 1위인지는 순위표 미확인"],
    sources=src("dnr_es", "decoder_dnr", "kookie_dnr"))
revise("C3-M-004", "갱신", "신뢰 20%가 DNR 요약에서 직접 확인되고 검색엔진 32%·소셜 22%와 비교된다.",
    statement="AI 챗봇이 전한 뉴스를 믿는다는 응답은 전체 20%였다(뉴스 전반 37%, 검색엔진 32%, 소셜 22%보다 낮음). 챗봇 이용자는 44%, 비이용자는 17%였다.",
    check_flags=["이용자 44%·비이용자 17%는 Decoder(2차)만 근거 — DNR 원문 표 확인 필요", "문항 문구가 요약 페이지('챗봇 답변 신뢰')와 Edelman('AI 챗봇 뉴스 신뢰')에서 다름"],
    sources=src("dnr_es", "edelman_dnr", "decoder_dnr"))
revise("C3-M-005", "상충", "4%·19%·17%는 27개 시장 전체 응답자 기준이고, DNR 요약은 챗봇 뉴스 이용자의 42%가 항상·자주 클릭한다고 적는다. 분모가 다른 수치를 섞었다.",
    statement="AI 챗봇으로 뉴스를 보는 사람의 42%는 출처 링크를 항상 또는 자주 누른다(한국 56%로 가장 높고 덴마크 26%). 비교로 검색 이용자는 44%, 소셜 이용자는 36%다. 전체 응답자 기준으로 환산하면 챗봇 4%·검색 19%·소셜 17%다.",
    value=42, unit="% (챗봇 뉴스 이용자 기준)", definition="Reuters Institute DNR 2026, 이용자 중 원문을 항상·자주 클릭하는 비율(전체 응답자 기준 환산 값 4%·19%·17%는 Decoder 인용)",
    check_flags=["Edelman 요약은 '검색 이용자보다 훨씬 덜 누른다'고 적어 DNR 본문 챕터로 최종 확인 필요", "분모가 달라 이용자 기준(42%)과 전체 기준(4%)을 섞지 않음"],
    sources=src("dnr_es", "decoder_dnr", "edelman_dnr"))
revise("C3-M-006", "상충", "Chartbeat 40.2%가 페이지뷰 수의 변화인지 채널 비중의 변화인지 보고서가 밝히지 않고, AI 유입 0.01%도 분모가 정의되지 않았다.",
    statement="Chartbeat 보고서 표기로, 뉴스 퍼블리셔로 가는 Google 검색 유입은 2025년 7월~2026년 7월 사이 40.2% 줄었다(전년 감소폭 21.9%). 이 수치가 페이지뷰 수 변화인지 채널 비중 변화인지는 밝혀져 있지 않다. AI 챗봇 유입은 전체 트래픽의 0.01%로 표기됐다(분모 미정의).",
    check_flags=["Chartbear 원문(다운로드 폼 뒤)은 미확인 — SEJ·Relevant Audience 해설 기준".replace("Chartbear", "Chartbeat"), "페이지뷰/비중 구분 불명", "전체 퍼블리셔 페이지뷰는 월 약 311억(전년 약 320억)으로 -3% 안팎(Relevant Audience)"],
    sources=src("chartbeat", "sej"))
revise("C3-M-007", "단정반증", "인용 1위 도메인은 엔진·시점별로 다르다. Peec 합산 기준 값임을 조건으로 적고, Graphite가 측정한 AI 인용 글의 AI 생성 비중(약 18%)을 덧붙인다.",
    statement="Peec(2026-03, 미국 5개 AI 검색 합산, 점유율 미공개) 기준으로 가장 많이 인용된 도메인은 Reddit, YouTube, LinkedIn, Wikipedia 순이었다. Ahrefs 분석은 ChatGPT 1위 Wikipedia(16.3%), Perplexity·AI Overviews 1위 YouTube, AI Mode는 Reddit 17.9%·YouTube 17.8%로 엔진별로 다르다. 한편 Graphite(2025-10)는 ChatGPT·Perplexity가 인용한 영문 기사·리스티클의 약 18%가 AI 생성이라고 측정했다(Google 순위권 약 14%).",
    check_flags=["엔진·시점별로 1위가 다름 — 합산 1위 Reddit은 Peec 기준에 한함", "Ahrefs 점유율은 B 등급이고 방법·표본 수 불투명", "Graphite 18%는 탐지기 1종, 위양성 4.2%, 2025-06 데이터라 지표 정의와 다를 수 있어 참고 수준 — 확인 필요"],
    sources=_more("C3-M-007", "ahrefs_am", "graphite_search"))
revise("C3-M-008", "갱신", "IAB 반복 조사(2024-08~10 대 2025-10~2026-01)에서 AI 광고에 부정적인 비율이 12%p 올랐고 긍정은 소폭 하락했다.",
    statement="AI로 만든 광고에 호감을 느끼는 미국 Gen Z·밀레니얼은 45%였지만, 광고주는 82%가 소비자가 호감을 느낄 것이라 봤다. 격차는 2024년 32%p에서 37%p로 벌어졌다. AI 광고에 부정적인 비율은 2024년보다 12%p 올랐고(Gen Z 21%→39%, 밀레니얼 15%→20%) 호감은 소폭 하락했다.",
    extra={"advertiser_belief": "82%", "gap_pp": 37, "gap_2024_pp": 32, "negative_genz": "39% (2024년 21%)", "negative_millennial": "20% (2024년 15%)"},
    check_flags=["2024년 호감 수치가 원문에 없어 호감이 3%p 이상 하락했는지는 확인 필요(IAB 2024년 12월 보고서 원문 미열람)"])
revise("C3-M-010", "상충", "Criteo 52%는 미국·영국·프랑스·독일·일본·한국 6개국 평균이라 '글로벌 평균'이 아니다.",
    statement="AI 쇼핑에서 허위·편향 정보에 노출될까 우려하는 한국 소비자는 64%로 6개국(미국·영국·프랑스·독일·일본·한국, 6,379명) 평균(52%)보다 높았다. 필드워크는 2026-01-01~02-28이다.",
    sources=src("criteo_pr", "criteo_kr"))

# --- 사건 ---
revise("C3-E-001", "갱신", "AI기본법 시행령·고시가 2026-07-21 시행됐고 정부는 '최소 1년 이상 계도기간'을 다시 밝혔다. 계도기간 시작일은 보도가 밝히지 않는다.",
    statement="한국 AI 기본법이 2026-01-22 시행됐고 시행령·하위 고시는 7월 21일 시행됐다. 생성형 AI 결과물 표시 의무는 AI 사업자에게만 있고 일반 이용자는 대상이 아니며, 과태료(최대 3천만 원)는 최소 1년 이상 계도기간으로 유예된다. 계도기간 시작일은 보도가 밝히지 않아 1월 22일부터인지 7월 21일부터인지 불명이다.",
    check_flags=["계도기간 종료일을 단정할 수 없음", "시행령 본문·과기정통부 공식 발표 원문은 미열람", "계도기간 2026-12 종료라는 블로그 주장은 C등급이라 채택하지 않음"],
    sources=src("newsis_aiact", "khan_aiact"))
revise("C3-E-002", "상충", "서로 다른 두 시행이 한 날짜로 묶여 있었다. 7월 21일은 전자상거래법 시행령 사용후기 정보공개 시행일이고, 가상인물 표시는 별도 건이다.",
    statement="전자상거래법 시행령 제27조의3에 따라 2026-07-21부터 온라인 쇼핑몰은 사용후기의 작성 자격·게시 기간·등급평가·삭제 기준·이의 절차를 공개해야 한다.",
    date="2026-07-21", actor="정부(전자상거래법 시행령)", check_flags=["가상인물 표시는 별도 사건(C3-E-005)으로 분리"], sources=src("newsis_ftc_kr", "bkl"))
revise("C3-E-003", "누락정정", "플랫폼 대응에 네이버가 빠졌다. 네이버는 5월 자율 'AI 활용' 표시, 7월 10일 스마트스토어 쇼핑 광고 이미지·영상의 AI 사용 표시 의무화를 도입했다.",
    statement="무신사가 리뷰에 AI 생성 이미지 첨부를 금지하고 해당 적립금을 회수할 수 있게 약관을 바꿨다. 쿠팡은 가짜 리뷰는 제재하지만 AI 도움을 받은 리뷰는 막지 않는다. 네이버는 5월 블로그·카페·클립에 자율 'AI 활용' 표시를 도입했고 7월 10일 스마트스토어 쇼핑 광고 이미지·영상의 AI 사용 표시를 의무화했다(리뷰는 대상으로 적히지 않음). 쿠팡은 8월 7일 'AI 리뷰 요약' 등 자체 AI 기능을 출시했다.",
    check_flags=["쿠팡 AI 리뷰 요약 출시는 2차 보도(표시·검증 방식 미기재) — 확인 필요"], sources=src("mtn_reviews", "mtn_naver1", "mtn_naver2"))

# --- 신규 ---
add(id="C3-M-011", type="지표", indicator="C3-T2", importance=2, added_on=CHG, statement="Pangram은 Amazon 베스트셀러 500개 상품의 첫 페이지 리뷰 30,000건 중 3%(909건)를 고신뢰 AI 생성으로 판정했다. AI 리뷰의 5점 비율은 74%(사람 59%), 1점 비율은 10%(사람 22%)였다.",
    value=3, unit="%", as_of="2026-05", region="Amazon(베스트셀러 첫 페이지)", definition="Pangram, 베스트셀러 500개 상품 첫 페이지 리뷰 30,000건 AI 탐지",
    sources=src("pangram"), verified=True, check_flags=["탐지 업체 자체 연구 — 베스트셀러 첫 페이지라 전체 리뷰를 대표하지 않음"])
add(id="C3-E-005", type="사건", importance=3, added_on=CHG, statement="공정위 추천·보증 심사지침 개정으로 AI 가상인물을 쓴 추천·보증 광고에 '가상인물' 표시가 필요해졌다(2026-04-08 행정예고, 6월 1일 적용 보도).",
    date="2026-06-01", actor="공정거래위원회", sources=src("shinkim", "newsis_ftc_kr"), verified=True, check_flags=["6월 1일 적용은 법무법인 뉴스레터 등 3곳이 일치하나 공정위 보도자료 원문은 미열람 — 확인 필요"])
add(id="C3-E-006", type="사건", importance=3, added_on=CHG, statement="방송미디어통신위원회가 정보통신망법을 개정해 AI 생성 이미지·영상을 올리는 이용자에게 표시 의무를 지우고 포털·플랫폼이 이를 관리하게 하는 방안을 12월까지 추진하기로 했다(입법 전 단계, 시행일 없음).",
    date="2026-09-30", actor="방송미디어통신위원회", sources=src("mtn_label"), verified=True)
add(id="C3-E-007", type="사건", importance=2, added_on=CHG, statement="EU AI Act 제50조(딥페이크·공익 목적 AI 텍스트 표시)가 2026-08-02 적용을 시작했다. 기존 시장 생성형 시스템의 워터마킹은 2026-12-02, 탐지 상호운용은 2027-02-02로 유예됐고, 상품 설명·사용자에게만 보이는 챗봇 답변은 텍스트 표시 대상이 아니다.",
    date="2026-08-02", actor="EU 집행위원회", sources=src("paulweiss"), verified=True)

# --- 해석 ---
revise("C3-I-001", "갱신", "최신 분기(2026년 1분기) 값 49.9%로 '절반 수준에서 멈춰 있다'가 유지되나 '이미 절반'은 50% 미만이다.",
    statement="정보 글의 생산은 절반 안팎까지 AI로 넘어갔고 그 수준에서 멈춰 있다(신규 영문 글의 AI 비중 49.9%, 50%를 넘은 분기는 2025년 4분기뿐). AI 글이 흔해질수록 사람의 실제 경험이 담긴 글이 상대적으로 귀해진다.")
revise("C3-I-002", "단정반증", "챗봇 뉴스 이용자의 42%는 원문을 자주 누르고, AI 요약이 검색 유입 감소의 원인이라는 직접 증거는 기록에 없다.",
    statement="AI 챗봇으로 뉴스를 보는 사람 중 절반 가까이(42%)는 원문을 여전히 자주 누르지만, 그런 이용자는 전체의 10%이고 퍼블리셔로 가는 Google 검색 유입은 Chartbeat 표기로 크게 줄었다. 검색 유입 감소의 원인이 AI 요약인지는 확인되지 않았다.",
    check_flags=["Chartbeat 기준 AI 챗봇 유입 0.01%(Axios 3월 보도는 1% 미만)는 분모가 달라 비교 불가"])
revise("C3-I-003", "갱신", "광고 호감 하락의 근거를 IAB 반복 조사의 부정 비율 12%p 상승으로 보강했다.",
    statement="AI를 거친 정보의 이용은 늘지만 신뢰는 따라오지 않았다. AI 뉴스를 믿는 사람은 이용자 안에서만 절반 가까이이고 전체로는 5명 중 1명이며, AI 광고에 부정적인 젊은 층은 1년 새 12%p 늘었다.")
revise("C3-I-004", "단정반증", "'브랜드 자체 콘텐츠보다'를 비교한 자료가 없고, 1위 도메인은 엔진·시점별로 다르다.",
    statement="미국 AI 검색 5개 합산 기준으로 AI 답변은 Reddit·YouTube 같은 사람의 경험담 도메인을 가장 많이 인용한다(엔진별로는 Wikipedia·YouTube가 1위인 경우도 있다). 브랜드 자체 콘텐츠와의 직접 비교 자료는 확인하지 못했다. 구매 판단의 근거가 '다른 사람의 실제 경험'에 있다는 해석은 이 인용 양상을 근거로 한 추정이다.",
    check_flags=["'브랜드 자체 콘텐츠보다 많이'는 비교 자료가 없어 확인 불가"])
revise("C3-I-005", "단정반증", "Pangram은 AI 리뷰가 5점에 쏠리고 1점은 오히려 적다고 했다. Originality와 탐지기·표본이 달라 '극단 별점에 몰린다'는 절반만 맞다. 플랫폼 대응에 네이버가 빠졌다.",
    statement="AI가 쓴 리뷰는 늘고 있고, 5점 쪽으로 쏠린다는 조사가 있다(Pangram: AI 리뷰 5점 74%·사람 59%, 1점 10%·사람 22%). Originality는 극단 별점(1·5점)이 중간 별점보다 약 1.3배 AI로 탐지된다고 했으나 두 조사는 탐지기·표본이 달라 직접 비교할 수 없다. 플랫폼 대응은 금지(무신사), 허용(쿠팡), 판매자 광고 콘텐츠만 의무 표시(네이버)로 갈려 리뷰의 신뢰 기준이 흔들리고 있다.",
    basis=["C3-M-002", "C3-M-011", "C3-E-003"])
revise("C3-I-006", "갱신", "방송미디어통신위원회가 이용자 AI 생성물 표시 의무를 12월까지 추진하기로 해, 이용자 영역은 '예정'으로 바뀌는 중이다. 아직 법이 아니다.",
    statement="한국은 표시 규제를 먼저 만들었지만 AI기본법의 대상은 AI 사업자이고 과태료도 유예됐으며, 가상인물 표시는 광고에 한정된다. 이용자가 쓰는 리뷰의 AI 사용은 아직 플랫폼 자율이다. 방송미디어통신위원회가 이용자의 AI 생성 이미지·영상 표시 의무를 12월까지 추진하겠다고 밝혔으나 입법 전 단계다. 소비자의 허위 정보 우려는 6개국 평균보다 높다.",
    basis=["C3-E-001", "C3-E-002", "C3-E-003", "C3-E-005", "C3-E-006", "C3-M-010"])

# --- 전망 ---
revise("C3-F-001", "판정 기준 보완", "정수 반올림이라 25%가 나올 수 있는데 F-001('25%를 넘지 못한다')과 F-101 마일스톤('25% 이상')이 모두 적중하는 충돌이 있었다. 경계를 '25% 초과'로 통일했다.",
    method="Reuters Institute Digital News Report 2027의 AI 뉴스 신뢰(전체) 수치 확인. 25% 이하면 적중, 26% 이상이면 빗나감. 문항 문구가 바뀌거나 문항이 빠지면 판정 불가")
revise("C3-F-002", "판정 기준 보완", "Chartbeat 수치가 페이지뷰 변화인지 채널 비중 변화인지 가를 수 없고 보고서가 다운로드 폼 뒤에 있다.",
    method="Chartbeat 2027 보고서에서 같은 정의로 공표한 퍼블리셔 Google 검색 유입 연간 변화율을 확인(채널 비중 변화는 제외). 공표가 없으면 판정 불가")
revise("C3-F-003", "전망 점검", "정부의 '최소 1년 이상 계도기간'이 시행령·고시 시행일(2026-07-21)에 다시 언급됐고 시작일이 불명이라 근거가 달라졌다. '유예'는 법정 기한이 아닌 계도 방침이다.",
    method="과기정통부 공식 발표로 계도기간 종료를 알린 날짜가 2027-01-22 이후인지 확인. 종료 발표가 없으면 계도 지속으로 판정", basis=["C3-E-001"],
    check_flags=["계도기간 시작일이 불명이라 7월 21일 기준이면 2027-01-22 이후까지 이미 이어지는 셈"])
revise("C3-F-004", "판정 기준 보완", "네이버는 이미 5월 블로그 자율 표시와 7월 광고 이미지 의무 표시를 도입했고(리뷰는 아님), 쿠팡은 8월 AI 리뷰 요약을 냈다. 판정 대상을 이용자 작성 리뷰로 좁혔다.",
    method="쿠팡 또는 네이버가 이용자 작성 리뷰의 AI 사용을 표시하거나 제한하는 약관·공지를 게시한 것을 확인. 판매자 광고 콘텐츠 표시·플랫폼 자체 AI 요약은 제외",
    basis=["C3-E-003", "C3-E-002", "C3-E-006"])
revise("C3-F-005", "판정 기준 보완", "기준이 현재값과 같은 45%이고 표본이 505명(오차 약 ±4%p)이라 오차범위 안의 하락도 적중이 된다. IAB 조사 주기가 약 13개월이라 조사가 안 나올 수 있다.",
    statement="IAB의 다음 조사에서 AI 광고에 호감을 느끼는 Gen Z·밀레니얼 비율은 42% 이하로 내려갈 것이다(45%에서 3%p 이상 하락).",
    method="IAB AI 광고 인식 조사 차기 발표에서 42% 이하이면 적중, 43% 이상이면 빗나감. 조사가 나오지 않으면 판정 불가")
revise("C3-F-006", "판정 기준 보완", "60% 미만은 현재값(49.9%)에서 10.1%p 여유라 거의 확정에 가깝고, Graphite가 방법을 바꾼 이력이 있어 방법 변경 시 판정 규칙이 필요했다.",
    statement="Graphite의 다음 측정에서도 신규 영문 웹 글 중 AI 생성 비중은 55% 미만에 머물 것이다.",
    condition="같은 방법(탐지기 3종 평균)으로 측정할 경우",
    method="Graphite 후속 연구의 AI 생성 비중 확인. 55% 이상이면 빗나감. 탐지 방법이 바뀌면 판정 불가")
revise("C3-F-101", "판정 기준 보완", "조건 (2) '국내 주요 쇼핑 플랫폼의 AI 리뷰 표시·제한'은 문자 그대로 읽으면 이미 충족돼 있었고, 마일스톤 '25% 이상'과 시나리오 문구 '넘는다'의 경계가 달랐다.",
    milestones=[
        {"by": "2027-01", "text": "AI 기본법 표시 의무 과태료 유예 종료, 집행 시작"},
        {"by": "2027-06", "text": "쿠팡·네이버 중 1곳 이상 이용자 작성 리뷰의 AI 사용 표시·제한 도입"},
        {"by": "2027-06", "text": "AI 뉴스 신뢰(전체) 25% 초과(26% 이상)"}],
    method="세 가지 중 두 가지 이상 충족 시 적중: (1) Reuters Institute 보고서의 AI 뉴스 신뢰(전체) 26% 이상 (2) 쿠팡·네이버 중 1곳 이상이 이용자 작성 리뷰의 AI 사용을 표시·제한(무신사 제외) (3) AI 기본법 표시 의무의 과태료 집행 시작",
    basis=["C3-M-004", "C3-E-001", "C3-E-002", "C3-E-003", "C3-E-006"])

revise("C3-F-102", "판정 기준 보완", "F-005의 기준을 42% 이하로 바꾸고 낙관 시나리오 조건을 고친 데 맞췄다.",
    milestones=[
        {"by": "2027-01", "text": "AI 기본법 과태료 유예 연장"},
        {"by": "2027-03", "text": "젊은 층의 AI 광고 호감 42% 이하로 하락"},
        {"by": "2027-09", "text": "퍼블리셔 Google 검색 유입 감소가 연 20% 이상 지속"}])

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

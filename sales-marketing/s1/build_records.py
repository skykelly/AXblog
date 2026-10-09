"""S1 R1 4유형 기록 생성 + 규칙 검증.
출력: i4/records.jsonl
"""
import json, sys
from pathlib import Path
from collections import Counter

R = "R1"
SRC = {
 "conductor": {"url": "https://www.businesswire.com/news/home/20251113364791/en/Conductor-Unveils-2026-AEO-GEO-Benchmarks-Report-How-AI-Shapes-Brand-Visibility-in-a-Zero-Click-World", "publisher": "Conductor 2026 AEO/GEO 벤치마크 (보도자료)", "date": "2025-11-13", "grade": "B"},
 "previsible": {"url": "https://previsible.com/seo-strategy/ai-traffic-report-july-2026/", "publisher": "Previsible AI 트래픽 보고서 (GA4 166개)", "date": "2026-07-06", "grade": "B"},
 "adobe_jul": {"url": "https://business.adobe.com/assets/pdfs/resources/sdk/ai-traffic-trends-report-august-2026/ai-traffic-trends-report-2026-08-19.pdf", "publisher": "Adobe Digital Insights", "date": "2026-08-19", "grade": "A"},
 "adobe_q1": {"url": "https://decrypt.co/364733/ai-traffic-us-retailers-jumps-q1-agentic-shoppers-outspend-humans", "publisher": "Decrypt (Adobe Analytics)", "date": "2026-04", "grade": "B"},
 "sparktoro": {"url": "https://sparktoro.com/blog/in-2026-less-than-one-third-of-google-searches-still-send-a-click/", "publisher": "SparkToro (Similarweb 패널)", "date": "2026-06", "grade": "A"},
 "pew": {"url": "https://www.pewresearch.org/short-reads/2025/07/22/google-users-are-less-likely-to-click-on-links-when-an-ai-summary-appears-in-the-results/", "publisher": "Pew Research Center", "date": "2025-07-22", "grade": "A"},
 "chartbeat": {"url": "https://www.relevantaudience.com/seo/chartbeat-google-search-publisher-traffic-down-40-percent/", "publisher": "Relevant Audience (Chartbeat 2026 보고서 인용)", "date": "2026-09-25", "grade": "B"},
 "google_q2": {"url": "https://blog.google/company-news/inside-google/message-ceo/alphabet-earnings-q2-2026/", "publisher": "Google (Alphabet 2분기 실적)", "date": "2026-07-22", "grade": "A"},
 "wix": {"url": "https://searchengineland.com/ai-citations-favor-listicles-articles-product-pages-study-472364", "publisher": "Search Engine Land (Wix Studio AI Search Lab)", "date": "2026-03-24", "grade": "B"},
 "peec": {"url": "https://docs.peec.ai/research/most-cited-domains-in-ai-search", "publisher": "Peec 연구", "date": "2026-03", "grade": "B"},
 "ahrefs": {"url": "https://ahrefs.com/blog/ai-overview-brand-correlation/", "publisher": "Ahrefs (7만 5천 브랜드 분석)", "date": "2025-05-26", "grade": "B"},
 "seer": {"url": "https://www.seerinteractive.com/insights/what-drives-brand-mentions-in-ai-answers", "publisher": "Seer Interactive", "date": "2025-01-07", "grade": "B"},
 "gml": {"url": "https://gigazine.net/gsc_news/en/20260521-google-marketing-ai-search", "publisher": "GIGAZINE (Google Marketing Live 2026)", "date": "2026-05-21", "grade": "B"},
 "chatgpt_ads": {"url": "https://siliconangle.com/2026/01/16/openai-start-testing-chatgpt-ads-across-free-go-tiers/", "publisher": "SiliconANGLE (OpenAI 발표)", "date": "2026-01-16", "grade": "B"},
 "profound": {"url": "https://www.mind.eu.com/retail/en/article/profound-raises-us96-million-in-series-c-funding-becoming-a-first-geo-unicorn/", "publisher": "MIND Retail", "date": "2026-02-24", "grade": "B"},
 "naver_call": {"url": "https://www.sentv.co.kr/article/view/sentv202602060034", "publisher": "서울경제TV (네이버 실적 발표)", "date": "2026-02-06", "grade": "B"},
 "naver_share": {"url": "https://m.ceoscoredaily.com/page/view/2026031016373092535", "publisher": "CEO스코어데일리 (인터넷트렌드)", "date": "2026-03-11", "grade": "B"},
 "naver_aitab": {"url": "https://byline.network/2026/06/26_12083847/", "publisher": "바이라인네트워크", "date": "2026-06-26", "grade": "B"},
}
def src(*keys): return [dict(SRC[k], key=k) for k in keys]

base = dict(question="S1", question_version="v1.0", first_seen=R, last_seen=R, status="유효", replaces=None, check_flags=[])
records = []
def add(**kw):
    r = dict(base); r.update(kw); records.append(r)

BASELINE = "조사 기간 이전 연구 — 기준선으로 사용"
VENDOR = "GEO·SEO 업체 연구 — 이해관계자 자료"

# ---------- 지표 (M) ----------
add(id="S1-M-001", type="지표", indicator="S1-T1", importance=3, statement="기업 웹사이트 1만 3천여 곳의 전체 방문 중 AI 답변 플랫폼에서 온 유입은 평균 1.08%다. 이 가운데 87.4%가 ChatGPT에서 왔다.",
    value=1.08, unit="%", as_of="2025-09", region="GLOBAL", definition="전체 세션 중 AI 플랫폼 유입 비중 (2025년 5~9월, 13,770개 도메인)", extra={"chatgpt_share": "87.4%"},
    sources=src("conductor"), verified=True, check_flags=[VENDOR, "2025년 5~9월 데이터 — 다음 벤치마크로 갱신 필요"])
add(id="S1-M-002", type="지표", indicator="S1-T2", importance=2, statement="GA4 166개 사이트에서 AI 유입 세션은 2024년 11월부터 2026년 5월까지 9.9배로 늘었다. ChatGPT가 92.4%를 차지하고, 이커머스 업종은 37배 늘었다.",
    value=9.9, unit="배 (19개월)", as_of="2026-05", region="GLOBAL", definition="AI 플랫폼 유입 세션 증가 배수", extra={"chatgpt_share": "92.4%", "ecommerce": "37배"},
    sources=src("previsible"), verified=True, check_flags=[VENDOR])
add(id="S1-M-003", type="지표", indicator="S1-T3", importance=3, statement="2026년 7월 미국 리테일 사이트의 AI 유입은 전년보다 62% 늘었고, 전환율은 AI가 아닌 유입보다 60% 높았다. 1분기에는 유입이 393% 늘었고, 1년 전 38% 낮던 전환율이 42% 높아졌다.",
    value=60, unit="% (비AI 대비 전환율 우위)", as_of="2026-07", region="US", definition="미국 리테일 사이트의 AI 유입 전환율, 비AI 유입 대비", extra={"traffic_yoy_jul": "+62%", "traffic_yoy_q1": "+393%"},
    sources=src("adobe_jul", "adobe_q1"), verified=True)
add(id="S1-M-004", type="지표", indicator="S1-T4", importance=3, statement="2026년 1~4월 미국 구글 검색의 68.01%가 클릭 없이 끝났다. 2024년에는 60.45%였다.",
    value=68.01, unit="%", as_of="2026-04", region="US", definition="클릭 없이 끝난 구글 검색 비율", sources=src("sparktoro"), verified=True)
add(id="S1-M-005", type="지표", indicator="S1-T4", importance=2, statement="구글 AI 요약이 뜬 검색에서 일반 결과 클릭률은 8%로, 요약이 없을 때(15%)의 절반이었다.",
    value=8, unit="% (AI 요약 노출 시 클릭률)", as_of="2025-03", region="US", definition="AI 요약 노출 검색의 일반 링크 클릭률", extra={"without_ai": "15%"},
    sources=src("pew"), verified=True, check_flags=[BASELINE])
add(id="S1-M-006", type="지표", indicator="S1-T4", importance=2, statement="뉴스 퍼블리셔로 가는 구글 검색 유입은 2025년 7월부터 1년 동안 40.2% 줄었다(전년 감소폭 21.9%). 같은 기간 AI 챗봇 유입은 전체의 0.01%였다.",
    value=-40.2, unit="% (구글 검색 유입, 전년 대비)", as_of="2026-07", region="GLOBAL", definition="Chartbeat 퍼블리셔 네트워크의 구글 검색 유입 변화", extra={"ai_chatbot_share": "0.01%"},
    sources=src("chartbeat"), verified=True, check_flags=["뉴스 퍼블리셔 기준 — 브랜드 사이트와 다를 수 있음"])
add(id="S1-M-007", type="지표", indicator="S1-T5", importance=2, statement="구글 검색의 약 25%에 AI 요약이 뜬다. 업종별로는 헬스케어 48.7%, 금융 25.8%다.",
    value=25, unit="%", as_of="2025-09", region="US", definition="AI Overviews가 노출되는 검색 비율", extra={"healthcare": "48.7%", "financials": "25.8%"},
    sources=src("conductor"), verified=True, check_flags=[VENDOR])
add(id="S1-M-008", type="지표", indicator="S1-T5", importance=3, statement="구글 AI Mode의 월간 이용자는 10억 명을 넘었다. 구글은 AI Mode와 AI 요약이 전체 검색량을 늘리고 있다고 밝혔고, 검색 매출은 17% 늘었다.",
    value=10, unit="억 명 (AI Mode 월간 이용자)", as_of="2026-07", region="GLOBAL", definition="구글 AI Mode 월간 활성 이용자", extra={"search_revenue_yoy": "+17%", "gemini_mau": "9.5억 명"},
    sources=src("google_q2"), verified=True)
add(id="S1-M-009", type="지표", indicator="S1-T5", importance=2, statement="2026년 1~4월 미국 구글 검색 중 AI Mode로 넘어간 비율은 0.34%였다.",
    value=0.34, unit="%", as_of="2026-04", region="US", definition="구글 검색 중 AI Mode로 이동한 비율", sources=src("sparktoro"), verified=True,
    check_flags=["구글의 'AI Mode 월 10억 명'과 기준이 다름 — 이용자 수 vs 검색 비중"])
add(id="S1-M-010", type="지표", indicator="S1-T6", importance=3, statement="ChatGPT·AI Mode·Perplexity의 답변 7만 5천 건, 인용 100만여 건을 보면 리스트형 글 21.9%, 일반 기사 16.7%, 상품 페이지 13.7% 순이다. 비교·구매 검토 질문에서는 리스트형 글이 40.9%, 구매 직전 질문에서는 상품·카테고리 페이지가 약 40%다.",
    value=21.9, unit="% (리스트형 글 인용 비중)", as_of="2026-03", region="GLOBAL", definition="AI 답변 인용의 콘텐츠 형식 비중",
    extra={"commercial_listicles": "40.9%", "transactional_product_pages": "약 40%", "third_party_listicles_prof_services": "80.9%"},
    sources=src("wix"), verified=True, check_flags=[VENDOR])
add(id="S1-M-011", type="지표", indicator="S1-T6", importance=2, statement="미국 AI 검색 5종이 가장 많이 인용한 도메인은 Reddit, YouTube, LinkedIn, Wikipedia 순이었다.",
    value=None, unit="", as_of="2026-03", region="US", definition="AI 검색 최다 인용 도메인", sources=src("peec"), verified=True, check_flags=[VENDOR])
add(id="S1-M-012", type="지표", indicator="S1-T6", importance=3, statement="브랜드 7만 5천 개를 분석한 결과, AI 요약 노출과 가장 강하게 연결된 신호는 웹상의 브랜드 언급(상관계수 0.664)이었다. 백링크 수(0.218)와 광고비(0.215)는 약했다.",
    value=0.664, unit="상관계수 (브랜드 언급)", as_of="2025-05", region="GLOBAL", definition="AI Overviews 브랜드 노출과 신호의 순위 상관",
    extra={"branded_anchors": 0.527, "branded_search": 0.392, "domain_rating": 0.326, "backlinks": 0.218, "ad_cost": 0.215},
    sources=src("ahrefs"), verified=True, check_flags=[BASELINE, VENDOR])
add(id="S1-M-013", type="지표", indicator="S1-T6", importance=2, statement="AI 답변의 브랜드 언급과 가장 강하게 연결된 것은 구글 1페이지 순위(상관계수 약 0.65)였고, 빙 순위(0.5~0.6)가 뒤를 이었다. 백링크와 콘텐츠 다양성은 영향이 약했다.",
    value=0.65, unit="상관계수 (구글 1페이지 순위)", as_of="2025-01", region="US", definition="AI 답변 브랜드 언급과 검색 순위의 상관 (금융·SaaS 질문 1만 개)",
    sources=src("seer"), verified=True, check_flags=[BASELINE, VENDOR])
add(id="S1-M-014", type="지표", indicator="S1-T8", importance=3, statement="네이버 AI 브리핑은 통합검색 쿼리의 약 20%에 적용되고, 15자 이상 긴 검색은 도입 전보다 두 배 넘게 늘었다. 네이버는 연말까지 적용 범위를 두 배로 넓히겠다고 밝혔다.",
    value=20, unit="% (통합검색 적용 비율)", as_of="2026-02", region="KR", definition="네이버 AI 브리핑이 적용되는 통합검색 쿼리 비율", extra={"year_end_target": "현재의 2배"},
    sources=src("naver_call"), verified=True)
add(id="S1-M-015", type="지표", indicator="S1-T8", importance=2, statement="2026년 1월~3월 초 국내 검색 점유율은 네이버 64.39%, 구글 28.54%였다. 네이버 점유율은 8년 만의 최고치로, AI 브리핑이 회복의 계기로 꼽힌다.",
    value=64.39, unit="% (네이버 검색 점유율)", as_of="2026-03", region="KR", definition="인터넷트렌드 기준 국내 검색엔진 점유율", extra={"google": "28.54%"},
    sources=src("naver_share"), verified=True)

# ---------- 사건 (E) ----------
add(id="S1-E-001", type="사건", importance=2, statement="OpenAI가 미국 ChatGPT 무료·Go 요금제에서 답변 아래 '스폰서' 카드 광고 시험을 시작한다고 발표했다.",
    date="2026-01-16", actor="OpenAI", sources=src("chatgpt_ads"), verified=True)
add(id="S1-E-002", type="사건", importance=2, statement="네이버가 AI 브리핑이 통합검색의 20%에 적용됐다고 밝히고, 연말까지 두 배로 넓히며 쇼핑·로컬로 확장하겠다고 했다.",
    date="2026-02-06", actor="네이버", sources=src("naver_call"), verified=True)
add(id="S1-E-003", type="사건", importance=2, statement="AI 답변 속 브랜드 노출을 측정하는 Profound가 9,600만 달러를 유치해 기업가치 10억 달러로 첫 GEO 유니콘이 됐다. 고객사는 700곳이 넘는다.",
    date="2026-02-24", actor="Profound", sources=src("profound"), verified=True)
add(id="S1-E-004", type="사건", importance=3, statement="구글이 AI Mode 답변 안에 들어가는 광고(대화형 발견 광고, 답변 목록 속 강조 광고)와 AI Mode 안 할인 제안·결제를 공개했다. 대화형 광고는 시험 중이다.",
    date="2026-05-20", actor="Google", sources=src("gml"), verified=True, check_flags=["출시 시기·국가는 원문에 없음"])
add(id="S1-E-005", type="사건", importance=2, statement="네이버가 대화형 검색 AI탭을 전체 이용자에게 정식 출시했다. 베타 두 달 동안 누적 이용자 400만 명, 상품·장소 카드 클릭률 20% 이상을 기록했다.",
    date="2026-06-26", actor="네이버", sources=src("naver_aitab"), verified=True)
add(id="S1-E-006", type="사건", importance=3, statement="구글이 AI Mode 월간 이용자 10억 명 돌파를 발표했다. AI 검색이 검색량을 줄이지 않고 늘린다고 강조했다.",
    date="2026-07-22", actor="Google", sources=src("google_q2"), verified=True)

# ---------- 해석 (I) ----------
add(id="S1-I-001", type="해석", importance=3, target="유입 저울", direction="약화",
    statement="브랜드 사이트 기준으로 보면 검색에서 잃는 클릭이 AI에서 얻는 유입보다 훨씬 크다. 구글 검색의 68%가 클릭 없이 끝나고 퍼블리셔 검색 유입은 1년 새 40% 줄었지만, AI 유입은 전체 방문의 1% 안팎이다.",
    basis=["S1-M-004", "S1-M-006", "S1-M-001"])
add(id="S1-I-002", type="해석", importance=3, target="AI 유입의 질", direction="강화",
    statement="AI 유입은 양은 작지만 질은 높다. 리테일에서 AI 유입의 전환율은 1년 만에 비AI보다 낮던 수준에서 60% 높은 수준으로 올라섰다. 이미 AI 답변에서 비교를 끝내고 들어오는 방문이기 때문이다.",
    basis=["S1-M-003", "S1-M-002"])
add(id="S1-I-003", type="해석", importance=3, target="노출의 무대", direction="강화",
    statement="브랜드가 보여야 하는 무대는 검색 결과 목록에서 AI 답변 안으로 옮겨가고 있다. 구글 검색의 약 4분의 1에 AI 요약이 뜨고 AI Mode 이용자가 10억 명을 넘었다. 다만 AI Mode가 검색에서 차지하는 비중은 아직 1%에 못 미친다.",
    basis=["S1-M-007", "S1-M-008", "S1-M-009"])
add(id="S1-I-004", type="해석", importance=3, target="인용 신호 ① 제3자 언급", direction="강화",
    statement="AI 답변 노출을 가르는 가장 강한 신호는 브랜드가 직접 말하는 것이 아니라 남이 브랜드를 말하는 것이다. 웹상의 브랜드 언급이 백링크·광고비보다 세 배 강하게 연결되고, 가장 많이 인용되는 곳은 Reddit·YouTube 같은 커뮤니티이며, 전문 서비스 분야에서는 리스트형 글 인용의 81%가 제3자 글이다.",
    basis=["S1-M-012", "S1-M-011", "S1-M-010"])
add(id="S1-I-005", type="해석", importance=2, target="인용 신호 ② 검색 순위", direction="중립",
    statement="기존 검색 순위는 여전히 AI 노출의 기반이다. 구글 1페이지 순위가 AI 답변의 브랜드 언급과 가장 강하게 연결됐다. GEO는 SEO를 대체하는 것이 아니라 그 위에 쌓인다.",
    basis=["S1-M-013"])
add(id="S1-I-006", type="해석", importance=2, target="인용 신호 ③ 질문 단계별 형식", direction="강화",
    statement="질문 단계마다 인용되는 형식이 다르다. 비교·검토 단계에서는 리스트형 비교 글이, 구매 직전에는 상품·카테고리 페이지가 인용의 약 40%를 차지한다. 브랜드가 직접 통제할 수 있는 영역은 구매 직전의 상품 데이터다.",
    basis=["S1-M-010"])
add(id="S1-I-007", type="해석", importance=2, target="유료 경로", direction="강화",
    statement="AI 답변 안 노출을 돈으로 살 수 있는 길이 열리고 있다. 구글은 AI Mode 답변 속 광고를, OpenAI는 ChatGPT 답변 아래 광고를 시험 중이다. 노출 측정 시장도 커져 GEO 측정 업체가 유니콘이 됐다.",
    basis=["S1-E-004", "S1-E-001", "S1-E-003"])
add(id="S1-I-008", type="해석", importance=3, target="한국", direction="강화",
    statement="한국의 GEO 무대는 네이버다. AI 브리핑이 검색의 20%에 적용되면서 네이버 점유율이 8년 만의 최고(64%)로 올라섰고, 연말까지 적용을 두 배로 넓힌다. 글로벌 GEO 공식(커뮤니티 언급)은 한국에서 네이버 블로그·카페 언급으로 읽어야 한다.",
    basis=["S1-M-014", "S1-M-015", "S1-E-005"])

# ---------- 세부 전망 (F) ----------
add(id="S1-F-001", type="전망", importance=2, status="유효", forecast_status="진행 중",
    statement="Conductor의 다음 벤치마크(2027년판)에서 AI 유입 비중은 2% 이상으로 나올 것이다.", due="2026-12-31", condition="같은 방식의 벤치마크가 발표될 경우",
    method="Conductor 2027 AEO/GEO 벤치마크 확인", basis=["S1-M-001", "S1-M-002"], result=None)
add(id="S1-F-002", type="전망", importance=3, status="유효", forecast_status="진행 중",
    statement="2026년 연말 쇼핑 시즌(11~12월) 미국 리테일 AI 유입은 전년보다 50% 이상 늘고, 전환율은 비AI 유입보다 높을 것이다.", due="2027-01-31", condition="없음",
    method="Adobe 연말 쇼핑 시즌 보고서 확인", basis=["S1-M-003"], result=None)
add(id="S1-F-003", type="전망", importance=2, status="유효", forecast_status="진행 중",
    statement="네이버는 2026년 4분기 실적 발표에서 AI 브리핑 적용 비율이 통합검색의 35% 이상이라고 밝힐 것이다.", due="2027-02-28", condition="네이버가 비율을 공개할 경우",
    method="네이버 2026년 4분기 실적 발표 확인", basis=["S1-M-014"], result=None)
add(id="S1-F-004", type="전망", importance=3, status="유효", forecast_status="진행 중",
    statement="2026년 말까지 구글이 AI Mode 또는 AI 요약 안 광고를 미국 광고주 전체로 정식 확대한다고 발표할 것이다.", due="2026-12-31", condition="없음",
    method="Google 공식 발표 확인", basis=["S1-E-004"], result=None)
add(id="S1-F-005", type="전망", importance=2, status="유효", forecast_status="진행 중",
    statement="2026년 하반기 미국 구글 검색의 제로클릭 비율은 70% 이상으로 집계될 것이다.", due="2027-03-31", condition="같은 방식의 집계가 발표될 경우",
    method="SparkToro·Similarweb 제로클릭 집계 확인", basis=["S1-M-004"], result=None)
add(id="S1-F-006", type="전망", importance=2, status="유효", forecast_status="진행 중",
    statement="2027년 상반기 AI 유입에서 ChatGPT의 점유율은 85% 미만으로 내려갈 것이다(Gemini 등 확대).", due="2027-07-31", condition="없음",
    method="GA4 패널 기반 AI 유입 보고서(Previsible·Conductor 등) 확인", basis=["S1-M-002", "S1-M-001"], result=None)

# ---------- 메인 질문 시나리오 ----------
add(id="S1-F-101", type="전망", importance=3, status="유효", forecast_status="진행 중", scenario="낙관",
    statement="2027년 말까지 AI 유입이 검색 손실의 일부를 메우는 '두 번째 검색'으로 자리 잡는다. AI 유입 비중이 3%를 넘고 전환율 우위가 유지되며, 브랜드는 인용 측정과 AI 답변 광고로 노출을 관리할 수 있게 된다.",
    milestones=[
        {"by": "2026-12", "text": "AI 유입 비중 2% 이상 (Conductor)"},
        {"by": "2027-01", "text": "연말 시즌 AI 유입 +50% 이상, 전환율 우위 유지"},
        {"by": "2027-06", "text": "AI 답변 광고 정식화, 측정 지표가 광고 상품에 포함"}],
    due="2027-12-31", condition="AI 플랫폼이 외부 링크 노출을 크게 줄이지 않을 경우",
    method="세 가지 중 두 가지 이상 충족 시 적중: (1) 공개 벤치마크의 AI 유입 비중 3% 이상 (2) Adobe 기준 AI 유입 전환율이 비AI보다 높음 (3) 구글 또는 OpenAI가 AI 답변 광고를 정식 출시",
    basis=["S1-M-001", "S1-M-003", "S1-E-004", "S1-E-001"],
    signposts=[{"id": "S1-F-001", "on_hit": "낙관", "on_miss": "비관"}, {"id": "S1-F-002", "on_hit": "낙관", "on_miss": "비관"},
               {"id": "S1-F-004", "on_hit": "낙관"}, {"id": "S1-F-005", "on_hit": "비관", "on_miss": "낙관"}], result=None)
add(id="S1-F-102", type="전망", importance=3, status="유효", forecast_status="진행 중", scenario="비관",
    statement="2027년 말까지 AI 답변이 클릭을 흡수해 브랜드 사이트 유입은 계속 줄고, AI 유입은 2% 아래에 머문다. 노출은 플랫폼 안 광고와 거래로 넘어가, 브랜드는 돈을 내야 보이는 구조가 된다.",
    milestones=[
        {"by": "2027-01", "text": "연말 시즌 AI 유입 증가 둔화"},
        {"by": "2027-03", "text": "제로클릭 70% 이상"},
        {"by": "2027-06", "text": "AI 답변 내 결제·할인 제안 확대로 사이트 방문 없는 구매 증가"}],
    due="2027-12-31", condition="없음",
    method="낙관 시나리오의 판정 조건 세 가지 중 하나 이하만 충족 시 적중",
    basis=["S1-M-004", "S1-M-006", "S1-M-001"], signposts=[], result=None)

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

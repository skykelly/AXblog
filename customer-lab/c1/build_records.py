"""C1 R1 4유형 기록 생성 + 규칙 검증.
출력: q1/records.jsonl
"""
import json, sys
from pathlib import Path

R = "R1"
SRC = {
 "msit": {"url": "https://www.kyeonggi.com/article/20260331580533", "publisher": "경기일보 (과기정통부 2025 인터넷 이용 실태조사 보도)", "date": "2026-03-31", "grade": "B"},
 "cjmezzo": {"url": "https://www.newsis.com/view/NISX20260526_0003644106", "publisher": "뉴시스 (CJ메조미디어 2026 디지털 라이프스타일 리포트)", "date": "2026-05-27", "grade": "B"},
 "sparktoro": {"url": "https://sparktoro.com/blog/in-2026-less-than-one-third-of-google-searches-still-send-a-click/", "publisher": "SparkToro (Similarweb 패널)", "date": "2026-06", "grade": "A"},
 "sel": {"url": "https://searchengineland.com/google-zero-click-searches-2026-study-479717", "publisher": "Search Engine Land", "date": "2026-06", "grade": "B"},
 "pew": {"url": "https://www.pewresearch.org/short-reads/2025/07/22/google-users-are-less-likely-to-click-on-links-when-an-ai-summary-appears-in-the-results/", "publisher": "Pew Research Center", "date": "2025-07-22", "grade": "A"},
 "adobe_jul": {"url": "https://www.digitalcommerce360.com/2026/08/19/adobe-ai-referral-traffic-data-july-2026/", "publisher": "Digital Commerce 360 (Adobe Analytics)", "date": "2026-08-19", "grade": "B"},
 "adobe_pdf": {"url": "https://business.adobe.com/assets/pdfs/resources/sdk/ai-traffic-trends-report-august-2026/ai-traffic-trends-report-2026-08-19.pdf", "publisher": "Adobe Digital Insights", "date": "2026-08-19", "grade": "A"},
 "adobe_q1": {"url": "https://decrypt.co/364733/ai-traffic-us-retailers-jumps-q1-agentic-shoppers-outspend-humans", "publisher": "Decrypt (Adobe Analytics)", "date": "2026-04", "grade": "B"},
 "criteo_kr": {"url": "https://www.criteo.com/kr/wp-content/uploads/sites/7/2026/06/보도자료_크리테오-2026-커머스와-AI-트렌드-리포트-공개-for-Web.pdf", "publisher": "Criteo 보도자료", "date": "2026-06-10", "grade": "A"},
 "prain": {"url": "https://ditoday.com/?p=150713", "publisher": "디지털인사이트 (프레인글로벌·한국PR학회 조사)", "date": "2026", "grade": "B"},
 "accenture": {"url": "https://www.accenture.com/gb-en/insights/consulting/talk-my-ai-agent", "publisher": "Accenture Consumer Pulse 2026", "date": "2026-06-03", "grade": "A"},
 "riskified": {"url": "https://ir.riskified.com/node/8896/pdf", "publisher": "Riskified IR", "date": "2026-04-27", "grade": "A"},
 "naver_ai_tab": {"url": "https://byline.network/2026/06/26_12083847/", "publisher": "바이라인네트워크", "date": "2026-06-26", "grade": "B"},
 "segye_ai_tab": {"url": "https://www.segye.com/newsView/20260626507402", "publisher": "세계일보", "date": "2026-06-26", "grade": "B"},
 "naver_shop_ga": {"url": "https://byline.network/2026/07/0701-2/", "publisher": "바이라인네트워크", "date": "2026-07-01", "grade": "B"},
 "naver_shop_beta": {"url": "https://navercorp.com/media/pressReleasesDetail?seq=34353", "publisher": "네이버 보도자료", "date": "2026-02-26", "grade": "A"},
 "openai_pivot": {"url": "https://forklog.com/en/openai-abandons-instant-checkout-feature-in-chatgpt/amp", "publisher": "ForkLog (The Information 인용)", "date": "2026-03-23", "grade": "B"},
 "m4e": {"url": "https://marketing4ecommerce.net/en/openai-abandon-instant-checkout/", "publisher": "Marketing4eCommerce", "date": "2026-03-06", "grade": "B"},
 "everythingpr": {"url": "https://everything-pr.com/agentic-commerce-chatgpt-gemini-checkout", "publisher": "Everything PR", "date": "2026", "grade": "C"},
 "godberry": {"url": "https://godberrystudios.com/posts/agentic-commerce-2026-chatgpt-shopify-visa-merchant-playbook/", "publisher": "Godberry Studios 블로그", "date": "2026", "grade": "C"},
 "shopappy": {"url": "https://shopappy.com/?p=9025", "publisher": "Shopappy 블로그", "date": "2026", "grade": "C"},
 "techinsider": {"url": "https://tech-insider.org/?p=21278", "publisher": "Tech Insider", "date": "2026-09", "grade": "C"},
}

def src(*keys):
    return [dict(SRC[k], key=k) for k in keys]

base = dict(question="C1", question_version="v1.0", first_seen=R, last_seen=R, status="유효", replaces=None, check_flags=[])
records = []
def add(**kw):
    r = dict(base); r.update(kw); records.append(r)

# ---------- 지표 (M) ----------
add(id="C1-M-001", type="지표", indicator="C1-T1", importance=3, statement="한국 국민의 생성형 AI 서비스 경험률은 2025년 44.5%로 전년(33.3%)보다 11.2%p 올랐다.",
    value=44.5, unit="%", as_of="2025", region="KR", definition="과기정통부 인터넷 이용 실태조사, 생성형 AI 서비스 경험률", prev_value=33.3,
    sources=src("msit"), verified=True, verified_note="보도 원문 확인, 정부 원보고서는 미대조", representative=True)
add(id="C1-M-002", type="지표", indicator="C1-T1", importance=1, statement="민간 온라인 조사에서는 생성형 AI 이용 경험 88%, 최근 1년 유료 구독 경험 43%로 나타났다.",
    value=88, unit="%", as_of="2026-05", region="KR", definition="CJ메조미디어 온라인 조사, 이용 경험", sources=src("cjmezzo"), verified=True,
    representative=False, check_flags=["수치 충돌: C1-M-001과 정의·표본 차이(온라인 패널). 대표값은 C1-M-001"])
add(id="C1-M-003", type="지표", indicator="C1-T3", importance=3, statement="2026년 1~4월 미국 구글 검색의 68.01%가 클릭 없이 끝났다(2024년 60.45%).",
    value=68.01, unit="%", as_of="2026-01~04", region="US", definition="SparkToro, Similarweb 웹 패널 기준 zero-click 비율(앱 제외)", prev_value=60.45,
    sources=src("sparktoro", "sel"), verified=True)
add(id="C1-M-004", type="지표", indicator="C1-T3", importance=2, statement="구글 AI 요약이 뜬 검색에서 일반 결과 클릭은 8%로, 요약이 없을 때(15%)의 절반 수준이었다.",
    value=8, unit="%", as_of="2025-03", region="US", definition="Pew, 900명 브라우징 데이터, AI 요약 노출 시 일반 결과 클릭률", prev_value=15,
    sources=src("pew"), verified=True, check_flags=["기준 시점이 조사 기간(최근 12개월) 밖 — 기준선 용도"])
add(id="C1-M-005", type="지표", indicator="C1-T3", importance=2, statement="2026년 1~4월 구글 검색 중 AI Mode로 넘어간 비율은 0.34%에 그쳤다.",
    value=0.34, unit="%", as_of="2026-01~04", region="US", definition="SparkToro, AI Mode 전환 검색 비율", sources=src("sparktoro"), verified=True)
add(id="C1-M-006", type="지표", indicator="C1-T4", importance=3, statement="2026년 7월 미국 리테일 사이트의 AI 유입 트래픽은 전년 대비 62% 늘었고, 전환율은 비AI 유입보다 60% 높았다.",
    value=62, unit="% YoY", as_of="2026-07", region="US", definition="Adobe Analytics, 생성형 AI 경유 리테일 방문 증가율", extra={"conversion_vs_nonAI": "+60%", "revenue_per_visit_vs_nonAI": "+53%", "engagement_vs_nonAI": "+14%"},
    sources=src("adobe_jul", "adobe_pdf"), verified=True)
add(id="C1-M-007", type="지표", indicator="C1-T4", importance=2, statement="2026년 1분기 미국 리테일 AI 유입 트래픽은 전년 대비 393% 늘었고, 3월 기준 전환율은 비AI 대비 42% 높았다(1년 전에는 38% 낮았음).",
    value=393, unit="% YoY", as_of="2026-C1", region="US", definition="Adobe Analytics, 분기 증가율", sources=src("adobe_q1"), verified=True)
add(id="C1-M-008", type="지표", indicator="C1-T5", importance=3, statement="AI 쇼핑 어시스턴트를 주요 쇼핑 수단으로 쓴다는 한국 소비자는 7%로, 6개국 평균(14%)의 절반이었다.",
    value=7, unit="%", as_of="2026-01~02", region="KR", definition="Criteo 6개국 6,379명(한국 1,107명) 설문", global_value=14, sources=src("criteo_kr"), verified=True)
add(id="C1-M-009", type="지표", indicator="C1-T5", importance=2, statement="한국 소비자의 제품 탐색 시작점은 마켓플레이스 59%, 검색엔진 20% 순이었다.",
    value=59, unit="%", as_of="2026-01~02", region="KR", definition="Criteo 설문, 탐색 시작 채널", sources=src("criteo_kr"), verified=True)
add(id="C1-M-010", type="지표", indicator="C1-T5", importance=2, statement="수도권 생성형 AI 이용자의 49.9%가 최근 3개월 내 AI가 추천한 제품·서비스를 샀고, 구매 시 첫 채널은 포털 검색 54.2%, 생성형 AI 14.0%였다.",
    value=49.9, unit="%", as_of="2026", region="KR", definition="프레인글로벌·한국PR학회, 수도권 AI 이용 경험자 1,000명", sources=src("prain"), verified=True,
    check_flags=["표본이 AI 이용 경험자로 한정 — 전체 소비자 비율 아님"])
add(id="C1-M-011", type="지표", indicator="C1-T6", importance=3, statement="16개국 소비자 중 32%는 예산·브랜드 범위 안에서 AI 에이전트가 고르게 하겠다고 했지만, 결제까지 맡기겠다는 응답은 9%였다.",
    value=9, unit="%", as_of="2026-01", region="GLOBAL", definition="Accenture Consumer Pulse 2026, 16개국 25,590명, 완전 자율 구매 허용", extra={"conditional_choice": "32%", "trust_more_than_friend": "74%"},
    sources=src("accenture"), verified=True)
add(id="C1-M-012", type="지표", indicator="C1-T6", importance=2, statement="미국·영국 소비자의 61.5%가 상품 탐색에 AI를 썼지만 55.0%는 AI 에이전트의 대리 구매가 불편하다고 답했다.",
    value=55.0, unit="%", as_of="2026-C1", region="US/UK", definition="Riskified Agentic Commerce Pulse, 2,000명", sources=src("riskified"), verified=True)
add(id="C1-M-013", type="지표", indicator="C1-T6", importance=2, statement="AI 쇼핑에서 허위·편향 정보를 우려하는 한국 소비자는 64%(평균 52%), 결제정보 제공이 부담스럽다는 응답은 53%(평균 46%)였다.",
    value=64, unit="%", as_of="2026-01~02", region="KR", definition="Criteo 설문, 우려 요인", sources=src("criteo_kr"), verified=True)
add(id="C1-M-014", type="지표", indicator="C1-T8", importance=2, statement="네이버 AI탭은 베타 2개월 동안 누적 사용자 400만 명, 상품·장소 카드 클릭률 각각 20% 이상을 기록했다.",
    value=400, unit="만 명(누적)", as_of="2026-06", region="KR", definition="네이버 발표 수치", sources=src("naver_ai_tab"), verified=True)
add(id="C1-M-015", type="지표", indicator="C1-T8", importance=2, statement="네이버 쇼핑 AI 에이전트의 6월 일간 이용자는 3월보다 50% 이상 늘었고, 에이전트 경유 거래액은 2.7배 이상 증가했다.",
    value=2.7, unit="배(거래액)", as_of="2026-06", region="KR", definition="네이버 발표, 3월 대비", extra={"long_tail_queries": "이용자 70% 이상이 15자 이상 질의"},
    sources=src("naver_shop_ga"), verified=True)

# ---------- 사건 (E) ----------
add(id="C1-E-001", type="사건", importance=2, statement="OpenAI가 ChatGPT 안에서 결제까지 끝내는 Instant Checkout을 출시했다.", date="2025-09", actor="OpenAI",
    sources=src("openai_pivot", "m4e"), verified=True, check_flags=["출시일 출처마다 9/29·10/14 상이 — 월 단위로 기록"])
add(id="C1-E-002", type="사건", importance=3, statement="OpenAI가 Instant Checkout을 접고, 구매는 ChatGPT 안의 리테일러 앱이나 판매자 사이트에서 끝내는 방식으로 전환했다.", date="2026-03", actor="OpenAI",
    sources=src("openai_pivot", "m4e"), verified=True, check_flags=["보도일 3/4~3/24로 상이 — 월 단위로 기록"])
add(id="C1-E-003", type="사건", importance=2, statement="Google이 Gemini와 AI Mode에서 결제를 지원하는 개방형 Universal Commerce Protocol을 발표했다.", date="2026-01-11", actor="Google",
    sources=src("everythingpr"), verified=False, check_flags=["출처 등급 C — 다음 회차 원문(Google 발표) 확인 필요"])
add(id="C1-E-004", type="사건", importance=1, statement="Microsoft가 Copilot 대화 안에서 구매하는 Copilot Checkout을 출시했다.", date="2026-01-08", actor="Microsoft",
    sources=src("godberry"), verified=False, check_flags=["출처 등급 C — 원문 확인 필요"])
add(id="C1-E-005", type="사건", importance=1, statement="Shopify가 미국 판매자의 상품을 ChatGPT·Copilot·Gemini·AI Mode에 기본 노출하는 Agentic Storefronts를 켰다.", date="2026-03-24", actor="Shopify",
    sources=src("godberry"), verified=False, check_flags=["출처 등급 C — 원문 확인 필요"])
add(id="C1-E-006", type="사건", importance=1, statement="Salesforce가 ChatGPT와 연동되는 리테일러 통제형 Agentforce Commerce를 정식 출시했다.", date="2026-07-06", actor="Salesforce",
    sources=src("shopappy"), verified=False, check_flags=["출처 등급 C — 원문 확인 필요"])
add(id="C1-E-007", type="사건", importance=2, statement="네이버가 네이버플러스 스토어 앱에 쇼핑 AI 에이전트 베타를 출시했다(요약·비교·리뷰 분석).", date="2026-02-26", actor="네이버",
    sources=src("naver_shop_beta"), verified=True)
add(id="C1-E-008", type="사건", importance=2, statement="네이버 쇼핑 AI 에이전트가 4개월 베타를 마치고 정식 출시됐으며, 하반기 장바구니·배송 기능 추가 계획을 밝혔다.", date="2026-06-25", actor="네이버",
    sources=src("naver_shop_ga"), verified=True)
add(id="C1-E-009", type="사건", importance=3, statement="네이버가 대화형 검색 AI탭을 전체 이용자에게 정식 출시하고 모바일 검색의 그린닷을 AI탭으로 교체했다.", date="2026-06-25", actor="네이버",
    sources=src("naver_ai_tab", "segye_ai_tab"), verified=True)
add(id="C1-E-010", type="사건", importance=2, statement="Google이 I/O 2026에서 AI Mode 월 사용자가 10억 명을 넘었고 질의량이 분기마다 2배 이상 늘고 있다고 밝혔다.", date="2026-05", actor="Google",
    sources=src("sparktoro"), verified=True, verified_note="SparkToro가 Google 발표를 인용 — Google 원문 미대조")
add(id="C1-E-011", type="사건", importance=1, statement="Anthropic이 쇼핑·판매자 운영 에이전트 구축용 Claude Commerce Agents를 공개했다.", date="2026-09-02", actor="Anthropic",
    sources=src("techinsider"), verified=False, check_flags=["출처 등급 C — 원문 확인 필요"])

# ---------- 해석 (I) ----------
add(id="C1-I-001", type="해석", importance=3, target="탐색(Search) 단계", direction="강화",
    statement="정보 탐색의 끝점이 웹사이트에서 검색 결과 화면의 AI 답변으로 옮겨가고 있다. 다만 미국에서도 전용 AI 검색(AI Mode) 이용은 아직 작다.",
    basis=["C1-M-003", "C1-M-004", "C1-M-005", "C1-E-010"])
add(id="C1-I-002", type="해석", importance=3, target="추천(Recommendation) 단계", direction="강화",
    statement="AI 경유 방문은 양은 작지만 이미 후보가 좁혀진 상태로 들어와 전환율이 비AI 유입을 앞질렀다. 추천 단계는 AI가 실질적으로 맡기 시작했다.",
    basis=["C1-M-006", "C1-M-007", "C1-M-010"])
add(id="C1-I-003", type="해석", importance=3, target="위임(Delegation) 단계", direction="약화",
    statement="소비자는 조건부 선택까지는 맡기겠다고 하지만 결제 위임은 소수이고, 대표 사례인 인챗 결제도 철회됐다. 위임은 리테일러가 결제를 쥔 채 AI 창구에 연결되는 형태로 수렴하고 있다.",
    basis=["C1-M-011", "C1-M-012", "C1-E-001", "C1-E-002"])
add(id="C1-I-004", type="해석", importance=3, target="한국 탐색 주도권", direction="강화",
    statement="한국에서는 범용 AI 챗봇보다 네이버 같은 기존 플랫폼 안의 AI가 탐색 단계를 흡수하고 있다. 탐색은 여전히 마켓플레이스와 포털에서 시작하고, 그 안에 AI가 들어가는 구조다.",
    basis=["C1-M-009", "C1-M-010", "C1-M-014", "C1-M-015", "C1-E-007", "C1-E-009"])
add(id="C1-I-005", type="해석", importance=2, target="한국 소비자 의사결정 주도권", direction="중립",
    statement="한국 소비자는 AI 이용률은 높지만 AI를 주 쇼핑 수단으로 쓰는 비율은 낮고 정보 신뢰 우려가 크다. 최종 판단은 본인이 쥐고 AI는 비교·검증 보조로 쓰는 단계다.",
    basis=["C1-M-001", "C1-M-008", "C1-M-013"])
add(id="C1-I-006", type="해석", importance=2, target="AI 유입 트래픽 성장 속도", direction="중립",
    statement="미국 AI 유입 트래픽의 증가율은 1분기 393%에서 7월 62%로 빠르게 낮아졌다. 기저가 커진 영향이며, 성장의 무게가 양에서 질(전환)로 옮겨가고 있다.",
    basis=["C1-M-006", "C1-M-007"])

# ---------- 전망 (F) ----------
add(id="C1-F-001", type="전망", importance=2, status="유효", forecast_status="진행 중",
    statement="Adobe의 2026년 연말 쇼핑 시즌(11~12월) 집계에서 미국 리테일 AI 유입 트래픽 증가율은 전년 대비 100% 미만으로 발표될 것이다.",
    due="2027-01-31", condition="Adobe가 연말 시즌 집계를 발표할 경우", method="Adobe Digital Insights 2026 holiday recap의 AI 유입 트래픽 YoY 수치 확인", basis=["C1-M-006", "C1-M-007", "C1-I-006"], result=None)
add(id="C1-F-002", type="전망", importance=3, status="유효", forecast_status="진행 중",
    statement="2027년 3월 말까지 ChatGPT가 미국 전체 사용자 대상으로 대화 안 결제(인챗 체크아웃)를 다시 출시하지 않을 것이다.",
    due="2027-03-31", condition="없음", method="OpenAI 공식 발표·도움말에서 ChatGPT 내 결제 기능의 전체 사용자 출시 여부 확인", basis=["C1-E-002", "C1-M-012", "C1-I-003"], result=None)
add(id="C1-F-003", type="전망", importance=2, status="유효", forecast_status="진행 중",
    statement="네이버는 2026년 안에 AI탭에 광고 상품을 도입한다고 발표할 것이다.",
    due="2026-12-31", condition="없음", method="네이버 보도자료·실적발표에서 AI탭 광고 도입 발표 확인", basis=["C1-E-009", "C1-M-014"], result=None)
add(id="C1-F-004", type="전망", importance=2, status="유효", forecast_status="진행 중",
    statement="과기정통부 2026 인터넷 이용 실태조사의 생성형 AI 경험률은 55% 이상으로 나올 것이다.",
    due="2027-04-30", condition="조사 문항 정의가 2025년과 같을 경우", method="과기정통부 2026 인터넷 이용 실태조사 발표 수치 확인", basis=["C1-M-001"], result=None)
add(id="C1-F-005", type="전망", importance=2, status="유효", forecast_status="진행 중",
    statement="Accenture의 다음 Consumer Pulse에서도 결제까지 AI에 맡기겠다는 응답은 15% 미만일 것이다.",
    due="2027-07-31", condition="같은 문항이 반복될 경우", method="Accenture Consumer Pulse 2027의 완전 자율 구매 응답 비율 확인", basis=["C1-M-011", "C1-M-012"], result=None)

add(id="C1-F-006", type="전망", importance=2, status="유효", forecast_status="진행 중",
    statement="네이버 쇼핑 AI 에이전트는 2026년 안에 대화 중 장바구니 담기 기능을 출시할 것이다.",
    due="2026-12-31", condition="없음", method="네이버 발표·앱 기능에서 에이전트 대화 내 장바구니 담기 제공 여부 확인", basis=["C1-E-008", "C1-M-015"], result=None)

# ---------- 메인 질문 시나리오 전망 (낙관·비관) ----------
# signposts: 세부 전망의 판정 결과가 어느 시나리오 쪽 신호인지 (적중/빗나감 → 낙관/비관)
add(id="C1-F-101", type="전망", importance=3, status="유효", forecast_status="진행 중", scenario="낙관",
    statement="2027년 말까지 AI는 반복 구매와 저관여 상품에서 '결정'을 대신하기 시작한다. 미국에서는 대화 안에서 결제까지 끝내는 구매가 주요 AI 서비스에 다시 열리고, 한국에서는 네이버 쇼핑 에이전트가 장바구니·결제까지 연결된다. 결제까지 AI에 맡기겠다는 소비자는 15%를 넘는다.",
    milestones=[
        {"by": "2026-12", "text": "네이버 쇼핑 에이전트에 장바구니 담기 출시, AI탭 광고 도입"},
        {"by": "2027-06", "text": "ChatGPT·Gemini 중 하나 이상이 미국 전체 사용자에게 대화 내 결제 제공"},
        {"by": "2027-12", "text": "결제 위임 의향 15% 이상, 한국 '결정' 단계가 확산으로 이동"}],
    due="2027-12-31", condition="결제 사고·규제 이슈가 대형 사건으로 번지지 않을 경우",
    method="세 가지 중 두 가지 이상 충족 시 적중: (1) 미국 주요 AI 서비스의 전체 사용자 대상 대화 내 결제 제공 (2) 글로벌 소비자 조사에서 결제 위임 의향 15% 이상 (3) 네이버 쇼핑 에이전트의 장바구니·결제 연결 출시",
    basis=["C1-M-006", "C1-M-015", "C1-E-008", "C1-M-011"],
    signposts=[{"id": "C1-F-002", "on_miss": "낙관"}, {"id": "C1-F-003", "on_hit": "낙관"}, {"id": "C1-F-004", "on_hit": "낙관"},
               {"id": "C1-F-005", "on_miss": "낙관"}, {"id": "C1-F-006", "on_hit": "낙관"}], result=None)
add(id="C1-F-102", type="전망", importance=3, status="유효", forecast_status="진행 중", scenario="비관",
    statement="2027년 말에도 AI는 '추천'까지만 대신한다. 결정과 결제는 리테일러 사이트와 앱에 남고, AI는 그 앞의 검색·비교 창구 역할에 머문다. 결제 위임 의향은 10% 안팎에 머물고, 한국은 기존 플랫폼 안 AI가 검색을 대체할 뿐 구매 결정은 소비자가 계속 쥔다.",
    milestones=[
        {"by": "2027-01", "text": "Adobe 연말 집계에서 AI 유입 트래픽 증가율이 100% 아래로 둔화"},
        {"by": "2027-03", "text": "ChatGPT 대화 내 결제 재출시 없음, 리테일러 앱 연결 방식 유지"},
        {"by": "2027-12", "text": "결제 위임 의향 15% 미만 유지, 한국 '결정' 단계는 얼리어답터에 머묾"}],
    due="2027-12-31", condition="없음",
    method="낙관 시나리오의 판정 조건 세 가지 중 하나 이하만 충족 시 적중",
    basis=["C1-E-002", "C1-M-011", "C1-M-012", "C1-M-008", "C1-M-013"],
    signposts=[{"id": "C1-F-001", "on_hit": "비관"}, {"id": "C1-F-002", "on_hit": "비관"}, {"id": "C1-F-005", "on_hit": "비관"},
               {"id": "C1-F-006", "on_miss": "비관"}], result=None)

# ---------- 검증 ----------
ids = {r["id"] for r in records}
facts = {r["id"] for r in records if r["type"] in ("지표", "사건")}
errs = []
_t = {r["id"]: r["type"] for r in records}
def by_type(i): return _t.get(i)
for r in records:
    if r["type"] in ("지표", "사건"):
        if not r.get("sources") or not all(s.get("url") for s in r["sources"]):
            errs.append(f"{r['id']}: 원문 링크 없음")
    if r["type"] == "해석":
        if not set(r.get("basis", [])) & facts:
            errs.append(f"{r['id']}: 사실 기록 연결 없음")
        if r.get("direction") not in ("강화", "약화", "중립"):
            errs.append(f"{r['id']}: 방향 값 오류")
    if r["type"] == "전망":
        for f in ("due", "method", "basis"):
            if not r.get(f):
                errs.append(f"{r['id']}: {f} 없음")
        if not set(r["basis"]) & facts:
            errs.append(f"{r['id']}: 해석에만 기대는 전망")
    for sp in r.get("signposts", []):
        if sp["id"] not in ids or by_type(sp["id"]) != "전망":
            errs.append(f"{r['id']}: 판정 신호 {sp['id']}가 세부 전망이 아님")
    if r.get("scenario") and r["scenario"] not in ("낙관", "비관"):
        errs.append(f"{r['id']}: 시나리오 값 오류")
    for b in r.get("basis", []):
        if b not in ids:
            errs.append(f"{r['id']}: 존재하지 않는 근거 {b}")
if len(ids) != len(records):
    errs.append("중복 ID")

with open(Path(__file__).parent / "records.jsonl", "w", encoding="utf-8") as f:
    for r in records:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")

from collections import Counter
print("기록 수:", len(records), dict(Counter(r["type"] for r in records)))
print("원문 미확인 사실:", [r["id"] for r in records if r["type"] in ("지표","사건") and not r.get("verified")])
inds = {r.get("indicator") for r in records if r["type"] == "지표"}
print("값 채워진 추적 지표:", sorted(i for i in inds if i), f"{len(inds)}/8")
print("검증 오류:", errs or "없음")
sys.exit(1 if errs else 0)

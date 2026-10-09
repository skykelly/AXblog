"""S2 R1 4유형 기록 생성 + 규칙 검증.
출력: i4/records.jsonl
"""
import json, sys
from pathlib import Path
from collections import Counter

R = "R1"
SRC = {
 "rufus": {"url": "https://www.modernretail.co/technology/amazon-says-its-ai-shopping-assistant-is-gaining-traction-with-rufus-users-up-115/", "publisher": "Modern Retail (Amazon 실적 발표)", "date": "2026-04-30", "grade": "B"},
 "walmart": {"url": "https://ppc.land/walmarts-chatgpt-checkout-flopped-heres-what-comes-next/", "publisher": "PPC Land (WIRED 인터뷰·Walmart 발표 인용)", "date": "2026-03-22", "grade": "B"},
 "shopify": {"url": "https://www.retailtouchpoints.com/news/shopify-credits-ai-for-34-revenue-growth-in-q2-2026/620805/", "publisher": "Retail TouchPoints (Shopify 2분기 실적)", "date": "2026-08-05", "grade": "B"},
 "forrester": {"url": "https://www.forrester.com/blogs/agentic-payments-in-b2c-commerce-where-we-are-now/", "publisher": "Forrester", "date": "2026-04", "grade": "B"},
 "visa_onchain": {"url": "https://www.visa.com/en-us/thought-leadership/innovation/agentic-payments-from-the-ground-up", "publisher": "Visa (Artemis 온체인 데이터)", "date": "2026-07-14", "grade": "A"},
 "fee": {"url": "https://www.techradar.com/pro/what-openais-4-percent-checkout-fee-means-for-the-future-of-commerce", "publisher": "TechRadar", "date": "2026-03-24", "grade": "B"},
 "rufus_ads": {"url": "https://www.shopifreaks.com/amazon-reveals-pricing-and-measurement-details-for-sponsored-ads-inside-rufus-ai-shopping-assistant/", "publisher": "Shopifreaks (Adweek 보도 인용)", "date": "2026-04-01", "grade": "B"},
 "ms": {"url": "https://morganstanley.com/insights/articles/agentic-commerce-market-impact-outlook", "publisher": "Morgan Stanley", "date": "2025-12-08", "grade": "A"},
 "naver_agent": {"url": "https://byline.network/2026/07/0701-2/", "publisher": "바이라인네트워크", "date": "2026-07-01", "grade": "B"},
 "kakao_q1": {"url": "https://v.daum.net/v/20260507121150759", "publisher": "다음 뉴스 (카카오 1분기 실적 발표)", "date": "2026-05-07", "grade": "B"},
 "kakao_q2": {"url": "https://m.ddaily.co.kr/page/view/2026080609174229488", "publisher": "디지털데일리 (카카오 2분기 실적 발표)", "date": "2026-08-06", "grade": "B"},
 "openai_end": {"url": "https://forklog.com/en/openai-abandons-instant-checkout-feature-in-chatgpt/amp", "publisher": "ForkLog (The Information 인용)", "date": "2026-03-23", "grade": "B"},
 "ucp": {"url": "https://blog.google/products/ads-commerce/agentic-commerce-ai-tools-protocol-retailers-platforms/", "publisher": "Google 공식 블로그", "date": "2026-01-11", "grade": "A"},
 "amz_block": {"url": "https://www.geekwire.com/2026/judge-blocks-perplexitys-ai-bot-from-shopping-on-amazon-in-early-test-of-agentic-commerce/", "publisher": "GeekWire", "date": "2026-03-10", "grade": "B"},
 "amz_appeal": {"url": "https://www.eweek.com/news/perplexity-ai-shopping-agent-returns-amazon/", "publisher": "eWeek (Reuters 인용)", "date": "2026-08-05", "grade": "B"},
 "visa_apac": {"url": "https://www.visa.com.sg/about-visa/newsroom/press-releases/visa-launches-agentic-ready-program-in-asia-pacific-with-over-50-partners-advancing-agentic-commerce.html", "publisher": "Visa 보도자료", "date": "2026-04-30", "grade": "A"},
 "naver_ad": {"url": "https://www.segye.com/newsView/20260626507402", "publisher": "세계일보", "date": "2026-06-26", "grade": "B"},
}
def src(*keys): return [dict(SRC[k], key=k) for k in keys]

base = dict(question="S2", question_version="v1.0", first_seen=R, last_seen=R, status="유효", replaces=None, check_flags=[])
records = []
def add(**kw):
    r = dict(base); r.update(kw); records.append(r)

# ---------- 지표 (M) ----------
add(id="S2-M-001", type="지표", indicator="S2-T1", importance=3, statement="Amazon의 쇼핑 에이전트 Rufus는 2025년 고객 3억 명이 썼고, 연환산 약 120억 달러의 증분 매출을 만들었다. Rufus를 쓰는 고객은 구매를 끝낼 가능성이 60% 높다.",
    value=3, unit="억 명 (Rufus 이용 고객)", as_of="2025", region="US", definition="유통사 자체 쇼핑 에이전트 이용 고객", extra={"incremental_sales": "연환산 약 120억 달러", "purchase_likelihood": "+60%"},
    sources=src("rufus"), verified=True, check_flags=["증분 매출은 회사 자체 추정"])
add(id="S2-M-002", type="지표", indicator="S2-T1", importance=2, statement="Walmart 앱 이용자의 절반이 쇼핑 에이전트 Sparky를 써 봤고, Sparky 이용자는 주문당 약 35% 더 쓴다.",
    value=50, unit="% (앱 이용자 중 Sparky 사용)", as_of="2026-03", region="US", definition="Walmart 앱 이용자 중 Sparky 사용 비율", extra={"order_value": "+35%"},
    sources=src("walmart"), verified=True, check_flags=["임원 인터뷰·발표 수치"])
add(id="S2-M-003", type="지표", indicator="S2-T2", importance=3, statement="Shopify 상점으로 들어온 AI 경유 트래픽과 주문은 2026년 2분기에 1년 전의 3배가 됐다. AI 채널에서는 신규 구매자 주문 비율이 다른 채널의 약 2배이고, AI 유입의 절반이 상품 페이지로 바로 들어온다.",
    value=3, unit="배 (AI 경유 주문, 전년 대비)", as_of="2026-Q2", region="GLOBAL", definition="Shopify 상점의 AI 경유 트래픽·주문 증가", extra={"new_buyer_rate": "약 2배", "product_page_landing": "50%"},
    sources=src("shopify"), verified=True)
add(id="S2-M-004", type="지표", indicator="S2-T3", importance=3, statement="ChatGPT 안에서 바로 결제하는 Instant Checkout의 전환율은 Walmart 사이트로 넘어가 사는 경우의 3분의 1이었다.",
    value=0.33, unit="배 (사이트 이동 대비 전환율)", as_of="2026-03", region="US", definition="AI 대화 안 결제의 전환율, 유통사 사이트 이동 대비",
    sources=src("walmart", "forrester"), verified=True, check_flags=["Walmart 한 곳의 수치"])
add(id="S2-M-005", type="지표", indicator="S2-T4", importance=3, statement="카드망의 에이전트 결제는 아직 시험 규모다. Visa는 2025년 12월 시범에서 '수백 건'을, Mastercard는 2026년 3월 통제된 환경에서 실거래 1건을 완료했다. 반면 중국 Alipay의 AI 결제는 2월까지 1억 2천만 건에 이르렀다.",
    value=1.2, unit="억 건 (Alipay AI 결제, 비교 기준)", as_of="2026-02", region="GLOBAL", definition="에이전트가 시작한 결제 거래 수", extra={"visa_pilot": "수백 건", "mastercard": "1건 (통제 환경)"},
    sources=src("forrester"), verified=True)
add(id="S2-M-006", type="지표", indicator="S2-T4", importance=1, statement="기계 간 결제 프로토콜 x402는 2025년 5월 출시 이후 약 1억 1천만 건, 1,500만 달러를 처리했다. 건수는 많지만 금액은 작아 소비자 쇼핑과는 거리가 있다.",
    value=1500, unit="만 달러 (x402 누적)", as_of="2026-04", region="GLOBAL", definition="x402 프로토콜 조정 거래액", extra={"transactions": "약 1억 960만 건"},
    sources=src("visa_onchain"), verified=True)
add(id="S2-M-007", type="지표", indicator="S2-T5", importance=3, statement="OpenAI는 ChatGPT에서 결제된 Shopify 판매자 주문에 4% 수수료를 매겼다. Amazon 마켓플레이스 판매 수수료(8~15%)보다 낮다.",
    value=4, unit="%", as_of="2026-03", region="US", definition="AI 플랫폼의 결제 거래 수수료", extra={"amazon_referral": "8~15%"},
    sources=src("fee"), verified=True, check_flags=["Instant Checkout 종료로 적용 범위 불확실"])
add(id="S2-M-008", type="지표", indicator="S2-T6", importance=2, statement="Amazon 광고 매출은 2026년 1분기 172억 달러로 24% 늘었다. Amazon은 Rufus 대화 안에 브랜드 질문형 광고를 클릭당 과금으로 붙이고 있다.",
    value=172, unit="억 달러 (Amazon 1분기 광고 매출)", as_of="2026-Q1", region="GLOBAL", definition="Amazon 광고 매출", extra={"yoy": "+24%", "rufus_ads": "CPC"},
    sources=src("rufus", "rufus_ads"), verified=True)
add(id="S2-M-009", type="지표", indicator="S2-T7", importance=2, statement="Morgan Stanley는 2030년 미국 에이전트 커머스를 1,900억~3,850억 달러, 온라인 소매의 약 10%(낙관 20%)로 전망했다. 미국인의 약 23%가 지난달 AI를 통해 무언가를 샀다고 추정했다.",
    value=10, unit="% (2030 온라인 소매 점유, 기본)", as_of="2025-12", region="US", definition="2030년 에이전트 커머스의 미국 온라인 소매 점유 전망", extra={"size": "1,900억~3,850억 달러", "bull": "20%"},
    sources=src("ms"), verified=True, check_flags=["전망치 — 사실 기록 아님"])
add(id="S2-M-010", type="지표", indicator="S2-T8", importance=3, statement="네이버 쇼핑 AI 에이전트의 6월 일간 이용자는 3월보다 50% 넘게 늘었고, 에이전트를 거친 거래액은 2.7배 이상 늘었다.",
    value=2.7, unit="배 (거래액, 3월 대비 6월)", as_of="2026-06", region="KR", definition="네이버 쇼핑 AI 에이전트 경유 거래액 증가", extra={"dau": "+50% 이상"},
    sources=src("naver_agent"), verified=True)
add(id="S2-M-011", type="지표", indicator="S2-T8", importance=2, statement="카카오는 카카오톡 AI 에이전트를 쓸 수 있는 이용자가 2026년 말 3,100만 명(카톡 월간 이용자의 약 62%)이 될 것으로 봤다.",
    value=3100, unit="만 명 (2026년 말 전망)", as_of="2026-05", region="KR", definition="카카오톡 AI 에이전트 이용 가능 이용자", sources=src("kakao_q1"), verified=True, check_flags=["회사 전망치"])

# ---------- 사건 (E) ----------
add(id="S2-E-001", type="사건", importance=3, statement="OpenAI가 ChatGPT 안에서 결제까지 끝내는 Instant Checkout을 출시했다. Etsy·Walmart·Shopify 판매자가 초기에 참여했다.",
    date="2025-09-29", actor="OpenAI", sources=src("openai_end"), verified=True)
add(id="S2-E-002", type="사건", importance=3, statement="구글이 탐색·구매·사후관리를 잇는 개방형 표준 Universal Commerce Protocol을 발표했다. 유통사가 판매 당사자로 남고, AI Mode·Gemini 안 결제(미국)와 브랜드 응대 Business Agent, AI Mode 할인 광고(Direct Offers) 시범을 함께 공개했다.",
    date="2026-01-11", actor="Google", sources=src("ucp"), verified=True)
add(id="S2-E-003", type="사건", importance=2, statement="미국 법원이 Perplexity의 쇼핑 에이전트가 Amazon에서 대신 쇼핑하는 것을 막는 가처분을 내렸다.",
    date="2026-03-09", actor="미국 연방법원", sources=src("amz_block"), verified=True)
add(id="S2-E-004", type="사건", importance=3, statement="OpenAI가 Instant Checkout을 접었다. 상품은 ChatGPT에서 찾되 결제는 유통사 앱·사이트에서 끝내는 방식으로 바꿨다. 업계는 통합의 복잡성과 부정확한 상품 데이터를 원인으로 꼽았다.",
    date="2026-03-23", actor="OpenAI", sources=src("openai_end", "forrester"), verified=True)
add(id="S2-E-005", type="사건", importance=3, statement="Walmart가 자사 쇼핑 에이전트 Sparky를 ChatGPT 안에 넣었다(4월 Gemini). 장바구니는 Walmart 사이트·앱과 동기화된다.",
    date="2026-03-25", actor="Walmart", sources=src("walmart"), verified=True)
add(id="S2-E-006", type="사건", importance=2, statement="Amazon이 Rufus 대화 안 광고(스폰서 상품·브랜드 질문 프롬프트)를 정식 판매 단계로 옮겼다.",
    date="2026-04-01", actor="Amazon", sources=src("rufus_ads"), verified=True, check_flags=["유출된 광고 제안서 기반 보도"])
add(id="S2-E-007", type="사건", importance=2, statement="Visa가 한국을 포함한 아태 10개 시장에서 에이전트 결제 준비 프로그램을 시작했다. 한국에서는 하나·현대·KB국민·삼성·신한카드와 카카오뱅크가 참여했다.",
    date="2026-04-30", actor="Visa", sources=src("visa_apac"), verified=True)
add(id="S2-E-008", type="사건", importance=2, statement="네이버 쇼핑 AI 에이전트가 정식 출시됐다. 하반기에 장바구니·배송 기능을 더하겠다고 밝혔다.",
    date="2026-06-25", actor="네이버", sources=src("naver_agent"), verified=True)
add(id="S2-E-009", type="사건", importance=2, statement="네이버가 AI탭을 정식 출시하고 4분기에 AI탭 광고 도입을 추진한다고 밝혔다.",
    date="2026-06-25", actor="네이버", sources=src("naver_ad"), verified=True)
add(id="S2-E-010", type="사건", importance=3, statement="미국 항소법원이 Perplexity 쇼핑 에이전트에 대한 가처분을 뒤집었다. 에이전트는 사용자 지시로 움직이므로 접근 주체는 사용자라고 봤다. 본안 소송은 계속된다.",
    date="2026-08-04", actor="미국 제9순회 항소법원", sources=src("amz_appeal"), verified=True)
add(id="S2-E-011", type="사건", importance=2, statement="카카오가 카카오톡 AI 에이전트의 첫 파트너로 쿠팡이츠를 정하고, 채팅방 안에서 주문·결제까지 끝내는 서비스를 준비 중이라고 밝혔다. 수익화는 2027년부터로 봤다.",
    date="2026-08-06", actor="카카오", sources=src("kakao_q2"), verified=True)

# ---------- 해석 (I) ----------
add(id="S2-I-001", type="해석", importance=3, target="실거래 단계", direction="중립",
    statement="AI가 실제로 대신하는 일은 '고르기'까지다. 탐색·비교는 유통사 에이전트에서 대규모로 운영되지만(Rufus 3억 명, Shopify AI 주문 3배), 외부 AI 안 결제는 시험 뒤 후퇴했다.",
    basis=["S2-M-001", "S2-M-003", "S2-E-004"])
add(id="S2-I-002", type="해석", importance=3, target="외부 AI 안 결제", direction="약화",
    statement="외부 AI 안 결제가 후퇴한 이유는 전환율이다. ChatGPT 안 결제는 사이트로 넘어가 사는 것보다 전환율이 3분의 1이었고, 상품 데이터가 부정확했다. 카드망의 에이전트 결제도 수백 건 규모의 시험에 머문다.",
    basis=["S2-M-004", "S2-E-004", "S2-M-005"])
add(id="S2-I-003", type="해석", importance=3, target="고객 관계·데이터", direction="강화",
    statement="고객 관계와 데이터는 유통사가 지키고 있다. 구글 표준에서도 유통사가 판매 당사자로 남고, Walmart는 자기 에이전트를 ChatGPT 안에 들고 나가 장바구니를 자기 시스템에 묶었다.",
    basis=["S2-E-002", "S2-E-005", "S2-M-002"])
add(id="S2-I-004", type="해석", importance=3, target="수익 배분", direction="강화",
    statement="에이전트 커머스의 돈은 거래 수수료보다 광고로 흐른다. 4% 결제 수수료 모델은 결제 후퇴로 흔들린 반면, Amazon은 Rufus 안 광고를 정식화했고 구글은 AI Mode 할인 광고를, 네이버는 AI탭 광고를 준비한다.",
    basis=["S2-M-007", "S2-M-008", "S2-E-006", "S2-E-002", "S2-E-009"])
add(id="S2-I-005", type="해석", importance=2, target="결제망", direction="중립",
    statement="결제망 자리는 기존 강자가 선점하고 있지만 실거래는 아직 없다. Visa·Mastercard가 발급사 준비 프로그램을 돌리는 단계이며, 대규모 실거래는 자기 앱 안에서 결제를 묶은 중국 Alipay에서만 나타났다.",
    basis=["S2-M-005", "S2-E-007"])
add(id="S2-I-006", type="해석", importance=2, target="접근권", direction="중립",
    statement="외부 에이전트가 유통사 사이트에 들어갈 권리는 법정에서 다퉈지고 있다. 1심은 Amazon 편이었지만 항소심은 '에이전트는 사용자의 대리인'이라며 가처분을 뒤집었다.",
    basis=["S2-E-003", "S2-E-010"])
add(id="S2-I-007", type="해석", importance=3, target="한국", direction="강화",
    statement="한국 에이전트 커머스는 외부 AI가 아니라 플랫폼 안에서 자란다. 네이버 쇼핑 에이전트의 거래액은 3개월 새 2.7배가 됐고, 카카오는 카톡 안에서 쿠팡이츠 주문·결제까지 끝내는 에이전트를 준비한다. 결제를 이미 가진 플랫폼이라 결제 단계에 먼저 닿을 수 있다.",
    basis=["S2-M-010", "S2-E-008", "S2-E-011", "S2-M-011"])
add(id="S2-I-008", type="해석", importance=2, target="전망과 현실의 간격", direction="중립",
    statement="2030년 온라인 소매의 10~20%라는 전망과, 카드망 실거래 수백 건이라는 현실 사이의 간격이 크다. 다만 미국인의 약 23%가 이미 AI를 거쳐 무언가를 샀다는 추정은, 결제가 아니라 '고르기'에서 AI가 이미 거래에 관여한다는 뜻이다.",
    basis=["S2-M-009", "S2-M-005"])

# ---------- 세부 전망 (F) ----------
add(id="S2-F-001", type="전망", importance=2, status="유효", forecast_status="진행 중",
    statement="카카오는 2026년 말까지 카카오톡 안에서 쿠팡이츠 주문·결제까지 끝내는 AI 에이전트를 정식 출시할 것이다.", due="2026-12-31", condition="없음",
    method="카카오 공식 발표 또는 주요 언론 보도 확인", basis=["S2-E-011", "S2-M-011"], result=None)
add(id="S2-F-002", type="전망", importance=2, status="유효", forecast_status="진행 중",
    statement="네이버는 2026년 말까지 쇼핑 AI 에이전트에 장바구니 담기 또는 결제 연동 기능을 출시할 것이다.", due="2026-12-31", condition="없음",
    method="네이버 공식 발표 확인", basis=["S2-E-008", "S2-M-010"], result=None)
add(id="S2-F-003", type="전망", importance=2, status="유효", forecast_status="진행 중",
    statement="Amazon의 2026년 4분기 광고 매출은 전년보다 20% 이상 늘 것이다.", due="2027-02-28", condition="없음",
    method="Amazon 2026년 4분기 실적 확인", basis=["S2-M-008"], result=None)
add(id="S2-F-004", type="전망", importance=3, status="유효", forecast_status="진행 중",
    statement="구글은 2027년 3월 말까지 AI Mode·Gemini 안 결제(UCP)를 미국 밖 한 곳 이상으로 넓힌다고 발표할 것이다.", due="2027-03-31", condition="없음",
    method="Google 공식 발표 확인", basis=["S2-E-002"], result=None)
add(id="S2-F-005", type="전망", importance=3, status="유효", forecast_status="진행 중",
    statement="2027년 6월 말까지 Visa 또는 Mastercard가 에이전트 결제 실거래를 100만 건 이상이라고 공식 발표하지는 않을 것이다.", due="2027-06-30", condition="없음",
    method="Visa·Mastercard 공식 발표·실적 발표 확인", basis=["S2-M-005", "S2-E-007"], result=None)
add(id="S2-F-006", type="전망", importance=2, status="유효", forecast_status="진행 중",
    statement="OpenAI는 2027년 6월 말까지 ChatGPT 대화 안 직접 결제를 미국에서 다시 일반 출시하지 않을 것이다.", due="2027-06-30", condition="없음",
    method="OpenAI 공식 발표 확인", basis=["S2-E-004", "S2-M-004"], result=None)

# ---------- 메인 질문 시나리오 ----------
add(id="S2-F-101", type="전망", importance=3, status="유효", forecast_status="진행 중", scenario="낙관",
    statement="2027년 말까지 에이전트가 결제 단계까지 실거래를 만든다. 외부 AI 안 결제가 미국 밖으로 넓어지고 카드망 에이전트 결제가 백만 건 단위로 올라서며, 한국에서는 네이버·카카오 에이전트 안 결제가 정식 운영된다. 수수료·광고·데이터를 AI 플랫폼과 유통사가 나눠 갖는 구조가 자리 잡는다.",
    milestones=[
        {"by": "2026-12", "text": "카카오톡 쿠팡이츠 주문·결제 에이전트, 네이버 장바구니·결제 기능 출시"},
        {"by": "2027-03", "text": "구글 AI Mode 결제 미국 밖 확대"},
        {"by": "2027-06", "text": "카드망 에이전트 결제 100만 건 이상 공개"}],
    due="2027-12-31", condition="대형 에이전트 결제 사고가 없을 경우",
    method="세 가지 중 두 가지 이상 충족 시 적중: (1) 구글·OpenAI 등 외부 AI 안 결제가 미국 밖 또는 일반 출시로 정식 운영 (2) Visa·Mastercard 에이전트 결제 100만 건 이상 공식 발표 (3) 네이버 또는 카카오 에이전트 안 결제 정식 운영",
    basis=["S2-E-002", "S2-M-005", "S2-E-011", "S2-M-010"],
    signposts=[{"id": "S2-F-001", "on_hit": "낙관", "on_miss": "비관"}, {"id": "S2-F-002", "on_hit": "낙관"},
               {"id": "S2-F-004", "on_hit": "낙관", "on_miss": "비관"}, {"id": "S2-F-005", "on_hit": "비관", "on_miss": "낙관"},
               {"id": "S2-F-006", "on_hit": "비관", "on_miss": "낙관"}, {"id": "S2-F-003", "on_hit": "비관"}], result=None)
add(id="S2-F-102", type="전망", importance=3, status="유효", forecast_status="진행 중", scenario="비관",
    statement="2027년 말까지 AI는 '고르기'에 머물고 결제는 유통사 사이트·앱으로 돌아간다. 에이전트 커머스의 수익은 결제 수수료가 아니라 에이전트 안 광고로 흐르고, 고객 관계와 데이터는 유통사·마켓플레이스가 계속 쥔다.",
    milestones=[
        {"by": "2027-02", "text": "Amazon 광고 매출 20% 이상 성장 지속"},
        {"by": "2027-06", "text": "OpenAI 대화 안 결제 재출시 없음"},
        {"by": "2027-06", "text": "카드망 에이전트 결제 대규모 실적 미공개"}],
    due="2027-12-31", condition="없음",
    method="낙관 시나리오의 판정 조건 세 가지 중 하나 이하만 충족 시 적중",
    basis=["S2-M-004", "S2-E-004", "S2-M-008"], signposts=[], result=None)

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

"""C2 R1 4유형 기록 생성 + 규칙 검증.
출력: q2/records.jsonl
"""
import json, sys
from pathlib import Path
from collections import Counter

R = "R1"
SRC = {
 "mr_rufus": {"url": "https://www.modernretail.co/technology/amazon-says-its-ai-shopping-assistant-is-gaining-traction-with-rufus-users-up-115/", "publisher": "Modern Retail (Amazon 실적 발표)", "date": "2026-04-30", "grade": "B"},
 "aa_ucp": {"url": "https://www.androidauthority.com/google-universal-commerce-protocol-announcement-3631662", "publisher": "Android Authority (Google 발표)", "date": "2026-01-12", "grade": "B"},
 "sa_ads": {"url": "https://siliconangle.com/2026/01/16/openai-start-testing-chatgpt-ads-across-free-go-tiers/", "publisher": "SiliconANGLE (OpenAI 발표)", "date": "2026-01-16", "grade": "B"},
 "cloro_ads": {"url": "https://cloro.dev/blog/chatgpt-ads-rollout-2026/", "publisher": "cloro 모니터링 블로그", "date": "2026-09-15", "grade": "C"},
 "gartner_cs": {"url": "https://gcom.pdo.aws.gartner.com/en/newsroom/press-releases/2026-08-04-gartner-survey-finds-87-percent-of-customers-say-companies-using-genai-for-customer-service-must-provide-access-to-a-human-agent0", "publisher": "Gartner 보도자료", "date": "2026-08-04", "grade": "A"},
 "gw_amzn": {"url": "https://www.geekwire.com/2026/judge-blocks-perplexitys-ai-bot-from-shopping-on-amazon-in-early-test-of-agentic-commerce/", "publisher": "GeekWire", "date": "2026-03-10", "grade": "B"},
 "ew_amzn": {"url": "https://www.eweek.com/news/perplexity-ai-shopping-agent-returns-amazon/", "publisher": "eWeek (Reuters 인용)", "date": "2026-08-05", "grade": "B"},
 "kakao": {"url": "https://v.daum.net/v/20260507121150759", "publisher": "다음 뉴스 (카카오 1분기 실적 발표)", "date": "2026-05-07", "grade": "B"},
 "visa_ap": {"url": "https://www.visa.com.sg/about-visa/newsroom/press-releases/visa-launches-agentic-ready-program-in-asia-pacific-with-over-50-partners-advancing-agentic-commerce.html", "publisher": "Visa 보도자료", "date": "2026-04-30", "grade": "A"},
 "naver_shop_ga": {"url": "https://byline.network/2026/07/0701-2/", "publisher": "바이라인네트워크", "date": "2026-07-01", "grade": "B"},
 "segye_ai_tab": {"url": "https://www.segye.com/newsView/20260626507402", "publisher": "세계일보", "date": "2026-06-26", "grade": "B"},
 "forklog": {"url": "https://forklog.com/en/openai-abandons-instant-checkout-feature-in-chatgpt/amp", "publisher": "ForkLog (The Information 인용)", "date": "2026-03-23", "grade": "B"},
 "lgu_aicc": {"url": "https://www.newsis.com/view/NISX20260714_0003707948", "publisher": "뉴시스", "date": "2026-07-14", "grade": "B"},
}
def src(*keys): return [dict(SRC[k], key=k) for k in keys]

base = dict(question="C2", question_version="v1.0", first_seen=R, last_seen=R, status="유효", replaces=None, check_flags=[])
records = []
def add(**kw):
    r = dict(base); r.update(kw); records.append(r)

# ---------- 지표 (M) ----------
add(id="C2-M-001", type="지표", indicator="C2-T1", importance=3, statement="Amazon 쇼핑 Agent Rufus는 2025년 고객 3억 명이 썼고, 연환산 약 120억 달러의 증분 매출을 만들었다.",
    value=120, unit="억 달러(연환산 증분 매출)", as_of="2025", region="US/GLOBAL", definition="Amazon 2025년 4분기 실적 발표(2026년 2월)", extra={"users_2025": "3억 명"},
    sources=src("mr_rufus"), verified=True)
add(id="C2-M-002", type="지표", indicator="C2-T1", importance=2, statement="2026년 1분기 Rufus 월간 이용자는 전년 대비 115%, 이용 활동(engagement)은 400% 늘었다.",
    value=115, unit="% YoY(MAU)", as_of="2026-C1", region="US/GLOBAL", definition="Amazon 1분기 실적 발표", sources=src("mr_rufus"), verified=True)
add(id="C2-M-003", type="지표", indicator="C2-T1", importance=2, statement="Amazon에 따르면 Rufus를 쓰는 고객은 구매를 끝낼 가능성이 60% 높다.",
    value=60, unit="% (구매 완료 가능성 차이)", as_of="2026-02", region="US/GLOBAL", definition="Amazon 발표", sources=src("mr_rufus"), verified=True)
add(id="C2-M-004", type="지표", indicator="C2-T8", importance=2, statement="Amazon 광고 매출은 2026년 1분기 172억 달러로 전년 대비 24% 늘었다.",
    value=24, unit="% YoY", as_of="2026-C1", region="GLOBAL", definition="Amazon 1분기 광고 매출", extra={"ad_revenue": "172억 달러"}, sources=src("mr_rufus"), verified=True)
add(id="C2-M-005", type="지표", indicator="C2-T2", importance=2, statement="Rufus 안의 브랜드 스폰서 질문을 누른 쇼핑객의 약 20%가 그 브랜드에 대해 대화를 이어갔다.",
    value=20, unit="%", as_of="2026-C1", region="US", definition="Amazon 발표, 스폰서 프롬프트 참여 후 대화 지속 비율", sources=src("mr_rufus"), verified=True)
add(id="C2-M-006", type="지표", indicator="C2-T2", importance=1, statement="외부 모니터링 기준 2026년 7월 초 미국 ChatGPT 응답의 약 51%에 광고가 붙었다.",
    value=51, unit="%", as_of="2026-07", region="US", definition="cloro 자체 모니터링, 최근 7일 응답 중 광고 노출 비율", sources=src("cloro_ads"), verified=False,
    check_flags=["출처 등급 C(단일 모니터링 업체) — 판단 근거에서 제외"])
add(id="C2-M-007", type="지표", indicator="C2-T4", importance=3, statement="최근 고객 서비스 상황에서 고객은 기업이 제공한 챗봇보다 ChatGPT·Gemini 같은 서드파티 AI를 약 3배 더 많이 썼다.",
    value=3, unit="배", as_of="2026-02~03", region="GLOBAL", definition="Gartner 고객 조사(B2B·B2C 3,566명)", sources=src("gartner_cs"), verified=True)
add(id="C2-M-008", type="지표", indicator="C2-T4", importance=3, statement="고객의 87%는 AI로 상담하는 기업이라도 사람 상담원 연결은 반드시 있어야 한다고 답했다.",
    value=87, unit="%", as_of="2026-02~03", region="GLOBAL", definition="Gartner 고객 조사", sources=src("gartner_cs"), verified=True)
add(id="C2-M-009", type="지표", indicator="C2-T4", importance=2, statement="생성형 AI를 쓰는 고객의 58%가 AI에게 자기 대신 일을 처리시킨 경험이 있다(B2B는 74%).",
    value=58, unit="%", as_of="2026-02~03", region="GLOBAL", definition="Gartner 고객 조사", sources=src("gartner_cs"), verified=True)
add(id="C2-M-010", type="지표", indicator="C2-T3", importance=2, statement="Google의 Universal Commerce Protocol에는 발표 시점에 20곳 이상이 참여했고, Shopify·Walmart·Target·Etsy·Wayfair가 공동 개발했다.",
    value=20, unit="곳 이상", as_of="2026-01", region="US", definition="UCP 참여 파트너 수", sources=src("aa_ucp"), verified=True)
add(id="C2-M-011", type="지표", indicator="C2-T3", importance=2, statement="Visa의 Agent 결제 준비 프로그램에 아태 50곳 이상이 참여했고, 한국에서는 하나·현대·KB국민·삼성·신한카드와 카카오뱅크가 이름을 올렸다.",
    value=6, unit="곳(한국)", as_of="2026-04", region="KR/APAC", definition="Visa Agentic Ready 참여 발급사", extra={"apac_partners": "50곳 이상", "markets": "한국 포함 10개 시장"},
    sources=src("visa_ap"), verified=True, check_flags=["국가 구분은 회사명으로 추정"])
add(id="C2-M-012", type="지표", indicator="C2-T7", importance=2, statement="카카오는 카카오톡 AI 에이전트를 쓸 수 있는 이용자가 2026년 말 3,100만 명(1분기 카톡 MAU 4,958만 명의 약 62%)이 될 것으로 봤다.",
    value=3100, unit="만 명(예상)", as_of="2026-05", region="KR", definition="카카오 1분기 실적 발표", sources=src("kakao"), verified=True)
add(id="C2-M-013", type="지표", indicator="C2-T7", importance=2, statement="네이버 쇼핑 AI 에이전트 경유 거래액은 3월 대비 6월에 2.7배 이상 늘었다.",
    value=2.7, unit="배", as_of="2026-06", region="KR", definition="네이버 발표", sources=src("naver_shop_ga"), verified=True)

# ---------- 사건 (E) ----------
add(id="C2-E-001", type="사건", importance=3, statement="Google이 AI Mode와 Gemini 안에서 결제까지 끝내는 Universal Commerce Protocol과, 브랜드가 자기 목소리로 응대하는 Business Agent를 발표했다.",
    date="2026-01-11", actor="Google", sources=src("aa_ucp"), verified=True)
add(id="C2-E-002", type="사건", importance=3, statement="OpenAI가 미국 ChatGPT 무료·Go 요금제에서 광고 시험을 시작한다고 발표했다. 광고는 답변 아래 '스폰서' 카드로 붙는다.",
    date="2026-01-16", actor="OpenAI", sources=src("sa_ads"), verified=True)
add(id="C2-E-003", type="사건", importance=3, statement="미국 법원이 Perplexity의 쇼핑 Agent(Comet)가 Amazon에서 대신 쇼핑하는 것을 막는 가처분을 내렸다.",
    date="2026-03-09", actor="Amazon·Perplexity", sources=src("gw_amzn"), verified=True)
add(id="C2-E-004", type="사건", importance=2, statement="OpenAI가 ChatGPT 대화 안 결제를 접고, 구매를 리테일러 앱과 사이트로 넘겼다.",
    date="2026-03", actor="OpenAI", sources=src("forklog"), verified=True)
add(id="C2-E-005", type="사건", importance=2, statement="Visa가 한국을 포함한 아태 10개 시장에서 카드 발급사용 Agent 결제 준비 프로그램을 시작했다.",
    date="2026-04-30", actor="Visa", sources=src("visa_ap"), verified=True)
add(id="C2-E-006", type="사건", importance=3, statement="카카오가 카카오톡 안에서 검색·추천·결제까지 이어지는 AI 에이전트를 하반기에 내겠다고 밝혔다. 4월부터 '선물하기' 연동 베타를 운영 중이다.",
    date="2026-05-07", actor="카카오", sources=src("kakao"), verified=True)
add(id="C2-E-007", type="사건", importance=2, statement="네이버가 AI탭을 전체 이용자에게 정식 출시했고, 4분기에 AI탭 광고 도입을 추진한다고 밝혔다.",
    date="2026-06-25", actor="네이버", sources=src("segye_ai_tab"), verified=True)
add(id="C2-E-008", type="사건", importance=2, statement="네이버 쇼핑 AI 에이전트가 정식 출시됐고, 하반기에 개인화 멤버십 혜택 추천·장바구니·배송 기능을 더하겠다고 밝혔다.",
    date="2026-06-25", actor="네이버", sources=src("naver_shop_ga"), verified=True)
add(id="C2-E-009", type="사건", importance=1, statement="LG유플러스가 조회·판단·실행까지 하는 에이전틱 AI 상담봇과 상담 품질 사전 검증 도구를 공개했다.",
    date="2026-07-14", actor="LG유플러스", sources=src("lgu_aicc"), verified=True)
add(id="C2-E-010", type="사건", importance=3, statement="미국 항소법원(제9순회)이 Perplexity 쇼핑 Agent에 대한 가처분을 뒤집었다. Agent는 사용자 지시로 움직이므로 접근 주체는 사용자라고 봤다. 본안 소송은 계속된다.",
    date="2026-08-04", actor="Amazon·Perplexity", sources=src("ew_amzn"), verified=True)
add(id="C2-E-011", type="사건", importance=2, statement="Amazon이 Rufus에 생필품 재주문·신제품 추적 같은 반복 쇼핑 작업 설정 기능을 더했다. 설정 가격에 닿으면 자동 구매하는 기능은 이미 있다.",
    date="2026-04", actor="Amazon", sources=src("mr_rufus"), verified=True)

# ---------- 해석 (I) ----------
add(id="C2-I-001", type="해석", importance=3, target="발견 접점", direction="강화",
    statement="발견 접점은 AI 답변 안으로 옮겨가고 있고, 그 지면은 플랫폼이 광고로 팔기 시작했다. 브랜드는 AI 답변에 노출되려면 플랫폼에 광고비를 내는 구조가 생기고 있다.",
    basis=["C2-E-002", "C2-M-005", "C2-M-004", "C2-E-007"])
add(id="C2-I-002", type="해석", importance=3, target="상담 접점", direction="강화",
    statement="상담 접점은 브랜드 밖으로 빠져나가고 있다. 고객은 기업 챗봇보다 범용 AI를 세 배 더 많이 쓴다. 다만 87%가 사람 연결을 요구해, 브랜드 상담의 차별점은 'AI 안내 + 사람 연결'로 좁혀지고 있다.",
    basis=["C2-M-007", "C2-M-008", "C2-M-009"])
add(id="C2-I-003", type="해석", importance=3, target="판매 접점", direction="중립",
    statement="결제 접점은 아직 주인이 정해지지 않았다. Google은 AI 화면 안 결제로 들어왔고 OpenAI는 결제를 리테일러에게 돌려줬으며, Amazon과 Perplexity는 고객 Agent의 접근권을 놓고 법정에서 다투고 있다.",
    basis=["C2-E-001", "C2-E-004", "C2-E-003", "C2-E-010"])
add(id="C2-I-004", type="해석", importance=3, target="플랫폼 자체 Agent", direction="강화",
    statement="지금 가장 앞선 쇼핑 Agent는 외부 범용 AI가 아니라 Amazon Rufus 같은 플랫폼 자체 Agent다. 이용자·매출·전환 모두 숫자로 확인되고, 스폰서 질문으로 광고까지 붙었다.",
    basis=["C2-M-001", "C2-M-002", "C2-M-003", "C2-M-005"])
add(id="C2-I-005", type="해석", importance=3, target="한국 주도권", direction="강화",
    statement="한국은 네이버(검색·쇼핑)와 카카오(메신저·선물하기)가 발견부터 결제까지 자사 안에 묶는 방식으로 Agent를 키우고 있다. 브랜드는 두 플랫폼 안에 입점하는 형태로 Agent 채널에 들어가게 된다.",
    basis=["C2-E-006", "C2-M-012", "C2-M-013", "C2-E-007", "C2-E-008"])
add(id="C2-I-006", type="해석", importance=2, target="Agent 결제 인프라", direction="중립",
    statement="Agent 결제의 인프라는 준비 단계다. 한국 카드사 6곳이 Visa 프로그램에 들어갔지만 시험 환경 검증이 1단계이고, 일반 소비자 상용 거래는 아직 없다.",
    basis=["C2-M-011", "C2-E-005"])

# ---------- 세부 전망 (F) ----------
add(id="C2-F-001", type="전망", importance=2, status="유효", forecast_status="진행 중",
    statement="네이버는 2026년 안에 AI탭 광고 상품을 출시할 것이다.", due="2026-12-31", condition="없음",
    method="네이버 보도자료·실적발표에서 AI탭 광고 출시 확인", basis=["C2-E-007"], result=None)
add(id="C2-F-002", type="전망", importance=3, status="유효", forecast_status="진행 중",
    statement="카카오톡 AI 에이전트는 2026년 안에 정식 출시되며, 선물하기 외 외부 커머스 결제 연결을 포함할 것이다.", due="2026-12-31", condition="없음",
    method="카카오 발표에서 정식 출시와 외부 커머스(자사 외 쇼핑몰) 결제 연결 여부 확인", basis=["C2-E-006", "C2-M-012"], result=None)
add(id="C2-F-003", type="전망", importance=3, status="유효", forecast_status="진행 중",
    statement="2027년 6월 말까지 Perplexity 쇼핑 Agent의 Amazon 이용이 다시 법원 명령으로 막히지 않을 것이다.", due="2027-06-30", condition="없음",
    method="Amazon v. Perplexity 소송의 법원 명령·합의 내용 확인", basis=["C2-E-010", "C2-E-003"], result=None)
add(id="C2-F-004", type="전망", importance=2, status="유효", forecast_status="진행 중",
    statement="Amazon이 발표하는 2026년 Rufus 기여 매출은 2025년(연환산 약 120억 달러)보다 클 것이다.", due="2027-02-28", condition="Amazon이 같은 지표를 공개할 경우",
    method="Amazon 2026년 4분기 실적 발표의 Rufus 매출 기여 수치 확인", basis=["C2-M-001", "C2-M-002"], result=None)
add(id="C2-F-005", type="전망", importance=2, status="유효", forecast_status="진행 중",
    statement="Gartner의 다음 고객 조사에서도 고객은 기업 챗봇보다 서드파티 AI를 더 많이 쓸 것이다.", due="2027-09-30", condition="같은 문항이 반복될 경우",
    method="Gartner 2027 고객 서비스 조사의 서드파티 AI 대 기업 챗봇 이용 비교 확인", basis=["C2-M-007"], result=None)
add(id="C2-F-006", type="전망", importance=2, status="유효", forecast_status="진행 중",
    statement="2027년 6월 말까지 한국 카드사 중 1곳 이상이 일반 소비자 대상 AI Agent 결제를 상용 출시할 것이다.", due="2027-06-30", condition="없음",
    method="국내 카드사·Visa·Mastercard 발표에서 일반 소비자 대상 Agent 결제 상용 출시 확인", basis=["C2-M-011", "C2-E-005"], result=None)

# ---------- 메인 질문 시나리오 (브랜드 관점 낙관·비관) ----------
add(id="C2-F-101", type="전망", importance=3, status="유효", forecast_status="진행 중", scenario="낙관",
    statement="(브랜드 관점) 2027년 말까지 Agent 채널이 여러 플랫폼과 개방 규격으로 나뉜다. 고객 Agent의 쇼핑 접근권이 법적으로 유지되고, 브랜드는 UCP 같은 개방 규격과 자체 Agent로 여러 AI 창구에 직접 연결해 판매·관계 접점을 지킨다. 한국에서도 카카오·네이버 Agent가 외부 브랜드몰 결제를 연결한다.",
    milestones=[
        {"by": "2026-12", "text": "카카오톡 AI 에이전트 정식 출시, 외부 커머스 결제 연결"},
        {"by": "2027-06", "text": "Perplexity 쇼핑 Agent의 Amazon 접근 유지, 한국 카드사 Agent 결제 상용 출시"},
        {"by": "2027-12", "text": "브랜드 자체 Agent가 Google·ChatGPT 등 여러 AI 창구에서 직접 응대·판매"}],
    due="2027-12-31", condition="대형 플랫폼이 외부 Agent 차단을 기술적으로 강화하지 않을 경우",
    method="세 가지 중 두 가지 이상 충족 시 적중: (1) 고객 Agent의 대형 마켓플레이스 쇼핑 접근이 법원 명령으로 막히지 않음 (2) 브랜드 자체 Agent가 둘 이상의 AI 플랫폼에서 일반 이용자에게 제공됨 (3) 한국 메신저·포털 Agent에 외부 브랜드몰 결제 연결",
    basis=["C2-E-001", "C2-E-010", "C2-M-010", "C2-E-006"],
    signposts=[{"id": "C2-F-002", "on_hit": "낙관", "on_miss": "비관"}, {"id": "C2-F-003", "on_hit": "낙관", "on_miss": "비관"}, {"id": "C2-F-006", "on_hit": "낙관"}], result=None)
add(id="C2-F-102", type="전망", importance=3, status="유효", forecast_status="진행 중", scenario="비관",
    statement="(브랜드 관점) 2027년 말까지 소수 플랫폼이 발견부터 결제까지 장악한다. AI 답변 안 노출은 광고로 사야 하고, 쇼핑 Agent는 Amazon Rufus·네이버·카카오처럼 플랫폼 자체 Agent가 주도한다. 브랜드는 판매 데이터와 고객 관계를 플랫폼에 넘기고 상품 공급자 위치로 밀린다.",
    milestones=[
        {"by": "2026-12", "text": "네이버 AI탭 광고 출시, ChatGPT 광고 미국 밖으로 확대"},
        {"by": "2027-02", "text": "Amazon Rufus 기여 매출이 2025년보다 커짐"},
        {"by": "2027-12", "text": "고객 상담의 첫 창구가 기업 챗봇이 아닌 범용 AI로 굳어짐"}],
    due="2027-12-31", condition="없음",
    method="낙관 시나리오의 판정 조건 세 가지 중 하나 이하만 충족 시 적중",
    basis=["C2-E-002", "C2-M-001", "C2-M-004", "C2-M-007", "C2-E-007"],
    signposts=[{"id": "C2-F-001", "on_hit": "비관"}, {"id": "C2-F-004", "on_hit": "비관"}, {"id": "C2-F-005", "on_hit": "비관"}], result=None)


# ---------- 정정·추가 (2026-10-11 검증 반영, probe_20261011/verification_report.md) ----------
# 원본 기록은 ID를 유지한 채 고치고, 고치기 전 진술과 이유를 revisions에 남긴다. 새 기록은 added_on으로 구분한다.
CHG = "2026-10-11"
SRC.update({
 "amzn_q2": {"url": "https://www.aboutamazon.com/news/company-news/amazon-ceo-andy-jassy-stores-growth-ai-shopping-q2-2026-earnings", "publisher": "Amazon (2026 2분기 실적 발표)", "date": "2026-07-30", "grade": "A"},
 "amzn_q2_pdf": {"url": "https://s2.q4cdn.com/299287126/files/doc_earnings/2026/q2/earnings-result/AMZN-Q2-2026-Earnings-Release.pdf", "publisher": "Amazon (2026 2분기 실적 릴리스)", "date": "2026-07-30", "grade": "A"},
 "amzn_q1_sec": {"url": "https://www.sec.gov/Archives/edgar/data/1018724/000101872426000012/amzn-20260331xex991.htm", "publisher": "Amazon (2026 1분기 실적 릴리스, SEC)", "date": "2026-04-30", "grade": "A"},
 "fn_naver_shop": {"url": "https://www.fnnews.com/news/202609270633124595", "publisher": "파이낸셜뉴스", "date": "2026-09-27", "grade": "B"},
 "zdnet_kakao": {"url": "https://zdnet.co.kr/view/?no=20260806111654", "publisher": "ZDNet Korea (카카오 2분기 콜)", "date": "2026-08-06", "grade": "B"},
 "newsis_kakao_q2": {"url": "https://www.newsis.com/view/NISX20260806_0003738743", "publisher": "뉴시스 (카카오 2분기 콜)", "date": "2026-08-06", "grade": "B"},
 "naver_q2_pr": {"url": "https://www.navercorp.com/media/pressReleasesDetail?seq=10034577", "publisher": "네이버 보도자료 (2분기 실적)", "date": "2026-08", "grade": "A"},
 "daum_naver_brief": {"url": "https://v.daum.net/v/20260703000247237", "publisher": "다음 뉴스 (네이버 AI 브리핑 광고)", "date": "2026-07-03", "grade": "B"},
 "openai_ads": {"url": "https://openai.com/index/testing-ads-in-chatgpt/", "publisher": "OpenAI (Testing ads in ChatGPT)", "date": "2026-02-09", "grade": "A"},
 "yahoo_oai_ads": {"url": "https://finance.yahoo.com/media-advertising/articles/openai-chatgpt-ads-hit-1-132117654.html", "publisher": "Yahoo Finance (CNBC 인용)", "date": "2026-08-31", "grade": "B"},
 "mr_ic": {"url": "https://www.modernretail.co/technology/what-went-wrong-with-chatgpts-instant-checkout/", "publisher": "Modern Retail", "date": "2026-03", "grade": "B"},
 "dc360_oai": {"url": "https://www.digitalcommerce360.com/2026/03/24/openai-agentic-commerce-updates-chatgpt-walmart/amp/", "publisher": "Digital Commerce 360", "date": "2026-03-24", "grade": "B"},
 "dc360_perplexity": {"url": "https://digitalcommerce360.com/2026/03/18/court-grants-perplexity-access-amazon-agentic-ai/", "publisher": "Digital Commerce 360", "date": "2026-03-18", "grade": "B"},
 "mediapost_9c": {"url": "https://www.mediapost.com/publications/article/417793/appeals-court-again-rejects-amazon-bid-to-block-pe.html", "publisher": "MediaPost", "date": "2026-09-11", "grade": "B"},
 "cooley_9c": {"url": "https://www.cooley.com/news/insight/2026/2026-08-06-ninth-circuit-rules-on-ai-agent-access-to-third-party-websites-under-cfaa", "publisher": "Cooley (법률 해설)", "date": "2026-08-06", "grade": "A"},
 "google_blog_ucp": {"url": "https://blog.google/products/ads-commerce/agentic-commerce-ai-tools-protocol-retailers-platforms/", "publisher": "Google 블로그 (UCP 발표)", "date": "2026-01-11", "grade": "A"},
 "gartner_0708": {"url": "https://www.gartner.com/en/newsroom/press-releases/2026-07-08-gartner-survey-finds-customers-are-three-times-more-likely-to-use-third-party-genai-than-company-provided-chatbots-for-customer-service", "publisher": "Gartner 보도자료 (7월 8일)", "date": "2026-07-08", "grade": "A"},
 "axios_msft": {"url": "https://www.axios.com/2026/01/08/microsoft-ai-copilot-checkout", "publisher": "Axios (Microsoft Copilot Checkout)", "date": "2026-01-08", "grade": "B"},
 "ppc_muse": {"url": "https://ppc.land/amazon-blocks-metas-muse-ai-agent-from-shopping-on-its-site/", "publisher": "PPC Land (Amazon의 Meta Muse 차단)", "date": "2026-09-21", "grade": "B"},
 "tc_agents": {"url": "https://techcrunch.com/2026/10/06/the-next-hurdle-for-ai-agents-getting-websites-to-let-them-in", "publisher": "TechCrunch", "date": "2026-10-06", "grade": "B"},
 "mc_kr": {"url": "https://www.mastercard.com/news/ap/en/newsroom/press-releases/en/2026/mastercard-completes-korea-s-first-live-agentic-transactions-unlocking-trusted-ai-powered-commerce/", "publisher": "Mastercard 보도자료 (한국 첫 라이브 에이전틱 거래)", "date": "2026-03-17", "grade": "A"},
 "amzn_branded": {"url": "https://advertising.amazon.com/library/news/branded-conversations-review-requests", "publisher": "Amazon Ads (Branded Conversations)", "date": "2026-09-29", "grade": "A"},
 "emarketer_pplx": {"url": "https://www.emarketer.com/content/perplexity-retreat-ads-marks-split-on-ai-monetization-models", "publisher": "eMarketer", "date": "2026", "grade": "B"},
})
def _get(i): return next(r for r in records if r["id"] == i)
def revise(i, kind, why, **ch):
    r = _get(i)
    r.setdefault("revisions", []).append({"on": CHG, "kind": kind, "before": r.get("statement") if "statement" in ch else None, "why": why})
    r.update(ch)

# --- 지표 ---
revise("C2-M-001", "갱신", "Rufus와 Alexa+가 2026-05-13 'Alexa for Shopping'으로 통합됐고, 2분기 기준 값(최근 12개월 이용 고객 3.5억 명 이상)이 나와 기간이 다른 값을 함께 적었다.",
    statement="Amazon 쇼핑 Agent Rufus는 2025년 고객 3억 명이 썼고, 연환산 약 120억 달러의 증분 매출을 만들었다. 2026-05-13 Rufus와 Alexa+는 'Alexa for Shopping'으로 통합됐고, 2분기(7월 30일 발표) 기준 최근 12개월 이용 고객은 3.5억 명 이상이다(기간이 달라 증가율로 계산하지 않는다).",
    check_flags=["3억 명(2025년)과 3.5억 명(최근 12개월)은 기간이 달라 비교 금지", "2025년 값 원문(Q4'25 실적)은 직접 열람 못 하고 Modern Retail(B)로 확인 — 확인 필요", "미국 이용 고객의 주문당 지출 40% 이상은 이용자-비이용자 비교이며 인과 아님"],
    sources=src("mr_rufus", "amzn_q2", "amzn_q2_pdf"))
revise("C2-M-004", "갱신", "2분기 값(198.09억 달러, +26%)이 나왔고, 1분기 +24%는 환율 제외 시 +22%다.",
    statement="Amazon 광고 매출은 2026년 2분기 198.09억 달러로 전년 대비 26%(환율 영향 없음) 늘었다. 1분기 172.43억 달러의 +24%는 환율 제외 시 +22%다.",
    value=26, as_of="2026-Q2", prev_value=24, extra={"ad_revenue": "198.09억 달러", "q1_ad_revenue": "172.43억 달러(+24%, 환율 제외 +22%)"},
    check_flags=["2분기는 Prime Day가 대부분 국가에서 2분기로 이동해 전년 동기 대비가 부풀려질 수 있음", "분기끼리 성장률을 비교하지 않음"],
    sources=src("amzn_q2_pdf", "amzn_q1_sec"))
revise("C2-M-005", "상충", "Amazon 원문은 '프롬프트와 상호작용한 쇼핑객의 거의 20%가 그 브랜드 대화를 이어간다'이며 '스폰서'라는 한정이 없다.",
    statement="Rufus 안의 브랜드 프롬프트와 상호작용한 쇼핑객의 거의 20%가 그 브랜드에 대한 대화를 이어갔다(Amazon 1분기 릴리스 표현, 스폰서 한정 없음).",
    check_flags=["스폰서 프롬프트는 2025-11 무료 베타 후 2026-03-25 클릭당 과금으로 전환", "2분기 구매 전환 +48%·지출 +21%는 ppc.land(B) 인용이라 실적 원문에서 확인 못 함 — 확인 필요"],
    sources=src("amzn_q1_sec", "mr_rufus"))
revise("C2-M-006", "전망 점검", "C등급 단일 모니터링 업체 값이며 글 날짜와 기준 시점이 달라 판단 근거에서 계속 제외한다. OpenAI 1차 페이지는 노출 비율을 공개하지 않는다.",
    check_flags=["출처 등급 C(단일 모니터링 업체) — 판단 근거에서 제외", "글 날짜(2026-09-15)와 기준 시점(2026-07)이 달라 확인 필요"])
revise("C2-M-007", "누락정정", "Gartner 원문은 '약 3배 더 이용할 가능성'이고 가장 최근 서비스 상호작용 기준이며 절대 이용률과 조사 지역은 공개되지 않았다. 3배 비율의 출처는 7월 8일 릴리스다.",
    statement="최근 고객 서비스 상호작용에서 고객은 기업이 제공한 챗봇보다 ChatGPT·Gemini 같은 서드파티 AI를 약 3배 더 이용할 가능성이 높았다(절대 이용률은 공개되지 않음). 서드파티 생성형 AI 이용은 1년간 거의 2배가 됐고 기업 챗봇 이용은 2022년 이후 통계적으로 변하지 않았다.",
    unit="배(이용 가능성)", region="미명시", check_flags=["조사 지역이 릴리스에 명시되지 않음", "58%(생성형 AI 이용자 분모)·87%(전체 응답자 분모)는 분모가 달라 혼용 금지"],
    sources=src("gartner_0708", "gartner_cs"))
revise("C2-M-010", "상충", "공동 개발 5곳과 지지(endorse) 20곳 이상을 구분하지 않았다.",
    statement="Google의 Universal Commerce Protocol은 Shopify·Etsy·Wayfair·Target·Walmart 5곳이 공동 개발했고, Adyen·Amex·Best Buy·Stripe·Visa 등 20곳 이상이 지지했다. 출시 시점 체크아웃과 Business Agent는 미국 리테일러 한정이었다.",
    sources=src("google_blog_ucp", "aa_ucp"), check_flags=["9to5google은 공동 개발을 4곳(Walmart 제외)으로 적었으나 Google 1차 글(5곳)을 따름"])
revise("C2-M-012", "상충", "3,100만 명은 '카나나 인 카카오톡을 내려받을 수 있는 이용자(연말 전망)'이지 에이전트를 쓰는 이용자가 아니다. 2분기 콜에는 3,100만이 나오지 않았다.",
    statement="카카오는 1분기 콜에서 카카오톡 안 AI 서비스(카나나)를 내려받을 수 있는 이용자가 2026년 말 3,100만 명(1분기 카톡 MAU 4,957.5만 명의 약 62%)이 될 것으로 봤다. 2분기 콜(2026-08-06)에는 이 수치가 나오지 않았고, 연말 목표는 카톡 안에서 AI를 접하는 월간 활성 이용자 1,000만 명이며 챗GPT 포 카카오 누적 이용자는 1,300만 명이다.",
    unit="만 명(다운로드 가능 이용자 전망)", check_flags=["3,100만(다운로드 가능)·1,000만(MAU 목표)·1,300만(누적)은 분모가 달라 같은 규모로 읽지 않음", "카카오 IR 원문은 미열람 — 기사 기준"],
    sources=src("kakao", "zdnet_kakao"))
revise("C2-M-013", "갱신", "6월 값(거래액 2.7배 이상)이 8월 기준 값(월간 이용자 약 5배, 일평균 거래액 약 4배)으로 이어졌다. 지표 정의가 달라 섞지 않는다.",
    statement="네이버 쇼핑 AI 에이전트는 출시 초기(3월) 대비 8월 기준 월간 이용자·일평균 대화 수가 약 5배, 에이전트 일평균 거래액이 약 4배로 늘었다(2026-09-27 보도). 6월 시점 값은 거래액 2.7배 이상이었다. 에이전트 안 결제는 연내 일부 상품군 시범 적용을 계획 중이다.",
    value=4, unit="배(에이전트 일평균 거래액, 3월 대비 8월)", prev_value=2.7, as_of="2026-08",
    check_flags=["6월 지표와 8월 지표는 정의가 달라 섞지 않음", "절대 이용자 수·거래액은 미공개", "기준 시점 '지난달'은 보도일 기준 8월로 추정"],
    sources=src("fn_naver_shop", "naver_shop_ga"))

# --- 사건 ---
revise("C2-E-002", "누락정정", "광고 시험을 실제로 시작한 날은 2026-02-09이고 1월 16일은 '곧 보이겠다'는 계획 발표다.",
    statement="OpenAI가 미국 ChatGPT 무료·Go 요금제에서 광고 시험을 시작했다(2026-02-09). 1월 16일에는 시작 계획을 발표했다. 광고는 '스폰서' 라벨로 유기적 답변과 구분되는 지면에 붙는다.",
    date="2026-02-09", sources=src("openai_ads", "sa_ads"))
revise("C2-E-003", "누락정정", "2026-03-09 가처분은 시행 직전인 03-16 제9순회 항소법원의 행정정지로 일시 효력이 멈췄고, 효력 범위는 Amazon의 비밀번호 보호 영역으로 한정됐다.",
    statement="미국 법원이 Perplexity의 쇼핑 Agent(Comet)가 Amazon에서 대신 쇼핑하는 것을 막는 가처분을 내렸다(2026-03-09). 시행 직전인 3월 16일 제9순회 항소법원의 행정정지로 효력이 일시 멈췄고(Comet은 계속 접근 가능), 효력 범위는 Amazon의 비밀번호 보호 영역으로 한정됐다.",
    check_flags=["정지가 정식 '항소 중 집행정지'인지는 MediaPost가 불명확하다고 적음"], sources=src("gw_amzn", "dc360_perplexity"))
revise("C2-E-004", "누락정정", "정확한 날짜는 2026-03-24이고, 완전 폐지가 아니라 '이동'이다(ChatGPT 안 앱 방식은 유지).",
    statement="OpenAI는 2026-03-24 블로그에서 Instant Checkout 초기 버전이 유연성이 부족했다며 판매자가 자체 체크아웃을 쓰게 하고 상품 발견에 집중하겠다고 밝혔다. Target·Sephora·Nordstrom·Lowe's·Best Buy·Home Depot·Wayfair가 ACP로 상품 발견에 연동했고, Walmart는 계정 연결·자사 결제를 쓰는 앱을 ChatGPT 안에 냈다.",
    date="2026-03-24", check_flags=["OpenAI 블로그 원문은 못 읽고 B 기사 2건으로 확인", "Walmart 임원의 '챗봇 안 결제 전환율 외부 클릭 대비 약 3배 낮음'은 회사 측 발언"],
    sources=src("mr_ic", "dc360_oai", "forklog"))
revise("C2-E-006", "갱신", "2분기 콜(2026-08-06)에서 카톡 에이전트의 첫 외부 버티컬로 쿠팡이츠 연동 계획이 나왔으나 출시일 없이 '구현되면' 단계이고, 3,100만 목표는 언급되지 않았다.",
    statement="카카오가 카카오톡 안에서 검색·추천·결제까지 이어지는 AI 에이전트를 하반기에 내겠다고 밝혔고(5월 1분기 콜), 4월부터 '선물하기' 연동 베타를 운영 중이다. 8월 6일 2분기 콜에서는 첫 외부 버티컬로 쿠팡이츠 연동(추천→주문→결제를 카톡 안에서)을 밝혔으나 출시일은 없다. 에이전트 커머스 수수료·AI 구독 수익화는 2027년부터, AI 광고는 2028년이 목표다.",
    check_flags=["결제 연동의 실제 동작은 확인되지 않음"], sources=src("kakao", "newsis_kakao_q2"))
revise("C2-E-007", "누락정정", "AI탭 정식 출시 발표일은 2026-06-26이다. 네이버는 AI 브리핑에 광고를 이미 붙였고(7월 21일 노출 시작), AI탭 광고는 4분기 '추진·검토' 단계다.",
    statement="네이버가 AI탭을 전체 이용자에게 정식 출시했고(2026-06-26 발표), 4분기에 AI탭 광고 도입을 추진한다고 밝혔다. 이미 AI 브리핑(검색 상단 AI 요약)에는 광고를 붙였다. 5월 7일~7월 2일 광고주 베타 후 7월 21일부터 노출을 시작했고, 네이버는 기존 검색광고 대비 클릭 전환율 30% 이상·구매 전환율 3배 이상(회사 주장)이라 밝혔다.",
    date="2026-06-26", check_flags=["AI탭 광고는 확정 일정이 아닌 '4분기 추진' 단계", "AI 브리핑 광고 노출 시작일은 기사(7/21)와 공식(7월 말)이 다름", "전환율 수치는 네이버 주장"],
    sources=src("segye_ai_tab", "naver_q2_pr", "daum_naver_brief"))
revise("C2-E-010", "누락정정", "가처분 단계에서 연방 해킹법(CFAA·CDAFA) 청구 성립 가능성이 낮다고 본 것이며 약관·계약 청구는 열려 있고, 9월 10일 재심리 요청이 받아들여지지 않았다.",
    statement="미국 항소법원(제9순회)이 2026-08-04 Perplexity 쇼핑 Agent에 대한 가처분을 뒤집었다. CFAA·CDAFA 청구만 다뤘고 약관·계약·불법행위 청구는 열려 있으며 본안은 판단하지 않았다. 9월 10일 재심리 요청은 받아들여지지 않아 판결이 유지됐다.",
    check_flags=["Amazon의 9월 21일 수정 소장 보도는 AI Weekly(등급 C) 단일 출처 — 확인 필요", "판결 원문은 못 읽고 Cooley·eWeek·MediaPost 해설 기준"],
    sources=src("ew_amzn", "cooley_9c", "mediapost_9c"))

# --- 신규 사건 ---
add(id="C2-E-012", type="사건", importance=3, added_on=CHG, statement="ChatGPT 광고가 미국 밖으로 확대됐다. OpenAI는 3월 26일 캐나다·호주·뉴질랜드 시범을, 5월 7일 영국·멕시코·브라질·일본·한국 확대를 예고했고 8월 11일 그 5개 시장 출시를 밝혔다. 8월 31일에는 연환산 매출 약 10억 달러, 40개국 이상이 보도됐다.",
    date="2026-08-11", actor="OpenAI", sources=src("openai_ads", "yahoo_oai_ads"), verified=True,
    check_flags=["10억 달러·40개국은 Yahoo Finance(CNBC 인용) 2차 — 확인 필요", "한국 시점은 6월 파일럿 보도와 8월 출시 발표가 달라 구분 확인 필요"])
add(id="C2-E-013", type="사건", importance=2, added_on=CHG, statement="Microsoft가 Copilot 대화 안에서 결제까지 끝내는 Copilot Checkout을 미국에서 발표했다(Shopify·PayPal·Stripe 연동, 리테일러가 판매자 지위 유지).",
    date="2026-01-08", actor="Microsoft", sources=src("axios_msft"), verified=True, check_flags=["이용 규모 미공개"])
add(id="C2-E-014", type="사건", importance=3, added_on=CHG, statement="Amazon이 Meta의 개인 에이전트 Muse(9월 8일 출시)가 Amazon.com에서 주문하는 것을 막았다. 무허가 AI 에이전트의 접근은 이용약관 위반이라는 입장이며 법적 조치 여부는 답하지 않았다. Walmart는 Muse와 제휴 관계라고 밝혔다.",
    date="2026-09-20", actor="Amazon·Meta", sources=src("ppc_muse", "tc_agents"), verified=True, check_flags=["Walmart 언급은 TechCrunch에만 있음"])
add(id="C2-E-015", type="사건", importance=2, added_on=CHG, statement="Mastercard가 한국 첫 라이브 인증 에이전틱 거래를 완료했다고 발표했다(AI 에이전트가 인천공항→광화문 호텔 차량 예약·결제, Agent Pay 사용). 발급 카드사·은행은 공개되지 않았다.",
    date="2026-03-17", actor="Mastercard", sources=src("mc_kr"), verified=True, check_flags=["시범성 1건이며 일반 소비자 상용은 아님"])
add(id="C2-E-016", type="사건", importance=2, added_on=CHG, statement="Amazon이 'Branded Conversations'를 발표했다. 브랜드가 자사 제품 지식을 제공하면 Alexa for Shopping이 '스폰서' 표시로 더 깊은 상담을 하는 광고 상품이며 2027년 1월 미국에서 출시된다.",
    date="2026-09-29", actor="Amazon", sources=src("amzn_branded"), verified=True)

# --- 해석 ---
revise("C2-I-001", "단정반증", "'플랫폼 일반'이 광고로 팔기 시작했다는 서술은 Perplexity의 광고 철수, Anthropic·Google(Gemini 앱)의 부인 사례와 맞지 않는다.",
    statement="발견 접점은 AI 답변 안으로 옮겨가고 있고, 그 지면을 OpenAI·Amazon·Google(AI Mode 테스트)·네이버 등 일부 플랫폼이 광고로 팔기 시작했다. 브랜드는 AI 답변에 노출되려면 그 플랫폼에 광고비를 내는 구조가 생기고 있다. Amazon은 브랜드의 제품 지식까지 광고 상품(Branded Conversations)에 넣으려 한다. Perplexity는 광고에서 철수했다(FT 인용).",
    basis=["C2-E-002", "C2-M-005", "C2-M-004", "C2-E-007", "C2-E-012", "C2-E-016"])
revise("C2-I-002", "상충", "근거 수치가 '이용할 가능성의 배수'라 이용 규모(이용 비중)를 직접 보여주지 못한다.",
    statement="상담 접점은 브랜드 밖으로 빠져나가고 있다. 고객은 기업 챗봇보다 범용 AI를 이용할 가능성이 약 세 배 높다(절대 이용률은 공개되지 않음). 다만 87%가 사람 연결을 요구해, 브랜드 상담의 차별점은 'AI 안내 + 사람 연결'로 좁혀지고 있다.")
revise("C2-I-003", "갱신", "Microsoft Copilot Checkout이 빠져 'AI 화면 안 결제' 주체가 둘 이상임이 드러나지 않았다.",
    statement="결제 접점은 아직 주인이 정해지지 않았다. Google과 Microsoft는 AI 화면 안 결제로 들어왔고 OpenAI는 Instant Checkout을 판매자 자체 체크아웃 쪽으로 돌렸으며, Amazon은 Perplexity와 법정에서, Meta Muse와는 약관으로 고객 Agent의 접근권을 다투고 있다.",
    basis=["C2-E-001", "C2-E-004", "C2-E-003", "C2-E-010", "C2-E-013", "C2-E-014"])
revise("C2-I-004", "단정반증", "외부 범용 AI의 쇼핑 이용 규모를 1차 수치로 확인하지 못해 '가장 앞선'을 비교할 근거가 없고, Rufus는 5월에 Alexa for Shopping으로 통합됐다.",
    statement="공개된 수치가 가장 많은 쇼핑 Agent는 Amazon의 Alexa for Shopping(옛 Rufus) 같은 플랫폼 자체 Agent다. 이용 고객·매출·전환이 숫자로 공개돼 있고 브랜드 프롬프트로 광고까지 붙었다. 외부 범용 AI와의 이용 규모 비교 수치는 없다.",
    check_flags=["외부 범용 AI(ChatGPT·Gemini 등)의 쇼핑 이용 규모는 A·B 등급 1차 수치로 확인하지 못함"])
revise("C2-I-005", "단정반증", "네이버 에이전트 안 결제는 연내 일부 상품군 시범 계획 단계이고, 카카오의 외부 연동은 출시 전이다.",
    statement="한국은 네이버(검색·쇼핑)와 카카오(메신저·선물하기)가 발견부터 결제까지 자사 안에 묶으려는 단계다. 네이버 에이전트 안 결제는 연내 일부 상품군 시범 계획이고, 카카오는 선물하기 연동 베타 외에 쿠팡이츠 연동을 계획 중이다. 브랜드는 두 플랫폼 안에 입점하는 형태로 Agent 채널에 들어가게 된다.")
revise("C2-I-006", "단정반증", "3월 Mastercard 한국 라이브 거래가 빠졌고, Visa 명단은 카드사 5곳과 카카오뱅크다.",
    statement="Agent 결제의 인프라는 준비 단계다. 한국에서는 카드사 5곳과 카카오뱅크가 Visa 프로그램에 들어갔고 Mastercard가 3월 라이브 거래 1건을 시범으로 마쳤지만, 일반 소비자 대상 상용 출시는 확인되지 않았다.",
    basis=["C2-M-011", "C2-E-005", "C2-E-015"],
    check_flags=["한국 카드사 발급 상용 서비스가 없다는 것을 직접 확인한 1차 근거는 없음 — 확인 필요"])

# --- 전망 ---
revise("C2-F-001", "판정 기준 보완", "AI 브리핑 광고(7월 이미 출시)는 AI탭 광고와 다른 지면이다. 지면 단위로 판정 대상을 정했다.",
    method="네이버 공지로 AI탭 화면에 별도 광고 지면이 열린 것을 확인. AI 브리핑 광고(2026-07 출시)는 제외", basis=["C2-E-007"])
revise("C2-F-002", "판정 기준 보완", "카카오가 밝힌 첫 외부 연동은 배달 서비스 쿠팡이츠이고 출시 전이며, 카나나 독립 앱 종료로 서비스명이 바뀔 수 있다.",
    statement="2026년 안에 카카오 공식 발표로 카카오톡 안 주문·결제가 일반 이용자에게 열린 외부 사업자가 1곳 이상 생길 것이다(카톡 안 AI 에이전트 기준).",
    method="카카오 공식 발표로 카톡 안 주문·결제가 일반 이용자에게 열린 외부 사업자(선물하기 제외) 1곳 이상 확인. 서비스 이름이 바뀌어도 카톡 안 AI 에이전트이면 인정")
revise("C2-F-003", "전망 점검", "연방 해킹법 쟁점은 8월 판결·9월 재심리 거부로 정리됐으나 Amazon이 주법·불법 간섭·약관 청구로 소송을 이어가고 있어 판정 변수가 바뀌었다. '막힘'의 범위를 명시했다.",
    method="Amazon v. Perplexity에서 본안 판결·가처분·합의로 접근이 제한된 경우를 모두 '막힘'으로 보고, 법원 명령·합의 내용으로 확인. Perplexity의 자발적 중단(5월 iOS Comet, C등급 보도)은 제외",
    check_flags=["Amazon의 9월 21일 수정 소장 보도는 C등급 단일 출처 — 확인 필요"], basis=["C2-E-010", "C2-E-003", "C2-E-014"])
revise("C2-F-004", "판정 기준 보완", "Rufus 명칭이 2026-05-13 사라졌고 2분기 릴리스는 증분 매출 금액 없이 활성 이용자·주문당 지출만 제시해 같은 지표가 이어질지 불확실하다.",
    method="Amazon 2026년 4분기 실적 발표의 Alexa for Shopping(옛 Rufus) 관련 증분 매출 금액 확인. 금액이 공개되지 않으면 이용 고객 수(최근 12개월)로 대체하지 않고 '판정 불가'로 둠")
revise("C2-F-005", "판정 기준 보완", "이번 지표가 '이용할 가능성의 배수'이고 절대 이용률이 공개되지 않아 비교 지표를 고정했다.",
    method="Gartner 2027 고객 서비스 조사에서 서드파티 생성형 AI 이용 가능성이 기업 챗봇보다 높다(배수 1 초과)고 공개되는지 확인. 같은 방식으로 공개되지 않으면 '판정 불가'")
revise("C2-F-006", "판정 기준 보완", "Mastercard 한국 라이브 거래(3/17, 발급사 비공개)와 Visa Agentic Ready가 이미 있어 '상용 출시'의 경계를 정했다.",
    method="국내 카드사가 자사 이름으로 일반 회원이 실결제할 수 있는 AI Agent 결제를 공지한 것을 확인. 카드망 사업자(Visa·Mastercard)의 시범 거래와 발급사 비공개 거래는 제외")
revise("C2-F-101", "판정 기준 보완", "전제와 판정 방법 (1)이 Amazon의 9월 20일 Meta Muse 차단(법원 명령 없는 자체 차단)을 잡지 못했다.",
    condition="대형 플랫폼이 법원 명령 없이 약관·기술로 외부 Agent를 차단하는 일이 일반화하지 않을 경우",
    method="세 가지 중 두 가지 이상 충족 시 적중: (1) 고객 Agent의 대형 마켓플레이스 쇼핑 접근이 법원 명령이나 플랫폼의 약관·기술 차단으로 막히지 않음(Amazon의 Meta Muse 차단 이후 상태 기준) (2) 브랜드 자체 Agent가 둘 이상의 AI 플랫폼에서 일반 이용자에게 새로 제공됨(2026-10 시점 기존 사례 제외) (3) 한국 메신저·포털 Agent에 외부 브랜드몰 결제 연결",
    basis=["C2-E-001", "C2-E-010", "C2-M-010", "C2-E-006", "C2-E-014"])
revise("C2-F-102", "전망 교체", "이정표 '2026-12 ChatGPT 광고 미국 밖으로 확대'는 기록 시점에 이미 달성돼 있어 판정 변별력이 없다. 광고주 셀프서브 개방 기준으로 바꿨다.",
    milestones=[
        {"by": "2026-12", "text": "네이버 AI탭 광고 출시, ChatGPT 광고주 셀프서브가 한국을 포함한 10개국 이상에 개방(미국 밖 확대는 이미 달성)"},
        {"by": "2027-02", "text": "Amazon의 Alexa for Shopping(옛 Rufus) 기여 매출 또는 이용 고객이 2025년보다 커짐"},
        {"by": "2027-12", "text": "고객 상담의 첫 창구가 기업 챗봇이 아닌 범용 AI로 굳어짐"}],
    statement="(브랜드 관점) 2027년 말까지 소수 플랫폼이 발견부터 결제까지 장악한다. AI 답변 안 노출은 광고로 사야 하고, 쇼핑 Agent는 Amazon의 Alexa for Shopping(옛 Rufus)·네이버·카카오처럼 플랫폼 자체 Agent가 주도한다. 브랜드는 판매 데이터와 고객 관계를 플랫폼에 넘기고 상품 공급자 위치로 밀린다.",
    basis=["C2-E-002", "C2-M-001", "C2-M-004", "C2-M-007", "C2-E-007", "C2-E-012"])

# ---------- 검증 ----------
ids = {r["id"] for r in records}
_t = {r["id"]: r["type"] for r in records}
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
        elif r["type"] in ("해석", "전망") and b in facts and _t[b] in ("지표", "사건") and not next(x for x in records if x["id"] == b).get("verified"):
            errs.append(f"{r['id']}: 원문 미확인 기록 {b}을 근거로 씀")
if len(ids) != len(records): errs.append("중복 ID")

out = Path(__file__).parent / "records.jsonl"
with open(out, "w", encoding="utf-8") as f:
    for r in records: f.write(json.dumps(r, ensure_ascii=False) + "\n")

print("기록 수:", len(records), dict(Counter(r["type"] for r in records)))
print("원문 미확인 사실:", [r["id"] for r in records if r["type"] in ("지표", "사건") and not r.get("verified")])
inds = {r.get("indicator") for r in records if r["type"] == "지표" and r.get("verified")}
print("값 채워진 추적 지표(확인된 값 기준):", sorted(inds), f"{len(inds)}/8")
print("검증 오류:", errs or "없음")
sys.exit(1 if errs else 0)

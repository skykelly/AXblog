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
add(id="C2-M-001", type="지표", indicator="C2-K1", importance=3, statement="Amazon 쇼핑 Agent Rufus는 2025년 고객 3억 명이 썼고, 연환산 약 120억 달러의 증분 매출을 만들었다.",
    value=120, unit="억 달러(연환산 증분 매출)", as_of="2025", region="US/GLOBAL", definition="Amazon 2025년 4분기 실적 발표(2026년 2월)", extra={"users_2025": "3억 명"},
    sources=src("mr_rufus"), verified=True)
add(id="C2-M-002", type="지표", indicator="C2-K1", importance=2, statement="2026년 1분기 Rufus 월간 이용자는 전년 대비 115%, 이용 활동(engagement)은 400% 늘었다.",
    value=115, unit="% YoY(MAU)", as_of="2026-C1", region="US/GLOBAL", definition="Amazon 1분기 실적 발표", sources=src("mr_rufus"), verified=True)
add(id="C2-M-003", type="지표", indicator="C2-K1", importance=2, statement="Amazon에 따르면 Rufus를 쓰는 고객은 구매를 끝낼 가능성이 60% 높다.",
    value=60, unit="% (구매 완료 가능성 차이)", as_of="2026-02", region="US/GLOBAL", definition="Amazon 발표", sources=src("mr_rufus"), verified=True)
add(id="C2-M-004", type="지표", indicator="C2-K8", importance=2, statement="Amazon 광고 매출은 2026년 1분기 172억 달러로 전년 대비 24% 늘었다.",
    value=24, unit="% YoY", as_of="2026-C1", region="GLOBAL", definition="Amazon 1분기 광고 매출", extra={"ad_revenue": "172억 달러"}, sources=src("mr_rufus"), verified=True)
add(id="C2-M-005", type="지표", indicator="C2-K2", importance=2, statement="Rufus 안의 브랜드 스폰서 질문을 누른 쇼핑객의 약 20%가 그 브랜드에 대해 대화를 이어갔다.",
    value=20, unit="%", as_of="2026-C1", region="US", definition="Amazon 발표, 스폰서 프롬프트 참여 후 대화 지속 비율", sources=src("mr_rufus"), verified=True)
add(id="C2-M-006", type="지표", indicator="C2-K2", importance=1, statement="외부 모니터링 기준 2026년 7월 초 미국 ChatGPT 응답의 약 51%에 광고가 붙었다.",
    value=51, unit="%", as_of="2026-07", region="US", definition="cloro 자체 모니터링, 최근 7일 응답 중 광고 노출 비율", sources=src("cloro_ads"), verified=False,
    check_flags=["출처 등급 C(단일 모니터링 업체) — 판단 근거에서 제외"])
add(id="C2-M-007", type="지표", indicator="C2-K4", importance=3, statement="최근 고객 서비스 상황에서 고객은 기업이 제공한 챗봇보다 ChatGPT·Gemini 같은 서드파티 AI를 약 3배 더 많이 썼다.",
    value=3, unit="배", as_of="2026-02~03", region="GLOBAL", definition="Gartner 고객 조사(B2B·B2C 3,566명)", sources=src("gartner_cs"), verified=True)
add(id="C2-M-008", type="지표", indicator="C2-K4", importance=3, statement="고객의 87%는 AI로 상담하는 기업이라도 사람 상담원 연결은 반드시 있어야 한다고 답했다.",
    value=87, unit="%", as_of="2026-02~03", region="GLOBAL", definition="Gartner 고객 조사", sources=src("gartner_cs"), verified=True)
add(id="C2-M-009", type="지표", indicator="C2-K4", importance=2, statement="생성형 AI를 쓰는 고객의 58%가 AI에게 자기 대신 일을 처리시킨 경험이 있다(B2B는 74%).",
    value=58, unit="%", as_of="2026-02~03", region="GLOBAL", definition="Gartner 고객 조사", sources=src("gartner_cs"), verified=True)
add(id="C2-M-010", type="지표", indicator="C2-K3", importance=2, statement="Google의 Universal Commerce Protocol에는 발표 시점에 20곳 이상이 참여했고, Shopify·Walmart·Target·Etsy·Wayfair가 공동 개발했다.",
    value=20, unit="곳 이상", as_of="2026-01", region="US", definition="UCP 참여 파트너 수", sources=src("aa_ucp"), verified=True)
add(id="C2-M-011", type="지표", indicator="C2-K3", importance=2, statement="Visa의 Agent 결제 준비 프로그램에 아태 50곳 이상이 참여했고, 한국에서는 하나·현대·KB국민·삼성·신한카드와 카카오뱅크가 이름을 올렸다.",
    value=6, unit="곳(한국)", as_of="2026-04", region="KR/APAC", definition="Visa Agentic Ready 참여 발급사", extra={"apac_partners": "50곳 이상", "markets": "한국 포함 10개 시장"},
    sources=src("visa_ap"), verified=True, check_flags=["국가 구분은 회사명으로 추정"])
add(id="C2-M-012", type="지표", indicator="C2-K7", importance=2, statement="카카오는 카카오톡 AI 에이전트를 쓸 수 있는 이용자가 2026년 말 3,100만 명(1분기 카톡 MAU 4,958만 명의 약 62%)이 될 것으로 봤다.",
    value=3100, unit="만 명(예상)", as_of="2026-05", region="KR", definition="카카오 1분기 실적 발표", sources=src("kakao"), verified=True)
add(id="C2-M-013", type="지표", indicator="C2-K7", importance=2, statement="네이버 쇼핑 AI 에이전트 경유 거래액은 3월 대비 6월에 2.7배 이상 늘었다.",
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

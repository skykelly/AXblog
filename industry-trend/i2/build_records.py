"""I2 R1 4유형 기록 생성 + 규칙 검증.
출력: t2/records.jsonl
"""
import json, sys
from pathlib import Path
from collections import Counter

R = "R1"
SRC = {
 "tc_chatgpt": {"url": "https://techcrunch.com/2026/02/27/chatgpt-reaches-900m-weekly-active-users", "publisher": "TechCrunch (OpenAI 발표 인용)", "date": "2026-02-27", "grade": "B"},
 "cc_rev": {"url": "https://enterprisedna.co/resources/news/claude-code-25-billion-arr-anthropic-2026", "publisher": "Enterprise DNA (Anthropic 공개 수치 인용)", "date": "2026-06-14", "grade": "B"},
 "waymo": {"url": "https://electrek.co/2026/07/08/waymo-driverless-las-vegas-four-new-cities/", "publisher": "Electrek", "date": "2026-07-08", "grade": "B"},
 "humanoid": {"url": "https://humanoid.guide/humanoid-deployments-in-2026-favor-figure-and-agility/", "publisher": "Humanoid.guide (기업 발표 정리)", "date": "2026-07-19", "grade": "B"},
 "liferay": {"url": "https://www.cmswire.com/the-wire/new-liferay-study-finds-54-of-companies-are-running-ai-agents-yet-only-25-measure-their-impact/", "publisher": "Liferay 조사 (GlobeNewswire)", "date": "2026-08-12", "grade": "B"},
 "adversa": {"url": "https://adversa.ai/blog/ai-coding-agent-incidents/", "publisher": "Adversa AI (보안 업체 집계)", "date": "2026-08-04", "grade": "B"},
 "openai_work": {"url": "https://openai.com/index/chatgpt-for-your-most-ambitious-work/", "publisher": "OpenAI 공식 발표", "date": "2026-07-09", "grade": "A"},
 "tesla": {"url": "https://engadget.com/2240859/tesla-robotaxi-fleet-might-finally-be-driving-around-austin-unsupervised", "publisher": "Engadget (The Verge·크라우드소싱 추적 인용)", "date": "2026-08-20", "grade": "B"},
 "kakao_av": {"url": "https://biz.sbs.co.kr/amp/article/20000297494", "publisher": "SBS Biz", "date": "2026-03-15", "grade": "B"},
 "hyundai_atlas": {"url": "https://www.heraldk.com/article/2026010514301001612", "publisher": "헤럴드경제 (현대차그룹 CES 발표)", "date": "2026-01-05", "grade": "B"},
}
def src(*keys): return [dict(SRC[k], key=k) for k in keys]

base = dict(question="I2", question_version="v1.0", first_seen=R, last_seen=R, status="유효", replaces=None, check_flags=[])
records = []
def add(**kw):
    r = dict(base); r.update(kw); records.append(r)

# ---------- 지표 (M) ----------
add(id="I2-M-001", type="지표", indicator="I2-T1", importance=3, statement="ChatGPT 주간 이용자는 2026년 2월 9억 명으로 넉 달 새 1억 명 늘었고, 유료 구독자는 5천만 명이다.",
    value=9, unit="억 명(주간)", as_of="2026-02", region="GLOBAL", definition="OpenAI 발표, ChatGPT 주간 활성 이용자", prev_value=8, extra={"paid_subscribers": "5,000만 명"},
    sources=src("tc_chatgpt"), verified=True)
add(id="I2-M-002", type="지표", indicator="I2-T2", importance=3, statement="Claude Code의 연환산 매출은 2026년 2월 25억 달러를 넘었고, 주간 이용자는 1월 초부터 5주 만에 두 배 넘게 늘었다.",
    value=25, unit="억 달러 이상(연환산)", as_of="2026-02", region="GLOBAL", definition="Anthropic 공개 수치(투자 유치 시점), 2차 보도", sources=src("cc_rev"), verified=True,
    check_flags=["2차 보도 — Anthropic 원문 미대조"])
add(id="I2-M-003", type="지표", indicator="I2-T2", importance=2, statement="Uber에서는 Claude Code를 받은 엔지니어 약 5천 명 중 84%가 매달 쓰고, 커밋 코드의 70%를 AI가 썼다(2026년 4월).",
    value=70, unit="% (AI 작성 커밋 코드)", as_of="2026-04", region="US", definition="대형 고객 사례, 2차 보도", sources=src("cc_rev"), verified=True)
add(id="I2-M-004", type="지표", indicator="I2-T4", importance=3, statement="Waymo는 2026년 들어 주간 유료 탑승 약 50만 회, 차량 약 3,500대로 미국 11개 도시를 운행하고 있다. 누적 탑승은 2천만 회를 넘었고, 연말 목표는 주 100만 회다.",
    value=50, unit="만 회(주간 유료 탑승)", as_of="2026-07", region="US", definition="Waymo 주간 유료 탑승 수", extra={"fleet": "약 3,500대", "cities": 11, "cumulative": "2천만 회 이상"},
    sources=src("waymo"), verified=True)
add(id="I2-M-005", type="지표", indicator="I2-T5", importance=2, statement="Agility Robotics의 휴머노이드 Digit은 9개 고객 시설에서 누적 6만 5천 시간 이상 일했다. Figure는 BMW 공장에서 11개월 파일럿으로 1,250시간 동안 부품 9만 개 이상을 옮겼다.",
    value=65000, unit="시간(Agility 누적 운영)", as_of="2026-07", region="US", definition="기업 발표 운영 시간", sources=src("humanoid"), verified=True, check_flags=["기업 자체 발표 수치"])
add(id="I2-M-006", type="지표", indicator="I2-T5", importance=2, statement="중국 Unitree는 2025년 휴머노이드 약 5,500대를 출하했고 2026년 1만~2만 대를 목표로 한다. Tesla Optimus는 아직 외부 판매가 없고 공개 판매는 2027년 말로 예상된다.",
    value=5500, unit="대(2025 출하)", as_of="2026-07", region="CN/US", definition="휴머노이드 출하량", sources=src("humanoid"), verified=True)
add(id="I2-M-007", type="지표", indicator="I2-T6", importance=3, statement="미국 기업의 54%가 AI 에이전트를 운영하거나 시범 운영하고 있지만, 성과를 명확한 지표로 측정하는 곳은 25%다. 회사 차원의 AI 사용 정책이 있는 곳도 24%에 그친다.",
    value=54, unit="%", as_of="2026-08", region="US", definition="Liferay 조사, AI 의사결정·실무자 500명", extra={"measure_kpi": "25%", "ai_policy": "24%"}, sources=src("liferay"), verified=True)
add(id="I2-M-008", type="지표", indicator="I2-T7", importance=2, statement="2025년 6월부터 2026년 7월까지 코딩 에이전트가 데이터를 지운 공개 사고가 9건 집계됐다. 운영 데이터베이스 삭제, 클라우드 장애, 홈 디렉터리 삭제 등이며 상당수는 복구되지 못했다.",
    value=9, unit="건", as_of="2026-07", region="GLOBAL", definition="보안 업체 집계, 데이터 삭제 사고", sources=src("adversa"), verified=True, check_flags=["보안 업체 집계 — 사용자 보고 기반"])

# ---------- 사건 (E) ----------
add(id="I2-E-001", type="사건", importance=2, statement="현대차그룹이 Boston Dynamics 휴머노이드 Atlas를 2028년부터 미국 조지아 공장의 부품 분류 공정에 투입하고, 2030년 이후 조립 공정으로 넓히겠다고 발표했다.",
    date="2026-01-05", actor="현대차그룹", sources=src("hyundai_atlas"), verified=True)
add(id="I2-E-002", type="사건", importance=2, statement="카카오모빌리티가 서울 강남에서 평일 밤 10시~새벽 5시 자율주행 택시 운행을 시작했다. 처음에는 무료이고 4월부터 유료로 전환할 계획이다.",
    date="2026-03-16", actor="카카오모빌리티·서울시", sources=src("kakao_av"), verified=True, check_flags=["안전요원 탑승 여부는 기사에 없음"])
add(id="I2-E-003", type="사건", importance=3, statement="Waymo가 라스베이거스에서 완전 무인 운행을 시작하고 덴버·샌디에이고·탬파를 다음 지역으로 예고했다.",
    date="2026-07-08", actor="Waymo", sources=src("waymo"), verified=True)
add(id="I2-E-004", type="사건", importance=3, statement="OpenAI가 앱과 파일을 넘나들며 몇 시간짜리 프로젝트를 수행하는 ChatGPT Work를 정식 출시했다. 이용량은 공개하지 않았다.",
    date="2026-07-09", actor="OpenAI", sources=src("openai_work"), verified=True)
add(id="I2-E-005", type="사건", importance=2, statement="Claude Code와 Opus 5로 데이터베이스 마이그레이션을 하던 개발자의 운영 데이터베이스 테이블이 모두 초기화됐다. 모델이 피해를 스스로 알렸고 데이터는 수 시간에 걸쳐 복구됐다.",
    date="2026-07", actor="개인 개발자", sources=src("adversa"), verified=True, check_flags=["사용자 보고 기반 — 시험용 프로젝트였다는 설명"])
add(id="I2-E-006", type="사건", importance=2, statement="Tesla 오스틴 로보택시가 안전요원 없이 운행하는 것으로 보인다는 보도가 나왔다. 크라우드소싱 추적 앱 기준 최근 2주 170회 탑승이 모두 무감독이었지만, Tesla는 공식 확인하지 않았다.",
    date="2026-08-20", actor="Tesla", sources=src("tesla"), verified=True, check_flags=["회사 미확인 — 추정치"])

# ---------- 해석 (I) ----------
add(id="I2-I-001", type="해석", importance=3, target="대화형 Assistant·Coding Agent", direction="강화",
    statement="이용량과 매출을 공개할 만큼 '대규모 운영'에 들어선 소프트웨어 제품은 대화형 Assistant와 Coding Agent 둘이다. Coding Agent는 대형 고객에서 커밋 코드의 대부분을 쓰는 수준까지 왔다.",
    basis=["I2-M-001", "I2-M-002", "I2-M-003"])
add(id="I2-I-002", type="해석", importance=3, target="로보택시", direction="강화",
    statement="물리 세계에서 대규모 운영에 들어선 AI 제품은 로보택시, 그중에서도 Waymo 하나다. 주간 탑승 50만 회에 11개 도시로 넓어졌고, 경쟁 사업자는 아직 무인 운행을 공식 확인하지 못했다.",
    basis=["I2-M-004", "I2-E-003", "I2-E-006"])
add(id="I2-I-003", type="해석", importance=3, target="업무형 Agent", direction="중립",
    statement="시간 단위 업무 Agent는 정식 출시됐지만 운영 성과는 공개되지 않았다. 기업 절반이 에이전트를 운영·시범 중이지만 성과를 지표로 재는 곳은 4분의 1이라, '써 보는 단계'와 '운영 단계' 사이에 있다.",
    basis=["I2-E-004", "I2-M-007"])
add(id="I2-I-004", type="해석", importance=2, target="휴머노이드", direction="중립",
    statement="휴머노이드는 고객 현장 파일럿과 초기 상용 단계다. 운영 시간은 쌓이고 있지만 단일 고객 대량 배치는 없고, 출하 대수는 중국 Unitree가 앞선다.",
    basis=["I2-M-005", "I2-M-006"])
add(id="I2-I-005", type="해석", importance=3, target="운영 실패", direction="약화",
    statement="권한을 받은 에이전트가 운영 데이터를 지우는 사고가 1년 넘게 반복되고 있다. 사람의 승인 단계를 우회하거나 지시를 무시한 사례가 많아, 업무형 Agent 확산의 가장 직접적인 걸림돌이 되고 있다.",
    basis=["I2-M-008", "I2-E-005"])
add(id="I2-I-006", type="해석", importance=2, target="한국 상용화", direction="중립",
    statement="한국의 물리 AI 상용화는 발표·제한 운행 단계다. 자율주행 택시는 강남 심야로 구역과 시간을 묶어 시작했고, 휴머노이드는 2028년 현장 투입 계획이다.",
    basis=["I2-E-001", "I2-E-002"])

# ---------- 세부 전망 (F) ----------
add(id="I2-F-001", type="전망", importance=3, status="유효", forecast_status="진행 중",
    statement="Waymo는 2026년 말까지 주간 유료 탑승 100만 회를 달성했다고 발표할 것이다.", due="2027-01-31", condition="없음",
    method="Waymo 공식 발표 확인", basis=["I2-M-004"], result=None)
add(id="I2-F-002", type="전망", importance=3, status="유효", forecast_status="진행 중",
    statement="OpenAI 또는 Anthropic은 2027년 6월 말까지 시간 단위 업무 Agent의 이용자 수나 작업 수를 공개할 것이다.", due="2027-06-30", condition="없음",
    method="OpenAI·Anthropic 공식 발표 확인", basis=["I2-E-004"], result=None)
add(id="I2-F-003", type="전망", importance=2, status="유효", forecast_status="진행 중",
    statement="Tesla는 2026년 말까지 2개 이상 도시에서 안전요원 없는 유료 로보택시 운행을 공식 확인할 것이다.", due="2026-12-31", condition="없음",
    method="Tesla 공식 발표·실적 발표 확인", basis=["I2-E-006"], result=None)
add(id="I2-F-004", type="전망", importance=2, status="유효", forecast_status="진행 중",
    statement="Figure 또는 Agility는 2027년 6월 말까지 단일 고객 현장에 휴머노이드 100대 이상을 상용 배치했다고 발표할 것이다.", due="2027-06-30", condition="없음",
    method="Figure·Agility·고객사 공식 발표 확인", basis=["I2-M-005"], result=None)
add(id="I2-F-005", type="전망", importance=2, status="유효", forecast_status="진행 중",
    statement="서울 자율주행 택시는 2027년 6월 말까지 운전석에 사람이 없는 유상 운행을 시작할 것이다.", due="2027-06-30", condition="없음",
    method="서울시·국토교통부·운영사 발표 확인", basis=["I2-E-002"], result=None)
add(id="I2-F-006", type="전망", importance=2, status="유효", forecast_status="진행 중",
    statement="2027년 6월 말까지 주요 AI 기업의 에이전트가 기업 고객의 운영 데이터를 손상한 사건이 회사의 공식 사후 보고로 공개될 것이다.", due="2027-06-30", condition="없음",
    method="OpenAI·Anthropic·Google·Microsoft·Amazon 사후 보고 또는 공식 확인 확인", basis=["I2-M-008"], result=None)

# ---------- 메인 질문 시나리오 ----------
add(id="I2-F-101", type="전망", importance=3, status="유효", forecast_status="진행 중", scenario="낙관",
    statement="2027년 말까지 대규모 운영 영역이 셋에서 다섯으로 늘어난다. 업무형 Agent가 이용량과 성과를 공개하고, 로보택시는 Waymo 주 100만 회에 Tesla 무인 유료 운행이 더해지며, 휴머노이드가 고객 현장에 100대 단위로 들어간다.",
    milestones=[
        {"by": "2026-12", "text": "Waymo 주 100만 회, Tesla 무인 유료 2개 도시"},
        {"by": "2027-06", "text": "업무형 Agent 이용량 공개, 휴머노이드 단일 고객 100대 배치"},
        {"by": "2027-06", "text": "서울 무인 유상 자율주행 택시"}],
    due="2027-12-31", condition="대형 에이전트 사고나 로보택시 중대 사고로 규제가 강화되지 않을 경우",
    method="세 가지 중 두 가지 이상 충족 시 적중: (1) 업무형 Agent의 이용량·성과 공식 공개 (2) 로보택시 2개 이상 사업자의 무인 유료 운행 + Waymo 주 100만 회 (3) 휴머노이드 단일 고객 100대 이상 상용 배치",
    basis=["I2-E-004", "I2-M-004", "I2-M-005", "I2-E-006"],
    signposts=[{"id": "I2-F-001", "on_hit": "낙관", "on_miss": "비관"}, {"id": "I2-F-002", "on_hit": "낙관", "on_miss": "비관"},
               {"id": "I2-F-003", "on_hit": "낙관"}, {"id": "I2-F-004", "on_hit": "낙관"}, {"id": "I2-F-005", "on_hit": "낙관"}, {"id": "I2-F-006", "on_hit": "비관"}], result=None)
add(id="I2-F-102", type="전망", importance=3, status="유효", forecast_status="진행 중", scenario="비관",
    statement="2027년 말에도 대규모 운영은 Assistant·Coding Agent·Waymo 세 곳에 머문다. 업무형 Agent는 사고와 성과 측정 문제로 시범 운영에 묶이고, 휴머노이드는 파일럿을 반복한다.",
    milestones=[
        {"by": "2027-06", "text": "업무형 Agent 이용량 비공개 지속"},
        {"by": "2027-06", "text": "에이전트의 운영 데이터 손상 사고 공식 확인"},
        {"by": "2027-12", "text": "휴머노이드 단일 고객 배치 수십 대 이하"}],
    due="2027-12-31", condition="없음",
    method="낙관 시나리오의 판정 조건 세 가지 중 하나 이하만 충족 시 적중",
    basis=["I2-M-007", "I2-M-008", "I2-M-006"],
    signposts=[], result=None)

# ---------- 2026-10-11 검증 반영 ----------
CHG = "2026-10-11"
SRC.update({
 "cb_chatgpt": {"url": "https://cryptobriefing.com/chatgpt-one-billion-weekly-users/", "publisher": "CryptoBriefing (ChatGPT 10억, OpenAI 확인 보도)", "date": "2026-09-29", "grade": "B"},
 "alphabet_q2": {"url": "https://blog.google/company-news/inside-google/message-ceo/alphabet-earnings-q2-2026/", "publisher": "Alphabet 2026 Q2 CEO 발언 (Google 블로그)", "date": "2026-07-22", "grade": "A"},
 "ms_fy26": {"url": "https://office365itpros.com/2026/07/30/fy26-q4-microsoft-results/", "publisher": "Microsoft 365 for IT Pros (FY26 Q4 해설)", "date": "2026-07-30", "grade": "B"},
 "unite_anth": {"url": "https://www.unite.ai/?p=453467", "publisher": "Unite.AI (Anthropic 650억 달러, Bloomberg 인용)", "date": "2026-08-17", "grade": "B"},
 "waymo_blog": {"url": "https://waymo.com/blog/2026/10/waymo-closes-5-billion-debt-financing/", "publisher": "Waymo 블로그 (50억 달러 부채 조달)", "date": "2026-10-08", "grade": "A"},
 "cb_waymo": {"url": "https://cryptobriefing.com/waymo-paid-robotaxi-denver-san-diego-tampa/", "publisher": "CryptoBriefing (Waymo 덴버·샌디에이고·탬파)", "date": "2026-09-01", "grade": "B"},
 "baidu_q2": {"url": "https://www.sec.gov/Archives/edgar/data/0001329099/000119312526355431/d112854dex991.htm", "publisher": "Baidu Q2 2026 실적 릴리스 (SEC 6-K)", "date": "2026-08-18", "grade": "A"},
 "mkt_baidu": {"url": "https://www.marketbeat.com/instant-alerts/baidu-q2-earnings-call-highlights-2026-08-18/", "publisher": "MarketBeat (Baidu Q2 콜 요약)", "date": "2026-08-18", "grade": "B"},
 "evwire": {"url": "https://evwire.com/p/tesla-robotaxi-2-4-million-paid-miles-six-metros", "publisher": "EVwire (Tesla Q2 주주 업데이트)", "date": "2026-07-22", "grade": "B"},
 "scd_tesla": {"url": "https://smartcitiesdive.com/news/tesla-robotaxis-cybercab-safety/825988", "publisher": "Smart Cities Dive (Tesla Q2 콜)", "date": "2026-07-23", "grade": "B"},
 "kpmg_q3": {"url": "https://kpmg.com/us/en/media/news/q3-ai-pulse-2026.html", "publisher": "KPMG Q3 2026 AI Pulse", "date": "2026-09-24", "grade": "A"},
 "eweek_sag": {"url": "https://www.eweek.com/news/china-humanoid-robots-agibot-unitree-apac/", "publisher": "eWeek (SAG 상반기 휴머노이드 출하)", "date": "2026-08-11", "grade": "B"},
 "scmp_agibot": {"url": "https://www.scmp.com/tech/tech-trends/article/3363544/agibot-overtakes-unitree-top-global-humanoid-robot-vendor-first-half-amid-ipo-push", "publisher": "SCMP (AgiBot, Unitree 추월)", "date": "2026-08-10", "grade": "B"},
 "techrepublic_pocket": {"url": "https://www.techrepublic.com/fr/article/ai-agent-deletes-company-database-admits-violating-guardrails/", "publisher": "TechRepublic (PocketOS 삭제 사고)", "date": "2026-05-04", "grade": "B"},
 "daum_sangam": {"url": "https://v.daum.net/v/20260630111713463", "publisher": "다음뉴스 (서울 상암 레벨4 로보택시)", "date": "2026-06-30", "grade": "B"},
 "asiae_seoul": {"url": "https://view.asiae.co.kr/article/2026070210170759922", "publisher": "아시아경제 (하반기 달라지는 서울생활)", "date": "2026-07-02", "grade": "B"},
})
def _get(i): return next(r for r in records if r["id"] == i)
def revise(i, kind, why, **ch):
    r = _get(i)
    r.setdefault("revisions", []).append({"on": CHG, "kind": kind, "before": r.get("statement") if "statement" in ch else None, "why": why})
    r.update(ch)
def _more(i, *keys): return _get(i)["sources"] + src(*keys)
def _fl(i, *new): return _get(i)["check_flags"] + list(new)

# --- 신규 지표·사건 (수정한 해석·전망이 근거로 삼는 최소한) ---
add(id="I2-M-009", type="지표", indicator="I2-T1", importance=3, added_on=CHG,
    statement="Gemini 앱은 월간 이용자 9억 5천만 명 이상(2026년 2분기)이다. Microsoft 365 Copilot은 유료 3천만 석으로 분기마다 늘었다(1,500만→2,000만→3,000만, FY26 4분기). ChatGPT가 주간, Gemini가 월간 기준이라 같은 선에 놓고 비교하지 않는다.",
    value=9.5, unit="억 명 이상(월간, Gemini 앱)", as_of="2026-Q2", region="GLOBAL", definition="Alphabet 2분기 CEO 발언, Microsoft FY26 4분기 해설",
    extra={"m365_copilot_paid_seats": "3,000만 석"}, sources=src("alphabet_q2", "ms_fy26"), verified=True,
    check_flags=["Microsoft 수치는 해설 사이트 인용 — 실적 원문 확인 필요", "월간(Gemini)과 주간(ChatGPT) 기준이 다름"])
add(id="I2-M-010", type="지표", indicator="I2-T6", importance=3, added_on=CHG,
    statement="KPMG 2026년 3분기 조사(매출 10억 달러 이상 미국 기업 314곳, 7~8월)에서 62%가 에이전트를 구축·배치·개발 중(직전 분기 53%)이라 했고, 약 60%가 측정 가능한 사업 가치를 보고했으며 70%가 AI 모니터링 대시보드를 쓴다. '개발 중'을 포함해 운영 비율이 아니고 사업 가치는 자기 평가다.",
    value=62, unit="% (구축·배치·개발 중)", as_of="2026-08", region="US", definition="KPMG AI Pulse, 대기업 314곳 설문", prev_value=53,
    extra={"measurable_value": "약 60%", "monitoring_dashboard": "70%"}, sources=src("kpmg_q3"), verified=True,
    check_flags=["Liferay(개인 500명)와 응답자·정의가 달라 합산·비교하지 않음", "'운영' 비율이 아니라 '개발 중' 포함 비율"])
add(id="I2-M-011", type="지표", indicator="I2-T4", importance=2, added_on=CHG,
    statement="중국 Baidu Apollo Go는 2026년 2분기 완전 무인 탑승 약 100만 회(콜 요약), 누적 2,300만 회 이상, 28개 도시를 공개했다. 분기 100만 회는 주 환산 약 8만 회로 영역 기준(주 10만 회)에 못 미친다(역산 추정).",
    value=100, unit="만 회(분기 완전 무인)", as_of="2026-Q2", region="CN", definition="Baidu 2분기 실적 릴리스·콜 요약",
    extra={"cities": 28, "cumulative": "2,300만 회 이상"}, sources=src("baidu_q2", "mkt_baidu"), verified=True,
    check_flags=["도시 수는 실적 릴리스(A), 탑승 횟수는 콜 요약(B)", "누적에는 안전요원 탑승분이 섞였을 수 있음 — 확인 필요", "주 환산은 역산 추정"])
add(id="I2-M-012", type="지표", indicator="I2-T5", importance=2, added_on=CHG,
    statement="2026년 상반기 전 세계 휴머노이드 출하는 약 1만 9,100대(전년 대비 +272%)로 AgiBot 약 8,400대(44%), Unitree 약 5,900대(31%)이고 중국 업체가 97% 이상이다(Smart Analytics Global).",
    value=19100, unit="대(2026 상반기 출하)", as_of="2026-H1", region="GLOBAL", definition="조사사 집계, 출하 대수",
    extra={"agibot": "약 8,400대", "unitree": "약 5,900대"}, sources=src("eweek_sag", "scmp_agibot"), verified=True,
    check_flags=["단일 조사사 값", "출하는 현장 가동이 아니며 연구·교육·전시 구매가 섞였을 수 있음 — 확인 필요"])
add(id="I2-E-007", type="사건", importance=2, added_on=CHG,
    statement="서울시가 2026년 11월 마포 상암동에서 레벨4 로보택시를 앱 호출로 본격 도입한다(초기에는 안전관리자가 조수석에 타고 평일 운행). 요금은 보도에 없다.",
    date="2026-06-30", actor="서울시", sources=src("daum_sangam", "asiae_seoul"), verified=True,
    check_flags=["계획 단계 — 서울시 1차 자료 미확인(확인 필요)", "요금·유상 여부 미확인"])

# --- 지표·사건 ---
revise("I2-M-001", "갱신", "9월에 OpenAI가 주간 이용자 10억 명 이상을 확인했다는 보도가 나왔지만 대상(ChatGPT 단독인지 OpenAI 제품군인지)이 보도마다 달라 2월 값을 최신 확정값으로 두지 못한다.",
    statement="ChatGPT 주간 이용자는 2026년 2월 9억 명이고 유료 구독자는 5천만 명이다. 9월에는 OpenAI가 주간 이용자 10억 명 이상(8월 중순 기준)을 확인했다는 보도가 나왔으나 대상이 ChatGPT 단독인지 OpenAI 제품군인지 보도마다 달라 확인 필요하다.",
    sources=_more("I2-M-001", "cb_chatgpt"), check_flags=["10억 명 이상은 2차 보도 — OpenAI 원문 미열람, 대상(ChatGPT 단독/제품군) 확인 필요", "유료 구독자는 2월 이후 새 공식 수치를 찾지 못함"])
revise("I2-M-002", "갱신", "기록의 2월 값은 2차 글로만 달려 있고 이후 매출이 크게 늘었다. Claude Code 단독 최신 수치는 없고 Anthropic 전체 매출은 단독 매출과 다르다.",
    statement="Claude Code의 연환산 매출은 2026년 2월 25억 달러를 넘었고, 주간 이용자는 1월 초부터 5주 만에 두 배 넘게 늘었다. 이후 Claude Code 단독 수치는 확인하지 못했다. Anthropic 전체 연환산 매출은 7월 말 650억 달러 이상으로 보도됐지만 익명 소식통 기반 추정이며 Claude Code 매출과 다르다. OpenAI Codex는 주간 이용자 500만 명 이상(2026년 7월 OpenAI 발표)이다.",
    sources=_more("I2-M-002", "unite_anth", "openai_work"), check_flags=["2차 보도 — Anthropic 원문 미대조", "650억 달러는 Bloomberg 인용 보도(익명 소식통)로 추정 — 확인 필요", "근거 글의 제목('13개월에 25억 달러')과 본문('2월 달성')이 맞지 않음"])
revise("I2-M-003", "상충", "기록이 단 출처에서 Uber 수치의 별도 근거가 확인되지 않는다. 이 지표의 단독 근거가 2차 글 하나다.",
    statement="2차 글에 따르면 Uber에서는 Claude Code를 받은 엔지니어 약 5천 명 중 84%가 매달 쓰고 커밋 코드의 70%를 AI가 썼다(2026년 4월). Uber·Anthropic 원문에서는 확인하지 못했다.",
    check_flags=["Uber 수치는 2차 글 단독 — 원문 확인 필요", "출처로 건 Anthropic 페이지에는 Uber가 없음"])
revise("I2-M-004", "갱신", "도시 수·기준 시점이 낡았다. 주간 유료 탑승 50만 회와 차량 3,500대는 1분기 실적 시점 값이고 이후 새 공식 수치가 없다.",
    statement="Waymo는 2026년 7월 기준 미국 11개 도시를 운행했고, 9월 1일 덴버·샌디에이고·탬파에서 유료 공개를 시작해 14개 시장이 됐다. 10월 8일 Waymo 블로그는 지난달 15번째 미국 도시를 열었다고 밝혔다. 주간 유료 탑승 약 50만 회와 차량 약 3,500대는 2026년 1분기 실적 시점 수치이고 이후 새 공식 수치는 없다(차량은 4,000대 이상으로 보도, 확인 필요). 누적 탑승은 2천만 회를 넘었고 연말 목표는 주 100만 회다.",
    as_of="2026-Q1", extra={"fleet": "약 3,500대(1분기 시점, 4,000대 이상 보도)", "cities": "15번째 도시 개설(2026-09)", "cumulative": "2천만 회 이상"},
    sources=_more("I2-M-004", "cb_waymo", "waymo_blog"), check_flags=["탑승·차량 수치는 1분기 시점 — 이후 공식 수치 없음", "9월 1일 시작·4,000대는 1건 보도 — 확인 필요"])
revise("I2-M-007", "상충", "응답자는 기업이 아니라 AI 의사결정·실무자 500명이고 벤더 조사이며 '운영·시범·KPI' 정의가 없다. KPMG와 분모·정의가 달라 비교할 수 없다.",
    statement="Liferay 조사(미국 AI 의사결정·실무자 500명, 벤더 조사)에서 54%가 AI 에이전트를 운영하거나 시범 운영한다고 답했고 25%가 성과를 명확한 지표로 측정한다고 했으며, 회사 차원의 AI 사용 정책이 있는 곳은 24%다. '운영'·'시범'·'KPI'의 정의는 제시되지 않았다. KPMG 대기업 조사(I2-M-010)와는 응답자와 정의가 달라 합산·비교하지 않는다.",
    check_flags=["응답자는 기업이 아닌 개인 500명 — 정의 미제시", "조사 시점·응답 가중치 미공개", "KPMG와 비교 금지"])
revise("I2-M-008", "누락정정", "2026년 4월 PocketOS 사건이 집계에서 빠져 있어 9건은 하한이다. 일부 사건은 분쟁 중이다.",
    statement="2025년 6월부터 2026년 7월까지 코딩 에이전트가 데이터를 지운 공개 사고가 보안 업체 목록에 9건 집계됐다. 운영 데이터베이스 삭제, 클라우드 장애, 홈 디렉터리 삭제 등이며 상당수는 복구되지 못했다. 2026년 4월 PocketOS 사건(창업자 주장: 에이전트가 운영 데이터베이스와 백업을 삭제, 3개월 전 백업으로 복구)은 목록에 없어 실제로는 10건 이상이다(하한).",
    sources=_more("I2-M-008", "techrepublic_pocket"), check_flags=["보안 업체 집계 — 사용자 보고 기반", "PocketOS는 창업자 주장 중심 보도, Cursor·Anthropic 응답 없음 — 확인 필요", "집계에 분쟁 중인 사건 포함(Amazon은 Kiro 건을 권한 설정 문제로 반박)"])
revise("I2-E-003", "갱신", "'다음 지역으로 예고'한 도시들이 9월 1일 유료 공개로 이어졌다.",
    statement="Waymo가 라스베이거스에서 완전 무인 운행을 시작했고(7월 8일), 덴버·샌디에이고·탬파에서는 9월 1일 유료 공개를 시작한 것으로 보도됐다(1건 보도, 확인 필요).",
    sources=_more("I2-E-003", "cb_waymo", "waymo_blog"), check_flags=["9월 1일 시작은 CryptoBriefing 1건 — 확인 필요", "Electrek 기사는 세 도시의 시작일을 적지 않음"])
revise("I2-E-004", "갱신", "ChatGPT Work 발표문에 Codex 이용량(주간 500만 명 이상, 비개발 업무 100만 명 이상)이 함께 공개돼 '이용량 공개 없음'만 쓰면 시간 단위 업무 Agent 계열 이용량이 전혀 없는 것처럼 읽힌다.",
    statement="OpenAI가 앱과 파일을 넘나들며 몇 시간짜리 프로젝트를 수행하는 ChatGPT Work를 정식 출시했다. ChatGPT Work 자체의 이용량은 공개하지 않았지만, 같은 발표문에서 Codex 주간 이용자 500만 명 이상, 그중 100만 명 이상이 소프트웨어 개발 밖 업무에 쓴다고 밝혔다.",
    check_flags=["Codex 이용량이 업무형 Agent '대규모 운영' 기준(유료 기업 1만 곳 또는 연환산 매출 10억 달러)에 해당하는지는 정의가 달라 단계 상향 확인 필요", "Codex는 Coding Agent에도 계상돼 이중 집계 가능", "비개발 업무 100만 명이 시간 단위 작업을 하는지·성과가 있는지 미공개"])
revise("I2-E-006", "갱신", "7월 22일 Tesla 2분기 주주 업데이트 보도가 8월 20일 '공식 확인 안 함' 서술과 시점상 어긋난다. 무감독 주행(약 38만 마일)과 유료 전체(약 240만 마일)는 다른 지표다.",
    statement="Tesla는 2026년 7월 22일 2분기 주주 업데이트에서 오스틴 등 6개 도시 무감독 운행과 누적 유료 주행 약 240만 마일을 밝힌 것으로 보도됐다. 무감독 주행은 약 38만 마일이고 240만 마일에는 샌프란시스코 베이의 안전요원 탑승 주행이 포함돼 '무감독 유료'로 읽을 수 없다. 8월 20일 보도는 오스틴이 크라우드소싱 추적 앱 기준 최근 2주 170회 탑승이 모두 무감독으로 보인다고 했다.",
    date="2026-07-22", sources=_more("I2-E-006", "evwire", "scd_tesla"),
    check_flags=["Tesla 원문(ir.tesla.com) 미열람 — 보도 3건 인용, 확인 필요", "Smart Cities Dive 제목은 '4개 도시'로 불일치", "무감독과 유료가 같은 지표로 공개되는지 불분명"])

# --- 해석 ---
revise("I2-I-001", "누락정정", "R1은 ChatGPT만 근거로 들어 Assistant '대규모 운영' 판정이 한 회사에 치우쳤다. Gemini 앱과 Microsoft 365 Copilot 규모도 공개돼 있다. 판정 단계는 그대로다.",
    statement="이용량과 매출을 공개한 '대규모 운영' 소프트웨어 제품은 대화형 Assistant와 Coding Agent 둘이다. Assistant는 ChatGPT 외에 Gemini 앱(월간 9.5억 명 이상)과 Microsoft 365 Copilot(유료 3천만 석)도 규모를 공개했다(주간·월간 기준이 달라 직접 비교하지 않는다). Coding Agent는 연환산 매출이 25억 달러를 넘었고, 대형 고객 사례에서는 커밋 코드의 대부분을 쓰는 수준이라는 보도가 있다(2차 보도, 확인 필요).",
    basis=["I2-M-001", "I2-M-009", "I2-M-002", "I2-M-003"])
revise("I2-I-002", "단정반증", "'Waymo 하나'와 '경쟁 사업자는 무인 운행을 공식 확인하지 못했다'는 Baidu Apollo Go(실적 릴리스)와 Tesla(2분기 업데이트 보도)로 반증된다. Baidu는 주 환산 약 8만 회로 영역 기준에 못 미쳐 판정 단계는 그대로다.",
    statement="물리 세계에서 대규모 운영에 들어선 AI 제품은 로보택시이고, 규모는 Waymo가 가장 크다. 주간 유료 탑승 약 50만 회(1분기 시점)에 14개 이상 시장으로 넓어졌다. Baidu Apollo Go는 2분기 완전 무인 약 100만 회·28개 도시를 공개했지만 주 환산 약 8만 회로 영역 기준(주 10만 회)에 못 미친다(역산 추정). Tesla는 6개 도시 무감독 운행을 밝힌 것으로 보도됐으나 원문 확인이 필요하다.",
    basis=["I2-M-004", "I2-E-003", "I2-E-006", "I2-M-011"], check_flags=["Tesla 원문 미열람 — 확인 필요", "Baidu 주 환산은 역산 추정"])
revise("I2-I-003", "상충", "기업 도입 수치가 조사마다 갈린다. KPMG는 대기업 62%가 구축·배치·개발 중이라 했지만 '운영' 비율이 아니고 Liferay와 응답자·정의가 달라 단계 상향은 확정하지 못한다.",
    statement="시간 단위 업무 Agent는 정식 출시됐지만 ChatGPT Work의 이용량·성과는 공개되지 않았고, 같은 발표문에서 밝힌 Codex 주간 이용자 500만 명 이상(비개발 업무 100만 명 이상)만 있다. 기업 도입 수치는 조사마다 정의가 달라 갈린다. Liferay(AI 의사결정·실무자 500명)는 54%가 에이전트를 운영·시범 중, 25%가 성과를 지표로 측정한다고 했고, KPMG(매출 10억 달러 이상 미국 기업 314곳)는 62%가 구축·배치·개발 중, 약 60%가 측정 가능한 사업 가치를 보고했다고 했다. 두 조사 모두 '운영' 비율이 아니어서 '써 보는 단계'와 '운영 단계' 사이로 두되 단계 상향 여부는 확인 필요다.",
    basis=["I2-E-004", "I2-M-007", "I2-M-010"],
    check_flags=["단계 상향 후보(Codex 이용량·KPMG 조사) — 영역 기준과 정의가 달라 현재 판정 유지, 확인 필요", "KPMG '측정 가능한 사업 가치'는 자기 평가 설문, Liferay '성과 측정'과 문항이 다름"])
revise("I2-I-004", "상충", "'출하 대수는 Unitree가 앞선다'는 2025년에만 맞고 2026년 상반기는 AgiBot이 앞선다. 상반기 약 1.9만 대 출하를 '대규모 운영'으로 읽을지는 정의 차이다(출하≠가동, 단일 조사사).",
    statement="휴머노이드는 고객 현장 파일럿과 초기 상용 단계다. 운영 시간은 쌓이고 있지만 단일 고객 대량 배치는 확인되지 않았다. 출하 대수는 2025년에는 Unitree가 앞섰고(약 5,500대), 2026년 상반기에는 AgiBot 약 8,400대, Unitree 약 5,900대 등 전 세계 약 1만 9,100대로 중국 업체가 97% 이상이라는 조사가 있다(단일 조사사). 출하는 현장 가동이 아니어서 영역 기준(상업 현장 유료 가동 1,000대)과 다르며, 단계 상향 여부는 확인 필요다.",
    basis=["I2-M-005", "I2-M-006", "I2-M-012"],
    check_flags=["단계 상향 후보(상반기 출하 공개) — 출하≠가동, 단일 조사사라 현재 판정 유지, 확인 필요"])
revise("I2-I-005", "단정반증", "사고가 '가장 직접적인 걸림돌'이라는 순위 근거가 없다. 공개 사고는 10건 안팎이고 이용 규모 대비 비율을 알 수 없으며 일부는 개인·시험 환경이었다.",
    statement="권한을 받은 에이전트가 운영 데이터를 지우는 공개 사고가 1년 넘게 반복되고 있다(집계 10건 안팎, 하한). 이용 규모 대비 비율은 알 수 없고, 사람의 승인 단계를 우회하거나 지시를 무시한 사례가 있다. 업무형 Agent 확산의 위험 요인 중 하나이며, 비용·불분명한 가치·위험 통제 같은 다른 요인과의 순위는 확인되지 않았다.",
    basis=["I2-M-008", "I2-E-005", "I2-M-010"])
revise("I2-I-006", "누락정정", "서울시가 11월 상암에서 레벨4 로보택시를 도입할 계획이 있어 '강남 심야'만 적은 서술을 보완한다. 무인(운전석)과 유상 여부를 구분해야 한다.",
    statement="한국의 물리 AI 상용화는 발표·제한 운행 단계다. 자율주행 택시는 강남 심야로 구역과 시간을 묶어 시작했고, 서울시는 11월 상암에서 안전관리자 조수석 탑승으로 레벨4 로보택시를 앱 호출로 도입할 계획이다(요금 미확인). 휴머노이드는 2028년 현장 투입 계획이다.",
    basis=["I2-E-001", "I2-E-002", "I2-E-007"], check_flags=["카카오모빌리티 4월 유료 전환 여부와 안전요원 탑승 여부 미확인", "상암 도입은 계획 단계 — 확인 필요"])

# --- 전망 ---
revise("I2-F-002", "판정 기준 보완", "'시간 단위 업무 Agent'가 ChatGPT Work 한정인지 Codex 등을 포함하는지 방법에 없었다. 2026-07-09 Codex 이용자 공개가 기록 시점에 이미 있어 부분 충족으로 읽힐 수 있었다(제안 기준).",
    statement="OpenAI 또는 Anthropic은 2027년 6월 말까지 ChatGPT Work 또는 Claude의 시간 단위 업무 Agent 제품의 이용자 수나 작업 수를 제품명을 밝혀 공개할 것이다.",
    method="OpenAI·Anthropic 공식 발표에서 ChatGPT Work 또는 Claude 업무 Agent의 이용자 수·작업 수를 제품명으로 명시 공개했는지 확인. Codex 이용자 수(2026-07-09 공개)는 Coding Agent 계열로 보고 이 전망의 충족으로 세지 않는다",
    basis=["I2-E-004"], check_flags=["판정 대상을 제품명으로 좁힌 제안 기준", "ChatGPT Work·Codex가 같은 앱·사용량 구조라 경계가 모호할 수 있음"])
revise("I2-F-003", "전망 점검", "7월 22일 Tesla 2분기 업데이트가 6개 도시 무감독 운행을 밝힌 것으로 보도돼 기록 시점에 이미 충족됐을 수 있다. '무감독'과 '유료' 공개가 같은 지표인지 불분명하다.",
    method="Tesla 공식 발표·실적 발표에서 도시별로 안전요원 없는(무감독) 유료 승객 운행을 확인. 2026년 7월 22일 2분기 업데이트의 6개 도시 보도가 이미 있어 기록 시점에 충족됐을 가능성이 있으며 Tesla 원문으로 재확인한다",
    basis=["I2-E-006"], check_flags=["기록 시점에 이미 달성됐을 가능성 — Tesla 원문 미열람, 보도 3건 일치 (확인 필요)", "무감독 38만 마일과 유료 240만 마일은 별개 지표, 샌프란시스코 베이는 안전요원 탑승"])
revise("I2-F-005", "판정 기준 보완", "서울 상암 11월 도입은 조수석 안전관리자 탑승이어서 '운전석 무인'과 '차량 내 무인', '유상'과 '실증'을 구분해야 판정이 갈리지 않는다(제안 기준).",
    statement="서울 자율주행 택시는 2027년 6월 말까지 운전석에 사람이 없는 유상 운행을 시작할 것이다(조수석 안전관리자 탑승은 허용).",
    method="서울시·국토교통부·운영사 발표로 확인. '운전석 무인'은 조수석 안전관리자 탑승을 허용하고 '차량 내 무인'과 구분해 표기한다. '유상'은 요금 부과 공지, '운행'은 일반 이용자가 앱으로 호출할 수 있는 경우로 보며 실증은 제외한다",
    basis=["I2-E-002", "I2-E-007"], check_flags=["조수석 안전관리자 허용은 제안 기준", "카카오모빌리티 강남 심야의 유료 전환·안전요원 탑승 여부 미확인(확인 필요)"])
revise("I2-F-006", "판정 기준 보완", "'손상'·'기업 고객'·'공식 사후 보고' 정의가 없었다. 프롬프트 인젝션 유출(패치 공지)은 손상이 아니고 PocketOS 사건은 방법의 대상 5개사가 아닌 Railway가 대응했다(제안 기준).",
    method="OpenAI·Anthropic·Google·Microsoft·Amazon이 AI 에이전트가 고객 데이터를 삭제·변조한 사실을 사후 보고서 형태로 인정했는지 확인. 보안 취약점 패치 공지(데이터 유출)와 제3자 인프라·에이전트 제작사의 보고는 제외한다",
    check_flags=["손상=삭제·변조로 좁힌 제안 기준", "Amazon의 Kiro 건 반박('잘못 설정된 권한')이 공식 확인인지 모호"])
revise("I2-F-101", "전망 점검", "낙관 판정 방법의 (2)는 Waymo·Baidu·Tesla가 기록 시점에 이미 충족 쪽이고 이정표 'Tesla 무인 유료 2개 도시'도 이미 보도돼, (1)·(2)만으로 적중이 가능해 비관과의 변별력이 약했다. 방법을 고쳤다(제안 기준).",
    milestones=[
        {"by": "2026-12", "text": "Waymo 주 100만 회 공개 (Tesla 무인 유료 2개 도시는 2026-07 보도로 이미 달성, 원문 확인 필요)"},
        {"by": "2027-06", "text": "ChatGPT Work·Claude 업무 Agent 이용량 제품명 공개, 휴머노이드 단일 고객 100대 배치"},
        {"by": "2027-06", "text": "서울 무인 유상 자율주행 택시"}],
    method="세 가지 중 두 가지 이상 충족 시 적중: (1) ChatGPT Work 또는 Claude 업무 Agent의 이용량·성과를 제품명으로 공식 공개(F-002 기준, Codex 제외) (2) 로보택시 2개 이상 사업자의 무인 유료 운행과 Waymo 주 100만 회 공개를 함께 충족(Waymo·Baidu·Tesla는 기록 시점에 이미 보도·공개돼 Waymo 100만 회가 사실상 관건) (3) 휴머노이드 단일 고객 100대 이상 상용 배치",
    basis=["I2-E-004", "I2-M-004", "I2-M-005", "I2-E-006", "I2-M-011"],
    check_flags=["Tesla 무인 유료 운행은 원문 미열람 보도 기준 — 확인 필요", "(2)에서 Waymo 100만 회를 필수로 둔 것은 제안 기준", "낙관 전제(규제 강화 없음): Waymo 고속도로 중단·리콜 보도가 있으나 규제 강화 여부 미확인"])
revise("I2-F-102", "전망 점검", "'Waymo 세 곳' 표현은 Baidu·Tesla 무인 유료 운행이 이미 있어 맞지 않는다. 영역 기준으로 다시 썼고, 업무형 Agent 이정표 대상을 F-002 기준에 맞췄다. 낙관 (1)·(2)가 이미 충족 쪽이라 비관 적중 가능성은 낮아 보인다(확신 중간).",
    statement="2027년 말에도 대규모 운영은 Assistant·Coding Agent·로보택시 세 영역에 머문다. 업무형 Agent는 사고와 성과 측정 문제로 시범 운영에 묶이고, 휴머노이드는 파일럿을 반복한다.",
    milestones=[
        {"by": "2027-06", "text": "ChatGPT Work·Claude 업무 Agent 이용량 비공개 지속"},
        {"by": "2027-06", "text": "에이전트의 운영 데이터 손상 사고 공식 확인"},
        {"by": "2027-12", "text": "휴머노이드 단일 고객 배치 수십 대 이하"}],
    basis=["I2-M-007", "I2-M-008", "I2-M-006", "I2-M-010"],
    check_flags=["낙관 판정 (1)·(2)가 기록 시점에 이미 충족 쪽 — 비관 적중 가능성 낮음(확신 중간)"])

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

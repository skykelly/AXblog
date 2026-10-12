"""I4 R1 4유형 기록 생성 + 규칙 검증.
출력: i4/records.jsonl
"""
import json, sys
from pathlib import Path
from collections import Counter

R = "R1"
SRC = {
 "census": {"url": "https://www.census.gov/library/stories/2026/05/ai-use-businesses.html", "publisher": "미국 인구조사국 (BTOS)", "date": "2026-05-26", "grade": "A"},
 "mck": {"url": "https://www.mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai", "publisher": "McKinsey State of AI 2026", "date": "2026-08-25", "grade": "A"},
 "dc_delay": {"url": "https://tech-insider.org/us-ai-data-center-delays-cancellations-7gw-capacity-crisis-2026/", "publisher": "Tech Insider (Bloomberg·Sightline Climate 인용)", "date": "2026-04-17", "grade": "B"},
 "ms_diff": {"url": "https://news.microsoft.com/source/asia/2026/01/12/global-ai-adoption-in-2025/?lang=ko", "publisher": "Microsoft AI 확산 보고서", "date": "2026-01-12", "grade": "A"},
 "kcci": {"url": "https://eiec.kdi.re.kr/policy/domesticView.do?ac=0000187625", "publisher": "대한상의·산업연구원 (KDI 경제정보센터)", "date": "2024-08-30", "grade": "A"},
 "settle": {"url": "https://writerbeware.blog/2026/07/23/anthropic-settlement-update-final-settlement-approved/", "publisher": "Writer Beware", "date": "2026-07-23", "grade": "B"},
 "kr_plan": {"url": "https://www.fnnews.com/news/202605140910476269", "publisher": "파이낸셜뉴스", "date": "2026-05-14", "grade": "B"},
 "csa_ipi": {"url": "https://labs.cloudsecurityalliance.org/research/csa-research-note-indirect-prompt-injection-in-the-wild-2026/", "publisher": "Cloud Security Alliance (OWASP·Google·Unit 42 인용)", "date": "2026-04-26", "grade": "B"},
 "export_tl": {"url": "https://whatledto.com/events/nvidia-china-export-controls", "publisher": "WhatLedTo 타임라인 (BIS·Reuters·NVIDIA 공시 인용)", "date": "2026-09-03", "grade": "B"},
 "nvda_q2": {"url": "https://www.sec.gov/Archives/edgar/data/0001045810/000104581026000073/q2fy27pr.htm", "publisher": "NVIDIA 실적 발표 (SEC 8-K)", "date": "2026-08-26", "grade": "A"},
 "eo": {"url": "https://www.clarkhill.com/news-events/news/what-does-trumps-ai-executive-order-mean-for-colorados-ai-act/", "publisher": "Clark Hill (로펌 분석)", "date": "2025-12-12", "grade": "B"},
 "colorado": {"url": "https://www.lawfuel.com/colorado-ai-act-2026-sb-26-189/", "publisher": "LawFuel", "date": "2026-06-09", "grade": "B"},
 "kr_law": {"url": "https://www.newsis.com/view/NISX20260121_0003484769", "publisher": "뉴시스", "date": "2026-01-21", "grade": "B"},
 "eu_omni": {"url": "https://www.orrick.com/en/Insights/2026/07/EU-AI-Act-Update-Digital-Omnibus-Finalizes-8-Compliance-Changes", "publisher": "Orrick (로펌 분석)", "date": "2026-07-29", "grade": "B"},
 "doj": {"url": "https://axios.com/2026/09/19/justice-department-openai-new-york-times", "publisher": "Axios", "date": "2026-09-19", "grade": "B"},
}
def src(*keys): return [dict(SRC[k], key=k) for k in keys]

base = dict(question="I4", question_version="v1.0", first_seen=R, last_seen=R, status="유효", replaces=None, check_flags=[])
records = []
def add(**kw):
    r = dict(base); r.update(kw); records.append(r)

# ---------- 지표 (M) ----------
add(id="I4-M-001", type="지표", indicator="I4-T1", importance=3, statement="미국 기업 가운데 AI로 재화·서비스를 만들고 있다는 곳은 2026년 5월 초 19.8%다. 2025년 12월부터 5월까지 17~20% 사이에 머물렀고, 6개월 뒤 사용 예상은 20~23%다.",
    value=19.8, unit="%", as_of="2026-05", region="US", definition="BTOS '최근 2주 AI 사용' 응답 기업 비율", extra={"expected_6m": "20~23%"}, sources=src("census"), verified=True)
add(id="I4-M-002", type="지표", indicator="I4-T2", importance=3, statement="업종별로는 정보 산업이 39.7%로 가장 높고 금융·보험이 33.9%로 뒤를 잇는다. 소매업은 약 14%로 가장 낮다.",
    value=39.7, unit="% (정보 산업)", as_of="2026-05", region="US", definition="BTOS 업종별 현재 AI 사용률", extra={"finance": "33.9%", "retail": "약 14%"}, sources=src("census"), verified=True)
add(id="I4-M-003", type="지표", indicator="I4-T3", importance=2, statement="직원 250명 이상 기업의 AI 사용률은 37%, 100~249명 기업은 32%다. 20명 이상 기업에서는 사용률이 올랐지만 20명 미만 기업은 변화가 없었다.",
    value=37, unit="% (250명 이상)", as_of="2026-05", region="US", definition="BTOS 규모별 AI 사용률", sources=src("census"), verified=True)
add(id="I4-M-004", type="지표", indicator="I4-T4", importance=3, statement="AI를 전사로 확장하고 있다는 기업은 44%로 1년 전 38%에서 늘었다. AI Agent를 확장 중인 곳은 매출 10억 달러 이상 기업 40%, 그보다 작은 기업 22%다. 반면 AI로 EBIT 효과를 봤다는 곳은 37%로 1년 전과 비슷하다.",
    value=44, unit="% (전사 확장)", as_of="2026-06", region="GLOBAL", definition="McKinsey 글로벌 설문(1,719명, 2026년 5~6월)", extra={"agents_large": "40%", "agents_small": "22%", "ebit": "37%", "token_cost_constraint": "약 20%"},
    sources=src("mck"), verified=True)
add(id="I4-M-005", type="지표", indicator="I4-T5", importance=3, statement="2026년 완공 예정이던 미국 데이터센터의 30~50%가 지연되거나 취소됐다는 집계가 나왔다. 발표된 12~16GW 가운데 실제 공사 중인 것은 약 5GW다. 병목은 GPU보다 전력망 연결이다.",
    value=50, unit="% (지연·취소, 상단)", as_of="2026-05", region="US", definition="2026년 완공 예정 데이터센터 용량 중 지연·취소 비율", extra={"under_construction": "약 5GW", "announced": "12~16GW"},
    sources=src("dc_delay"), verified=True, check_flags=["2차 정리 기사 — 원자료(Sightline Climate·Bloomberg) 확인 필요, 수치 범위가 기사 안에서도 다름"])
add(id="I4-M-006", type="지표", indicator="I4-T6", importance=2, statement="Anthropic과 저자들의 15억 달러 저작권 합의가 최종 승인됐다. 청구된 저작물 44만 490건에 건당 약 3,127달러가 지급된다.",
    value=3127, unit="달러 (저작물당)", as_of="2026-07", region="US", definition="AI 학습 저작권 합의의 저작물당 배상액", extra={"total": "15억 달러", "works": "440,490건"}, sources=src("settle"), verified=True)
add(id="I4-M-007", type="지표", indicator="I4-T7", importance=2, statement="2026년 1~4월 OWASP가 꼽은 주요 AI 보안 사고 8건 가운데 CVE가 붙은 것은 1건뿐이다. 웹 페이지에 숨긴 지시로 에이전트를 조종하는 간접 프롬프트 주입은 시연을 넘어 실제 공격 단계에 들어섰다.",
    value=8, unit="건 (2026-01~04 주요 사고)", as_of="2026-04", region="GLOBAL", definition="OWASP GenAI 분기 정리의 주요 AI 보안 사고", extra={"google_ipi_growth": "+32% (2025-11 → 2026-02)"},
    sources=src("csa_ipi"), verified=True)
add(id="I4-M-008", type="지표", indicator="I4-T8", importance=3, statement="한국의 생산가능인구 AI 사용률은 2025년 하반기 30%를 넘어 세계 18위로 7계단 올랐다. 2024년 10월 이후 증가율은 80% 이상으로 세계 평균(35%)의 두 배를 넘는다.",
    value=30, unit="% 이상 (국민 사용률)", as_of="2025-H2", region="KR", definition="생산가능인구 중 생성형 AI 사용 비율", extra={"rank": "18위", "growth": "80% 이상"}, sources=src("ms_diff"), verified=True)
add(id="I4-M-009", type="지표", indicator="I4-T8", importance=2, statement="국내 기업의 AI 활용률은 30.6%다. 대기업 48.8%, 중소기업 28.7%이고, 업종별로는 서비스업 53.0%(금융 57.1%), 제조업 23.8%다.",
    value=30.6, unit="% (기업 활용률)", as_of="2024", region="KR", definition="국내 기업 500개사 AI 기술 활용 비율", extra={"large": "48.8%", "sme": "28.7%", "service": "53.0%", "manufacturing": "23.8%"},
    sources=src("kcci"), verified=True, check_flags=["2024년 조사 — 2025년 이후 공식 기업 도입 통계로 갱신 필요"])
add(id="I4-M-010", type="지표", indicator="I4-T8", importance=2, statement="정부는 GPU 1만 3천 장을 확보해 산·학·연(4천 장), 국가 프로젝트(3천 장), 독자 파운데이션 모델(3천 장)에 배분했다. AI 행동계획 326개 과제 중 288개(88%)가 정상 추진 중이다.",
    value=13000, unit="장 (정부 확보 GPU)", as_of="2026-05", region="KR", definition="정부 확보 GPU 수량", extra={"tasks_on_track": "288/326"}, sources=src("kr_plan"), verified=True)

# ---------- 사건 (E) ----------
add(id="I4-E-001", type="사건", importance=3, statement="미국이 H200의 중국 판매를 승인하고 매출의 25%를 정부가 가져가는 조건을 붙였다.",
    date="2025-12-08", actor="미국 정부", sources=src("export_tl"), verified=True, check_flags=["타임라인 정리 — 원 보도 The Register·BIS"])
add(id="I4-E-002", type="사건", importance=3, statement="트럼프 대통령이 주(州) AI 법을 연방 정책으로 묶는 행정명령에 서명했다. 법무부에 주 법에 소송을 거는 전담 조직을 만들게 하고, 부담이 큰 주에는 연방 보조금을 제한할 수 있게 했다.",
    date="2025-12-11", actor="미국 백악관", sources=src("eo"), verified=True)
add(id="I4-E-003", type="사건", importance=2, statement="미국 상무부가 H200 수출을 개별 심사로 바꿨고, 같은 주 중국 세관은 H200 반입을 막았다. 이후 일부 승인이 나왔지만 8월까지 실제 출하는 소량에 그쳤다.",
    date="2026-01-13", actor="미국 상무부·중국 정부", sources=src("export_tl"), verified=True, check_flags=["타임라인 정리 — 원 보도 BIS·Reuters"])
add(id="I4-E-004", type="사건", importance=3, statement="한국 AI 기본법이 시행됐다. 고영향 AI와 생성형 AI 표시 의무가 생겼고, 과태료는 최소 1년 유예됐다.",
    date="2026-01-22", actor="한국 정부", sources=src("kr_law"), verified=True)
add(id="I4-E-005", type="사건", importance=2, statement="미국 콜로라도주가 2024년 AI법을 대폭 줄인 대체 법에 서명했다. 위험관리·영향평가 의무를 없애고 통지·설명·사람 검토 권리만 남겼으며, 시행은 2027년 1월로 미뤘다.",
    date="2026-05-14", actor="콜로라도주", sources=src("colorado"), verified=True)
add(id="I4-E-006", type="사건", importance=2, statement="국가인공지능전략위원회가 AI 행동계획 이행을 점검하고 GPU 1만 3천 장 확보·배분 현황을 밝혔다.",
    date="2026-05-14", actor="국가인공지능전략위원회", sources=src("kr_plan"), verified=True)
add(id="I4-E-007", type="사건", importance=3, statement="EU가 AI법 개정(디지털 옴니버스)을 확정해 고위험 AI 의무 적용을 2026년 8월에서 2027년 12월로, 제품 결합형 고위험 AI는 2028년 8월로 미뤘다.",
    date="2026-07", actor="EU", sources=src("eu_omni"), verified=True, check_flags=["관보 게재 정확한 날짜는 원문에 없음"])
add(id="I4-E-008", type="사건", importance=2, statement="법원이 Anthropic과 저자들의 15억 달러 저작권 합의를 최종 승인했다.",
    date="2026-07-21", actor="미국 연방법원", sources=src("settle"), verified=True)
add(id="I4-E-009", type="사건", importance=2, statement="NVIDIA가 다음 분기 전망에서 중국 데이터센터 매출을 0으로 잡았다. 중국 수출 허용 물량의 일부만 출하했고 H200 재고 4억 달러를 손실 처리했다.",
    date="2026-08-26", actor="NVIDIA", sources=src("nvda_q2", "export_tl"), verified=True)
add(id="I4-E-010", type="사건", importance=3, statement="미국 법무부가 뉴욕타임스 대 OpenAI 소송에서 'AI 학습은 새롭고 변형적이어서 공정 이용'이라는 의견서를 냈다. 출력물까지 같은 논리가 적용되지는 않는다고 선을 그었다.",
    date="2026-09-19", actor="미국 법무부", sources=src("doj"), verified=True)

# ---------- 해석 (I) ----------
add(id="I4-I-001", type="해석", importance=3, target="확산의 넓이와 깊이", direction="중립",
    statement="AI 확산은 넓이가 아니라 깊이로 진행되고 있다. 미국 기업 전체 사용률은 반년째 20% 안팎에서 멈췄지만, 대기업은 전사 확장과 Agent 확장을 빠르게 늘리고 있다.",
    basis=["I4-M-001", "I4-M-003", "I4-M-004"])
add(id="I4-I-002", type="해석", importance=3, target="산업·업무", direction="강화",
    statement="실제 운영 단계에 들어선 곳은 정보·금융 산업과 IT·소프트웨어 개발 업무다. 소매와 제조는 아직 초기 확산 단계이며, 제조는 공급망·재고 업무에서 Agent를 시험하는 수준이다.",
    basis=["I4-M-002", "I4-M-004", "I4-M-009"])
add(id="I4-I-003", type="해석", importance=3, target="규제", direction="강화",
    statement="규제의 브레이크는 풀리는 쪽이다. EU는 고위험 의무를 1년 4개월 미뤘고, 미국은 연방이 주 법을 압박해 콜로라도가 법을 크게 줄였으며, 법무부는 학습 단계의 공정 이용을 지지했다.",
    basis=["I4-E-007", "I4-E-002", "I4-E-005", "I4-E-010"])
add(id="I4-I-004", type="해석", importance=2, target="저작권", direction="중립",
    statement="저작권은 '막는 요인'에서 '비용'으로 바뀌고 있다. 해적판 학습에는 저작물당 약 3,100달러라는 가격이 매겨졌고, 정상 취득한 데이터의 학습은 공정 이용 쪽으로 기울고 있다.",
    basis=["I4-M-006", "I4-E-008", "I4-E-010"])
add(id="I4-I-005", type="해석", importance=3, target="전력·인프라", direction="약화",
    statement="지금 확산을 가장 크게 막는 것은 규제가 아니라 전력이다. 올해 완공 예정 데이터센터의 30~50%가 늦어지고 있어, 돈이 있어도 연산 능력이 제때 들어서지 못한다.",
    basis=["I4-M-005"])
add(id="I4-I-006", type="해석", importance=2, target="Agent 보안", direction="약화",
    statement="Agent 보안은 운영 확대의 새 제약이다. 간접 프롬프트 주입이 실제 공격으로 쓰이고 있지만 대부분 CVE 없이 처리돼, 기업이 위험을 추적하기 어렵다.",
    basis=["I4-M-007"])
add(id="I4-I-007", type="해석", importance=2, target="수출 통제", direction="중립",
    statement="미국과 중국의 AI 시장은 분리가 굳어지고 있다. 미국이 수수료를 받고 H200 판매를 허용했지만 중국이 수입을 억제해, NVIDIA는 중국 매출을 전망에서 뺐다.",
    basis=["I4-E-001", "I4-E-003", "I4-E-009"])
add(id="I4-I-008", type="해석", importance=2, target="한국", direction="강화",
    statement="한국은 개인 사용은 빠르게 늘고(국민 30% 이상, 증가율 세계 평균의 두 배), 법과 GPU 같은 제도·인프라도 갖춰지고 있다. 다만 기업 도입 통계는 2024년(30.6%) 이후 공식 갱신이 없어, 기업 운영 단계는 판정하기 어렵다.",
    basis=["I4-M-008", "I4-M-009", "I4-M-010", "I4-E-004"])

# ---------- 세부 전망 (F) ----------
add(id="I4-F-001", type="전망", importance=2, status="유효", forecast_status="진행 중",
    statement="NVIDIA는 다음 분기(2026년 11월~2027년 1월) 전망에서도 중국 데이터센터 매출을 0으로 잡을 것이다.", due="2026-11-30", condition="없음",
    method="NVIDIA 3분기(FY2027) 실적 발표의 전망 문구 확인", basis=["I4-E-009"], result=None)
add(id="I4-F-002", type="전망", importance=3, status="유효", forecast_status="진행 중",
    statement="미국 기업 AI 사용률(BTOS)은 2026년 12월 말 기준 21% 이상일 것이다.", due="2027-01-31", condition="BTOS 조사가 계속 발표될 경우",
    method="미국 인구조사국 BTOS 최신 격주 자료 확인", basis=["I4-M-001", "I4-M-003"], result=None)
add(id="I4-F-003", type="전망", importance=2, status="유효", forecast_status="진행 중",
    statement="2027년 6월 말까지 뉴욕타임스 대 OpenAI 소송에서 학습 단계의 공정 이용 여부에 대한 법원 판단(약식판결 포함)이 나올 것이다.", due="2027-06-30", condition="합의로 종결되지 않을 경우",
    method="법원 기록 또는 주요 언론 보도 확인", basis=["I4-E-010"], result=None)
add(id="I4-F-004", type="전망", importance=3, status="유효", forecast_status="진행 중",
    statement="2027년 상반기에도 미국 데이터센터 계획 용량의 30% 이상이 지연·취소됐다는 집계가 나올 것이다.", due="2027-06-30", condition="없음",
    method="Sightline Climate·Bloomberg 등 집계 확인", basis=["I4-M-005"], result=None)
add(id="I4-F-005", type="전망", importance=2, status="유효", forecast_status="진행 중",
    statement="EU는 2027년 6월 말까지 고위험 AI 의무(2027년 12월 적용)를 다시 미루자는 공식 제안을 내지 않을 것이다.", due="2027-06-30", condition="없음",
    method="EU 집행위원회 발표 확인", basis=["I4-E-007"], result=None)
add(id="I4-F-006", type="전망", importance=3, status="유효", forecast_status="진행 중",
    statement="McKinsey 2027년 조사에서 AI를 전사로 확장 중이라는 기업 비율은 50% 이상일 것이다.", due="2027-09-30", condition="같은 문항이 유지될 경우",
    method="McKinsey State of AI 2027 확인", basis=["I4-M-004"], result=None)

# ---------- 메인 질문 시나리오 ----------
add(id="I4-F-101", type="전망", importance=3, status="유효", forecast_status="진행 중", scenario="낙관",
    statement="2027년 말까지 AI가 정보·금융을 넘어 소매·제조의 핵심 업무로 들어간다. 미국 기업 사용률이 25%를 넘고, 대기업 과반이 AI를 전사로 확장한다. 규제는 연기·완화 기조가 유지되고, 전력 병목은 신규 발전·연결로 풀리기 시작한다.",
    milestones=[
        {"by": "2027-01", "text": "미국 기업 AI 사용률 21% 이상"},
        {"by": "2027-06", "text": "데이터센터 지연 비율 30% 미만으로 하락"},
        {"by": "2027-09", "text": "McKinsey 전사 확장 50% 이상"}],
    due="2027-12-31", condition="대형 AI 사고나 경기 침체로 기업 투자가 멈추지 않을 경우",
    method="세 가지 중 두 가지 이상 충족 시 적중: (1) 미국 BTOS 현재 AI 사용률 25% 이상 (2) McKinsey 전사 확장 비율 50% 이상 (3) 미국 데이터센터 지연·취소 비율 집계 30% 미만",
    basis=["I4-M-001", "I4-M-004", "I4-M-005"],
    signposts=[{"id": "I4-F-002", "on_hit": "낙관", "on_miss": "비관"}, {"id": "I4-F-004", "on_hit": "비관", "on_miss": "낙관"},
               {"id": "I4-F-006", "on_hit": "낙관", "on_miss": "비관"}, {"id": "I4-F-005", "on_miss": "낙관"}], result=None)
add(id="I4-F-102", type="전망", importance=3, status="유효", forecast_status="진행 중", scenario="비관",
    statement="2027년 말까지 확산은 대기업·정보 산업 안에 머문다. 미국 기업 사용률은 20% 근처에서 정체하고, 전력 부족과 Agent 보안 사고가 운영 확대를 늦춘다. 규제 완화로 생긴 공백을 소송과 사고가 메운다.",
    milestones=[
        {"by": "2027-01", "text": "미국 기업 AI 사용률 21% 미만"},
        {"by": "2027-06", "text": "데이터센터 지연 30% 이상 지속"},
        {"by": "2027-09", "text": "McKinsey 전사 확장 50% 미만, EBIT 효과 정체"}],
    due="2027-12-31", condition="없음",
    method="낙관 시나리오의 판정 조건 세 가지 중 하나 이하만 충족 시 적중",
    basis=["I4-M-001", "I4-M-005", "I4-M-007"], signposts=[], result=None)

# ---------- 정정·추가 (2026-10-11 검증 반영, probe_20261011/report_i4.md) ----------
# 원본 기록은 ID를 유지한 채 고치고, 고치기 전 진술과 이유를 revisions에 남긴다. 새 기록은 added_on으로 구분한다.
CHG = "2026-10-11"
SRC.update({
 "minneapolisfed": {"url": "https://www.minneapolisfed.org/article/2026/ai-adoption-in-business-grows-steadily-but-unevenly", "publisher": "미니애폴리스 연준 (BTOS 4월 보충조사 해설)", "date": "2026-05-29", "grade": "B"},
 "eenews": {"url": "https://www.eenews.net/articles/data-center-construction-delays-grow-report/", "publisher": "E&E News (Sightline Climate 보고 인용)", "date": "2026-02-24", "grade": "B"},
 "latitude": {"url": "https://www.latitudemedia.com/news/up-to-half-of-the-worlds-data-centers-may-be-delayed-this-year/", "publisher": "Latitude Media (Sightline Climate 인용)", "date": "2026-02-24", "grade": "B"},
 "pearlcohen": {"url": "https://pearlcohen.com/federal-court-approves-1-5-billion-anthropic-copyright-settlement-largest-in-history", "publisher": "Pearl Cohen", "date": "2026-07", "grade": "B"},
 "eweek": {"url": "https://www.eweek.com/de/news/anthropic-15-billion-ai-copyright-settlement-approved/", "publisher": "eWeek", "date": "2026-07", "grade": "B"},
 "lewissilkin": {"url": "https://www.lewissilkin.com/insights/2026/07/27/the-digital-omnibus-on-ai-enters-into-force-today-102nedo", "publisher": "Lewis Silkin (EU 디지털 옴니버스 발효)", "date": "2026-07-27", "grade": "B"},
 "sidley": {"url": "https://datamatters.sidley.com/2026/06/22/eu-lawmakers-reach-provisional-agreement-to-delay-key-eu-ai-act-obligations/", "publisher": "Sidley (EU 옴니버스 잠정합의·의회 표결)", "date": "2026-06-22", "grade": "B"},
 "kbmaeil": {"url": "https://kbmaeil.com/article/20260719500014", "publisher": "경북매일 (AI 기본법 개정안·시행령 7/21 적용)", "date": "2026-07-20", "grade": "B"},
 "twig24": {"url": "https://www.twig24.com/news/2026/01/23/20260123030002", "publisher": "트윅24 (AI 기본법 시행·계도기간)", "date": "2026-01-23", "grade": "B"},
 "ms_q1": {"url": "https://www.microsoft.com/en-us/research/wp-content/uploads/2026/05/Microsoft-AI-Diffusion-Report-2026-Q1.pdf", "publisher": "Microsoft AI Diffusion Report 2026 Q1 (PDF)", "date": "2026-05", "grade": "A"},
 "khan": {"url": "https://www.khan.co.kr/en/article/202609281402017", "publisher": "경향신문 영문판 (Microsoft Q2 보고서 보도)", "date": "2026-09-28", "grade": "B"},
 "digitaltoday": {"url": "https://www.digitaltoday.co.kr/en/view/108144/south-korea-ranks-12th-in-generative-ai-usage-fastest-growth-among-major-economies", "publisher": "Digital Today (Microsoft Q2 보고서 보도)", "date": "2026-09-28", "grade": "B"},
 "etoday_corp": {"url": "https://www.etoday.co.kr/news/view/2435207", "publisher": "이투데이 (과기정통부 2024 기업정보화통계집)", "date": "2025-01-06", "grade": "B"},
 "mt_gpu": {"url": "https://www.mt.co.kr/tech/2025/10/31/2025103112075597559", "publisher": "머니투데이 (엔비디아 GPU 26만 장)", "date": "2025-10-31", "grade": "B"},
 "axios_0908": {"url": "https://axios.com/2026/09/08/nyt-openai-microsoft-copyright-lawsuit", "publisher": "Axios (NYT v. OpenAI 약식판결 국면)", "date": "2026-09-08", "grade": "B"},
 "lawnext": {"url": "https://www.lawnext.com/2026/09/3rd-circuit-rules-for-thomson-reuters-in-its-copyright-fight-against-legal-research-startup-ross.html", "publisher": "LawNext (제3순회 Thomson Reuters v. ROSS)", "date": "2026-09-30", "grade": "B"},
 "owasp_q3": {"url": "https://genai.owasp.org/2026/10/08/genai-and-agentic-ai-exploit-roundup-q3-2026/", "publisher": "OWASP GenAI Exploit Roundup Q3 2026", "date": "2026-10-08", "grade": "B"},
 "csa_brief": {"url": "https://labs.cloudsecurityalliance.org/research/ciso-daily-briefing-20260904/", "publisher": "CSA CISO 일일 브리핑", "date": "2026-09-04", "grade": "B"},
})
def _get(i): return next(r for r in records if r["id"] == i)
def revise(i, kind, why, **ch):
    r = _get(i)
    r.setdefault("revisions", []).append({"on": CHG, "kind": kind, "before": r.get("statement") if "statement" in ch else None, "why": why})
    r.update(ch)
def _more(i, *keys): return _get(i)["sources"] + src(*keys)

# --- 지표 ---
revise("I4-M-001", "누락정정", "BTOS 질문이 2025-11-17에 '재화·서비스 생산에 AI 사용'에서 '어떤 업무 기능에서든 AI 사용'으로 넓어졌는데 문장은 옛 정의로 적혀 있었다. 값(19.8%)은 넓어진 정의 기준이다.",
    statement="미국 기업 가운데 최근 2주 안에 어떤 업무 기능에서든 AI를 쓴 곳은 2026년 5월 초 19.8%다. BTOS 질문은 2025년 11월 17일에 '재화·서비스를 만드는 데 AI를 썼는가'에서 '어떤 업무 기능에서든 썼는가'로 넓어졌고, 이 값은 넓어진 정의 기준이다. 2025년 12월부터 5월까지 17~20% 구간이고, 같은 문항의 2025년 말 값(약 10%)은 재화·서비스 생산 기준이라 직접 비교할 수 없다. 6개월 뒤 사용 예상은 20~23%다.",
    definition="BTOS 최근 2주 안에 어떤 업무 기능에서든 AI를 쓴 기업 비율(2025-11-17 이후 정의)",
    extra={"expected_6m": "20~23%", "definition_changed": "2025-11-17", "old_definition_2025_end": "약 10% (재화·서비스 생산 기준, 직접 비교 불가)"},
    check_flags=["'주로 AI로 한다'는 엄격한 기준보다 느슨한 정의라, 엄격 기준을 적용하면 업종 단계가 한 단계 내려갈 수 있음 — 좁은 정의 값 확인 필요", "2026-05-03 이후 값은 확인하지 못함 — 확인 필요"],
    sources=_more("I4-M-001", "minneapolisfed"))
revise("I4-M-002", "단정반증", "'소매업이 가장 낮다'는 Census가 제시한 업종 안에서만 맞다(4월 보충조사에는 10% 미만 업종이 있다). 업종 이름도 BTOS '정보' 업종으로 한정해야 하고, 값은 넓어진 정의 기준이다.",
    statement="BTOS 업종별로는 정보 업종이 39.7%로 가장 높고 금융·보험이 33.9%로 뒤를 잇는다(2025년 11월 넓어진 정의 기준). 소매업은 약 14%로 Census가 제시한 업종 중 가장 낮다. 4월 보충조사에서는 농업·운송·숙박음식·건설이 10% 미만, 제조가 약 12%여서 소매보다 낮은 업종이 있고, 정보·전문서비스는 약 40%로 묶여 업종 구분이 다르다. '주로 AI로 한다'는 엄격한 기준을 적용하면 정보·금융은 한 단계 내려갈 수 있다.",
    extra={"finance": "33.9%", "retail": "약 14%", "supplement_survey_2026_04": "농업·운송·숙박음식·건설 10% 미만, 제조 약 12%, 정보·전문서비스 약 40% (본조사와 업종 구분이 다름)"},
    check_flags=["좁은 정의(주로 AI로 한다)의 업종별 값은 확인하지 못함 — 단계 판정은 유지하되 확인 필요", "4월 보충조사는 본조사와 업종 구분이 달라 같은 선에 놓을 수 없음", "'정보' 업종의 세부 구성(출판·방송·통신·데이터 처리 등)은 원문으로 확인하지 못함"],
    sources=_more("I4-M-002", "minneapolisfed"))
revise("I4-M-003", "누락정정", "소기업 값이 없었고, 본조사(37% 대 20% 미만)와 4월 보충조사(30% 대 17%)의 격차가 서로 달라 조사를 밝혀야 한다.",
    statement="직원 250명 이상 기업의 AI 사용률은 37%, 100~249명 기업은 32%이고 4명 이하 기업은 20% 미만이다. 20명 이상 기업에서는 사용률이 올랐지만 20명 미만 기업은 변화가 없었다. 4월 보충조사에서는 250명 이상 30%, 20명 미만 17%로 본조사와 수준·격차가 달라, 격차는 조사별로 따로 본다.",
    check_flags=["본조사와 보충조사는 문항·시점이 달라 격차를 단순 비교할 수 없음", "20명 미만 전체의 본조사 값은 확인하지 못함(4명 이하만 '20% 미만')"],
    sources=_more("I4-M-003", "minneapolisfed"))
revise("I4-M-004", "누락정정", "기록에 없던 대기업·소기업 격차와 코딩 Agent 값이 McKinsey 2026 본문에 있다.",
    statement="AI를 전사로 확장하고 있다는 기업은 44%로 1년 전 38%에서 늘었다. 매출 10억 달러 초과 대기업은 54%, 소기업은 약 3분의 1이다. AI Agent를 확장 중인 곳은 대기업 40%(1년 전 27%), 그보다 작은 기업 22%(보합)다. 코딩 Agent를 확장 중인 곳은 전체 약 2할, 대기업 31%다. 3개 이상 기능에서 AI를 쓰는 곳은 56%(전년 51%)이고, AI로 EBIT 효과를 봤다는 곳은 37%로 1년 전과 비슷하며 고성과자(EBIT 5% 이상)는 약 6%다.",
    extra={"agents_large": "40% (전년 27%)", "agents_small": "22% (보합)", "ebit": "37%", "enterprise_scale_large": "54%", "enterprise_scale_small": "약 3분의 1", "coding_agents_scale": "전체 약 2할, 대기업 31%", "three_plus_functions": "56% (전년 51%)", "high_performers": "약 6%", "token_cost_constraint": "약 20% (본문에서 확인하지 못함)"},
    check_flags=["extra의 token_cost_constraint 약 20%는 열람한 본문에서 확인하지 못함 — 확인 필요", "McKinsey 자체 응답자 설문(1,719명, 2026-05-04~06-08)이며 표본·가중 방식은 확인하지 못함", "대기업 전사 확장(54%)의 1년 전 값은 확인하지 못함"])
revise("I4-M-005", "단정반증", "'30~50%가 지연되거나 취소됐다'는 과거형이 틀렸다. 근거는 Sightline Climate의 2026-02-24 전망(밀릴 수 있다는 예측)이고 실현치는 2025년 26%다. 단독 근거였던 Tech Insider는 수치·날짜가 서로 맞지 않는 2차 정리라 근거에서 뺐다. '병목은 전력망 연결' 단일 원인도 쓸 수 없다.",
    statement="Sightline Climate가 2026년 2월 24일 내놓은 전망에 따르면, 2026년 완공 예정이던 미국 데이터센터 140개(16GW) 프로젝트의 30~50%가 2027년 이후로 밀릴 수 있다(전망치). 실현치는 2025년 110개 중 26% 지연, 취소 확인 9건이다. 지연 요인으로 전력 제약·지역 반대·변압기 등 전력망 장비 부족이 함께 꼽혔고, 10개 이상 주에서 모라토리엄이 제안됐다.",
    value=50, unit="% (2027년 이후로 밀릴 수 있는 비율, 전망 상단)", as_of="2026-02", definition="Sightline Climate 전망: 2026년 완공 예정 용량 중 2027년 이후로 밀릴 수 있는 비율(전망치, 실현치 아님)",
    extra={"projects_2026": "140개(16GW)", "realized_2025": "110개 중 26% 지연, 취소 확인 9건", "range": "30~50% (매체마다 30%·약 3분의 1·30~50%로 표기)"},
    check_flags=["전망치이며 실현치가 아님 — 2025년 실현 지연은 26%", "Sightline 원문과 Bloomberg 원자료는 열람하지 못함 — 확인 필요", "인용 매체마다 30%·약 3분의 1·30~50%로 표기가 갈림"],
    sources=src("eenews", "latitude"))
revise("I4-M-006", "상충", "3,127달러는 변호사비·비용을 뺀 순액을 청구된 저작물 수로 나눈 값이라 기준을 밝혀야 한다. 보도의 '약 3,000달러'는 반올림이다.",
    statement="Anthropic과 저자들의 15억 달러 저작권 합의가 최종 승인됐다. 변호사비·비용 등 약 1억 2,246만 달러를 뺀 순액 13억 7,754만 달러를 청구된 저작물 44만 490건으로 나누면 건당 약 3,127달러다. 총액 15억 달러를 대상 목록 482,460건으로 나누면 약 3,109달러이고, 보도의 '약 3,000달러'는 반올림이다. 합의이므로 공정 이용 판단은 없다.",
    extra={"total": "15억 달러", "works": "440,490건(청구)", "works_listed": "482,460건(대상 목록)", "net_of_fees": "13억 7,754만 달러", "per_work_total_basis": "약 3,109달러"},
    sources=_more("I4-M-006", "pearlcohen"))
revise("I4-M-007", "갱신", "OWASP 3분기 정리(2026-10-08)가 나와 '1~4월 8건' 서술이 1분기 이야기가 됐다. 3분기는 평가 환경의 Agent 경계 이탈과 공급망 사고가 중심이다. 'Google +32%'는 절대 건수가 아닌 상대 변화다.",
    statement="OWASP GenAI 3분기 정리(2026년 10월 8일 발표, 7~9월)는 확인 사건 7건·연구 시연 1건·시도 1건이며, 평가 환경의 샌드박스 탈출 5건, 공급망 3건, 프롬프트 주입 1건이 중심이다. 1분기(1~4월)에는 주요 사고 8건 가운데 CVE가 붙은 것이 1건뿐이었고 간접 프롬프트 주입이 실제 공격 단계에 들어섰다. OWASP 공식 발행물이 아니고 전수 집계도 아니며, 7건이 독립 공격 7건도 아니다.",
    value=7, unit="건 (2026년 3분기 확인 사건)", as_of="2026-Q3", prev_value=8,
    extra={"q1_major_incidents": "8건(CVE 1건)", "q3_confirmed": "7건·연구 시연 1건·시도 1건", "q3_types": "샌드박스 탈출 5·공급망 3·프롬프트 주입 1", "google_ipi_growth": "+32% (2025-11 → 2026-02, 악성 IPI 콘텐츠 비율의 상대 변화이며 절대 건수가 아님)"},
    check_flags=["OWASP 3분기 정리는 공식 발행물이 아니며 전수가 아님(OpenAI 캠페인 3건은 한 묶음)", "Hugging Face 침투 규모가 CSA는 '1,200 Agent 중 약 700개', OWASP는 '41개 프로덕션 워커'로 달라 단일 숫자로 쓰지 않음", "전 분기 대비 추세는 정리에 없음", "Google +32%의 원 출처는 열지 못함"],
    sources=_more("I4-M-007", "owasp_q3", "csa_brief"))
revise("I4-M-008", "갱신", "2026년 1·2분기 값이 나와 '2025년 하반기 30%대·18위'는 두 분기 전 값이 됐다. 2분기 값은 Microsoft 원문이 아니라 보도 기준이다.",
    statement="한국의 생성형 AI 사용률(15~64세)은 2026년 2분기 40.6%로 세계 12위이고 직전 분기보다 3.5%p 올랐다(세계 18.8%). 1분기는 37.1%(16위, +6.4%p, 세계 17.8%, 미국 31.3%·21위)였고, 2025년 하반기는 30%대(18위)였다. '1회 이상 사용'을 텔레메트리로 추정한 값이다.",
    value=40.6, unit="% (국민 사용률)", as_of="2026-Q2", prev_value=37.1,
    extra={"rank": "12위(2026-Q2)", "q1": "37.1% (16위)", "world_avg_q2": "18.8%"},
    check_flags=["2분기 값(40.6%·12위)은 경향신문·Digital Today 보도 기준이며 Microsoft 2분기 원문은 열지 못함 — 확인 필요", "방법론은 '1회 이상 사용'을 텔레메트리로 추정한 값"],
    sources=_more("I4-M-008", "ms_q1", "khan", "digitaltoday"))
revise("I4-M-009", "상충", "'공식 갱신이 없다'고 했지만 과기정통부 2024 기업정보화통계집(213,266개 기업, 30.3%)이 표본이 훨씬 커 1순위 값이다. 대한상의 500개사 조사는 업종별 값으로 병기한다.",
    statement="국내 기업의 AI 활용률은 과기정통부 2024 기업정보화통계집(2025년 1월 발표, 213,266개 기업 대상)에서 30.3%(전년 +2.3%p)다. 대한상의·산업연구원 500개사 조사(2024)는 30.6%이고, 대기업 48.8%, 중소기업 28.7%, 서비스업 53.0%(금융 57.1%), 제조업 23.8%다.",
    value=30.3, definition="과기정통부 기업정보화통계집 기업 AI 활용률(213,266개 기업). 업종별 값은 대한상의 500개사 조사", extra={"kcci_total": "30.6%", "large": "48.8%", "sme": "28.7%", "service": "53.0%", "manufacturing": "23.8%"},
    check_flags=["2024년 조사 — 2025년 이후 공식 기업 도입 통계로 갱신 필요(2025년 판은 찾지 못함)", "과기정통부 통계집 원문은 열지 못하고 이투데이 보도 본문으로 확인 — 확인 필요", "2026-09 AWS 의뢰 설문(58%)은 정의가 달라 같은 선에 놓지 않음, 이해관계가 있어 단독 근거로 쓰지 않음"],
    sources=_more("I4-M-009", "etoday_corp"))
revise("I4-M-010", "누락정정", "배분 합계가 1만 장이고 나머지 3천 장의 용처는 기사에 없다. 2025-10 엔비디아 26만 장 공급 발표와의 관계도 구분되지 않는다.",
    statement="정부는 GPU 1만 3천 장을 확보했다고 밝혔고, 산·학·연(4천 장), 국가 프로젝트(3천 장), 독자 파운데이션 모델(3천 장)에 합계 1만 장을 배분했다. 나머지 3천 장의 용처는 기사에 없다. AI 행동계획 326개 과제 중 288개(88%)가 정상 추진 중이다. 2025년 10월 31일 엔비디아 GPU 26만 장 공급 계획 발표(공공 5만, 삼성·SK 등 20만)와의 관계는 확인 필요하다.",
    check_flags=["나머지 3천 장의 용처가 기사에 없음 — 확인 필요", "26만 장은 공급 계획 발표이며 확보 완료가 아님. 머니투데이 본문은 열지 못하고 검색 요약으로만 확인 — 확인 필요"],
    sources=_more("I4-M-010", "mt_gpu"))

# --- 사건 ---
revise("I4-E-001", "갱신", "이번 재조사에서 원문과 타임라인을 열지 못해 검증하지 못했다. 타임라인 정리(2차)에만 의존한다.",
    check_flags=["타임라인 정리 — 원 보도 The Register·BIS", "원문·타임라인을 이번 재조사에서 열지 못함 — 확인 필요"])
revise("I4-E-003", "갱신", "이번 재조사에서 원문과 타임라인을 열지 못해 검증하지 못했다. 타임라인 정리(2차)에만 의존한다.",
    check_flags=["타임라인 정리 — 원 보도 BIS·Reuters", "원문·타임라인을 이번 재조사에서 열지 못함 — 확인 필요"])
revise("I4-E-004", "갱신", "2026-07-21 개정안·시행령 개정안 적용이 빠져 있었다. 한 매체 기준이다.",
    statement="한국 AI 기본법이 시행됐다. 고영향 AI와 생성형 AI 표시 의무가 생겼고, 과태료는 최소 1년 유예됐다. 2026년 7월 21일에는 개정안·시행령 개정안이 적용돼 생성형 AI 결과물 표시 기준과 고영향 AI 관리 기준이 구체화됐고, 국가AI전략위원회가 법정위원회로 바뀌고 'AI 제품·서비스 확인제도'가 생겼다(확인 필요).",
    check_flags=["7월 개정 내용은 경북매일 한 건 기준 — 정부 보도자료·법제처 원문 확인 필요", "계도기간의 시작·종료일은 보도에 없음"],
    sources=_more("I4-E-004", "kbmaeil", "twig24"))
revise("I4-E-007", "누락정정", "관보 게재(07-24)·발효(07-27) 날짜와 시행 일정 세부가 빠져 있었다.",
    statement="EU가 AI법 개정(디지털 옴니버스, Regulation (EU) 2026/1744)을 2026년 7월 24일 관보에 게재하고 7월 27일 발효시켰다. 고위험 AI 의무 적용을 2026년 8월에서 2027년 12월 2일로, 제품 결합형 고위험 AI는 2028년 8월로 미뤘고, 공공기관용 AI는 2030년 8월 2일로 따로 정해졌다. 투명성 의무(Article 50)는 2026년 8월 2일 그대로 적용되고, 이미 시판된 생성 AI의 표시 의무는 2026년 12월 2일이다.",
    date="2026-07-24", check_flags=["관보 날짜는 Lewis Silkin, 법규 번호는 Orrick(모두 B) 기준이며 EUR-Lex 원문은 열지 못함"],
    sources=_more("I4-E-007", "lewissilkin", "sidley"))
revise("I4-E-008", "상충", "최종 승인일이 출처마다 다르다(Pearl Cohen·eWeek 07-20, Writer Beware는 '화요일'이라 07-21로 추정).",
    statement="법원이 Anthropic과 저자들의 15억 달러 저작권 합의를 2026년 7월 20일(월)에 최종 승인했다고 두 곳이 전한다. Writer Beware는 '화요일'이라 해 7월 21일로 읽힌다.",
    date="2026-07-20", check_flags=["법원 명령 원문은 열지 못함 — 7월 20일·21일 중 확인 필요", "Writer Beware의 07-21은 글 날짜(07-23)에서 추정한 값"],
    sources=_more("I4-E-008", "pearlcohen", "eweek"))
revise("I4-E-009", "상충", "8-K에는 '컴퓨트 매출 가정 없음'과 3분기 전망만 있고 '일부만 출하'·'H200 재고 4억 달러 손실'은 타임라인 정리(B)에만 있다. 8-K를 A 출처로 함께 달아 A로 확인된 것처럼 읽혔다.",
    statement="NVIDIA가 2026년 8월 실적 발표에서 3분기(8~10월) 전망에 중국 데이터센터 컴퓨트 매출을 가정하지 않았다(3분기 매출 전망 1,080억 달러, ±2%). 중국 수출 허용 물량의 일부만 출하했고 H200 재고 4억 달러를 손실 처리했다는 내용은 8-K에는 없고 타임라인 정리(B)에만 있다(확인 필요).",
    check_flags=["'일부만 출하'·'H200 재고 4억 달러 손실'은 8-K에 없고 WhatLedTo 타임라인(B)에만 있음 — 컨퍼런스콜·10-Q 확인 필요", "'중국 데이터센터 매출 0'이 아니라 '컴퓨트 매출 가정 없음'"])
revise("I4-E-010", "상충", "문서는 의견서가 아니라 statement of interest(관심 표명서)이고, Axios 09-08 기사가 이미 DOJ 지지 서면을 전했다. 09-19는 기사 날짜일 수 있다.",
    statement="미국 법무부가 뉴욕타임스 대 OpenAI 소송에 statement of interest(관심 표명서)를 내 'AI 학습은 새롭고 변형적이어서 공정 이용'이라는 입장을 밝혔다. 출력물까지 같은 논리가 적용되지는 않는다고 선을 그었다. 정부 입장일 뿐 판결이 아니다.",
    check_flags=["사건 날짜(2026-09-19)는 기사 날짜일 수 있어 실제 제출일은 더 이를 수 있음 — 확인 필요", "09-08 Axios 기사가 같은 서면을 가리키는지 확신하지 못함", "법원 기록 원문은 열지 못함"],
    sources=_more("I4-E-010", "axios_0908"))
add(id="I4-E-011", type="사건", importance=3, added_on=CHG, statement="미국 제3순회 연방항소법원이 Thomson Reuters v. ROSS에서 AI 학습을 공정 이용으로 보지 않은 1심을 유지했다(9월 29일 판결, 30일 공개). 첫 연방 항소심의 AI 학습 공정 이용 판단이다. 비생성형 AI이고 직접 경쟁 제품이라 판단 범위가 좁을 수 있으며, ROSS는 대법원 상고를 예정하고 있다.",
    date="2026-09-29", actor="미국 제3순회 연방항소법원", sources=src("lawnext"), verified=True,
    check_flags=["판결문 전문은 비공개 — 기사 요약 기준이며 B등급 단일 출처(확인 필요)", "ROSS의 대법원 상고 예정이라 확정 아님"])

# --- 해석 ---
revise("I4-I-001", "단정반증", "'반년째 20% 안팎에서 멈췄다'는 근거가 약하다(17~20% 구간의 상단이고 20명 이상 기업은 올랐다). '대기업이 전사 확장을 빠르게 늘린다'도 전년 값이 없어 쓸 수 없다. Agent 확장(27%→40%)만 확인된다.",
    statement="AI 확산은 넓이보다 깊이로 진행되고 있다. 미국 기업 전체 사용률은 2025년 12월부터 17~20% 구간이고(최신 19.8%), 20명 이상 기업은 올랐지만 20명 미만 기업은 변화가 없었다. 대기업은 Agent 확장을 27%에서 40%로 늘렸고 전사 확장은 54%다(대기업의 1년 전 값은 확인 필요).",
    check_flags=["대기업 전사 확장의 1년 전 값을 확인하지 못해 증가 속도는 판단하지 않음", "BTOS 2026-05-03 이후 값은 확인하지 못함 — 정체인지 완만한 상승인지 확인 필요"])
revise("I4-I-002", "단정반증", "'IT·소프트웨어 개발은 운영 단계'는 기록된 근거에 없다. 코딩 Agent 확장은 전체 약 2할(대기업 31%)이라 판정 기준표로는 전체 초기 확산, 대기업만 확산이다. 정보·금융 단계는 BTOS 정의 변경으로 엄격 기준에서는 내려갈 수 있다.",
    statement="미국 기업 사용률이 가장 높은 업종은 정보(39.7%)와 금융·보험(33.9%)이고, 이들이 실제 운영 단계에 들어섰다(2025년 11월 넓어진 정의 기준이라 '주로 AI로 한다'는 엄격한 기준에서는 한 단계 낮아질 수 있다). IT·소프트웨어 개발 업무는 코딩 Agent 확장이 전체 약 2할, 대기업 31%라 전체로는 초기 확산, 대기업은 확산 단계다. 소매와 제조는 아직 초기 확산 단계이며, 제조는 공급망·재고 업무에서 Agent를 시험하는 수준이다.",
    check_flags=["BTOS 정의가 넓어져 엄격 기준(주로 AI로 한다)을 적용하면 정보·금융이 초기 확산으로 내려갈 수 있음 — 좁은 정의의 업종별 값 확인 필요(판정 유지)", "IT·소프트웨어 개발 업무의 운영 단계 판정은 코딩 Agent 확장 비율(약 2할)로는 뒷받침되지 않음 — 확인 필요"])
revise("I4-I-003", "단정반증", "'규제의 브레이크가 풀리는 쪽'은 고위험 의무와 단속에만 맞다. EU 투명성 의무는 2026-08-02 그대로 적용되고 한국은 7월에 표시·고영향 기준이 구체화됐다. 방향 판정(강화)은 유지한다.",
    statement="규제의 브레이크는 고위험 의무와 단속 쪽에서 풀리고 있다. EU는 고위험 의무를 1년 4개월 미뤘고, 미국은 연방이 주 법을 압박해 콜로라도가 법을 크게 줄였으며, 법무부는 학습 단계의 공정 이용을 지지했다. 다만 표시·투명성 의무는 유지·구체화되고 있다(EU 투명성 의무 2026년 8월 적용, 한국 7월 표시·고영향 AI 기준 구체화).",
    basis=["I4-E-007", "I4-E-002", "I4-E-005", "I4-E-010", "I4-E-004"])
revise("I4-I-004", "단정반증", "'정상 취득 데이터의 학습은 공정 이용 쪽으로 기울고 있다'는 단정은 제3순회 ROSS 판결(항소심 첫 판단, 학습 공정 이용 부정)과 맞지 않는다. 사건별로 갈린다.",
    statement="저작권은 '막는 요인'에서 '비용'으로 바뀌고 있지만 판단은 사건별로 갈린다. 해적판 학습에는 저작물당 약 3,100달러라는 가격이 매겨졌다. 앞선 1심 결정 가운데는 공정 이용을 인정한 것이 있으나, 제3순회는 2026년 9월 Thomson Reuters v. ROSS에서 AI 학습의 공정 이용을 부정한 1심을 유지했다(비생성형·직접 경쟁 사안, ROSS는 상고 예정). 뉴욕타임스 사건은 판단 전이고 법무부 입장은 판결이 아니다.",
    basis=["I4-M-006", "I4-E-008", "I4-E-010", "I4-E-011"],
    check_flags=["ROSS 판결문 전문은 비공개 — 기사 요약 기준, 판결 범위가 비생성형 사안에 한정될 수 있음(확인 필요)"])
revise("I4-I-005", "단정반증", "'30~50%가 늦어지고 있다'는 Sightline의 전망치이고 실현치는 2025년 26%다. 원인도 전력 하나가 아니다. 전력이 1위 제약이라는 순위를 바꿀 근거는 없다.",
    statement="지금 확산을 가장 크게 막는 것은 규제가 아니라 전력이다. 올해 완공 예정 미국 데이터센터의 30~50%가 2027년 이후로 밀릴 수 있다는 전망이 나왔고(2025년 실현 지연은 26%), 전력 제약·지역 반대·변압기 등 장비 부족이 함께 꼽힌다. 돈이 있어도 연산 능력이 제때 들어서지 못할 수 있다.",
    check_flags=["30~50%는 전망치이며 실현치가 아님 — Sightline 원문 확인 필요"])
revise("I4-I-006", "단정반증", "'간접 프롬프트 주입이 실제 공격으로 쓰이지만 대부분 CVE 없이 처리된다'는 1분기 이야기다. 3분기 정리는 평가 환경의 Agent 경계 이탈과 공급망 사고가 중심이고 CVE가 붙은 사건도 있다. '새 제약'이라는 방향은 유지한다.",
    statement="Agent 보안은 운영 확대의 새 제약이다. 1분기에는 간접 프롬프트 주입이 실제 공격 단계에 들어섰고 주요 사고 8건 중 CVE는 1건뿐이었다. 3분기 정리는 평가 환경에서 Agent가 경계를 벗어난 사고 5건과 공급망 사고 3건이 중심이고 CVE가 붙은 사건도 있다. 사건 대부분이 평가·연구 환경 사고라 기업 운영 확대와 직결되는지는 확인 필요하다.",
    check_flags=["3분기 사건이 기업 운영 확대의 제약으로 이어지는지는 확인 필요"])
revise("I4-I-007", "상충", "NVIDIA 8-K는 '중국 컴퓨트 매출을 가정하지 않음'까지만 확인되고, H200 승인·세관 차단(E-001·E-003)은 이번에 원문을 열지 못했다.",
    statement="미국과 중국의 AI 시장은 분리가 굳어지고 있다. 미국이 수수료를 받고 H200 판매를 허용했지만 중국이 수입을 억제해, NVIDIA는 중국 데이터센터 컴퓨트 매출을 전망에 넣지 않았다. 승인·세관 차단의 경위는 타임라인 정리 기준이라 확인이 필요하다.",
    check_flags=["H200 승인·세관 차단(I4-E-001·I4-E-003)은 2차 타임라인 정리 기준 — 확인 필요"])
revise("I4-I-008", "갱신", "한국 국민 사용률이 2026년 2분기 40.6%(12위)로 갱신됐다. 기업 도입률은 과기정통부 2024 통계(30.3%)가 가장 큰 표본이다.",
    statement="한국은 개인 사용이 빠르게 늘고(국민 40.6%, 2026년 2분기, 세계 12위), 법과 GPU 같은 제도·인프라도 갖춰지고 있다. 다만 기업 도입 통계는 과기정통부 2024년 30.3%가 가장 큰 표본의 최신 값이라, 기업 운영 단계는 판정하기 어렵다.",
    check_flags=["2분기 사용률(40.6%)은 보도 기준 — Microsoft 원문 확인 필요"])

# --- 전망 ---
revise("I4-F-001", "판정 기준 보완", "NVIDIA 표현('중국 Data Center compute revenue를 가정하지 않음')에 맞추고, 판정 대상 분기를 분명히 했다. 8월 8-K의 전망은 3분기(8~10월)분이라 헷갈렸다.",
    statement="NVIDIA가 2026년 11월 3분기 실적 발표에서 내놓을 4분기(2026년 11월~2027년 1월) 전망에서도 중국 데이터센터 컴퓨트 매출을 가정하지 않을 것이다.",
    method="NVIDIA 3분기(FY2027) 실적 발표의 4분기 전망 문구에서 'Data Center compute revenue from China를 가정하지 않는다'는 표현이 유지되는지 확인. 네트워킹 등 컴퓨트 외 중국 매출은 판정에서 제외",
    check_flags=["3분기 실적 발표일이 2026-11-30 이전인지 확인하지 못함 — 확인 필요"])
revise("I4-F-002", "판정 기준 보완", "어떤 값을 볼지 정하지 않았다. 최신 확인값 19.8%와 임계값 21%의 차이(1.2%p)가 17~20% 변동폭 안이고, 문항이 2025-11에 바뀐 전례가 있다(제안 기준).",
    statement="BTOS 전국 현재 AI 사용률(최근 2주 안에 어떤 업무 기능에서든 AI 사용)은 2026년 12월 마지막 두 격주 값의 평균이 21% 이상일 것이다.",
    condition="BTOS 조사가 계속 발표되고 문항이 유지될 경우",
    method="미국 인구조사국 BTOS 전국 현재 AI 사용률 2026-12 마지막 두 격주 값의 평균 확인",
    check_flags=["2026-05-03 이후 값을 확인하지 못해 이미 21%를 넘었을 가능성을 배제하지 못함 — 확인 필요", "문항이 2025-11-17에 바뀐 전례가 있어 다시 바뀌면 판정이 불가능"])
revise("I4-F-003", "판정 기준 보완", "'판단'이 약식판결 일부(학습 단계만, 일부 청구만)를 포함하는지 정하지 않았다(제안 기준). 약식판결 변론은 끝났고 판사가 수개월 안에 결정할 것으로 보도됐다.",
    statement="2027년 6월 말까지 뉴욕타임스 대 OpenAI 소송에서 학습 단계의 공정 이용 여부에 대한 법원의 명시적 판단(약식판결 일부 포함)이 나올 것이다. 학습·출력을 나눠 판단하면 학습 부분만 있어도 인정한다.",
    method="법원 기록 또는 주요 언론 보도에서 학습 단계 공정 이용에 대한 명시적 판단(약식판결 일부 포함) 확인",
    check_flags=["중간 항소로 지연될 가능성은 확인하지 못함", "법원 기록 원문은 열지 못함"])
revise("I4-F-004", "판정 기준 보완", "예측(2026-02 Sightline '30~50% 지연 가능')과 실현을 구분하지 않았고, 2025년 실현치가 26%로 30% 미만이었다. 분모와 집계 기관도 정하지 않았다(제안 기준).",
    statement="2027년 6월 말까지 공개된 Sightline Climate 또는 Bloomberg 집계에서 2026년 예정 미국 데이터센터 프로젝트(건수 기준)의 실제 지연·취소 비율이 30% 이상으로 나올 것이다.",
    method="Sightline Climate·Bloomberg 집계에서 2026년 예정 프로젝트(건수 기준)의 실제 지연·취소 비율 확인. 지연과 취소를 합쳐 보고, 전망치가 아니라 실현치만 인정",
    check_flags=["기준 변경은 제안 기준이며 Sightline 원문을 열지 못함 — 확인 필요", "2025년 실현치가 26%였으므로 임계값 30%는 전망이 맞아도 실현치로는 틀릴 수 있음", "집계 기관이 2027년 상반기 안에 새 집계를 내는지 알 수 없음"])
revise("I4-F-005", "판정 기준 보완", "'다시 미루자는 공식 제안'이 무엇인지 정하지 않았다(제안 기준). 디지털 옴니버스는 2026-07-27 이미 발효했고 고위험 의무는 2027-12-02로 확정돼 있다.",
    statement="2027년 6월 말까지 EU 집행위원회가 고위험 AI 의무(2027년 12월 2일 적용) 시기의 추가 연기를 입법 제안(Commission proposal)으로 공식 제출하지 않을 것이다.",
    method="EU 집행위원회 발표 확인. 집행위가 입법 제안으로 고위험 의무 시기 연기를 공식 제출한 경우만 인정하고 의회·이사회 논의나 위원 발언은 인정하지 않는다. 공공기관용 AI(2030-08-02)는 대상에서 제외",
    check_flags=["재연기 가능성의 증거는 찾지 못함", "기준 변경은 제안 기준"])
revise("I4-F-006", "판정 기준 보완", "발표 시점 위험이 있다(2026 보고서는 2026-08-25 발표, 설문은 5~6월). 같은 문항·응답자 전체 기준인지 정해야 하고, +6%p(38→44) 속도면 정확히 50%라 경계에 걸린다(제안 기준).",
    statement="McKinsey 2027년 조사가 2027년 9월 30일까지 발표되면, 같은 문항('scaling across the enterprise')의 응답자 전체 기준 전사 확장 비율은 50% 이상일 것이다.",
    method="McKinsey State of AI 2027에서 같은 문항의 응답자 전체(대기업만이 아닌) 전사 확장 비율 확인. 2027-09-30까지 발표되지 않으면 판정 보류",
    check_flags=["같은 속도(+6%p)로 늘면 정확히 50%로 임계값 경계", "2025년 보고서의 발표 시기는 확인하지 못함", "기한 처리(발표 지연 시 보류)는 제안 기준"])
revise("I4-F-101", "전망 점검", "서술의 '대기업 과반이 전사로 확장'은 McKinsey 2026에서 이미 충족돼 있고(대기업 54%), 판정 방법 (2)는 응답자 전체 44%를 기준으로 해 서술과 방법이 다른 지표를 가리켰다. 방법의 BTOS 항목은 문항 유지를, 지연·취소 항목은 F-004의 실현치 기준을 따르도록 맞췄다(제안 기준).",
    statement="2027년 말까지 AI가 정보·금융을 넘어 소매·제조의 핵심 업무로 들어간다. 미국 기업 사용률이 25%를 넘고, 응답 기업 전체의 과반이 AI를 전사로 확장한다(대기업은 2026년 이미 54%). 규제는 연기·완화 기조가 유지되고, 전력 병목은 신규 발전·연결로 풀리기 시작한다.",
    method="세 가지 중 두 가지 이상 충족 시 적중: (1) 미국 BTOS 전국 현재 AI 사용률 25% 이상(문항 유지 시) (2) McKinsey 전사 확장 비율(응답자 전체 기준) 50% 이상 (3) Sightline Climate·Bloomberg 집계에서 2026년 예정 미국 데이터센터 프로젝트의 실제 지연·취소 비율(건수 기준) 30% 미만",
    check_flags=["(1)은 BTOS가 19.8%에서 5%p 넘게 올라야 하는 가장 어려운 조건이고, 문항이 다시 바뀌면 시계열이 끊김", "(3)은 2025년 실현치가 26%라 이미 충족 상태에 가까움 — 변별력 확인 필요", "방법 변경은 제안 기준"])

# ---------- 수동 입력 (patches.jsonl — tools/intake.py가 쓴다) ----------
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "lib"))
from records import apply_patches
apply_patches(records, Path(__file__).parent / "patches.jsonl")

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

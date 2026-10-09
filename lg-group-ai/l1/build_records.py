"""L1 R1 4유형 기록 생성 + 규칙 검증.
출력: i4/records.jsonl
"""
import json, sys
from pathlib import Path
from collections import Counter

R = "R1"
SRC = {
 "lge_air": {"url": "https://www.newsis.com/view/NISX20261005_0003814461", "publisher": "뉴시스 (LG전자 발표)", "date": "2026-10-05", "grade": "B"},
 "lge_q2": {"url": "https://www.dailian.co.kr/news/view/1672740/", "publisher": "데일리안 (LG전자 2분기 실적)", "date": "2026-07-30", "grade": "B"},
 "lge_dcw": {"url": "https://www.lg.com/global/newsroom/news/eco-solution/lg-electronics-showcases-ai-data-center-cooling-solutions-at-data-center-world-2026/", "publisher": "LG전자 뉴스룸", "date": "2026-04-21", "grade": "A"},
 "lges_q2": {"url": "https://inside.lgensol.com/2026/07/lg%EC%97%90%EB%84%88%EC%A7%80%EC%86%94%EB%A3%A8%EC%85%98-2026%EB%85%84-2%EB%B6%84%EA%B8%B0-%EC%8B%A4%EC%A0%81%EB%B0%9C%ED%91%9C-%EB%A7%A4%EC%B6%9C-7%EC%A1%B05602%EC%96%B5-%EC%9B%90-%EC%98%81%EC%97%85/", "publisher": "LG에너지솔루션 Battery Inside (2분기 실적)", "date": "2026-07-30", "grade": "A"},
 "cns_h1": {"url": "https://www.thelec.kr/news/articleView.html?idxno=62708", "publisher": "디일렉 (LG CNS 반기보고서)", "date": "2026-09-23", "grade": "B"},
 "cns_naver": {"url": "https://www.etnews.com/20260401000451", "publisher": "전자신문 (LG CNS 공시)", "date": "2026-04-01", "grade": "B"},
 "cns_box": {"url": "https://byline.network/2026/03/5-405/", "publisher": "바이라인네트워크 (LG CNS 발표)", "date": "2026-03-05", "grade": "B"},
 "lgu_paju": {"url": "https://www.ajunews.com/view/20260607075248654", "publisher": "아주경제 (LG유플러스 간담회)", "date": "2026-06-07", "grade": "B"},
 "nvda_map": {"url": "https://technode.global/prnasia/lg-teams-with-nvidia-to-shape-the-future-with-m-a-p-mobility-ai-infra-physical-ai/", "publisher": "PR Newswire (LG 발표)", "date": "2026-06-08", "grade": "A"},
 "ms_plan": {"url": "https://www.datacenterdynamics.com/en/news/microsoft-to-use-lg-electronics-cooling-infrastructure-in-some-ai-data-centers", "publisher": "DatacenterDynamics", "date": "2025-04-21", "grade": "B"},
 "ms_show": {"url": "https://www.koreaherald.com/article/10882162", "publisher": "Korea Herald", "date": "2026-09-22", "grade": "B"},
 "vertiv": {"url": "https://www.marketbeat.com/instant-alerts/vertiv-q2-earnings-call-highlights-2026-08-01/", "publisher": "MarketBeat (Vertiv 2분기 실적)", "date": "2026-08-01", "grade": "B"},
}
def src(*keys): return [dict(SRC[k], key=k) for k in keys]

base = dict(question="L1", question_version="v1.0", first_seen=R, last_seen=R, status="유효", replaces=None, check_flags=[])
records = []
def add(**kw):
    r = dict(base); r.update(kw); records.append(r)

TARGET = "회사 목표·전망 — 실적 아님"

# ---------- 지표 (M) ----------
add(id="L1-M-001", type="지표", indicator="L1-T1", importance=3, statement="LG전자의 2026년 상반기 AI 데이터센터 냉각 수주액은 6,000억 원을 넘었다. 10월에는 북미 데이터센터 인프라 기업 Air Control Concept과 총 5GW 규모의 칠러 장기 공급 계약을 맺었고, 회사는 연말 누적 수주가 수조 원대에 이를 것으로 본다.",
    value=6000, unit="억 원 이상 (상반기 AIDC 냉각 수주)", as_of="2026-H1", region="GLOBAL", definition="LG전자 AI 데이터센터 냉각 솔루션 수주액", extra={"lta": "5GW (Air Control Concept)", "year_end_outlook": "수조 원대 (회사 전망)"},
    sources=src("lge_air"), verified=True, check_flags=["5GW 계약의 금액·기간 미공개", "연말 전망은 회사 전망"])
add(id="L1-M-002", type="지표", indicator="L1-T2", importance=2, statement="LG전자 냉난방공조(ES) 사업본부의 2026년 2분기 매출은 2조 7,261억 원, 영업이익률 8.6%였다. AI 데이터센터 냉각 매출은 따로 공개되지 않았고, 칠러 사업 매출 1조 원 목표를 2027년 말보다 앞당기겠다고 밝혔다.",
    value=27261, unit="억 원 (ES사업본부 2분기 매출)", as_of="2026-Q2", region="GLOBAL", definition="LG전자 ES사업본부 분기 매출", extra={"op_margin": "8.6%", "chiller_target": "칠러 매출 1조 원 (조기 달성 목표)"},
    sources=src("lge_q2", "lge_air"), verified=True, check_flags=["AIDC 냉각 매출 미분리", TARGET])
add(id="L1-M-003", type="지표", indicator="L1-T3", importance=3, statement="LG에너지솔루션의 2026년 상반기 ESS 신규 수주는 3조 원을 넘었고, 여기에는 최종 고객이 하이퍼스케일러인 AI 데이터센터 프로젝트가 포함됐다.",
    value=3, unit="조 원 이상 (상반기 ESS 신규 수주)", as_of="2026-H1", region="GLOBAL", definition="LG에너지솔루션 ESS 신규 수주", extra={"ai_dc": "하이퍼스케일러 AI 데이터센터 프로젝트 포함"},
    sources=src("lges_q2"), verified=True, check_flags=["AI 데이터센터 프로젝트의 규모·고객명 미공개"])
add(id="L1-M-004", type="지표", indicator="L1-T4", importance=2, statement="LG에너지솔루션의 2026년 상반기 ESS 매출은 1년 전의 4.6배로 늘어 전체 매출의 20% 후반이 됐다. 북미 ESS 생산능력은 연말 50GWh 이상이 목표다.",
    value=4.6, unit="배 (상반기 ESS 매출, 전년 대비)", as_of="2026-H1", region="GLOBAL", definition="LG에너지솔루션 ESS 매출 성장", extra={"share": "20% 후반", "na_capacity_target": "50GWh 이상 (연말)"},
    sources=src("lges_q2"), verified=True)
add(id="L1-M-005", type="지표", indicator="L1-T5", importance=3, statement="LG CNS는 2026년 상반기 데이터센터 설계·구축·운영(DBO) 수주 1조 원 이상을 확보했다. 인도네시아 자카르타 데이터센터(30MW, 220MW까지 확장 가능, 약 1,000억 원)에서는 냉각·전력·통신 인프라를 맡았다.",
    value=1, unit="조 원 이상 (상반기 DBO 수주)", as_of="2026-H1", region="GLOBAL", definition="LG CNS 데이터센터 DBO 수주", extra={"jakarta": "30MW → 220MW, 약 1,000억 원"},
    sources=src("cns_h1"), verified=True)
add(id="L1-M-006", type="지표", indicator="L1-T6", importance=3, statement="LG CNS는 네이버클라우드와 고양 삼송 데이터센터 입주(코로케이션) 계약을 약 6,034억 원 규모로 맺었다. 기간은 2026년 7월부터 2035년 5월까지다.",
    value=6034, unit="억 원 (계약 규모)", as_of="2026-04", region="KR", definition="데이터센터 코로케이션 계약 규모", extra={"term": "2026-07 ~ 2035-05", "customer": "네이버클라우드"},
    sources=src("cns_naver"), verified=True, check_flags=["AI 전용 여부는 계약에 명시되지 않음"])
add(id="L1-M-007", type="지표", indicator="L1-T7", importance=3, statement="LG유플러스 파주 AIDC는 200MW로 시작해 600MW까지 늘릴 계획이며, 200MW 기준 Blackwell GPU 약 7만 장을 수용한다. 첫 동(50MW)은 이미 고객을 확보했고 가동은 2027년이다. 향후 5년간 수주 매출 5조 원이 목표다.",
    value=200, unit="MW (1단계 용량)", as_of="2026-06", region="KR", definition="LG유플러스 파주 AIDC 용량", extra={"expansion": "600MW", "gpu": "약 7만 장", "building1": "50MW 고객 확보 (고객명 비공개)", "go_live": "2027", "order_target": "5년간 5조 원"},
    sources=src("lgu_paju"), verified=True, check_flags=["첫 동 고객명 비공개", TARGET])
add(id="L1-M-008", type="지표", indicator="L1-T7", importance=2, statement="LG CNS는 Vera Rubin을 포함한 GPU·인프라에 3,814억 원을 투자한다. 삼송 데이터센터(80MW), 부산 AI Box 캠퍼스(약 60MW, AI Box 50개), 인천공항 AI 데이터센터(40MW, 지분 33.22%)를 추진한다.",
    value=3814, unit="억 원 (GPU·인프라 투자)", as_of="2026-06", region="KR", definition="LG CNS GPU 투자와 데이터센터 용량", extra={"samsong": "80MW", "busan": "약 60MW", "incheon": "40MW"},
    sources=src("cns_h1"), verified=True)
add(id="L1-M-009", type="지표", indicator="L1-T8", importance=2, statement="글로벌 데이터센터 냉각·전력 1위권 Vertiv의 2026년 2분기 매출은 32억 7,400만 달러로 24% 늘었다(유기적 성장 18%). 직접 칩 냉각(콜드 플레이트) 기업을 인수해 액체냉각 포트폴리오를 넓혔다.",
    value=32.74, unit="억 달러 (Vertiv 분기 매출)", as_of="2026-Q2", region="GLOBAL", definition="경쟁사 Vertiv 분기 매출", extra={"growth": "+24%", "organic": "+18%"},
    sources=src("vertiv"), verified=True)

# ---------- 사건 (E) ----------
add(id="L1-E-001", type="사건", importance=2, statement="Microsoft가 차세대 AI 데이터센터 일부에 LG전자 냉각 설비(콜드 플레이트·CDU·칠러·CRAH)를 쓸 계획이라고 밝혀졌다. 계약 규모·범위는 공개되지 않았다.",
    date="2025-04-21", actor="LG전자·Microsoft", sources=src("ms_plan"), verified=True, check_flags=["조사 기간 이전 — 기준선", "계약 체결 여부·규모 미공개"])
add(id="L1-E-002", type="사건", importance=2, statement="LG·LS 계열사가 Microsoft 레드먼드 본사에서 냉각·배터리 저장·전력·모듈형 데이터센터 기술을 선보였다. 구매 주문·물량·계약 금액은 발표되지 않았다.",
    date="2025-12", actor="LG 계열사·Microsoft", sources=src("ms_show"), verified=True, check_flags=["'연간 수십억 달러 계약' 보도는 원문으로 확인되지 않음"])
add(id="L1-E-003", type="사건", importance=2, statement="LG CNS가 컨테이너형 AI 데이터센터 'AI Box'(최대 GPU 576장·1.2MW, 약 6개월 구축)를 내놓고 부산에 50개 규모 캠퍼스를 짓겠다고 밝혔다.",
    date="2026-03-05", actor="LG CNS", sources=src("cns_box"), verified=True)
add(id="L1-E-004", type="사건", importance=3, statement="LG CNS가 네이버클라우드와 6,034억 원 규모의 삼송 데이터센터 입주 계약을 공시했다.",
    date="2026-04-01", actor="LG CNS", sources=src("cns_naver"), verified=True)
add(id="L1-E-005", type="사건", importance=2, statement="LG전자가 Data Center World 2026에서 1.4MW CDU·콜드 플레이트·액침 냉각·DC Grid(LS·LG에너지솔루션 공동)를 선보였다.",
    date="2026-04-21", actor="LG전자", sources=src("lge_dcw"), verified=True)
add(id="L1-E-006", type="사건", importance=3, statement="LG유플러스가 파주 AIDC 첫 동(50MW)의 고객을 확보했다고 밝히고, 향후 5년간 수주 매출 5조 원 목표를 제시했다. LG전자의 액체냉각·칠러가 적용된다.",
    date="2026-06-05", actor="LG유플러스", sources=src("lgu_paju"), verified=True)
add(id="L1-E-007", type="사건", importance=3, statement="LG와 NVIDIA가 M.A.P. 협력을 발표했다. AI 인프라에서는 LG유플러스가 Rubin GPU 기반 인프라를, LG CNS가 NVIDIA DSX 참조 설계 기반 AI 데이터센터를, LG전자가 CDU·콜드 플레이트 냉각을, LG에너지솔루션이 800V DC 전력 솔루션을 맡는다.",
    date="2026-06-08", actor="LG·NVIDIA", sources=src("nvda_map"), verified=True)
add(id="L1-E-008", type="사건", importance=2, statement="LG에너지솔루션이 상반기 ESS 신규 수주 3조 원 이상, 하이퍼스케일러 AI 데이터센터 프로젝트 포함을 발표했다. LG전자는 자체 개발 CDU가 글로벌 AI 데이터센터 핵심 공급망 진입을 앞두고 있다고 밝혔다.",
    date="2026-07-30", actor="LG에너지솔루션·LG전자", sources=src("lges_q2", "lge_q2"), verified=True)
add(id="L1-E-009", type="사건", importance=2, statement="LG CNS 반기보고서에서 상반기 데이터센터 DBO 수주 1조 원 이상, GPU·인프라 투자 3,814억 원이 확인됐다.",
    date="2026-09-23", actor="LG CNS", sources=src("cns_h1"), verified=True)
add(id="L1-E-010", type="사건", importance=3, statement="LG전자가 북미 Air Control Concept과 총 5GW 규모의 AI 데이터센터 칠러 장기 공급 계약을 맺었다. 물량이 보장되는 방식이며, CDU로의 품목 확대를 협의 중이다.",
    date="2026-10-05", actor="LG전자", sources=src("lge_air"), verified=True)

# ---------- 해석 (I) ----------
add(id="L1-I-001", type="해석", importance=3, target="냉각", direction="강화",
    statement="냉각은 '계약(고객 공개)' 단계에 들어섰다. 북미 Air Control Concept과의 5GW 장기 공급 계약, 상반기 수주 6,000억 원 이상이 확인됐다. 다만 AI 데이터센터 냉각 매출은 아직 따로 공개되지 않았고, CDU는 공급망 진입 직전이다.",
    basis=["L1-M-001", "L1-E-010", "L1-M-002", "L1-E-008"])
add(id="L1-I-002", type="해석", importance=3, target="전력·ESS", direction="강화",
    statement="전력·ESS는 '계약' 단계지만 고객이 공개되지 않았다. 상반기 ESS 수주 3조 원에 하이퍼스케일러 AI 데이터센터 프로젝트가 포함됐고, ESS 매출은 4.6배로 늘었다. AI 데이터센터 전용인 800V DC 전력은 NVIDIA와 개발 단계다.",
    basis=["L1-M-003", "L1-M-004", "L1-E-007"])
add(id="L1-I-003", type="해석", importance=3, target="구축(DBO)", direction="강화",
    statement="구축(DBO)은 수주로 가장 많이 확인된 영역이다. LG CNS는 상반기 DBO 수주 1조 원 이상을 확보했고 자카르타에서 냉각·전력·통신을 맡았다. 모듈형 AI Box는 자체 캠퍼스 계획 단계로, 외부 판매는 아직 확인되지 않는다.",
    basis=["L1-M-005", "L1-E-003", "L1-E-009"])
add(id="L1-I-004", type="해석", importance=3, target="운영(AIDC·코로케이션)", direction="중립",
    statement="운영은 계약은 있지만 매출은 2027년부터다. LG CNS는 네이버클라우드와 9년 6,034억 원 계약을 맺었지만 AI 전용인지는 명시되지 않았고, LG유플러스 파주 AIDC는 첫 동 고객을 확보했지만 고객명은 비공개이며 가동은 2027년이다.",
    basis=["L1-M-006", "L1-M-007", "L1-E-006"])
add(id="L1-I-005", type="해석", importance=3, target="계약에서 매출로", direction="중립",
    statement="네 제품군 모두 '계약' 단계에 와 있지만, AI 데이터센터 매출로 따로 확인된 것은 없다. 냉각 매출은 ES사업본부에, AI 데이터센터 ESS는 ESS 전체에 섞여 있고, AIDC 운영은 2027년 가동이다. 2027년이 매출 전환을 확인하는 해다.",
    basis=["L1-M-002", "L1-M-003", "L1-M-007"])
add(id="L1-I-006", type="해석", importance=2, target="One LG 패키지", direction="강화",
    statement="계열사 역할 분담은 NVIDIA 협력에서 정식화됐다(U+ 운영, CNS 설계·구축, 전자 냉각, 엔솔 전력). 실제로 묶어 판 첫 사례는 그룹 내부다. 파주 AIDC에 LG전자 냉각이 들어가고, DC Grid는 LG전자·엔솔이 함께 만든다. 외부 고객 대상 패키지 수주는 아직 확인되지 않는다.",
    basis=["L1-E-007", "L1-E-006", "L1-E-005"])
add(id="L1-I-007", type="해석", importance=2, target="Microsoft", direction="중립",
    statement="Microsoft와의 냉각 협력은 '계획·협의' 단계로 남아 있다. 2025년 4월 냉각 설비를 쓸 계획이 알려졌고 12월 기술 시연이 있었지만, 계약 규모나 주문은 공개되지 않았다. '연간 수십억 달러' 보도는 원문으로 확인되지 않는다.",
    basis=["L1-E-001", "L1-E-002"])
add(id="L1-I-008", type="해석", importance=2, target="글로벌 비교", direction="중립",
    statement="LG 냉각 사업은 빠르게 크지만 규모는 아직 작다. Vertiv의 분기 매출은 약 33억 달러로, LG전자 ES사업본부 전체 분기 매출(약 2조 7천억 원)보다 크다. LG의 AI 데이터센터 냉각 수주는 반기 6,000억 원 수준이다. 경쟁사가 직접 칩 냉각 인수로 포트폴리오를 넓히는 만큼, CDU 공급망 진입이 LG의 다음 관문이다.",
    basis=["L1-M-009", "L1-M-001", "L1-M-002"])

# ---------- 세부 전망 (F) ----------
add(id="L1-F-001", type="전망", importance=3, status="유효", forecast_status="진행 중",
    statement="LG전자는 2026년 말까지 CDU 공급 계약을 고객 또는 규모를 밝혀 발표할 것이다.", due="2026-12-31", condition="없음",
    method="LG전자 공식 발표 또는 주요 언론 보도 확인", basis=["L1-E-008", "L1-E-010"], result=None)
add(id="L1-F-002", type="전망", importance=3, status="유효", forecast_status="진행 중",
    statement="LG전자는 2026년 연간 AI 데이터센터 냉각 수주를 1조 원 이상이라고 밝힐 것이다.", due="2027-01-31", condition="수주액을 공개할 경우",
    method="LG전자 2026년 4분기 실적 발표 또는 공식 발표 확인", basis=["L1-M-001"], result=None)
add(id="L1-F-003", type="전망", importance=2, status="유효", forecast_status="진행 중",
    statement="LG CNS의 2026년 연간 데이터센터 DBO 수주는 2조 원 이상으로 확인될 것이다.", due="2027-03-31", condition="없음",
    method="LG CNS 사업보고서 또는 공식 발표 확인", basis=["L1-M-005"], result=None)
add(id="L1-F-004", type="전망", importance=2, status="유효", forecast_status="진행 중",
    statement="LG유플러스는 2027년 6월 말까지 파주 AIDC 둘째 동 이상의 고객 확보를 발표할 것이다.", due="2027-06-30", condition="없음",
    method="LG유플러스 공식 발표 또는 실적 발표 확인", basis=["L1-M-007"], result=None)
add(id="L1-F-005", type="전망", importance=2, status="유효", forecast_status="진행 중",
    statement="LG에너지솔루션은 2027년 6월 말까지 AI 데이터센터용 ESS·UPS·BBU 수주를 고객명 또는 규모를 밝혀 발표할 것이다.", due="2027-06-30", condition="없음",
    method="LG에너지솔루션 공식 발표·실적 발표 확인", basis=["L1-M-003"], result=None)
add(id="L1-F-006", type="전망", importance=2, status="유효", forecast_status="진행 중",
    statement="2027년 6월 말까지 LG 또는 Microsoft가 냉각 설비 공급 계약을 규모와 함께 공식 발표하지는 않을 것이다.", due="2027-06-30", condition="없음",
    method="LG전자·Microsoft 공식 발표 확인", basis=["L1-E-001", "L1-E-002"], result=None)

# ---------- 메인 질문 시나리오 ----------
add(id="L1-F-101", type="전망", importance=3, status="유효", forecast_status="진행 중", scenario="낙관",
    statement="2027년 말까지 LG의 AI 데이터센터 계약이 매출로 확인된다. LG전자 칠러·AIDC 냉각 매출이 연 1조 원을 넘고, 파주 AIDC가 가동되며 대부분의 동이 채워지고, 두 개 이상 계열사가 함께 들어간 해외 AIDC 수주가 나온다.",
    milestones=[
        {"by": "2026-12", "text": "CDU 공급 계약 공개"},
        {"by": "2027-01", "text": "2026년 AIDC 냉각 수주 1조 원 이상"},
        {"by": "2027-06", "text": "파주 AIDC 추가 동 고객 확보"}],
    due="2027-12-31", condition="북미 데이터센터 투자가 급감하지 않을 경우",
    method="세 가지 중 두 가지 이상 충족 시 적중: (1) LG전자 칠러 또는 AIDC 냉각 연매출 1조 원 이상 공개 (2) 파주 AIDC 가동과 4개 동 중 3개 동 이상 고객 확보 발표 (3) 두 개 이상 LG 계열사가 함께 참여한 해외 AIDC 수주 공개",
    basis=["L1-M-001", "L1-M-002", "L1-M-007", "L1-M-005"],
    signposts=[{"id": "L1-F-001", "on_hit": "낙관", "on_miss": "비관"}, {"id": "L1-F-002", "on_hit": "낙관", "on_miss": "비관"},
               {"id": "L1-F-003", "on_hit": "낙관"}, {"id": "L1-F-004", "on_hit": "낙관", "on_miss": "비관"},
               {"id": "L1-F-005", "on_hit": "낙관"}, {"id": "L1-F-006", "on_hit": "비관", "on_miss": "낙관"}], result=None)
add(id="L1-F-102", type="전망", importance=3, status="유효", forecast_status="진행 중", scenario="비관",
    statement="2027년 말까지 계약은 늘지만 매출 전환이 늦다. 냉각은 칠러 중심에 머물고 CDU·콜드 플레이트는 경쟁사에 밀리며, 파주 AIDC 고객 확보가 지연되고, 대형 고객(Microsoft 등) 계약은 공개되지 않는다.",
    milestones=[
        {"by": "2026-12", "text": "CDU 공급 계약 미공개"},
        {"by": "2027-06", "text": "파주 AIDC 추가 고객 미발표"},
        {"by": "2027-12", "text": "AIDC 냉각 매출 1조 원 미달"}],
    due="2027-12-31", condition="없음",
    method="낙관 시나리오의 판정 조건 세 가지 중 하나 이하만 충족 시 적중",
    basis=["L1-M-002", "L1-M-009", "L1-E-002"], signposts=[], result=None)

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

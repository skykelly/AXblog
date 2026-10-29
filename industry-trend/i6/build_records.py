"""I6 R1 4유형 기록 생성 + 규칙 검증.
출력: i6/records.jsonl
"""
import json, sys
from pathlib import Path
from collections import Counter

R = "R1"
SRC = {
 "ifr26": {"url": "https://ifr.org/ifr-press-releases/news/five-million-robots-now-operate-in-factories-globally", "publisher": "국제로봇연맹 IFR World Robotics 2026", "date": "2026-09-24", "grade": "A"},
 "ifr25": {"url": "https://ifr.org/ifr-press-releases/news/global-robot-demand-in-factories-doubles-over-10-years", "publisher": "국제로봇연맹 IFR World Robotics 2025", "date": "2025-09-25", "grade": "A"},
 "ifr_den": {"url": "https://www.roboticstomorrow.com/news/2026/04/08/robot-density-surges-in-europe-asia-and-americas-%E2%80%93-ifr-reports/26379/", "publisher": "Robotics Tomorrow (IFR 로봇 밀도 발표)", "date": "2026-04-08", "grade": "B"},
 "wef_lh": {"url": "https://www.weforum.org/press/2026/06/new-global-lighthouse-sites-demonstrate-how-ai-is-rewiring-manufacturing-and-supply-chains/", "publisher": "세계경제포럼 Global Lighthouse Network", "date": "2026-06-22", "grade": "A"},
 "miit": {"url": "https://english.henan.gov.cn/2026/01-08/3307611.html", "publisher": "허난성 정부 (신화통신, 중국 공업정보화부 발표)", "date": "2026-01-08", "grade": "A"},
 "xiaomi": {"url": "https://www.slashgear.com/2144548/xiaomi-smartphone-robot-dark-factory-how-works-makes-phones-fast/", "publisher": "SlashGear", "date": "2026", "grade": "B"},
 "amazon_nyt": {"url": "https://gizmodo.com/leaked-amazon-plans-say-robots-will-help-it-avoid-hiring-600000-workers-2000674920", "publisher": "Gizmodo (뉴욕타임스 보도 인용)", "date": "2025-10-21", "grade": "B"},
 "amazon_robot": {"url": "https://www.techspot.com/news/109947-leaked-documents-reveal-amazon-aims-replace-600000-us.html", "publisher": "TechSpot", "date": "2025-10", "grade": "B"},
 "waymo_jul": {"url": "https://electrek.co/2026/07/08/waymo-driverless-las-vegas-four-new-cities/", "publisher": "Electrek", "date": "2026-07-08", "grade": "B"},
 "waymo_sep": {"url": "https://driveteslacanada.ca/news/waymo-driverless-rides-denver-san-diego-tampa/", "publisher": "Drive Tesla Canada", "date": "2026-09-01", "grade": "C"},
 "baidu": {"url": "https://www.sec.gov/Archives/edgar/data/0001329099/000119312526355431/d112854dex991.htm", "publisher": "Baidu 2026년 2분기 실적 (SEC 6-K)", "date": "2026-08-18", "grade": "A"},
 "pony": {"url": "https://www.automotiveworld.com/news/pony-ai-q2-2026-revenues-up-68-8-on-robotaxi-surge/", "publisher": "Automotive World (Pony.ai 2분기 실적)", "date": "2026-08-18", "grade": "B"},
 "tesla": {"url": "https://electrek.co/2026/03/31/tesla-expands-unsupervised-robotaxi-service-area-still-only-handful-vehicles/", "publisher": "Electrek", "date": "2026-03-31", "grade": "B"},
 "aurora": {"url": "https://www.techspot.com/news/111323-aurora-sets-new-milestone-1000-mile-driverless-freight.html?rand=98523", "publisher": "TechSpot (Aurora 주주서한 인용)", "date": "2026", "grade": "B"},
 "waymo_recall": {"url": "https://www.npr.org/2025/12/06/nx-s1-5635614/waymo-school-buses-recall", "publisher": "NPR", "date": "2025-12-06", "grade": "B"},
 "seoul_jan": {"url": "https://www.twig24.com/news/2026/01/27/20260127019003", "publisher": "트위그24", "date": "2026-01-27", "grade": "C"},
 "seoul_jun": {"url": "https://v.daum.net/v/20260630111713463", "publisher": "다음 뉴스 (서울시 '2026 하반기 달라지는 서울생활' 인용)", "date": "2026-06-30", "grade": "B"},
 "molit": {"url": "https://news.mtn.co.kr/news-detail/2026050617123164061", "publisher": "머니투데이방송 (국토교통부)", "date": "2026-05-06", "grade": "B"},
 "idc": {"url": "https://en.jiemian.com/article/13925066.html", "publisher": "Jiemian (IDC 휴머노이드 출하 보고서 인용)", "date": "2026-01", "grade": "B"},
 "unitree": {"url": "https://scmp.com/tech/tech-trends/article/3340446/chinas-unitree-ships-more-5500-humanoid-robots-2025-surpassing-us-peers", "publisher": "South China Morning Post (Omdia 인용)", "date": "2026-01", "grade": "B"},
 "figure": {"url": "https://bgr.com/2039425/humanoid-ai-robot-retired-figure-02-bmw-x3", "publisher": "BGR", "date": "2025-12-04", "grade": "B"},
 "hyundai": {"url": "https://www.newsis.com/view/NISX20260721_0003717549", "publisher": "뉴시스", "date": "2026-07-25", "grade": "B"},
 "walmart": {"url": "https://dronexl.co/2026/05/31/walmart-1m-drone-deliveries-40/", "publisher": "DroneXL (Walmart 발표 인용)", "date": "2026-05-31", "grade": "B"},
 "kr_robot": {"url": "https://www.kbmaeil.com/article/20260531500390", "publisher": "경북매일", "date": "2026-05-31", "grade": "B"},
}
def src(*keys): return [dict(SRC[k], key=k) for k in keys]

base = dict(question="I6", question_version="v1.0", first_seen=R, last_seen=R, status="유효", replaces=None, check_flags=[])
records = []
def add(**kw):
    r = dict(base); r.update(kw); records.append(r)

# ---------- 지표 (M) ----------
add(id="I6-M-001", type="지표", indicator="I6-T1", importance=3,
    statement="한국의 제조업 로봇 밀도는 근로자 1만 명당 1,220대로 세계 1위다(2024년). 싱가포르 818대, 독일 449대, 일본 446대, 미국 307대, 중국 166대이고 세계 평균은 132대다.",
    value=1220, unit="대/근로자 1만 명", as_of="2024", region="KR", definition="제조업 근로자 1만 명당 가동 중인 산업용 로봇",
    extra={"world": "132", "singapore": "818", "germany": "449", "japan": "446", "us": "307", "china": "166"}, sources=src("ifr_den"), verified=True)
add(id="I6-M-002", type="지표", indicator="I6-T2", importance=3,
    statement="2025년 세계 공장에 새로 설치된 산업용 로봇은 60만 대를 넘어 11% 늘었고, 가동 대수는 9% 늘어 500만 대가 됐다. 중국 설치는 20% 늘어 35만 4천 대로 세계의 59%다.",
    value=600000, unit="대 이상 (2025년 설치)", as_of="2025", region="GLOBAL", definition="세계 산업용 로봇 연간 신규 설치",
    extra={"stock": "500만 대", "china": "354,000대 (59%)", "2024": "542,000대"}, sources=src("ifr26", "ifr25"), verified=True)
add(id="I6-M-003", type="지표", indicator="I6-T2", importance=2,
    statement="2025년 한국의 산업용 로봇 설치는 3만 대로 1% 줄어 세계 4위다. 미국은 12% 늘어 약 3만 8,500대로 2위가 됐고, 일본은 19% 줄어 3만 6,219대, 독일은 8% 줄어 2만 5천 대 미만이다.",
    value=30000, unit="대 (한국 2025년 설치)", as_of="2025", region="KR", definition="국가별 산업용 로봇 연간 신규 설치",
    extra={"kr_2024": "30,600대", "us": "약 38,500대", "japan": "36,219대", "germany": "25,000대 미만"}, sources=src("ifr26", "ifr25"), verified=True)
add(id="I6-M-004", type="지표", indicator="I6-T2", importance=2,
    statement="국제로봇연맹은 세계 산업용 로봇 설치가 2026년 65만 5천 대(+9%), 2029년 80만 6천 대에 이를 것으로 전망했다.",
    value=655000, unit="대 (2026년 전망)", as_of="2026-09", region="GLOBAL", definition="IFR 연간 설치 전망",
    extra={"2029": "806,000대"}, sources=src("ifr26"), verified=True, check_flags=["IFR 전망치이며 실측치가 아님"])
add(id="I6-M-005", type="지표", indicator="I6-T3", importance=2,
    statement="세계경제포럼 등대 공장 네트워크는 2026년 6월 16곳을 새로 지정해 238곳이 됐다. 새 지정에는 중국·인도·사우디·싱가포르·스위스·미국 사업장이 들어갔고 한국은 없었다. 발표문에는 무인 가동(lights-out) 기준이 언급되지 않는다.",
    value=238, unit="곳 (등대 공장)", as_of="2026-06", region="GLOBAL", definition="WEF Global Lighthouse Network 지정 사업장 수",
    extra={"new": "16곳"}, sources=src("wef_lh"), verified=True, check_flags=["등대 공장은 첨단 제조 사업장 지정이며 무인 공장 기준이 아님"])
add(id="I6-M-006", type="지표", indicator="I6-T3", importance=2,
    statement="중국 공업정보화부는 선진급 스마트공장이 7천 곳을 넘고, 그 위 단계인 우수급이 500곳을 넘는다고 밝혔다. 최상위 선도급 육성 대상은 15곳이다.",
    value=7000, unit="곳 이상 (선진급 스마트공장)", as_of="2025-12", region="CN", definition="중국 스마트공장 4단계(기초·선진·우수·선도) 중 선진급",
    extra={"excellence": "500곳 이상", "pioneer": "15곳"}, sources=src("miit"), verified=True, check_flags=["스마트공장 등급이며 무인 공장 여부와 같은 기준이 아님"])
add(id="I6-M-007", type="지표", indicator="I6-T3", importance=2,
    statement="샤오미 창핑 스마트공장은 연간 플래그십 스마트폰 1천만 대를 만들고 생산 라인 자동화율을 81%라고 밝혔다. '1초에 1대'라는 홍보와 달리 연간 평균으로는 약 3.15초에 1대이고, 감독·유지보수 인력은 남아 있다.",
    value=81, unit="% (회사 발표 자동화율)", as_of="2024-07", region="CN", definition="생산 라인 자동화율(회사 발표)",
    extra={"annual_output": "1,000만 대", "cycle": "약 3.15초/대"}, sources=src("xiaomi"), verified=True,
    check_flags=["자동화율은 회사 발표 — 외부 검증 미확보", "기사 게재일 미표기", "'완전 무인' 여부는 확인되지 않음"])
add(id="I6-M-008", type="지표", indicator="I6-T4", importance=3,
    statement="IDC는 2025년 세계 휴머노이드 로봇 출하를 약 1만 8천 대로 집계했다. 1년 전보다 약 508% 늘었고, 주요 용도는 오락·연구·데이터 수집·안내·제조·창고 6개다. 중국 AgiBot이 6개 용도 중 5개에서 출하 1위였다.",
    value=18000, unit="대 (2025년 출하)", as_of="2025", region="GLOBAL", definition="IDC 휴머노이드 로봇 출하 집계",
    extra={"yoy": "+508%"}, sources=src("idc"), verified=True, check_flags=["IDC 원문은 열지 못하고 Jiemian 인용(B)으로 확인 — 휴머노이드 정의(바퀴형 포함 여부) 원문 확인 필요"])
add(id="I6-M-009", type="지표", indicator="I6-T4", importance=2,
    statement="중국 Unitree는 2025년 이족보행 휴머노이드를 5,500대 넘게 출하했다고 알려졌다. Omdia 집계로 Tesla·Figure AI·Agility Robotics는 각각 약 150대였다.",
    value=5500, unit="대 이상 (Unitree 2025년)", as_of="2025", region="CN", definition="이족보행 휴머노이드 연간 출하",
    extra={"tesla_figure_agility": "각 약 150대 (Omdia)"}, sources=src("unitree"), verified=True,
    check_flags=["Unitree 수치는 익명 소식통 기준이고 회사는 논평하지 않음"])
add(id="I6-M-010", type="지표", indicator="I6-T5", importance=3,
    statement="Waymo는 2026년 상반기 기준 약 3,500대로 미국 10개 시장(피닉스·샌프란시스코·LA·오스틴·애틀랜타·마이애미·댈러스·휴스턴·샌안토니오·올랜도)에서 주당 약 50만 건의 유료 운행을 했고, 7월 라스베이거스에서 완전 무인 운행을 시작했다. 2026년 말 목표는 주당 100만 건이다.",
    value=500000, unit="건/주 (유료 운행)", as_of="2026-H1", region="US", definition="안전요원 없는 유료 로보택시 주간 운행", xref=["I2-M-004"],
    extra={"fleet": "약 3,500대", "markets": "10곳 + 라스베이거스", "target": "주 100만 건 (2026년 말)"}, sources=src("waymo_jul"), verified=True,
    check_flags=["사업자 발표 기준(자사 집계)", "기사 안에서 차량 수가 3,500대와 3,000대로 엇갈림", "주당 50만 건·3,500대는 2026년 1분기 시점 수치이고 이후 공식 수치 없음(I2-M-004)"])
add(id="I6-M-011", type="지표", indicator="I6-T5", importance=3,
    statement="Baidu Apollo Go는 2026년 8월 기준 세계 28개 도시에서 운영하며, 누적 자율주행 거리 3억 5천만 km 중 완전 무인 주행이 2억 4천만 km를 넘었다.",
    value=28, unit="곳 (운영 도시)", as_of="2026-08", region="CN", definition="Apollo Go 운영 도시 수",
    extra={"driverless_km": "2억 4천만 km 이상", "total_km": "3억 5천만 km 이상"}, sources=src("baidu"), verified=True,
    check_flags=["I2-I-002는 2분기 완전 무인 약 100만 회를 기록했으나 이번 6-K 요약에서는 운행 건수를 확인하지 못함 — 상충, 원문 재확인 필요", "사업자 발표 기준(자사 집계)"], xref=["I2-I-002"])
add(id="I6-M-012", type="지표", indicator="I6-T5", importance=2,
    statement="Pony.ai 로보택시는 2026년 6월 말 1,975대이고 연말 3,500대 이상이 목표다. 2분기 로보택시 매출은 1,210만 달러로 691% 늘었다. 광저우·선전에서 운영하고 싱가포르에서 일반 서비스를 시작했다.",
    value=1975, unit="대 (로보택시)", as_of="2026-06", region="CN", definition="Pony.ai 로보택시 차량 수",
    extra={"target": "3,500대 이상 (2026년 말)", "revenue": "1,210만 달러 (+691%)"}, sources=src("pony"), verified=True,
    check_flags=["도시별 완전 무인·유료 여부는 기사에 없음"])
add(id="I6-M-013", type="지표", indicator="I6-T5", importance=2,
    statement="Tesla의 차 안 안전요원 없는 로보택시는 2026년 3월 오스틴에서만 운행되며 4~8대로 추정된다. 오스틴 전체 차량 37~42대 대부분은 안전요원이 타고, 무인 차량도 원격 감독을 받는다.",
    value=8, unit="대 이하 (무감독 추정)", as_of="2026-03", region="US", definition="차 안 안전요원 없이 운행하는 Tesla 로보택시",
    extra={"austin_fleet": "37~42대"}, sources=src("tesla"), verified=True, check_flags=["SNS 목격 기반 추정치 — 회사 공식 수치 아님"])
add(id="I6-M-014", type="지표", indicator="I6-T6", importance=3,
    statement="Waymo 차량이 오스틴에서 정차한 스쿨버스를 지나친 사례가 19건 보고돼 미국 도로교통안전국(NHTSA)이 조사에 들어갔고, Waymo는 2025년 12월 소프트웨어 리콜을 하기로 했다. 부상은 없었다.",
    value=19, unit="건 (스쿨버스 통과)", as_of="2025-12", region="US", definition="자율주행 관련 조사·리콜 원인 사례",
    sources=src("waymo_recall"), verified=True)
add(id="I6-M-015", type="지표", indicator="I6-T7", importance=3,
    statement="서울시는 2026년 11월 상암동에서 누구나 택시 앱으로 부를 수 있는 레벨4 로보택시를 시작한다. 초기에는 안전관리자가 조수석에 탄다. 1월 보도는 3대로 시작해 2027년 10대 이상으로 늘린다고 전했다.",
    value=3, unit="대 (초기 차량)", as_of="2026-06", region="KR", definition="서울 레벨4 로보택시 시범 운행",
    extra={"start": "2026-11", "safety_staff": "조수석 안전관리자", "2027": "10대 이상"}, sources=src("seoul_jun", "seoul_jan"), verified=True,
    check_flags=["차량 수(3대)는 C등급 보도에만 있음 — 확인 필요", "1월 보도는 '무인', 6월 서울시 발표는 '안전관리자 탑승'으로 상충", "요금 부과 여부 미확인"])
add(id="I6-M-016", type="지표", indicator="I6-T8", importance=3,
    statement="Walmart의 미국 드론 배송은 2026년 5월 누적 100만 건을 넘었고, 그중 40%가 직전 한 분기에 나왔다. 4개 주 5개 대도시권 66개 매장에서 Wing·Zipline과 운영하며, Wing과는 2027년까지 270개 매장 이상으로 넓힐 계획이다.",
    value=1000000, unit="건 (누적 드론 배송)", as_of="2026-05", region="US", definition="Walmart 드론 배송 누적 건수",
    extra={"stores": "66곳", "quarter_share": "40%", "wing_target": "270곳 이상 (2027년)"}, sources=src("walmart"), verified=True,
    check_flags=["사업자 발표 기준(자사 집계)"])
add(id="I6-M-017", type="지표", indicator="I6-T3", importance=3,
    statement="Amazon은 물류 현장에 로봇 100만 대를 배치했다. 뉴욕타임스가 입수한 내부 문서에는 2033년까지 미국에서 60만 명 넘는 채용을 로봇으로 대신하고, 운영의 75%를 자동화한다는 목표가 담겼다.",
    value=1000000, unit="대 (물류 로봇)", as_of="2025-07", region="US", definition="Amazon 물류 현장 로봇 배치 대수",
    extra={"avoid_hires_2033": "60만 명 이상", "avoid_hires_2027": "16만 명 이상", "automation_goal": "75%"}, sources=src("amazon_robot", "amazon_nyt"), verified=True,
    check_flags=["내부 문서 목표는 회사가 '일부 팀의 시각'이라며 부인", "로봇 100만 대는 회사 발표(자사 집계)"])
add(id="I6-M-018", type="지표", indicator="I6-T8", importance=2,
    statement="Aurora는 자율주행 트럭 30대 중 10대를 운전자 없이 운행하며, 상업 운행 이후 무인 주행 25만 마일을 넘었다. 대부분 차량에는 트럭 제조사 요구로 관찰자가 탄다.",
    value=10, unit="대 (무인 트럭)", as_of="2026-Q1", region="US", definition="운전자 없이 화물을 나르는 자율주행 트럭",
    extra={"fleet": "30대", "driverless_miles": "25만 마일 이상", "target_2026": "200대 이상"}, sources=src("aurora"), verified=True,
    check_flags=["기사 게재일 미표기(2025년 4분기 실적 이후)", "사업자 발표 기준(자사 집계)"])

# ---------- 사건 (E) ----------
add(id="I6-E-001", type="사건", importance=2, date="2025-09-25", actor="국제로봇연맹",
    statement="IFR이 2024년 산업용 로봇 설치가 54만 2천 대로 10년 전의 두 배를 넘었고, 중국이 54%를 차지했다고 발표했다.", sources=src("ifr25"), verified=True)
add(id="I6-E-002", type="사건", importance=3, date="2025-10-21", actor="Amazon",
    statement="뉴욕타임스가 Amazon이 로봇으로 2033년까지 미국 채용 60만 명 이상을 대신할 계획이라는 내부 문서를 보도했다. Amazon은 일부 팀의 시각이라고 반박했다.", sources=src("amazon_nyt"), verified=True)
add(id="I6-E-003", type="사건", importance=2, date="2025-12-04", actor="Figure AI·BMW",
    statement="Figure AI의 휴머노이드 Figure 02가 BMW 스파턴버그 공장에서 11개월 동안 판금 부품 9만 개를 적재하고(BMW X3 3만 대 이상 생산에 참여) 퇴역했다.", sources=src("figure"), verified=True)
add(id="I6-E-004", type="사건", importance=3, date="2025-12-06", actor="Waymo·NHTSA",
    statement="Waymo가 정차한 스쿨버스를 지나친 사례로 NHTSA 조사를 받은 뒤 소프트웨어 리콜을 하기로 했다.", sources=src("waymo_recall"), verified=True)
add(id="I6-E-005", type="사건", importance=2, date="2026-01-08", actor="중국 공업정보화부",
    statement="중국 공업정보화부가 선진급 스마트공장 7천 곳, 우수급 500곳을 넘었다고 발표했다.", sources=src("miit"), verified=True)
add(id="I6-E-006", type="사건", importance=2, date="2026-01", actor="IDC",
    statement="IDC가 2025년 세계 휴머노이드 출하를 약 1만 8천 대(+508%)로 집계했다.", sources=src("idc"), verified=True, check_flags=["보고서 정확한 발표일은 기사에 없음"])
add(id="I6-E-007", type="사건", importance=2, date="2026-03-31", actor="Tesla",
    statement="Tesla가 오스틴 무감독 로보택시 운행 구역을 넓혔지만 안전요원 없는 차량은 여전히 10대 안팎에 그쳤다.", sources=src("tesla"), verified=True)
add(id="I6-E-008", type="사건", importance=2, date="2026-05-06", actor="국토교통부",
    statement="국토교통부가 자율주행 시범운행지구 지정 권한을 시·도지사로 넘기고, 무인 자율주행차 안전 의무 지침과 운전석 없는 차량의 일반도로 운행 특례를 추진한다고 밝혔다.", sources=src("molit"), verified=True)
add(id="I6-E-009", type="사건", importance=2, date="2026-05-29", actor="Walmart",
    statement="Walmart가 미국 드론 배송 누적 100만 건을 발표했다.", sources=src("walmart"), verified=True)
add(id="I6-E-010", type="사건", importance=2, date="2026-06-22", actor="세계경제포럼",
    statement="세계경제포럼이 등대 공장 16곳을 새로 지정해 네트워크가 238곳이 됐다.", sources=src("wef_lh"), verified=True)
add(id="I6-E-011", type="사건", importance=3, date="2026-06-30", actor="서울시",
    statement="서울시가 2026년 11월 상암동에서 레벨4 로보택시를 시작한다고 밝혔다. 초기에는 안전관리자가 조수석에 탄다.", sources=src("seoul_jun"), verified=True)
add(id="I6-E-012", type="사건", importance=3, date="2026-07-07", actor="Waymo",
    statement="Waymo가 라스베이거스에서 완전 무인 운행을 시작하고 덴버·샌디에이고·탬파를 다음 도시로 발표했다.", sources=src("waymo_jul"), verified=True,
    check_flags=["발표일은 기사(07-08)의 '화요일' 기준 추정"])
add(id="I6-E-013", type="사건", importance=2, date="2026-07-25", actor="현대차그룹",
    xref=["I2-E-001"], statement="현대차그룹이 2028년까지 연 3만 대 로봇 생산 체계를 갖추고, 휴머노이드 아틀라스를 2028년 미국 메타플랜트에서 안전 검증한 뒤 2030년부터 조립 공정에 넓힌다는 계획이 보도됐다.", sources=src("hyundai"), verified=True)
add(id="I6-E-014", type="사건", importance=3, date="2026-08-18", actor="Baidu",
    statement="Baidu가 2분기 실적에서 Apollo Go 운영 도시가 28곳이 됐다고 밝혔다.", sources=src("baidu"), verified=True)
add(id="I6-E-015", type="사건", importance=2, date="2026-08-18", actor="Pony.ai",
    statement="Pony.ai가 2분기 실적에서 로보택시 1,975대, 로보택시 매출 691% 증가를 발표했다.", sources=src("pony"), verified=True)
add(id="I6-E-016", type="사건", importance=2, date="2026-09-01", actor="Waymo",
    statement="Waymo가 덴버·샌디에이고·탬파에서 초대 방식의 유료 무인 운행을 시작해 서비스 도시가 14곳, 차량이 4,000대를 넘었다고 보도됐다.", sources=src("waymo_sep"), verified=False,
    check_flags=["C등급 단독 출처 — 판단 근거로 쓰지 않음. I2-M-004는 Waymo 블로그(10월 8일)의 '9월 15번째 미국 도시 개시'를 기록"], xref=["I2-M-004", "I2-E-003"])
add(id="I6-E-017", type="사건", importance=3, date="2026-09-24", actor="국제로봇연맹",
    statement="IFR이 2025년 산업용 로봇 설치가 60만 대를 넘고 가동 대수가 500만 대가 됐다고 발표했다. 미국이 일본을 제치고 설치 2위가 됐다.", sources=src("ifr26"), verified=True)
add(id="I6-E-018", type="사건", importance=2, date="2026-01-27", actor="서울시",
    statement="서울시가 2026년 하반기 상암에서 세계 세 번째 레벨4 무인 로보택시 실증을 하겠다는 계획이 보도됐다.", sources=src("seoul_jan"), verified=False,
    check_flags=["C등급 단독 출처 — 6월 서울시 발표(안전관리자 탑승)와 상충"])
add(id="I6-E-019", type="사건", importance=2, date="2026-02", actor="Aurora",
    statement="Aurora가 포트워스~피닉스 약 1,000마일 구간에서 운전자 없는 화물 운행을 했다고 밝혔다.", sources=src("aurora"), verified=True,
    check_flags=["정확한 운행일은 기사에 없음(2025년 4분기 실적 이후로 추정)"])

# ---------- 해석 (I) ----------
add(id="I6-I-001", type="해석", importance=3, target="로보택시", direction="강화",
    statement="사람 없이 돌아가는 영역 중 대규모 상용에 들어선 것은 로보택시뿐이다. Waymo는 미국 11개 대도시권에서 약 3,500대로 주당 50만 건 유료 운행을 하고, Baidu는 28개 도시, Pony.ai는 2천 대 가까운 차량을 운영한다.",
    basis=["I6-M-010", "I6-M-011", "I6-M-012"])
add(id="I6-I-002", type="해석", importance=2, target="로보택시 격차", direction="중립",
    statement="로보택시의 대규모 상용은 소수 사업자에 몰려 있다. Waymo가 3,500대를 운행하는 동안 Tesla의 무감독 차량은 4~8대로 추정되고, 발표한 7개 도시 확장은 이뤄지지 않았다.",
    basis=["I6-M-010", "I6-M-013", "I6-E-007"])
add(id="I6-I-003", type="해석", importance=3, target="제조 무인화", direction="중립",
    statement="공장 자동화는 로봇 대수로는 빠르게 늘지만(2025년 60만 대, 가동 500만 대) '완전 무인 공장'은 검증된 사례가 드물다. 등대 공장과 중국 스마트공장 등급은 무인 가동을 기준으로 삼지 않고, 대표 사례인 샤오미도 회사 발표 자동화율 81%에 감독 인력이 남아 있다.",
    basis=["I6-M-002", "I6-M-005", "I6-M-006", "I6-M-007"])
add(id="I6-I-004", type="해석", importance=3, target="중국", direction="강화",
    statement="무인화 설비는 중국이 끌고 있다. 세계 로봇 설치의 59%, 선진급 스마트공장 7천 곳, 휴머노이드 출하에서 Unitree 한 곳이 5,500대로 미국 주요 업체(각 약 150대)를 크게 앞선다.",
    basis=["I6-M-002", "I6-M-006", "I6-M-008", "I6-M-009"])
add(id="I6-I-005", type="해석", importance=3, target="휴머노이드", direction="중립",
    xref=["I2-M-005", "I2-M-012"], statement="휴머노이드는 아직 시범 운영 단계다. 2025년 출하 1만 8천 대의 용도는 오락·연구·데이터 수집이 중심이고, 공장 투입 사례인 Figure 02는 11개월 동안 부품 적재를 하고 퇴역했다. 현대차의 공장 투입도 2028년 안전 검증부터다.",
    basis=["I6-M-008", "I6-E-003", "I6-E-013"])
add(id="I6-I-006", type="해석", importance=3, target="한국", direction="중립",
    statement="한국은 로봇 밀도 세계 1위지만 무인화 확산 속도는 느리다. 로봇 설치는 2년째 3만 대 안팎에서 줄었고, 로보택시는 2026년 11월에야 안전관리자가 탄 채 시작한다. 제도는 시범운행지구 지정 권한 이양처럼 이제 정비 중이다.",
    basis=["I6-M-001", "I6-M-003", "I6-M-015", "I6-E-008"])
add(id="I6-I-007", type="해석", importance=3, target="최대 제약", direction="약화",
    statement="무인화를 가장 크게 막는 것은 안전 검증과 사람 감독 요구다. 선두 Waymo도 스쿨버스 사례로 리콜했고, 한국 로보택시는 안전관리자 탑승으로 시작하며, Aurora 무인 트럭 대부분에는 제조사 요구로 관찰자가 탄다.",
    basis=["I6-M-014", "I6-M-015", "I6-M-018"])
add(id="I6-I-008", type="해석", importance=2, target="물류·배송", direction="강화",
    statement="물류·배송은 무인 운영이 빠르게 늘지만 고용 영향은 해고보다 채용 회피로 나타난다. Amazon은 로봇 100만 대를 배치했고 내부 문서는 60만 명 채용을 대신하는 목표를 담았다. Walmart 드론 배송은 누적 100만 건 중 40%가 한 분기에 나왔다.",
    basis=["I6-M-017", "I6-E-002", "I6-M-016"])

# ---------- 세부 전망 (F) ----------
ON = "2026-10-29"
add(id="I6-F-001", type="전망", importance=3, status="유효", forecast_status="진행 중", made_on=ON,
    statement="Waymo는 2027년 6월 말까지 주당 유료 운행 100만 건 이상을 공식 발표할 것이다.",
    due="2027-06-30", condition="대형 사고로 운행이 중단되지 않을 경우",
    method="Waymo 공식 블로그·발표 또는 주요 언론의 Waymo 인용에서 주당 유료 운행 100만 건 이상 확인",
    reasoning="주당 50만 건을 달성한 뒤 도시와 차량을 빠르게 늘리고 있고, 2026년 말 100만 건을 목표로 잡았다.",
    counter="리콜·규제 조사나 신규 도시의 초기 수요 부족으로 목표가 늦어질 수 있다.",
    basis=["I6-M-010", "I6-E-012", "I6-I-001"], result=None)
add(id="I6-F-002", type="전망", importance=2, status="유효", forecast_status="진행 중", made_on=ON,
    statement="IFR World Robotics 2027에서 2026년 세계 산업용 로봇 설치 중 중국 비중은 55% 이상일 것이다.",
    due="2027-10-31", condition="IFR이 2027년 9~10월 보고서를 낼 경우",
    method="IFR World Robotics 2027 보도자료의 2026년 중국 설치 비중 확인",
    reasoning="중국 비중은 2024년 54%에서 2025년 59%로 커졌고, 스마트공장 육성이 정부 정책으로 이어지고 있다.",
    counter="중국 경기 둔화나 미국 설치 급증(2025년 +12%)으로 비중이 낮아질 수 있다.",
    basis=["I6-M-002", "I6-M-006", "I6-I-004"], result=None)
add(id="I6-F-003", type="전망", importance=3, status="유효", forecast_status="진행 중", made_on=ON,
    statement="2027년 6월 말까지 서울 레벨4 로보택시는 차 안에 안전관리자 없이 일반 승객을 태우는 운행을 시작하지 못할 것이다.",
    due="2027-06-30", condition="없음",
    method="서울시·국토교통부 발표 또는 주요 언론에서 서울 로보택시가 차 안 안전 인력 없이 일반 승객을 태운다는 보도 확인. 확인되면 틀림",
    reasoning="11월 시작부터 안전관리자가 타고, 무인 차량 안전 의무 지침은 아직 추진 단계다.",
    counter="시범 성과가 좋으면 서울시가 2027년 상반기에 안전관리자를 뺄 수 있다.",
    basis=["I6-M-015", "I6-E-008", "I6-I-006"], result=None)
add(id="I6-F-004", type="전망", importance=2, status="유효", forecast_status="진행 중", made_on=ON,
    statement="IDC가 집계하는 2026년 세계 휴머노이드 출하는 4만 대 이상일 것이다.",
    due="2027-04-30", condition="IDC가 같은 기준으로 2026년 집계를 발표할 경우",
    method="IDC 2026년 휴머노이드 출하 집계(보도 포함) 확인. 2027-04-30까지 발표가 없으면 판정 불가",
    reasoning="2025년 출하가 508% 늘어 1만 8천 대였고, 다른 조사사(Smart Analytics Global)는 2026년 상반기에만 약 1만 9,100대를 집계했다(I2-M-012).", xref=["I2-M-012"],
    counter="연구·오락용 수요가 한 번에 몰린 효과일 수 있고, 공장 투입은 아직 시범 단계다.",
    basis=["I6-M-008", "I6-M-009", "I6-I-005"], result=None)
add(id="I6-F-005", type="전망", importance=2, status="유효", forecast_status="진행 중", made_on=ON,
    statement="2027년 6월 말까지 Walmart의 미국 드론 배송 누적 300만 건 이상이 발표될 것이다.",
    due="2027-06-30", condition="Walmart 또는 협력사가 누적 건수를 공개할 경우",
    method="Walmart·Wing·Zipline 발표 또는 주요 언론에서 Walmart 드론 배송 누적 300만 건 이상 확인. 공개가 없으면 판정 불가",
    reasoning="누적 100만 건 중 40%가 한 분기에 나왔고, Wing과 2027년까지 매장을 4배 이상 늘릴 계획이다.",
    counter="새 지역의 허가·소음 민원으로 확장이 늦어지면 분기 증가폭이 정체될 수 있다.",
    basis=["I6-M-016", "I6-E-009", "I6-I-008"], result=None)

add(id="I6-F-101", type="전망", importance=3, status="유효", forecast_status="진행 중", scenario="낙관", made_on=ON,
    statement="2027년 말까지 로보택시가 주요 도시의 일상 교통수단으로 자리 잡고, 휴머노이드가 시범을 넘어 일부 공장 공정에 정규 투입된다. 한국도 안전관리자 없는 로보택시 운행을 시작한다.",
    milestones=[{"by": "2027-04", "text": "2026년 휴머노이드 출하 4만 대 이상"}, {"by": "2027-06", "text": "Waymo 주당 100만 건"}, {"by": "2027-06", "text": "서울 무인 로보택시"}],
    due="2027-12-31", condition="대형 인명 사고가 없을 경우",
    method="세 가지 중 두 가지 이상 충족 시 적중: (1) Waymo 주당 유료 운행 100만 건 이상 발표 (2) IDC 2026년 휴머노이드 출하 4만 대 이상 (3) 한국에서 차 안 안전 인력 없이 일반 승객을 태우는 로보택시 운행 시작",
    basis=["I6-M-010", "I6-M-008", "I6-M-015", "I6-I-001"],
    signposts=[{"id": "I6-F-001", "on_hit": "낙관", "on_miss": "비관"}, {"id": "I6-F-003", "on_hit": "비관", "on_miss": "낙관"},
               {"id": "I6-F-004", "on_hit": "낙관", "on_miss": "비관"}, {"id": "I6-F-005", "on_hit": "낙관"}], result=None)
add(id="I6-F-102", type="전망", importance=3, status="유효", forecast_status="진행 중", scenario="비관", made_on=ON,
    statement="2027년 말까지 무인화는 소수 사업자의 로보택시와 대형 물류센터에 머문다. 사고·리콜로 로보택시 확장이 늦어지고, 휴머노이드는 연구·시범용에 그친다.",
    milestones=[{"by": "2027-04", "text": "휴머노이드 출하 4만 대 미만"}, {"by": "2027-06", "text": "Waymo 주당 100만 건 미달"}, {"by": "2027-12", "text": "로보택시 운행 중단 조치 발생"}],
    due="2027-12-31", condition="없음",
    method="세 가지 중 두 가지 이상 충족 시 적중: (1) 2027-06-30까지 Waymo 주당 100만 건 미발표 (2) IDC 2026년 휴머노이드 출하 4만 대 미만 (3) 2027년 중 미국·중국 규제기관이 주요 로보택시 사업자의 한 도시 이상 운행을 중단시킴",
    basis=["I6-M-014", "I6-M-013", "I6-M-008", "I6-I-007"],
    signposts=[{"id": "I6-F-001", "on_hit": "낙관", "on_miss": "비관"}, {"id": "I6-F-003", "on_hit": "비관", "on_miss": "낙관"},
               {"id": "I6-F-004", "on_hit": "낙관", "on_miss": "비관"}, {"id": "I6-F-002", "on_hit": "비관"}], result=None)

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
    if r["type"] in ("지표", "사건") and r.get("sources") and all(s["grade"] == "C" for s in r["sources"]) and r.get("verified"):
        errs.append(f"{r['id']}: C등급 단독 근거를 확인으로 표시")
    if r["type"] == "해석":
        if len(set(r.get("basis", [])) & facts) < 2: errs.append(f"{r['id']}: 사실 기록 2건 미만")
        if r.get("direction") not in ("강화", "약화", "중립"): errs.append(f"{r['id']}: 방향 값 오류")
    if r["type"] == "전망":
        for f in ("due", "method", "basis"):
            if not r.get(f): errs.append(f"{r['id']}: {f} 없음")
        if len(set(r["basis"]) & facts) < 2: errs.append(f"{r['id']}: 사실 기록 2건 미만")
        if not any(_t.get(b) == "해석" for b in r["basis"]): errs.append(f"{r['id']}: 해석 근거 없음")
        if not ("2027-04-29" <= r["due"] <= "2028-04-29"): errs.append(f"{r['id']}: 마감 6~18개월 밖")
    for sp in r.get("signposts", []):
        if _t.get(sp["id"]) != "전망": errs.append(f"{r['id']}: 판정 신호 {sp['id']}가 세부 전망이 아님")
    if r.get("scenario") and r["scenario"] not in ("낙관", "비관"): errs.append(f"{r['id']}: 시나리오 값 오류")
    for b in r.get("basis", []):
        if b not in ids: errs.append(f"{r['id']}: 존재하지 않는 근거 {b}")
        elif r["type"] in ("해석", "전망") and b in facts and not _v[b]: errs.append(f"{r['id']}: 원문 미확인 기록 {b}을 근거로 씀")
if len(ids) != len(records): errs.append("중복 ID")

with open(Path(__file__).parent / "records.jsonl", "w", encoding="utf-8") as f:
    for r in records: f.write(json.dumps(r, ensure_ascii=False) + "\n")

print("기록 수:", len(records), dict(Counter(r["type"] for r in records)), "출처:", len(SRC))
print("원문 미확인 사실:", [r["id"] for r in records if r["type"] in ("지표", "사건") and not r.get("verified")])
inds = {r.get("indicator") for r in records if r["type"] == "지표" and r.get("verified")}
print("값 채워진 추적 지표:", sorted(inds), f"{len(inds)}/8")
print("검증 오류:", errs or "없음")
sys.exit(1 if errs else 0)

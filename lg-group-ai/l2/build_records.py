"""L2 R1 4유형 기록 생성 + 규칙 검증.
출력: i4/records.jsonl
"""
import json, sys
from pathlib import Path
from collections import Counter

R = "R1"
SRC = {
 "sf_fn": {"url": "https://www.fnnews.com/news/202607241613595892", "publisher": "파이낸셜뉴스", "date": "2026-07-26", "grade": "B"},
 "sf_2024": {"url": "https://www.australianmanufacturing.com.au/lg-integrates-ai-with-66-year-manufacturing-expertise-for-smart-factories", "publisher": "Australian Manufacturing (LG 발표)", "date": "2024-07-22", "grade": "B"},
 "factova": {"url": "https://www.lg.co.kr/media/release/30179", "publisher": "LG 보도자료 (LG CNS)", "date": "2026-05-20", "grade": "A"},
 "pw": {"url": "https://www.etoday.co.kr/news/view/2582268", "publisher": "이투데이 (LG CNS 발표)", "date": "2026-05-07", "grade": "B"},
 "kurly": {"url": "https://zdnet.co.kr/view/?no=20260518100553", "publisher": "ZDNet Korea", "date": "2026-05-18", "grade": "B"},
 "lxp": {"url": "https://www.dailian.co.kr/news/view/1654748/LG-CNSLX%ED%8C%90%ED%86%A0%EC%8A%A4-%EB%AC%BC%EB%A5%98%EC%84%BC%ED%84%B0-%ED%9C%B4%EB%A8%B8%EB%85%B8-2026", "publisher": "데일리안 (LG CNS 발표)", "date": "2026-06-11", "grade": "B"},
 "ces_ceo": {"url": "https://dealsite.co.kr/articles/154677/068020", "publisher": "딜사이트 (CES 2026 간담회)", "date": "2026-01-08", "grade": "B"},
 "cloid": {"url": "https://www.lg.com/us/press-release/lg-cloid-home-robot", "publisher": "LG전자 보도자료", "date": "2026-01-04", "grade": "A"},
 "thinq_on": {"url": "https://www.heraldk.com/article/2025102118250730033", "publisher": "헤럴드경제", "date": "2025-10-21", "grade": "B"},
}
def src(*keys): return [dict(SRC[k], key=k) for k in keys]

base = dict(question="L2", question_version="v1.0", first_seen=R, last_seen=R, status="유효", replaces=None, check_flags=[])
records = []
def add(**kw):
    r = dict(base); r.update(kw); records.append(r)

OWN = "자사 공장 수치 — 외부 고객 성과 아님"
EST = "회사 추정·기대 효과"

# ---------- 지표 (M) ----------
add(id="L2-M-001", type="지표", indicator="L2-T1", importance=3, statement="LG전자 스마트팩토리 솔루션 사업의 외부 수주는 2024년 전담 조직 신설 이후 2년 만에 약 5,000억 원 규모로 늘었다. 2030년 외부 매출을 조 단위로 키우는 것이 목표다.",
    value=5000, unit="억 원 (2년 누적 수주)", as_of="2026-07", region="GLOBAL", definition="LG전자 스마트팩토리 외부 수주", extra={"target_2030": "외부 매출 조 단위", "named_customer": "로지스밸리 인천공항 GDC"},
    sources=src("sf_fn"), verified=True, check_flags=["연도별 수주·매출 미공개", "2030 목표는 회사 목표"])
add(id="L2-M-002", type="지표", indicator="L2-T2", importance=2, statement="LG전자 창원 등대공장은 생산성 17% 향상, 불량 관련 품질 비용 70% 감소, 에너지 효율 30% 향상을 기록했다고 회사가 밝혔다. 회사가 보유한 제조 데이터는 770TB다.",
    value=17, unit="% (생산성 향상)", as_of="2024-07", region="KR", definition="LG전자 자사 등대공장 성과", extra={"quality_cost": "-70%", "energy": "+30%", "data": "770TB"},
    sources=src("sf_2024"), verified=True, check_flags=[OWN, "조사 기간 이전 — 기준선"])
add(id="L2-M-003", type="지표", indicator="L2-T3", importance=3, statement="LG CNS의 공장 운영 AI 'Factova Control'은 국내외 설비 10만 개 이상에 적용됐다. 한 배터리 공장에서는 도입 한 달 만에 합격품 비중이 90%를 넘고 불량 반품 비용이 약 70% 줄었으며, 한 전자 공장에서는 작업 생산성이 약 20% 올랐다.",
    value=10, unit="만 개 이상 (적용 설비)", as_of="2026-05", region="GLOBAL", definition="Factova Control 적용 설비 수와 고객 공장 성과",
    extra={"battery_yield": "90% 이상 (1개월)", "battery_return_cost": "-70%", "electronics_productivity": "+20%"},
    sources=src("factova"), verified=True, check_flags=["고객 공장 이름 비공개"])
add(id="L2-M-004", type="지표", indicator="L2-T4", importance=3, statement="LG CNS의 로봇 학습·운영 플랫폼 PhysicalWorks는 학습 모듈(Forge)로 20곳 넘는 고객과 실증을 진행 중이다. 회사는 로봇 현장 투입 기간이 수개월에서 1~2개월로 줄고, 로봇 100대 규모 운영에서 생산성 15% 이상 향상·운영비 최대 18% 절감을 기대한다고 밝혔다.",
    value=20, unit="곳 이상 (Forge 실증 고객)", as_of="2026-05", region="KR", definition="PhysicalWorks 실증 고객 수와 기대 효과", extra={"deploy_time": "수개월 → 1~2개월", "productivity": "+15% 이상", "opex": "-18%"},
    sources=src("pw"), verified=True, check_flags=[EST])
add(id="L2-M-005", type="지표", indicator="L2-T8", importance=2, statement="LG전자 스마트팩토리 조직은 2024년 이후 2배 넘게 커졌다. 2026년 7월 스마트팩토리솔루션센터가 전무급으로 격상되고 로보틱스사업센터가 새로 생겼다.",
    value=2, unit="배 이상 (조직 규모, 2년)", as_of="2026-07", region="KR", definition="LG전자 스마트팩토리 조직 규모", sources=src("sf_fn"), verified=True)

# ---------- 사건 (E) ----------
add(id="L2-E-001", type="사건", importance=2, statement="LG전자가 생성형 AI 홈 허브 '씽큐 온'을 국내 출시했다. 여러 기기에 걸친 명령을 순서대로 실행하고, 센서로 상황을 판단해 기기를 스스로 작동시킨다.",
    date="2025-10-22", actor="LG전자", sources=src("thinq_on"), verified=True)
add(id="L2-E-002", type="사건", importance=2, statement="LG전자가 CES 2026에서 다섯 손가락으로 집안일을 하는 홈 로봇 'CLOiD'를 공개했다. 가격·출시일은 밝히지 않았다.",
    date="2026-01-04", actor="LG전자", sources=src("cloid"), verified=True)
add(id="L2-E-003", type="사건", importance=3, statement="LG전자 CEO가 CLOiD를 '내년 실험실에서 나와 현장에 투입'하겠다고 밝히고 로봇 사업 체계를 제시했다. 산업용은 로보스타, 상업용은 베어로보틱스, 가정용은 CLOiD가 맡고, 액추에이터 브랜드 '악시움'을 공개했으며, 센서는 LG이노텍·배터리는 LG에너지솔루션·시스템 통합은 LG CNS와 검토한다. 로봇 파운데이션 모델은 외부 협력이 필요하다고 했다.",
    date="2026-01-07", actor="LG전자", sources=src("ces_ceo"), verified=True)
add(id="L2-E-004", type="사건", importance=3, statement="LG CNS가 로봇 학습·운영 플랫폼 PhysicalWorks(Forge·Baton)를 공개하고, 다리형·4족·바퀴형·AMR 로봇 4종의 물류 협업을 시연했다.",
    date="2026-05-07", actor="LG CNS", sources=src("pw"), verified=True)
add(id="L2-E-005", type="사건", importance=2, statement="LG CNS가 컬리 물류센터에서 휴머노이드 실증(PoC)과 물류 자동화 협력 업무협약을 맺었다. 기존 방식 대비 정확도·속도·효율을 측정하며, 정량 목표는 공개되지 않았다.",
    date="2026-05-18", actor="LG CNS·컬리", sources=src("kurly"), verified=True)
add(id="L2-E-006", type="사건", importance=2, statement="LG CNS가 미국 IoT 테크 엑스포에 국내 기업 유일로 참가해 Factova MES·Control로 북미 중소·중견 제조기업 공략을 본격화한다고 밝혔다.",
    date="2026-05-19", actor="LG CNS", sources=src("factova"), verified=True)
add(id="L2-E-007", type="사건", importance=3, statement="LG CNS와 LX판토스가 청라 물류센터에 휴머노이드를 투입하는 업무협약을 맺었다. 셔틀 로봇이 꺼낸 물품을 휴머노이드(LG CNS가 3월 투자한 미국 Dexmate의 바퀴형 모델)가 분류 설비로 옮기며, 하반기에 실증 공간을 만든다.",
    date="2026-06-11", actor="LG CNS·LX판토스", sources=src("lxp"), verified=True)
add(id="L2-E-008", type="사건", importance=2, statement="LG전자가 스마트팩토리솔루션센터를 전무급으로 격상하고 로보틱스사업센터를 신설했다. 물류사 로지스밸리의 인천공항 글로벌배송센터에 LG전자 스마트팩토리 솔루션이 적용된 것으로 알려졌다.",
    date="2026-07", actor="LG전자", sources=src("sf_fn"), verified=True, check_flags=["로지스밸리 적용은 '알려졌다' 수준 보도"])

# ---------- 해석 (I) ----------
add(id="L2-I-001", type="해석", importance=3, target="공장 — 외부 스마트팩토리", direction="강화",
    statement="공장 영역은 '상용 계약' 단계다. LG전자 스마트팩토리 외부 수주가 2년 새 약 5,000억 원이 됐고, 조직도 두 배 넘게 키웠다. 다만 연도별 매출과 고객 대부분은 공개되지 않았고, 공개된 성과 수치는 자사 공장 기준이다.",
    basis=["L2-M-001", "L2-M-005", "L2-M-002"])
add(id="L2-I-002", type="해석", importance=3, target="공장 — 운영 AI", direction="강화",
    statement="공장 운영 AI는 외부 고객 성과가 숫자로 나온 유일한 영역이다. Factova Control은 설비 10만 개 이상에 적용됐고, 배터리 공장에서 한 달 만에 합격품 비중 90% 이상, 전자 공장에서 생산성 20% 향상을 보였다. 고객 이름은 공개되지 않았다.",
    basis=["L2-M-003", "L2-E-006"])
add(id="L2-I-003", type="해석", importance=3, target="물류 로봇·휴머노이드", direction="강화",
    statement="물류 로봇과 휴머노이드는 '외부 실증' 단계다. 컬리·LX판토스와 업무협약을 맺고 PhysicalWorks로 20곳 넘게 실증 중이지만, 상용 계약과 실측 성과는 아직 없다. 공개된 생산성·비용 수치는 회사가 기대하는 값이다.",
    basis=["L2-E-005", "L2-E-007", "L2-M-004"])
add(id="L2-I-004", type="해석", importance=2, target="가전", direction="중립",
    statement="가전에서는 홈 허브가 상용 출시 단계, 홈 로봇은 내부 실증 단계다. 씽큐 온은 상황을 판단해 기기를 스스로 작동시키는 기능으로 출시됐고, CLOiD는 공개됐지만 현장 투입은 다음 해로 잡혔다.",
    basis=["L2-E-001", "L2-E-002", "L2-E-003"])
add(id="L2-I-005", type="해석", importance=3, target="성능 증거의 질", direction="중립",
    statement="성능 수치의 대부분은 자사 공장 측정이거나 회사의 기대 효과다. 외부 고객 현장에서 측정된 수치는 Factova 사례(고객명 비공개) 정도이며, 로봇·휴머노이드의 실측 성과는 아직 공개되지 않았다.",
    basis=["L2-M-002", "L2-M-003", "L2-M-004"])
add(id="L2-I-006", type="해석", importance=2, target="로봇 밸류체인 분업", direction="강화",
    statement="LG는 로봇 밸류체인을 계열사로 나눠 맡는 구조를 만들고 있다. LG전자는 하드웨어와 액추에이터, LG이노텍은 센서, LG에너지솔루션은 배터리, LG CNS는 학습·운영 플랫폼과 통합을 맡는다. 비어 있는 자리는 로봇 파운데이션 모델로, 외부 협력에 기대고 있다.",
    basis=["L2-E-003", "L2-E-004", "L2-E-007"])
add(id="L2-I-007", type="해석", importance=2, target="사업화 의지", direction="강화",
    statement="조직과 투자는 사업화 쪽으로 움직였다. 스마트팩토리 센터를 전무급으로 올리고 로보틱스사업센터를 새로 만들었으며, LG CNS는 휴머노이드 기업 Dexmate에 투자해 LX판토스 실증에 투입한다.",
    basis=["L2-M-005", "L2-E-008", "L2-E-007"])

# ---------- 세부 전망 (F) ----------
add(id="L2-F-001", type="전망", importance=2, status="유효", forecast_status="진행 중",
    statement="LG CNS와 LX판토스는 2026년 말까지 청라 물류센터 휴머노이드 실증 공간 구축을 마쳤다고 발표할 것이다.", due="2026-12-31", condition="없음",
    method="LG CNS 또는 LX판토스 공식 발표 확인", basis=["L2-E-007"], result=None)
add(id="L2-F-002", type="전망", importance=3, status="유효", forecast_status="진행 중",
    statement="2027년 6월 말까지 컬리 또는 LX판토스 휴머노이드 실증의 정량 결과(정확도·속도·처리량)가 공개될 것이다.", due="2027-06-30", condition="없음",
    method="회사 발표 또는 주요 언론 보도 확인", basis=["L2-E-005", "L2-E-007"], result=None)
add(id="L2-F-003", type="전망", importance=3, status="유효", forecast_status="진행 중",
    statement="LG CNS는 2027년 6월 말까지 PhysicalWorks 또는 물류 휴머노이드의 첫 상용 계약을 고객명을 밝혀 발표할 것이다.", due="2027-06-30", condition="없음",
    method="LG CNS 공식 발표 확인", basis=["L2-M-004", "L2-E-004"], result=None)
add(id="L2-F-004", type="전망", importance=2, status="유효", forecast_status="진행 중",
    statement="LG CNS는 2027년 6월 말까지 Factova의 북미 고객 계약을 고객명을 밝혀 발표할 것이다.", due="2027-06-30", condition="없음",
    method="LG CNS 공식 발표 확인", basis=["L2-E-006", "L2-M-003"], result=None)
add(id="L2-F-005", type="전망", importance=2, status="유효", forecast_status="진행 중",
    statement="LG전자는 2027년 6월 말까지 스마트팩토리 솔루션의 외부 고객 신규 계약을 고객명을 밝혀 발표할 것이다.", due="2027-06-30", condition="없음",
    method="LG전자 공식 발표 또는 주요 언론 보도 확인", basis=["L2-M-001"], result=None)
add(id="L2-F-006", type="전망", importance=2, status="유효", forecast_status="진행 중",
    statement="LG전자는 2027년 말까지 CLOiD의 상업 현장(가정 외 시설 포함) 실증 시작을 발표할 것이다.", due="2027-12-31", condition="없음",
    method="LG전자 공식 발표 확인", basis=["L2-E-003"], result=None)

# ---------- 메인 질문 시나리오 ----------
add(id="L2-F-101", type="전망", importance=3, status="유효", forecast_status="진행 중", scenario="낙관",
    statement="2027년 말까지 LG의 피지컬 AI가 외부 고객 현장에서 성과로 확인된다. 물류 휴머노이드·로봇 운영 플랫폼의 상용 계약이 나오고, 외부 고객 기준 성능 수치가 공개되며, CLOiD가 현장에 들어간다.",
    milestones=[
        {"by": "2026-12", "text": "LX판토스 실증 공간 구축 완료"},
        {"by": "2027-06", "text": "휴머노이드 실증 정량 결과 공개, PhysicalWorks 첫 상용 계약"},
        {"by": "2027-12", "text": "CLOiD 현장 실증 시작"}],
    due="2027-12-31", condition="휴머노이드 안전 사고로 실증이 중단되지 않을 경우",
    method="세 가지 중 두 가지 이상 충족 시 적중: (1) PhysicalWorks 또는 물류 휴머노이드 상용 계약(고객명 공개) (2) 외부 고객 현장 기준 성능 수치 공개(고객명 공개) (3) CLOiD 현장 실증 시작 발표",
    basis=["L2-M-004", "L2-E-007", "L2-E-003"],
    signposts=[{"id": "L2-F-001", "on_hit": "낙관"}, {"id": "L2-F-002", "on_hit": "낙관", "on_miss": "비관"},
               {"id": "L2-F-003", "on_hit": "낙관", "on_miss": "비관"}, {"id": "L2-F-004", "on_hit": "낙관"},
               {"id": "L2-F-005", "on_hit": "낙관"}, {"id": "L2-F-006", "on_hit": "낙관", "on_miss": "비관"}], result=None)
add(id="L2-F-102", type="전망", importance=3, status="유효", forecast_status="진행 중", scenario="비관",
    statement="2027년 말까지 로봇·휴머노이드는 실증에 머물고, 공개되는 성과는 여전히 자사 공장 수치와 기대 효과다. 스마트팩토리 수주는 늘지만 외부 고객 성과가 드러나지 않아 차별화가 약하다.",
    milestones=[
        {"by": "2027-06", "text": "휴머노이드 실증 결과 미공개"},
        {"by": "2027-06", "text": "로봇 플랫폼 상용 계약 없음"},
        {"by": "2027-12", "text": "CLOiD 현장 투입 연기"}],
    due="2027-12-31", condition="없음",
    method="낙관 시나리오의 판정 조건 세 가지 중 하나 이하만 충족 시 적중",
    basis=["L2-M-002", "L2-M-004", "L2-E-005"], signposts=[], result=None)

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

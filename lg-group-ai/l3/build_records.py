"""L3 R1 4유형 기록 생성 + 규칙 검증.
출력: i4/records.jsonl
"""
import json, sys
from pathlib import Path
from collections import Counter

R = "R1"
SRC = {
 "lge_ir": {"url": "https://www.lge.co.kr/kr/upload/admin/investment/result/2026_Q2_Earnings%20Release%20of%20LGE_KR.pdf", "publisher": "LG전자 2분기 실적 자료 (IR)", "date": "2026-07-30", "grade": "A"},
 "vs_margin": {"url": "https://www.mt.co.kr/industry/2026/05/26/2026052614464720033", "publisher": "머니투데이 (분기보고서·TechInsights 인용)", "date": "2026-05-26", "grade": "B"},
 "renault": {"url": "https://www.etnews.com/20261006000204", "publisher": "전자신문 (LG전자 발표)", "date": "2026-10-06", "grade": "B"},
 "inno_lidar": {"url": "https://v.daum.net/v/20260413060304293", "publisher": "쿠키뉴스", "date": "2026-04-13", "grade": "B"},
 "inno_ces": {"url": "https://tools.prnewswire.com/en-us/live/20823/release/20260105EN56019", "publisher": "PR Newswire (LG이노텍)", "date": "2026-01-05", "grade": "A"},
 "lgd_auto": {"url": "https://www.mt.co.kr/article/2026082613581788601", "publisher": "머니투데이", "date": "2026-08-26", "grade": "B"},
 "lges_sdv": {"url": "https://www.heraldk.com/article/2026040215280143224", "publisher": "헤럴드경제 (LG에너지솔루션 발표)", "date": "2026-04-02", "grade": "B"},
 "lge_ces": {"url": "https://zdnet.co.kr/view/?no=20251217091749", "publisher": "ZDNet Korea (LG전자 발표)", "date": "2025-12-17", "grade": "B"},
 "nvda_map": {"url": "https://www.thailand-business-news.com/pr-news/lg-teams-with-nvidia-to-shape-the-future-with-m-a-p-mobility-ai-infra-physical-ai", "publisher": "PR Newswire (LG 발표)", "date": "2026-06-08", "grade": "A"},
}
def src(*keys): return [dict(SRC[k], key=k) for k in keys]

base = dict(question="L3", question_version="v1.0", first_seen=R, last_seen=R, status="유효", replaces=None, check_flags=[])
records = []
def add(**kw):
    r = dict(base); r.update(kw); records.append(r)

TARGET = "회사 목표 — 실적 아님"

# ---------- 지표 (M) ----------
add(id="L3-M-001", type="지표", indicator="L3-T1", importance=3, statement="LG전자 VS(전장)사업본부의 2026년 2분기 매출은 3조 259억 원(+6.2%), 영업이익은 1,912억 원으로 2분기 기준 최대였다. 영업이익률은 6.3%다. 회사는 전기차 수요 정체로 완성차 수요 회복이 제한적이지만 수주잔고를 바탕으로 매출 성장을 이어가겠다고 밝혔다.",
    value=30259, unit="억 원 (VS 2분기 매출)", as_of="2026-Q2", region="GLOBAL", definition="LG전자 VS사업본부 분기 실적", extra={"op": "1,912억 원", "opm": "6.3%", "yoy": "+6.2%"},
    sources=src("lge_ir"), verified=True, check_flags=["수주잔고 금액은 공개되지 않음"])
add(id="L3-M-002", type="지표", indicator="L3-T2", importance=2, statement="LG전자 VS사업본부의 2026년 1분기 영업이익률은 6.9%로 출범 후 처음 6%대에 올랐다. 보쉬 모빌리티 부문(1.8%)의 3배를 넘고 콘티넨탈(3.9%)보다 높다.",
    value=6.9, unit="% (VS 1분기 영업이익률)", as_of="2026-Q1", region="GLOBAL", definition="VS 영업이익률과 글로벌 Tier 1 비교", extra={"bosch": "1.8%", "continental": "3.9%"},
    sources=src("vs_margin"), verified=True, check_flags=["경쟁사 수치는 전년 연간 기준"])
add(id="L3-M-003", type="지표", indicator="L3-T3", importance=2, statement="LG전자는 2025년 4분기 글로벌 텔레매틱스 시장 점유율 23%로 1위였다.",
    value=23, unit="% (텔레매틱스 점유율)", as_of="2025-Q4", region="GLOBAL", definition="글로벌 차량 텔레매틱스 점유율 (TechInsights)", sources=src("vs_margin"), verified=True)
add(id="L3-M-004", type="지표", indicator="L3-T5", importance=2, statement="LG이노텍은 2030년 자율주행 센싱 매출 약 2조 원, 모빌리티솔루션 전체 약 5조 원을 목표로 한다. Aeva와 함께 개발하는 초슬림·초장거리 라이다 모듈은 2028년 글로벌 완성차 탑재가 목표이며, 고객명은 공개되지 않았다.",
    value=2, unit="조 원 (2030 센싱 매출 목표)", as_of="2026-04", region="GLOBAL", definition="LG이노텍 자율주행 센싱 매출 목표", extra={"mobility_target": "약 5조 원", "lidar_sop": "2028"},
    sources=src("inno_lidar"), verified=True, check_flags=[TARGET, "라이다 고객명 비공개"])
add(id="L3-M-005", type="지표", indicator="L3-T6", importance=2, statement="LG디스플레이는 2025년 글로벌 차량용 OLED 매출 점유율 15.9%로 2위였다(1위 삼성디스플레이 70.2%). 글로벌 완성차 10여 곳에 OLED 패널을 공급한다.",
    value=15.9, unit="% (차량용 OLED 점유율)", as_of="2025", region="GLOBAL", definition="차량용 OLED 매출 점유율", extra={"samsung": "70.2%", "oem_count": "10여 곳"},
    sources=src("lgd_auto"), verified=True, check_flags=["고객사 이름 비공개"])
add(id="L3-M-006", type="지표", indicator="L3-T7", importance=2, statement="LG에너지솔루션은 GM 주도의 차량 소프트웨어 마켓 SDVerse에 배터리 기업 최초로 합류해 배터리 SW 5종(플랫폼 SW, 안전 진단 보정, 셀 상태 진단, 수명 시뮬레이터, 열화 저감)을 올렸다.",
    value=5, unit="종 (등록 배터리 SW)", as_of="2026-04", region="GLOBAL", definition="SDVerse 등록 배터리 SW 수", sources=src("lges_sdv"), verified=True, check_flags=["고객·수익 모델 미공개"])

# ---------- 사건 (E) ----------
add(id="L3-E-001", type="사건", importance=2, statement="LG전자가 CES 2026용 AI 차량 솔루션(투명 OLED 앞유리, 시선 분석 비전 AI, 뒷좌석 AI 큐레이션)과 완성차용 온디바이스 'AI 캐빈 플랫폼'을 발표했다. 인캐빈 센싱 등은 글로벌 완성차와 양산을 논의 중이며 몇 년 안에 상용화하겠다고 했다.",
    date="2025-12-17", actor="LG전자", sources=src("lge_ces"), verified=True)
add(id="L3-E-002", type="사건", importance=2, statement="LG이노텍이 CES 2026에서 자율주행 부품 16종과 전기차 솔루션 15종(Aeva 공동 라이다, 5G NTN 모듈, 800V 무선 BMS 등)을 공개했다. 고객·수주는 밝히지 않았다.",
    date="2026-01-05", actor="LG이노텍", sources=src("inno_ces"), verified=True)
add(id="L3-E-003", type="사건", importance=2, statement="LG에너지솔루션이 GM·Magna·Wipro가 세운 차량 SW 마켓 SDVerse에 배터리 기업 최초로 합류했다.",
    date="2026-04-03", actor="LG에너지솔루션", sources=src("lges_sdv"), verified=True)
add(id="L3-E-004", type="사건", importance=3, statement="LG와 NVIDIA가 M.A.P. 협력을 발표했다. 모빌리티에서는 LG전자가 인포테인먼트 역량에 NVIDIA DRIVE Hyperion을 결합해 차세대 ADAS를 개발하고, LG이노텍이 DRIVE Hyperion용 통신·센싱·조명 부품 개발을 넓힌다.",
    date="2026-06-08", actor="LG·NVIDIA", sources=src("nvda_map"), verified=True)
add(id="L3-E-005", type="사건", importance=2, statement="LG전자 VS사업본부가 2분기 기준 최대 영업이익(1,912억 원)을 냈다.",
    date="2026-07-30", actor="LG전자", sources=src("lge_ir"), verified=True)
add(id="L3-E-006", type="사건", importance=3, statement="LG전자가 르노그룹의 '유럽 첫 상용 SDV' New Trafic E-Tech Electric에 계기판과 인포테인먼트를 하나로 통합 제어하는 콕핏 솔루션을 공급한다고 발표했다. 규모·물량은 비공개다.",
    date="2026-10-06", actor="LG전자·르노", sources=src("renault"), verified=True)

# ---------- 해석 (I) ----------
add(id="L3-I-001", type="해석", importance=3, target="공급 범위 확대", direction="강화",
    statement="고객과 차종을 밝힌 AI·SDV 수주는 르노 한 건이다. 계기판과 인포테인먼트를 통합 제어하는 콕핏을 '유럽 첫 상용 SDV'에 공급하는 것으로, LG전자가 부품 공급사에서 통합 솔루션 공급사로 넓어지는 첫 공개 사례다.",
    basis=["L3-E-006"])
add(id="L3-I-002", type="해석", importance=3, target="수익성", direction="강화",
    statement="수익 기회는 매출보다 이익률에서 먼저 드러난다. VS 매출 성장은 6%대지만 영업이익률은 6~7%로 보쉬 모빌리티의 3배를 넘는다. 통합 콕핏처럼 공급 범위가 넓어지면 이익률을 더 끌어올릴 여지가 있다.",
    basis=["L3-M-001", "L3-M-002", "L3-E-005"])
add(id="L3-I-003", type="해석", importance=2, target="이미 양산 중인 강점", direction="중립",
    statement="양산 적용 단계에 있는 것은 AI 이전부터의 강점이다. 텔레매틱스는 점유율 23%로 1위, 차량용 OLED는 15.9%로 2위이며 완성차 10여 곳에 공급한다. 이 기반 위에 AI 기능을 얹는 구조다.",
    basis=["L3-M-003", "L3-M-005"])
add(id="L3-I-004", type="해석", importance=3, target="AI 고유 영역", direction="중립",
    statement="AI 고유 영역(AI 캐빈, ADAS, 라이다 센싱)은 아직 콘셉트이거나 고객명 없는 수주 단계다. AI 캐빈 기능은 '몇 년 안에 상용화', 라이다는 2028년 탑재가 목표다. AI에서 나오는 수익은 2028년 전후부터 확인될 것이다.",
    basis=["L3-E-001", "L3-M-004", "L3-E-002"])
add(id="L3-I-005", type="해석", importance=2, target="배터리 SW", direction="강화",
    statement="배터리 SW는 판매 채널을 먼저 확보했다. LG에너지솔루션은 GM 주도 마켓에 SW 5종을 올렸지만 고객과 수익 모델은 아직 공개되지 않았다. 셀 공급사가 소프트웨어로 수익을 내는 구조는 실험 단계다.",
    basis=["L3-M-006", "L3-E-003"])
add(id="L3-I-006", type="해석", importance=2, target="ADAS 진입", direction="강화",
    statement="NVIDIA 협력은 LG전자가 인포테인먼트에서 ADAS로 공급 범위를 넓히는 통로다. 인포테인먼트 역량과 DRIVE Hyperion을 결합한 ADAS를 개발하고, LG이노텍이 같은 플랫폼용 센싱·통신 부품을 맞춘다.",
    basis=["L3-E-004"])
add(id="L3-I-007", type="해석", importance=2, target="시장 역풍", direction="약화",
    statement="전기차 수요 정체는 매출 확대의 제약이다. LG전자는 완성차 수요 회복이 당분간 제한적일 것으로 봤고, VS 2분기 매출은 전 분기보다 1.3% 줄었다.",
    basis=["L3-M-001"])

# ---------- 세부 전망 (F) ----------
add(id="L3-F-001", type="전망", importance=2, status="유효", forecast_status="진행 중",
    statement="LG전자 VS사업본부의 2026년 3분기 매출은 전년보다 늘고, 영업이익률은 5% 이상일 것이다.", due="2026-10-31", condition="없음",
    method="LG전자 2026년 3분기 실적 확인", basis=["L3-M-001", "L3-M-002"], result=None)
add(id="L3-F-002", type="전망", importance=3, status="유효", forecast_status="진행 중",
    statement="LG전자는 2027년 6월 말까지 르노 외 완성차의 통합 콕핏·SDV 수주를 고객명을 밝혀 발표할 것이다.", due="2027-06-30", condition="없음",
    method="LG전자 공식 발표 또는 주요 언론 보도 확인", basis=["L3-E-006"], result=None)
add(id="L3-F-003", type="전망", importance=3, status="유효", forecast_status="진행 중",
    statement="LG전자는 2027년 말까지 DRIVE Hyperion 기반 ADAS 수주를 고객명을 밝혀 발표할 것이다.", due="2027-12-31", condition="없음",
    method="LG전자 공식 발표 확인", basis=["L3-E-004"], result=None)
add(id="L3-F-004", type="전망", importance=2, status="유효", forecast_status="진행 중",
    statement="LG이노텍은 2027년 6월 말까지 라이다 또는 AD/ADAS 센싱 수주를 고객명을 밝혀 발표할 것이다.", due="2027-06-30", condition="없음",
    method="LG이노텍 공식 발표 확인", basis=["L3-M-004", "L3-E-002"], result=None)
add(id="L3-F-005", type="전망", importance=2, status="유효", forecast_status="진행 중",
    statement="LG에너지솔루션은 2027년 6월 말까지 배터리 SW(BMS·BMTS·SDVerse 상품)의 완성차 고객을 공개할 것이다.", due="2027-06-30", condition="없음",
    method="LG에너지솔루션 공식 발표 확인", basis=["L3-M-006"], result=None)
add(id="L3-F-006", type="전망", importance=2, status="유효", forecast_status="진행 중",
    statement="LG디스플레이의 2026년 차량용 OLED 점유율은 15% 이상을 유지할 것이다.", due="2027-04-30", condition="시장조사 기관 집계가 발표될 경우",
    method="Omdia·UBI리서치 등 2026년 차량용 OLED 점유율 확인", basis=["L3-M-005"], result=None)

# ---------- 메인 질문 시나리오 ----------
add(id="L3-F-101", type="전망", importance=3, status="유효", forecast_status="진행 중", scenario="낙관",
    statement="2027년 말까지 LG의 공급 범위가 부품에서 통합 콕핏·ADAS로 넓어진다. 고객명을 밝힌 통합 콕핏·SDV 수주가 두 곳 이상이 되고, ADAS 또는 라이다 수주가 고객명과 함께 나오며, VS 이익률은 6% 이상을 지킨다.",
    milestones=[
        {"by": "2026-10", "text": "VS 3분기 이익률 5% 이상"},
        {"by": "2027-06", "text": "르노 외 통합 콕핏 수주, 라이다 수주 고객 공개"},
        {"by": "2027-12", "text": "DRIVE Hyperion 기반 ADAS 수주"}],
    due="2027-12-31", condition="전기차 수요가 더 꺾이지 않을 경우",
    method="세 가지 중 두 가지 이상 충족 시 적중: (1) 고객명 공개 통합 콕핏·SDV 수주 2곳 이상(르노 포함) (2) ADAS 또는 라이다 수주 고객명 공개 (3) VS 2027년 연간 영업이익률 6% 이상",
    basis=["L3-E-006", "L3-M-002", "L3-E-004"],
    signposts=[{"id": "L3-F-001", "on_hit": "낙관", "on_miss": "비관"}, {"id": "L3-F-002", "on_hit": "낙관", "on_miss": "비관"},
               {"id": "L3-F-003", "on_hit": "낙관"}, {"id": "L3-F-004", "on_hit": "낙관"},
               {"id": "L3-F-005", "on_hit": "낙관"}, {"id": "L3-F-006", "on_hit": "낙관", "on_miss": "비관"}], result=None)
add(id="L3-F-102", type="전망", importance=3, status="유효", forecast_status="진행 중", scenario="비관",
    statement="2027년 말까지 통합 수주는 르노 한 건에 머물고, AI 캐빈·ADAS·라이다는 콘셉트와 개발 단계에 남는다. 전기차 수요 정체로 매출이 정체되고, 완성차의 자체 OS 강화로 LG의 역할이 부품 공급사로 좁아진다.",
    milestones=[
        {"by": "2027-06", "text": "추가 통합 수주 미발표"},
        {"by": "2027-06", "text": "라이다·배터리 SW 고객 미공개"},
        {"by": "2027-12", "text": "VS 매출 정체"}],
    due="2027-12-31", condition="없음",
    method="낙관 시나리오의 판정 조건 세 가지 중 하나 이하만 충족 시 적중",
    basis=["L3-M-001", "L3-M-004", "L3-M-006"], signposts=[], result=None)

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

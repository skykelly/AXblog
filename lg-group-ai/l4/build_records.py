"""L4 R1 4유형 기록 생성 + 규칙 검증.
출력: i4/records.jsonl
"""
import json, sys
from pathlib import Path
from collections import Counter

R = "R1"
SRC = {
 "lge_fair": {"url": "https://v.daum.net/v/20260527175602742", "publisher": "다음 뉴스 (AX Fair 2026 현장)", "date": "2026-05-27", "grade": "B"},
 "lgd_ax": {"url": "https://www.ajunews.com/view/20250805141250999", "publisher": "아주경제 (LG디스플레이 AX 세미나)", "date": "2025-08-05", "grade": "B"},
 "lges_ax": {"url": "https://v.daum.net/v/20260427104536341", "publisher": "다음 뉴스", "date": "2026-04-27", "grade": "B"},
 "lgchem_ax": {"url": "https://ceoscoredaily.com/page/view/2026052809581976650", "publisher": "CEO스코어데일리 (LG화학 발표)", "date": "2026-05-28", "grade": "B"},
 "cns_q1": {"url": "https://byline.network/2026/04/30-525/", "publisher": "바이라인네트워크 (LG CNS 1분기 실적)", "date": "2026-04-30", "grade": "B"},
 "cns_h1": {"url": "https://www.thelec.kr/news/articleView.html?idxno=62708", "publisher": "디일렉 (LG CNS 반기보고서)", "date": "2026-09-23", "grade": "B"},
 "palantir": {"url": "https://byline.network/2026/03/12-548/", "publisher": "바이라인네트워크 (LG CNS 발표)", "date": "2026-03-12", "grade": "B"},
 "claude": {"url": "https://view.asiae.co.kr/article/2026060908300307384", "publisher": "아시아경제 (LG CNS 발표)", "date": "2026-06-09", "grade": "B"},
}
def src(*keys): return [dict(SRC[k], key=k) for k in keys]

base = dict(question="L4", question_version="v1.0", first_seen=R, last_seen=R, status="유효", replaces=None, check_flags=[])
records = []
def add(**kw):
    r = dict(base); r.update(kw); records.append(r)

TARGET = "목표치 — 결과 아님"

# ---------- 지표 (M) ----------
add(id="L4-M-001", type="지표", indicator="L4-T1", importance=3, statement="LG전자 사내 AX 플랫폼 LGenie의 월간 사용자는 약 3만 명이다.",
    value=3, unit="만 명 (월간 사용자)", as_of="2026-05", region="KR", definition="LG전자 사내 AI 플랫폼 월간 활성 사용자", sources=src("lge_fair"), verified=True, check_flags=["행사 발표 수치, 사용률 미공개"])
add(id="L4-M-002", type="지표", indicator="L4-T2", importance=3, statement="LG전자가 지난해 개발한 업무 AI 에이전트 96개 가운데 지금도 쓰이는 것은 46개로 절반이 안 된다. 기술(OCR·비전 AI)부터 시작해 쓸 곳을 찾은 경우가 실패했고, 현업의 반복 비효율에서 출발한 경우가 성공했다.",
    value=48, unit="% (에이전트 생존율, 46/96)", as_of="2026-05", region="KR", definition="개발한 업무 에이전트 중 계속 쓰이는 비율", extra={"built": "96개", "alive": "46개", "lgenie_agents": "약 125개 운영"},
    sources=src("lge_fair"), verified=True, check_flags=["46개와 LGenie 운영 125개의 관계는 기사에 설명되지 않음"])
add(id="L4-M-003", type="지표", indicator="L4-T3", importance=2, statement="LG에너지솔루션은 2028년까지 AX로 전사 생산성을 50% 개선하겠다고 밝혔다. 연초의 '2030년까지 30%' 목표를 앞당기고 높인 것이다. LG디스플레이는 3년 안에 업무 생산성 30% 이상 향상이 목표다.",
    value=50, unit="% (엔솔 2028 생산성 목표)", as_of="2026-04", region="KR", definition="계열사 AX 생산성 목표", extra={"lgd_target": "3년 내 30% 이상"},
    sources=src("lges_ax", "lgd_ax"), verified=True, check_flags=[TARGET])
add(id="L4-M-004", type="지표", indicator="L4-T4", importance=3, statement="LG디스플레이는 AI로 이형 디스플레이 설계 기간을 한 달에서 8시간으로, 품질 개선 기간을 평균 3주에서 2일로 줄였다. OLED AI 생산 체계로 연 2,000억 원 이상의 원가 효과를 보고, 사내 AI 비서 Hi-D 도입 후 일일 업무 생산성이 약 10% 올랐다고 밝혔다.",
    value=2000, unit="억 원 이상 (연간 원가 효과)", as_of="2025-08", region="KR", definition="LG디스플레이 AX 결과치", extra={"design": "30일 → 8시간", "quality": "3주 → 2일", "hid": "+10%"},
    sources=src("lgd_ax"), verified=True, check_flags=["조사 기간 이전 발표 — 기준선"])
add(id="L4-M-005", type="지표", indicator="L4-T5", importance=2, statement="LG에너지솔루션이 LG AI연구원과 만든 리튬 가격 예측 모델은 정확도 90% 이상으로 알려졌다. ESS 안전진단 체계는 배터리 셀 100만 개 이상의 데이터를 학습했고, 500개 이상 ESS 사이트에서 연 100TB 넘는 데이터를 분석한다.",
    value=90, unit="% 이상 (리튬 가격 예측 정확도)", as_of="2026-04", region="GLOBAL", definition="AI 의사결정 품질 지표", extra={"ess_cells": "100만 개 이상", "ess_sites": "500곳 이상"},
    sources=src("lges_ax"), verified=True, check_flags=["'알려졌다' 수준 — 측정 방법 미공개"])
add(id="L4-M-006", type="지표", indicator="L4-T6", importance=2, statement="LG화학의 AX 교육 이수자가 3,000명을 넘었다. 지난 반년간 사무직의 절반이 교육을 마쳤고, CEO를 포함한 리더 약 1,000명이 먼저 교육받았다. '1인 1에이전트' 방식으로 개인 업무용 AI 에이전트를 만든다.",
    value=3000, unit="명 이상 (AX 교육 이수)", as_of="2026-05", region="KR", definition="LG화학 AX 교육 이수 인원", extra={"office_share": "사무직 절반", "leaders": "약 1,000명"},
    sources=src("lgchem_ax"), verified=True, check_flags=["시간 절감 등 결과치 미공개"])
add(id="L4-M-007", type="지표", indicator="L4-T7", importance=3, statement="LG CNS의 2026년 상반기 AI·클라우드 매출은 1조 6,714억 원으로 전체 매출의 약 59%다. 대외 매출 비중은 51.1%다.",
    value=16714, unit="억 원 (상반기 AI·클라우드 매출)", as_of="2026-H1", region="KR", definition="LG CNS AI·클라우드 매출", extra={"share": "약 59%", "external_share": "51.1%", "yoy": "+5.1%"},
    sources=src("cns_h1"), verified=True)
add(id="L4-M-008", type="지표", indicator="L4-T8", importance=2, statement="LG CNS가 2월부터 공급하는 ChatGPT Enterprise는 1분기 기준 약 10곳의 고객이 계약했다.",
    value=10, unit="곳 (ChatGPT Enterprise 고객)", as_of="2026-04", region="KR", definition="LG CNS 재판매 AI 플랫폼 고객 수", sources=src("cns_q1"), verified=True, check_flags=["고객명·성과 미공개"])

# ---------- 사건 (E) ----------
add(id="L4-E-001", type="사건", importance=2, statement="LG디스플레이가 AX 성과(설계 30일→8시간, 품질 개선 3주→2일, 연 2,000억 원 원가 효과)를 공개하고 3년 내 생산성 30% 목표를 밝혔다.",
    date="2025-08-05", actor="LG디스플레이", sources=src("lgd_ax"), verified=True, check_flags=["조사 기간 이전 — 기준선"])
add(id="L4-E-002", type="사건", importance=3, statement="LG CNS가 Palantir와 전략적 파트너십을 맺었다. LG 계열사 한 곳의 품질 관리 영역 PoC를 마친 뒤 본 계약으로 이어졌고, 전방배치 엔지니어링(FDE) 조직을 만들어 LG그룹부터 적용한 뒤 외부로 넓힌다.",
    date="2026-03-12", actor="LG CNS·Palantir", sources=src("palantir"), verified=True, check_flags=["계약 규모 미공개"])
add(id="L4-E-003", type="사건", importance=2, statement="LG에너지솔루션 CEO가 AX로 2028년까지 생산성 50% 개선 목표를 밝히고, 매월 CEO가 주재하는 AI 거버넌스 위원회를 운영한다고 했다.",
    date="2026-04-13", actor="LG에너지솔루션", sources=src("lges_ax"), verified=True)
add(id="L4-E-004", type="사건", importance=2, statement="LG CNS가 1분기 실적에서 AI·클라우드 매출 7,654억 원(전체의 약 58%)과 ChatGPT Enterprise 고객 약 10곳을 밝혔다.",
    date="2026-04-30", actor="LG CNS", sources=src("cns_q1"), verified=True)
add(id="L4-E-005", type="사건", importance=3, statement="LG전자가 AX Fair 2026에서 지난해 만든 업무 에이전트 96개 중 46개만 살아남았다고 공개했다. '기술보다 현업의 문제를 먼저 정의하는 것'이 AX의 핵심이라고 했다.",
    date="2026-05-27", actor="LG전자", sources=src("lge_fair"), verified=True)
add(id="L4-E-006", type="사건", importance=2, statement="LG화학이 AX 교육 이수자 3,000명 돌파와 '1인 1에이전트' 방식을 발표했다.",
    date="2026-05-28", actor="LG화학", sources=src("lgchem_ax"), verified=True)
add(id="L4-E-007", type="사건", importance=3, statement="LG CNS가 Anthropic과 Claude Enterprise 도입 계약을 맺었다. LG CNS 전 직원이 쓰고, LG그룹 전 계열사로 적용할 수 있는 통합 계약이며, 외부 기업 도입도 지원한다.",
    date="2026-06-09", actor="LG CNS·Anthropic", sources=src("claude"), verified=True, check_flags=["계약 규모·사용자 수 미공개"])
add(id="L4-E-008", type="사건", importance=2, statement="LG CNS 반기보고서에서 상반기 AI·클라우드 매출 1조 6,714억 원(약 59%)이 확인됐다.",
    date="2026-09-23", actor="LG CNS", sources=src("cns_h1"), verified=True)

# ---------- 해석 (I) ----------
add(id="L4-I-001", type="해석", importance=3, target="계열사별 AX 단계", direction="중립",
    statement="계열사마다 AX 단계가 다르다. LG디스플레이와 LG에너지솔루션은 업무 단위 성과 공개, LG전자는 업무 적용(LGenie 월 3만 명), LG화학과 LG CNS는 교육·도구 배포 단계다. LG CNS는 사내 성과 대신 외부 사업화(AI·클라우드 매출 59%)가 앞서 있다.",
    basis=["L4-M-007", "L4-M-004", "L4-M-005", "L4-M-001", "L4-M-006"])
add(id="L4-I-002", type="해석", importance=3, target="목표치와 결과치", direction="중립",
    statement="목표는 전사 단위인데 결과는 업무 단위다. LG에너지솔루션 50%, LG디스플레이 30% 같은 전사 생산성 목표에 대응하는 전사 결과치는 아직 어느 계열사도 공개하지 않았다. 공개된 결과는 설계·품질·가격 예측 같은 개별 업무의 개선이다.",
    basis=["L4-M-003", "L4-M-004", "L4-M-005"])
add(id="L4-I-003", type="해석", importance=3, target="에이전트 생존율", direction="중립",
    statement="업무 에이전트의 절반은 살아남지 못한다. LG전자 사례에서 96개 중 46개만 남았고, 기술에서 출발한 에이전트가 사라졌다. AX의 실행 체계는 에이전트를 많이 만드는 것이 아니라 현업 문제를 먼저 정의하는 방식으로 바뀌고 있다.",
    basis=["L4-M-002", "L4-E-005"])
add(id="L4-I-004", type="해석", importance=3, target="외부 사업화 경로", direction="강화",
    statement="그룹 내부가 외부 AX 사업의 시험장 역할을 한다. Palantir 협력은 LG 계열사 품질 관리 PoC를 거쳐 본 계약이 됐고, Claude Enterprise도 그룹 적용 뒤 외부로 넓힌다. LG CNS는 이 경로로 AI·클라우드 매출을 전체의 59%까지 키웠다.",
    basis=["L4-E-002", "L4-E-007", "L4-M-007"])
add(id="L4-I-005", type="해석", importance=2, target="외부 플랫폼 조합", direction="중립",
    statement="LG의 AX는 여러 외부 플랫폼을 조합한다. 데이터 통합·의사결정은 Palantir, 그룹 통합 업무 AI는 Anthropic Claude, 외부 재판매는 OpenAI ChatGPT Enterprise(고객 약 10곳)를 쓴다. 자체 모델 EXAONE과의 역할 분담은 공개되지 않았다.",
    basis=["L4-E-002", "L4-E-007", "L4-M-008"])
add(id="L4-I-006", type="해석", importance=2, target="의사결정 품질", direction="강화",
    statement="AI가 업무 시간 단축을 넘어 의사결정 품질에도 쓰인다. LG에너지솔루션의 리튬 가격 예측은 정확도 90% 이상으로 알려졌고, ESS 안전진단은 셀 100만 개·사이트 500곳의 데이터를 쓴다. CEO가 매월 AI 거버넌스 위원회를 주재한다.",
    basis=["L4-M-005", "L4-E-003"])
add(id="L4-I-007", type="해석", importance=2, target="확산", direction="강화",
    statement="사용과 교육은 넓게 퍼지고 있다. LG전자 LGenie는 월 3만 명이 쓰고, LG화학은 반년 만에 사무직 절반이 AX 교육을 마쳤다. 다만 사용률과 시간 절감 같은 결과치는 공개되지 않았다.",
    basis=["L4-M-001", "L4-M-006"])

# ---------- 세부 전망 (F) ----------
add(id="L4-F-001", type="전망", importance=2, status="유효", forecast_status="진행 중",
    statement="LG CNS의 2026년 연간 AI·클라우드 매출 비중은 55% 이상일 것이다.", due="2027-03-31", condition="없음",
    method="LG CNS 2026년 사업보고서 또는 4분기 실적 확인", basis=["L4-M-007"], result=None)
add(id="L4-F-002", type="전망", importance=3, status="유효", forecast_status="진행 중",
    statement="LG CNS는 2027년 6월 말까지 Palantir 기반 AX 사업의 LG 계열사 외 고객 계약을 발표할 것이다.", due="2027-06-30", condition="없음",
    method="LG CNS 공식 발표 확인", basis=["L4-E-002"], result=None)
add(id="L4-F-003", type="전망", importance=2, status="유효", forecast_status="진행 중",
    statement="2026년 말까지 LG CNS 외 LG 계열사 한 곳 이상이 Claude 전사 도입을 발표할 것이다.", due="2026-12-31", condition="없음",
    method="계열사 공식 발표 또는 주요 언론 보도 확인", basis=["L4-E-007"], result=None)
add(id="L4-F-004", type="전망", importance=3, status="유효", forecast_status="진행 중",
    statement="LG에너지솔루션은 2027년 3월 말까지 2026년 AX 생산성 개선 실적치(%)를 공개할 것이다.", due="2027-03-31", condition="없음",
    method="LG에너지솔루션 실적 발표·공식 발표 확인", basis=["L4-M-003", "L4-E-003"], result=None)
add(id="L4-F-005", type="전망", importance=2, status="유효", forecast_status="진행 중",
    statement="LG전자는 2027년 6월 말까지 AX로 인한 전사 생산성 개선 결과치(%)를 공개할 것이다.", due="2027-06-30", condition="없음",
    method="LG전자 공식 발표 또는 AX 행사 발표 확인", basis=["L4-M-001", "L4-M-002"], result=None)
add(id="L4-F-006", type="전망", importance=2, status="유효", forecast_status="진행 중",
    statement="LG화학은 2026년 말까지 사무직 전체의 AX 교육 이수를 발표할 것이다.", due="2026-12-31", condition="없음",
    method="LG화학 공식 발표 확인", basis=["L4-M-006"], result=None)

# ---------- 메인 질문 시나리오 ----------
add(id="L4-F-101", type="전망", importance=3, status="유효", forecast_status="진행 중", scenario="낙관",
    statement="2027년 말까지 LG의 AX가 목표에서 결과로 넘어간다. 두 곳 이상 계열사가 전사 생산성 개선 결과치를 공개하고, LG CNS가 그룹에서 검증한 Palantir·Claude 기반 AX를 외부 고객에 팔며, AI·클라우드 매출 비중이 60%를 넘는다.",
    milestones=[
        {"by": "2026-12", "text": "다른 계열사 Claude 전사 도입"},
        {"by": "2027-03", "text": "엔솔 2026 생산성 실적치 공개"},
        {"by": "2027-06", "text": "Palantir 기반 외부 고객 계약"}],
    due="2027-12-31", condition="없음",
    method="세 가지 중 두 가지 이상 충족 시 적중: (1) 두 곳 이상 계열사가 전사 생산성 개선 결과치(%) 공개 (2) LG CNS의 Palantir 또는 Claude 기반 외부 고객 계약 공개 (3) LG CNS 2027년 AI·클라우드 매출 비중 60% 이상",
    basis=["L4-M-003", "L4-E-002", "L4-M-007"],
    signposts=[{"id": "L4-F-001", "on_hit": "낙관", "on_miss": "비관"}, {"id": "L4-F-002", "on_hit": "낙관", "on_miss": "비관"},
               {"id": "L4-F-003", "on_hit": "낙관"}, {"id": "L4-F-004", "on_hit": "낙관", "on_miss": "비관"},
               {"id": "L4-F-005", "on_hit": "낙관", "on_miss": "비관"}, {"id": "L4-F-006", "on_hit": "낙관"}], result=None)
add(id="L4-F-102", type="전망", importance=3, status="유효", forecast_status="진행 중", scenario="비관",
    statement="2027년 말까지 도구와 교육은 퍼지지만 결과는 개별 업무 단위에 머문다. 전사 생산성 결과치는 공개되지 않고, 에이전트는 계속 만들어지고 사라지며, 외부 플랫폼이 늘어날수록 데이터·권한·비용 관리가 복잡해진다.",
    milestones=[
        {"by": "2027-03", "text": "전사 생산성 결과치 미공개"},
        {"by": "2027-06", "text": "Palantir 외부 고객 미발표"},
        {"by": "2027-12", "text": "AI·클라우드 매출 비중 정체"}],
    due="2027-12-31", condition="없음",
    method="낙관 시나리오의 판정 조건 세 가지 중 하나 이하만 충족 시 적중",
    basis=["L4-M-002", "L4-M-003", "L4-M-008"], signposts=[], result=None)

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

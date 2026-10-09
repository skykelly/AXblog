"""L6 R1 4유형 기록 생성 + 규칙 검증.
출력: i4/records.jsonl
"""
import json, sys
from pathlib import Path
from collections import Counter

R = "R1"
SRC = {
 "nvda_map": {"url": "https://www.thailand-business-news.com/pr-news/lg-teams-with-nvidia-to-shape-the-future-with-m-a-p-mobility-ai-infra-physical-ai", "publisher": "PR Newswire (LG 발표)", "date": "2026-06-08", "grade": "A"},
 "nvda_visit": {"url": "https://www.heraldk.com/article/2026062102354578033", "publisher": "헤럴드경제", "date": "2026-06-21", "grade": "B"},
 "ms_tmm": {"url": "https://economist.co.kr/article/view/ecn202609220008", "publisher": "이코노미스트 (LG 발표)", "date": "2026-09-22", "grade": "B"},
 "palantir": {"url": "https://byline.network/2026/03/12-548/", "publisher": "바이라인네트워크 (LG CNS 발표)", "date": "2026-03-12", "grade": "B"},
 "claude": {"url": "https://view.asiae.co.kr/article/2026060908300307384", "publisher": "아시아경제 (LG CNS 발표)", "date": "2026-06-09", "grade": "B"},
 "skild": {"url": "https://www.itworld.co.kr/article/4007927/lg-cns-ai-로봇-기업-스킬드ai와-전략적-협력-발표.html", "publisher": "ITWorld (LG CNS 발표)", "date": "2025-06-17", "grade": "B"},
 "koo_sv": {"url": "https://www.heraldk.com/article/2026040617000044878", "publisher": "헤럴드경제 (LG 발표)", "date": "2026-04-06", "grade": "B"},
 "lxp": {"url": "https://www.dailian.co.kr/news/view/1654748/LG-CNSLX%ED%8C%90%ED%86%A0%EC%8A%A4-%EB%AC%BC%EB%A5%98%EC%84%BC%ED%84%B0-%ED%9C%B4%EB%A8%B8%EB%85%B8-2026", "publisher": "데일리안 (LG CNS 발표)", "date": "2026-06-11", "grade": "B"},
 "inno": {"url": "https://v.daum.net/v/20260413060304293", "publisher": "쿠키뉴스", "date": "2026-04-13", "grade": "B"},
 "cusp": {"url": "https://view.asiae.co.kr/en/article/2026072710221174471", "publisher": "Asia Economy (LG CNS 발표)", "date": "2026-07-27", "grade": "B"},
 "dnd": {"url": "https://www.biopharminternational.com/view/lg-ai-research-d-d-pharmatech-partner-to-advance-ai-driven-oral-peptide-drug-discovery", "publisher": "BioPharm International", "date": "2026-06-17", "grade": "B"},
 "lgchem": {"url": "https://www.newspim.com/news/view/20260618000055", "publisher": "뉴스핌 (LG화학 발표)", "date": "2026-06-18", "grade": "B"},
 "sdverse": {"url": "https://www.heraldk.com/article/2026040215280143224", "publisher": "헤럴드경제 (LG에너지솔루션 발표)", "date": "2026-04-02", "grade": "B"},
 "cns_q1": {"url": "https://byline.network/2026/04/30-525/", "publisher": "바이라인네트워크 (LG CNS 1분기 실적)", "date": "2026-04-30", "grade": "B"},
}
def src(*keys): return [dict(SRC[k], key=k) for k in keys]

base = dict(question="L6", question_version="v1.0", first_seen=R, last_seen=R, status="유효", replaces=None, check_flags=[])
records = []
def add(**kw):
    r = dict(base); r.update(kw); records.append(r)

NOVAL = "계약 금액·조건 미공개"

# ---------- 지표 (M) ----------
add(id="L6-M-001", type="지표", indicator="L6-T1", importance=3, statement="LG–NVIDIA M.A.P. 협력에는 모빌리티·AI 인프라·피지컬 AI 세 분야에 LG전자·LG이노텍·LG유플러스·LG CNS·LG에너지솔루션·LG AI연구원 여섯 곳이 참여한다. 회동 2주 뒤 30여 명 규모의 워킹그룹이 NVIDIA 본사를 찾아 레퍼런스 로봇 공동 개발 등 우선 과제를 논의했다.",
    value=6, unit="곳 (참여 계열사)", as_of="2026-06", region="GLOBAL", definition="NVIDIA 협력 참여 계열사 수", extra={"areas": "모빌리티·AI 인프라·피지컬 AI", "working_group": "30여 명"},
    sources=src("nvda_map", "nvda_visit"), verified=True)
add(id="L6-M-002", type="지표", indicator="L6-T2", importance=3, statement="LG전자의 대용량 CDU와 LG에너지솔루션의 ESS가 NVIDIA AI 팩토리 프로그램 'DSX Ready' 제품에 포함됐다.",
    value=2, unit="개 (DSX Ready 포함 제품군)", as_of="2026-09", region="GLOBAL", definition="파트너 공급망 프로그램에 포함된 LG 제품", sources=src("ms_tmm"), verified=True)
add(id="L6-M-003", type="지표", indicator="L6-T4", importance=3, statement="LG그룹은 Microsoft와 AI 데이터센터 인프라(냉각·전력·IT 공급 기회 탐색), 사무직 AX(Copilot 등 도입), 피지컬 AI(제조·물류·모빌리티 모델 학습과 데이터 플라이휠) 세 분야의 전략적 파트너십을 맺었다. 구광모 회장과 계열사 CEO 5명이 참석했다.",
    value=3, unit="분야 (합의 분야)", as_of="2026-09", region="GLOBAL", definition="Microsoft 협력 합의 분야 수", extra={"attendees": "구광모 회장 + 경영진 5명"},
    sources=src("ms_tmm"), verified=True, check_flags=[NOVAL])
add(id="L6-M-004", type="지표", indicator="L6-T5", importance=2, statement="확인된 AI·로봇 지분 투자는 네 건이다. LG테크놀로지벤처스의 Anthropic(2023)·Skild AI(2025) 투자, LG CNS의 Dexmate 투자(2026년 3월), LG이노텍의 4D 이미징 레이더 기업 스마트레이더시스템 지분 4.9%다.",
    value=4, unit="건 (확인된 AI·로봇 지분 투자)", as_of="2026-06", region="GLOBAL", definition="LG CVC·계열사의 AI·로봇 지분 투자",
    sources=src("claude", "skild", "lxp", "inno"), verified=True, check_flags=["투자 금액 미공개"])
add(id="L6-M-005", type="지표", indicator="L6-T6", importance=2, statement="LG CNS가 창립 멤버로 합류한 CuspAI 주도 소재 AI 협력체에는 NVIDIA·Meta·AMD 등 48개 기업·연구기관이 참여한다.",
    value=48, unit="곳 (협력체 참여 기관)", as_of="2026-07", region="GLOBAL", definition="소재 AI 협력체 규모", sources=src("cusp"), verified=True)
add(id="L6-M-006", type="지표", indicator="L6-T7", importance=2, statement="LG에너지솔루션은 GM 주도 차량 SW 마켓 SDVerse에 배터리 SW 5종을 올렸다.",
    value=5, unit="종 (등록 배터리 SW)", as_of="2026-04", region="GLOBAL", definition="외부 마켓에 올린 LG SW 수", sources=src("sdverse"), verified=True, check_flags=["고객 미공개"])
add(id="L6-M-007", type="지표", indicator="L6-T8", importance=2, statement="LG CNS가 재판매하는 ChatGPT Enterprise는 1분기 기준 약 10곳의 고객이 계약했다.",
    value=10, unit="곳 (ChatGPT Enterprise 고객)", as_of="2026-04", region="KR", definition="파트너 플랫폼 재판매 고객 수", sources=src("cns_q1"), verified=True)

# ---------- 사건 (E) ----------
add(id="L6-E-001", type="사건", importance=2, statement="LG CNS가 Skild AI와 국내 첫 전략적 협력을 맺고, LG테크놀로지벤처스를 통해 지분 투자했다. Skild의 로봇 파운데이션 모델을 제조·물류 데이터로 미세 조정해 산업용 휴머노이드 솔루션을 만든다.",
    date="2025-06-17", actor="LG CNS·Skild AI", sources=src("skild"), verified=True, check_flags=["조사 기간 이전 — 기준선", "투자 금액 미공개"])
add(id="L6-E-002", type="사건", importance=3, statement="LG CNS가 Palantir와 전략적 파트너십을 맺었다. LG 계열사 품질 관리 PoC 뒤 본 계약이 됐고, 전방배치 엔지니어링(FDE) 조직을 만들어 그룹에서 외부로 넓힌다.",
    date="2026-03-12", actor="LG CNS·Palantir", sources=src("palantir"), verified=True, check_flags=[NOVAL])
add(id="L6-E-003", type="사건", importance=2, statement="구광모 회장이 실리콘밸리에서 Palantir CEO 알렉스 카프, Skild AI 공동 창업자, LG테크놀로지벤처스 경영진을 만났다. 온톨로지·AI 의사결정 체계와 휴머노이드 시연을 살폈고, 구체적 계약 발표는 없었다.",
    date="2026-04-02", actor="LG", sources=src("koo_sv"), verified=True)
add(id="L6-E-004", type="사건", importance=2, statement="LG에너지솔루션이 GM·Magna·Wipro가 세운 차량 SW 마켓 SDVerse에 배터리 기업 최초로 합류했다.",
    date="2026-04-03", actor="LG에너지솔루션", sources=src("sdverse"), verified=True)
add(id="L6-E-005", type="사건", importance=3, statement="구광모 회장과 젠슨 황 CEO가 서울에서 만나 LG–NVIDIA M.A.P.(모빌리티·AI 인프라·피지컬 AI) 협력과 레퍼런스 로봇 공동 개발에 합의했다.",
    date="2026-06-08", actor="LG·NVIDIA", sources=src("nvda_map", "nvda_visit"), verified=True)
add(id="L6-E-006", type="사건", importance=3, statement="LG CNS가 Anthropic과 LG그룹 전 계열사에 적용할 수 있는 Claude Enterprise 통합 계약을 맺었다. LG테크놀로지벤처스는 2023년부터 Anthropic 지분을 갖고 있다.",
    date="2026-06-09", actor="LG CNS·Anthropic", sources=src("claude"), verified=True, check_flags=[NOVAL])
add(id="L6-E-007", type="사건", importance=2, statement="LG CNS가 LX판토스 물류센터 휴머노이드 실증에 3월 투자한 미국 Dexmate의 바퀴형 휴머노이드를 투입하기로 했다.",
    date="2026-06-11", actor="LG CNS", sources=src("lxp"), verified=True)
add(id="L6-E-008", type="사건", importance=2, statement="LG AI연구원이 D&D Pharmatech과, LG화학이 LabGenius와 AI 신약 협력을 잇달아 맺었다. LabGenius와는 선급금·연구비를 내는 라이선스 옵션 계약이다.",
    date="2026-06-18", actor="LG AI연구원·LG화학", sources=src("dnd", "lgchem"), verified=True)
add(id="L6-E-009", type="사건", importance=2, statement="LG 계열사 경영진과 실무진 30여 명이 NVIDIA 본사를 찾아 피지컬 AI·로보틱스 우선 과제를 논의했다.",
    date="2026-06-22", actor="LG·NVIDIA", sources=src("nvda_visit"), verified=True)
add(id="L6-E-010", type="사건", importance=2, statement="LG CNS가 CuspAI 주도 소재 AI 협력체의 창립 멤버이자 국내 플랫폼 공급 파트너가 됐다.",
    date="2026-07-27", actor="LG CNS", sources=src("cusp"), verified=True)
add(id="L6-E-011", type="사건", importance=3, statement="LG그룹 사장단이 Microsoft 본사에서 사티아 나델라 CEO와 AI 데이터센터·AX·피지컬 AI 세 분야의 전략적 파트너십을 맺었다. 같은 날 LG전자 CDU와 LG에너지솔루션 ESS가 NVIDIA DSX Ready 제품에 포함됐다.",
    date="2026-09-21", actor="LG·Microsoft·NVIDIA", sources=src("ms_tmm"), verified=True, check_flags=[NOVAL])

# ---------- 해석 (I) ----------
add(id="L6-I-001", type="해석", importance=3, target="파트너별 단계 분포", direction="중립",
    statement="상용 계약까지 간 협력은 LG가 '고객'인 경우다. Palantir와 Anthropic은 그룹 도입 계약으로 이어졌지만, LG가 '공급자'가 되는 NVIDIA·Microsoft 협력은 공동개발·공급 기회 탐색 단계다. 협력이 LG의 매출로 바뀌는 것은 아직 이르다.",
    basis=["L6-E-002", "L6-E-006", "L6-E-005", "L6-M-003"])
add(id="L6-I-002", type="해석", importance=3, target="NVIDIA", direction="강화",
    statement="NVIDIA는 가장 넓은 축이다. 세 분야에 여섯 계열사가 참여하고, LG전자 CDU와 LG에너지솔루션 ESS가 DSX Ready 제품에 들어가 NVIDIA 기반 AI 팩토리의 공급망 입구에 섰다. 레퍼런스 로봇 공동 개발은 피지컬 AI의 기술 접점이다.",
    basis=["L6-M-001", "L6-M-002", "L6-E-005", "L6-E-009"])
add(id="L6-I-003", type="해석", importance=3, target="Microsoft", direction="강화",
    statement="Microsoft와의 관계는 LG가 고객이자 공급자 후보인 양면 구조다. LG는 사무직에 Copilot 등을 도입하고, Microsoft 데이터센터에 냉각·전력·IT를 공급할 기회를 찾는다. 공급 쪽은 금액이 공개되지 않은 탐색 단계다.",
    basis=["L6-M-003", "L6-E-011"])
add(id="L6-I-004", type="해석", importance=3, target="종속 위험", direction="약화",
    statement="핵심층을 외부가 쥐고 있다. 의사결정·온톨로지는 Palantir, 로봇 두뇌는 Skild AI와 NVIDIA GR00T, 컴퓨팅은 NVIDIA에 기댄다. LG가 직접 쥔 축은 EXAONE, PhysicalWorks 같은 운영 플랫폼, 그리고 현장 데이터다.",
    basis=["L6-E-002", "L6-E-001", "L6-E-005"])
add(id="L6-I-005", type="해석", importance=2, target="CVC 옵션", direction="강화",
    statement="CVC 투자가 협력과 실증으로 이어지는 경로가 생겼다. 가장 빠른 사례는 Dexmate로, 3월 투자 뒤 6월 LX판토스 물류 실증에 투입됐다. Anthropic은 2023년 투자 뒤 2026년 그룹 통합 계약으로 이어졌다.",
    basis=["L6-M-004", "L6-E-007", "L6-E-006"])
add(id="L6-I-006", type="해석", importance=2, target="파트너 기술 재판매", direction="강화",
    statement="파트너 기술은 LG CNS의 외부 사업이 된다. ChatGPT Enterprise를 약 10곳에 팔았고, Palantir는 FDE 조직으로, CuspAI는 국내 소재 기업 공급으로 재판매한다. 협력이 내재화되기보다 '유통'되는 경로다.",
    basis=["L6-M-007", "L6-E-002", "L6-E-010"])
add(id="L6-I-007", type="해석", importance=2, target="실행 속도", direction="강화",
    statement="오너가 직접 협력 속도를 끌어올린다. 구광모 회장은 4월 실리콘밸리, 6월 젠슨 황, 9월 사티아 나델라를 직접 만났고, NVIDIA 회동 2주 만에 30여 명의 워킹그룹이 꾸려졌다.",
    basis=["L6-E-003", "L6-E-005", "L6-E-009", "L6-E-011"])

# ---------- 세부 전망 (F) ----------
add(id="L6-F-001", type="전망", importance=2, status="유효", forecast_status="진행 중",
    statement="LG는 2027년 1월 CES까지 NVIDIA와 공동 개발한 레퍼런스 로봇을 공개할 것이다.", due="2027-01-31", condition="없음",
    method="LG·NVIDIA 공식 발표 또는 CES 2027 전시 확인", basis=["L6-E-005"], result=None)
add(id="L6-F-002", type="전망", importance=2, status="유효", forecast_status="진행 중",
    statement="LG 계열사는 2026년 말까지 사무직 대상 Microsoft Copilot 도입을 발표할 것이다.", due="2026-12-31", condition="없음",
    method="계열사 공식 발표 또는 주요 언론 보도 확인", basis=["L6-M-003"], result=None)
add(id="L6-F-003", type="전망", importance=3, status="유효", forecast_status="진행 중",
    statement="LG는 2027년 6월 말까지 Skild AI 또는 NVIDIA GR00T 기반 로봇의 LG 현장 실증 결과를 공개할 것이다.", due="2027-06-30", condition="없음",
    method="LG 계열사 공식 발표 확인", basis=["L6-E-001", "L6-E-005"], result=None)
add(id="L6-F-004", type="전망", importance=2, status="유효", forecast_status="진행 중",
    statement="LG테크놀로지벤처스 또는 계열사는 2027년 6월 말까지 로봇·피지컬 AI 스타트업 지분 투자를 한 건 이상 추가 발표할 것이다.", due="2027-06-30", condition="없음",
    method="공식 발표 또는 주요 언론 보도 확인", basis=["L6-M-004"], result=None)
add(id="L6-F-005", type="전망", importance=3, status="유효", forecast_status="진행 중",
    statement="LG전자 CDU가 NVIDIA DSX 참조 설계 기반 고객 프로젝트에 공급된다는 발표가 2027년 6월 말까지 나올 것이다.", due="2027-06-30", condition="없음",
    method="LG전자·NVIDIA 공식 발표 확인", basis=["L6-M-002"], result=None)
add(id="L6-F-006", type="전망", importance=2, status="유효", forecast_status="진행 중",
    statement="LG그룹은 2027년 6월 말까지 Google·Amazon·Meta·OpenAI 가운데 한 곳과 그룹 차원의 전략적 파트너십을 새로 발표할 것이다.", due="2027-06-30", condition="없음",
    method="LG 공식 발표 확인", basis=["L6-E-011", "L6-E-005"], result=None)

# ---------- 메인 질문 시나리오 ----------
add(id="L6-F-101", type="전망", importance=3, status="유효", forecast_status="진행 중", scenario="낙관",
    statement="2027년 말까지 협력이 LG의 공급망 진입과 고객 확보로 이어진다. NVIDIA·Microsoft 관련 LG 제품 공급 계약이 공식화되고, 외부 로봇 파운데이션 모델이 LG 현장에서 성과를 내며, 파트너 기술을 결합한 LG CNS 외부 고객이 늘어난다.",
    milestones=[
        {"by": "2027-01", "text": "레퍼런스 로봇 공개"},
        {"by": "2027-06", "text": "CDU의 DSX 기반 프로젝트 공급, 외부 RFM 로봇 현장 실증 결과"},
        {"by": "2027-12", "text": "Microsoft 공급 계약 공식화"}],
    due="2027-12-31", condition="미국 수출 통제·관세 변화로 협력이 멈추지 않을 경우",
    method="세 가지 중 두 가지 이상 충족 시 적중: (1) NVIDIA 또는 Microsoft 관련 LG 제품 공급 계약 공식 발표 (2) 외부 로봇 파운데이션 모델(Skild·GR00T) 기반 로봇의 LG 현장 실증 결과 공개 (3) 파트너 기술(Palantir·Claude·CuspAI 등)을 결합한 LG CNS 외부 고객 계약 2건 이상 공개",
    basis=["L6-M-002", "L6-M-003", "L6-E-001", "L6-E-002"],
    signposts=[{"id": "L6-F-001", "on_hit": "낙관"}, {"id": "L6-F-003", "on_hit": "낙관", "on_miss": "비관"},
               {"id": "L6-F-005", "on_hit": "낙관", "on_miss": "비관"}, {"id": "L6-F-002", "on_hit": "낙관"},
               {"id": "L6-F-004", "on_hit": "낙관"}, {"id": "L6-F-006", "on_hit": "낙관"}], result=None)
add(id="L6-F-102", type="전망", importance=3, status="유효", forecast_status="진행 중", scenario="비관",
    statement="2027년 말까지 회동·MOU·프로그램 참여는 늘지만 공급 계약과 내재화 성과는 드러나지 않는다. 핵심층(의사결정·로봇 두뇌·컴퓨팅)의 외부 의존이 깊어지고, 협력은 LG CNS의 재판매 매출에 머문다.",
    milestones=[
        {"by": "2027-06", "text": "DSX 기반 공급 미발표"},
        {"by": "2027-06", "text": "외부 RFM 현장 성과 미공개"},
        {"by": "2027-12", "text": "Microsoft 공급 계약 미공식화"}],
    due="2027-12-31", condition="없음",
    method="낙관 시나리오의 판정 조건 세 가지 중 하나 이하만 충족 시 적중",
    basis=["L6-M-003", "L6-M-007", "L6-E-002"], signposts=[], result=None)

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

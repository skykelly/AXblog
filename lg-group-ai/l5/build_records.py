"""L5 R1 4유형 기록 생성 + 규칙 검증.
출력: i4/records.jsonl
"""
import json, sys
from pathlib import Path
from collections import Counter

R = "R1"
SRC = {
 "exd": {"url": "https://www.mt.co.kr/industry/2026/02/03/2026020308502174042", "publisher": "머니투데이 (LG AI연구원 발표)", "date": "2026-02-03", "grade": "B"},
 "icml": {"url": "https://www.lg.co.kr/media/release/30327", "publisher": "LG 보도자료 (LG AI연구원)", "date": "2026-07-08", "grade": "A"},
 "dnd": {"url": "https://www.biopharminternational.com/view/lg-ai-research-d-d-pharmatech-partner-to-advance-ai-driven-oral-peptide-drug-discovery", "publisher": "BioPharm International", "date": "2026-06-17", "grade": "B"},
 "lgchem": {"url": "https://www.newspim.com/news/view/20260618000055", "publisher": "뉴스핌 (LG화학 발표)", "date": "2026-06-18", "grade": "B"},
 "lges": {"url": "https://www.etnews.com/20260724000112", "publisher": "전자신문", "date": "2026-07-26", "grade": "B"},
 "cusp": {"url": "https://view.asiae.co.kr/en/article/2026072710221174471", "publisher": "Asia Economy (LG CNS 발표)", "date": "2026-07-27", "grade": "B"},
}
def src(*keys): return [dict(SRC[k], key=k) for k in keys]

base = dict(question="L5", question_version="v1.0", first_seen=R, last_seen=R, status="유효", replaces=None, check_flags=[])
records = []
def add(**kw):
    r = dict(base); r.update(kw); records.append(r)

CO = "회사 발표 수치 — 독립 검증 없음"
TARGET = "목표치 — 결과 아님"

# ---------- 지표 (M) ----------
add(id="L5-M-001", type="지표", indicator="L5-T1", importance=3, statement="LG AI연구원의 EXAONE Discovery로 화장품 소재 4,000만 건 이상의 물성·합성 용이성·안전성 검토를, 기존 약 22개월에서 하루로 줄였다고 회사가 밝혔다.",
    value=1, unit="일 (기존 약 22개월)", as_of="2026-02", region="KR", definition="AI 기반 물질 검토 소요 기간", extra={"materials": "4,000만 건 이상", "before": "약 22개월"},
    sources=src("exd"), verified=True, check_flags=[CO])
add(id="L5-M-002", type="지표", indicator="L5-T2", importance=3, statement="LG생활건강과 LG AI연구원은 AI로 42만 개 이상의 후보에서 하루 만에 탈모 관리 신소재 '람시딜'을 골라냈다. 스테로이드 유래 성분 없이 탈모 방지 효과를 보였다는 결과를 세계모발학회에서 발표했고, 제품화를 준비 중이다.",
    value=42, unit="만 개 이상 (후보 물질)", as_of="2026-07", region="KR", definition="AI 발굴 화장품 원료의 탐색 규모와 검증 단계", extra={"stage": "학회 효과 발표, 제품화 준비"},
    sources=src("icml"), verified=True)
add(id="L5-M-003", type="지표", indicator="L5-T5", importance=2, statement="LG화학은 통상 5년 넘게 걸리는 항체 신약 후보 발굴(표적 검증~선도물질 최적화) 기간을 AI 협력으로 절반가량 줄이는 것이 목표다.",
    value=50, unit="% (기간 단축 목표)", as_of="2026-06", region="KR", definition="신약 후보 발굴 기간 단축 목표", extra={"baseline": "5년 이상"},
    sources=src("lgchem"), verified=True, check_flags=[TARGET])
add(id="L5-M-004", type="지표", indicator="L5-T5", importance=2, statement="LG에너지솔루션은 AI 에이전트와 자동 실험 설비로 배터리 개발 기간을 절반으로 줄이거나 같은 일을 절반의 자원으로 하는 것을 목표로 한다. 측정된 결과는 공개되지 않았다.",
    value=50, unit="% (개발 기간·자원 절감 목표)", as_of="2026-07", region="GLOBAL", definition="배터리 R&D 기간·자원 절감 목표",
    sources=src("lges"), verified=True, check_flags=[TARGET])
add(id="L5-M-005", type="지표", indicator="L5-T6", importance=2, statement="LG AI연구원은 2020년 12월 출범 이후 주요 AI 학회 논문 363편을 냈고, 특허를 838건(국내 371·해외 243·PCT 224) 출원했다. EXAONE Discovery는 '길목 특허'로 등록됐다.",
    value=838, unit="건 (특허 출원)", as_of="2026-07", region="GLOBAL", definition="LG AI연구원 누적 특허 출원", extra={"papers": "363편"},
    sources=src("icml", "exd"), verified=True)
add(id="L5-M-006", type="지표", indicator="L5-T7", importance=2, statement="LG AI연구원의 신소재 생성 AI 기술은 소재 생성 벤치마크 LeMat-GenBench 종합 2위를 기록했다.",
    value=2, unit="위 (LeMat-GenBench 종합)", as_of="2026-07", region="GLOBAL", definition="신소재 생성 AI 벤치마크 순위", sources=src("icml"), verified=True)
add(id="L5-M-007", type="지표", indicator="L5-T8", importance=2, statement="LG CNS는 영국 CuspAI가 주도하는 소재 AI 협력체 'AI Materials Foundry'의 창립 멤버가 됐다. NVIDIA·Meta·AMD 등 48개 기업·연구기관이 참여하며, LG CNS는 국내 소재 기업에 플랫폼을 공급한다.",
    value=48, unit="곳 (참여 기업·기관)", as_of="2026-07", region="GLOBAL", definition="외부 소재 AI 협력체 규모", sources=src("cusp"), verified=True)

# ---------- 사건 (E) ----------
add(id="L5-E-001", type="사건", importance=2, statement="LG AI연구원이 논문·특허·분자 구조를 함께 분석해 실험 설계와 신소재 예측까지 잇는 EXAONE Discovery 특허를 등록했다. 배터리·반도체·신약으로 넓힐 계획이다.",
    date="2026-02-03", actor="LG AI연구원", sources=src("exd"), verified=True)
add(id="L5-E-002", type="사건", importance=3, statement="LG AI연구원과 D&D Pharmatech이 AI 기반 경구용 펩타이드 신약을 함께 개발하기로 했다. LG는 후보 서열 설계 모델을, D&D는 합성·실험·경구 전달·전임상·임상을 맡고 결과를 모델에 되먹인다. 현재 발견 단계다.",
    date="2026-06-17", actor="LG AI연구원·D&D Pharmatech", sources=src("dnd"), verified=True, check_flags=["계약 조건 미공개"])
add(id="L5-E-003", type="사건", importance=3, statement="LG화학이 영국 LabGenius와 다중항체 항암 후보 공동연구·라이선스 옵션 계약을 맺었다(선급금·연구비 지급). AI 설계와 로봇 실험을 반복하는 방식이며, 자체 AI 플랫폼 MediX와 Galux 협력도 운영한다.",
    date="2026-06-18", actor="LG화학", sources=src("lgchem"), verified=True, check_flags=["금액 미공개"])
add(id="L5-E-004", type="사건", importance=2, statement="LG AI연구원이 ICML 2026에서 AI로 찾은 탈모 관리 소재 람시딜과, GS칼텍스와 함께 만든 AI 데이터센터용 액침 냉각유 소재를 선보였다.",
    date="2026-07-08", actor="LG AI연구원", sources=src("icml"), verified=True)
add(id="L5-E-005", type="사건", importance=2, statement="LG에너지솔루션이 배터리 R&D에 AI 에이전트와 자동 실험을 결합했다고 밝혔다. 전해질 후보를 AI가 좁히고 자동 설비가 만들어 시험한 뒤 결과를 다시 학습하며, 초기 충방전 데이터만으로 수명을 예측한다.",
    date="2026-07-26", actor="LG에너지솔루션", sources=src("lges"), verified=True)
add(id="L5-E-006", type="사건", importance=2, statement="LG CNS가 CuspAI 주도 소재 AI 협력체의 창립 멤버로 합류했다. 의뢰 기업이 신소재 특허를 소유하고, 데이터는 전용 서버로 분리한다.",
    date="2026-07-27", actor="LG CNS", sources=src("cusp"), verified=True)

# ---------- 해석 (I) ----------
add(id="L5-I-001", type="해석", importance=3, target="탐색 속도", direction="강화",
    statement="AI는 탐색 단계를 크게 줄였다. 4,000만 건 검토가 22개월에서 하루로, 42만 개 후보 선별이 하루로 줄었다고 회사가 밝혔다. 다만 모두 회사 발표 수치이며 독립 검증은 없다.",
    basis=["L5-M-001", "L5-M-002"])
add(id="L5-I-002", type="해석", importance=3, target="사업화 거리", direction="중립",
    statement="AI로 찾은 물질 가운데 제품·임상까지 간 것은 아직 없다. 가장 앞선 것은 탈모 소재 람시딜로, 효과를 학회에서 발표하고 제품화를 준비 중이다. 신약은 펩타이드·항체 모두 발견 단계다.",
    basis=["L5-M-002", "L5-E-002", "L5-E-003"])
add(id="L5-I-003", type="해석", importance=3, target="폐쇄 루프", direction="강화",
    statement="AI 제안과 실험을 잇는 폐쇄 루프가 만들어지고 있다. D&D Pharmatech은 실험 결과를 모델에 되먹이고, LabGenius는 로봇 실험을 반복하며, LG에너지솔루션은 자동 설비로 전해질 후보를 시험한다. 탐색 속도가 실험 속도에 막히지 않게 하는 구조다.",
    basis=["L5-E-002", "L5-E-003", "L5-E-005"])
add(id="L5-I-004", type="해석", importance=2, target="개발 기간", direction="중립",
    statement="개발 기간 단축은 목표 단계다. LG화학은 항체 후보 발굴 5년 이상을 절반으로, LG에너지솔루션은 배터리 개발 기간을 절반으로 줄이는 것이 목표지만 측정된 결과는 공개되지 않았다.",
    basis=["L5-M-003", "L5-M-004"])
add(id="L5-I-005", type="해석", importance=2, target="자체와 외부의 결합", direction="중립",
    statement="자체 플랫폼과 외부 협력을 함께 쓴다. 소재·화장품은 자체 EXAONE Discovery로, 신약은 D&D·LabGenius·Galux 같은 외부 바이오텍과, 외부 소재 고객은 CuspAI 플랫폼으로 지원한다.",
    basis=["L5-E-001", "L5-E-002", "L5-E-003", "L5-E-006"])
add(id="L5-I-006", type="해석", importance=2, target="연구 역량", direction="강화",
    statement="연구 역량 지표는 글로벌 수준이다. 신소재 생성 벤치마크 종합 2위, 특허 출원 838건, 주요 학회 논문 363편이다. 기술 역량과 사업 성과 사이의 거리가 이 질문의 핵심 판정 대상이다.",
    basis=["L5-M-006", "L5-M-005"])
add(id="L5-I-007", type="해석", importance=1, target="테마 간 연결", direction="강화",
    statement="AI for Science는 AI 데이터센터와도 연결된다. LG AI연구원이 GS칼텍스와 만든 액침 냉각유 소재는 L1(AI 데이터센터 냉각)의 소재가 될 수 있다.",
    basis=["L5-E-004"])

# ---------- 세부 전망 (F) ----------
add(id="L5-F-001", type="전망", importance=3, status="유효", forecast_status="진행 중",
    statement="LG생활건강은 2027년 6월 말까지 람시딜을 적용한 제품을 출시할 것이다.", due="2027-06-30", condition="없음",
    method="LG생활건강 공식 발표 확인", basis=["L5-M-002"], result=None)
add(id="L5-F-002", type="전망", importance=2, status="유효", forecast_status="진행 중",
    statement="LG AI연구원과 D&D Pharmatech은 2027년 말까지 첫 후보 물질 또는 전임상 진입을 발표할 것이다.", due="2027-12-31", condition="없음",
    method="양사 공식 발표 확인", basis=["L5-E-002"], result=None)
add(id="L5-F-003", type="전망", importance=2, status="유효", forecast_status="진행 중",
    statement="LG화학은 2027년 말까지 LabGenius 협력의 후보 선정 또는 라이선스 옵션 행사를 발표할 것이다.", due="2027-12-31", condition="없음",
    method="LG화학 공식 발표 또는 공시 확인", basis=["L5-E-003"], result=None)
add(id="L5-F-004", type="전망", importance=3, status="유효", forecast_status="진행 중",
    statement="2027년 말까지 LG 계열사가 AI로 설계한 신약 후보가 임상 1상에 진입하지는 않을 것이다.", due="2027-12-31", condition="없음",
    method="계열사 공시·임상 등록 확인", basis=["L5-E-002", "L5-E-003"], result=None)
add(id="L5-F-005", type="전망", importance=2, status="유효", forecast_status="진행 중",
    statement="LG에너지솔루션은 2027년 말까지 AI로 찾은 소재(전해질·첨가제 등)를 적용한 제품 또는 양산 계획을 발표할 것이다.", due="2027-12-31", condition="없음",
    method="LG에너지솔루션 공식 발표 확인", basis=["L5-E-005", "L5-M-004"], result=None)
add(id="L5-F-006", type="전망", importance=2, status="유효", forecast_status="진행 중",
    statement="LG CNS는 2027년 6월 말까지 CuspAI 플랫폼 기반 국내 소재 기업 고객 계약을 발표할 것이다.", due="2027-06-30", condition="없음",
    method="LG CNS 공식 발표 확인", basis=["L5-M-007", "L5-E-006"], result=None)

# ---------- 메인 질문 시나리오 ----------
add(id="L5-F-101", type="전망", importance=3, status="유효", forecast_status="진행 중", scenario="낙관",
    statement="2027년 말까지 AI가 찾은 물질이 제품과 개발 후기 단계로 이어진다. 람시딜 제품이 출시되고, 신약 후보가 전임상에 들어가며, 배터리에서 AI 탐색 소재의 적용 계획이 나온다.",
    milestones=[
        {"by": "2027-06", "text": "람시딜 적용 제품 출시"},
        {"by": "2027-12", "text": "펩타이드·항체 후보 선정 또는 전임상 진입"},
        {"by": "2027-12", "text": "AI 탐색 배터리 소재 적용 발표"}],
    due="2027-12-31", condition="없음",
    method="세 가지 중 두 가지 이상 충족 시 적중: (1) AI 발굴 화장품 원료 적용 제품 출시 (2) AI 설계 신약 후보 선정 또는 전임상 진입 발표 (3) AI 탐색 배터리 소재 적용 제품·양산 계획 발표",
    basis=["L5-M-002", "L5-E-002", "L5-E-005"],
    signposts=[{"id": "L5-F-001", "on_hit": "낙관", "on_miss": "비관"}, {"id": "L5-F-002", "on_hit": "낙관"},
               {"id": "L5-F-003", "on_hit": "낙관"}, {"id": "L5-F-005", "on_hit": "낙관", "on_miss": "비관"},
               {"id": "L5-F-006", "on_hit": "낙관"}], result=None)
add(id="L5-F-102", type="전망", importance=3, status="유효", forecast_status="진행 중", scenario="비관",
    statement="2027년 말까지 AI for Science의 성과는 탐색 속도 발표와 협력 계약에 머문다. 화장품 원료 외에는 제품화가 없고, 신약은 발견 단계에 남으며, 개발 기간 단축은 목표치로만 남는다.",
    milestones=[
        {"by": "2027-06", "text": "람시딜 제품 출시 지연"},
        {"by": "2027-12", "text": "신약 후보 미공개"},
        {"by": "2027-12", "text": "기간 단축 결과치 미공개"}],
    due="2027-12-31", condition="없음",
    method="낙관 시나리오의 판정 조건 세 가지 중 하나 이하만 충족 시 적중",
    basis=["L5-M-001", "L5-M-003", "L5-M-004"], signposts=[], result=None)

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

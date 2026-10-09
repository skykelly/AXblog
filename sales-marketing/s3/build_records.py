"""S3 R1 4유형 기록 생성 + 규칙 검증.
출력: i4/records.jsonl
"""
import json, sys
from pathlib import Path
from collections import Counter

R = "R1"
SRC = {
 "cmo": {"url": "https://cmosurvey.org/wp-content/uploads/2026/04/The_CMO_Survey-Highlights_and_Insights_Report-2026.pdf", "publisher": "The CMO Survey 2026 (Duke·Deloitte·AMA)", "date": "2026-04", "grade": "A"},
 "gartner": {"url": "https://www.promptthemarket.com/gartner-cmo-spend-survey-2026/", "publisher": "Prompt the Market (Gartner CMO Spend Survey 2026 인용)", "date": "2026-09-05", "grade": "B"},
 "meta_q2": {"url": "https://www.mediapost.com/publications/article/416925/meta-boosts-advertising-in-q2-tries-to-reassure-i.html", "publisher": "MediaPost (Meta 2분기 실적)", "date": "2026-07-31", "grade": "B"},
 "google_ai": {"url": "https://www.marketscale.com/industries/marketing-tech/googles-ai-ad-machine-drove-15-more-conversions-last-quarter-and-most-marketers-arent-copying-it", "publisher": "MarketScale (Alphabet 2분기 실적 인용)", "date": "2026-08-03", "grade": "B"},
 "haus": {"url": "https://www.haus.io/blog/the-meta-report-lessons-from-640-haus-incrementality-experiments", "publisher": "Haus (증분 실험 640건)", "date": "2025-07-28", "grade": "B"},
 "smec": {"url": "https://almcorp.com/blog/google-ai-max-search-campaigns-performance-cpa-revenue-study/", "publisher": "ALM Corp (Smarter Ecommerce 분석 인용)", "date": "2026-03-06", "grade": "B"},
 "braze": {"url": "https://tei.forrester.com/go/Braze/AIDecisioningSpotlight/?lang=en-us", "publisher": "Forrester TEI (Braze 의뢰)", "date": "2026-05", "grade": "B"},
 "creative": {"url": "https://www.taboola.com/press-releases/genai-ads-study-2026/", "publisher": "Taboola 보도자료 (Columbia·Harvard·TUM·CMU 연구)", "date": "2026-01-28", "grade": "B"},
 "naver_q2": {"url": "https://www.inews24.com/view/1992775", "publisher": "아이뉴스24 (네이버 2분기 실적)", "date": "2026-08-07", "grade": "B"},
 "gml": {"url": "https://gigazine.net/gsc_news/en/20260521-google-marketing-ai-search", "publisher": "GIGAZINE (Google Marketing Live 2026)", "date": "2026-05-21", "grade": "B"},
}
def src(*keys): return [dict(SRC[k], key=k) for k in keys]

base = dict(question="S3", question_version="v1.0", first_seen=R, last_seen=R, status="유효", replaces=None, check_flags=[])
records = []
def add(**kw):
    r = dict(base); r.update(kw); records.append(r)

PLATFORM = "플랫폼 자체 보고 — 업체 주장"

# ---------- 지표 (M) ----------
add(id="S3-M-001", type="지표", indicator="S3-T1", importance=3, statement="미국 기업 마케팅 활동 중 AI를 쓰는 비중은 2026년 24.2%로 2024년(13.1%)의 두 배 가까이 됐다. 생성형 AI는 22.4%(2024년 7.0%)다. 용도는 콘텐츠 제작 73.9%, 콘텐츠 개인화 65.4%, 마케팅 자동화 48.9%, 타기팅 결정 45.2%, 고객 예측 분석 41.5% 순이다.",
    value=24.2, unit="% (마케팅 활동 중 AI 사용)", as_of="2026-01", region="US", definition="마케팅 활동 중 AI 사용 비중 (마케팅 임원 308명)",
    extra={"genai": "22.4%", "content": "73.9%", "personalization": "65.4%", "automation": "48.9%", "targeting": "45.2%", "predictive": "41.5%", "in_3y": "55.9%"},
    sources=src("cmo"), verified=True)
add(id="S3-M-002", type="지표", indicator="S3-T2", importance=3, statement="AI 덕분에 매출 생산성이 좋아졌다는 개선 폭은 2026년 14.1%로 1년 전(8.6%)보다 커졌다. 고객 만족 개선은 10.8%, 마케팅 간접비 절감은 14.6%다.",
    value=14.1, unit="% (매출 생산성 개선)", as_of="2026-01", region="US", definition="AI로 인한 매출 생산성 개선 (마케터 자기 평가)", extra={"satisfaction": "10.8%", "overhead": "-14.6%"},
    sources=src("cmo"), verified=True, check_flags=["마케터 자기 평가 — 측정된 증분 아님"])
add(id="S3-M-003", type="지표", indicator="S3-T3", importance=2, statement="마케팅 예산은 매출의 7.8%로 거의 그대로였고, 그중 15.3%가 AI에 쓰인다. AI를 키울 준비가 됐다는 조직은 30%뿐이며, 이들은 예산의 21.3%를 AI에 쓴다.",
    value=15.3, unit="% (마케팅 예산 중 AI)", as_of="2026-05", region="US·EU", definition="마케팅 예산 중 AI 배분 (마케팅 임원 401명)", extra={"budget_of_revenue": "7.8%", "mature_share": "30%", "mature_ai_budget": "21.3%"},
    sources=src("gartner"), verified=True)
add(id="S3-M-004", type="지표", indicator="S3-T4", importance=3, statement="Meta의 AI 광고 묶음 Advantage+는 2026년 2분기 연환산 매출 750억 달러에 이르렀다. 광고 매출은 594억 달러로 27% 늘었고, 900만 곳 넘는 소상공인이 Meta의 AI 크리에이티브 도구를 쓴다.",
    value=750, unit="억 달러 (Advantage+ 연환산)", as_of="2026-Q2", region="GLOBAL", definition="Meta Advantage+ 연환산 매출", extra={"ad_revenue": "594억 달러 (+27%)", "creative_tool_smb": "900만 곳 이상"},
    sources=src("meta_q2"), verified=True)
add(id="S3-M-005", type="지표", indicator="S3-T5", importance=3, statement="구글은 AI Max와 Performance Max를 함께 쓴 캠페인이 비슷한 광고 수익률에서 전환(또는 전환 가치)을 평균 15% 더 냈다고 밝혔다. AI Max는 베타를 마치고 광고주 50만 곳이 쓴다.",
    value=15, unit="% (전환 증가, 플랫폼 보고)", as_of="2026-Q2", region="GLOBAL", definition="구글 AI 검색 캠페인의 전환 개선", extra={"ai_max_advertisers": "50만 곳"},
    sources=src("google_ai"), verified=True, check_flags=[PLATFORM])
add(id="S3-M-006", type="지표", indicator="S3-T6", importance=3, statement="리테일 검색 캠페인 250여 개를 분석한 결과, AI Max를 켜면 매출은 중앙값 13% 늘었지만 전환당 비용도 16% 올랐다. 광고 수익률은 캠페인에 따라 +42%에서 -35%까지 갈렸다.",
    value=16, unit="% (전환당 비용 상승, 중앙값)", as_of="2025-11", region="GLOBAL", definition="AI Max 적용 시 매출·전환당 비용 변화 (독립 분석)", extra={"revenue": "+13%", "roas_range": "+42% ~ -35%"},
    sources=src("smec"), verified=True, check_flags=["대행사 분석 — 실험 설계 미공개"])
add(id="S3-M-007", type="지표", indicator="S3-T6", importance=3, statement="Meta 광고 증분 실험 640건에서 AI 자동 캠페인(Advantage+)의 증분 광고 수익률은 수동 캠페인보다 12% 낮았다. 브랜드의 58%가 수동 쪽이 더 나았고 42%는 Advantage+가 나았다. Meta 광고 전체로는 핵심 지표를 평균 19% 끌어올렸다.",
    value=-12, unit="% (Advantage+ 증분 ROAS, 수동 대비)", as_of="2025-07", region="US", definition="홀드아웃 실험 기반 증분 광고 수익률 비교", extra={"manual_better_share": "58%", "meta_lift": "+19%"},
    sources=src("haus"), verified=True, check_flags=["조사 기간 이전 연구 — 기준선으로 사용", "측정 업체 자료, 2026년 재분석에서 일부 결론 수정 표시"])
add(id="S3-M-008", type="지표", indicator="S3-T6", importance=2, statement="Braze가 의뢰한 Forrester 분석에서 1:1 개인화 의사결정 AI는 3년간 투자수익률 457%로 추정됐다. 인터뷰 기업 중 한 미디어 회사는 구독 갱신율이 70%에서 84%로 올랐다.",
    value=457, unit="% (3년 ROI, 가상 기업)", as_of="2026-04", region="GLOBAL", definition="AI 개인화 의사결정의 경제 효과 (벤더 의뢰 연구)", extra={"renewal": "70% → 84%"},
    sources=src("braze"), verified=True, check_flags=["벤더 의뢰 연구 — 기업 사례로만 인정"])
add(id="S3-M-009", type="지표", indicator="S3-T7", importance=2, statement="실제 광고 수십만 건(노출 5억 회)을 비교한 연구에서 AI 생성 광고의 클릭률은 0.76%로 사람 제작 광고(0.65%)보다 약간 높았고, 엄격한 통제를 하면 비슷했다. 'AI 티가 나지 않는' AI 광고가 가장 잘 됐다.",
    value=0.76, unit="% (AI 광고 클릭률)", as_of="2026-01", region="GLOBAL", definition="AI 생성 광고와 사람 제작 광고의 클릭률 비교", extra={"human": "0.65%"},
    sources=src("creative"), verified=True, check_flags=["클릭 기준 — 매출 효과는 측정 안 됨", "광고 플랫폼이 연구 당사자"])
add(id="S3-M-010", type="지표", indicator="S3-T8", importance=3, statement="네이버의 2026년 2분기 광고 매출은 7.5% 늘었고, 회사는 그 성장의 60% 이상이 AI 기반 지면 최적화·타기팅에서 나왔다고 밝혔다. 7월 말 정식 출시한 AI 브리핑 광고는 기존 검색 광고보다 클릭 전환율이 30% 이상, 구매 전환율이 3배 이상 높았다고 한다.",
    value=60, unit="% 이상 (광고 성장 중 AI 기여)", as_of="2026-Q2", region="KR", definition="네이버 광고 매출 성장 중 AI 기여분", extra={"ad_growth": "+7.5%", "briefing_ad_purchase_cvr": "3배 이상"},
    sources=src("naver_q2"), verified=True, check_flags=[PLATFORM])

# ---------- 사건 (E) ----------
add(id="S3-E-001", type="사건", importance=2, statement="컬럼비아·하버드·뮌헨공대·카네기멜런 연구진이 실제 광고 데이터로 AI 생성 광고가 사람 제작 광고와 비슷하거나 약간 더 클릭된다는 연구를 냈다.",
    date="2026-01-28", actor="연구진·Taboola", sources=src("creative"), verified=True)
add(id="S3-E-002", type="사건", importance=2, statement="Gartner가 CMO 예산 조사를 내고, 예산은 그대로인데 AI 도입 성과까지 요구받는 '삼중 압박'을 지적했다. AI 효율화의 가장 큰 장애는 내부 AI 역량 부족(38%)이었다.",
    date="2026-05-11", actor="Gartner", sources=src("gartner"), verified=True)
add(id="S3-E-003", type="사건", importance=2, statement="구글이 검색 광고 문구를 AI가 맥락에 맞춰 쓰는 기능을 몇 달 안에 넣겠다고 발표했다. AI Mode 안 대화형 광고도 시험 중이다.",
    date="2026-05-20", actor="Google", sources=src("gml"), verified=True)
add(id="S3-E-004", type="사건", importance=3, statement="구글이 AI Max가 베타를 마치고 광고주 50만 곳이 쓴다고 밝혔다.",
    date="2026-07-22", actor="Google", sources=src("google_ai"), verified=True)
add(id="S3-E-005", type="사건", importance=3, statement="Meta가 AI 광고 묶음 Advantage+의 연환산 매출이 750억 달러에 이르렀다고 밝혔다.",
    date="2026-07-30", actor="Meta", sources=src("meta_q2"), verified=True)
add(id="S3-E-006", type="사건", importance=2, statement="네이버가 AI 브리핑 답변 안에 들어가는 광고를 정식 출시했다.",
    date="2026-07", actor="네이버", sources=src("naver_q2"), verified=True, check_flags=["정확한 출시일은 원문에 '7월 말'"])

# ---------- 해석 (I) ----------
add(id="S3-I-001", type="해석", importance=3, target="변화의 깊이", direction="강화",
    statement="AI가 가장 깊이 바꾼 곳은 광고 집행과 타기팅이다. 플랫폼 AI가 입찰·지면·대상을 스스로 운영하는 단계에 들어섰고(Advantage+ 연환산 750억 달러, AI Max 광고주 50만 곳), 마케터는 목표와 예산을 정하는 쪽으로 물러났다.",
    basis=["S3-M-004", "S3-M-005", "S3-E-004"])
add(id="S3-I-002", type="해석", importance=3, target="확산의 폭", direction="중립",
    statement="AI는 마케팅 전체가 아니라 몇몇 업무에 몰려 있다. 마케팅 활동 중 AI 비중은 24%지만, 콘텐츠 제작(74%)과 개인화(65%)에 집중되고 고객 예측 분석(42%)·세분화(36%)는 덜 쓰인다.",
    basis=["S3-M-001"])
add(id="S3-I-003", type="해석", importance=3, target="광고 AI의 증분 성과", direction="중립",
    statement="광고 AI의 증분 성과는 엇갈린다. 플랫폼은 같은 수익률에서 전환 15% 증가를 말하지만, 독립 분석에서는 매출이 13% 늘어도 전환당 비용이 16% 올랐고, 홀드아웃 실험에서는 자동 캠페인의 증분 수익률이 수동보다 12% 낮았다. AI 자동화는 '양'은 늘리지만 '효율'은 보장하지 않는다.",
    basis=["S3-M-005", "S3-M-006", "S3-M-007"])
add(id="S3-I-004", type="해석", importance=2, target="콘텐츠", direction="강화",
    statement="콘텐츠는 'AI 생성'이 표준이 됐다. AI 광고는 사람 제작 광고만큼 클릭되고, AI 티가 나지 않을 때 가장 잘 된다. 다만 검증된 것은 클릭까지이고, 주된 효과는 매출 증가보다 제작 비용·속도다.",
    basis=["S3-M-009", "S3-M-001", "S3-M-004"])
add(id="S3-I-005", type="해석", importance=2, target="CRM·개인화", direction="중립",
    statement="CRM의 1:1 개인화 AI는 이탈 방지·교차 판매에서 큰 효과를 보고하지만(구독 갱신율 70%→84%), 근거는 벤더가 의뢰한 사례 연구 수준이다. 독립된 증분 검증은 아직 없다.",
    basis=["S3-M-008"])
add(id="S3-I-006", type="해석", importance=2, target="체감 성과와 예산", direction="강화",
    statement="마케터가 체감하는 AI 성과는 1년 새 커졌지만(매출 생산성 개선 8.6% → 14.1%), 예산은 매출의 7.8%로 그대로다. AI 예산은 늘어난 것이 아니라 기존 예산 안에서 옮겨진 것이고, 준비된 조직은 30%뿐이다.",
    basis=["S3-M-002", "S3-M-003", "S3-E-002"])
add(id="S3-I-007", type="해석", importance=2, target="측정 주도권", direction="약화",
    statement="광고비가 플랫폼 AI 캠페인으로 옮겨갈수록 성과 측정의 주도권도 플랫폼으로 넘어간다. 플랫폼 보고와 독립 실험이 다르게 나오는 만큼, 증분 실험을 직접 돌리는 능력이 마케팅 조직의 핵심 역량이 된다.",
    basis=["S3-M-004", "S3-M-005", "S3-M-007"])
add(id="S3-I-008", type="해석", importance=2, target="한국", direction="강화",
    statement="한국에서도 광고 성장은 플랫폼 AI가 이끈다. 네이버는 광고 성장의 60% 이상을 AI 최적화·타기팅 덕으로 돌렸고, AI 브리핑 답변 속 광고는 구매 전환율이 검색 광고의 3배라고 밝혔다. 모두 플랫폼 자체 보고다.",
    basis=["S3-M-010", "S3-E-006"])

# ---------- 세부 전망 (F) ----------
add(id="S3-F-001", type="전망", importance=2, status="유효", forecast_status="진행 중",
    statement="Meta의 2026년 3분기 광고 매출은 전년보다 20% 이상 늘 것이다.", due="2026-11-15", condition="없음",
    method="Meta 2026년 3분기 실적 확인", basis=["S3-M-004"], result=None)
add(id="S3-F-002", type="전망", importance=2, status="유효", forecast_status="진행 중",
    statement="네이버는 2026년 말까지 AI 브리핑 광고를 쇼핑 또는 로컬 질의로 넓힐 것이다.", due="2026-12-31", condition="없음",
    method="네이버 공식 발표 또는 실적 발표 확인", basis=["S3-E-006", "S3-M-010"], result=None)
add(id="S3-F-003", type="전망", importance=2, status="유효", forecast_status="진행 중",
    statement="네이버의 2026년 4분기 광고 매출 성장률은 2분기(7.5%)보다 높을 것이다.", due="2027-02-28", condition="없음",
    method="네이버 2026년 4분기 실적 확인", basis=["S3-M-010"], result=None)
add(id="S3-F-004", type="전망", importance=3, status="유효", forecast_status="진행 중",
    statement="The CMO Survey 2027에서 마케팅 활동 중 AI 사용 비중은 30% 이상일 것이다.", due="2027-05-31", condition="같은 문항이 유지될 경우",
    method="The CMO Survey 2027 보고서 확인", basis=["S3-M-001"], result=None)
add(id="S3-F-005", type="전망", importance=3, status="유효", forecast_status="진행 중",
    statement="The CMO Survey 2027에서 AI로 인한 매출 생산성 개선 폭은 2026년(14.1%)보다 클 것이다.", due="2027-05-31", condition="같은 문항이 유지될 경우",
    method="The CMO Survey 2027 보고서 확인", basis=["S3-M-002"], result=None)
add(id="S3-F-006", type="전망", importance=2, status="유효", forecast_status="진행 중",
    statement="Gartner CMO Spend Survey 2027에서 마케팅 예산 중 AI 비중은 18% 이상일 것이다.", due="2027-06-30", condition="같은 문항이 유지될 경우",
    method="Gartner CMO Spend Survey 2027 확인", basis=["S3-M-003"], result=None)

# ---------- 메인 질문 시나리오 ----------
add(id="S3-F-101", type="전망", importance=3, status="유효", forecast_status="진행 중", scenario="낙관",
    statement="2027년 말까지 AI가 광고를 넘어 CRM·콘텐츠·고객 이해까지 '운영' 단계로 들어가고, 매출 효과가 마케터 조사에서도 뚜렷해진다. AI 활동 비중이 35%를 넘고 매출 생산성 개선이 20% 이상으로 커지며, AI 예산도 20%를 넘는다.",
    milestones=[
        {"by": "2026-11", "text": "Meta 광고 매출 20% 이상 성장 유지"},
        {"by": "2027-05", "text": "CMO Survey AI 활동 비중 30% 이상, 매출 생산성 개선 확대"},
        {"by": "2027-06", "text": "Gartner AI 예산 비중 18% 이상"}],
    due="2027-12-31", condition="광고 시장 전체가 침체하지 않을 경우",
    method="세 가지 중 두 가지 이상 충족 시 적중: (1) The CMO Survey(2027 또는 2028년판) AI 활동 비중 35% 이상 (2) 같은 조사의 AI 매출 생산성 개선 20% 이상 (3) Gartner 마케팅 예산 중 AI 비중 20% 이상",
    basis=["S3-M-001", "S3-M-002", "S3-M-003"],
    signposts=[{"id": "S3-F-004", "on_hit": "낙관", "on_miss": "비관"}, {"id": "S3-F-005", "on_hit": "낙관", "on_miss": "비관"},
               {"id": "S3-F-006", "on_hit": "낙관", "on_miss": "비관"}, {"id": "S3-F-001", "on_hit": "낙관"},
               {"id": "S3-F-002", "on_hit": "낙관"}, {"id": "S3-F-003", "on_hit": "낙관", "on_miss": "비관"}], result=None)
add(id="S3-F-102", type="전망", importance=3, status="유효", forecast_status="진행 중", scenario="비관",
    statement="2027년 말까지 AI는 광고 플랫폼 안의 자동화와 콘텐츠 제작 비용 절감에 머문다. 독립 실험에서 자동 캠페인의 효율이 계속 엇갈리고, 마케터가 체감하는 매출 효과는 제자리이며, 예산은 늘지 않은 채 측정 주도권만 플랫폼으로 넘어간다.",
    milestones=[
        {"by": "2027-05", "text": "CMO Survey AI 활동 비중 30% 미만"},
        {"by": "2027-06", "text": "AI 예산 비중 정체"},
        {"by": "2027-12", "text": "독립 증분 실험에서 자동 캠페인 열세 지속"}],
    due="2027-12-31", condition="없음",
    method="낙관 시나리오의 판정 조건 세 가지 중 하나 이하만 충족 시 적중",
    basis=["S3-M-006", "S3-M-007", "S3-M-003"], signposts=[], result=None)

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

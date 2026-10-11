"""I3 R1 4유형 기록 생성 + 규칙 검증.
출력: i3/records.jsonl
"""
import json, sys
from pathlib import Path
from collections import Counter

R = "R1"
SRC = {
 "nvda_q2": {"url": "https://www.sec.gov/Archives/edgar/data/0001045810/000104581026000073/q2fy27pr.htm", "publisher": "NVIDIA 실적 발표 (SEC 8-K)", "date": "2026-08-26", "grade": "A"},
 "capex_yahoo": {"url": "https://finance.yahoo.com/sectors/technology/articles/hyperscalers-hit-700-billion-2026-111243744.html", "publisher": "Yahoo Finance", "date": "2026-05-01", "grade": "B"},
 "sk_q2": {"url": "https://www.newsis.com/view/NISX20260729_0003728008", "publisher": "뉴시스 (SK하이닉스 공시)", "date": "2026-07-29", "grade": "B"},
 "lab_rev": {"url": "https://www.sovereignmagazine.com/article/anthropic-65-billion-run-rate-ai-bubble-case", "publisher": "Sovereign Magazine (Bloomberg·Fortune·The Information 인용)", "date": "2026-08-18", "grade": "B"},
 "openai_raise": {"url": "https://techcrunch.com/2026/02/27/chatgpt-reaches-900m-weekly-active-users", "publisher": "TechCrunch", "date": "2026-02-27", "grade": "B"},
 "nvda_hf": {"url": "https://news.bloomberglaw.com/crypto/nvidia-agrees-to-13-billion-deal-for-ai-platform-hugging-face", "publisher": "Bloomberg Law", "date": "2026-09-03", "grade": "B"},
 "af_sept": {"url": "https://af.net/realtime/september-2026-ai-releases-claude-opus-5-5-gpt-6-sol-and-more/", "publisher": "ThursdAI (2026년 9월 출시 정리)", "date": "2026-09-24", "grade": "B"},
 "kr_gpu": {"url": "https://mobile.newsis.com/view/NISX20251101_0003386182", "publisher": "뉴시스", "date": "2025-11-01", "grade": "B"},
}
def src(*keys): return [dict(SRC[k], key=k) for k in keys]

base = dict(question="I3", question_version="v1.0", first_seen=R, last_seen=R, status="유효", replaces=None, check_flags=[])
records = []
def add(**kw):
    r = dict(base); r.update(kw); records.append(r)

# ---------- 지표 (M) ----------
add(id="I3-M-001", type="지표", indicator="I3-T1", importance=3, statement="2026년 1분기 설비투자는 Amazon 442억 달러, Alphabet 357억 달러(전년의 두 배 이상), Microsoft 309억 달러(+84%)였다. Meta는 연간 가이던스를 1,250억~1,450억 달러로 올렸다. 4사 합산 올해 계획은 7천억 달러를 넘는다는 집계가 나온다.",
    value=7000, unit="억 달러 이상(4사 2026 계획, 집계)", as_of="2026-Q1", region="US", definition="빅테크 4사 설비투자", extra={"meta_2026_guidance": "1,250억~1,450억 달러"},
    sources=src("capex_yahoo"), verified=True, check_flags=["4사 합산치는 집계 기관마다 6,500억~7,250억 달러로 다름"])
add(id="I3-M-002", type="지표", indicator="I3-T2", importance=3, statement="NVIDIA의 2026년 5~7월 분기 데이터센터 매출은 890억 달러로 1년 전보다 117% 늘었고, 매출총이익률은 75%였다. 다음 분기 매출 전망은 1,080억 달러다.",
    value=890, unit="억 달러(분기)", as_of="2026-07", region="GLOBAL", definition="NVIDIA 데이터센터 부문 매출", extra={"total_revenue": "962억 달러(+106%)", "gross_margin": "75.0%", "next_q_guide": "1,080억 달러"},
    sources=src("nvda_q2"), verified=True)
add(id="I3-M-003", type="지표", indicator="I3-T3", importance=3, statement="SK하이닉스는 2026년 2분기 매출 79조 3,187억 원, 영업이익 60조 5,426억 원으로 사상 최대를 기록했다. 영업이익률은 76.3%로 NVIDIA(65.6%)보다 높았고 Micron(80.4%) 다음이었다.",
    value=76.3, unit="% (영업이익률)", as_of="2026-Q2", region="KR", definition="SK하이닉스 연결 실적", extra={"revenue": "79.3조 원(+256.8%)", "op_income": "60.5조 원(+557.2%)"},
    sources=src("sk_q2"), verified=True)
add(id="I3-M-004", type="지표", indicator="I3-T4", importance=3, statement="Anthropic의 연환산 매출은 2026년 7월 약 650억 달러로 2025년 초 약 10억 달러에서 크게 늘었다. OpenAI는 8월 약 400억 달러로 2025년 말의 두 배 수준이다.",
    value=650, unit="억 달러(Anthropic 연환산)", as_of="2026-07", region="US", definition="투자자 대상 잠정 연환산 매출", extra={"openai_run_rate": "약 400억 달러(2026-08)"},
    sources=src("lab_rev"), verified=True, check_flags=["감사받지 않은 잠정치 — 주요 언론 보도 기준"])
add(id="I3-M-005", type="지표", indicator="I3-T5", importance=3, statement="Anthropic은 2026년 2분기 잠정 매출 약 115억 달러에 조정 영업이익 흑자를 냈다. OpenAI는 2026년 약 140억 달러 손실을 내부 전망한 것으로 보도됐다.",
    value=-140, unit="억 달러(OpenAI 2026 손실 전망)", as_of="2026-08", region="US", definition="프런티어 연구소 수익성, 보도 기준", extra={"anthropic_q2": "조정 영업이익 흑자, 매출 약 115억 달러"},
    sources=src("lab_rev"), verified=True, check_flags=["회사 공식 재무제표 아님 — 보도 기준"])
add(id="I3-M-006", type="지표", indicator="I3-T6", importance=2, statement="2026년 1분기 Microsoft의 AI 사업 연환산 매출은 370억 달러를 넘어 123% 늘었고, AWS는 15분기 만에 가장 빠른 28% 성장을 기록했다. Google Cloud의 수주 잔고는 한 분기 만에 두 배 가까이 늘어 4,600억 달러를 넘었다.",
    value=370, unit="억 달러(Microsoft AI 연환산)", as_of="2026-Q1", region="US", definition="클라우드 AI 매출·성장률·수주 잔고", extra={"aws_growth": "28%", "gcp_backlog": "4,600억 달러 이상"},
    sources=src("capex_yahoo"), verified=True)
add(id="I3-M-007", type="지표", indicator="I3-T7", importance=2, statement="9월 신모델은 가격을 크게 낮췄다. Claude Opus 5.5는 Fable급 성능을 Opus 5보다 40% 낮은 비용에, GPT-6 Sol은 GPT-5.6의 절반 가격에 내놓았다.",
    value=-50, unit="% (GPT-6 Sol, 전 세대 대비)", as_of="2026-09", region="GLOBAL", definition="같은 등급 모델의 가격 변화", extra={"opus_5_5": "-40% (Opus 5 대비)"}, sources=src("af_sept"), verified=True)
add(id="I3-M-008", type="지표", indicator="I3-T8", importance=2, statement="NVIDIA는 한국에 차세대 GPU 26만 장을 우선 공급하기로 했다. 정부가 약 5만 장을 공공 부문에, 삼성전자·현대차·네이버 등 기업이 약 20만 장을 확보한다.",
    value=26, unit="만 장", as_of="2025-10", region="KR", definition="한국 GPU 공급 약속 물량", sources=src("kr_gpu"), verified=True, check_flags=["공급 기간·기업별 배분 미공개, 공공+기업 합이 25만 장으로 총량과 차이"])

# ---------- 사건 (E) ----------
add(id="I3-E-001", type="사건", importance=2, statement="NVIDIA가 APEC 기간에 한국 정부와 주요 기업에 차세대 GPU 26만 장을 우선 공급하겠다고 밝혔다.",
    date="2025-10-31", actor="NVIDIA·한국 정부", sources=src("kr_gpu"), verified=True)
add(id="I3-E-002", type="사건", importance=3, statement="OpenAI가 기업가치 7,300억 달러(투자 전)로 1,100억 달러를 유치했다. Amazon이 500억 달러, NVIDIA와 SoftBank가 각각 300억 달러를 냈다.",
    date="2026-02-27", actor="OpenAI", sources=src("openai_raise"), verified=True)
add(id="I3-E-003", type="사건", importance=2, statement="Meta가 부품 가격 상승과 데이터센터 비용을 이유로 2026년 설비투자 가이던스를 1,150억~1,350억 달러에서 1,250억~1,450억 달러로 올렸다.",
    date="2026-04", actor="Meta", sources=src("capex_yahoo"), verified=True)
add(id="I3-E-004", type="사건", importance=2, statement="SK하이닉스가 2분기 사상 최대 실적을 내고 HBM4 양산 출하를 시작했다. 2027년 물량·가격 협상이 순조롭다고 밝혔다.",
    date="2026-07-29", actor="SK하이닉스", sources=src("sk_q2"), verified=True)
add(id="I3-E-005", type="사건", importance=3, statement="NVIDIA가 분기 매출 962억 달러를 발표하며 Vera Rubin이 전면 양산에 들어갔다고 밝혔다. 다음 분기 전망에서는 중국 데이터센터 매출을 0으로 잡았다.",
    date="2026-08-26", actor="NVIDIA", sources=src("nvda_q2"), verified=True)
add(id="I3-E-006", type="사건", importance=3, statement="NVIDIA가 오픈소스 AI 플랫폼 Hugging Face를 약 130억 달러에 인수하기로 했다.",
    date="2026-09-03", actor="NVIDIA", sources=src("nvda_hf"), verified=True)
add(id="I3-E-007", type="사건", importance=2, statement="Anthropic(Opus 5.5)과 OpenAI(GPT-6 Sol)가 같은 달 이전 세대보다 40~50% 싼 신모델을 내놓았다.",
    date="2026-09", actor="Anthropic·OpenAI", sources=src("af_sept"), verified=True, check_flags=["정확한 출시일은 원문에 없음"])

# ---------- 해석 (I) ----------
add(id="I3-I-001", type="해석", importance=3, target="투자 곡선", direction="강화",
    statement="빅테크의 AI 투자는 꺾이지 않고 오히려 올라가고 있다. 분기 설비투자가 1년 새 두 배 가까이 늘었고, 부품값 상승까지 겹쳐 연간 계획이 상향되고 있다.",
    basis=["I3-M-001", "I3-E-003"])
add(id="I3-I-002", type="해석", importance=3, target="이익이 먼저 나는 곳", direction="강화",
    statement="투자한 돈을 가장 먼저 이익으로 바꾸는 곳은 칩과 메모리다. NVIDIA는 매출총이익률 75%, SK하이닉스는 영업이익률 76%로, 공급이 수요를 못 따라가는 층이 가장 큰 몫을 가져간다.",
    basis=["I3-M-002", "I3-M-003", "I3-E-004"])
add(id="I3-I-003", type="해석", importance=3, target="수익 곡선", direction="강화",
    statement="수익 곡선도 빠르게 올라오고 있다. Anthropic 연환산 매출은 1년 반 새 수십 배로, Microsoft AI 매출은 두 배 넘게 늘었다. 수익의 증가 속도가 투자의 증가 속도보다 빨라 두 곡선의 간격은 좁혀지기 시작했지만, 절대 규모는 아직 투자가 크다.",
    basis=["I3-M-004", "I3-M-006", "I3-M-001"])
add(id="I3-I-004", type="해석", importance=3, target="모델 기업 수익성", direction="중립",
    statement="모델 기업의 수익성은 갈렸다. Anthropic은 분기 조정 영업이익 흑자로 돌아섰고 매출에서도 OpenAI를 앞섰지만, OpenAI는 연간 대규모 손실이 예상된다.",
    basis=["I3-M-005", "I3-M-004"])
add(id="I3-I-005", type="해석", importance=2, target="모델 가격", direction="약화",
    statement="모델 가격은 세대마다 절반 가까이 내려가고 있다. 이용량 확대에는 도움이 되지만, 모델 판매의 마진에는 압박이 된다.",
    basis=["I3-M-007", "I3-E-007"])
add(id="I3-I-006", type="해석", importance=2, target="순환 투자와 수직 확장", direction="중립",
    statement="칩 회사가 고객에게 투자하고 생태계를 사들이는 흐름이 커지고 있다. NVIDIA는 OpenAI에 300억 달러를 넣고 Hugging Face를 인수했다. 공급자와 고객의 돈이 서로 얽혀, 수요의 독립성을 따져 봐야 하는 구조가 됐다.",
    basis=["I3-E-002", "I3-E-006"])
add(id="I3-I-007", type="해석", importance=2, target="한국", direction="강화",
    statement="한국은 메모리 호황의 최대 수혜국이면서 GPU 26만 장으로 수요자 쪽 기반도 마련했다. 다만 이익은 메모리 공급에 몰려 있고, 국내 모델·서비스 매출은 아직 보이지 않는다.",
    basis=["I3-M-003", "I3-M-008", "I3-E-001"])

# ---------- 세부 전망 (F) ----------
add(id="I3-F-001", type="전망", importance=2, status="유효", forecast_status="진행 중",
    statement="NVIDIA의 2026년 8~10월 분기 매출은 가이던스 하단(1,058억 달러) 이상일 것이다.", due="2026-11-30", condition="없음",
    method="NVIDIA 3분기(FY2027) 실적 발표 확인", basis=["I3-M-002"], result=None)
add(id="I3-F-002", type="전망", importance=3, status="유효", forecast_status="진행 중",
    statement="빅테크 4사의 2027년 설비투자 계획 합계는 2026년보다 클 것이다.", due="2027-02-28", condition="4사 모두 연간 계획을 밝힐 경우",
    method="Amazon·Microsoft·Alphabet·Meta 2026년 4분기 실적 발표의 2027년 계획 확인", basis=["I3-M-001", "I3-E-003"], result=None)
add(id="I3-F-003", type="전망", importance=3, status="유효", forecast_status="진행 중",
    statement="Anthropic의 연환산 매출은 2026년 말 1,000억 달러 이상으로 보도될 것이다.", due="2027-01-31", condition="없음",
    method="회사 발표 또는 주요 언론(Bloomberg 등) 보도 확인", basis=["I3-M-004"], result=None)
add(id="I3-F-004", type="전망", importance=2, status="유효", forecast_status="진행 중",
    statement="OpenAI의 2026년 실제 손실은 내부 전망(약 140억 달러)보다 클 것으로 보도될 것이다.", due="2027-03-31", condition="없음",
    method="회사 발표 또는 주요 언론 보도 확인", basis=["I3-M-005"], result=None)
add(id="I3-F-005", type="전망", importance=2, status="유효", forecast_status="진행 중",
    statement="SK하이닉스의 2026년 3분기 영업이익은 2분기(60조 5,426억 원) 이상일 것이다.", due="2026-10-31", condition="없음",
    method="SK하이닉스 3분기 실적 공시 확인", basis=["I3-M-003", "I3-E-004"], result=None)
add(id="I3-F-006", type="전망", importance=2, status="유효", forecast_status="진행 중",
    statement="2027년 6월 말까지 빅테크나 OpenAI가 대형 AI 데이터센터 프로젝트의 취소나 연기를 공식 발표할 것이다.", due="2027-06-30", condition="없음",
    method="각 사 공식 발표·실적 발표 확인", basis=["I3-M-001", "I3-M-005"], result=None)

# ---------- 메인 질문 시나리오 ----------
add(id="I3-F-101", type="전망", importance=3, status="유효", forecast_status="진행 중", scenario="낙관",
    statement="2027년 말까지 수익 곡선이 투자 곡선을 따라잡기 시작한다. 프런티어 연구소 매출 합계가 연 2,000억 달러를 넘고 연간 흑자 기업이 나오며, 빅테크는 2027년에도 투자를 늘린다. 칩·메모리의 높은 이익도 유지된다.",
    milestones=[
        {"by": "2026-11", "text": "NVIDIA·SK하이닉스 다음 분기 실적이 직전 분기 이상"},
        {"by": "2027-01", "text": "Anthropic 연환산 매출 1,000억 달러 이상"},
        {"by": "2027-02", "text": "빅테크 2027년 설비투자 계획이 2026년보다 큼"}],
    due="2027-12-31", condition="거시 경기 침체나 수출 통제 확대로 수요가 급감하지 않을 경우",
    method="세 가지 중 두 가지 이상 충족 시 적중: (1) Anthropic+OpenAI 연환산 매출 합계 2,000억 달러 이상 (2) 둘 중 하나의 연간 영업이익(조정 포함) 흑자 공식 확인 (3) 빅테크 4사 2027년 설비투자 계획 합계가 2026년보다 큼",
    basis=["I3-M-004", "I3-M-005", "I3-M-001", "I3-M-002"],
    signposts=[{"id": "I3-F-001", "on_hit": "낙관", "on_miss": "비관"}, {"id": "I3-F-002", "on_hit": "낙관", "on_miss": "비관"},
               {"id": "I3-F-003", "on_hit": "낙관", "on_miss": "비관"}, {"id": "I3-F-004", "on_hit": "비관"}, {"id": "I3-F-005", "on_hit": "낙관"}, {"id": "I3-F-006", "on_hit": "비관"}], result=None)
add(id="I3-F-102", type="전망", importance=3, status="유효", forecast_status="진행 중", scenario="비관",
    statement="2027년 말까지 가격 인하와 손실 탓에 수익 곡선의 기울기가 꺾이고, 빅테크가 투자 속도를 조정하며 일부 데이터센터 계획이 미뤄진다. 메모리 가격이 내려가 공급망 이익도 줄어든다.",
    milestones=[
        {"by": "2027-02", "text": "빅테크 2027년 설비투자 계획이 2026년 수준 이하"},
        {"by": "2027-03", "text": "OpenAI 2026년 손실이 전망보다 큼"},
        {"by": "2027-06", "text": "대형 데이터센터 프로젝트 취소·연기 발표"}],
    due="2027-12-31", condition="없음",
    method="낙관 시나리오의 판정 조건 세 가지 중 하나 이하만 충족 시 적중",
    basis=["I3-M-007", "I3-M-005", "I3-E-002"],
    signposts=[], result=None)

# ---------- 2026-10-11 검증 반영 (probe_20261011) ----------
CHG = "2026-10-11"
SRC.update({
 "meta_q2": {"url": "https://investor.atmeta.com/investor-news/press-release-details/2026/Meta-Reports-Second-Quarter-2026-Results/", "publisher": "Meta 2026년 2분기 실적 릴리스", "date": "2026-07-29", "grade": "A"},
 "amzn_q2": {"url": "https://s2.q4cdn.com/299287126/files/doc_earnings/2026/q2/earnings-result/AMZN-Q2-2026-Earnings-Release.pdf", "publisher": "Amazon 2026년 2분기 실적 릴리스", "date": "2026-07-30", "grade": "A"},
 "platformonomics": {"url": "https://platformonomics.com/2026/07/follow-the-capex-q2-2026-scoreboard/", "publisher": "Platformonomics (Follow the CAPEX Q2 2026)", "date": "2026-07", "grade": "B"},
 "tnw_goog": {"url": "https://thenextweb.com/news/alphabet-q2-2026-capex-205bn-cloud-82", "publisher": "The Next Web (Alphabet 2분기)", "date": "2026-07-23", "grade": "B"},
 "fool_msft": {"url": "https://www.fool.com/earnings/call-transcripts/2026/08/07/microsoft-msft-q4-2026-earnings-call-transcript/", "publisher": "Motley Fool (Microsoft FY26 4분기 콜 녹취)", "date": "2026-07-29", "grade": "B"},
 "epoch": {"url": "https://epoch.ai/gradient-updates/an-update-on-ais-most-important-number", "publisher": "Epoch AI (OpenAI·Anthropic 매출 비교)", "date": "2026-08", "grade": "B"},
 "roic_openai": {"url": "https://www.roic.ai/news/openai-adds-more-consumer-revenue-in-q3-than-in-all-of-last-year-source-says-09-29-2026", "publisher": "Roic News (Axios 인용, OpenAI 연환산 약 700억)", "date": "2026-09-29", "grade": "B"},
 "digg_openai": {"url": "https://digg.com/tech/g9qgeu1y", "publisher": "Digg (Axios 요약)", "date": "2026-09-29", "grade": "B"},
 "aimag_anth": {"url": "https://aimagazine.com/news/how-anthropics-revenue-run-rate-topped-us-65bn", "publisher": "AI Magazine (Anthropic 650억, Reuters 인용)", "date": "2026-08-18", "grade": "B"},
 "futurum_amzn": {"url": "https://futurumgroup.com/?p=93531", "publisher": "Futurum (Amazon 2분기)", "date": "2026-08-04", "grade": "B"},
 "startuphub": {"url": "https://www.startuphub.ai/news/figure-satya-nadella-company-financial-breakdown-2026-07-24", "publisher": "StartupHub (Microsoft AI 370억 공시 시점)", "date": "2026-07-24", "grade": "B"},
 "upperedge": {"url": "https://upperedge.com/cloud/aws-hits-37-growth-azure-tops-100b-gcp-launches-flexible-savings-plan-what-q2-2026-earnings-mean-for-enterprise-cloud-contracts/", "publisher": "UpperEdge (클라우드 2분기)", "date": "2026-08-13", "grade": "B"},
 "tnw_openai_q1": {"url": "https://thenextweb.com/news/openai-burned-3-7-billion-q1-2026", "publisher": "The Next Web (OpenAI 1분기 현금 소진, The Information 인용)", "date": "2026-06-17", "grade": "B"},
 "zitron": {"url": "https://wheresyoured.at/news-openai-had-a-negative-122-operating-margin-in-q1-2026-and-chatgpt-growth-has-stalled", "publisher": "Where's Your Ed At (The Information 인용, OpenAI 1분기)", "date": "2026-05-22", "grade": "B"},
 "futurum_anth": {"url": "https://futurumgroup.com/insights/anthropic-files-for-ipo-looking-to-beat-openai-to-the-punch/", "publisher": "Futurum (Anthropic IPO 서류 제출)", "date": "2026-06-02", "grade": "B"},
 "samsung_q2": {"url": "https://news.samsung.com/global/samsung-electronics-announces-second-quarter-2026-results", "publisher": "Samsung Electronics 2026년 2분기 실적 발표", "date": "2026-07-30", "grade": "A"},
 "ytn_samsung": {"url": "https://www.ytn.co.kr/_ln/0102_202610080945200200", "publisher": "YTN (삼성전자 3분기 잠정)", "date": "2026-10-08", "grade": "B"},
 "segye_hbm": {"url": "https://www.segye.com/newsView/20260729502603", "publisher": "세계일보 (HBM 점유율, Counterpoint 인용)", "date": "2026-07-29", "grade": "B"},
 "micron_q4": {"url": "https://www.sec.gov/Archives/edgar/data/0000723125/000072312526000018/a2026q4ex991-pressrelease.htm", "publisher": "Micron FQ4 2026 실적 (SEC 8-K)", "date": "2026-09-30", "grade": "A"},
 "nextplatform": {"url": "https://www.nextplatform.com/store/2026/10/02/microns-numbers-show-why-hbm4-memory-is-worth-15x-its-weight-in-gold/5300701", "publisher": "The Next Platform (Micron HBM 해설)", "date": "2026-10-02", "grade": "B"},
 "nvda_hf_8k": {"url": "https://www.sec.gov/Archives/edgar/data/0001045810/000104581026000078/nvda-20260902.htm", "publisher": "NVIDIA 8-K (Hugging Face 인수 계약)", "date": "2026-09-03", "grade": "A"},
 "anthropic_price": {"url": "https://platform.claude.com/docs/en/about-claude/pricing", "publisher": "Anthropic 가격표 (platform.claude.com)", "date": "2026-10-11", "grade": "A"},
 "mtn_gpu": {"url": "https://news.mtn.co.kr/news-detail/2026081108563068126", "publisher": "MTN (삼성SDS 국가 AI 인프라, 해남 착공)", "date": "2026-08-11", "grade": "B"},
})
def _get(i): return next(r for r in records if r["id"] == i)
def revise(i, kind, why, **ch):
    r = _get(i)
    r.setdefault("revisions", []).append({"on": CHG, "kind": kind, "before": r.get("statement") if "statement" in ch else None, "why": why})
    r.update(ch)
def _more(i, *keys): return _get(i)["sources"] + src(*keys)

# --- 신규 지표 (판정 영향·문장 수정에 필요한 것만) ---
add(id="I3-M-009", type="지표", indicator="I3-T1", importance=3, added_on=CHG,
    statement="2026년 2분기 빅테크의 잉여현금흐름(FCF)이 나빠졌다. Alphabet은 2분기 FCF가 -59억 달러로 첫 분기 유출이고(약 20년 만이라는 보도) 약 400억 달러 규모의 주식 매각(ATM)을 시작한다고 보도됐다. Amazon은 최근 12개월 FCF가 -76억 달러(전년 +182억), Meta는 2분기 FCF가 7.8억 달러(전년 85.5억)다. 4사 합산 최근 12개월 FCF는 전 분기보다 18%, 1년 전보다 24% 줄었다는 집계가 있다.",
    value=-76, unit="억 달러(Amazon 최근 12개월 FCF)", as_of="2026-Q2", region="US", definition="빅테크 잉여현금흐름",
    extra={"alphabet_q2_fcf": "-59억 달러", "meta_q2_fcf": "7.8억 달러(전년 85.5억)", "big4_ttm_fcf_change": "전 분기 -18%, 전년 -24%(Platformonomics)"},
    sources=src("amzn_q2", "meta_q2", "tnw_goog", "platformonomics"), verified=True,
    check_flags=["Alphabet FCF·ATM 규모와 4사 합산 증감은 B등급 보도·집계 기준 — 확인 필요", "FCF 정의(리스 원금 포함 여부)가 회사마다 다를 수 있음"])
add(id="I3-M-010", type="지표", indicator="I3-T3", importance=2, added_on=CHG,
    statement="Micron은 9월 30일 FQ4(9월 3일 종료) 매출 542.3억 달러(전년 113.2억), GAAP 영업이익 437.5억 달러(영업이익률 80.7%), GAAP 매출총이익률 86.8%를 발표했고 FQ1 매출 가이던스는 615억±15억 달러다. 2027년 HBM 물량 대부분을 이미 계약했고 가격 인상이 포함된다는 CEO 발언이 해설 매체를 통해 인용됐다(확인 필요).",
    value=80.7, unit="% (Micron FQ4 영업이익률)", as_of="2026-09", region="US", definition="Micron 분기 실적(GAAP)",
    extra={"revenue": "542.3억 달러", "gross_margin": "86.8%", "fq1_guide": "615억±15억 달러"},
    sources=src("micron_q4", "nextplatform"), verified=True,
    check_flags=["HBM 계약·가격 인상 발언은 Micron 릴리스에 없고 해설 매체(B) 인용 — 확인 필요", "HBM 매출 추정치는 제3자 추정이라 쓰지 않음"])

# --- 지표 ---
revise("I3-M-001", "갱신", "기록은 1분기 값이고 2분기 실적이 이미 나와 있었다. 4사 정의가 달라 단순 합산은 근사치다(Amazon 현금 PP&E 매입, Meta·Microsoft 금융리스 포함). 연간 계획 합계는 7,000억 달러 이상에서 7,200억~7,450억 달러로 바뀐다.",
    statement="2026년 2분기 설비투자는 Amazon 약 542억 달러(현금 PP&E 매입, 금융리스 포함 집계 548억), Alphabet 449억(전년 약 2배), Microsoft 410억(금융리스 56억 포함, 회계연도 4분기), Meta 311억(금융리스 원금 포함)으로 4사 합계 약 1,720억 달러(+77% YoY)다. 1분기는 Amazon 442억, Alphabet 357억, Microsoft 309억 달러였다. 연간 계획은 Amazon 약 2,200억(기존 2,000억), Alphabet 1,950억~2,050억, Meta 1,300억~1,450억, Microsoft 2026 캘린더연도 약 1,750억(회계 처리 변경 전 약 1,900억)으로 합계 약 7,200억~7,450억 달러다.",
    value=7200, unit="억 달러 이상(4사 2026 계획 합계 7,200억~7,450억)", as_of="2026-Q2",
    extra={"meta_2026_guidance": "1,300억~1,450억 달러(7월 좁힘)", "q2_total": "약 1,720억 달러(+77% YoY)", "q1": "Amazon 442억·Alphabet 357억·Microsoft 309억 달러"},
    check_flags=["4사 합산은 정의가 달라 근사치(Amazon 현금 PP&E, Meta·Microsoft 금융리스 포함)", "Amazon 연간 2,200억·Alphabet 하단 1,950억은 B등급 출처에서만 확인(Amazon 릴리스에 가이던스 문구 없음) — 확인 필요", "Alphabet 가이던스 하단 표기가 출처마다 다름(1,800~1,900억에서 상향, 최대 2,050억)", "Microsoft 2026 캘린더연도 약 1,750억은 내용연수·리스 분류 변경 후 값(변경 전 약 1,900억), 실지출 불변은 해설 추정", "집계 기관별 합산 차이(Platformonomics 표 합계는 행 합과 불일치)"],
    sources=_more("I3-M-001", "meta_q2", "amzn_q2", "platformonomics", "tnw_goog", "fool_msft"))
revise("I3-E-003", "갱신", "7월 29일 하단이 1,250억에서 1,300억 달러로 올랐다(공식 릴리스 기준). 출처마다 직전 시작점이 달라 공식 릴리스 값을 쓴다.",
    statement="Meta가 4월 부품 가격 상승과 데이터센터 비용을 이유로 2026년 설비투자 가이던스를 1,150억~1,350억 달러에서 1,250억~1,450억 달러로 올렸고, 7월 29일에는 1,300억~1,450억 달러(금융리스 원금 포함)로 좁혔다. 총비용 가이던스는 1,650억~1,690억 달러다.",
    date="2026-07-29", sources=_more("I3-E-003", "meta_q2"),
    check_flags=["출처마다 직전 시작점이 다름(Platformonomics는 1,250~1,400억) — 공식 릴리스 기준 사용"])
revise("I3-M-003", "누락정정", "삼성전자가 빠져 있었다. 2분기 이익 규모는 삼성전자 DS(영업이익 89.2조 원)가 SK하이닉스(60.5조 원)보다 컸다. 영업이익률 65.6%·80.4%는 집계 기간이 불분명했고, 시점·정의를 맞추면 NVIDIA 66.2%(GAAP, 릴리스 값에서 계산), Micron 80.7%(FQ4)다. 순위(Micron > SK하이닉스 > NVIDIA)는 같다.",
    statement="SK하이닉스는 2026년 2분기 매출 79조 3,187억 원, 영업이익 60조 5,426억 원으로 사상 최대를 기록했고 영업이익률은 76.3%였다. 같은 분기 삼성전자 DS(반도체) 부문은 매출 127.5조 원, 영업이익 89.2조 원(약 70%)으로 이익 규모가 더 컸다. 영업이익률은 NVIDIA 66.2%(FY27 2분기 GAAP, 릴리스 값에서 계산), Micron 80.7%(FQ4)로, 시점·정의를 맞춘 순위는 Micron > SK하이닉스 > NVIDIA다. 삼성전자 3분기 잠정은 매출 195조 원, 영업이익 107.4조 원(이익률 55.1%, 10월 8일 발표, 부문별 수치 미공개)이다. HBM 매출 점유율은 SK하이닉스 58%, 삼성전자·Micron 각 21%다(Counterpoint, 2026년 1분기).",
    check_flags=["메모리 층 선두는 이익 규모(삼성 DS)·이익률(Micron)·HBM 점유율(SK하이닉스) 기준에 따라 갈림 — 층 판정 '굳어짐'은 유지", "삼성전자 3분기 잠정은 공시 원문(DART) 미열람, 부문별 수치 없어 DS 이익 추정 불가 — 확인 필요", "삼성전자 HBM 점유율·물량은 비공개", "총이익률(NVIDIA 75.0%, Micron 86.8%)과 영업이익률은 정의가 달라 섞어 쓰지 않음"],
    sources=_more("I3-M-003", "samsung_q2", "ytn_samsung", "segye_hbm", "micron_q4", "nvda_q2"))
revise("I3-M-004", "갱신", "OpenAI 연환산이 9월 말 약 700억 달러에 근접했다는 보도가 나왔다(익명 소식통, 원문·회사 확인 필요). 8월 약 400억은 그 직전 값이다. Anthropic은 7월 말 650억 이상이 가장 최근 확인값이다.",
    statement="Anthropic의 연환산 매출은 2026년 5월 말 약 470억 달러에서 7월 말 650억 달러 이상으로 늘었다(2025년 초 약 10억 달러). OpenAI는 8월 약 400억 달러였고, 9월 말 약 700억 달러에 근접했다는 보도가 나왔다(Axios 최초, 익명 소식통, 3분기 초 대비 +70% 이상, B2B 2배 이상 — 확인 필요). Anthropic의 8~9월 최신값은 확인하지 못했다. Anthropic은 총액, OpenAI는 순액으로 매출을 인식해 직접 비교할 수 없다.",
    extra={"openai_run_rate": "약 400억 달러(2026-08), 약 700억 달러 근접(2026-09 말, 익명 소식통 보도)", "anthropic_may": "약 470억 달러(5월 말)"},
    check_flags=["감사받지 않은 잠정치 — 주요 언론 보도 기준", "OpenAI 약 700억은 Axios 단독 보도의 재인용(B) — Axios 원문·회사 확인 필요", "Anthropic 8~9월 최신 연환산 미확인(투자자 기대 연말 1,000억~1,200억은 FT 재인용)", "Anthropic 총액·OpenAI 순액 인식으로 비교 기준이 다름"],
    sources=_more("I3-M-004", "roic_openai", "digg_openai", "epoch", "aimag_anth"))
revise("I3-M-005", "상충", "OpenAI '2026년 약 140억 달러 손실 내부 전망'은 원 보도(The Information)를 확인하지 못했고 1월 시점 값이 재인용됐을 수 있어 '보도 기준'으로 낮췄다. 확인되는 값은 1분기 매출·현금 소진이다. Anthropic 2분기 흑자는 조정 기준·비감사 회사 보고 수치이고, 회사는 이후 분기 적자 복귀 가능성을 경고했다.",
    statement="OpenAI의 '2026년 약 140억 달러 손실 내부 전망'은 원 보도(The Information)를 확인하지 못했고 1월 시점 값이 재인용됐을 가능성이 있다(확인 필요). 확인되는 값은 2026년 1분기 매출 약 57억 달러와 현금 소진 약 37억 달러(The Information 인용 보도)이고, 조정 영업마진 -122%(주식보상 등 제외)는 해설 매체 경유 값이다. Anthropic은 2분기 매출 약 115억 달러와 조정 영업이익 흑자를 냈다고 보도됐으며, 회사 보고·비감사 수치이고 회사는 이후 분기 적자 복귀 가능성을 경고했다.",
    unit="억 달러(OpenAI 2026 손실 전망, 보도 기준·원문 미확인)",
    check_flags=["회사 공식 재무제표 아님 — 보도 기준", "140억 달러 손실 전망은 원 보도 미확인, 1월 시점 값이 재인용됐을 가능성 — 확인 필요", "1분기 하나로 연 140억 가정과 부합하는지 불분명(-122%×57억은 해설자 계산)", "-122% 조정 영업마진은 해설 매체 경유 — 확인 필요", "Anthropic 2분기 매출 115억은 6월 전망치 109억과 다르고 공시 전 수치", "Anthropic 2025년 영업손실 등은 C등급 단일 출처(유출 초안 재인용)라 제외"],
    sources=_more("I3-M-005", "tnw_openai_q1", "zitron", "futurum_anth"))
revise("I3-M-006", "갱신", "기록의 1분기 값(AWS 28%, Google 수주 잔고 4,600억 달러)이 한 분기 낡았다. Microsoft AI 연환산 370억·+123%는 4월 29일 발표분이며 7월 콜에서 갱신 수치는 확인되지 않았다.",
    statement="2026년 2분기(Microsoft 회계 4분기) AWS 매출은 422억 달러(+37%, 영업이익 166억·이익률 39.4%), Azure는 +43%(고정환율, 연 매출 1,000억 달러 돌파), Google Cloud는 매출 248억 달러(+82%, 영업이익률 35.6%)다. 수주 잔고는 Google 5,140억, AWS 4,960억, Microsoft 상업 RPO 6,780억(+84%, OpenAI 제외 +25%) 달러다. Microsoft AI 연환산 370억 달러(+123%)는 4월 29일 발표한 3월 말 값이며, 7월 콜에서 갱신된 수치는 확인되지 않았다.",
    unit="억 달러(Microsoft AI 연환산, 3월 말 발표)", as_of="2026-Q2",
    extra={"aws_growth": "37%(2분기)", "azure_growth": "43%(고정환율)", "gcp_backlog": "5,140억 달러(2분기)", "aws_backlog": "4,960억 달러", "msft_rpo": "6,780억 달러(+84%, OpenAI 제외 +25%)", "q1": "AWS +28%, Google 수주 잔고 4,600억 달러 이상"},
    check_flags=["AWS 백로그는 Futurum(B) 인용, 릴리스에는 없음 — 확인 필요", "Google Cloud 매출·백로그는 TNW·UpperEdge(B)이며 전 분기 백로그는 4,600억과 4,900억으로 출처가 갈림", "Azure는 달러 매출·영업이익 비공개, 고정환율과 보고 기준이 섞임", "Microsoft AI 370억은 3월 말 값으로 이후 갱신 미확인"],
    sources=_more("I3-M-006", "amzn_q2", "futurum_amzn", "upperedge", "fool_msft", "tnw_goog", "startuphub"))
revise("I3-M-007", "상충", "Claude Opus 5.5의 공식 정가는 Opus 5보다 20% 낮아 '40% 낮은 비용'과 맞지 않는다. 40%는 출처 문구(성능 기준 비용)라 단가 하락률로 읽을 수 없고, GPT-6 Sol의 약 50%는 공식 가격표로 확인하지 못했다.",
    statement="Claude Opus 5.5의 정가는 입력 $4·출력 $20로 Opus 5($5/$25)보다 20% 낮다(Anthropic 가격표). 9월 출시 정리 글은 '40% 낮은 비용'(같은 성능 기준 총비용인지 토큰 단가인지 불명확)과 GPT-6 Sol이 GPT-5.6의 절반 가격이라고 적었으나, 후자는 공식 가격표로 확인하지 못했다(확인 필요).",
    value=-20, unit="% (Claude Opus 5.5 단가, Opus 5 대비)", extra={"opus_5_5": "입력 $4·출력 $20 (Opus 5 $5/$25 대비 -20%)", "gpt_6_sol": "GPT-5.6 대비 약 -50%는 집계 사이트(C) 값, 공식 가격표 미확인", "article_claim": "Opus 5.5 -40%(성능 기준 비용 문구)"},
    check_flags=["GPT-6 Sol 약 -50%는 공식 가격표 미확인(OpenAI 가격표 미열람) — 확인 필요", "'40% 낮은 비용'은 같은 성능 기준 총비용 표현으로 단가와 다름", "같은 달 상위 등급 GPT-6 Astra는 입력 $10·출력 $50(제공처별 상이, 집계 C)", "'같은 등급' 비교는 신모델 성능이 오르면 기준이 불명확"],
    sources=_more("I3-M-007", "anthropic_price"))
revise("I3-M-008", "갱신", "26만 장은 '우선 공급 약속'이고 배분(정부 약 5만, 기업 약 20만)·공급 일정은 미공개다. 이후 해남 국가AI컴퓨팅센터 착공과 삼성SDS 연구용 GPU 공급이 있었으나 2026년 실제 도입 장수는 확인하지 못했다.",
    statement="NVIDIA의 한국 공급 26만 장은 '우선 공급 약속'이며 배분은 정부 약 5만, 삼성전자·현대차·네이버 등 기업 약 20만이다(회사별 수치·공급 일정 미공개). 이후 해남 국가AI컴퓨팅센터가 2026년 8월 3일 착공(2.5조 원, 2028년 전면 가동)했고 삼성SDS가 연구용 GPU(H100·B300)를 7월 20일부터 공급한다.",
    check_flags=["공급 기간·기업별 배분 미공개, 공공+기업 합이 25만 장으로 총량과 차이", "2026년 실제 도입 장수는 확인하지 못함 — 확인 필요", "삼성SDS 7월 20일·해남 8월 3일은 기사 표현('지난달 20일', '지난 3일')에서 추정한 날짜"],
    sources=_more("I3-M-008", "mtn_gpu"))

# --- 사건 ---
revise("I3-E-006", "갱신", "8-K 기준 인수가는 약 119억 달러에 직원 보유 프로그램 최대 약 10억 달러가 별도이고(언론은 약 130억), 종결 전이며 개방·다중 칩 지원 유지를 공시했다.",
    statement="NVIDIA가 9월 2일 오픈소스 AI 플랫폼 Hugging Face 인수 계약을 체결했다(SEC 8-K 9월 3일). 인수가는 약 119억 달러에 직원 보유 프로그램 최대 약 10억 달러가 별도다(언론 보도는 약 130억). 종결은 2027년 상반기·규제 승인을 전제로 하며, NVIDIA는 플랫폼을 계속 개방하고 다른 칩 업체 지원도 유지한다고 공시했다.",
    sources=_more("I3-E-006", "nvda_hf_8k"))
revise("I3-E-007", "상충", "공식 가격표 기준 Opus 5.5는 Opus 5보다 20% 낮고, GPT-6 Sol의 약 50%는 공식 확인이 없다. '40~50% 싼 신모델'은 같은 단서가 필요하다.",
    statement="9월에 Anthropic이 Opus 5.5를, OpenAI가 GPT-6 Sol을 이전 세대보다 낮은 가격에 내놓았다는 정리가 나왔다. 공식 가격표 기준 Opus 5.5는 Opus 5보다 20% 낮고, GPT-6 Sol의 약 50% 인하는 공식 가격표로 확인하지 못했다(확인 필요).",
    check_flags=["정확한 출시일은 원문에 없음", "GPT-6 Sol 인하율은 공식 가격표 미확인 — 확인 필요"], sources=_more("I3-E-007", "anthropic_price"))

# --- 해석 ---
revise("I3-I-001", "누락정정", "투자 증가만 적고 재원 쪽 근거가 빠져 있었다. 2분기 빅테크 잉여현금흐름이 나빠졌다(Alphabet 분기 -59억 달러 등). '투자는 올라가고 수익도 빨리 올라온다'는 서술에 반대 측 근거를 더한다. 방향('강화')은 유지한다.",
    statement="빅테크의 AI 투자는 꺾이지 않고 오히려 올라가고 있다. 2분기 4사 설비투자는 약 1,720억 달러로 1년 새 77% 늘었고, 연간 계획도 상향되고 있다. 다만 투자 재원은 잉여현금에서 나오지 않는다. Alphabet은 2분기 FCF가 -59억 달러로 첫 분기 유출이고, Amazon은 최근 12개월 FCF가 -76억 달러이며, Meta의 2분기 FCF는 7.8억 달러(전년 85.5억)로 줄었다.",
    basis=["I3-M-001", "I3-E-003", "I3-M-009"],
    check_flags=["'간격이 좁혀진다'는 매출 증가 속도 대 투자 증가 속도의 비교이며 이익·현금으로의 회수를 뜻하지 않음"])
revise("I3-I-002", "상충", "NVIDIA 매출총이익률(75%)과 SK하이닉스 영업이익률(76%)은 정의가 다른 값이다. NVIDIA 영업이익률은 66.2%이고, 이익 규모는 삼성전자 DS가 가장 크며, Micron 최신 분기 영업이익률은 80.7%다.",
    statement="투자한 돈을 가장 먼저 이익으로 바꾸는 곳은 칩과 메모리다. NVIDIA는 매출총이익률 75%(영업이익률 66%), SK하이닉스는 영업이익률 76%, Micron은 최신 분기 영업이익률 81%로, 공급이 수요를 못 따라가는 층이 가장 큰 몫을 가져간다. 이익 규모로는 삼성전자 DS 부문(2분기 영업이익 89.2조 원)이 가장 크다.",
    basis=["I3-M-002", "I3-M-003", "I3-E-004", "I3-M-010"])
revise("I3-I-003", "상충", "수익 곡선 합계 '약 1,420억 달러'는 시점이 7월·8월·3월 말로 섞여 있다. 최신 보도값(OpenAI 9월 말 약 700억)을 쓰면 약 1,720억 달러로 연간 투자 계획의 약 4.2~4.3배이고, 확인된 값(OpenAI 8월 400억) 기준은 약 5배다. OpenAI 700억은 익명 소식통 보도라 칩 문구('투자 5배')는 유지하고 본문에 두 값을 함께 적는다.",
    statement="수익 곡선도 빠르게 올라오고 있다. Anthropic 연환산 매출은 1년 반 새 수십 배(2025년 초 약 10억 달러에서 2026년 7월 말 650억 달러 이상)로 늘었고, OpenAI는 8월 약 400억 달러에서 9월 말 약 700억 달러에 근접했다는 보도가 나왔다(익명 소식통, 확인 필요). Microsoft AI는 3월 말 연환산 370억 달러(+123%)이고 이후 갱신값은 확인되지 않았다. 시점이 다른 값을 더하면 확인된 값 기준 약 1,420억 달러(650+400+370), OpenAI 9월 보도값 기준 약 1,720억 달러이고, 연간 투자 계획 7,200억~7,450억 달러의 약 5배와 약 4.2~4.3배다. 합산 대상이 겹치고(Microsoft AI에 OpenAI 소비분 포함) Anthropic은 총액·OpenAI는 순액으로 인식하므로 상한 참고값이다. 수익의 증가 속도가 투자의 증가 속도보다 빨라 두 곡선의 간격은 좁혀지기 시작했지만, 절대 규모는 아직 투자가 몇 배 크다.",
    check_flags=["합산한 값의 시점이 다름(Anthropic 7월 말, OpenAI 8월 또는 9월 말, Microsoft AI 3월 말) — 배수는 참고치", "OpenAI 약 700억은 익명 소식통 보도 — 확인 필요, 칩 문구 '투자 5배'는 확인된 값 기준으로 유지", "Microsoft AI 연환산에는 OpenAI 소비분이 겹칠 수 있고 AWS AI 사업 연환산 250억 이상은 합산에 없음", "일부는 순간 연환산, 일부는 연간 계획이라 성격이 다름"])
revise("I3-I-004", "단정반증", "'Anthropic이 매출에서도 OpenAI를 앞섰다'는 기준 없이 쓸 수 없다. 2026년 1분기 분기 매출은 OpenAI가 앞섰고, 연환산은 7~8월 Anthropic이 앞섰으나 9월 말 OpenAI 약 700억 보도(확인 필요)로 다시 가까워졌다. 인식 기준(총액·순액)도 다르다. Anthropic 흑자는 조정 기준·비감사다.",
    statement="모델 기업의 수익성은 갈렸다. Anthropic은 2분기 조정 영업이익 흑자를 냈다고 보도됐지만(회사 보고, 비감사, 이후 분기 적자 복귀 가능성 경고), OpenAI는 1분기 현금 소진 37억 달러 등 큰 손실이 이어지는 것으로 보도됐다. 매출 선두는 기준에 따라 다르다. 1분기 분기 매출은 OpenAI 약 57억 달러, Anthropic 약 47억~48억 달러로 OpenAI가 앞섰고, 연환산은 7~8월 Anthropic(650억 대 400억)이 앞섰지만 9월 말 OpenAI가 약 700억 달러에 근접했다는 보도가 있다(확인 필요). Anthropic은 총액, OpenAI는 순액으로 매출을 인식해 직접 비교할 수 없다.",
    check_flags=["Anthropic 1분기·2분기 매출은 출처마다 다름(47.3억 대 48억, 109억 전망 대 115억 보고)", "OpenAI 1분기 매출 57억은 The Information 인용(B) — 확인 필요", "Anthropic 흑자는 조정 기준·비감사"])
revise("I3-I-005", "단정반증", "'모델 가격은 세대마다 절반 가까이 내려간다'는 일반화는 공식 가격표로 확인되지 않는다. Opus 5.5는 Opus 5보다 20% 낮고 Opus 5는 Opus 4.8과 같은 가격이다. GPT-6 Sol 약 50%는 집계 사이트(C) 값이라 확인 필요이고, 신상위 등급은 더 비싸다. 방향('약화')은 근거가 충분히 확정되지 않아 유지한다.",
    statement="모델 가격이 세대마다 절반 가까이 내려간다고 일반화하기는 어렵다. 공식 가격표 기준 Claude Opus 5.5는 입력 $4·출력 $20로 Opus 5($5/$25)보다 20% 낮고, Opus 5는 Opus 4.8과 가격이 같다. GPT-6 Sol이 GPT-5.6 대비 약 50% 낮다는 값은 집계 사이트 기준이라 확인이 필요하고, 같은 달 신상위 등급 GPT-6 Astra는 입력 $10·출력 $50 수준(제공처별로 다름)이다. 가격 인하는 이용량 확대에는 도움이 되지만 모델 판매의 마진에는 압박이 되며, 그 폭은 모델·등급에 따라 갈린다.",
    check_flags=["OpenAI 쪽 가격은 집계 사이트(C) 기준 — OpenAI 가격표 미열람, 확인 필요", "방향 '약화'는 마진 압박 해석에 기댄 것 — 공식 가격표 기준으로는 '혼조'에 가까울 수 있음", "2026년 8~9월 가격 인상 사례(캐시 입력가·소개가격 종료)는 C등급 단일 출처라 본문에서 제외"])
revise("I3-I-006", "갱신", "Hugging Face는 인수 계약 체결 단계(종결은 2027년 상반기 예정)라 '인수했다'를 '인수하기로 했다'로 고쳤다.",
    statement="칩 회사가 고객에게 투자하고 생태계를 사들이는 흐름이 커지고 있다. NVIDIA는 OpenAI에 300억 달러를 넣었고 Hugging Face 인수 계약을 맺었다(종결 전). 공급자와 고객의 돈이 서로 얽혀, 수요의 독립성을 따져 봐야 하는 구조가 됐다.")
revise("I3-I-007", "갱신", "GPU 26만 장은 우선 공급 약속 단계이고 배분·일정이 미공개다. '수요자 쪽 기반을 마련했다'는 약속 단계임을 밝혀 쓴다.",
    statement="한국은 메모리 호황의 최대 수혜국이면서 NVIDIA의 GPU 26만 장 우선 공급 약속(배분·일정 미공개)으로 수요자 쪽 기반의 발판도 마련했다. 다만 이익은 메모리 공급에 몰려 있고, 국내 모델·서비스 매출은 아직 보이지 않는다.")

# --- 전망 ---
revise("I3-F-001", "전망 점검", "기준을 total revenue로 명시했다. 하단 1,058억 달러는 가이던스 1,080억 ±2% 계산과 맞고, 중국 데이터센터 컴퓨트 매출은 0으로 가정됐다. '8~10월'은 근사이며 실제는 FY27 3분기다.",
    method="NVIDIA FY27 3분기(2분기가 7월 26일 종료된 다음 분기) 실적 발표의 total revenue가 1,058억 달러(가이던스 1,080억 ±2%의 하단) 이상인지 확인",
    check_flags=["분기 종료일·발표일 미확인(10월 하순~11월 예정은 추정)"])
revise("I3-F-002", "판정 기준 보완", "비교 기준이 없었다. 회사별 정의 차이(Amazon 현금 PP&E 매입, Meta·Microsoft 금융리스 포함)와 Microsoft의 캘린더연도·회계연도, 리스 분류 변경(1,900억에서 1,750억) 처리, 2027 계획을 밝히지 않는 회사의 처리를 정했다(제안 기준).",
    method="Amazon·Microsoft·Alphabet·Meta 2026년 4분기 실적 발표에서 각 사가 공식 밝힌 2027년 연간 설비투자 계획의 합계를 같은 정의의 2026년 계획 합계와 비교. Microsoft는 2026 캘린더연도(약 1,750억 달러)와 FY27 회계연도를 구분하고 운용리스 전환 효과(약 150억 달러, 추정) 보정 여부를 병기. 2027년 계획을 밝히지 않은 회사가 있으면 조건 미충족으로 보아 판정 보류",
    check_flags=["Microsoft의 정의 변경이 적중 여부를 뒤집을 수 있음", "Microsoft·Google은 2027 증가를 이미 예고(콜 녹취·집계 B) — 적중 가능성이 높음"])
revise("I3-F-003", "판정 기준 보완", "'연환산 매출'의 인정 범위가 없었다. 회사 발표와 주요 언론 보도를 구분하고, 총액·순액 인식과 환산 방식을 병기하며, IPO 진행 중 공개 정의를 우선하도록 정했다(제안 기준).",
    method="Anthropic의 연환산 매출이 회사 발표 또는 주요 언론(Bloomberg·Reuters 등) 보도에서 1,000억 달러 이상으로 나오는지 확인. 총액 인식(클라우드 파트너 판매분 포함)임을 병기하고 순액 기준 값과 섞지 않으며, 월 매출×12인지 최근 4주 환산인지 보도가 밝힌 방식을 적는다. IPO 공시가 나오면 공시 정의를 우선",
    check_flags=["7월 말 650억·5월 말 470억이 최신 확인값, 투자자 기대 연말 1,000억~1,200억은 FT 재인용(B)", "IPO 일정(10월 중순 마케팅·11월 중간선거 전)은 변동 가능, 공개 S-1 제출 여부 미확인"])
revise("I3-F-004", "판정 기준 보완", "'손실'의 정의와 기준선이 없었다. 기준선 약 140억 달러는 출처가 불명확해(I3-M-005) 보도 기준으로 낮췄고, 비상장사라 연간 수치가 공개되지 않으면 판정 불가로 둔다(제안 기준).",
    statement="OpenAI의 2026년 실제 손실은 보도된 기준선(약 140억 달러)보다 클 것으로 보도될 것이다.",
    method="회사 발표 또는 주요 언론 보도에서 OpenAI 2026년 손실이 기준선(약 140억 달러, 보도 기준·원문 미확인)보다 큰지 확인. 현금 소진·순손실·조정 영업손실 중 보도가 쓴 정의를 병기하고 같은 정의로 비교될 때만 판정한다. 2027-03-31까지 연간 수치가 공개되지 않으면 '판정 불가'",
    check_flags=["기준선 140억 달러의 출처 불명확 — 확인 필요", "기한 2027-03-31이 비상장사 연간 수치 공개 시점으로 부적합할 수 있음"])
revise("I3-F-005", "전망 점검", "기준을 연결 영업이익(K-IFRS)으로 명시했다. 삼성전자 3분기 잠정 영업이익이 107.4조 원으로 2분기(89.5조)보다 약 20% 늘어 달성 가능성이 높아 보이나, 부문별 수치가 없어 메모리 단독 추세는 확정하지 못한다.",
    method="SK하이닉스 3분기 실적 공시의 연결 영업이익(K-IFRS)이 2분기 60조 5,426억 원 이상인지 확인",
    check_flags=["SK하이닉스 3분기 발표일 미확인(기한 10월 31일 이전 발표 여부 불명)", "삼성전자 3분기 증가분에는 DX 부문 변화가 섞여 있을 수 있음", "3분기 전망 약 78조 원은 컨센서스 출처 없는 보도라 보조 근거로만 사용"])
revise("I3-F-006", "판정 기준 보완", "시작 기준일이 없어 이미 일어난 사건(2026년 4월 OpenAI의 Stargate UK·Norway 보류 등)을 소급해 적중으로 처리할 위험이 있었다. 기준일을 2026-10-09로 두고 인정 범위를 정했다(제안 기준).",
    statement="2026년 10월 9일 이후 2027년 6월 말까지 빅테크나 OpenAI가 대형 AI 데이터센터 프로젝트의 취소나 연기를 공식 발표할 것이다.",
    method="2026-10-09 이후 각 사의 공식 발표·실적 발표만 인정(보도·분석 기사만 있으면 제외). Microsoft의 회계 처리(리스 분류) 변경은 취소로 보지 않음. 규모와 사유는 발표문에 적힌 대로 병기",
    check_flags=["2026년 4월 Stargate UK·Norway 보류는 기준일 이전이라 제외(공식성·사유 미확인)", "Oracle-OpenAI 텍사스 확장 취소 보도는 미열람"])
revise("I3-F-101", "판정 기준 보완", "낙관 판정(세 조건 중 둘 이상)이 기록 시점에 이미 변별력이 약하다. (2)는 Anthropic이 2분기 조정 영업이익 흑자를 이미 보고했고, (3)은 Microsoft·Google이 2027 증가를 예고했으며, (1)은 시점이 섞인 약 1,350억 달러다. 인정 기준을 고정했다(제안 기준).",
    method="세 가지 중 두 가지 이상 충족 시 적중: (1) 2026년 말 시점의 Anthropic+OpenAI 연환산 매출 합계 2,000억 달러 이상(같은 시점 값으로 합산, 총액·순액 인식 구분 병기. 2026-10-11 현재 확인 가능한 값은 약 1,350억 달러이며 7월 말 650억+9월 말 약 700억 보도의 시점 혼합·확인 필요) (2) 둘 중 하나의 GAAP 기준 연간 영업이익 흑자 공식 확인(조정 영업이익 흑자는 Anthropic이 2분기에 이미 보고해 인정하지 않음) (3) 빅테크 4사 2027년 설비투자 계획 합계가 같은 정의의 2026년 계획보다 큼(I3-F-002 기준)",
    basis=["I3-M-004", "I3-M-005", "I3-M-001", "I3-M-002", "I3-M-010"],
    check_flags=["합계 약 1,350억 달러는 Anthropic 총액·OpenAI 순액 혼합이고 OpenAI 700억은 Axios 단독 보도 — 확인 필요", "비관(I3-F-102)은 낙관 조건 하나 이하 충족일 때만 적중이라, 낙관이 거의 확정이면 판정이 사실상 불가", "이정표 2026-11 NVIDIA·SK하이닉스 실적은 I3-F-001·I3-F-005와 중복"])

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

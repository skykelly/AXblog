"""I1 R1 4유형 기록 생성 + 규칙 검증.
출력: i1/records.jsonl
"""
import json, sys
from pathlib import Path
from collections import Counter

R = "R1"
SRC = {
 "metr_wiki": {"url": "https://en.wikipedia.org/wiki/METR", "publisher": "Wikipedia (METR Time Horizon 1.1 결과 정리)", "date": "2026", "grade": "B"},
 "arc_opus5": {"url": "https://arcprize.org/results/anthropic-claude-opus-5", "publisher": "ARC Prize (검증 결과)", "date": "2026-07-24", "grade": "A"},
 "av_july": {"url": "https://www.analyticsvidhya.com/?p=256745", "publisher": "Analytics Vidhya (2026년 7월 모델 출시 일지)", "date": "2026-07", "grade": "B"},
 "af_sept": {"url": "https://af.net/realtime/september-2026-ai-releases-claude-opus-5-5-gpt-6-sol-and-more/", "publisher": "ThursdAI (2026년 9월 출시 정리)", "date": "2026-09-24", "grade": "B"},
 "iw_gemini4": {"url": "https://www.infoworld.com/article/4226642/google-plans-gemini-4-release-before-year-end-2.html", "publisher": "InfoWorld", "date": "2026-09-25", "grade": "B"},
 "anthropic_stmt": {"url": "https://www.anthropic.com/news/fable-mythos-access", "publisher": "Anthropic 공식 발표", "date": "2026-06-12", "grade": "A"},
 "openai_work": {"url": "https://openai.com/index/chatgpt-for-your-most-ambitious-work/", "publisher": "OpenAI 공식 발표", "date": "2026-07-09", "grade": "A"},
 "erdos": {"url": "https://letsdatascience.com/news/ai-advances-on-longstanding-erdos-problems-cd73fc86", "publisher": "Let's Data Science (OpenAI 발표 인용)", "date": "2026-08-03", "grade": "B"},
 "genie": {"url": "https://blog.google/innovation-and-ai/models-and-research/google-deepmind/project-genie/", "publisher": "Google 공식 블로그", "date": "2026-01-29", "grade": "A"},
 "micron_hbm4": {"url": "https://www.storagenewsletter.com/2026/03/17/nvidia-gtc-2026-micron-in-high-volume-production-of-hbm4-designed-for-nvidia-vera-rubin-pcie-gen6-ssd-and-socamm2/", "publisher": "StorageNewsletter (Micron 보도자료)", "date": "2026-03-17", "grade": "B"},
 "kr_dopamo": {"url": "https://www.smarttoday.co.kr/ko-kr/articles/110572", "publisher": "스마트투데이 (과기정통부 발표)", "date": "2026-08-18", "grade": "B"},
}
def src(*keys): return [dict(SRC[k], key=k) for k in keys]

base = dict(question="I1", question_version="v1.0", first_seen=R, last_seen=R, status="유효", replaces=None, check_flags=[])
records = []
def add(**kw):
    r = dict(base); r.update(kw); records.append(r)

# ---------- 지표 (M) ----------
add(id="I1-M-001", type="지표", indicator="I1-T1", importance=3, statement="METR 기준 AI가 50% 확률로 해내는 소프트웨어 작업 길이는 Claude Opus 4.6이 약 12시간(11시간 59분), 4월 Claude Mythos Preview는 최소 16시간으로 측정됐다. 16시간 이상은 현재 과제 세트로는 신뢰하기 어렵다.",
    value=16, unit="시간 이상(최고치)", as_of="2026-04", region="GLOBAL", definition="METR Time Horizon 1.1, 50% 성공 작업 길이", extra={"opus_4_6": "11h59m (2026-02)", "gpt_5_4_xhigh": "5h42m"},
    sources=src("metr_wiki"), verified=True, check_flags=["16시간 이상은 METR 스스로 하한값으로 표시"])
add(id="I1-M-002", type="지표", indicator="I1-T1", importance=2, statement="METR는 AI가 해내는 작업 길이가 2023년 이후 약 131일(4.3개월)마다 두 배로 늘었다고 추정했다. 2025년 3월 추정치(약 7개월)보다 빨라졌다.",
    value=130.8, unit="일(배가 기간)", as_of="2026-01", region="GLOBAL", definition="METR Time Horizon 1.1, 2023년 이후 배가 기간", prev_value=213, sources=src("metr_wiki"), verified=True)
add(id="I1-M-003", type="지표", indicator="I1-T2", importance=3, statement="처음 보는 상호작용 환경에서 규칙을 스스로 익혀야 하는 ARC-AGI-3의 최고 점수는 Claude Opus 5의 30.2%다(2026년 7월 기준).",
    value=30.2, unit="%", as_of="2026-07", region="GLOBAL", definition="ARC Prize 검증, ARC-AGI-3", sources=src("arc_opus5"), verified=True)
add(id="I1-M-004", type="지표", indicator="I1-T2", importance=2, statement="같은 모델이 ARC-AGI-2에서는 90.4%, ARC-AGI-1에서는 97.5%를 기록했다. 정형 추론 퍼즐은 사실상 포화됐다.",
    value=90.4, unit="%", as_of="2026-07", region="GLOBAL", definition="ARC Prize 검증, ARC-AGI-2 Semi-Private", sources=src("arc_opus5"), verified=True)
add(id="I1-M-005", type="지표", indicator="I1-T3", importance=2, statement="컴퓨터를 직접 조작하는 OSWorld-Verified에서 Gemini 3.6 Flash가 83.0%(이전 78.4%)를 기록했다고 Google이 밝혔다.",
    value=83.0, unit="%", as_of="2026-07", region="GLOBAL", definition="OSWorld-Verified, 기업 자체 발표", prev_value=78.4, sources=src("av_july"), verified=True, check_flags=["기업 자체 발표 수치"])
add(id="I1-M-006", type="지표", indicator="I1-T3", importance=2, statement="실무형 코딩 평가 SWE-Bench Pro에서 Claude Fable 5는 80%, GPT-5.6 Sol은 64.6%를 기록했다. 다른 코딩 지수에서는 GPT-5.6이 앞섰지만 METR가 벤치마크 과적합 가능성을 지적했다.",
    value=80, unit="%", as_of="2026-07", region="GLOBAL", definition="SWE-Bench Pro, 출시 일지 인용", sources=src("av_july"), verified=True, check_flags=["벤치마크 과적합 논란 — 단일 지표로 판정하지 않음"])
add(id="I1-M-007", type="지표", indicator="I1-T4", importance=2, statement="100만 토큰 입력은 프런티어 모델의 표준이 됐다. Claude Opus 5·Fable 5, GPT-5.6, Gemini 3.6 Flash, 오픈 웨이트 Kimi K3가 모두 100만 토큰 안팎을 지원한다.",
    value=1000000, unit="토큰", as_of="2026-07", region="GLOBAL", definition="주요 모델 최대 입력 길이", sources=src("av_july"), verified=True)
add(id="I1-M-008", type="지표", indicator="I1-T5", importance=3, statement="중국 Moonshot이 2.8조 파라미터(활성 1,040억), 100만 토큰 문맥의 Kimi K3를 오픈 웨이트로 공개했다. 프런트엔드 코딩 블라인드 평가에서 미국 선두 모델보다 높게 평가됐다는 보도가 나왔다.",
    value=2.8, unit="조 파라미터", as_of="2026-07", region="CN", definition="최대 오픈 웨이트 모델 규모", sources=src("av_july"), verified=True, check_flags=["블라인드 평가 순위는 보도 인용"])
add(id="I1-M-009", type="지표", indicator="I1-T7", importance=2, statement="Micron이 NVIDIA Vera Rubin용 HBM4(36GB 12단)를 대량 생산해 1분기부터 출하했다. 대역폭은 2.8TB/s 이상으로 HBM3E의 2.3배다.",
    value=2.8, unit="TB/s", as_of="2026-03", region="GLOBAL", definition="HBM4 스택당 대역폭, 기업 발표", sources=src("micron_hbm4"), verified=True)
add(id="I1-M-010", type="지표", indicator="I1-T8", importance=3, statement="정부 독자 AI 파운데이션 모델 2차 평가에서 4개 팀 모두 Artificial Analysis 지능 지수 31점 이상이었고, 40점 이상 최상위 구간에 미국·중국과 함께 한국 모델이 들어가 국가별 3위로 평가됐다. LG의 K-엑사원 2.0은 7,500억 파라미터다.",
    value=3, unit="위(국가별)", as_of="2026-08", region="KR", definition="과기정통부 발표, AAII 기준 국가별 순위", sources=src("kr_dopamo"), verified=True)

# ---------- 사건 (E) ----------
add(id="I1-E-001", type="사건", importance=2, statement="Google이 월드 모델 Genie 3 기반의 Project Genie를 미국 AI Ultra 구독자에게 열었다. 글이나 그림으로 세계를 만들고 실시간으로 돌아다닐 수 있지만, 한 번에 60초까지다.",
    date="2026-01-29", actor="Google DeepMind", sources=src("genie"), verified=True)
add(id="I1-E-002", type="사건", importance=2, statement="Micron이 GTC 2026에서 NVIDIA Vera Rubin용 HBM4 대량 생산을 발표했다.",
    date="2026-03-17", actor="Micron·NVIDIA", sources=src("micron_hbm4"), verified=True)
add(id="I1-E-003", type="사건", importance=3, statement="Anthropic이 Claude Fable 5를 출시했지만, 사흘 뒤 미국 정부의 수출 통제 지시로 Fable 5와 Mythos 5 접근을 전면 중단했다(7월 1일 복구).",
    date="2026-06-09", actor="Anthropic", sources=src("anthropic_stmt", "av_july"), verified=True)
add(id="I1-E-004", type="사건", importance=3, statement="OpenAI가 GPT-5.6과 함께 앱·파일을 넘나들며 몇 시간짜리 프로젝트를 끝까지 수행하는 ChatGPT Work를 출시했다.",
    date="2026-07-09", actor="OpenAI", sources=src("openai_work"), verified=True)
add(id="I1-E-005", type="사건", importance=2, statement="Moonshot이 Kimi K3를 API로 먼저 내놓고 열흘 뒤 가중치를 공개했다.",
    date="2026-07-16", actor="Moonshot", sources=src("av_july"), verified=True)
add(id="I1-E-006", type="사건", importance=3, statement="Anthropic이 Claude Opus 5를 출시했고, ARC Prize가 ARC-AGI-3 최고 기록(30.2%)으로 검증했다.",
    date="2026-07-24", actor="Anthropic", sources=src("arc_opus5", "av_july"), verified=True)
add(id="I1-E-007", type="사건", importance=3, statement="OpenAI가 미공개 내부 모델(Astra)로 에르되시 문제 3개에서 진전을 냈고 증명을 Lean으로 형식화했다고 발표했다. 독립 전문가 검증은 아직이다.",
    date="2026-08-01", actor="OpenAI", sources=src("erdos"), verified=True, check_flags=["독립 검증 전 — 성과로 확정하지 않음"])
add(id="I1-E-008", type="사건", importance=2, statement="과기정통부가 독자 AI 파운데이션 모델 2차 평가 결과 LG AI연구원·SK텔레콤·업스테이지를 3차로 올렸다. 최종 2개 팀은 내년 초에 정한다.",
    date="2026-08-18", actor="과학기술정보통신부", sources=src("kr_dopamo"), verified=True)
add(id="I1-E-009", type="사건", importance=3, statement="Anthropic이 Claude Opus 5.5를, OpenAI가 GPT-6 Sol·Luna를 9월에 내놓았다. Opus 5.5는 Fable급 성능을 Opus 5보다 40% 낮은 비용에, GPT-6 Sol은 GPT-5.6의 절반 가격에 제공한다는 설명이다.",
    date="2026-09", actor="Anthropic·OpenAI", sources=src("af_sept"), verified=True, check_flags=["정확한 출시일은 원문에 없음 — 월 단위 기록"])
add(id="I1-E-010", type="사건", importance=2, statement="Google DeepMind가 Gemini 4를 사후 학습 초기 단계에 두고 연내보다 훨씬 이른 출시를 예고했다. Gemini 3 Pro 이후 Pro급 신모델은 1년 가까이 나오지 않았다.",
    date="2026-09-25", actor="Google DeepMind", sources=src("iw_gemini4"), verified=True)

# ---------- 해석 (I) ----------
add(id="I1-I-001", type="해석", importance=3, target="Agent·장시간 작업", direction="강화",
    statement="AI에게 맡길 수 있는 일의 길이가 반나절을 넘어 하루에 다가섰고, 그 능력이 바로 시간 단위 업무 에이전트로 제품화됐다. 작업 길이는 4개월 남짓마다 두 배가 되고 있다.",
    basis=["I1-M-001", "I1-M-002", "I1-E-004"])
add(id="I1-I-002", type="해석", importance=3, target="Reasoning", direction="강화",
    statement="정형화된 추론 퍼즐은 포화됐고, 한계선은 '처음 보는 환경에서 스스로 규칙을 배우는 능력'으로 옮겨갔다. 이 축의 최고 점수는 아직 30%다.",
    basis=["I1-M-003", "I1-M-004", "I1-E-006"])
add(id="I1-I-003", type="해석", importance=2, target="측정의 신뢰성", direction="약화",
    statement="모델이 측정 도구보다 빨리 좋아지고 있다. METR는 16시간 이상을 신뢰하기 어렵다고 했고, 코딩 지수는 과적합 논란이 생겼다. 단일 벤치마크 순위로 기술 수준을 판정하기 어려워졌다.",
    basis=["I1-M-001", "I1-M-006"])
add(id="I1-I-004", type="해석", importance=3, target="오픈 웨이트 추격", direction="강화",
    statement="오픈 웨이트 모델이 조 단위 규모와 100만 토큰 문맥으로 프런티어에 바짝 붙었다. 성능 우위의 지속 기간이 짧아지고, 경쟁의 축이 가격과 배포 방식으로 옮겨가고 있다.",
    basis=["I1-M-008", "I1-E-005", "I1-M-007", "I1-E-009"])
add(id="I1-I-005", type="해석", importance=2, target="World Model·AI for Science", direction="중립",
    statement="월드 모델과 AI 과학 발견은 모두 시연 단계다. Genie는 1분짜리 체험으로 제한돼 있고, 에르되시 문제 결과는 독립 검증을 기다린다.",
    basis=["I1-E-001", "I1-E-007"])
add(id="I1-I-006", type="해석", importance=2, target="한국 모델", direction="중립",
    statement="한국은 국가별 3위권에 들었지만, 대표 모델들은 정부 프로젝트 평가 단계에 있고 글로벌 프런티어와의 격차는 남아 있다.",
    basis=["I1-M-010", "I1-E-008"])
add(id="I1-I-007", type="해석", importance=2, target="Compute", direction="강화",
    statement="차세대 가속기용 HBM4가 양산에 들어가 다음 세대 학습·추론 시스템의 공급이 시작됐다.",
    basis=["I1-M-009", "I1-E-002"])

# ---------- 세부 전망 (F) ----------
add(id="I1-F-001", type="전망", importance=3, status="유효", forecast_status="진행 중",
    statement="METR는 2027년 3월 말까지 50% 작업 길이 24시간 이상인 모델 측정 결과를 발표할 것이다.", due="2027-03-31", condition="METR가 새 과제 세트를 공개할 경우 그 기준으로 판정",
    method="METR time horizons 공식 결과 확인", basis=["I1-M-001", "I1-M-002"], result=None)
add(id="I1-F-002", type="전망", importance=3, status="유효", forecast_status="진행 중",
    statement="ARC-AGI-3 최고 점수는 2027년 6월 말까지 50%를 넘을 것이다.", due="2027-06-30", condition="없음",
    method="ARC Prize 검증 리더보드 확인", basis=["I1-M-003"], result=None)
add(id="I1-F-003", type="전망", importance=2, status="유효", forecast_status="진행 중",
    statement="Google은 2026년 안에 Gemini 4를 출시할 것이다.", due="2026-12-31", condition="없음",
    method="Google 공식 발표 확인", basis=["I1-E-010"], result=None)
add(id="I1-F-004", type="전망", importance=3, status="유효", forecast_status="진행 중",
    statement="OpenAI가 발표한 에르되시 문제 결과 가운데 1개 이상이 2027년 6월 말까지 독립 전문가 검증(학술지 게재 또는 수학자 공개 확인)을 받을 것이다.", due="2027-06-30", condition="없음",
    method="학술지 게재 또는 erdosproblems.com 등 공개 검증 기록 확인", basis=["I1-E-007"], result=None)
add(id="I1-F-005", type="전망", importance=2, status="유효", forecast_status="진행 중",
    statement="Google은 2027년 6월 말까지 Project Genie를 미국 밖으로 넓히거나 1회 생성 시간을 60초보다 늘릴 것이다.", due="2027-06-30", condition="없음",
    method="Google 공식 발표 확인", basis=["I1-E-001"], result=None)
add(id="I1-F-006", type="전망", importance=2, status="유효", forecast_status="진행 중",
    statement="과기정통부는 2027년 3월 말까지 독자 AI 파운데이션 모델 최종 2개 팀을 발표하고, LG AI연구원이 포함될 것이다.", due="2027-03-31", condition="없음",
    method="과기정통부 발표 확인", basis=["I1-E-008", "I1-M-010"], result=None)

# ---------- 메인 질문 시나리오 ----------
add(id="I1-F-101", type="전망", importance=3, status="유효", forecast_status="진행 중", scenario="낙관",
    statement="2027년 말까지 AI가 맡을 수 있는 일의 길이가 하루를 넘어 며칠 단위로 늘고, 처음 보는 환경에서의 추론이 절반을 넘는다. 월드 모델과 AI 과학 발견도 시연을 넘어 제품과 검증된 성과로 들어선다.",
    milestones=[
        {"by": "2026-12", "text": "Gemini 4 출시로 3사 모두 새 세대 모델 보유"},
        {"by": "2027-03", "text": "METR 50% 작업 길이 24시간 이상 측정"},
        {"by": "2027-06", "text": "ARC-AGI-3 50% 돌파, AI 수학 결과 독립 검증"}],
    due="2027-12-31", condition="수출 통제·안전 문제로 프런티어 모델 공개가 막히지 않을 경우",
    method="세 가지 중 두 가지 이상 충족 시 적중: (1) METR 50% 작업 길이 24시간 이상 공식 측정 (2) ARC-AGI-3 검증 점수 50% 이상 (3) AI 주도 수학·과학 결과의 독립 검증",
    basis=["I1-M-001", "I1-M-002", "I1-M-003", "I1-E-007"],
    signposts=[{"id": "I1-F-001", "on_hit": "낙관", "on_miss": "비관"}, {"id": "I1-F-002", "on_hit": "낙관", "on_miss": "비관"},
               {"id": "I1-F-003", "on_hit": "낙관"}, {"id": "I1-F-004", "on_hit": "낙관", "on_miss": "비관"}, {"id": "I1-F-005", "on_hit": "낙관"}], result=None)
add(id="I1-F-102", type="전망", importance=3, status="유효", forecast_status="진행 중", scenario="비관",
    statement="2027년 말까지 작업 길이 증가가 측정 한계와 신뢰성 문제에 막히고, 처음 보는 환경에서의 추론은 30%대에 머문다. 월드 모델과 AI 과학은 시연 단계에 남고, 경쟁은 성능보다 가격·속도 개선 중심으로 옮겨간다.",
    milestones=[
        {"by": "2027-03", "text": "24시간 이상 작업 길이 측정 없음"},
        {"by": "2027-06", "text": "ARC-AGI-3 최고 점수 50% 미만"},
        {"by": "2027-12", "text": "신모델 발표의 중심이 가격 인하와 속도"}],
    due="2027-12-31", condition="없음",
    method="낙관 시나리오의 판정 조건 세 가지 중 하나 이하만 충족 시 적중",
    basis=["I1-M-006", "I1-M-001", "I1-E-009", "I1-E-001"],
    signposts=[], result=None)

# ---------- 정정·추가 (2026-10-11 재조사 시험 1회, probe_20261011/diff_report.md) ----------
# 원본 기록은 ID를 유지한 채 고치고, 고치기 전 진술과 이유를 revisions에 남긴다. 새 기록은 added_on으로 구분한다.
CHG = "2026-10-11"
SRC.update({
 "arc_astra": {"url": "https://arcprize.org/blog/astra", "publisher": "ARC Prize (GPT-6 Astra 검증 결과)", "date": "2026-09-03", "grade": "A"},
 "benchlm": {"url": "https://benchlm.ai/benchmarks/arcagi3", "publisher": "BenchLM (ARC-AGI-3 순위)", "date": "2026-10-10", "grade": "B"},
 "fwm_astra": {"url": "https://fourweekmba.com/ai-gpt-6-astra-independent-benchmarks-flat-general-intelligence/", "publisher": "FourWeekMBA (GPT-6 Astra 독립 벤치마크 정리)", "date": "2026-09", "grade": "B"},
 "ld_argon": {"url": "https://letsdatascience.com/news/google-releases-gemini-4-argon-to-cyber-defenders-1093bb0b", "publisher": "Let's Data Science (Gemini 4 Argon)", "date": "2026-10-07", "grade": "B"},
 "localai_oct": {"url": "https://local-ai-zone.github.io/blog/October_2026_AI_Model_Updates.html", "publisher": "Local AI Zone (2026년 10월 모델 정리)", "date": "2026-10-07", "grade": "B"},
 "lwai346": {"url": "https://lastweekin.ai/p/last-week-in-ai-346-719-math-manuscripts", "publisher": "Last Week in AI #346", "date": "2026-10-09", "grade": "B"},
 "officechai": {"url": "https://officechai.com/ai/openai-has-also-included-proofs-for-23-erdos-problems-in-its-latest-math-proof-drop/", "publisher": "OfficeChai (에르되시 문제 23개)", "date": "2026-10-08", "grade": "B"},
 "aa_cmp": {"url": "https://artificialanalysis.ai/models/comparisons/glm-5-3-vs-kimi-k3", "publisher": "Artificial Analysis (GLM-5.3 vs Kimi K3)", "date": "2026-10", "grade": "A"},
 "kedhbm": {"url": "https://www.kedglobal.com/korean-chipmakers/newsView/ked202603080004", "publisher": "KED Global (Rubin HBM4 공급사)", "date": "2026-03-08", "grade": "B"},
 "llmstats": {"url": "https://llm-stats.com/ai-news", "publisher": "LLM Stats (AI 뉴스 모음)", "date": "2026-10-09", "grade": "B"},
})
def _get(i): return next(r for r in records if r["id"] == i)
def revise(i, kind, why, **ch):
    r = _get(i)
    r.setdefault("revisions", []).append({"on": CHG, "kind": kind, "before": r.get("statement") if "statement" in ch else None, "why": why})
    r.update(ch)

revise("I1-M-003", "누락정정", "R1 조사에서 9월 GPT-6 Astra의 검증 결과를 놓쳤다. 최고 기록은 30.2%가 아니라 62.7%였다.",
    statement="처음 보는 상호작용 환경에서 규칙을 스스로 익혀야 하는 ARC-AGI-3의 표준 조건 최고 점수는 OpenAI GPT-6 Astra의 62.7%다(ARC Prize 검증, 2026년 9월). 제공사 어댑터 조건에서는 99.9%였으나 조건이 달라 따로 본다. 이전 최고는 7월 Claude Opus 5의 30.2%였다.",
    value=62.7, as_of="2026-09", definition="ARC Prize 검증, ARC-AGI-3 표준 harness", prev_value=30.2,
    extra={"adapter_harness": "99.9% (Astra high)", "cost_usd": "표준 62.7% 약 26,100 · 어댑터 99.9% 약 18,800"},
    sources=src("arc_astra", "benchlm", "arc_opus5"), check_flags=["어댑터 조건 99.9%와 표준 조건 62.7%는 비교할 수 없음", "최고 기록 1건에 약 2.6만 달러"])
revise("I1-M-004", "갱신", "ARC-AGI-3 최고 기록 모델이 바뀌어 '같은 모델' 표현을 고쳤다.",
    statement="Claude Opus 5는 ARC-AGI-2에서 90.4%, ARC-AGI-1에서 97.5%를 기록했다(7월). 정형 추론 퍼즐은 사실상 포화됐다.")
revise("I1-E-006", "갱신", "당시 최고 기록이라는 점을 분명히 했다.",
    statement="Anthropic이 Claude Opus 5를 출시했고, ARC Prize가 당시 ARC-AGI-3 최고 기록(30.2%)으로 검증했다.")
revise("I1-E-009", "누락정정", "9월 말 신모델이 빠져 있었다.",
    statement=_get("I1-E-009")["statement"] + " 9월 말에는 Claude Sonnet 5.5(9/28)와 GPT-6.1 Sol(9/29)이 이어졌다.",
    sources=_get("I1-E-009")["sources"] + src("localai_oct"))
add(id="I1-E-011", type="사건", importance=3, added_on=CHG, statement="OpenAI가 GPT-6 Astra를 출시했다(입력 $10·출력 $50/백만 토큰). ARC Prize는 ARC-AGI-3 표준 조건 62.7%로 검증했고, 이는 당시 최고 기록이었다. Artificial Analysis 지능 지수는 약 61로 GPT-5.6 Sol과 같은 수준이다.",
    date="2026-09-02", actor="OpenAI", sources=src("arc_astra", "fwm_astra"), verified=True, check_flags=["OpenAI 자체 발표 98.6%는 어댑터 조건이라 표준 점수와 다름"])
add(id="I1-E-012", type="사건", importance=3, added_on=CHG, statement="Google이 Gemini 4 Argon을 발표했지만 Fairwind Program(사이버 방어 신뢰 파트너)에만 제한 공개했고 일반 공개 날짜는 밝히지 않았다. 컨텍스트는 100만 토큰, 가격은 도입기 $2/$10, 이후 $4/$20(백만 토큰)이다.",
    date="2026-09-30", actor="Google", sources=src("ld_argon"), verified=True, check_flags=["벤치마크는 Google 자체 발표"])
add(id="I1-E-013", type="사건", importance=3, added_on=CHG, statement="OpenAI가 내부 모델이 쓴 수학 원고 719편(372개 주제군)을 GitHub에 공개했다. 에르되시 문제 결과는 23개이고 19개에 Lean 형식화가 있다. 문제 사이트 운영자 Thomas Bloom은 증명을 면밀히 검토하지 않았고 어느 문제도 해결된 것으로 보면 안 된다고 밝혔다. Terence Tao는 한꺼번에 공개한 방식을 비판했다.",
    date="2026-10-06", actor="OpenAI", sources=src("lwai346", "officechai"), verified=True, check_flags=["일부 원고 철회·정정은 블로그(C급) 보도뿐이라 원문 확인 전까지 반영하지 않음", "독립 검증 전 — 성과로 확정하지 않음"])
add(id="I1-E-014", type="사건", importance=2, added_on=CHG, statement="Anthropic이 Claude Haiku 5.5를 내놓았다. 100만 토큰 컨텍스트와 노력 수준 조절을 지원하는 첫 Haiku이고, 10만 토큰 이하 입력은 백만 토큰당 $0.10(출력 $0.50)으로 이전 세대보다 90% 낮다.",
    date="2026-10-07", actor="Anthropic", sources=src("lwai346", "llmstats"), verified=True, check_flags=["벤치마크는 자체 발표"])
revise("I1-I-002", "누락정정", "ARC-AGI-3 최고 점수 정정(M-003)에 따라 '아직 30%'라는 결론을 고쳤다.",
    statement="정형화된 추론 퍼즐은 포화됐고, 한계선은 ‘처음 보는 환경에서 스스로 규칙을 배우는 능력’이다. 이 축의 표준 조건 최고 점수는 7월 30%에서 9월 62.7%로 한 세대 만에 두 배가 됐다. 다만 최고 기록 한 건에 약 2.6만 달러가 들었고 조건에 따라 점수가 크게 갈려, 한계선은 점수에서 비용과 조건으로 옮겨가고 있다.",
    basis=["I1-M-003", "I1-M-004", "I1-E-006", "I1-E-011"])
revise("I1-M-008", "갱신", "성능 지수 기준 선두를 추가했다.",
    statement="중국 Moonshot이 2.8조 파라미터(활성 1,040억), 100만 토큰 문맥의 Kimi K3를 오픈 웨이트로 공개했다. Artificial Analysis 지능 지수는 Kimi K3가 44, Z.ai의 GLM-5.3(7,530억·활성 400억, 8월 공개)이 45로 성능 선두는 GLM-5.3이고 규모는 Kimi K3가 가장 크다. 프런트엔드 코딩 블라인드 평가에서 미국 선두 모델보다 높게 평가됐다는 보도가 나왔다.",
    sources=_get("I1-M-008")["sources"] + src("aa_cmp"), check_flags=_get("I1-M-008")["check_flags"] + ["두 모델의 1점 차이는 오차 범위일 수 있음"])
revise("I1-I-004", "갱신", "성능 선두와 서방 오픈 웨이트 소식을 반영했다.",
    statement="오픈 웨이트 모델이 조 단위 규모와 100만 토큰 문맥으로 프런티어에 바짝 붙었다. 성능 지수는 GLM-5.3(45)과 Kimi K3(44)가 앞서고, 서방에서도 Mistral Large 4와 Reflection AI의 Beam이 가중치 공개를 예고했다. 성능 우위의 지속 기간이 짧아지고, 경쟁의 축이 가격과 배포 방식으로 옮겨가고 있다.")
revise("I1-M-007", "갱신", "10월 출시 모델을 추가했다.",
    statement=_get("I1-M-007")["statement"] + " 10월에는 Claude Haiku 5.5와 Gemini 4 Argon도 100만 토큰을 지원한다.",
    sources=_get("I1-M-007")["sources"] + src("llmstats", "ld_argon"))
revise("I1-M-009", "상충", "Rubin용 HBM4 공급사 구성에 대한 보도가 엇갈려, 마이크론 발표 표현을 낮추고 상충을 표시했다.",
    statement="Micron이 NVIDIA Vera Rubin용 HBM4(36GB 12단)를 GTC에서 대량 생산 중이라고 발표했고 1분기부터 출하한다고 밝혔다. 대역폭은 2.8TB/s 이상으로 HBM3E의 2.3배다. Rubin 공급사 구성은 보도가 엇갈려, 3월 KED는 삼성전자·SK하이닉스만 공급한다고 전했다.",
    sources=_get("I1-M-009")["sources"] + src("kedhbm"), check_flags=["Rubin용 HBM4 공급사 구성이 보도마다 다름(마이크론 제외 vs 3사 모두 양산)"])
revise("I1-I-007", "갱신", "공급사 구성은 확인이 필요하다는 점을 덧붙였다.",
    statement="차세대 가속기용 HBM4가 양산 단계에 들어가 다음 세대 학습·추론 시스템의 공급이 시작됐다. 다만 공급사 구성은 확인이 필요하다.")
revise("I1-I-005", "갱신", "10월 수학 원고 공개와 검증 상태를 반영했다.",
    statement="월드 모델과 AI 과학 발견은 모두 시연 단계다. Genie는 1분짜리 체험으로 제한돼 있고, OpenAI가 10월에 공개한 수학 원고 719편(에르되시 문제 23개 포함)은 아직 독립 검증을 받지 못했다. 문제 사이트 운영자도 증명을 면밀히 검토하지 않았다고 밝혔다.",
    basis=["I1-E-001", "I1-E-007", "I1-E-013"])
revise("I1-F-002", "전망 교체", "기존 기준(50% 초과)은 기록 시점에 이미 62.7%로 충족돼 있었다. 이미 달성된 전망은 둘 수 없어 표준 조건 80%로 교체했다.",
    statement="ARC-AGI-3 표준 조건 최고 점수는 2027년 6월 말까지 80%를 넘을 것이다.",
    method="ARC Prize 검증 리더보드의 표준 harness 점수 확인", basis=["I1-M-003", "I1-E-011"])
revise("I1-F-003", "판정 기준 보완", "9/30 Argon이 제한 공개로 발표돼, 출시의 기준이 필요해졌다.",
    statement="Google은 2026년 안에 Gemini 4를 일반 공개로 출시할 것이다.",
    method="Google 공식 발표 확인. 일반 개발자 API 또는 일반 앱 이용이 가능해야 출시로 보고, 제한 공개(예: Fairwind Program)는 제외", basis=["I1-E-010", "I1-E-012"])
revise("I1-F-004", "전망 점검", "원고 공개 규모는 커졌지만 학술지 게재나 수학자의 공개 확인은 아직 없다. 달성 가능성 판단 근거에 10월 공개 사건을 추가했다.",
    basis=["I1-E-007", "I1-E-013"])
_s = _get("I1-F-101")
revise("I1-F-101", "전망 교체", "ARC-AGI-3 기준을 표준 조건 80%로 바꾼 것(F-002)에 맞췄다.",
    statement="2027년 말까지 AI가 맡을 수 있는 일의 길이가 하루를 넘어 며칠 단위로 늘고, 처음 보는 환경에서의 추론이 표준 조건 80%를 넘는다. 월드 모델과 AI 과학 발견도 시연을 넘어 제품과 검증된 성과로 들어선다.",
    milestones=[{"by": "2026-12", "text": "Gemini 4 일반 공개로 3사 모두 새 세대 모델 보유"}, {"by": "2027-03", "text": "METR 50% 작업 길이 24시간 이상 측정"}, {"by": "2027-06", "text": "ARC-AGI-3 표준 조건 80% 돌파, AI 수학 결과 독립 검증"}],
    method="세 가지 중 두 가지 이상 충족 시 적중: (1) METR 50% 작업 길이 24시간 이상 공식 측정 (2) ARC-AGI-3 표준 조건 검증 점수 80% 이상 (3) AI 주도 수학·과학 결과의 독립 검증",
    basis=["I1-M-001", "I1-M-002", "I1-M-003", "I1-E-007"])
revise("I1-F-102", "전망 교체", "표준 조건 점수가 이미 62.7%라 '30%대에 머문다'는 시나리오를 고쳤다.",
    statement="2027년 말까지 작업 길이 증가가 측정 한계와 신뢰성 문제에 막히고, 처음 보는 환경에서의 추론은 표준 조건 80%를 넘지 못한다. 월드 모델과 AI 과학은 시연 단계에 남고, 경쟁은 성능보다 가격·속도 개선 중심으로 옮겨간다.",
    milestones=[{"by": "2027-03", "text": "24시간 이상 작업 길이 측정 없음"}, {"by": "2027-06", "text": "ARC-AGI-3 표준 조건 최고 점수 80% 미만"}, {"by": "2027-12", "text": "신모델 발표의 중심이 가격 인하와 속도"}])

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

"""I5 R1 4유형 기록 생성 + 규칙 검증.
출력: i5/records.jsonl
"""
import json, sys
from pathlib import Path
from collections import Counter

R = "R1"
SRC = {
 "canaries26": {"url": "https://digitaleconomy.stanford.edu/news/canariesaug26/", "publisher": "Stanford Digital Economy Lab (Brynjolfsson·Chandar·Chen)", "date": "2026-08-12", "grade": "A"},
 "canaries25": {"url": "https://www.theregister.com/2025/08/26/ai_hurts_recent_college_grads_jobs/", "publisher": "The Register (Stanford 논문 요약)", "date": "2025-08-26", "grade": "B"},
 "chall_jul": {"url": "https://www.challengergray.com/wp-content/uploads/2026/08/Challenger-Report-July-2026.pdf", "publisher": "Challenger, Gray & Christmas 감원 보고서 (7월)", "date": "2026-08-06", "grade": "A"},
 "chall_aug": {"url": "https://www.challengergray.com/wp-content/uploads/2026/09/Challenger-Report-August-2026.pdf", "publisher": "Challenger, Gray & Christmas 감원 보고서 (8월)", "date": "2026-09-03", "grade": "A"},
 "chall_sep": {"url": "https://pro.thestreet.com/market-commentary/job-cuts-hit-4-year-low-while-full-year-hiring-plummets", "publisher": "TheStreet Pro (Challenger 9월 보고서 인용)", "date": "2026-10-01", "grade": "B"},
 "bok25": {"url": "https://www.heraldk.com/article/2025102921152134344", "publisher": "헤럴드경제 (한국은행 'AI 확산과 청년고용 위축' 인용)", "date": "2025-10-29", "grade": "B"},
 "bok26": {"url": "https://www.inews24.com/view/1995762", "publisher": "아이뉴스24 (한국은행 BOK 이슈노트 인용)", "date": "2026-08-18", "grade": "B"},
 "kostat_sep": {"url": "https://www.inews24.com/view/2015634", "publisher": "아이뉴스24 (국가데이터처 9월 고용동향 인용)", "date": "2026-10-16", "grade": "B"},
 "nyfed": {"url": "https://libertystreeteconomics.newyorkfed.org/2025/09/are-businesses-scaling-back-hiring-due-to-ai/", "publisher": "뉴욕 연방준비은행 Liberty Street Economics", "date": "2025-09-04", "grade": "A"},
 "chifed": {"url": "https://ohiocpa.com/get-involved/news/2026/07/24/report--jobs-in-occupations-most-exposed-to-ai-increased-by-4", "publisher": "Ohio Society of CPAs (시카고 연준 연구 인용)", "date": "2026-07-24", "grade": "B"},
 "yale": {"url": "https://fortune.com/2026/02/02/ai-labor-market-yale-budget-lab-ai-washing/", "publisher": "Fortune (Yale Budget Lab·Oxford Economics 인용)", "date": "2026-02-02", "grade": "B"},
 "indeed": {"url": "https://officechai.com/ai/us-software-job-postings-are-up-15-since-launch-of-claude-code-while-overall-job-postings-are-down-7-indeed-data/", "publisher": "OfficeChai (Indeed Hiring Lab 인용)", "date": "2026-07-11", "grade": "B"},
 "anth": {"url": "https://builtin.com/articles/anthropic-economic-index-2026-ai-jobs-report", "publisher": "Built In (Anthropic Economic Index 2026년 3월 보고서 인용)", "date": "2026-04-22", "grade": "B"},
 "linkedin": {"url": "https://www.socialmediatoday.com/news/linkedin-shares-data-on-rising-job-roles/809069/", "publisher": "Social Media Today (LinkedIn Jobs on the Rise 2026 인용)", "date": "2026-01-07", "grade": "B"},
 "jobkorea": {"url": "https://news.bizwatch.co.kr/special/2026/view/202609160006", "publisher": "비즈워치 (잡코리아 상반기 AI 직무 공고 분석 인용)", "date": "2026-09-16", "grade": "B"},
 "keis": {"url": "https://newsseoul.co.kr/news/view/1065584418676511", "publisher": "뉴스서울 (고용노동부·한국고용정보원 직업사전 발표 인용)", "date": "2025-07-30", "grade": "B"},
 "soc": {"url": "https://www.bls.gov/soc/2028/2028_soc_revision.htm", "publisher": "미국 노동통계국 (2028 SOC 개정)", "date": "2026-09-30", "grade": "A"},
 "wef": {"url": "https://www.weforum.org/press/2025/01/future-of-jobs-report-2025-78-million-new-job-opportunities-by-2030-but-urgent-upskilling-needed-to-prepare-workforces/?width=350", "publisher": "세계경제포럼 Future of Jobs Report 2025", "date": "2025-01-08", "grade": "A"},
 "salesforce": {"url": "https://www.itpro.com/technology/artificial-intelligence/marc-benioff-says-salesforce-has-already-cut-4-000-customer-support-staff-for-ai-agents-and-workforce-productivity-hasnt-dipped", "publisher": "ITPro", "date": "2025-09-01", "grade": "B"},
 "klarna": {"url": "https://tech.co/news/klarna-reverses-ai-overhaul", "publisher": "Tech.co", "date": "2025-05-20", "grade": "B"},
 "amazon25": {"url": "https://abc7news.com/post/amazon-layoffs-company-could-cut-many-30000-corporate-jobs-reports-say/18078414/", "publisher": "ABC7 (AP)", "date": "2025-10-28", "grade": "B"},
 "amazon26": {"url": "https://www.aljazeera.com/economy/2026/1/28/amazon-cuts-thousands-of-jobs-amid-ai-push", "publisher": "Al Jazeera", "date": "2026-01-28", "grade": "B"},
 "accenture": {"url": "https://www.irishtimes.com/business/2025/09/26/accenture-to-exit-staff-who-cannot-be-retrained-for-age-of-ai", "publisher": "The Irish Times", "date": "2025-09-26", "grade": "B"},
 "kbcall": {"url": "https://www.khan.co.kr/article/202604150600111", "publisher": "경향신문", "date": "2026-04-15", "grade": "B"},
 "moel_plan": {"url": "https://www.newsis.com/view/NISX20260709_0003701773", "publisher": "뉴시스 (산업전환 고용안정 기본계획)", "date": "2026-07-09", "grade": "B"},
 "moel_ai": {"url": "https://www.newsis.com/view/NISX20251217_0003445138", "publisher": "뉴시스 (노동시장 AI 인재양성 추진방안)", "date": "2025-12-18", "grade": "B"},
}
def src(*keys): return [dict(SRC[k], key=k) for k in keys]

base = dict(question="I5", question_version="v1.0", first_seen=R, last_seen=R, status="유효", replaces=None, check_flags=[])
records = []
def add(**kw):
    r = dict(base); r.update(kw); records.append(r)

# ---------- 지표 (M) ----------
add(id="I5-M-001", type="지표", indicator="I5-T1", importance=3,
    statement="미국에서 AI 노출이 큰 직무의 22~25세 고용은 노출이 작은 직무와 같은 속도로 움직였을 경우보다 약 19% 낮다(2026년 6월). 2025년 7월 자료 기준으로는 15%였다. 노출 상위 두 분위의 22~25세 고용은 2022년 11월부터 2026년 6월까지 약 11% 줄었고, 노출 하위 세 분위는 약 10% 늘었다. 경력자에서는 같은 격차가 보이지 않는다.",
    value=19, unit="% (기대 대비 부족)", as_of="2026-06", region="US", definition="ADP 급여 자료, AI 노출 상위 직무의 22~25세 고용과 노출 하위 직무 추세의 차이",
    extra={"prev_vintage": "15% (2025-07 자료)", "level_change_exposed": "약 -11% (2022-11→2026-06)", "level_change_low": "약 +10%"},
    sources=src("canaries26"), verified=True, check_flags=["저자 스스로 인과 추정이 아닌 기술 통계라고 밝힘"])
add(id="I5-M-002", type="지표", indicator="I5-T1", importance=3,
    statement="한국은행은 2022~2026년 청년 일자리 감소의 약 94%(26만 8천 개)가 AI 노출이 큰 업종에서 나왔다고 분석했다. 같은 기간 50대 일자리는 약 23만 개 늘었고 그중 약 17만 3천 개가 AI 노출 업종이었다. 업종별 청년 고용은 정보서비스 -31.4%, 출판 -27.4%, 컴퓨터 프로그래밍·시스템 통합 -16.6%다. 한국은행은 AI가 주원인일 가능성은 낮고 기존 변화를 키우는 요인이라고 봤다.",
    value=94, unit="% (AI 고노출 업종 비중)", as_of="2026-06", region="KR", definition="한국은행 BOK 이슈노트, 국민연금 가입자 기준 청년 일자리 증감의 업종 분해",
    extra={"youth_loss_total": "약 28만 5천 개(본문) / 제목 26만 개", "youth_loss_exposed": "26만 8천 개", "age50_gain": "약 23만 개"},
    sources=src("bok26"), verified=True, check_flags=["기사 제목(26만)과 본문(28만 5천) 수치가 다름 — 한국은행 원문 확인 필요", "비교 기간의 정확한 시작·끝 월은 원문 확인 필요"])
add(id="I5-M-003", type="지표", indicator="I5-T1", importance=2,
    statement="한국은행의 첫 분석(2025년 10월)에서는 2022년 7월부터 2025년 7월까지 청년(15~29세) 일자리 21만 1천 개가 줄었고, 그중 98.6%(20만 8천 개)가 AI 노출 상위 업종에서 나왔다. 같은 기간 50대 일자리는 20만 9천 개 늘었다.",
    value=98.6, unit="% (AI 노출 상위 업종 비중)", as_of="2025-07", region="KR", definition="국민연금 가입자 기준 15~29세 일자리 증감, AI 노출 3·4분위 업종",
    extra={"youth_loss": "21만 1천 개", "age50_gain": "20만 9천 개"}, sources=src("bok25"), verified=True)
add(id="I5-M-004", type="지표", indicator="I5-T2", importance=3,
    statement="2026년 1~9월 미국 기업이 감원 사유로 AI를 든 인원은 12만 136명으로 전체 발표 감원 57만 3,195명의 약 21%다. 누적 기준으로는 AI가 감원 사유 1위다.",
    value=120136, unit="명 (2026년 1~9월)", as_of="2026-09", region="US", definition="Challenger 집계, 기업이 감원 발표에서 AI를 사유로 든 인원",
    extra={"share": "약 21%", "total_cuts": "573,195명"}, sources=src("chall_sep", "chall_aug"), verified=True,
    check_flags=["기업이 밝힌 사유를 집계한 값이라 실제로 AI 때문인지는 검증되지 않음", "9월 값은 TheStreet 인용(B), 8월까지는 보고서 원문(A)으로 확인"])
add(id="I5-M-005", type="지표", indicator="I5-T2", importance=2,
    statement="AI 사유 감원은 2026년 3월부터 7월까지 다섯 달 연속 감원 사유 1위였다. 7월에는 1만 970명(그달 감원의 33%)이었으나 8월 3,462명, 9월 3,961명(9%, 5위)으로 줄었다.",
    value=3961, unit="명 (2026년 9월)", as_of="2026-09", region="US", definition="Challenger 월간 집계의 AI 사유 감원",
    extra={"jul": "10,970명 (33%)", "aug": "3,462명", "sep": "3,961명 (9%)"}, sources=src("chall_jul", "chall_aug", "chall_sep"), verified=True)
add(id="I5-M-006", type="지표", indicator="I5-T2", importance=2,
    statement="2025년 1~11월 AI를 사유로 든 미국 감원은 약 5만 5천 명으로 전체의 4.5%였다. 같은 기간 '시장·경제 상황' 사유는 24만 5천 명이었다. Oxford Economics는 일부 기업이 감원을 좋은 소식처럼 포장하려고 AI를 사유로 든다고 의심했다.",
    value=55000, unit="명 (2025년 1~11월)", as_of="2025-11", region="US", definition="Challenger 집계를 인용한 Oxford Economics 분석",
    extra={"share": "4.5%"}, sources=src("yale"), verified=True, check_flags=["Challenger 원문이 아닌 Fortune의 Oxford Economics 인용 — 원 보고서 확인 필요"])
add(id="I5-M-007", type="지표", indicator="I5-T3", importance=3,
    statement="미국 소프트웨어 개발 채용공고는 2025년 2월 말 이후 약 15% 늘었지만 여전히 2020년 2월보다 약 27.5% 적다. 같은 기간 전체 채용공고는 7% 줄었다. 2025년 5월~2026년 5월 소프트웨어 공고 순증가의 71%는 시니어 직무였고, 37%는 직무명에 AI가 들어간 공고였다.",
    value=-27.5, unit="% (2020년 2월 대비)", as_of="2026-07", region="US", definition="Indeed 소프트웨어 개발 채용공고 지수(2020-02 = 100)",
    extra={"since_2025_02": "약 +15%", "overall": "-7%", "senior_share_of_increase": "71%", "ai_title_share": "37%"},
    sources=src("indeed"), verified=True, check_flags=["Indeed Hiring Lab 원문은 열지 못하고 OfficeChai 인용(B)으로 확인 — 원문 확인 필요"])
add(id="I5-M-008", type="지표", indicator="I5-T3", importance=3,
    statement="뉴욕 연준 조사(2025년 8월)에서 AI를 쓰는 서비스 기업은 40%(1년 전 25%)였다. 최근 6개월 AI 때문에 해고했다는 서비스 기업은 1%였지만, 채용을 줄였다는 곳은 약 12%였다. 앞으로 6개월 안에 AI 때문에 채용을 줄이겠다는 곳은 약 4분의 1이었고, 줄어든 채용은 대졸 직무에 몰렸다.",
    value=12, unit="% (AI로 채용 축소, 서비스 기업)", as_of="2025-08", region="US", definition="뉴욕 연준 관할 서비스·제조 기업 설문",
    extra={"ai_use_service": "40%", "layoff_due_ai": "1%", "expect_hire_fewer": "약 25%", "manufacturing_layoff": "0%"},
    sources=src("nyfed"), verified=True, check_flags=["뉴욕 연준 관할 지역 기업 설문 — 미국 전체 대표성은 제한"])
add(id="I5-M-009", type="지표", indicator="I5-T3", importance=2,
    statement="시카고 연준 연구에서 AI 노출이 가장 큰 직무의 고용은 2019~2024년 4.05% 늘었고, 노출이 작은 직무는 고용을 줄였다. 임금은 노출 정도와 관계없이 올랐다.",
    value=4.05, unit="% (2019→2024)", as_of="2024", region="US", definition="AI 노출 상위 직무의 고용 증감",
    sources=src("chifed"), verified=True, check_flags=["시카고 연준 원문이 아닌 회계사협회 뉴스 인용 — 원문 확인 필요", "연령 구분이 없는 전체 고용 기준이라 I5-M-001(22~25세)과 대상이 다름"])
add(id="I5-M-010", type="지표", indicator="I5-T4", importance=2,
    statement="Anthropic Economic Index(2026년 3월)에서 Claude에 일을 통째로 맡기는 지시형 대화는 오래 쓴 사용자 29.4%, 새 사용자 38.1%였다. 업무 목적 사용은 각각 약 49%, 42%였다. 2025년 11월~2026년 2월 API에서는 영업 아웃리치 자동화와 자동 매매 업무가 각각 약 두 배로 늘었다.",
    value=38.1, unit="% (지시형, 새 사용자)", as_of="2026-02", region="GLOBAL", definition="Claude 대화 약 100만 건의 업무 분류, 지시형 = 자동화에 가까운 사용",
    extra={"directive_high_tenure": "29.4%", "work_use": "49% / 42%"}, sources=src("anth"), verified=True,
    check_flags=["Anthropic 원문은 열지 못하고 Built In 인용(B)으로 확인 — 전체 자동화 비율은 원문 확인 필요", "한 회사 서비스의 사용 자료라 경제 전체를 대표하지 않음"])
add(id="I5-M-011", type="지표", indicator="I5-T5", importance=3,
    statement="LinkedIn의 2026년 미국 '떠오르는 직업' 1위는 AI 엔지니어, 2위는 AI 컨설턴트·전략가다. 4위 데이터 라벨러, 5위 AI·ML 연구원까지 상위 5개 중 4개가 AI 직무다.",
    value=4, unit="개 (상위 5개 중 AI 직무)", as_of="2026-01", region="US", definition="LinkedIn Jobs on the Rise, 최근 3년 채용 증가율 순위",
    extra={"rank1": "AI 엔지니어", "rank2": "AI 컨설턴트·전략가", "rank4": "데이터 라벨러", "rank5": "AI·ML 연구원"}, sources=src("linkedin"), verified=True)
add(id="I5-M-012", type="지표", indicator="I5-T5", importance=3,
    statement="잡코리아에 2026년 상반기 올라온 AI 키워드 공고는 약 1만 8천 건이다. 기업이 AI 전문 직무로 지정한 공고는 1년 전보다 128% 늘었고(경력 +140%, 신입 +55%), 비개발 AI 직무는 325% 늘어 AI 공고 중 비중이 11.6%에서 21.6%로 커졌다. AI가 아닌 개발 공고는 6.6% 줄었고 웹 퍼블리셔 -40.1%, 앱 개발 -32.2%였다.",
    value=128, unit="% (AI 전문 직무 공고 증가)", as_of="2026-06", region="KR", definition="잡코리아 공고 중 AI 전문 직무로 지정된 공고의 전년 동기 대비 증가율",
    extra={"ai_keyword_postings": "약 18,000건", "non_dev_ai": "+325%", "non_ai_dev": "-6.6%", "web_publisher": "-40.1%", "app_dev": "-32.2%"},
    sources=src("jobkorea"), verified=True, check_flags=["한 채용 플랫폼 자료 — 국내 전체 채용시장 대표성은 제한"])
add(id="I5-M-013", type="지표", indicator="I5-T6", importance=2,
    statement="2025년 한국직업사전 발표에서 AI 관련 신규 직업으로는 '인공지능서비스운영관리자'가 이름을 올렸다. 생성형 AI 콘텐츠 개발·품질관리 직업은 아직 등재되지 않았다.",
    value=1, unit="개 (기사에 확인된 AI 신규 직업)", as_of="2025-07", region="KR", definition="한국직업사전 신규 등재 직업 중 AI 관련",
    sources=src("keis"), verified=True, check_flags=["전체 신규 등재 수와 AI 관련 직업의 전체 목록은 기사에 없음 — 한국고용정보원 원문 확인 필요"])
add(id="I5-M-014", type="지표", indicator="I5-T6", importance=2,
    statement="미국 표준직업분류(SOC) 2028 개정은 아직 1차 의견 검토 단계다. 2차 고시 일정은 미정이고 최종안은 2027년, 통계 적용은 2028년부터다. 개정 안내에는 AI 관련 직업이 따로 언급되지 않는다.",
    value=0, unit="개 (공식 분류에 신설된 AI 직업)", as_of="2026-09", region="US", definition="미국 SOC 개정 현황",
    sources=src("soc"), verified=True)
add(id="I5-M-015", type="지표", indicator="I5-T7", importance=3,
    statement="2026년 9월 한국 청년(15~29세) 고용률은 44.0%로 1년 전보다 1.1%p 낮다. 청년 취업자는 14만 7천 명 줄어 47개월 연속 감소했고 청년 실업률은 5.4%다. 같은 달 사무종사자는 24만 7천 명, 전문가·관련 종사자는 9만 1천 명 늘었다.",
    value=44.0, unit="% (청년 고용률)", as_of="2026-09", region="KR", definition="국가데이터처 경제활동인구조사, 15~29세",
    extra={"youth_employed_change": "-14만 7천 명", "streak": "47개월", "office_workers": "+24만 7천 명", "professionals": "+9만 1천 명", "age15_34_rate": "56.1%"},
    sources=src("kostat_sep"), verified=True, check_flags=["이번 발표부터 청년 기준을 15~34세로도 냄 — 시계열 비교 때 기준 확인"])
add(id="I5-M-016", type="지표", indicator="I5-T7", importance=2,
    statement="KB국민은행 콜센터 상담사는 1,133명에서 2025년 869명으로 264명 줄었고, AI 처리율은 41.3%다. 상담사 1인당 하루 상담은 약 70건에서 100~120건으로 늘었다. 반면 신한은행 상담 인력은 AICC 도입 뒤에도 693명(2024)에서 697명(2025)으로 늘었다.",
    value=869, unit="명 (KB국민은행 상담사, 2025)", as_of="2025", region="KR", definition="은행 콜센터 상담 인력",
    extra={"kb_prev": "1,133명", "kb_ai_rate": "41.3%", "shinhan": "693→697명", "nh_ai_rate": "21.7%"},
    sources=src("kbcall"), verified=True, check_flags=["KB 감소 전 시점(1,133명)의 연도는 기사에 없음"], xref=["S4-M-008", "S4-I-006"])
add(id="I5-M-017", type="지표", indicator="I5-T8", importance=3,
    statement="정부는 2030년까지 100만 명 이상에게 AI 직업훈련을 지원하고, 2027년 한국형 AI 노출지수(K-AIOE)를 만들어 직업·업종·연령별 고용 변화를 보는 '한국형 카나리아 대시보드'를 구축하기로 했다.",
    value=1000000, unit="명 (2030년까지 AI 직업훈련)", as_of="2026-07", region="KR", definition="산업전환 고용안정 기본계획의 AI 직업훈련 목표",
    sources=src("moel_plan"), verified=True)
add(id="I5-M-018", type="지표", indicator="I5-T5", importance=2,
    statement="세계경제포럼은 2030년까지 일자리 1억 7천만 개가 생기고 9,200만 개가 사라져 순증 7,800만 개를 전망했다. 줄어드는 직무로는 계산원·사무보조원, 늘어나는 직무로는 AI·로봇·재생에너지 전문직을 꼽았다. 고용주의 41%는 AI 자동화로 인력을 줄일 계획이라고 답했다.",
    value=78, unit="백만 개 (2030년 순증 전망)", as_of="2025-01", region="GLOBAL", definition="세계경제포럼 고용주 설문 기반 전망",
    extra={"created": "1억 7천만", "displaced": "9,200만", "employers_reduce": "41%"}, sources=src("wef"), verified=True,
    check_flags=["고용주 전망 설문이며 실측치가 아님"])

# ---------- 사건 (E) ----------
add(id="I5-E-001", type="사건", importance=2, date="2025-01-08", actor="세계경제포럼",
    statement="세계경제포럼이 Future of Jobs Report 2025에서 2030년까지 일자리 1억 7천만 개 생성, 9,200만 개 소멸을 전망했다.", sources=src("wef"), verified=True)
add(id="I5-E-002", type="사건", importance=2, date="2025-05-20", actor="Klarna",
    statement="Klarna가 상담 인력을 AI로 대체하던 방침을 바꿔 사람 상담원 채용을 다시 시작했다. AI와 사람 상담을 함께 두는 방식이라고 밝혔다.", sources=src("klarna"), verified=True)
add(id="I5-E-003", type="사건", importance=2, date="2025-08-26", actor="Stanford Digital Economy Lab",
    statement="Stanford 연구진이 AI 노출이 큰 직무의 22~25세 고용이 다른 직무보다 13% 상대적으로 줄었다는 첫 분석을 냈다.", sources=src("canaries25"), verified=True)
add(id="I5-E-004", type="사건", importance=3, date="2025-09-01", actor="Salesforce",
    statement="Salesforce CEO가 AI 에이전트 도입 뒤 고객지원 인력을 9,000명에서 약 5,000명으로 줄였다고 밝혔다.", sources=src("salesforce"), verified=True,
    check_flags=["CEO 발언 기준 — 회사 공시로는 확인하지 못함"])
add(id="I5-E-005", type="사건", importance=2, date="2025-09-25", actor="Accenture",
    statement="Accenture가 3개월 동안 1만 1천 명 넘게 인력을 줄였다고 밝혔다. CEO는 필요한 기술에 대해 재교육은 현실적인 경로가 아니라고 말했고, 구조조정 비용은 8억 6,500만 달러다.", sources=src("accenture"), verified=True)
add(id="I5-E-006", type="사건", importance=2, date="2025-10-28", actor="Amazon",
    statement="Amazon이 본사 인력 약 1만 4천 명(본사 인력의 약 4%) 감원을 발표했다. 회사는 관료주의와 조직 계층을 줄이는 조치라고 설명했다.", sources=src("amazon25"), verified=True)
add(id="I5-E-007", type="사건", importance=3, date="2025-10-30", actor="한국은행",
    statement="한국은행이 'AI 확산과 청년고용 위축' 보고서에서 AI 노출 업종의 청년 일자리 감소와 50대 일자리 증가를 분석했다.", sources=src("bok25"), verified=True)
add(id="I5-E-008", type="사건", importance=2, date="2025-12-18", actor="고용노동부",
    statement="고용노동부가 5년간 100만 명에게 AI 훈련을 제공하는 '노동시장 AI 인재양성 추진방안'을 발표했다. 주니어 개발자 1만 명을 AI 엔지니어로 키우는 과정이 들어 있다.", sources=src("moel_ai"), verified=True)
add(id="I5-E-009", type="사건", importance=2, date="2026-01-07", actor="LinkedIn",
    statement="LinkedIn이 2026년 미국 떠오르는 직업 1·2위로 AI 엔지니어와 AI 컨설턴트·전략가를 발표했다.", sources=src("linkedin"), verified=True)
add(id="I5-E-010", type="사건", importance=3, date="2026-01-28", actor="Amazon",
    statement="Amazon이 본사 인력 약 1만 6천 명을 추가로 줄여 2025년 10월 이후 감원이 3만 명을 넘었다. CEO는 2025년 6월 AI로 본사 인력이 줄어들 것이라고 예고한 바 있다.", sources=src("amazon26", "yale"), verified=True,
    check_flags=["Fortune은 Amazon이 감원 사유를 AI가 아닌 관료주의 축소로 설명했다고 보도"])
add(id="I5-E-011", type="사건", importance=2, date="2026-02-02", actor="Yale Budget Lab",
    statement="Yale Budget Lab이 ChatGPT 출시 이후 직업 구성 변화가 경제 전체로는 큰 충격이 아니라 안정에 가깝다는 갱신 분석을 냈다. AI 고노출 직무의 실업 기간도 변하지 않았다.", sources=src("yale"), verified=True)
add(id="I5-E-012", type="사건", importance=3, date="2026-07-09", actor="정부(고용노동부 등)",
    statement="정부가 '산업전환 고용안정 기본계획'을 발표했다. 한국형 AI 노출지수와 카나리아 대시보드 구축, 2030년까지 100만 명 AI 직업훈련, 소득 기반 고용보험 전환을 담았다.", sources=src("moel_plan"), verified=True)
add(id="I5-E-013", type="사건", importance=3, date="2026-08-06", actor="Challenger, Gray & Christmas",
    statement="7월 감원 보고서에서 AI가 다섯 달 연속 감원 사유 1위였다(7월 1만 970명, 연초 이후 11만 2,713명).", sources=src("chall_jul"), verified=True)
add(id="I5-E-014", type="사건", importance=3, date="2026-08-12", actor="Stanford Digital Economy Lab",
    statement="Stanford 연구진이 갱신 분석에서 AI 노출 직무의 22~25세 고용 격차가 19%로 커졌다고 밝혔다(2025년 7월 자료 15%).", sources=src("canaries26"), verified=True)
add(id="I5-E-015", type="사건", importance=3, date="2026-08-18", actor="한국은행",
    statement="한국은행이 BOK 이슈노트에서 최근 청년 고용 감소의 주원인은 AI가 아닐 가능성이 크고, AI는 경력직 선호 같은 기존 변화를 키우는 요인이라고 분석했다.", sources=src("bok26"), verified=True)
add(id="I5-E-016", type="사건", importance=2, date="2026-10-01", actor="Challenger, Gray & Christmas",
    statement="9월 감원 보고서에서 AI 사유 감원은 3,961명으로 사유 5위로 내려갔다. 1위는 시장·경제 상황(8,789명)이었다.", sources=src("chall_sep"), verified=True)
add(id="I5-E-017", type="사건", importance=2, date="2026-10-16", actor="국가데이터처",
    statement="9월 고용동향에서 청년(15~29세) 취업자가 47개월 연속 줄었다. 국가데이터처는 이번 발표부터 15~34세 기준 통계도 함께 냈다.", sources=src("kostat_sep"), verified=True)
add(id="I5-E-018", type="사건", importance=2, date="2026-09-16", actor="잡코리아",
    statement="잡코리아가 2026년 상반기 AI 직무 공고 분석에서 비개발 AI 직무 공고가 1년 새 325% 늘었다고 발표했다.", sources=src("jobkorea"), verified=True)

# ---------- 해석 (I) ----------
add(id="I5-I-001", type="해석", importance=3, target="신입·청년 사무직", direction="강화",
    statement="AI 노출 직무의 신입 고용 감소는 미국과 한국 통계에서 함께 보인다. 미국은 22~25세 격차가 15%에서 19%로 커졌고, 한국은 청년 일자리 감소의 94~99%가 AI 노출 업종에서 나왔다. 다만 두 분석 모두 인과를 확정하지 않았고, 한국은행은 AI를 주원인이 아닌 가속 요인으로 봤다.",
    basis=["I5-M-001", "I5-M-002", "I5-M-003", "I5-E-015"])
add(id="I5-I-002", type="해석", importance=3, target="영향 경로", direction="중립",
    statement="AI의 고용 영향은 해고보다 채용 축소로 나타난다. AI 때문에 해고한 서비스 기업은 1%였지만 채용을 줄인 곳은 12%였고, 줄어든 채용은 대졸 직무에 몰렸다. 고용 감소가 신입에만 보이고 경력자에게 보이지 않는 것도 같은 방향이다.",
    basis=["I5-M-008", "I5-M-001", "I5-M-002"])
add(id="I5-I-003", type="해석", importance=3, target="AI 사유 감원", direction="중립",
    statement="AI를 사유로 든 감원은 2025년 1~11월 약 5만 5천 명에서 2026년 1~9월 12만 명으로 늘었다. 그러나 3~7월에 몰렸고 8~9월에는 월 4천 명 아래로 줄었다. 큰 감원을 한 Amazon도 사유를 관료주의 축소로 설명해, 이 수치는 실제 대체 규모가 아니라 기업이 밝힌 사유의 집계로 읽어야 한다.",
    basis=["I5-M-004", "I5-M-005", "I5-M-006", "I5-E-006", "I5-E-010"])
add(id="I5-I-004", type="해석", importance=2, target="고객응대·상담", direction="중립",
    xref=["S4-I-002", "S4-M-005"], statement="고객 상담은 개별 기업 단위의 감축 신호만 있고 방향이 엇갈린다. Salesforce는 지원 인력을 약 4,000명, KB국민은행은 상담사를 264명 줄였다. 반면 Klarna는 사람 상담원을 다시 뽑았고, 신한은행은 AICC 도입 뒤에도 상담 인력이 늘었다. 상담 직무 전체의 고용 통계는 아직 없다.",
    basis=["I5-E-004", "I5-M-016", "I5-E-002"])
add(id="I5-I-005", type="해석", importance=3, target="소프트웨어 개발", direction="중립",
    statement="소프트웨어 개발은 수요가 줄었다기보다 경력과 AI 쪽으로 옮겨 가고 있다. 미국 개발 공고는 2025년 2월 이후 15% 늘었지만 순증의 71%가 시니어였다. 한국은 AI가 아닌 개발 공고가 6.6% 줄었고, 컴퓨터 프로그래밍 업종의 청년 고용은 16.6% 감소했다.",
    basis=["I5-M-007", "I5-M-012", "I5-M-002"])
add(id="I5-I-006", type="해석", importance=3, target="새 직무·업종", direction="강화",
    statement="새 직무는 채용공고에서 먼저 보이고 공식 분류는 뒤따르지 못한다. LinkedIn 상위 5개 중 4개가 AI 직무이고, 잡코리아 AI 전문 직무 공고는 128%, 비개발 AI 직무는 325% 늘었다. 반면 미국 표준직업분류는 2028년에야 개정되고, 한국직업사전에서 확인된 AI 신규 직업은 1개다.",
    basis=["I5-M-011", "I5-M-012", "I5-M-013", "I5-M-014"])
add(id="I5-I-007", type="해석", importance=2, target="한국 정책", direction="강화",
    statement="한국 정부의 대응은 훈련 확대에서 감지 체계로 넓어졌다. 2025년 12월에는 100만 명 AI 훈련이 중심이었고, 2026년 7월에는 한국형 AI 노출지수와 직업·연령별 고용 대시보드를 더했다.",
    basis=["I5-E-008", "I5-E-012", "I5-M-017"])
add(id="I5-I-008", type="해석", importance=3, target="한국 청년 고용", direction="강화",
    statement="한국에서도 '신입은 줄고 경력은 는다'는 패턴이 미국과 같다. 청년 취업자는 47개월 연속 줄었지만 사무종사자 전체는 늘었고, AI 노출 업종에서는 50대 일자리가 늘었다.",
    basis=["I5-M-015", "I5-M-002", "I5-M-003", "I5-M-001"])

# ---------- 세부 전망 (F) ----------
ON = "2026-10-29"
add(id="I5-F-001", type="전망", importance=3, status="유효", forecast_status="진행 중", made_on=ON,
    statement="2027년 1~6월 Challenger 집계의 AI 사유 감원 누계는 2026년 같은 기간(10만 1,743명)보다 적을 것이다.",
    due="2027-07-31", condition="Challenger가 AI 사유 분류를 유지할 경우",
    method="Challenger 2027년 6월 보고서의 AI 사유 연초 이후 누계와 101,743명(2026년 7월 누계 112,713명 - 7월 10,970명) 비교",
    reasoning="AI 사유 감원은 2026년 3~7월에 몰렸고 8~9월은 월 4천 명 아래로 내려왔다.",
    counter="대형 기술 기업이 연초 구조조정에서 AI를 사유로 들면 한 달에도 수만 명이 늘 수 있다.",
    basis=["I5-M-004", "I5-M-005", "I5-I-003"], result=None)
add(id="I5-F-002", type="전망", importance=3, status="유효", forecast_status="진행 중", made_on=ON,
    statement="Stanford Digital Economy Lab의 다음 갱신에서 AI 노출 상위 직무 22~25세의 고용 격차는 19% 이상으로 유지되거나 커질 것이다.",
    due="2027-09-30", condition="같은 방법(ADP 자료, 노출 분위 비교)으로 갱신이 발표될 경우",
    method="Stanford Digital Economy Lab 갱신 보고서의 22~25세 노출 상위 직무 격차 수치 확인. 2027-09-30까지 갱신이 없으면 판정 불가",
    reasoning="격차가 2025년 7월 15%에서 2026년 6월 19%로 커졌고, 같은 기간 신입 채용을 줄이겠다는 기업이 늘었다.",
    counter="개발 공고처럼 AI 노출 직무의 채용이 다시 늘고 있어 신입 고용도 회복될 수 있다.",
    basis=["I5-M-001", "I5-M-008", "I5-I-002"], result=None)
add(id="I5-F-003", type="전망", importance=2, status="유효", forecast_status="진행 중", made_on=ON,
    statement="2027년 4월 발표되는 3월 고용동향에서도 한국 청년(15~29세) 취업자는 1년 전보다 줄어 있을 것이다(53개월 연속 감소).",
    due="2027-04-30", condition="15~29세 기준 통계가 계속 발표될 경우",
    method="국가데이터처 2027년 3월 고용동향의 15~29세 취업자 전년 동월 대비 증감 확인",
    reasoning="청년 취업자는 47개월 연속 줄었고, 한국은행은 경력직 선호와 AI가 겹친 구조 변화로 봤다.",
    counter="청년 인구 감소 폭이 줄거나 경기 회복으로 채용이 늘면 반등할 수 있다.",
    basis=["I5-M-015", "I5-M-002", "I5-I-008"], result=None)
add(id="I5-F-004", type="전망", importance=2, status="유효", forecast_status="진행 중", made_on=ON,
    statement="2027년 6월 Indeed 미국 소프트웨어 개발 채용공고 지수는 여전히 2020년 2월 수준(100)보다 낮을 것이다.",
    due="2027-07-31", condition="Indeed가 같은 지수를 계속 발표할 경우",
    method="Indeed Hiring Lab 소프트웨어 개발 채용공고 지수의 2027년 6월 값이 100 미만인지 확인",
    reasoning="1년 반 동안 15% 늘었지만 아직 27.5% 낮고, 늘어난 공고는 시니어와 AI 직무에 몰렸다.",
    counter="AI 제품 개발 수요가 빠르게 늘면 1년 안에 격차가 닫힐 수 있다.",
    basis=["I5-M-007", "I5-M-012", "I5-I-005"], result=None)
add(id="I5-F-005", type="전망", importance=2, status="유효", forecast_status="진행 중", made_on=ON,
    statement="잡코리아의 2027년 상반기 분석에서도 AI 전문 직무 공고는 1년 전보다 늘어 있을 것이다.",
    due="2027-09-30", condition="잡코리아가 같은 분류로 분석을 발표할 경우",
    method="잡코리아 2027년 상반기 AI 직무 공고 분석의 전년 대비 증감률이 0%보다 큰지 확인",
    reasoning="AI 전문 직무 공고가 128%, 비개발 AI 직무가 325% 늘었고, 미국에서도 AI 직무가 떠오르는 직업 상위를 차지했다.",
    counter="경기 둔화로 전체 채용이 줄면 AI 직무 공고도 함께 줄 수 있다.",
    basis=["I5-M-012", "I5-M-011", "I5-I-006"], result=None)

add(id="I5-F-101", type="전망", importance=3, status="유효", forecast_status="진행 중", scenario="낙관", made_on=ON,
    statement="2027년 말까지 AI의 고용 충격은 신입 채용 축소에 머물고, 새 AI 직무와 재교육이 이를 일부 상쇄한다. AI 사유 감원은 2026년보다 줄고, 개발 공고 회복이 이어지며, 한국 청년 취업자 감소가 멈춘다.",
    milestones=[{"by": "2027-04", "text": "한국 청년 취업자 감소 멈춤"}, {"by": "2027-07", "text": "상반기 AI 사유 감원 2026년보다 적음"}, {"by": "2027-09", "text": "AI 직무 공고 증가 지속"}],
    due="2027-12-31", condition="경기 침체가 없을 경우",
    method="세 가지 중 두 가지 이상 충족 시 적중: (1) Challenger 2027년 연간 AI 사유 감원이 2026년 연간보다 적음 (2) Indeed 소프트웨어 개발 공고 지수 2027년 12월 값이 2026년 6월 값보다 높음 (3) 한국 15~29세 취업자가 2027년 중 전년 동월 대비 증가한 달이 1번 이상",
    basis=["I5-M-005", "I5-M-007", "I5-M-015", "I5-I-002"],
    signposts=[{"id": "I5-F-001", "on_hit": "낙관", "on_miss": "비관"}, {"id": "I5-F-002", "on_hit": "비관", "on_miss": "낙관"},
               {"id": "I5-F-003", "on_hit": "비관", "on_miss": "낙관"}, {"id": "I5-F-005", "on_hit": "낙관"}], result=None)
add(id="I5-F-102", type="전망", importance=3, status="유효", forecast_status="진행 중", scenario="비관", made_on=ON,
    statement="2027년 말까지 신입 채용 축소가 경력 초기 전반으로 번진다. Stanford 격차가 26~30세에서도 나타나고, AI 사유 감원이 2026년을 넘으며, 한국 청년 고용률은 43% 아래로 내려간다.",
    milestones=[{"by": "2027-04", "text": "한국 청년 취업자 53개월 연속 감소"}, {"by": "2027-07", "text": "상반기 AI 사유 감원 2026년 이상"}, {"by": "2027-09", "text": "Stanford 격차 19% 이상, 26~30세 격차 확인"}],
    due="2027-12-31", condition="없음",
    method="세 가지 중 두 가지 이상 충족 시 적중: (1) Stanford 갱신에서 26~30세 노출 상위 직무에도 통계적으로 의미 있는 격차 (2) Challenger 2027년 연간 AI 사유 감원이 2026년 연간 이상 (3) 한국 15~29세 고용률 월간 값이 43.0% 미만인 달이 2027년 중 1번 이상",
    basis=["I5-M-001", "I5-M-004", "I5-M-015", "I5-I-001"],
    signposts=[{"id": "I5-F-001", "on_hit": "낙관", "on_miss": "비관"}, {"id": "I5-F-002", "on_hit": "비관", "on_miss": "낙관"},
               {"id": "I5-F-003", "on_hit": "비관", "on_miss": "낙관"}, {"id": "I5-F-004", "on_hit": "비관"}], result=None)

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

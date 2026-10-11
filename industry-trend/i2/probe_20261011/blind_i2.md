# I2 백지 재조사 (검증용) — 2026-10-11

- 읽은 내부 파일: request_r1.md 1개뿐. 웹 조사(WebSearch/WebFetch)만 사용. records.jsonl·article·signal은 이 단계에서 열지 않음.
- 원문확인 기준: "예" = 1차 출처(기업 공식 발표·실적 원문·공식 블로그) 페이지를 직접 열어 해당 값을 읽음. "아니오" = 2차 기사·요약·스니펫만 확인(2차 기사 본문을 읽은 경우도 원문 아님). "접근불가" = ROBOTS_DISALLOWED 또는 fetch 오류.
- 등급: A 기업 공식·정부·1차, B 주요 언론·전문지·조사 요약, C 블로그·집계 사이트·익명 출처(단독 근거 금지).
- 한계: 검색 엔진이 링크만 돌려주는 경우가 많아 본문을 연 페이지 위주로 적었다. 열지 못한 값은 "미확인"으로 표시했다.

## 1. 지표별 최신값

| 지표ID | 값 | 단위 | 기준 시점 | 지역 | 측정 조건 | 출처 URL | 등급 | 원문확인 |
|---|---|---|---|---|---|---|---|---|
| I2-T1a | ChatGPT 주간 이용자 9억 명, 유료 구독자 5천만 명 | 명 | 2026-02-27 발표 | 글로벌 | OpenAI 블로그(1,100억 달러 투자 발표와 함께), TechCrunch 인용 | https://techcrunch.com/2026/02/27/chatgpt-reaches-900m-weekly-active-users | B | 아니오 |
| I2-T1b | ChatGPT·OpenAI 제품군 주간 이용자 10억 명 이상, 기업 고객 250만 | 명 | 2026-09-08 확인(8월 중순 스냅숏) | 글로벌 | OpenAI가 확인했다는 보도. 7월 29일 TNW는 The Information 인용 '10억 직전'. ChatGPT 단독인지 제품군 합산인지 기사 표현이 다름 | https://cryptobriefing.com/chatgpt-one-billion-weekly-users/ | B | 아니오 |
| I2-T1c | Gemini 앱 월간 이용자 9억 5천만 명 이상, 일간 이용자 1년 새 3배 | 명 | Q2 2026 (2026-07-22) | 글로벌 | Alphabet 실적 CEO 발언. 월간 기준이라 ChatGPT 주간과 직접 비교 불가 | https://blog.google/company-news/inside-google/message-ceo/alphabet-earnings-q2-2026/ | A | 예 |
| I2-T1d | Microsoft 365 Copilot 유료 좌석 3천만 석 이상(FY26 Q2 1,500만 → Q3 2,000만 → Q4 3,000만). GitHub 이용자 2.25억 명 중 5천만 명이 Copilot 이용. Agent 365에 등록된 에이전트 4천만 개 | 석·명·개 | FY26 Q4 (2026-07-29) | 글로벌 | 등록 에이전트 수는 실제 업무 수행 여부와 다름(해설자 지적) | https://office365itpros.com/2026/07/30/fy26-q4-microsoft-results/ | B | 아니오 |
| I2-T1e | Meta Business Agents: 주 100만 개 이상 기업이 고객 응대·판매에 사용. Meta AI 일간 이용자 60% 증가(전체 이용자 수 미공개). 개인 에이전트는 미출시 | 곳·% | Q2 2026 (2026-07-29) | 글로벌 | Meta 실적 발표문 | https://s21.q4cdn.com/399680738/files/doc_financials/2026/q2/META-Q2-2026-Prepared-Remarks.pdf | A | 예 |
| I2-T2a | Anthropic 연환산 매출 650억 달러 이상(7월 말), 5월 470억 달러, 2025년 말 약 90억 달러. 회사 최신 공식 수치는 470억 달러(Series H 글) | 달러 | 2026-07 말 | 글로벌 | Bloomberg·Reuters 보도, 익명 소식통. 회사 발표 아님. Claude Code 단독 수치는 이번 조사에서 새로 찾지 못함 | https://www.unite.ai/?p=453467 | B (추정) | 아니오 |
| I2-T2b | Claude Code 연환산 매출 25억 달러 이상(2026-02, Anthropic 투자 유치 시점), 출시 6개월에 10억 달러. Uber 엔지니어 5천 명 중 84%가 월 1회 이상 이용, 커밋 코드 70% AI 작성(2026-04) | 달러·% | 2026-02, 2026-04 | 글로벌·미국 | 2차 해설(Enterprise DNA)이 Anthropic을 출처로 적었으나 Uber 수치엔 별도 출처 없음 | https://enterprisedna.co/resources/news/claude-code-25-billion-arr-anthropic-2026 | B | 아니오 |
| I2-T2c | Cursor(Anysphere) 연환산 매출 40억 달러 이상 | 달러 | 2026-06 초 | 글로벌 | 익명 소식통 인용(Dealroom). 회사 미확인 | https://dealroom.co/news/134107-cursor-tops-4b-annualized-revenue/ | C | 아니오 |
| I2-T2d | Cognition(Devin) 연환산 매출 약 9억 달러, 연초의 3배 이상 | 달러 | 2026-08 | 글로벌 | CryptoBriefing→KuCoin 재게재. 기사 안에서 연초 기준 값이 2.8억·4.92억으로 엇갈림 | https://www.kucoin.com/news/flash/cognition-ai-hits-900m-arr-plans-800m-cash-burn-in-2026 | C | 아니오 |
| I2-T2e | OpenAI Codex 주간 이용자 500만 명 이상(2026-07-09), 업무(비개발)용 100만 명 이상. 이후 800만 명(7월 14일, OpenAI 임원 자체 보고) | 명 | 2026-07 | 글로벌 | 500만은 OpenAI 공식 페이지에서 확인. 800만은 해설 사이트 인용(B/C) | https://openai.com/index/chatgpt-for-your-most-ambitious-work/ | A (500만) | 예 (500만), 아니오 (800만) |
| I2-T2f | Google 신규 코드의 75%를 AI가 생성(사람 검토). 2024-10 25%, 2025 가을 50% | % | 2026-04 | 글로벌 | Pichai 발언 보도(Semafor·The Decoder). 원문 블로그 미열람 | https://the-decoder.com/google-says-75-percent-of-its-new-code-is-now-written-by-ai/ | B | 아니오 |
| I2-T3a | OpenAI ChatGPT Work(시간 단위 프로젝트를 앱·파일 횡단으로 수행) 2026-07-09 출시. 이용자·작업 수는 비공개. 같은 날 Codex 앱과 합쳐진 데스크톱 앱을 전 요금제에 제공 | 상태 | 2026-07-09 | 글로벌 | 사용량 한도는 Codex와 같은 구조 | https://openai.com/index/chatgpt-for-your-most-ambitious-work/ | A | 예 |
| I2-T3b | Bloomberg Government 보도 제목: OpenAI 모델이 10억 명 이상 활성 이용자, 200만 기업에 도달, 주간 출력 토큰의 99.8%가 Codex 기반 에이전트 작업 | 명·% | 2026-07-31 | 글로벌 | 제목·요약만 확인. 정의와 분모 미확인 | https://news.bgov.com/artificial-intelligence/openai-has-more-than-1-billion-users-2-million-businesses | B | 아니오 |
| I2-T4a | Waymo 주간 유료 탑승 50만 회 이상(Q1 실적 시점, Q2 실적에서도 '50만 이상'으로 재인용), 목표 연말 100만 회. 누적 2천만 회 이상 | 회/주 | 2026 Q1~Q2 | 미국 | Q2 재인용·캘리포니아 일 탑승 감소(4월 47,205 → 6월 44,964)는 예측 서비스 페이지 인용이라 약함 | https://futuresearch.ai/waymo-financial-forecast/ | C | 아니오 |
| I2-T4b | Waymo 도시: 2026-09-01 덴버·샌디에이고·탬파 유료 공개 → 총 14개 시장. 2026-10-08 Waymo 블로그는 '지난달 15번째 미국 도시 출시' | 곳 | 2026-09~10 | 미국 | 차량 4,000대 이상(보도 B). 공식 블로그엔 차량·탑승 수치 없음 | https://waymo.com/blog/2026/10/waymo-closes-5-billion-debt-financing/ | A (15번째 도시) | 예 |
| I2-T4c | Waymo 운영 차질: 5~7월 고속도로 운행 중단, 약 3,871대 소프트웨어 리콜, 침수 우려로 일부 도시 운행 중단 | 건 | 2026-05~08 | 미국 | 예측 서비스 페이지·Korea Business Review 미리보기 인용 | https://futuresearch.ai/waymo-financial-forecast/ | C | 아니오 |
| I2-T4d | Tesla 로보택시: Q2 주주 업데이트에서 무감독(unsupervised) 운행 6개 도시(오스틴·댈러스·휴스턴·마이애미·올랜도·탬파), 누적 유료 주행 약 240만 마일, 무감독 38만 마일 이상, '주목할 사고 0건'(회사 주장). 샌프란시스코 베이는 안전요원 탑승 | 곳·마일 | 2026-07-22 | 미국 | 회사 자체 수치. 차량 대수 미공개 | https://evwire.com/p/tesla-robotaxi-2-4-million-paid-miles-six-metros | B | 아니오 |
| I2-T4e | Tesla Cybercab 승객 탑승 2026-09-03 시작(오스틴 한정으로 보임, 앱은 6개 도시). 텍사스 자율주행 등록 차량 314~420대(출처별 상이), Cybercab 45~67대 | 대 | 2026-09 | 미국 | 등록 대수는 운행·유료 대수와 다름. 요금 미확인 | https://engadget.com/2250874/tesla-offering-cybercab-robotaxi-rides/ | B | 아니오 |
| I2-T4f | Baidu Apollo Go: Q2 완전 무인 운행 약 100만 회, 누적 2,300만 회 이상, 28개 도시, 완전 무인 2.4억 km 이상. 일부 중국 도시 규제로 운행 일시 조정, 8월 재개. 두바이 완전 무인 상업 운영 시작 | 회·곳 | Q2 2026 (2026-08-18) | 중국·중동 | 도시 수·거리는 실적 릴리스(SEC 6-K)에서 확인, 100만 회·2,300만 회는 실적 콜 요약(MarketBeat) | https://www.sec.gov/Archives/edgar/data/0001329099/000119312526355431/d112854dex991.htm | A (도시·거리) / B (탑승 수) | 예 (도시·거리), 아니오 (탑승 수) |
| I2-T5a | 휴머노이드 출하(2026 상반기): AgiBot 약 8,400대(44%), Unitree 약 5,900대(31%), 전 세계 약 19,100대(+272% YoY), 중국 업체 97% 이상 | 대 | 2026-01~06 (2026-08-10 보도) | 글로벌 | Smart Analytics Global 단일 조사. 출하 대수는 현장 가동 대수와 다름(교육·연구·전시 포함 가능) | https://www.eweek.com/news/china-humanoid-robots-agibot-unitree-apac/ | B (단일 조사사) | 아니오 |
| I2-T5b | Agility Digit: 고객 시설 9곳 누적 6만 5천 시간 이상(회사 발표), 고객 GXO·Schaeffler·Toyota Canada·Mercado Libre. RoboFab 연 최대 1만 대 설계(용량). Figure 02 BMW 11개월 파일럿 1,250시간·부품 9만 개 이상(2025-11 보고), 이후 Figure 03이 물류 순서화로 이동 | 시간 | 2026-07 | 미국 | 단일 고객 배치 대수 미공개 | https://humanoid.guide/humanoid-deployments-in-2026-favor-figure-and-agility/ | B | 아니오 |
| I2-T5c | Tesla Optimus: 2026 Q3 초기 제조 시작 예정(Fremont), 초기 물량은 내부 학습용 'Optimus Academy'. 2026-07-02 출하 보고에 Optimus 수치 없음. 외부 판매 시점 미확인 | 상태 | 2026-07 | 미국 | Q2 콜 요약(비공식 요약) | https://notateslaapp.com/news/4481/summary-of-teslas-2026-q2-earnings-call-cybercab-fsd-ai4-and-more | B | 아니오 |
| I2-T5d | 현대차그룹 Atlas: 2028년 연 3만 대 생산 체계, 초기 약 2.5만 대는 현대·기아 공장에 투입, 2028년 HMGMA 단계적 안전 검증, 2030년 이후 조립 확대 | 대 | 2026-07-25 보도 | 한국·미국 | 계획·전망이며 가동 실적 아님 | https://www.newsis.com/view/NISX20260721_0003717549 | B | 예 (뉴시스 본문) |
| I2-T6a | KPMG 미국 대기업(매출 10억 달러 이상, 314명) 62%가 에이전트를 '구축·배치·개발 중'(전 분기 53%), 멀티에이전트 25%(6%에서), 약 60%가 측정 가능한 사업 가치 보고, 49%가 자율 결정 금지 고위험 사례 정의 | % | 설문 2026-07-24~08-25, 발표 2026-09-24 | 미국 | '개발 중' 포함이라 운영 비율 아님 | https://kpmg.com/us/en/media/news/q3-ai-pulse-2026.html | A | 예 |
| I2-T6b | Liferay 조사: 미국 AI 의사결정·실무자 500명 중 54%가 에이전트를 '운영 또는 시범', 25%가 명확한 KPI로 성과 측정, 24%가 전사 AI 사용 정책 | % | 2026-08-12 발표 | 미국 | 벤더 조사, 정의·가중치 미공개, Pollfish | https://www.cmswire.com/the-wire/new-liferay-study-finds-54-of-companies-are-running-ai-agents-yet-only-25-measure-their-impact/ | B (벤더 조사) | 아니오 |
| I2-T6c | Gartner: 에이전틱 AI 프로젝트의 40% 이상이 2027년 말까지 중단될 것(전망, 2025-06 발표). 에이전트워싱 — 실제 에이전트 공급사 약 130곳 | % | 2025-06 | 글로벌 | 2025년 웨비나 응답자 3,412명 기반 전망. 2026 후속 갱신은 못 찾음 | https://www.silicon.eu/gartner-over-40-percent-of-agentic-ai-projects-will-be-discontinued-by-the-end-of-2027-18197.html | B | 아니오 |
| I2-T7a | Cursor+Claude Opus 4.6 에이전트가 PocketOS 운영 DB와 백업을 9초 만에 삭제(2026-04, 스테이징 작업 중 무관한 API 토큰 사용). 3개월 전 백업으로 복구, 30시간 이상 장애. Railway는 해당 엔드포인트에 지연 삭제 적용 | 건 | 2026-04 (보도 2026-05-04) | 미국 | 창업자 주장 중심. Cursor·Anthropic 응답은 기사에 없음 | https://www.techrepublic.com/fr/article/ai-agent-deletes-company-database-admits-violating-guardrails/ | B | 아니오 |
| I2-T7b | Adversa AI 집계: 2025-06~2026-07 공개 데이터 삭제 사고 9건(Cursor, Replit, Claude Code 3건, Gemini CLI, Antigravity, Kiro 등). 이 목록에는 2026-04 PocketOS 사건이 없음. Amazon은 Kiro 건을 잘못 설정된 권한 탓으로 반박 | 건 | 2026-08-04 | 글로벌 | 포럼·이슈·언론 기반, 선정 절차 없음 | https://adversa.ai/blog/ai-coding-agent-incidents/ | B (업체 집계) | 예 |
| I2-T7c | Microsoft Copilot Studio·Salesforce Agentforce 프롬프트 인젝션으로 공개 폼 경유 기업 데이터 유출 가능(Capsule Security 발견, OECD.AI가 AI 사고로 분류), 양사 패치 | 건 | 2026-04-15 | 글로벌 | 유출이며 삭제·손상과 다름. 패치 후에도 유출 보도 있음 | https://oecd.ai/en/incidents/2026-04-15-d934 | B | 예 (OECD 페이지) |
| I2-T8a (한국) | 서울시: 2026-11 마포 상암동에서 '레벨4 로보택시'를 앱 호출로 운행 예정. 초기에는 조수석 안전관리자 탑승(무인 아님) | 상태 | 2026-06-30 보도 | 한국 | 운영사·대수 기사에 없음 | https://v.daum.net/v/20260630111713463 | B | 예 (기사 본문) |
| I2-T8b (한국) | 카카오모빌리티 강남 심야(평일 22~05시) 자율주행 택시 2026-03-16 시작, 무료 후 4월 유료 전환 예정. 안전요원 탑승 여부·대수는 기사에 없음 | 상태 | 2026-03-15 | 한국 | 이후 실제 유료 전환 여부는 확인 못 함 | https://biz.sbs.co.kr/amp/article/20000297494 | B | 예 (기사 본문) |
| I2-T8c (한국) | 포스코DX 운영 AI 에이전트 110개, 재무팀 업무량 80% 감소(2026-02 도입 후), LG유플러스 고객 응대 시간 60% 단축 | 개·% | 2026-05-03 보도 | 한국 | 기업 주장을 한국경제가 2차 인용 | https://www.hankyung.com/article/2026050328881 | B | 예 (기사 본문) |
| I2-T8d (한국) | 한국 레벨4 목표 2027년, 광주 200대 실증 | 대 | 2026-09-10 보도 | 한국 | 유료 기사 미리보기만 확인 | https://www.koreabizreview.com/articles/global-radar-ai-tech-50-20260910-12gm | B | 아니오 (미리보기) |

## 2. 사건 목록 (월별)

| 날짜 | 주체 | 한 문장 사실 | 중요도 | 출처 URL | 등급 | 원문확인 |
|---|---|---|---|---|---|---|
| 2026-01-05 | 현대차그룹 | CES에서 Atlas를 2028년 미국 공장에 투입하겠다고 발표 | 2 | https://www.heraldk.com/article/2026010514301001612 | B | 아니오 |
| 2026-02-27 | OpenAI | ChatGPT 주간 9억 명·유료 5천만 명 공개 | 3 | https://techcrunch.com/2026/02/27/chatgpt-reaches-900m-weekly-active-users | B | 아니오 |
| 2026-03-16 | 카카오모빌리티 | 강남 심야 자율주행 택시 시작(무료) | 2 | https://biz.sbs.co.kr/amp/article/20000297494 | B | 예 |
| 2026-04 | PocketOS | Cursor+Opus 4.6 에이전트가 운영 DB·백업 삭제 | 3 | https://www.techrepublic.com/fr/article/ai-agent-deletes-company-database-admits-violating-guardrails/ | B | 예 (기사 본문) |
| 2026-04-15 | Capsule Security | Copilot Studio·Agentforce 프롬프트 인젝션 데이터 유출 취약점 | 2 | https://oecd.ai/en/incidents/2026-04-15-d934 | B | 예 |
| 2026-04 | Google | 신규 코드 75% AI 생성 발언 | 2 | https://the-decoder.com/google-says-75-percent-of-its-new-code-is-now-written-by-ai/ | B | 아니오 |
| 2026-05 | Anthropic | 연환산 매출 470억 달러(5월) | 3 | https://www.unite.ai/?p=453467 | B | 아니오 |
| 2026-06 초 | Cursor | 연환산 40억 달러 이상(익명 소식통) | 2 | https://dealroom.co/news/134107-cursor-tops-4b-annualized-revenue/ | C | 아니오 |
| 2026-06-30 | 서울시 | 11월 상암 레벨4 로보택시 계획(조수석 안전관리자) | 2 | https://v.daum.net/v/20260630111713463 | B | 예 |
| 2026-07-09 | OpenAI | ChatGPT Work 출시, Codex 주 500만 명 | 3 | https://openai.com/index/chatgpt-for-your-most-ambitious-work/ | A | 예 |
| 2026-07-22 | Alphabet | Gemini 앱 월 9.5억 명, 90% Fortune 100 Gemini Enterprise | 3 | https://blog.google/company-news/inside-google/message-ceo/alphabet-earnings-q2-2026/ | A | 예 |
| 2026-07-22 | Tesla | Q2 업데이트: 무감독 로보택시 6개 도시, 유료 240만 마일 | 3 | https://evwire.com/p/tesla-robotaxi-2-4-million-paid-miles-six-metros | B | 아니오 |
| 2026-07-29 | Microsoft | M365 Copilot 유료 3천만 석, Agent 365 에이전트 4천만 개 | 3 | https://office365itpros.com/2026/07/30/fy26-q4-microsoft-results/ | B | 아니오 |
| 2026-07-29 | Meta | Business Agents 주 100만 기업 | 2 | https://s21.q4cdn.com/399680738/files/doc_financials/2026/q2/META-Q2-2026-Prepared-Remarks.pdf | A | 예 |
| 2026-07 말 | Anthropic | 연환산 650억 달러 이상(보도) | 3 | https://www.unite.ai/?p=453467 | B | 아니오 |
| 2026-08-10 | SAG | 상반기 휴머노이드 출하 AgiBot 1위(8,400대), 전체 약 1.9만 대 | 3 | https://www.scmp.com/tech/tech-trends/article/3363544/agibot-overtakes-unitree-top-global-humanoid-robot-vendor-first-half-amid-ipo-push | B | 아니오 |
| 2026-08-14 | 캘리포니아 CPUC | Waymo 18개 카운티 확대 승인(예측 서비스 페이지 인용) | 1 | https://futuresearch.ai/waymo-financial-forecast/ | C | 아니오 |
| 2026-08-18 | Baidu | Q2: 28개 도시, 완전 무인 2.4억 km, 무인 100만 회(콜) | 3 | https://www.sec.gov/Archives/edgar/data/0001329099/000119312526355431/d112854dex991.htm | A | 예 (도시·거리) |
| 2026-09-01 | Waymo | 덴버·샌디에이고·탬파 유료 시작, 14개 시장 | 3 | https://cryptobriefing.com/waymo-paid-robotaxi-denver-san-diego-tampa/ | B | 아니오 |
| 2026-09-03 | Tesla | Cybercab 승객 탑승 시작(오스틴) | 3 | https://engadget.com/2250874/tesla-offering-cybercab-robotaxi-rides/ | B | 아니오 |
| 2026-09-08 | OpenAI | 주간 이용자 10억 명 이상 확인(보도) | 3 | https://cryptobriefing.com/chatgpt-one-billion-weekly-users/ | B | 아니오 |
| 2026-09-24 | KPMG | Q3 AI Pulse: 에이전트 구축·배치 62% | 3 | https://kpmg.com/us/en/media/news/q3-ai-pulse-2026.html | A | 예 |
| 2026-10-08 | Waymo | 첫 부채 조달 50억 달러, '15번째 미국 도시' 언급 | 2 | https://waymo.com/blog/2026/10/waymo-closes-5-billion-debt-financing/ | A | 예 |

## 3. 단정성 사실 점검

- '대규모 운영 로보택시는 Waymo 하나'라는 식의 단정은 반례가 있다: Baidu Apollo Go가 분기 완전 무인 약 100만 회·28개 도시(2026 Q2)를 공개했다. 도시 수·주행 거리는 공식 릴리스에서 확인, 탑승 수는 콜 요약(B).
- 'Tesla가 무인 운행을 공식 확인하지 않았다'는 서술은 7월 22일 이후엔 맞지 않을 수 있다. Tesla Q2 업데이트가 6개 도시 무감독 운행을 적은 것으로 3개 보도가 일치한다(Tesla 원문은 열지 못함). 8월 20일 Engadget은 크라우드소싱 추적 기준으로 '회사 미확인'이라 적어 시점에 따라 상충한다.
- '업무형 Agent는 이용량을 공개하지 않았다'는 서술은 부분 반증된다: Codex 주간 500만 명·비개발 업무 100만 명 이상(OpenAI 공식 페이지). 다만 ChatGPT Work 자체의 이용자·작업 수는 비공개.
- '휴머노이드 출하는 Unitree가 앞선다'는 서술은 2026 상반기 SAG 집계(AgiBot 8,400대 > Unitree 5,900대)와 어긋난다(단일 조사사).
- 에이전트 데이터 삭제 사고 9건 집계는 PocketOS(2026-04)를 빠뜨렸다. 집계는 하한선이다.
- 기업 에이전트 '54%'는 Liferay(미국 500명, 운영 또는 시범)와 KPMG(62%, 구축·배치·개발 중, 매출 10억 달러 이상 기업 314명)가 서로 다른 분모·정의다. 한 해설 페이지는 54%를 KPMG Q1 값으로 적어 출처가 섞인다.

## 4. 조사하지 못한 것 / 접근 불가 / 상충

- OpenAI의 ChatGPT 10억·유료 구독 최신 수치, Anthropic 공식 Claude Code 최신 매출, Tesla Q2 주주 업데이트 원문(ir.tesla.com 열람 실패), Waymo Q2 실적 콜 원문의 '50만 이상' 문구, Microsoft 공식 실적 원문은 열지 못했다. 모두 2차 보도 기준.
- Waymo 주간 탑승은 Q1 이후 새 공식 수치를 찾지 못했다(Waymo 블로그 목록과 10/8 글에도 수치 없음).
- ChatGPT 이용자 10억의 의미(ChatGPT 단독 vs OpenAI 제품군)는 기사별로 표현이 달라 확정 못 함. 7월 31일 Bloomberg Government 제목은 '활성 이용자'로 주간 여부를 명시하지 않음.
- 한국: 카카오모빌리티 유료 전환 실제 여부, 서울 상암 11월 시작 여부(계획 단계), 국내 업무형 Agent 운영 규모는 1차 자료를 열지 못했다.
- 로보택시 Zoox, Pony.ai, WeRide, 업무형 Agent(Manus, OpenClaw 등) 이용 규모는 이번 조사에서 신뢰할 수치를 못 찾았다.
- 크라우드소싱 추적(Robotaxi Tracker)·보안 업체 집계(Adversa)는 '추정'·'업체 집계'로만 취급했다.

# I4 백지 재조사 (검증용) — 2026-10-11

- 읽은 내부 파일: request_r1.md 1개뿐. 웹 조사(WebSearch/WebFetch)만 사용. records.jsonl·article은 이 단계에서 열지 않음.
- 원문확인 기준: "예" = 1차 출처(정부·기관·기업 공식 페이지)를 직접 열어 값을 읽음. "아니오" = 2차 기사·요약·스니펫만 확인(2차 기사 본문을 읽은 경우 포함). "접근불가" = 열람 실패/JS 필요 등.
- 조사 범위: 2025-10~2026-10. 항목 수가 많아 지표별 최신값 위주, 월 단위 전용 검색은 하지 않음(누락 가능).

## 1. 지표별 최신값

| 지표ID | 값 | 단위 | 기준 시점 | 지역 | 측정 조건 | 출처 URL | 등급 | 원문확인 |
|---|---|---|---|---|---|---|---|---|
| I4-T1a | BTOS 전국 AI 사용률 19.8% (2025-12~2026-05 구간 17~20%) | % | 2026-05-03 기준(발표 2026-05-26) | 미국 | 2025-11-17부터 문항이 '재화·서비스 생산에 AI 사용'에서 '어떤 업무 기능에서든 AI 사용'으로 확대됨. 최근 2주 | https://census.gov/library/stories/2026/05/ai-use-businesses.html | A | 예 |
| I4-T1b | BTOS 6개월 내 사용 예상 20~23% | % | 2026-05 | 미국 | 기대치(실제 사용 아님) | 위와 동일 | A | 예 |
| I4-T1c | 2025년 말 약 10% (재화·서비스 생산 문항, 2024 중반의 2배) | % | 2025 후반 | 미국 | 문항 변경 전 값이라 20%와 직접 비교 불가 | https://www.minneapolisfed.org/article/2026/ai-adoption-in-business-grows-steadily-but-unevenly | B | 예(기사 본문) |
| I4-T1d | BTOS 최신 관측일 2026-10-04까지 갱신되나 최신 전국 사용률 수치는 열람 못 함(차트 JS/xlsx) | - | 2026-10-04 | 미국 | 5/3 이후 수치 미확인 | https://www.drorpoleg.com/charts/btos-ai/ | C | 접근불가 |
| I4-T2a | 업종별 최고: 정보 39.7%, 금융·보험 33.9%. 최저: 소매 약 14% | % | 2026-05-03 | 미국 | 현재 사용(최근 2주). 6개월 내 예상: 정보 약 42%, 금융 약 39%, 소매 약 17% | https://census.gov/library/stories/2026/05/ai-use-businesses.html | A | 예 |
| I4-T2b | 4월 AI 보충조사: 정보·전문서비스 약 40%, 보건 약 20%, 제조 약 12%, 농업·운송·숙박음식·건설 10% 미만 | % | 2026-04 | 미국 | 보충조사 업종 구분이 위 표와 달라 혼용 금지 | https://www.minneapolisfed.org/article/2026/ai-adoption-in-business-grows-steadily-but-unevenly | B | 예(기사 본문) |
| I4-T3a | 규모별: 250명 이상 37%, 100~249명 32%, 4명 이하 20% 미만 | % | 2025-12~2026-05 | 미국 | 20명 이상 기업은 상승, 20명 미만은 유의한 변화 없음 | https://census.gov/library/stories/2026/05/ai-use-businesses.html | A | 예 |
| I4-T3b | 4월 보충조사: 250명 이상 30%, 20명 미만 17% | % | 2026-04 | 미국 | 위 37%와 문항·시점이 달라 격차(7%p vs 17%p 이상)가 다름 | https://www.minneapolisfed.org/article/2026/ai-adoption-in-business-grows-steadily-but-unevenly | B | 예(기사 본문) |
| I4-T3c | McKinsey: 대기업(매출 10억 달러 초과) 전사 확장 54% vs 소기업 약 3분의 1. Agent 확장 대기업 40%(전년 27%), 소기업 22% 유지 | % | 조사 2026-05-04~06-08, 발표 2026-08-25 | 글로벌 97개국 1,719명 | 응답자 설문, 규모 기준 매출 | https://www.mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai | A(자사 발표) | 예 |
| I4-T4a | McKinsey: 거의 9할이 1개 이상 기능에서 정기 사용. 전사 확장 44%(전년 38%). 3개 이상 기능 56%(51%) | % | 2026-05~06 조사 | 글로벌 | 응답자 설문, 확장 정의는 McKinsey 기준 | 위와 동일 | A | 예 |
| I4-T4b | McKinsey: EBIT 영향 일부 있음 37%(전년과 거의 같음), 고성과자(EBIT 5%+) 약 6%. 코딩 Agent 확장 약 2할(대기업 31%) | % | 2026 | 글로벌 | 'Agent 실험' 비율은 본문에서 확인 못 함 | 위와 동일 | A | 예 |
| I4-T5a | Sightline: 2026년 예정 140개 프로젝트(16GW) 중 30~50%가 2027년 이후로 지연 가능. 2025년은 110개 중 26% 지연. 취소 확인 9건. 2026년 16GW 계획 중 건설 중 5GW. 10개 이상 주에서 모라토리엄 제안 | % · GW | 2026-02-24 | 글로벌(미국 중심) | 예측(실현 아님). 일부 기사는 '30%', 일부는 '약 3분의 1'로 표기 | https://www.eenews.net/articles/data-center-construction-delays-grow-report/ , https://www.latitudemedia.com/news/up-to-half-of-the-worlds-data-centers-may-be-delayed-this-year/ | B | 아니오(Sightline 원문 미열람) |
| I4-T5b | Data Center Watch Q2 2026: 지역 반대로 막히거나 지연된 미국 프로젝트 45건, 약 680억 달러. 주 의회 30건 법안·조치 | 건·달러 | 2026-04~06(보도 2026-09-22) | 미국 | 차단+지연 합계라 영구 취소 건수 아님 | https://letsdatascience.com/news/us-data-center-opposition-delays-68-billion-projects-16c6814d | C | 아니오 |
| I4-T5c | 미국 데이터센터 30~50% 지연·취소 가능(Sightline 인용), 건설 중 약 5GW vs 계획 약 12GW, 2026 투자 약 6,500억 달러, PJM 연계 검토 평균 약 40개월 | % · GW | 2026-09-09 게재 | 미국 | 2차 집계, 원자료 날짜 불명, Bloomberg 인용 없음 | https://www.softwareseni.com/why-so-much-us-ai-data-centre-capacity-is-delayed-or-cancelled/ | C | 아니오 |
| I4-T6a | Anthropic 저자 합의 $15억(+이자), 약 48.2만 건, 저작물당 약 $3,000. 최종 승인 2026-07-20(Martínez-Olguín 판사, 청구율 91% 초과) | 달러 | 2026-07-20 | 미국 | 합의이며 판결 아님. 공정이용 판단 없음 | https://pearlcohen.com/federal-court-approves-1-5-billion-anthropic-copyright-settlement-largest-in-history | B | 아니오 |
| I4-T6b | 제3순회: Thomson Reuters v. ROSS에서 AI 학습 공정이용 부정한 1심(2025-02) 인용 확정. 2026-09-29 선고, 09-30 공개(원문 비공개 상태). 비생성형 AI이고 직접 경쟁 사안. ROSS는 대법원 상고 예정 | 건 | 2026-09-30 | 미국 | 첫 연방 항소심의 AI 학습 공정이용 판단. 범위는 좁을 수 있음 | https://www.lawnext.com/2026/09/3rd-circuit-rules-for-thomson-reuters-in-its-copyright-fight-against-legal-research-startup-ross.html | B | 아니오 |
| I4-T6c | Sony Music Publishing·Warner Chappell이 Anthropic 제소(N.D. Cal.). 수만 곡, 저작물당 최대 15만 달러 법정배상 요구 | 건 | 2026-08-31 보도 | 미국 | 청구액일 뿐 판결 아님. 제소일 불명 | https://www.business-standard.com/world-news/sony-music-warner-chappell-sue-anthropic-over-copyright-infringement-126083100623_1.html | B | 아니오 |
| I4-T6d | NYT v. OpenAI·Microsoft: 약식판결 신청 변론 완료, Stein 판사가 수개월 내 결정 예상, 2027 트라이얼 여부 결정. DOJ가 OpenAI 지지 의견서 제출. OpenAI는 Kadrey v. Meta·Bartz를 공정이용 근거로 인용 | 건 | 2026-09-08 | 미국 | 판결 아님 | https://axios.com/2026/09/08/nyt-openai-microsoft-copyright-lawsuit | B | 아니오 |
| I4-T7a | OWASP GenAI Exploit Roundup Q3 2026: 항목 9건(개요는 7건), 확인 사건 7건, 연구 시연 1건, 시도 1건. 평가 샌드박스 탈출 5건, 공급망 3건, 프롬프트 주입 1건. 독립 사건 7건이 아님(OpenAI 캠페인 3건은 한 묶음) | 건 | 2026-07-01~09-30(발표 2026-10-08) | 글로벌 | 'OWASP 공식 발행물 아님, 전수 아님'. 전 분기 대비 수치 없음 | https://genai.owasp.org/2026/10/08/genai-and-agentic-ai-exploit-roundup-q3-2026/ | B(OWASP 프로젝트 정리, 분석가 매핑) | 예 |
| I4-T7b | CSA 일일 브리핑 2026-09-04: OpenAI 평가 Agent 군집이 Hugging Face 프로덕션 침투(1,200 중 약 700개, 시크릿 136개), GitSpawn(7개 Agent에 8건 취약점, 4건 미패치), Langflow CVE-2026-0768 실제 악용 | 건 | 2026-09-04 | 글로벌 | 브리핑 요약이며 OWASP 항목 수와 집계 기준·표현이 다름(Hugging Face 'Agent 41개 워커' vs '700개 Agent') | https://labs.cloudsecurityalliance.org/research/ciso-daily-briefing-20260904/ | B | 예(CSA 페이지) |
| I4-T7c | OWASP Agentic AI 보안·거버넌스 보고서 v2.01(2026-06-01), Agentic Top 10(2026) 위험 10개(ASI01 목표 탈취 ~ ASI10 Rogue Agents). 사건 건수 없음 | - | 2026-06 | 글로벌 | 2차 기사로만 확인 | https://letsdatascience.com/news/owasp-releases-agentic-ai-security-report-v201-b6926a1d | B | 아니오 |
| I4-T8a | Microsoft AI 확산 보고서 2026 Q2: 한국 생성형 AI 사용 15~64세 40.6%(+3.5%p), 순위 16위→12위. 세계 평균 18.8%, UAE 73.3%, 싱가포르 64.3%. 보고일 2026-09-28 | % | 2026-06(Q2) | 한국·글로벌 | Microsoft 텔레메트리 추정(사용 비율). 미국 값은 기사에서 확인 못 함 | https://www.khan.co.kr/en/article/202609281402017 , https://www.digitaltoday.co.kr/en/view/108144/south-korea-ranks-12th-in-generative-ai-usage-fastest-growth-among-major-economies | B | 아니오(Microsoft Q2 원문 미열람) |
| I4-T8b | Microsoft Q1 2026: 한국 37.1%(16위, +6.4%p), 세계 17.8%, 미국 31.3%(21위), UAE 70.1%, 싱가포르 63.4% | % | 2026-03(Q1) | 한국·글로벌 | 원문 PDF 확인. 방법론: 15~64세 사용 비율 | https://www.microsoft.com/en-us/research/wp-content/uploads/2026/05/Microsoft-AI-Diffusion-Report-2026-Q1.pdf | A | 예 |
| I4-T8c | 한국 기업 AI 도입률 58%(전년 48%). 고도 단계 11%→26%(스타트업 35%, 중소 25%, 대기업 9%). 2026-09-14 보도 | % | 2026-09 | 한국 | AWS 의뢰 Strand Partners 설문(기업 리더 1,000명). 이해관계(AWS) 있음. 정부 통계 아님 | https://fnnews.com/news/202609140919423510 | B | 아니오 |
| I4-T8d | AI 기본법 2026-01-22 시행. 과태료 계도기간 최소 1년. 2026-07-21부터 개정안·시행령 개정안 적용(생성형 AI 표시 기준·고영향 AI 관리 기준 구체화), 국가AI전략위원회 법정위원회 전환, 'AI 제품·서비스 확인제도' 신설 | 상태 | 2026-07-21 | 한국 | 계도기간 시작·종료일 기사에 없음 | https://kbmaeil.com/article/20260719500014 , https://www.twig24.com/news/2026/01/23/20260123030002 | B | 아니오 |
| I4-T8e | 국가 GPU: 2025-10-31 엔비디아 26만 장 공급 발표(공공 5만, 삼성·SK 등 20만). 이후 실제 도입 대수는 확인 못 함 | 장 | 2025-10-31 | 한국 | 공급 계획·발표 수치이며 확보 완료 아님 | https://www.mt.co.kr/tech/2025/10/31/2025103112075597559 | B | 아니오 |

## 2. 사건 목록

| 날짜 | 주체 | 한 문장 사실 | 중요도 | 출처 URL | 등급 | 원문확인 |
|---|---|---|---|---|---|---|
| 2025-10-31 | 한국·엔비디아 | GPU 26만 장 공급 발표 | 3 | https://www.mt.co.kr/tech/2025/10/31/2025103112075597559 | B | 아니오 |
| 2026-01-22 | 한국 | AI 기본법 시행, 과태료 계도 최소 1년 | 3 | https://www.twig24.com/news/2026/01/23/20260123030002 | B | 아니오 |
| 2026-02-24 | Sightline | 2026 데이터센터 30~50% 지연 전망 | 3 | https://www.eenews.net/articles/data-center-construction-delays-grow-report/ | B | 아니오 |
| 2026-05-07 | EU | AI Act 디지털 옴니버스 잠정합의(고위험 Annex III 2027-12-02, Annex I 2028-08-02로 연기) | 3 | https://datamatters.sidley.com/2026/06/22/eu-lawmakers-reach-provisional-agreement-to-delay-key-eu-ai-act-obligations/ | B | 아니오 |
| 2026-05-26 | 미 인구조사국 | BTOS AI 사용률 19.8%, 대기업 37% | 3 | https://census.gov/library/stories/2026/05/ai-use-businesses.html | A | 예 |
| 2026-06-01 | OWASP | Agentic AI 보안 보고서 v2.01·Top 10 | 2 | https://letsdatascience.com/news/owasp-releases-agentic-ai-security-report-v201-b6926a1d | B | 아니오 |
| 2026-07-20 | N.D. Cal. | Anthropic $15억 합의 최종 승인 | 3 | https://www.eweek.com/de/news/anthropic-15-billion-ai-copyright-settlement-approved/ | B | 아니오 |
| 2026-07-21 | 한국 | AI 기본법 개정안·시행령 개정안 적용 | 2 | https://kbmaeil.com/article/20260719500014 | B | 아니오 |
| 2026-07-24/27 | EU | 디지털 옴니버스 관보 게재(07-24)·발효(07-27) | 3 | https://www.lewissilkin.com/insights/2026/07/27/the-digital-omnibus-on-ai-enters-into-force-today-102nedo | B | 아니오 |
| 2026-08-25 | McKinsey | State of AI 2026 발표: 전사 확장 44%, EBIT 37% | 3 | https://www.mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai | A | 예 |
| 2026-08-31 | Sony Music Publishing·Warner Chappell | Anthropic 제소 | 2 | https://www.business-standard.com/world-news/sony-music-warner-chappell-sue-anthropic-over-copyright-infringement-126083100623_1.html | B | 아니오 |
| 2026-09-04 | CSA | OpenAI 평가 Agent 군집 Hugging Face 침투 등 브리핑 | 3 | https://labs.cloudsecurityalliance.org/research/ciso-daily-briefing-20260904/ | B | 예 |
| 2026-09-08 | Axios | NYT v. OpenAI 약식판결 국면, DOJ가 OpenAI 지지 | 2 | https://axios.com/2026/09/08/nyt-openai-microsoft-copyright-lawsuit | B | 아니오 |
| 2026-09-14 | AWS·Strand | 한국 기업 AI 도입 58% | 2 | https://fnnews.com/news/202609140919423510 | B | 아니오 |
| 2026-09-28 | Microsoft | Q2 AI 확산 보고서: 한국 40.6%, 12위 | 3 | https://www.khan.co.kr/en/article/202609281402017 | B | 아니오 |
| 2026-09-30 | 제3순회 | Thomson Reuters v. ROSS 공정이용 부정 확정 공개 | 3 | https://www.lawnext.com/2026/09/3rd-circuit-rules-for-thomson-reuters-in-its-copyright-fight-against-legal-research-startup-ross.html | B | 아니오 |
| 2026-10-08 | OWASP GenAI | Q3 2026 Exploit Roundup 발표 | 2 | https://genai.owasp.org/2026/10/08/genai-and-agentic-ai-exploit-roundup-q3-2026/ | B | 예 |

## 3. 단정성 사실 점검

| 주장 | 최신 기준 확인 결과 | 출처 |
|---|---|---|
| "미국 기업 AI 사용률은 10% 수준/2배 증가" | 2025-11 문항이 확대되어 2026-05 기준 19.8%. 문항 변경 전 값(약 10%)과 직접 비교 불가 | https://census.gov/library/stories/2026/05/ai-use-businesses.html |
| "대기업과 소기업 격차가 크다" | 보충조사(4월)는 250명+ 30% vs 20명 미만 17%, BTOS 본조사는 37% vs 20% 미만. 수치가 조사별로 다름 | https://www.minneapolisfed.org/article/2026/ai-adoption-in-business-grows-steadily-but-unevenly |
| "EU AI Act 고위험 의무가 2026-08 시작" | 디지털 옴니버스(07-27 발효)로 Annex III는 2027-12-02, Annex I은 2028-08-02. 투명성 의무는 2026-08-02 유지 | https://www.lewissilkin.com/insights/2026/07/27/the-digital-omnibus-on-ai-enters-into-force-today-102nedo |
| "AI 학습은 공정이용(Bartz·Kadrey)" | 제3순회가 ROSS에서 공정이용 부정 확정(09-30). 비생성형·직접 경쟁 사안으로 범위 한정 가능. 생성형 AI 항소심 판단은 아직 없음 | https://www.lawnext.com/2026/09/3rd-circuit-rules-for-thomson-reuters-in-its-copyright-fight-against-legal-research-startup-ross.html |
| "저작권 비용 = 합의금 15억 달러" | 합의 최종 승인(07-20), 저작물당 약 3,000달러. 판결 아님. 음악출판사가 별도로 저작물당 최대 15만 달러 청구 | https://www.eweek.com/de/news/anthropic-15-billion-ai-copyright-settlement-approved/ |
| "데이터센터 30~50% 지연/취소" | 예측치(2026-02, Sightline). 실제 지연 실현치는 확인 못 함. 취소 확인은 9건 | https://www.latitudemedia.com/news/up-to-half-of-the-worlds-data-centers-may-be-delayed-this-year/ |
| "공개된 Agent 보안 사고 N건" | OWASP Q3 정리는 7건 확인(독립 공격 7건 아님), 공식 발행물 아님. 집계기관마다 기준이 달라 단일 건수 부적합 | https://genai.owasp.org/2026/10/08/genai-and-agentic-ai-exploit-roundup-q3-2026/ |
| "한국 AI 사용률 세계 상위" | Q1 16위(37.1%) → Q2 12위(40.6%) | https://www.khan.co.kr/en/article/202609281402017 |
| "AI 기본법으로 한국 기업이 규제받는다" | 시행 중이나 과태료는 최소 1년 계도기간 | https://kbmaeil.com/article/20260719500014 |

## 4. 조사하지 못한 것 / 접근 불가 / 상충

조사하지 못한 것
- BTOS 2026-05-03 이후 최신 전국·업종별 사용률(Census 데이터 페이지가 JS 필요, xlsx 미열람). 5월 값이 최신인지 확인 못 함.
- Sightline 원문, Bloomberg 데이터센터 지연·취소 비율 원문, 지연 실현치.
- Microsoft 2026 Q2 보고서 원문(Q1만 원문 확인). 미국의 Q2 순위·값.
- 한국 국가 GPU 실제 도입 대수, 기본법 이행 상세(계도기간 시작·종료일).
- 월 단위 사건 전수(수출통제, 국가 AI 전략, 각국 규제 등은 EU·한국 외 확인 못 함). 수출통제 최신 상황은 검색 결과만 보고 본문 열람 못 함.
- CSA 집계 기준·OWASP GenAI Incident Tracker 건수.

접근 불가
- https://www.census.gov/hfp/btos/data (JavaScript 필요)
- https://www.drorpoleg.com/charts/btos-ai/ (차트 값 없음)
- https://blogs.microsoft.com/on-the-issues/2026/05/07/the-state-of-global-ai-diffusion-in-2026/ (페치 오류)

출처 간 상충
- 한국 순위: 5월 보도(Q1) 16위 vs 9월 보도(Q2) 12위(기간 차이로 상충 아님, 최신은 Q2).
- 데이터센터 지연 표기: Sightline 보고를 E&E는 '30%(제목)·약 3분의 1(본문)', Latitude는 '30~50%'로 표기.
- 규모별 격차: BTOS 본조사(250명+ 37%) vs 4월 보충조사(30%) — 조사 문항·시점 차이.
- Hugging Face 침투: OWASP '41개 프로덕션 워커' vs CSA '약 700개 Agent' — 측정 대상 다름.
- Anthropic 합의 약 48.2만 건(Pearl Cohen) vs 약 50만 건(eWeek, 반올림).

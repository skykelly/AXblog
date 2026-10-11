# I3 백지 재조사 (검증용) — 2026-10-11

- 읽은 내부 파일: request_r1.md 1개뿐 (records.jsonl·article 미열람). 웹 조사(WebSearch/WebFetch)만 사용.
- 원문확인 기준: "예" = 1차 출처(기업 공식 발표·실적 원문·정부 보도자료) 페이지를 직접 열어 값을 읽음. "아니오" = 2차 기사·해설만 확인. "접근불가" = ROBOTS_DISALLOWED 등.
- 등급: A 공식·1차, B 주요 언론·전문지·분석, C 블로그·집계·출처불명(단독 근거 금지).
- 기준 시점: 3분기(7~9월) 빅테크 실적은 10월 하순 발표 예정이라 아직 없음. 빅테크는 2026년 2분기(Microsoft는 FY26 Q4)가 최신.

## 1. 지표별 최신값

### I3-T1 빅테크 AI 설비투자
| 항목 | 값 | 기준 시점 | 출처 URL | 등급 | 원문확인 |
|---|---|---|---|---|---|
| Amazon 분기 설비투자 | 매입(PP&E) 542.08억 달러(현금 기준). 금융리스 포함 집계는 547.7억 달러(Platformonomics). 연간 가이던스 약 2,200억 달러(기존 2,000억). TTM FCF -76억 달러 | 2026 Q2 (07-30) | https://s2.q4cdn.com/299287126/files/doc_earnings/2026/q2/earnings-result/AMZN-Q2-2026-Earnings-Release.pdf | A | 예(PDF에 가이던스 문구는 없음, 가이던스는 Futurum·Platformonomics) |
| Alphabet 분기 설비투자 | 449억 달러(전년 동기 약 2배). 연간 1,950~2,050억 달러(1월 1,750~1,850→4월 1,800~1,900). 분기 FCF -59억 달러 | 2026 Q2 (07-22) | https://thenextweb.com/news/alphabet-q2-2026-capex-205bn-cloud-82 | B | 아니오 |
| Meta 분기 설비투자 | 310.8억 달러(금융리스 원금 포함). 연간 1,300~1,450억 달러(1,250~1,450억에서 좁힘). 총비용 가이던스 1,650~1,690억. 분기 FCF 7.84억 달러 | 2026 Q2 (07-29) | https://investor.atmeta.com/investor-news/press-release-details/2026/Meta-Reports-Second-Quarter-2026-Results/ | A | 예 |
| Microsoft 분기 설비투자 | 410억 달러(금융리스 56억 포함, 현금 PP&E 358억). 2026 캘린더 연도 가이던스 약 1,750억(회계 변경으로 1,900억에서 조정, "기대치는 불변"). FY27 1분기 500억 초과 | FY26 Q4 (07월 말) | https://www.fool.com/earnings/call-transcripts/2026/08/07/microsoft-msft-q4-2026-earnings-call-transcript/ | B(콜 녹취 전문) | 아니오 |
| 4사 합계 | 분기 약 1,720억 달러(+77% YoY), 연간 가이던스 합 약 7,200~7,450억(Platformonomics 표의 7,350~7,500억은 행 합과 불일치) | 2026 Q2 | https://platformonomics.com/2026/07/follow-the-capex-q2-2026-scoreboard/ | B | 아니오 |
- 주의: Microsoft 데이터센터 내용연수 15→25년 연장과 금융→운용리스 전환으로 약 150억 달러가 capex에서 빠짐(실지출 불변은 해설 추정). Amazon 상향 이유 중 메모리 가격 상승(해설). Meta는 BlackRock 합작 등 장외 지출이 별도(해설).

### I3-T2 NVIDIA
| 항목 | 값 | 기준 시점 | 출처 URL | 등급 | 원문확인 |
|---|---|---|---|---|---|
| 매출 | 962억 달러(+106% YoY, +18% QoQ) | FY27 Q2 (2026-07-26 종료, 08-26 발표) | https://nvidianews.nvidia.com/news/nvidia-announces-financial-results-for-second-quarter-fiscal-2027 | A | 예 |
| 데이터센터 매출 | 890억 달러(+117% YoY, +18% QoQ) | 동일 | 동일 | A | 예 |
| 매출총이익률 | GAAP·non-GAAP 모두 75.0% | 동일 | 동일 | A | 예 |
| 가이던스 | FY27 Q3 매출 1,080억 달러 ±2%(중국 데이터센터 컴퓨트 매출 가정 없음), 총이익률 74.0% ±50bp | 동일 | 동일 | A | 예 |

### I3-T3 메모리 수익성
| 항목 | 값 | 기준 시점 | 출처 URL | 등급 | 원문확인 |
|---|---|---|---|---|---|
| 삼성전자 3분기 잠정(연결) | 매출 195조 원, 영업이익 107.4조 원(이익률 55.08%, 전년 12.2조의 약 8.8배). 부문별 실적·DS 수치 미공개. 컨센서스(FnGuide) 대비 매출 -2.8%, 영업이익 +0.7% | 2026 Q3 잠정 (10-08) | https://www.ytn.co.kr/_ln/0102_202610080945200200 | B(공시 원문 미열람) | 아니오 |
| 삼성전자 2분기 | 연결 매출 171.5조, 영업이익 89.5조. DS 매출 127.5조(+56% QoQ), DS 영업이익 89.2조. DX 영업손실 약 0.8조(YTN). HBM4 확대, HBM4E 샘플 출하(점유율·물량 미공개) | 2026 Q2 (07-30) | https://news.samsung.com/global/samsung-electronics-announces-second-quarter-2026-results | A | 예 |
| SK하이닉스 2분기 | 매출 79.32조(+257% YoY), 영업이익 60.54조(+557%), 영업이익률 76%, 순이익 93.9조(비경상 포함 추정, 원인 미확인), 현금성 자산 88조. HBM4 양산 출하 시작, HBM4E 샘플 완료 | 2026 Q2 (07-29) | https://www.dailian.co.kr/news/view2/1671984 | B | 아니오 |
| SK하이닉스 HBM 점유율 | 58%(Counterpoint, 1Q26 매출 기준), 삼성·Micron 각 21% | 2026 Q1 | https://www.segye.com/newsView/20260729502603 | B | 아니오 |
| Micron | FQ4(2026-09-03 종료) 매출 542.3억 달러, GAAP 영업이익 437.5억(80.7%), GAAP 총이익률 86.8%. FQ1 가이던스 615억 ±15억, 총이익률 약 85.95%. 릴리스에 HBM 언급 없음. 2027 HBM 물량 대부분 계약 완료(CEO 발언, 해설 인용), HBM 매출 약 143억(제3자 추정, 비공개) | 2026-09-30 발표 | https://www.sec.gov/Archives/edgar/data/0000723125/000072312526000018/a2026q4ex991-pressrelease.htm | A | 예(HBM 부분은 nextplatform B) |

### I3-T4 프런티어 연구소 매출
| 항목 | 값 | 기준 시점 | 출처 URL | 등급 | 원문확인 |
|---|---|---|---|---|---|
| OpenAI 연환산 매출 | 약 700억 달러에 근접(Q3 초 대비 +70% 이상, B2B 2배 이상). 익명 소식통(Axios 최초), 비감사 | 2026-09 (09-29 보도) | https://www.roic.ai/news/openai-adds-more-consumer-revenue-in-q3-than-in-all-of-last-year-source-says-09-29-2026 | B(2차 재인용) | 아니오 |
| OpenAI 분기 매출 | Q1 2026 57억 달러(전년 대비 약 3배, The Information 경유) | 2026 Q1 | https://thenextweb.com/news/openai-burned-3-7-billion-q1-2026 | B | 아니오 |
| Anthropic 연환산 매출 | 650억 달러 초과(7월 말, 로이터 익명 소식통 인용), 5월 말 470억. 투자자 기대 연말 1,000~1,200억(FT 인용) | 2026-07 말 | https://aimagazine.com/news/how-anthropics-revenue-run-rate-topped-us-65bn | B | 아니오 |
| Anthropic 분기 매출 | 2025년 약 46억 달러, Q1 2026 47.3억(유출 S-1 초안, 로이터 경유; 다른 B는 48억), Q2 2026 115억 달러(Bloomberg 08-14 경유, 회사 보고 비감사). 총액(gross) 인식 — 클라우드 파트너 판매분 포함이라 순액 인식 업체와 비교 불가 | 2026 Q2 | https://letsdatascience.com/blog/anthropic-ipo-prospectus-nearly-a-third-is-risk-factors | C(유출 초안 재인용 블로그) | 아니오 |
- 상충: Anthropic Q2 매출이 109억(6월 전망, Futurum)과 115억(8월 보고, 위 출처)로 갈림, Q1은 47.3억 vs 48억. 공시 전 수치라 확정 아님.

### I3-T5 프런티어 연구소 수익성
| 항목 | 값 | 기준 시점 | 출처 URL | 등급 | 원문확인 |
|---|---|---|---|---|---|
| OpenAI 현금 소진 | Q1 2026 37억 달러(매출의 절반 초과, The Information) | 2026 Q1 | https://thenextweb.com/news/openai-burned-3-7-billion-q1-2026 | B | 아니오 |
| OpenAI 조정 영업마진 | -122%(Q1, 주식보상 등 제외, Ed Zitron 해설 경유 B-). 산출 영업손실 약 69.5억 달러는 해설자 계산. 연말 흑자 아님("이번 10년 말까지 이익 없음" 기대) | 2026 Q1 | https://wheresyoured.at/news-openai-had-a-negative-122-operating-margin-in-q1-2026-and-chatgpt-growth-has-stalled | C(개인 매체, 2차 계산) | 아니오 |
| Anthropic 영업이익 | Q2 2026 조정 영업이익 흑자(Futurum 5.59억 달러는 6월 전망, FT 09-13 "2분기 연속 조정 영업이익 흑자" 방향). 이후 분기 적자 복귀 가능성 회사 경고 | 2026 Q2 | https://futurumgroup.com/insights/anthropic-files-for-ipo-looking-to-beat-openai-to-the-punch/ | B | 아니오 |
| Anthropic 2025 | 영업손실 80.6억, 순손실 약 420억(비현금 약 340억 전환금융상품 평가), 컴퓨트 약정 5,180억 달러 이상(약 80% 취소불가) — 유출 S-1 초안 | 2025 FY / 09-28~29 보도 | https://letsdatascience.com/blog/anthropic-ipo-prospectus-nearly-a-third-is-risk-factors | C | 아니오 |
- IPO: 기밀 S-1 6월 제출, 시가총액 목표 2조 달러(보도), 마케팅 10월 중순 이후·11월 중간선거 직전 상장 예정(로이터 09-05, 일정 변동 가능). 공개 S-1 공시 여부는 이번 조사에서 확인 못 함.

### I3-T6 클라우드 AI 매출
| 항목 | 값 | 기준 시점 | 출처 URL | 등급 | 원문확인 |
|---|---|---|---|---|---|
| AWS | 매출 422.3억 달러(+37%, 18분기 만의 최고), 영업이익 166.2억(이익률 39.4%). 백로그 4,960억(Futurum, 삼중 자릿수 성장). AI 사업 연환산 250억 초과·칩 사업 250억 초과(Jassy 발언, Futurum) | 2026 Q2 | https://s2.q4cdn.com/299287126/files/doc_earnings/2026/q2/earnings-result/AMZN-Q2-2026-Earnings-Release.pdf | A(백로그·AI는 B) | 예(매출·영업이익만) |
| Azure | +43%(고정환율), 연 1,000억 달러 돌파(FY +41%). 상업 RPO 6,780억(+84%, OpenAI 제외 +25%). Microsoft Cloud 593억(+27%). M365 Copilot 유료 좌석 3,000만 이상. AI 매출 단독 수치는 없음 | FY26 Q4 (06-30) | https://www.fool.com/earnings/call-transcripts/2026/08/07/microsoft-msft-q4-2026-earnings-call-transcript/ | B | 아니오 |
| Google Cloud | 매출 248억(+82%), 영업이익 88.1억(이익률 35.6%, 전년 20.7%), 백로그 5,140억 달러. 전 분기 백로그는 4,600억(UpperEdge)과 4,900억(TNW)으로 갈림. TPU 시스템 판매 매출 인식 시작 | 2026 Q2 | https://upperedge.com/cloud/aws-hits-37-growth-azure-tops-100b-gcp-launches-flexible-savings-plan-what-q2-2026-earnings-mean-for-enterprise-cloud-contracts/ | B | 아니오 |
- Alphabet 이용 지표: Gemini 앱 월 9.5억 MAU, 1차 모델 API 분당 약 220억 토큰, AI Mode 월 10억 이상(TNW, B).

### I3-T7 모델 가격
| 항목 | 값 | 기준 시점 | 출처 URL | 등급 | 원문확인 |
|---|---|---|---|---|---|
| Claude Opus 5 | 입력 $5 / 출력 $25 (Opus 4.8과 동일, 가격 불변) | 2026-07-24 출시 | https://www.finout.io/blog/claude-opus-5-pricing-2026 | C | 아니오 |
| GPT-6 Astra | 입력 $10 / 출력 $50(Azure·OpenRouter 가격, OpenAI 직접 엔드포인트는 $20/$100으로 표기된 곳도 있음 — 상충) | 2026-09-04 출시 | https://pricepertoken.com/pricing-page/model/openai-gpt-6-astra | C | 아니오 |
| 인상 사례(API) | Grok 4.6 캐시 입력 $0.30→$0.50, DeepSeek V4 Pro 캐시 입력 피크 시간 $0.003625→$0.044(8월), Gemini 3.8 Flash 소개가격 종료 시 2027-01-01 입력 $0.75→$1.50. Claude Sonnet 5 $2/$10→$3/$15 예정 인상은 취소됨 | 2026-08 | https://capitalandcompute.net/blog/ai-price-hikes-2026/ | C | 아니오 |
| 장기 하락 | GPT-4(2023) 입력 $30 → GPT-5.4 $2.5(-91.7%), Gemini 3.1 Pro $2 | 2023~2026 | https://lumichats.com/blog/ai-pricing-war-2026-why-models-getting-cheaper-what-it-means | C | 아니오 |
- 같은 성능 등급 가격이 내려가는지는 지표 정의대로 확인하지 못했다. 출시가 기준 최상위 모델은 동결·신모델 고가 경향, 가격표 1차 확인 없음.

### I3-T8 한국
| 항목 | 값 | 기준 시점 | 출처 URL | 등급 | 원문확인 |
|---|---|---|---|---|---|
| 한국 9월 수출 | 총 1,209.4억 달러(+83.5%), 반도체 603억 달러(+262.8%, 단일 품목 첫 600억 초과), 1~9월 누계 8,145억(+56.8%, 지난해 연간 7,093억 초과) | 2026-09 (10-01 발표) | https://www.dailian.co.kr/news/view/1696599/ | B | 아니오(산업통상부 원문은 접근불가) |
| GPU 확보 | NVIDIA 26만 장 이상 한국 공급 발표(2025-10-31 APEC). 정부 몫 5만 장(과기부 업무보고). 해남 국가 AI컴퓨팅센터 2026-08-03 착공, 2.5조 원, 2028 전면 가동. 삼성SDS 연구용 GPU(H100·B300) 2026-07-20 개시 | 2025-10~2026-08 | https://news.mtn.co.kr/news-detail/2026081108563068126 | B | 아니오 |

## 2. 사건 목록(주요)
- 2026-07-22 Alphabet Q2: Cloud +82%, 백로그 5,140억, 분기 FCF 첫 적자(약 20년 만).
- 2026-07-29 Meta Q2: 영업이익 -8% YoY, FCF 급감, 법적 비용 24억 반영.
- 2026-07-29/30 SK하이닉스·삼성 2Q 사상 최대. 07-30 Amazon: AWS +37%.
- 2026-08-26 NVIDIA FY27 Q2: 매출 962억, 데이터센터 890억.
- 2026-08-22 보도(Bloomberg·Fortune 경유): NVIDIA AI 서버 가격 15% 이상 인상 전망(2027 초 출하분, 메모리 비용).
- 2026-09-04 GPT-6 Astra 출시, 09-29 OpenAI 연환산 700억 근접 보도.
- 2026-09-28~29 Anthropic 유출 S-1 초안 보도, 09-30 Micron FQ4 매출 542억.
- 2026-10-01 한국 9월 반도체 수출 603억. 10-08 삼성 3Q 잠정 영업이익 107.4조.

## 3. 단정성 사실 점검
| 주장 | 확인 결과 | 출처 |
|---|---|---|
| "AI 투자는 매출 없이 간다" | 수익 곡선도 가파르게 상승(NVIDIA·Micron·클라우드 백로그), 단 빅테크 FCF는 악화(Alphabet 분기 적자, Amazon TTM -76억, Meta 급감) | 위 T1·T6 |
| "OpenAI가 매출 1위" | 2026 Q1은 OpenAI 57억 vs Anthropic 약 47~48억이나 Q2는 Anthropic 115억(비감사, 총액 인식) — 순위 역전 가능성, 인식 기준 차이 | T4 |
| "Anthropic은 적자" | 2025는 대규모 적자, 2026 Q2는 조정 영업이익 흑자(비감사·조정치) | T5 |
| "Microsoft capex 감소" | 가이던스 1,900→1,750억은 회계 변경, 실지출 불변 | T1 |
| "모델 가격은 계속 하락" | 장기 하락은 사실이나 2026년 하반기 최상위·캐시·소개가격 인상 사례 존재 | T7 |

## 4. 조사하지 못한 것 / 접근 불가 / 상충
- 3분기 빅테크 실적(10월 하순 예정) 미발표. Oracle·CoreWeave·xAI·Stargate 자금 구조는 조사하지 않음.
- 한국 산업통상부 보도자료 원문: ROBOTS_DISALLOWED(https://www.motir.go.kr/kor/article/ATCL4fcf3d8c6/813/view). 삼성 3Q 잠정 공시(DART) 미열람.
- Alphabet·Microsoft 실적 원문(SEC) 미열람(2차 인용). OpenAI·Anthropic 수치는 전부 비공시 2차 보도.
- 가격표 1차(각 사 pricing 페이지) 미열람. 한국 GPU 장수 최신 집계 미확인.
- 상충: Alphabet 전 분기 백로그 4,600억 vs 4,900억 / Anthropic Q1·Q2 매출 / GPT-6 Astra 가격 / Platformonomics 합계 표 불일치.

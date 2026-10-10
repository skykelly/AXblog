# C1 백지 재조사 결과 (2026-10-11 실행)

- 범위: 2026-01-01 ~ 2026-10-11, 요청서(request_r1.md)의 추적 지표 T1~T8 + 월별 사건.
- 원문확인 "예" = WebFetch로 해당 페이지를 직접 읽음(추출 도구 요약 포함). "아니오" = 검색 스니펫·제목·타 기사 인용만 봄.
- 등급 A = 1차(기관·기업 공식), B = 언론·2차 정리글, C = 판단 근거 제외.
- 주의: "원문확인=예"라도 B 등급 기사 원문이면 1차 원문은 아님. 1차 출처를 직접 읽은 행은 등급 A로 표기.

## 1. 지표별 최신값

| 지표ID | 값 | 단위 | 기준 시점 | 지역 | 측정 조건 | 출처 URL | 등급 | 원문확인 |
|---|---|---|---|---|---|---|---|---|
| C1-T1 | 44.5 (전년 33.3, +11.2%p) | % | 2025 조사, 2026-03-31 발표 (조사 기간 미확인) | 한국 | 생성형 AI 이용 "경험"(월 이용 아님). 가구 22,671, 만 3세 이상 가구원 50,750명. ChatGPT 41.8%, Gemini 9.8%, 유료구독 7.9%, 직장인 71.9% | https://www.newspim.com/news/view/20260331000211 (1차: korea.kr 보도자료는 ROBOTS_DISALLOWED로 접근 불가) | B | 예(B 기사). 1차 아니오 |
| C1-T1 보조 | 한국 앱 MAU: ChatGPT 16.46M(Mobile Index) / 23.67M(Wiseapp·Retail), Gemini 9.47M, Claude 3.44M | 명 | 2026-07 | 한국 | 앱 패널 추정치. 두 업체 방식이 달라 수치 상충(4절 참조) | https://www.dataeconomy.co.kr/news/articleView.html?idxno=41880 | B | 예(B 기사) |
| C1-T2 | 49 (2024: 33) | % | 2026-02-17~23 조사, 2026-06-17 발표 | 미국 | 성인 5,119명, AI 챗봇 이용. ChatGPT 44%, Gemini 24%, Claude 6%. 매일 이용 24%. 정보검색 용도 42%. 2024 질문은 "챗봇을 들어본 사람"만 대상이라 직접 비교 제한 | https://www.pewresearch.org/internet/2026/06/17/americans-and-ai-2026-chatbots-smart-devices-and-views-on-impact/ | A | 예 |
| C1-T2 | 64 (2025: 61), 매일 25% | % | 2026-07 조사, 2026-09-16 발표 | 미국 | 성인 5,067명(Morning Consult), "AI 이용". Pew(49%)와 정의가 달라 섞지 말 것 | https://menlovc.com/perspective/2026-the-state-of-consumer-ai/ | A(VC 자체 조사) | 예 |
| C1-T2 | 10 (전년 7) | % | Digital News Report 2026, 2026-06-16~18 공개 | 글로벌(45~48개 시장, 아래 상충) | 뉴스 목적 AI 챗봇 주간 이용. 표본·조사일 원문 페이지에서 확인 안 됨 | https://reutersinstitute.politics.ox.ac.uk/digital-news-report/2026/emerging-uses-ai-chatbots-news-and-what-it-means-journalism | A | 예(부분 페이지) |
| C1-T2 보조 | ChatGPT 주간 10억(OpenAI 발표), Gemini 앱 월 10억(Pichai), AI Mode 월 10억 이상 | 명 | 2026-08-06 / 2026-08-11 | 글로벌 | 서로 다른 정의(주간/월간)·자사 발표 | https://tech.yahoo.com/ai/chatgpt/articles/chatgpt-tops-1b-weekly-users-191537749.html ; https://techcrunch.com/2026/08/11/googles-gemini-app-surges-to-one-billion-users/ | B | 예(B 기사). 1차(OpenAI·Google) 아니오 |
| C1-T3 | AI 요약 있는 방문의 전통 링크 클릭 8% vs 없는 방문 15%; AI 요약 내 링크 클릭 약 1%; 세션 종료 26% vs 16% | % | 2025-03 브라우징(2025-07 발표). 2026 신규 Pew 갱신치는 못 찾음 | 미국 | 성인 900명 KnowledgePanel, 2025-03-01~31 | https://www.pewresearch.org/short-reads/2025/07/22/google-users-are-less-likely-to-click-on-links-when-an-ai-summary-appears-in-the-results/ | A | 예 |
| C1-T3 | 제로클릭 68.01% (2024: 60.45%); 외부 웹 도달 1,000건 중 276건 | % | 2026-01~04, 2026-06-09 발표 | 미국 | Similarweb 클릭스트림 패널, 구글 브라우저 검색만(앱 제외), 2/3 모바일. 2024값은 Datos 패널이라 연속 비교 제한. SparkToro 원문 미확인 | https://www.digitalapplied.com/blog/sparktoro-zero-click-study-2026-68-percent-seo-analysis ; https://aisearch.similarweb.com/blog/zero-click-marketing/ | B (Similarweb 블로그는 A에 가까우나 2차 서술) | 예(2차). SparkToro 원문 아니오 |
| C1-T3 | AI Overview 있는 키워드의 1위 페이지 데스크톱 CTR 약 58% 감소 (1위 CTR 0.073→0.016) | % | 2023-12 대비 2025-12, 2026-02-04 발표 | 글로벌(Ahrefs DB, 데스크톱) | 키워드 30만 개(AIO 15만+비AIO 15만), Search Console 집계, 반사실 추정 | https://ahrefs.com/blog/ai-overviews-reduce-clicks-update | A | 예 |
| C1-T3 | AI 답변에서 원출처로 "항상/자주" 클릭 4% (검색 19%, SNS 17%); 한국 8% | % | DNR 2026 (2026-06-16) | 27개 시장 | 응답자 기준(뉴스 맥락) | 위 Reuters URL | A | 예 |
| C1-T3 보조 | AI Mode는 구글 전체 검색의 0.34%, 외부 리퍼럴 1.6~2.5% (일반 결과 17~19%) | % | 2026-01~04 | 미국 | Similarweb. 같은 글에서 AI Mode 월 10억 이용자 주장과 조정되지 않음 | https://aisearch.similarweb.com/blog/zero-click-marketing/ | B | 예 |
| C1-T4 | +393% YoY (2026 Q1); +138% YoY (2026-05); 2025 연말(11~12월) +693% (리테일 +769%/+673%) | % YoY | Q1: 2026-04-16 발표 / 5월: 2026-06-17 보도 / 연말: 2026-01 | 미국 리테일 | Adobe Analytics, 방문 1조 건 이상, "AI-referred"를 보고서가 공식 정의하지 않음. 2026-03 AI 유입 전환율 +42%, 방문당 매출 +37% | https://business.adobe.com/resources/sdk/.2026-q2-ai-traffic-report/q2-2026-adi-ai-sourced-traffic-insights.pdf ; https://www.digitalcommerce360.com/2026/06/17/adobe-ai-referred-traffic-to-retail-sites-doubles-in-a-year/ | Q1·연말 A / 5월 B | Q1·연말 예 / 5월 예(B 기사) |
| C1-T4 | 프라임데이 첫날 AI 유입 +98.3% YoY; AI 유입자가 구매 확률 약 40% 높음(처음으로 최고 전환 채널); 에이전트 AI는 주요 쇼핑몰 트래픽의 1% 미만(Amazon 약 0.4%, J.P. Morgan) | % | 2026-06 말(4일 행사) | 미국 | Adobe(지출 $26.4B), J.P. Morgan | https://thenextweb.com/news/ai-shopping-prime-day-amazon-chatbots ; https://www.geekwire.com/2026/prime-day-shows-how-ai-is-changing-shopping-testing-amazons-bet-against-chatgpt-and-others/ | B | 예(B 기사) |
| C1-T4 | Adobe 홀리데이 2026 예측: AI 유입 +130% YoY (11/1~12/31); 2026-08 AI 유입 방문당 매출 +43% | % | 2026-09-28 발표 | 미국 | 예측치. 정의·산식 기사에 없음. Bloomberg 원문 미열람 | https://cryptobriefing.com/adobe-chatgpt-holiday-shopping-forecast/ | B | 예(2차 재인용). Adobe·Bloomberg 원문 아니오 |
| C1-T4 (7월 데이터) | Adobe 2026-07 AI 유입 데이터 | - | 2026-08-19 기사 | 미국 | 페이지 로드 실패, 수치 확인 못 함 | https://www.digitalcommerce360.com/2026/08/19/adobe-ai-referral-traffic-data-july-2026/ | B | 아니오 |
| C1-T5 | 쇼핑 AI 이용자 중 가격 비교 50%, 후보 압축 43%, AI 추천으로 최종 결정 37%, AI가 구매 완료 26% | % (쇼핑 AI 이용자 기준) | 2026-07 조사, 09-16 발표 | 미국 | 분모가 "AI를 쓰는 쇼핑객"이라 전체 성인 비율 아님 | https://menlovc.com/perspective/2026-the-state-of-consumer-ai/ | A | 예 |
| C1-T5 | 42% (지난 1개월 내 AI 도구로 쇼핑); 상품 추천 17%; AI 쇼핑 어시스턴트 10%; 음성 재주문 10% | % | 2026 초, 2026-05-05 발표 | 미국 | NIQ, 월 웨이브당 약 500명, "AI tool" 미정의 | https://nielseniq.com/global/en/news-center/2026/42-of-consumers-now-use-ai-tools-to-shop-niq-data-shows/ | A | 예 |
| C1-T5 | 한국: AI 쇼핑 어시스턴트를 "주요 쇼핑 수단"으로 쓰는 비율 7% (글로벌 평균 14%); 76%는 AI 환경에서도 브랜드 차별성 중시 | % | 2026-01-01~02-28 조사, 2026-06 발표 | 6개국(한국 1,107명, 총 6,379명) | Criteo 조사. "이용 경험"이 아니라 "주요 수단" 정의 | https://www.criteo.com/kr/news/press-releases/2026/06/criteo-releases-2026-commerce-and-ai-trends-report/ | A | 예 |
| C1-T5 | 한국: 패션 상품 AI 탐색 경험 39%(10대 57%), 그 이용자 중 구매 59% | % | 2026-10-01 발표 (조사 기간 미확인) | 서울·경기·5대 광역시 약 1,000명 | CJ메조미디어, 최근 3개월 패션 구매자 대상. 하위 집단 분모 | https://www.fnnews.com/news/202610011112457473 | B | 예(B 기사) |
| C1-T5 | 한국: 생성형 AI 추천 제품·서비스를 최근 3개월 내 실제 구매 49.9% | % | 2026-08-13 보도 (조사 기간 미확인) | 서울·수도권 | 프레인글로벌·한국PR학회, 생성형 AI 이용 경험자 1,000명(10~50대). 전체 국민 비율 아님 | https://ditoday.com/%EC%9D%B4%EC%A0%9C%EB%8A%94-%EC%87%BC%ED%95%91-%ED%8C%8C%ED%8A%B8%EB%84%88-49-9-ai-%EC%B6%94%EC%B2%9C-%EC%A0%9C%ED%92%88-%EA%B5%AC%EB%A7%A4%ED%96%88%EB%8B%A4/ | B | 예(B 기사) |
| C1-T5 | 소비자 82% AI 사용 경험, 58% 추천 재확인 | % | 2026-10-04 보도 | 17개국 28,000명 | VML. 정의·조사 시점 기사에 없음, 원 보고서 미확인 | https://www.madtimes.co.kr/news/articleView.html?idxno=29154 | B | 예(B 기사). 원 보고서 아니오 |
| C1-T6 | 미국 AI 쇼핑객 중 AI에 구매 완료를 맡김 26%; AI 이용자 중 최종 승인 없이 AI가 대신 행동 1회 이상 32% | % | 2026-07 조사 | 미국 | Menlo, 이메일 등 에이전트 업무 포함(32%) | https://menlovc.com/perspective/2026-the-state-of-consumer-ai/ | A | 예 |
| C1-T6 | 구매 결정을 한도 내 AI에 맡길 의향(결제 전 승인) 32%; 자율 구매 완료 허용 9%; 반복 업무(구독 갱신·재주문) 위임 74% | % | 2026-01-07~22 조사 (발표일 문서에 없음, 2026-06 보도) | 16개국 25,590명 | Accenture Consumer Pulse 2026. 의향 지표, 경험 아님 | https://www.accenture.com/content/dam/accenture/final/accenture-com/document-fy26/q4/Accenture-Consumer-Pulse-2026.pdf | A | 예 |
| C1-T6 | AI로 거래를 완료해 본 비율 11%; 45%는 AI 구매를 전혀 신뢰하지 않음; 70%는 검토·변경 가능해야 | % | 2026-08-26 발표 | 미국 성인 1,000명 | NMI 조사(결제 업체) | https://www.nmi.com/about-us/news/nmi-research-consumers-want-ai-to-help-them-shop-not-control-their-spending/ | B(업체 자체 조사) | 예 |
| C1-T6 | 완전 자율 AI 에이전트로 주문 5% | % | 2026 초 | 미국 | NIQ | NIQ URL 위와 동일 | A | 예 |
| C1-T6 | 미국 밀레니얼 42%가 $250 한도·7일 반품 보장 시 AI 구매 허용; 전 세대 35%는 사람 검토 선호 | % | 2026-08-10 | 미·영·일·프 1,800명 이상 | RTB House(마케팅 업체) | https://www.retaildive.com/news/retail-shoppers-warm-up-agentic-ai-purchases/827563/ | B | 예(B 기사) |
| C1-T6 (범위 밖) | Bain: AI로 실제 구매 10%, 구매 완료 편안 24% | % | 2025-03 조사(2025-07-01 발표) | 미국 2,016명 | 2026 갱신치 못 찾음. 기간 밖이므로 참고만 | https://www.bain.com/insights/agentic-ai-commerce-hinges-on-consumer-trust/ | A | 예 |
| C1-T6 (미확인) | Visa/Mastercard 대규모 소비자 수치 | - | - | - | 2026-03 기준 Visa는 "수백 건" 파일럿(2025-12), Mastercard 유럽 첫 실거래는 "상용 출시 아님". 2026-04 이후 갱신치 못 찾음 | https://www.forrester.com/blogs/agentic-payments-in-b2c-commerce-where-we-are-now/ | B | 예(B). 카드사 원문 아니오 |
| C1-T7 | 일반 소비자용 AI 내 결제: 확인된 가동 건 = 아래 4절(상용 사례 목록). 정확한 합계 수치는 산출 불가 | 건 | 2026-10-11 | 미국 중심 | 아래 사례 표 참고 | 아래 표 | B | 일부 예 |
| C1-T8 | 한국 사례 4~5건(아래 표). 에이전트 구매·결제까지 가동 확인된 것은 0건(Naver AI탭 PC 우측 패널 직접 구매는 베타 설명, 결제 수치 없음) | 건/상태 | 2026-10-11 | 한국 | 아래 표 참고 | 아래 표 | A/B | 일부 예 |

### T7 사례 (일반 소비자 AI 내 결제·대리구매)
| 서비스 | 상태 | 날짜 | 출처 | 등급 | 원문확인 |
|---|---|---|---|---|---|
| ChatGPT Instant Checkout (OpenAI, Etsy 시작) | 2026-03 무기한 중단, 판매자 자체 체크아웃으로 전환. Forrester는 미국 소비자 채택이 낮고 정체였다고 평가 | 2025-09 출시 → 2026-03 중단 | https://explodingtopics.com/blog/agentic-commerce-protocol ; https://www.forrester.com/blogs/agentic-payments-in-b2c-commerce-where-we-are-now/ ; (OpenAI 원문 openai.com/index/powering-product-discovery-in-chatgpt/ 로드 실패) | B | 2차만 예, OpenAI 원문 아니오 |
| PayPal + Perplexity Instant Buy | 가동(미국 PayPal 판매자), 현재 상태 최신 확인 못 함 | 2025-11-25 | Forrester 위 URL | B | 예(B) |
| Microsoft Copilot Checkout | 미국 롤아웃 시작(2026-01 기준), 이후 상태 확인 못 함 | 2026-01-08 발표 | https://stellagent.ai/insights/microsoft-copilot-checkout-nrf-2026 | B | 예(B) |
| Google UCP 체크아웃(AI Mode·Gemini) / Universal Cart | UCP 발표(2026-01-11, "곧"); Universal Cart "올여름 미국" 롤아웃 예고(2026-05-19). 실제 일반 공개 시점·범위 확인 못 함 | 2026-01-11, 2026-05-19 | https://blog.google/products-and-platforms/products/shopping/google-shopping-cart/ ; https://blog.google/company-news/inside-google/message-ceo/nrf-2026-remarks/ | A | 예 |
| Amazon Alexa for Shopping (Rufus 대체, "Buy for Me"로 타 쇼핑몰 구매) | 미국 출시 | 2026-05-13 | https://www.resultsense.com/news/2026-05-14-amazon-alexa-for-shopping-launch/ | B | 예(B). Amazon 원문 아니오 |
| Alipay AI Pay (Qwen 앱) | 거래 1.2억 건 | 2026-02-13 기준 | Forrester 위 URL | B | 예(B) |
| Walmart Sparky in ChatGPT | 발표, 결제 직접 처리 여부 불명 | 2026-03-18 | Forrester 위 URL | B | 예(B) |

### T8 한국 사례
| 서비스 | 상태 | 날짜 | 출처 | 등급 | 원문확인 |
|---|---|---|---|---|---|
| 네이버 AI탭 | 베타(네이버플러스 회원) → 전체 정식 출시. 누적 사용자 400만(베타 약 2개월), 상품·장소 카드 CTR 각 20% 이상. 예약·결제 수치 없음 | 베타 2026-04-27(발표 04-28), 정식 2026-06-26 | https://www.navercorp.com/media/pressReleasesDetail?seq=10034429 ; https://www.navercorp.com/media/pressReleasesDetail?seq=34984 | A | 예 |
| 네이버 쇼핑 AI 에이전트 | 베타 약 2026-03 → 정식 2026-07-01. 3월 대비 6월 일간 사용자 +50% 이상, 에이전트 경유 거래액 2.7배 이상. 6월 1일 보도자료는 "먼저 말 거는" 에이전트이며 결제 언급 없음. 베타 출시일 정확히 못 확인(2026-02-26 asiae 스니펫만 봄) | 2026-07-01 / 2026-06-01 | https://v.daum.net/v/20260701063609483 (연합 재게재) ; https://www.navercorp.com/media/pressReleasesDetail?seq=10034315 | B(정식 출시 기사) / A(6월 보도자료) | 예 |
| 카카오 AI 에이전트 + 쿠팡이츠 | 2분기 실적 콜에서 발표, 카톡 안에서 주문·결제 예정. 출시일 미정, 파트너십 최종화 전 | 2026-08-06 | https://www.digitaltoday.co.kr/en/view/89887/kakao-to-team-up-with-coupang-eats-on-ai-agent-to-enable-food-orders-in-kakaotalk | B | 예 |
| 쿠팡 AI 쇼핑 기능 (상품 한눈에 보기·리뷰 요약·AI 비교 등) | 가동. 구매 대행·결제 기능 언급 없음. AI 비교는 2026 초 가전·디지털에 적용 | 2026-08-07 | https://news.coupang.com/archives/65494/ | A | 예 |
| 구글 AI 모드 한국어 | 2025-09-09 한국어 정식 지원(기간 밖, 맥락용) | 2025-09-09 | https://www.kmjournal.net/news/articleView.html?idxno=3282 | B | 예 |
| 한국 구글 vs 네이버 앱 MAU | 2026-07 구글 47.02M > 네이버 46.85M, Mobile Index 집계 이래 첫 역전 | 2026-08-20 보도 | https://www.dataeconomy.co.kr/news/articleView.html?idxno=41880 | B | 예 |

## 2. 사건 목록 (월별)

| 날짜 | 주체 | 한 문장 사실 | 중요도 | 출처 URL | 등급 | 원문확인 |
|---|---|---|---|---|---|---|
| 2026-01-07 | Salesforce(Forbes 보도) | 2025 연말 AI·에이전트가 전 세계 리테일 매출의 20%(약 $262B)에 "영향"을 줬다고 발표(기여 산정 방식 불명). | 2 | https://www.forbes.com/sites/sharonedelson/2026/01/07/salesforce-holiday-survey-sees-surge-in-use-of-ai-agents/ | B | 예(B) |
| 2026-01-08 | Microsoft | NRF에서 Copilot Checkout(Stripe·PayPal·Shopify) 발표, 미국 롤아웃 시작. | 2 | https://stellagent.ai/insights/microsoft-copilot-checkout-nrf-2026 | B | 예(B) |
| 2026-01-11 | Google | NRF에서 Universal Commerce Protocol(UCP) 발표, Shopify·Etsy·Wayfair·Target·Walmart 공동 개발. | 3 | https://blog.google/company-news/inside-google/message-ceo/nrf-2026-remarks/ | A | 예 |
| 2026-01-12경 | Adobe | 2025 연말 AI 유입이 리테일에서 +693% YoY, AI 유입 전환율 +31%로 보고. | 2 | https://business.adobe.com/blog/ai-driven-traffic-surges-across-industries | A | 예 |
| 2026-02-03경 | 삼정KPMG ERI | 에이전틱 커머스 이슈모니터 발간(한국 정량 수치 없음). | 1 | https://kpmg.com/kr/ko/insights/eri/2026/issuemonitor-0202.html | A | 예 |
| 2026-02-04 | Ahrefs | AIO 노출 키워드 1위 CTR 약 58% 감소(2025-12 기준). | 3 | https://ahrefs.com/blog/ai-overviews-reduce-clicks-update | A | 예 |
| 2026-02-13 | Alibaba(Forrester 인용) | Alipay AI Pay(Qwen) 누적 1.2억 건 거래. | 2 | https://www.forrester.com/blogs/agentic-payments-in-b2c-commerce-where-we-are-now/ | B | 예(B) |
| 2026-02-26 | 네이버 | 쇼핑 AI 에이전트 베타 출시 보도(검색 스니펫만 봄, 날짜 미확정). | 2 | https://view.asiae.co.kr/article/2026022608331356140 | B | 아니오 |
| 2026-03 (월 중) | OpenAI | Instant Checkout을 무기한 중단하고 판매자 자체 체크아웃·상품 탐색 중심으로 전환. 정확한 일자 확인 못 함. | 3 | https://explodingtopics.com/blog/agentic-commerce-protocol | B | 예(B). OpenAI 원문 아니오 |
| 2026-03-18 | Walmart/OpenAI | ChatGPT 내 Sparky 통합 발표(Forrester 정리). | 2 | https://www.forrester.com/blogs/agentic-payments-in-b2c-commerce-where-we-are-now/ | B | 예(B) |
| 2026-03-31 | 과기정통부 | 2025 인터넷이용실태조사 발표: 생성형 AI 경험 44.5%. | 3 | https://www.newspim.com/news/view/20260331000211 | B | 예(B). 1차 접근 불가 |
| 2026-04-16 | Adobe | Q1 AI 유입 리테일 +393% YoY, 3월 전환율 +42%(1년 전 -38%). | 3 | https://business.adobe.com/resources/sdk/.2026-q2-ai-traffic-report/q2-2026-adi-ai-sourced-traffic-insights.pdf | A | 예 |
| 2026-04-27 | 네이버 | AI탭 베타(네이버플러스 회원 한정). | 3 | https://www.navercorp.com/media/pressReleasesDetail?seq=34984 | A | 예 |
| 2026-05-05 | NIQ | 미국 42%가 지난 1개월 내 AI 도구로 쇼핑, 5%만 자율 에이전트 주문. | 2 | https://nielseniq.com/global/en/news-center/2026/42-of-consumers-now-use-ai-tools-to-shop-niq-data-shows/ | A | 예 |
| 2026-05-13 | Amazon | Rufus를 Alexa for Shopping으로 개편, "Buy for Me"로 타 쇼핑몰 구매 대행. | 3 | https://www.resultsense.com/news/2026-05-14-amazon-alexa-for-shopping-launch/ | B | 예(B) |
| 2026-05-19 | Google | I/O에서 Universal Cart·AP2(한도·브랜드 지정 후 자동 구매) 발표, 미국 올여름 롤아웃 예고. | 3 | https://blog.google/products-and-platforms/products/shopping/google-shopping-cart/ | A | 예 |
| 2026-06-01 | 네이버 | 쇼핑앱 AI 에이전트가 사용자에게 먼저 대화를 거는 방식으로 개편(결제 언급 없음). | 2 | https://www.navercorp.com/media/pressReleasesDetail?seq=10034315 | A | 예 |
| 2026-06-09 | SparkToro(Similarweb 데이터) | 미국 구글 검색 68.01% 제로클릭(2026-01~04). SparkToro 원문은 못 읽음. | 3 | https://www.digitalapplied.com/blog/sparktoro-zero-click-study-2026-68-percent-seo-analysis | B | 예(2차) |
| 2026-06-09경 | Accenture | 소비자 74%가 반복 업무를 에이전트에 맡길 의향 보도(스니펫 날짜; 보고서 자체는 읽음). | 2 | https://www.accenture.com/content/dam/accenture/final/accenture-com/document-fy26/q4/Accenture-Consumer-Pulse-2026.pdf | A | 예(보고서). 보도 날짜는 아니오 |
| 2026-06-16 | Reuters Institute | DNR 2026: 뉴스용 AI 챗봇 주간 이용 10%(전년 7%), AI 답변에서 원출처 클릭 4%. | 3 | https://reutersinstitute.politics.ox.ac.uk/digital-news-report/2026/emerging-uses-ai-chatbots-news-and-what-it-means-journalism | A | 예 |
| 2026-06-17 | Pew | 미국 성인 49% AI 챗봇 이용(2024 33%), ChatGPT 44%. | 3 | https://www.pewresearch.org/internet/2026/06/17/americans-and-ai-2026-chatbots-smart-devices-and-views-on-impact/ | A | 예 |
| 2026-06-17 | Adobe | 5월 AI 유입 +138% YoY, 2024-10 이후 누적 +1,324%. | 2 | https://www.digitalcommerce360.com/2026/06/17/adobe-ai-referred-traffic-to-retail-sites-doubles-in-a-year/ | B | 예(B) |
| 2026-06-26 | 네이버 | AI탭 전체 사용자 정식 출시, 베타 2개월 누적 400만. | 3 | https://www.navercorp.com/media/pressReleasesDetail?seq=10034429 | A | 예 |
| 2026-06 말 | Adobe/J.P. Morgan(보도) | 프라임데이에서 AI 유입자가 처음으로 최고 전환 채널(약 +40%), 단 에이전트 AI는 트래픽 1% 미만. | 3 | https://www.geekwire.com/2026/prime-day-shows-how-ai-is-changing-shopping-testing-amazons-bet-against-chatgpt-and-others/ | B | 예(B) |
| 2026-07-01 | 네이버 | 쇼핑 AI 에이전트 정식 출시, 3월 대비 에이전트 경유 거래액 2.7배. | 3 | https://v.daum.net/v/20260701063609483 | B | 예 |
| 2026-07 | Menlo Ventures | 미국 성인 5,067명 조사 실시(발표 9월). | 1 | https://menlovc.com/perspective/2026-the-state-of-consumer-ai/ | A | 예 |
| 2026-08-04 | 미 제9순회항소법원 | Amazon의 Perplexity Comet 쇼핑 에이전트 금지 가처분을 파기(CFAA 주장 불성립). 본안은 계속. | 3 | https://www.engadget.com/2230471/perplexity-has-successfully-overturned-amazon-injunction-on-its-ai-shopping-bot/ | B | 예(B). 판결문 아니오 |
| 2026-08-06 | OpenAI | ChatGPT 주간 활성 이용자 10억 명 발표(보도). | 3 | https://tech.yahoo.com/ai/chatgpt/articles/chatgpt-tops-1b-weekly-users-191537749.html | B | 예(B) |
| 2026-08-06 | 카카오 | 2분기 콜에서 AI 에이전트 첫 파트너 쿠팡이츠(카톡 내 주문·결제), 출시일 미정. | 2 | https://www.digitaltoday.co.kr/en/view/89887/kakao-to-team-up-with-coupang-eats-on-ai-agent-to-enable-food-orders-in-kakaotalk | B | 예 |
| 2026-08-07 | 쿠팡 | 상품 요약·리뷰 요약·인포그래픽·AI 비교 등 AI 쇼핑 기능 확대 발표, 대신 구매 기능 없음. | 2 | https://news.coupang.com/archives/65494/ | A | 예 |
| 2026-08-10 | RTB House | 4개국 1,800명 조사로 에이전트 구매 허용 조건부 의향 발표. | 1 | https://www.retaildive.com/news/retail-shoppers-warm-up-agentic-ai-purchases/827563/ | B | 예(B) |
| 2026-08-11 | Google(Pichai) | Gemini 앱 월 10억 이용자, AI Mode 월 10억 이상 주장(자사 발표). 같은 날 Wiseapp: 한국 ChatGPT MAU 23.67M. | 3 | https://techcrunch.com/2026/08/11/googles-gemini-app-surges-to-one-billion-users/ | B | 예(B) |
| 2026-08-13 | 프레인글로벌·한국PR학회 | 서울·수도권 AI 이용자 49.9%가 최근 3개월 내 AI 추천 제품 구매. | 2 | https://ditoday.com/%EC%9D%B4%EC%A0%9C%EB%8A%94-%EC%87%BC%ED%95%91-%ED%8C%8C%ED%8A%B8%EB%84%88-49-9-ai-%EC%B6%94%EC%B2%9C-%EC%A0%9C%ED%92%88-%EA%B5%AC%EB%A7%A4%ED%96%88%EB%8B%A4/ | B | 예(B) |
| 2026-08-19 | Adobe(DigitalCommerce360 보도) | 7월 데이터 보도. 내용 확인 못 함. | 2 | https://www.digitalcommerce360.com/2026/08/19/adobe-ai-referral-traffic-data-july-2026/ | B | 아니오 |
| 2026-08-20 | Mobile Index(보도) | 2026-07 한국 구글 앱 MAU가 네이버를 처음 추월(47.02M vs 46.85M). | 3 | https://www.dataeconomy.co.kr/news/articleView.html?idxno=41880 | B | 예 |
| 2026-08-26 | NMI | 미국 성인 11%만 AI로 거래 완료 경험. | 2 | https://www.nmi.com/about-us/news/nmi-research-consumers-want-ai-to-help-them-shop-not-control-their-spending/ | B | 예 |
| 2026-09 (월 중) | PYMNTS Intelligence | 미국 성인 약 1.32억 명이 AI 도움으로 리테일 상품 구매, 그중 59%는 Amazon에서 종료(방법론 없음). | 1 | https://www.pymnts.com/study/will-the-2026-shopping-season-go-agentic/ | B | 예(방법론 없음) |
| 2026-09-04 | CNBC | 새학기 쇼핑 AI 관련 기사(Amazon·Google 포지셔닝). 내용 확인 못 함. | 1 | https://www.cnbc.com/2026/09/04/back-to-school-shopping-brought-to-you-by-ai-how-amazon-google-are-positioned-to-win.html | B | 아니오 |
| 2026-09-15~16 | Menlo Ventures | State of Consumer AI 2026: 미국 성인 64% AI 이용, 매일 25%, 쇼핑 AI 이용자 26%가 구매 완료 위임, 소비자 AI 지출 $40B. | 3 | https://menlovc.com/perspective/2026-the-state-of-consumer-ai/ | A | 예 |
| 2026-09-28 | Adobe(Bloomberg 보도) | 홀리데이 2026 AI 유입 +130% 예측, 온라인 지출 $275.1B 예측. | 2 | https://cryptobriefing.com/adobe-chatgpt-holiday-shopping-forecast/ | B | 예(2차 재인용) |
| 2026-10-01 | CJ메조미디어 | 패션 AI 탐색 39%, 탐색자 중 구매 59%. | 2 | https://www.fnnews.com/news/202610011112457473 | B | 예 |
| 2026-10-04 | VML | 17개국 28,000명, AI 사용 82%·추천 재확인 58% 보도. | 1 | https://www.madtimes.co.kr/news/articleView.html?idxno=29154 | B | 예(원 보고서 아니오) |
| 2026-10-05 | MediaPost(Menlo 인용) | 에이전트 구매가 향후 12개월 $100B 온라인 매출을 낼 것이라는 Menlo 예측 보도. | 2 | https://www.mediapost.com/publications/article/418497/ai-agents-forecast-to-drive-100b-in-sales-by-next.html | B | 예 |

(2026-10-06~11 사이 신규 사건은 검색 한도 소진 전에 확인하지 못함. 4절 참조.)

## 3. 단정성 사실 점검

| '최고/최초/유일' 주장 | 최신 기준 확인 결과 | 출처 |
|---|---|---|
| "ChatGPT 내에서 바로 결제하는 서비스가 있다" | 반례: Instant Checkout은 2026-03 중단. 현재는 판매자 체크아웃 연결 방식. 단정 금지. | https://explodingtopics.com/blog/agentic-commerce-protocol (B) |
| "ChatGPT 이용자 9억 명(주간)" | 2026-08-06 OpenAI가 주간 10억 발표(보도). 이전 9억(2026-02)은 구값. | https://tech.yahoo.com/ai/chatgpt/articles/chatgpt-tops-1b-weekly-users-191537749.html (B) |
| "Gemini 앱 7.5억 / 9.5억 MAU" | 2026-08-11 Pichai가 월 10억 돌파 주장. 7.5억은 2025 Q4, 9.5억은 검색 결과 제목(2026-07)만 봄. | https://techcrunch.com/2026/08/11/googles-gemini-app-surges-to-one-billion-users/ (B) |
| "AI 유입 전환율이 비AI보다 낮다" | 반례: Adobe 2026-03 +42%, 프라임데이 최고 전환 채널. 2025 초 -38%는 과거값. | Adobe Q2 리포트 PDF (A), GeekWire (B) |
| "AI 유입 최고 증가율 693%" | 2025 연말 +693%, 2026 Q1 +393%, 5월 +138%로 증가율은 감소(기저 효과). 홀리데이 2026 예측 +130%. 절대 규모는 별도 확인 필요. | Adobe 블로그·PDF (A) |
| "AI 요약이 있으면 클릭 8% vs 15%" (Pew) | 2025-03 데이터. 2026 갱신 Pew 수치는 못 찾음. 최신 대체 지표는 Ahrefs(1위 CTR -58%). | Pew short read (A), Ahrefs (A) |
| "제로클릭 68%" | 방법론 변경(Datos→Similarweb)으로 2024와 직접 비교 불가, 브라우저 검색만. SparkToro 원문 미확인. | digitalapplied (B) |
| "네이버가 한국 검색·앱 1위" | 2026-07 Mobile Index 기준 구글 앱 MAU가 네이버를 처음 추월(3월 2021 집계 이래). 앱 MAU 기준이지 검색 점유율 아님. | https://www.dataeconomy.co.kr/news/articleView.html?idxno=41880 (B) |
| "Amazon은 외부 쇼핑 에이전트를 막는다/Perplexity는 금지됐다" | 2026-06 기사는 가처분 승소로 서술했으나 2026-08-04 항소심이 가처분 파기. 최신은 파기 상태(본안 진행). | Engadget (B) |
| "AI가 대신 구매하는 소비자는 소수" | 수치가 정의별로 5%~32%로 갈림(NIQ 5%, NMI 11%, Menlo 26%/32%, Accenture 자율 9%). 단일 수치로 단정 금지. | 지표 표 |
| "한국에 AI 구매 대행 에이전트가 없다" | 최신 기준 가동 확인 0건이나, 카카오-쿠팡이츠(결제 포함) 발표됨(미출시), 네이버 AI탭 PC 직접 구매 기능 베타 설명 있음. | 네이버 보도자료 (A), 디지털투데이 (B) |

## 4. 조사하지 못한 것, 접근 불가, 상충

### 접근 불가·로드 실패
- korea.kr 과기정통부 2025 인터넷이용실태조사 보도자료: ROBOTS_DISALLOWED (1차 미확인, 뉴스핌 기사로 대체).
- 네이트뉴스(카카오·AI쇼핑 경쟁 기사 2건): ROBOTS_DISALLOWED. 다른 매체로 대체.
- OpenAI 원문(powering-product-discovery, buy-it-in-chatgpt): 로드 실패·권한 미응답. Instant Checkout 중단은 2차 출처로만 확인.
- Adobe 2026-07 데이터 기사(digitalcommerce360 2026-08-19): 두 차례 로드 실패.
- CNBC 2026-03-20(OpenAI 쇼핑), 2026-09-04(새학기 AI 쇼핑): 로드 실패·미응답.
- Amazon Alexa for Shopping 1차(aboutamazon) 미열람, Bloomberg(Adobe 홀리데이 예측) 미열람.

### 조사 한도로 못 한 것
- WebSearch 호출 한도(200회)가 소진되어 Microsoft Copilot Checkout 이후 상태, 2026-10-06~11 신규 사건, Salesforce 2026 쇼핑 지표 1차, 한국 AI 쇼핑 설문(오픈서베이·대한상의 등)을 추가로 찾지 못함. 추가 조사는 후속 요청이 필요.
- Pew·Similarweb·SparkToro의 2026 갱신 클릭률 1차 원문, Visa·Mastercard 2026-04 이후 에이전트 결제 실적, KISDI 2026 통계는 확인 못 함.
- 한국 정부 통계는 2025 조사(2026-03 발표)만 확인. KISDI 자료는 2024 한국미디어패널(2025-07 발간)이라 기간 밖.
- Korea 월별 사건 중 2월(네이버 쇼핑 에이전트 베타 정확 일자), 9월(한국 AI 쇼핑 신규 발표)은 근거를 못 찾음.

### 출처끼리 상충
- 미국 AI 이용률: Pew 49%(챗봇, 2026-02) vs Menlo 64%(AI 일반, 2026-07). 정의·시점이 달라 섞지 말 것.
- 한국 ChatGPT MAU 2026-07: Mobile Index 16.46M vs Wiseapp·Retail 23.67M(방식 차이, 같은 기사).
- Reuters DNR 시장 수: GIJN 기사 "48개국" vs Reuters 페이지 "이용 질문 45개 시장, 클릭 질문 27개 시장". 표본·조사일은 어느 쪽에서도 확인 못 함.
- Reuters 클릭 지표: 페이지는 "응답자 4%가 AI에서 원출처 자주 클릭" vs GIJN은 "챗봇 이용자 42%가 자주 클릭"으로 분모가 다름.
- Gemini: 검색 결과(2026-07)에는 950M, TechCrunch(2026-08-11)는 1B. 시점 차이일 가능성이 크나 확정 못 함.
- Perplexity 금지 가처분: GeekWire 2026-06 서술(승소) vs Engadget 2026-08-04(항소심 파기). 시간 순서상 최신은 파기.
- Adobe 재인용: 2026-08 AI 방문당 매출 +43%는 2차 재인용(원문 미확인), 3월 +37%와 시점이 달라 비교 불가.
- Similarweb 글은 AI Mode 월 10억 이용자와 전체 검색 중 0.34% 비중을 조정 없이 병기.

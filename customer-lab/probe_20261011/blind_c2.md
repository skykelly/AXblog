# C2 백지 재조사 (검증용) — 2026-10-11

- 읽은 내부 파일: request_r1.md 1개뿐. 웹 조사(WebSearch/WebFetch)만 사용.
- 원문확인 기준: "예" = 1차 출처(기업 공식 발표·실적 원문·기관 보도자료) 페이지를 직접 열어 해당 값을 읽음. "아니오" = 2차 기사·요약·스니펫만 확인(2차 기사 본문을 읽은 경우에도 원문 아님). "접근불가" = ROBOTS_DISALLOWED 등.
- 월별 개별 검색은 1·2·4·6·9·10월은 월 단위로, 3·5·7·8월은 주제별 검색 결과에서 포착(월 단위 전용 검색 없음). 4번 항목 참조.

## 1. 지표별 최신값

| 지표ID | 값 | 단위 | 기준 시점 | 지역 | 측정 조건 | 출처 URL | 등급 | 원문확인 |
|---|---|---|---|---|---|---|---|---|
| C2-T1a | Alexa for Shopping(구 Rufus+Alexa+ 통합, 2026-05-13) 최근 12개월 이용 고객 350M 이상 | 명 | Q2 2026 (2026-07-30 발표) | 글로벌(Amazon 전체) | "last 12 months" 이용 고객. 활성 이용자 전년 대비 약 2배, 상호작용 5배 이상 | https://www.aboutamazon.com/news/company-news/amazon-ceo-andy-jassy-stores-growth-ai-shopping-q2-2026-earnings | A | 예 |
| C2-T1b | 미국 Alexa for Shopping 이용 고객 주문당 지출 비이용자 대비 40% 이상 많음 | % | Q2 2026 | 미국 | 이용자 vs 비이용자 비교, 인과 아님(상관). 표본·정의 미공개 | https://s2.q4cdn.com/299287126/files/doc_earnings/2026/q2/earnings-result/AMZN-Q2-2026-Earnings-Release.pdf | A | 예 |
| C2-T1c | Rufus 2025년 이용 고객 300M, 연환산 증분 매출 약 $12B, 구매 완료 가능성 60% 높음 | 명·달러·% | 2025년 기준, 2026-02 실적 발표 | 글로벌 | Amazon 자체 추정 증분 매출. 이후 Rufus 명칭은 Alexa for Shopping으로 대체. 원 실적 문서 미열람 | https://www.modernretail.co/technology/amazon-says-its-ai-shopping-assistant-is-gaining-traction-with-rufus-users-up-115/ | B | 아니오 |
| C2-T1d | Rufus 월간 활성 이용자 +115% YoY, 참여도 +400% | % YoY | Q1 2026 (2026-04-29 콜) | 글로벌 | Jassy 발언(콜). 분모 절대값 미공개 | https://www.modernretail.co/technology/amazon-says-its-ai-shopping-assistant-is-gaining-traction-with-rufus-users-up-115/ | B | 아니오 |
| C2-T1e | Walmart Sparky 이용 고객 +70% YoY, Sparky 이용자 주문당 +40% | % | Q2 FY27 (2026-07-31 종료, 08-20 발표) | 미국 | 2차 보도(ppc.land) 값. Walmart 공식 실적 페이지에는 Sparky 언급 없음 | https://ppc.land/walmart-ad-business-gains-38-as-walmart-connect-hits-43-in-q2/ | B | 아니오 |
| C2-T1f (한국) | 네이버 쇼핑 AI 에이전트: 월간 이용자·일 대화수 정식출시(3월) 대비 약 5배, 일 거래액 약 4배, 가전·디지털 거래액 비중 40%, 네이버플러스 회원 비중 78% | 배수·% | 2026-08 기준(보도 2026-09-27) | 한국 | 네이버 제시 수치의 연합 보도. 절대 이용자 수 미공개. 기준 시점 '지난달' | https://www.fnnews.com/news/202609270633124595 | B | 아니오 |
| C2-T1g (한국) | 네이버 에이전트 6월 일간 사용자 3월 대비 +50% 이상, 일 재방문 약 3배, 거래액 2.7배 이상 | 배수 | 2026-06 기준(2026-07-01 보도) | 한국 | 베타(3월) 대비. 절대값 미공개 | https://v.daum.net/v/20260701063609483 | B | 아니오 |
| C2-T1h (한국) | 챗GPT 포 카카오 누적 이용자 1,300만 | 명 | 2026 Q2 (2026-08-06 콜) | 한국 | 누적 이용자(MAU 아님). 연말 목표: 카카오톡 내 AI 월간 활성 1,000만 | https://zdnet.co.kr/view/?no=20260806111654 | B | 아니오 |
| C2-T2a | ChatGPT 광고: 미국 테스트 발표(02-09) 이후 08-11 영국·멕시코·브라질·일본·한국 확대. Free·Go 로그인 성인 대상, Plus 이상 무광고. 노출 비율(%) 공식 수치 없음 | 상태 | 2026-08-11 | 글로벌(미국 외 다수) | 광고는 답변 안 '스폰서' 라벨 구분 지면. 민감 주제(건강·정치 등)·미성년 제외 | https://openai.com/index/testing-ads-in-chatgpt/ | A | 예 |
| C2-T2b | ChatGPT 광고 연환산 매출 약 $1B, 40개국 이상 | 달러 | 2026-08-31 발표 | 글로벌 | run rate. OpenAI 발표를 Quartz 경유 재인용. CNBC 원 기사는 열람 실패 | https://finance.yahoo.com/media-advertising/articles/openai-chatgpt-ads-hit-1-132117654.html | B | 아니오 |
| C2-T2c | Amazon 스폰서 프롬프트(Rufus/Alexa): 2025-11-11 무료 베타, 2026-03-25 CPC 과금 전환. 프롬프트 클릭자 구매전환 +48%, 지출 +21% | 상태·% | Q2 2026 | 글로벌 | Jassy 발언을 ppc.land가 인용. Q1 릴리스에는 "프롬프트 상호작용자의 약 20%가 해당 브랜드 대화 지속" | https://ppc.land/amazon-advertising-gains-26-to-19-8-billion-as-sports-inventory-sells-out/ | B | 아니오 |
| C2-T2d | Amazon Q1 릴리스: 프롬프트 상호작용 쇼핑객 약 20%가 해당 브랜드 대화 지속 | % | Q1 2026 (2026-04-29) | 글로벌 | 릴리스 본문 요약 | https://www.sec.gov/Archives/edgar/data/1018724/000101872426000012/amzn-20260331xex991.htm | A | 예 |
| C2-T2e | Google AI Mode 광고: Conversational Discovery·Highlighted Answers 포맷 테스트 중(출시일 미정). Direct Offers 파일럿 2026-01 시작. Gemini 앱 내 광고는 2025-12-08 Google 광고 VP "계획 없음" 부인 이후 확인된 도입 없음 | 상태 | 2026-05-20 | 글로벌(지역 미명시) | 테스트 단계. 노출 비율 공식 수치 없음 | https://blog.google/products/ads-commerce/google-marketing-live-search-ads/ | A | 예 |
| C2-T2f | AI Overview 하단 광고 노출 약 25.5% (2026-03) | % | 2026-03 | 글로벌(추정) | 1차 출처 없음, 수치 자체 불일치(3%→25.5%인데 +394% 표기). 판단 근거 제외 | https://www.digitalapplied.com/blog/google-ai-mode-75m-users-ads-in-ai-results-2026 | C | 아니오 |
| C2-T2g | Perplexity 광고 철수 (2025-10 신규 광고주 중단, 구독·기업 판매 집중) | 상태 | 2026-02-18 보도 | 글로벌 | FT 인용 보도. 원문 미열람 | https://www.emarketer.com/content/perplexity-retreat-ads-marks-split-on-ai-monetization-models | B | 아니오 |
| C2-T2h (한국) | 네이버 AI 브리핑 광고(2026-07 말 출시): 클릭률 기존 검색광고 대비 +30% 이상, 구매전환 3배 이상(네이버 주장). 2분기 광고 매출 +7.5% YoY, 성장 기여의 60% 이상이 AI | % | 2026 Q2 (2026-08-07) | 한국 | 회사 주장, 표본·산식 미공개 | https://www.navercorp.com/media/pressReleasesDetail?seq=10034577 | A | 예 |
| C2-T3a | UCP: 공동개발 5곳(Shopify·Etsy·Wayfair·Target·Walmart), 지지(endorser) 20곳 이상 | 곳 | 2026-01-11 | 미국 중심 | Google 블로그 기준. 9to5google은 공동개발 4곳(Walmart 제외)으로 기재 → 상충 | https://blog.google/products/ads-commerce/agentic-commerce-ai-tools-protocol-retailers-platforms/ | A | 예 |
| C2-T3b | UCP 선언 스토어(검증) 17,767곳(Shopify 10,632, Wix 6,929) | 곳 | 2026-09-22 | 글로벌 | 제3자 크롤링 추적기(UCP Checker), 공개 manifest 기준. 실제 거래 가능 여부와 다름, 일부 대형 리테일러 누락 가능 | https://ucpchecker.com/blog/state-of-agentic-commerce-september-2026 | C | 아니오 |
| C2-T3c | ACP(OpenAI) 참여사 수 | 곳 | - | - | 공식 집계 확인 못 함. Instant Checkout은 2026-03 중단, ACP는 가맹점 앱 방식으로 유지(2차 보도) | https://webinterpret.com/en/blog/openai-abandons-instant-checkout | C | 아니오 |
| C2-T3d | Visa Intelligent Commerce Connect: 파일럿 파트너 7곳 명시(Aldar, AWS, Diddo, Highnote, Mesh, Payabli, Sumvin), "select partners including" | 곳 | 2026-04-08 추정(표기 04/08/2026이 4월 8일 vs 8월 4일 모호) | 글로벌 | 최소 7곳, 전체 수 미공개 | https://corporate.visa.com/en/sites/visa-perspectives/newsroom/visa-intelligent-commerce-connect-ai-shopping-for-businesses.html | A | 예 |
| C2-T3e | Mastercard Agent Pay: 참여사·거래 건수 미공개. 2026-09-30 '에이전트 개시 확률 점수'(미국 테스트), Cloudflare·Skyfire 파트너 | 상태 | 2026-09-30 | 미국 | 건수 수치 없음 | https://www.mastercard.com/us/en/news-and-trends/press/2026/september/new-trust-and-intelligence-services.html | A | 예 |
| C2-T4a | 고객이 최근 서비스 상호작용에서 서드파티 GenAI(ChatGPT·Gemini·Copilot)를 기업 챗봇보다 약 3배 더 이용. 서드파티 GenAI 이용은 1년간 거의 2배, 기업 챗봇 이용은 2022년 이후 통계적 불변 | 배수 | 조사 2026-02~03, 발표 2026-07-08 | 지역 미명시(Gartner 미국 발표) | B2B·B2C 고객 3,566명. GenAI 정의·문항 미공개 | https://www.gartner.com/en/newsroom/press-releases/2026-07-08-gartner-survey-finds-customers-are-three-times-more-likely-to-use-third-party-genai-than-company-provided-chatbots-for-customer-service | A | 예 |
| C2-T4b | 87%: GenAI 이용 기업은 사람 상담원 접근 옵션 제공이 필수. 50%: GenAI로 상호작용이 더 쉬워짐. 58%: GenAI 이용자 중 업무 대행에 사용(B2B 74%) | % | 조사 2026-02~03, 발표 2026-08-04 | 지역 미명시 | 동일 표본 3,566명. 분모(전체 vs GenAI 이용자) 항목별로 다름, 방법론·오차 미공개 | https://www.gartner.com/en/newsroom/press-releases/2026-08-04-gartner-survey-finds-87-percent-of-customers-say-companies-using-genai-for-customer-service-must-provide-access-to-a-human-agent0 | A | 예 |
| C2-T4c | 서비스·지원 리더 AI 예산 중앙값 12%, 긍정 재무 성과 입증 24% | % | 조사 2026-01~04 | 지역 미명시 | 리더 1,303명, 별도 조사 | 위 07-08 Gartner 릴리스 | A | 예 |
| C2-T4d | Forrester 2026 예측 등 Forrester 수치 | - | - | - | 보고서 유료 장벽으로 본문 미확인. 한 보도에서 "미국 성인 24%가 루틴 구매를 AI 에이전트에 맡길 만큼 신뢰(2025-03 Forrester)" 재인용만 확인 | https://www.fintechweekly.com/magazine/articles/agentic-commerce-launch-month-liability-risk-2026 | C | 아니오 |
| C2-T5a | Alexa for Shopping(2026-05-13 Rufus+Alexa+ 통합) | 건 | 2026-05 | 글로벌 | Amazon 자체 에이전트 | https://s2.q4cdn.com/299287126/files/doc_earnings/2026/q2/earnings-result/AMZN-Q2-2026-Earnings-Release.pdf | A | 예 |
| C2-T5b | Walmart Sparky를 ChatGPT·Gemini 안에 임베드, 결제는 Walmart 자체 시스템. OpenAI Instant Checkout 파일럿 종료(채팅 내 전환율이 자사 사이트 클릭 대비 약 3배 낮음) | 건·상태 | 2026-03-24 보도 | 미국 | Walmart 고위 관계자 발언 인용. Walmart 공식 발표 미열람 | https://thepaypers.com/payments/news/walmart-drops-openai-checkout-and-deploys-sparky-on-ai-platforms | B | 아니오 |
| C2-T5c (한국) | 네이버 쇼핑 AI 에이전트(베타 2026-02-26, 정식 07-01), 쿠팡 AI 상품 비교·하이라이트(2026-08-07, 정량 지표 없음), 카카오 카나나 인 카카오톡(2026-04 말 화면 내 결제), 카카오 에이전트 첫 파트너 쿠팡이츠(08-06) | 건 | 2026-02~09 | 한국 | 쿠팡은 별도 챗봇이 아니라 상품 페이지 내 AI 기능 | https://news.coupang.com/archives/65494/ | A (쿠팡 건) | 예 (쿠팡 건) |
| C2-T6a | Amazon v. Perplexity: 2026-03-09 N.D. Cal. 예비금지명령 인용(Chesney 판사) → 2026-08-04 제9순회 항소법원이 금지명령 파기·환송(No. 26-1444). CFAA·CDAFA 접근 요건 미충족 소지, 약관·계약·불법행위 청구는 열려 있음 | 건·상태 | 2026-08-04 | 미국 | 가처분 단계 판단(본안 아님). 판결문 원문 미열람, 로펌 요약 | https://www.cooley.com/news/insight/2026/2026-08-06-ninth-circuit-rules-on-ai-agent-access-to-third-party-websites-under-cfaa | B | 아니오 |
| C2-T6b | Amazon이 Meta Muse(2026-09-08 출시) 에이전트의 Amazon.com 주문 차단(2026-09-20, Conditions of Use 위반 주장). 법적 조치 여부 미공개, Meta와 협의 중 | 건 | 2026-09-20 | 미국 | Amazon 성명을 ppc.land 인용 | https://ppc.land/amazon-blocks-metas-muse-ai-agent-from-shopping-on-its-site/ | B | 아니오 |
| C2-T6c | 에이전트 차단·제한 사례: Yelp(유료 라이선스 외 비인간 트래픽 불허), eBay(무허가 에이전트 제한), Delta·United 약관 금지, Adidas·Pizza Hut(이용자 불만 기반), Walmart(Muse 체크아웃 실패는 의도 아님, Muse 파트너) | 건 | 2026-10-06 | 미국 | 집계 수치 없음, 일부는 이용자 주장 | https://techcrunch.com/2026/10/06/the-next-hurdle-for-ai-agents-getting-websites-to-let-them-in | B | 아니오 |
| C2-T7a (한국) | 네이버: 쇼핑 에이전트 정식 출시(07-01), 에이전트 내 결제 파일럿 연내 계획(미출시), PC 버전 연내 계획 | 상태 | 2026-09-27 | 한국 | 결제는 계획 단계 | https://www.fnnews.com/news/202609270633124595 | B | 아니오 |
| C2-T7b (한국) | 카카오: 카나나 독립 앱·PC 2026-10-15 종료, 카카오톡 안으로 통합. 카카오툴즈 연동 서비스 28개(2차 파트너 7곳 추가: 다이소몰·신한카드·LF몰 등) | 상태·건 | 2026-09-11 / 09-15 | 한국 | 챗GPT 포 카카오 안 연동 | https://view.asiae.co.kr/article/2026091110363804383 | B | 아니오 |
| C2-T7c (한국) | 네이버 2분기 Npay 결제액 25.2조 원(+21.0% YoY), 플랫폼 서비스 매출 +31.3%. 에이전트 별도 수치 없음 | 원·% | 2026 Q2 (2026-08-07) | 한국 | 에이전트 기여분 분리 안 됨 | https://www.navercorp.com/media/pressReleasesDetail?seq=10034577 | A | 예 |
| C2-T8a | Amazon 광고 서비스 매출 $19,809M, +26% YoY (2025 Q2 $15,694M) | 달러·% | Q2 2026 (2026-06-30 종료, 07-30 발표) | 글로벌 | 릴리스 표기 +26%. 일부 보도는 환율 제외 기준이라 명시, 릴리스 원문에서 환율 조건은 확인 못 함 | https://s2.q4cdn.com/299287126/files/doc_earnings/2026/q2/earnings-result/AMZN-Q2-2026-Earnings-Release.pdf | A | 예 |
| C2-T8b | Amazon 광고 Q1 2026 $17,243M, +24% (Q1 2025 $13,921M) | 달러·% | Q1 2026 | 글로벌 | 릴리스 표 | https://www.sec.gov/Archives/edgar/data/1018724/000101872426000012/amzn-20260331xex991.htm | A | 예 |
| C2-T8c | Walmart 글로벌 광고 +38%(VIZIO 포함), Walmart Connect 미국 +43%(VIZIO 제외), 국제 광고 +20% | % YoY | Q2 FY27 (2026-07-31 종료, 08-20 발표) | 글로벌·미국 | 공식 릴리스에서 43%·20% 확인. 38% 글로벌/미국은 ppc.land 보도 | https://corporate.walmart.com/news/2026/08/20/walmart-releases-q2-fy27-earnings | A | 예(43%·20%), 아니오(38%) |

## 2. 사건 목록 (월별)

| 날짜 | 주체 | 한 문장 사실 | 중요도 | 출처 URL | 등급 | 원문확인 |
|---|---|---|---|---|---|---|
| 2026-01-11 | Google | UCP 공개: 공동개발 5곳(Shopify·Etsy·Wayfair·Target·Walmart), AI Mode·Gemini 내 미국 리테일러 체크아웃과 Business Agent 발표 | 3 | https://blog.google/products/ads-commerce/agentic-commerce-ai-tools-protocol-retailers-platforms/ | A | 예 |
| 2026-01 | Google | Direct Offers 광고 파일럿 시작(AI Mode 내 독점 오퍼) | 2 | https://blog.google/products/ads-commerce/google-marketing-live-search-ads/ | A | 예 |
| 2026-01-11 | Walmart·Google | Walmart와 Gemini 쇼핑 제휴 발표 | 2 | https://www.cnbc.com/2026/01/11/walmart-partners-with-google-gemini-on-shopping-tool.html | B | 아니오 |
| 2026-02-09 | OpenAI | ChatGPT 광고 미국 테스트 발표 | 3 | https://openai.com/index/testing-ads-in-chatgpt/ | A | 예 |
| 2026-02 | Amazon | Rufus 2025년 이용 고객 300M, 증분 매출 약 $12B 공개(2차 보도) | 3 | https://www.modernretail.co/technology/amazon-says-its-ai-shopping-assistant-is-gaining-traction-with-rufus-users-up-115/ | B | 아니오 |
| 2026-02-18 | Perplexity | 인챗 광고에서 철수, 구독·기업 매출 집중(FT 인용) | 2 | https://www.emarketer.com/content/perplexity-retreat-ads-marks-split-on-ai-monetization-models | B | 아니오 |
| 2026-02-26 | 네이버 | 쇼핑 AI 에이전트 베타 출시(네이버플러스 스토어 앱) | 3 | https://view.asiae.co.kr/article/2026022608331356140 | B | 아니오 |
| 2026-03-05 | OpenAI | Instant Checkout 중단 인정("전환 미달"), 가맹점 앱 방식으로 전환(2차 보도, OpenAI 원문 미확인) | 3 | https://webinterpret.com/en/blog/openai-abandons-instant-checkout | C | 아니오 |
| 2026-03-09 | N.D. Cal. | Amazon v. Perplexity 예비금지명령 인용 | 3 | https://www.geekwire.com/2026/judge-blocks-perplexitys-ai-bot-from-shopping-on-amazon-in-early-test-of-agentic-commerce/ | B | 아니오 |
| 2026-03-19 | 카카오 | 카나나 정식 출시 보도(스니펫만 확인) | 1 | https://www.ajunews.com/view/20260319133505213 | B | 아니오 |
| 2026-03-24 | Walmart | OpenAI Instant Checkout 파일럿 종료, Sparky를 ChatGPT·Gemini에 임베드 | 3 | https://thepaypers.com/payments/news/walmart-drops-openai-checkout-and-deploys-sparky-on-ai-platforms | B | 아니오 |
| 2026-03-25 | Amazon | Rufus 스폰서 프롬프트 CPC 과금 전환(2025-11-11 무료 베타 후) | 2 | https://ppc.land/amazon-advertising-gains-26-to-19-8-billion-as-sports-inventory-sells-out/ | B | 아니오 |
| 2026-04-27 | 네이버 | 쇼핑·플레이스 연동 AI 탭 출시 | 1 | https://www.newspim.com/news/view/20260430000407 | B | 아니오 |
| 2026-04-29 | Amazon | Q1 광고 $17.2B +24%, 스폰서 프롬프트 상호작용 약 20% 대화 지속, Rufus MAU +115%(Jassy) | 3 | https://www.sec.gov/Archives/edgar/data/1018724/000101872426000012/amzn-20260331xex991.htm | A | 예(광고·프롬프트), 아니오(MAU) |
| 2026-04 말 | 카카오 | 카나나 인 카카오톡에 화면 내 결제 적용(2026-05-13 보도) | 2 | https://www.etnews.com/20260513000299 | B | 아니오 |
| 2026-05-13 | Amazon | Rufus와 Alexa+를 Alexa for Shopping으로 통합 | 3 | https://ppc.land/amazon-advertising-gains-26-to-19-8-billion-as-sports-inventory-sells-out/ | B | 아니오 |
| 2026-05-19 | Google | I/O: Universal Cart(Search·Gemini·YouTube·Gmail 횡단 장바구니), UCP 캐나다·호주·영국 확대 예고, AP2 도입 예고 | 3 | https://blog.google/products-and-platforms/products/shopping/google-shopping-cart/ | A | 예 |
| 2026-05-20 | Google | Marketing Live: AI Mode 광고 포맷(Conversational Discovery, Highlighted Answers) 테스트 | 3 | https://blog.google/products/ads-commerce/google-marketing-live-search-ads/ | A | 예 |
| 2026-05 (Q1 콜) | 카카오 | 카카오톡을 에이전틱 AI 플랫폼으로 전환(5천만 이용자), 2030 AI DAU 2천만 목표 | 2 | https://biz.newdaily.co.kr/site/data/html/2026/09/23/2026092300150.html | B | 아니오 |
| 2026-06-19 | OpenAI | ChatGPT 광고 한국 파일럿(Free·Go) | 2 | https://www.koreajoongangdaily.com/business/openai-starts-showing-ads-to-lowertier-chatgpt-users-in-korea/12731460 | B | 아니오 |
| 2026-07-01 | 네이버 | 쇼핑 AI 에이전트 정식 출시(베타 약 4개월 후) | 3 | https://v.daum.net/v/20260701063609483 | B | 아니오 |
| 2026-07-08 | Gartner | 고객의 서드파티 GenAI 이용이 기업 챗봇의 약 3배 | 3 | https://www.gartner.com/en/newsroom/press-releases/2026-07-08-gartner-survey-finds-customers-are-three-times-more-likely-to-use-third-party-genai-than-company-provided-chatbots-for-customer-service | A | 예 |
| 2026-07-21 | 재정경제부 | 에이전트 커머스 실증을 위한 제도 개선·규제 샌드박스 추진 | 2 | https://www.wowtv.co.kr/NewsCenter/News/Read?articleId=A202607210338 | B | 아니오 |
| 2026-07-30 | Amazon | Q2 광고 $19.8B +26%, Alexa for Shopping 12개월 350M 이상 | 3 | https://s2.q4cdn.com/299287126/files/doc_earnings/2026/q2/earnings-result/AMZN-Q2-2026-Earnings-Release.pdf | A | 예 |
| 2026-08-04 | 제9순회 항소법원 | Perplexity Comet 금지명령 파기·환송 | 3 | https://www.cooley.com/news/insight/2026/2026-08-06-ninth-circuit-rules-on-ai-agent-access-to-third-party-websites-under-cfaa | B | 아니오 |
| 2026-08-04 | Gartner | 87%가 GenAI 상담 시 사람 연결 옵션 필수 | 3 | https://www.gartner.com/en/newsroom/press-releases/2026-08-04-gartner-survey-finds-87-percent-of-customers-say-companies-using-genai-for-customer-service-must-provide-access-to-a-human-agent0 | A | 예 |
| 2026-08-06 | 카카오 | Q2 콜: 챗GPT 포 카카오 누적 1,300만, 에이전트 첫 파트너 쿠팡이츠 | 2 | https://zdnet.co.kr/view/?no=20260806111654 | B | 아니오 |
| 2026-08-07 | 쿠팡 | 상품 페이지 AI 요약·비교·리뷰 요약 도입(정량 지표 없음) | 2 | https://news.coupang.com/archives/65494/ | A | 예 |
| 2026-08-07 | 네이버 | Q2: 광고 +7.5%(AI 기여 60%+), AI 브리핑 광고, Npay 25.2조 원 | 2 | https://www.navercorp.com/media/pressReleasesDetail?seq=10034577 | A | 예 |
| 2026-08-11 | OpenAI | ChatGPT 광고를 영국·멕시코·브라질·일본·한국으로 확대 | 3 | https://openai.com/index/testing-ads-in-chatgpt/ | A | 예 |
| 2026-08-20 | Walmart | Q2 FY27: Walmart Connect 미국 +43%, 글로벌 광고 +38%, Sparky 이용자 +70% | 3 | https://corporate.walmart.com/news/2026/08/20/walmart-releases-q2-fy27-earnings | A | 예(43%), 아니오(Sparky·38%) |
| 2026-08-31 | OpenAI | ChatGPT 광고 연환산 약 $1B, 40개국 이상, 인도·EMEA 셀프서브 개방 | 3 | https://finance.yahoo.com/media-advertising/articles/openai-chatgpt-ads-hit-1-132117654.html | B | 아니오 |
| 2026-09-08 | Meta | Muse 개인 에이전트 출시(Stripe Link 결제), 9월 Connect에서 Walmart 등 파트너 발표 | 3 | https://ppc.land/amazon-blocks-metas-muse-ai-agent-from-shopping-on-its-site/ | B | 아니오 |
| 2026-09-11 | 카카오 | 카카오툴즈 파트너 7곳 추가, 연동 28개 | 2 | https://view.asiae.co.kr/article/2026091110363804383 | B | 아니오 |
| 2026-09-15 | 카카오 | 카나나 독립 앱 10-15 종료, 카카오톡 중심 전환 | 2 | https://www.fnnews.com/news/202609151803363368 | B | 아니오 |
| 2026-09-20 | Amazon | Meta Muse 에이전트의 Amazon 주문 차단 | 3 | https://ppc.land/amazon-blocks-metas-muse-ai-agent-from-shopping-on-its-site/ | B | 아니오 |
| 2026-09-22 | UCP Checker | UCP 선언 스토어 17,767곳 집계(제3자) | 1 | https://ucpchecker.com/blog/state-of-agentic-commerce-september-2026 | C | 아니오 |
| 2026-09-27 | 네이버 | 에이전트 내 결제 파일럿 연내 계획, 에이전트 지표(MAU·거래액 배수) 공개 | 3 | https://www.fnnews.com/news/202609270633124595 | B | 아니오 |
| 2026-09-29 | Amazon | Branded Conversations 발표(2027-01 미국 출시), Review Requests(2026-11) | 2 | https://advertising.amazon.com/library/news/branded-conversations-review-requests | A | 예 |
| 2026-09-30 | Mastercard | Agent Pay에 에이전트 개시 확률 점수·공유 신뢰 신호 추가(미국 테스트) | 2 | https://www.mastercard.com/us/en/news-and-trends/press/2026/september/new-trust-and-intelligence-services.html | A | 예 |
| 2026-09 | 은행 6곳·Stripe·Shopify | 은행 6곳 에이전틱 가이드라인(자율), Stripe 호스팅 체크아웃 에이전트 대응, Shopify 에이전트 체크아웃 기본 활성(전부 월 단위, 날짜 불명) | 2 | https://www.fintechweekly.com/magazine/articles/agentic-commerce-launch-month-liability-risk-2026 | C | 아니오 |
| 2026-10-05 | TikTok | Buy Direct(UCP 연동)와 Shopping Assistant 발표(광고주 대상 테스트) | 2 | https://pymnts.com/commerce/social-commerce/2026/tiktok-kicks-off-agentic-commerce-push-with-ai-shopping-assistant | B | 아니오 |
| 2026-10-06 | TechCrunch | 에이전트 접근 차단 현황 정리, Meta·Walmart·Stripe 등 에이전트-기업 통신 개방 표준 개발 중 | 2 | https://techcrunch.com/2026/10/06/the-next-hurdle-for-ai-agents-getting-websites-to-let-them-in | B | 아니오 |

## 3. 단정성 사실 점검

| 주장 | 최신 기준 확인 결과 | 출처 |
|---|---|---|
| "Rufus가 Amazon 쇼핑 Agent다" | 2026-05-13 Alexa+와 통합되어 "Alexa for Shopping"으로 개명. Rufus 명칭 단독 수치는 Q1(04-29)이 마지막 | https://s2.q4cdn.com/299287126/files/doc_earnings/2026/q2/earnings-result/AMZN-Q2-2026-Earnings-Release.pdf |
| "AI 에이전트의 사이트 접근을 막는 판결이 나왔다(Amazon 승)" | 03-09 가처분은 08-04 제9순회에서 파기·환송. 현재 법원 판단은 Perplexity 쪽(가처분 단계). 약관·계약 청구는 열려 있음 | https://www.cooley.com/news/insight/2026/2026-08-06-ninth-circuit-rules-on-ai-agent-access-to-third-party-websites-under-cfaa |
| "ChatGPT가 채팅 내 결제(Instant Checkout)를 제공한다" | 2026-03 중단 보도(2차). 가맹점 앱·자체 결제 방식으로 이동. OpenAI 원문 미확인 | https://webinterpret.com/en/blog/openai-abandons-instant-checkout |
| "ChatGPT 광고는 미국에서만" | 08-11 기준 영국·멕시코·브라질·일본·한국 추가, 08-31 기준 40개국 이상(2차) | https://openai.com/index/testing-ads-in-chatgpt/ |
| "Google은 Gemini에 광고가 없다" | 2025-12-08 "Gemini 앱에 광고 없음, 계획 없음" 부인. 2026-05 기준 AI Mode 광고는 테스트 중. 이후 Gemini 앱 내 광고 도입을 확인하는 1차 출처 못 찾음 | https://blog.google/products/ads-commerce/google-marketing-live-search-ads/ |
| "AI 답변 광고는 모두 도입하는 추세" | Perplexity는 광고 철수(02-18 보도) → 반례 | https://www.emarketer.com/content/perplexity-retreat-ads-marks-split-on-ai-monetization-models |
| "고객은 기업 챗봇을 쓴다/AI가 사람을 대체한다" | 기업 챗봇 이용은 2022년 이후 통계적 불변, 서드파티 GenAI 3배, 87%는 사람 연결 필수(Gartner) | 위 Gartner 두 릴리스 |
| "네이버가 에이전트 내 결제까지 제공" | 9월 27일 기준 연내 파일럿 '계획' 단계, 미출시 | https://www.fnnews.com/news/202609270633124595 |
| "카카오가 카카오톡에서 AI 결제 제공" | 카나나 인 카카오톡 화면 내 결제는 선물하기 연동(04월 말). 외부 파트너 결제는 단계적 도입 중, 쿠팡이츠가 첫 파트너(08-06). 완전 외부 연동 출시일 미확인 | https://www.etnews.com/20260513000299 |
| "Mastercard 첫 에이전트 거래" | 2025-10 CEO 발언으로 보도(2차). 이후 건수 공개 없음 | https://www.digitalcommerce360.com/2026/04/02/visa-mastercard-in-agentic-commerce/ |
| "Amazon이 외부 에이전트를 막는다" | 03 Perplexity 소송에 이어 09-20 Meta Muse 차단(반면 Walmart는 Muse 파트너로 개방) → 리테일러별 상반 | https://ppc.land/amazon-blocks-metas-muse-ai-agent-from-shopping-on-its-site/ |

## 4. 조사하지 못한 것 / 접근 불가 / 상충

조사하지 못한 것
- Visa Intelligent Commerce·Mastercard Agent Pay 참여사 총수, 에이전트 결제 거래 건수: 공식 수치 확인 못 함(T3 미충족).
- ACP 참여 가맹점 수 공식 집계, OpenAI 1차 발표(Instant Checkout 중단): 미확인.
- 월 단위 전용 검색은 1·2·4·6·9·10월만 수행. 3·5·7·8월은 주제별 검색에서 잡힌 사건만 수록(누락 가능).
- Amazon 2026-02 실적(Q4 2025) 원문, Q1 콜 녹취: 미열람(Rufus 300M·$12B·+115%는 2차).
- Forrester 수치(보고서 유료), Gartner 지역별 분포(릴리스에 미기재).
- 한국 카카오 Q1·Q2 콜 원문, 네이버 에이전트 절대 이용자 수(미공개), 쿠팡 에이전트 실적 지표(없음), 한국 소비자 AI 이용 설문.
- Amazon·Google·Meta 외 Microsoft Copilot Checkout, Anthropic·Perplexity 쇼핑 기능은 검색 결과만 확인, 본문 미열람.

접근 불가
- https://news.nate.com/view/20260508n22727 (ROBOTS_DISALLOWED)
- https://www.forrester.com/report/predictions-2026-customer-experience/RES185005 (유료 장벽, 요약만)
- https://www.cnn.com/2026/09/28/tech/meta-muse-ai-agents-amazon (ROBOTS_DISALLOWED)
- https://www.cnbc.com/2026/08/31/open-ai-chatgpt-ads-revenue.html, https://www.cnbc.com/2026/04/29/amazon-amzn-q1-earnings-report-2026.html (페치 오류)

출처 간 상충
- UCP 공동개발 수: Google 블로그(2026-01-11)는 5곳(Walmart 포함), 9to5google 기재는 4곳(Shopify·Etsy·Wayfair·Target, Walmart는 지지). 1차(Google) 기준 채택.
- ChatGPT 한국 광고 시점: JoongAng Daily는 2026-06-19 파일럿 시작, OpenAI 페이지는 2026-08-11 "launched" 및 05-07 확대 예고. 파일럿(06-19)과 본격 출시(08-11)의 차이일 가능성, 확정 못 함.
- Rufus 증분 매출: 2025-11 보도 "$10B 페이스"(제목 스니펫만) vs 2026-02 "약 $12B 연환산"(Modern Retail). 모두 2차.
- 네이버 에이전트 시작 시점: 2026-02-26 베타 보도(asiae) vs "3월 출시"(fnnews 9월 기사, 7월 기사의 '3월 대비'). 베타 02-26, 사용자 지표 기준점은 3월로 해석.
- Visa Intelligent Commerce Connect 릴리스 날짜 표기(04/08/2026) 모호(4월 8일 또는 8월 4일).
- Amazon Q2 광고 +26%: 릴리스는 +26%만 확인, "환율 제외" 조건은 2차 보도만 언급.
- 카나나 운영 기간: 1년 4개월(fnnews) vs 1년 5개월(newdaily). 종료일 10-15는 일치.
- Walmart 광고 성장률: 글로벌 +38%(VIZIO 포함) vs Walmart Connect 미국 +43%(VIZIO 제외)로 분모가 달라 혼용 금지.

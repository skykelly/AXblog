# C4 백지 재조사 (blind) — 조사일 2026-10-11

범례: 원문확인 "예" = WebFetch로 해당 URL을 열어 내용을 추출함(WebFetch는 모델 요약 방식이라 인용문 전체 대조는 아님). "아니오" = 검색 결과 제목만 확인했거나 열지 못함. 등급 A=1차/공식, B=언론·전문지, C=블로그·불명(판단 근거 아님).
제약: WebSearch 호출 상한(200회/턴) 소진으로 후반 검색이 막힘. 그 뒤로는 이미 확보한 URL만 WebFetch함. 4절 참조.

## 1. 지표별 최신값

| 지표ID | 값 | 단위 | 기준 시점 | 지역 | 측정 조건 | 출처 URL | 등급 | 원문확인 |
|---|---|---|---|---|---|---|---|---|
| C4-T1 Alexa+ | 출시 12개국: 미국, 영국, 캐나다, 멕시코, 이탈리아, 스페인, 독일, 오스트리아, 브라질, 프랑스, 호주, 인도. 인도는 9/16 얼리액세스 시작. 미국 월 $19.99(프라임 무료) | 상태 | 페이지 수정일 2026-09-16 (별도 페이지는 2026-07-21 갱신) | 글로벌 | 같은 페이지 안에서 국가 목록·메타 날짜가 서로 어긋남. 미국·캐나다는 "all customers", 나머지는 얼리액세스 | https://www.aboutamazon.com/news/devices/alexa-plus-international-launch , https://www.aboutamazon.com/news/devices/new-alexa-generative-artificial-intelligence | A | 예 |
| C4-T1 Gemini for Home | 얼리액세스 국가: 미국·캐나다(3/17)·멕시코(3/31)·16개국(4/7)·19개국 언어 옵트인(5/27)·독일(6/2)·러시아, 태국, 터키, 베트남 자동화 확대(8/5). 한국은 확인한 구간에 언급 없음 | 상태 | 2026-09-30 (최신 항목) | 글로벌, 한국 미확인 | 구글 도움말 "What's new" 앞 100,000자만 읽음. 2025년 말~2026-03 이전 항목은 읽지 못함 | https://support.google.com/googlehome/answer/15962877 | A | 예(부분) |
| C4-T1 Gemini for Home 16개국 | 16개국 10개 언어(미국 제외) | 개국 | I/O 2026 (기사일 2026-06-19) | 글로벌 | 위 도움말의 5/27 "19개 국가·언어"와 수치가 다름 | https://www.techinsights.com/blog/google-io-2026-gemini-home-takes-center-stage | B | 예 |
| C4-T1 LG 씽큐 온 | 2025-10-22 한국 출시, 출하가 246,000원, 생성형 AI 대화·Matter 인증·씽큐 플레이 약 800개 앱 서비스. 2026-08-31 에이전트 'ThinQ Claw' 시연(출시일·가격·국가 미공개) | 상태·원 | 2026-08-31 | 한국(출시), 유럽(IFA 시연) | 허브 가격은 LG 발표 기준. ThinQ Claw는 상용 일정 없음 | https://www.lg.co.kr/media/release/29491 , https://www.lg.com/global/newsroom/news/home-appliance-solution/lg-electronics-unveils-the-next-evolution-of-ai-home-at-ifa-2026/ | A | 예 |
| C4-T1 Apple | 홈 허브(HomePad)·homeOS는 WWDC(6/8)에서 개발자 프리뷰만. 제품은 10/13 "Welcome home" 이벤트 예정(Apple 확정은 일정뿐, 제품은 루머) | 상태 | 2026-10-09 | 글로벌 | 오늘(10/11) 기준 미출시 | https://www.notebookcheck.net/Welcome-home-Apple-event-on-October-13-2026.1419459.0.html , https://appleinsider.com/articles/26/10/08/what-to-expect-from-apples-october-13-welcome-home-releases | B | 예 |
| C4-T2 SmartThings | 글로벌 가입자 4억6천만 명 초과(2026-05 기준), 등록 가전 3,300만 대(2025-11), 한국 등록 기기 2,000만 대 초과(2025-12), WWST 파트너 390곳 이상·기기 4,700종 이상 | 명·대 | 2026-09-01 기사 | 글로벌, 한국 | 삼성 직접 발표가 아닌 언론 인용. 가입자(계정)와 기기(대) 단위가 다름 | https://www.asiatoday.co.kr/kn/view.php?key=20260902010000527 | B | 예 |
| C4-T2 Alexa | 전 세계 Alexa 기기 6억 대 이상. Alexa+ 호환은 "수만 개 서비스·기기"로만 표기(구체 수치 없음) | 대 | 2026-07-21 갱신 | 글로벌 | Alexa+ 전용 가입자 수는 미공개. 6억 대는 Alexa 전체 기준 | https://www.aboutamazon.com/news/devices/new-alexa-generative-artificial-intelligence | A | 예 |
| C4-T2 Alexa 이용 | "새 Alexa 경험을 쓰는 고객 수억 명", Alexa for Shopping 지난 12개월 3.5억 명 이상 | 명 | 2026 Q2 실적 콜(2026-08-07 게시) | 글로벌 | Alexa+ 단독 수치 아님 | https://www.fool.com/earnings/call-transcripts/2026/08/07/amazon-amzn-q2-2026-earnings-call-transcript/ | B | 예 |
| C4-T3 1X NEO | $20,000 구매 또는 월 $499, 보증금 $200. 2026-10-05 기준 고객 인도 확인 못 함. 예약 수 미공개. 어려운 작업은 1X 직원이 원격 지원 | 달러·대 | 2026-10-05 (2차), MIT TR 2026-10-08 | 미국 | 가격·정책은 제3자 사이트(botinfo)가 1X 페이지를 확인했다고 인용. 1X 원문은 접근 시도했으나 권한 응답 지연으로 열지 못함 | https://botinfo.ai/articles/1x-neo-home-robot , https://technologyreview.com/2026/10/08/1145923/ai-breakthroughs-in-robotics-wont-change-your-life-any-time-soon | C / B | 예(2차) |
| C4-T3 삼성 Ballie | 2025년 여름 출시 약속을 넘김. 2026-05-20 기준 판매 일정·리테일 목록 없음 | 상태 | 2026-05-20 | 글로벌 | 이후(6~10월) 상태는 확인 못 함 | https://the-gadgeteer.com/2026/05/20/home-robots-available-2026/ , https://www.t3.com/home-living/smart-home/samsungs-ballie-home-companion-robot-has-been-delayed-yet-again | B | 예 |
| C4-T3 LG CLOiD | 가격·출시일 없음. LG CFO는 2026 상반기 실증 시작, 2028년 홈로봇 상용화 기반 마련을 목표로 언급 | 상태 | 2026-04-29 | 한국·글로벌 | 업계 보도 기반 | https://www.lg.com/us/newsroom/home-appliance/lg-cloid-home-robot , https://news.bizwatch.co.kr/article/industry/2026/04/29/0044 | A / B | 예 |
| C4-T3 시장 전반 | 2025년 휴머노이드 출하 약 15,000대 중 중국 기업 약 90%. Unitree 일부 모델 $6,000 미만. 머스크는 Optimus 일반 판매를 2027년 말로 제시 | 대·달러 | 2026-10-08 | 글로벌 | 가정용 한정이 아니라 휴머노이드 전체 | https://technologyreview.com/2026/10/08/1145923/ai-breakthroughs-in-robotics-wont-change-your-life-any-time-soon | B | 예 |
| C4-T4 오픈서베이 | AI 주방가전 경험 39.1%(전년 대비 +6.6%p), AI 생활가전 경험 51%, 냉장고 49.5%, TV 40.1% | % | 조사 2026-03-11~12, 게시 03-30 | 한국 | 20~64세 1,500명 중 가전 구매 결정자·AI 가전 구매의향자 1,000명. 경험률은 AI 기능을 써 본 비율 | https://blog.opensurvey.co.kr/article/ai-home-appliance-2026-2/ , https://blog.opensurvey.co.kr/trendreport/ai-home-appliance-2026/ | A | 예 |
| C4-T4 오픈서베이 2025 | AI 가전 실제 이용 약 10%, 동일 가격이면 AI 탑재 선택 8/10 | % | 조사 2025-05-16~21 | 한국 | 20~59세 1,500명 + 관심자 1,000명. 정의·모집단이 2026과 달라 직접 비교 금지 | https://blog.opensurvey.co.kr/trendreport/ai-home-appliance-2025/ | A | 예 |
| C4-T4 Criteo | 한국 구매자 53%가 AI 챗봇·어시스턴트 이용(글로벌 48%), 이용자의 58%가 구매에 영향 받음 | % | 2026-10-08 발표 | 한국, 글로벌 | 가전 구매 탐색 중 AI 이용. AI 가전 기능 경험률이 아님. 글로벌 6,200명 이상(한국 표본 미공개) | https://www.tech42.co.kr/%EA%B0%80%EC%A0%84-%EA%B5%AC%EB%A7%A4%EC%97%90%EB%8F%84-ai-%ED%99%9C%EC%9A%A9-%ED%99%95%EC%82%B0-%ED%95%9C%EA%B5%AD-%EC%86%8C%EB%B9%84%EC%9E%90-53-ai-%EC%9D%B4%EC%9A%A9%ED%95%98%EC%A7%80/ | B | 예 |
| C4-T5 오픈서베이 | 신중 수용자 비중 상승(+6.0%p), 긍정 소비자를 처음 추월. 신중 수용자 45.7%는 한경 인용. 'AI가 스스로 판단해 불편' 문항 값은 찾지 못함 | % | 2026-03 | 한국 | 구매의향자 1,000명. 45.7%는 2차 인용이고 오픈서베이 원문 페이지에서는 미확인 | https://blog.opensurvey.co.kr/article/ai-home-appliance-2026-2/ , https://www.hankyung.com/article/202607107666g | A / B | 예 |
| C4-T5 Prosper(미국) | AI가 스마트홈을 관리하게 하겠다 10.0%, 식료품 구매 11.0%, 일상 업무 하나라도 맡기겠다 40.1%, AI 에이전트가 좋은 생각 17.6% | % | 2026-06 조사 | 미국 | 18세 이상 7,675명, Prosper Insights(Channel V Media 보고서) | https://www.businesswire.com/news/home/20261008533804/en/AI-Is-the-First-Channel-to-Act-on-Consumers-Behalf-40-of-Americans-Would-Let-It-But-Only-18-Think-Its-a-Good-Idea | A(원문 보도자료) | 예 |
| C4-T5 Ping Identity | 승인 하에 AI가 행동해도 편안 5%, 승인 없는 일상 거래 3%, 추천·지원은 56% 편안 | % | 2026-10-06 발표 | 12개국 | 11,000명(Talker Research), 스마트홈 한정 아님. 벤더 의뢰 조사 | https://press.pingidentity.com/2026-10-06-Ping-Identity-Survey-Finds-AI-Trust-Changes-When-Assistance-Turns-to-Action | A(벤더) | 예 |
| C4-T5 Prophet | 자율 에이전트를 도움이 된다고 본 비율 54%, 환경형 AI가 먼저 도와주길 원함 62% | % | 조사 2026-01~02 | 중국·독일·싱가포르·미국·영국 | 생성형 AI 개인 이용자 2,015명. 가전이 아닌 일반 소비 | https://prophet.com/2026/04/the-2026-ai-powered-consumer-report/ | B | 예 |
| C4-T6 Parks Associates | AI의 데이터 보안·프라이버시 우려 72%, 사회가 AI를 책임 있게 쓸 능력 의심 71% | % | 2026-04-30 발표 | 미국 | 미국 인터넷 가구 8,000, 스마트홈 한정 아님. 2024년 값은 69% | https://www.prnewswire.com/news-releases/industry-leaders-at-30th-annual-connections-the-connected-home-conference-address-ai-data-security-and-trusted-smart-home-experiences-302758267.html | A | 예 |
| C4-T6 Prosper | AI의 프라이버시 침해를 매우·극도로 우려 60.5% | % | 2026-06 | 미국 | 위 Prosper 조건 동일 | 위 businesswire URL | A | 예 |
| C4-T6 오픈서베이 | 개인정보 유출 우려 +6.9%(전년 대비 변화만 게시). 전체 우려 45.1%→52.2%, 경험자 47.5%→55.4% | % | 2026-03 | 한국 | 절대 수준은 개인정보 문항으로 공개되지 않음 | https://blog.opensurvey.co.kr/article/ai-home-appliance-2026-2/ | A | 예 |
| C4-T7 Matter | CSA 공식 인증 제품 총수는 찾지 못함. 참고: mattercatalog "미국 판매 Matter 제품 1,071개"(최신 인증일 2026-10-02) | 개 | 2026-10 | 미국 판매분 | CSA 인증 총수가 아님. CSA 제품 검색 페이지는 총수 표시 없음(pagination 1692쪽만 확인) | https://mattercatalog.com/new , https://csa-iot.org/csa-iot_products/ | C / A | 예 |
| C4-T7 Matter 버전 | 1.5 (2025-11-20), 1.5.1 (2026-03-31), 1.6 (2026-06-17: NFC 설정, Joint Fabric, Thermostat Suggestions 등) | 버전 | 2026-06-17 | 글로벌 | 버전 날짜는 위키 표(CSA 보도 인용), 1.6 기능은 Privacy Guides 기사 | https://www.privacyguides.org/news/2026/06/19/connectivity-standards-alliance-releases-matter-1-6-and-product-security-1-1-specifications/ , https://en.wikipedia.org/wiki/Matter_(standard) | B | 예 |
| C4-T8 AI 가전 판매 비중 | 찾지 못함 (삼성·LG의 AI 탑재 판매 비중 공개값 미확인) | % | - | - | 한경(7/10)·비즈니스워치(4/29)·스펙분석소 모두 해당 수치 없음 | - | - | 아니오 |

## 2. 사건 목록 (월별)

| 날짜 | 주체 | 사실 | 중요도 | 출처 URL | 등급 | 원문확인 |
|---|---|---|---|---|---|---|
| 2025-10-22 (참고, 기간 전) | LG전자 | 생성형 AI 홈 허브 '씽큐 온' 한국 출시, 246,000원 | 3 | https://www.lg.co.kr/media/release/29491 | A | 예 |
| 2026-01-04 | LG전자 | CES에서 홈 로봇 CLOiD 공개(세탁 시작, 빨래 개기, 냉장고에서 우유 꺼내기 데모). 가격·출시일 없음 | 3 | https://www.lg.com/us/newsroom/home-appliance/lg-cloid-home-robot | A | 예 |
| 2026-01-04 | 삼성전자 | CES에서 '홈 컴패니언' 콘셉트 발표(AI 냉장고·로봇청소기·AI 콤보). 출시 시기·가격 없음 | 2 | https://news.samsung.com/kr/ces-2026-%EB%B3%B4%EA%B3%A0-%EB%93%A3%EA%B3%A0-%EB%A7%90%ED%95%98%EB%8A%94-%EA%B0%80%EC%A0%84-%EC%82%BC%EC%84%B1-%ED%99%88-%EC%BB%B4%ED%8C%A8%EB%8B%88%EC%96%B8 | A | 예 |
| 2026-01 | SwitchBot | CES에서 휴머노이드 Onero H1 시연(데모 외 성능 미검증) | 1 | https://www.pymnts.com/artificial-intelligence-2/2026/at-ces-2026-domestic-robots-reappear-as-practical-ambitions-grow | B | 예 |
| 2026-01 | 삼성전자 | Ballie, CES 2026 불참(2026-05 기사 기준) | 2 | https://the-gadgeteer.com/2026/05/20/home-robots-available-2026/ | B | 예 |
| 2026-01 | 한국 | AI 기본법 시행(2026-01-22 추정) 관련 검색은 시도했으나 검색 상한으로 못 함 | - | - | - | 아니오 |
| 2026-02-05 | Amazon | Alexa+ 미국 전체 개방(얼리액세스 종료) 보도 | 3 | https://www.t3.com/tech/ai/alexa-plus-is-now-available-to-everyone-in-the-us-but-whens-it-coming-to-the-uk-too | B | 예 |
| 2026-02-10 | LG전자 | 북미 B2B용 ThinQ Pro를 KBIS(2/17~19)에 공개 | 1 | https://finance.yahoo.com/news/lg-electronics-debuts-lg-thinq-010300071.html | A | 예 |
| 2026-02 (월말) | SwitchBot | AI Hub 출시(OpenClaw 지원, 카메라 기반 요약·알림) | 1 | https://www.t3.com/home-living/smart-home/smart-home-launches-february-2026 | B | 예 |
| 2026-03-11~12 | 오픈서베이 | 한국 AI 가전 트렌드 조사 실시(3/30 게시) | 2 | https://blog.opensurvey.co.kr/trendreport/ai-home-appliance-2026/ | A | 예 |
| 2026-03-17 | Google | Gemini for Home 캐나다 추가 | 2 | https://support.google.com/googlehome/answer/15962877 | A | 예 |
| 2026-03-19 | Amazon | Alexa+ 영국 얼리액세스 시작 | 2 | https://servola.de/journal/five-markets-got-alexa-plus-first-us-graduates-first/ | C | 예 |
| 2026-03-31 | Google, CSA | Gemini for Home 멕시코 추가. Matter 1.5.1 공개 | 2 | https://support.google.com/googlehome/answer/15962877 , https://en.wikipedia.org/wiki/Matter_(standard) | A / B | 예 |
| 2026-04-07~08 | Google | Gemini for Home 16개국 확대(유럽 13, 호주·일본·뉴질랜드), 지연 최대 40% 감소 | 3 | https://9to5google.com/2026/04/08/google-home-expands-gemini-access-globally-as-the-assistant-replacement-improves/ | B | 예 |
| 2026-04-15, 04-23 | Amazon | Alexa+ 이탈리아·스페인 얼리액세스 | 1 | https://servola.de/journal/five-markets-got-alexa-plus-first-us-graduates-first/ | C | 예 |
| 2026-04-21 | 삼성전자 | SmartThings, IKEA Matter 기기 통합 확대(헤드라인만 확인) | 1 | https://news.samsung.com/global/category/corporate/technology | A | 예(목록만) |
| 2026-04-29 | LG전자 | 1분기 콘퍼런스콜: 홈로봇 실증 올해 시작, 2028 상용화 기반 | 2 | https://news.bizwatch.co.kr/article/industry/2026/04/29/0044 | B | 예 |
| 2026-04-30 | Parks Associates | 미국 8,000가구 조사: 생성형 AI 사용 58%(2024년 40%), 프라이버시 우려 72% | 2 | (1절 C4-T6 URL) | A | 예 |
| 2026-05-03 | Google | Gemini for Home 유럽·APAC 확대 이어짐 | 1 | https://9to5google.com/2026/05/03/google-home-gemini-europe-asia-pacific-broader-rollout/ | B | 예 |
| 2026-05-05 | Google | Gemini 3.1 적용, 한 문장 다단계 요청 가능 | 2 | https://support.google.com/googlehome/answer/15962877 | A | 예 |
| 2026-05-07, 05-26 | Amazon | Alexa+ 독일(5/7), 프랑스(5/26) 얼리액세스 시작(기사별 날짜 상이: 프랑스는 6/4 행사 보도도 있음) | 1 | https://servola.de/journal/five-markets-got-alexa-plus-first-us-graduates-first/ | C | 예 |
| 2026-05-19 | Google | I/O에서 Gemini for Home 중심, 신규 하드웨어 없음(Gemini Built-In 레퍼런스 설계 스피커까지 확대) | 2 | https://www.techinsights.com/blog/google-io-2026-gemini-home-takes-center-stage | B | 예 |
| 2026-05-20 | The Gadgeteer | 홈 로봇 중 실제 구매 가능한 것은 NEO(예약), Astro 등. 빨래·설거지는 실가정에서 자율 수행 드묾 | 2 | https://the-gadgeteer.com/2026/05/20/home-robots-available-2026/ | B | 예 |
| 2026-05-27 | Google | 기존 사용자 19개 국가·언어 옵트인, 카메라 이벤트 기반 자동화 시작점 | 2 | https://support.google.com/googlehome/answer/15962877 | A | 예 |
| 2026-06-02 | Google | Gemini for Home 독일 얼리액세스 | 1 | 위와 동일 | A | 예 |
| 2026-06-04 | Amazon | 런던 행사에서 Alexa+ 프랑스 추가 | 1 | https://eftm.com/2026/06/alexa-rolls-out-to-more-countries-but-australia-has-to-wait-till-2027-276635 | B | 예 |
| 2026-06-08 | Apple | WWDC: homeOS 개발자 프리뷰, Gemini 기반 Siri 재구성(허브 하드웨어는 미공개) | 3 | https://www.techtimes.com/articles/317985/20260608/apple-wwdc-2026-siri-rebuilt-gemini-homeos-previewed-cook-farewell-keynote.htm | B | 예 |
| 2026-06 | Prosper | 미국 7,675명 조사 실시(AI에 스마트홈 관리 맡김 10.0%) | 2 | (1절 C4-T5 URL) | A | 예 |
| 2026-06-17 | CSA | Matter 1.6 공개 | 2 | https://www.privacyguides.org/news/2026/06/19/connectivity-standards-alliance-releases-matter-1-6-and-product-security-1-1-specifications/ | B | 예 |
| 2026-07-10 | 한국경제 | 스마트홈 가전 시장 전망 기사(판매 비중 수치 없음). 오픈서베이 신중 수용자 45.7% 인용 | 1 | https://www.hankyung.com/article/202607107666g | B | 예 |
| 2026-07-23 | Google | 1세대 Google Home Mini·Nest Hub에도 Gemini Live(프리미엄) | 1 | https://support.google.com/googlehome/answer/15962877 | A | 예 |
| 2026-08-05 | Google | 러시아·태국·터키·베트남에 자동화 확대(Gemini 홈은 이 국가들 얼리액세스에 해당 여부 도움말 문맥상 불명) | 1 | 위와 동일 | A | 예 |
| 2026-08-06~07 | Amazon | Q2 실적: Alexa+ 독일·오스트리아·프랑스·브라질 확대, Alexa+ 써 본 고객의 프라임 가입률 약 25% 높음. 호주 시작은 aboutamazon 페이지에 8/6 | 2 | https://www.fool.com/earnings/call-transcripts/2026/08/07/amazon-amzn-q2-2026-earnings-call-transcript/ | B | 예 |
| 2026-08-31 | LG전자 | IFA 전 ThinQ Claw 공개(채팅형 에이전트, 가전·캘린더 연동, 선호 기억) | 3 | https://www.lg.com/global/newsroom/news/home-appliance-solution/lg-electronics-unveils-the-next-evolution-of-ai-home-at-ifa-2026/ | A | 예 |
| 2026-09-01 | 삼성 SmartThings | 가입자 4.6억, 한국 2,000만 대 등 수치 인용 기사. API 유료화 검토는 업계 전언 | 2 | https://www.asiatoday.co.kr/kn/view.php?key=20260902010000527 | B | 예 |
| 2026-09-02~08 | IFA 2026 | 1,900여 브랜드·49개국. 중국 기업 932곳(전년 691곳). 주제는 AI 홈과 피지컬 AI. 샤오미 첫 메인홀, 삼성 AI 리빙, 로보락·에코백스·드리미 AI 자율주행 | 3 | https://www.seoul.co.kr/news/economy/industry/2026/09/04/20260904500242 , https://www.koreaherald.com/article/10860301 | B | 예 |
| 2026-09-03 | LG전자 | IFA에서 ThinQ ON 차세대 허브 중심 AI 홈, CLOiD 전시, Homey 기반 HEMS(5만 개 이상 IoT 기기 연결), ThinQ Pro 유럽 데뷔 | 2 | https://www.nextdaily.co.kr/news/articleView.html?idxno=252750 | B | 예 |
| 2026-09-16 | Google | Google Home MCP 얼리액세스(개인 에이전트가 기기·이벤트 기록 접근) | 3 | https://support.google.com/googlehome/answer/15962877 | A | 예 |
| 2026-09-16 | Amazon | Alexa+ 인도 얼리액세스 시작(영어·힌디·힝글리시) | 2 | https://www.aboutamazon.com/news/devices/alexa-plus-international-launch | A | 예 |
| 2026-09-19 | Ynet | 홈은 아직 스스로 돌아가지 않는다는 분석(로보락 Saros Z70 로봇팔 등). 통계 없음 | 1 | https://www.ynetnews.com/tech-and-digital/article/hkugjlofzx | B | 예 |
| 2026-09-30 | Google | 배경 대화 필터링, 3개 언어 가구 처리 개선 | 1 | https://support.google.com/googlehome/answer/15962877 | A | 예 |
| 2026-10-06 | 삼성전자 | "SmartThings Now" 플랫폼 업데이트 보도자료(제목만 확인, 내용 미확인) | 2 | https://news.samsung.com/global/category/corporate/technology | A | 아니오(제목만) |
| 2026-10-06 | Ping Identity | 12개국 11,000명: 승인 하 AI 행동 5%, 승인 없는 거래 3% | 2 | https://press.pingidentity.com/2026-10-06-Ping-Identity-Survey-Finds-AI-Trust-Changes-When-Assistance-Turns-to-Action | A(벤더) | 예 |
| 2026-10-08 | Criteo | 한국 가전 구매자 AI 이용 53%, 최종 선택은 직접 | 1 | (1절 C4-T4 Criteo URL) | B | 예 |
| 2026-10-08 | MIT Tech Review | 홈 로봇 실사용까지 "10년"(Agility), NEO는 원격 조작 필요 | 2 | https://technologyreview.com/2026/10/08/1145923/ai-breakthroughs-in-robotics-wont-change-your-life-any-time-soon | B | 예 |
| 2026-10-09 | Qubo(인도) | 인도 스마트홈 보급률 2% 미만(회사 추정), 허브보다 AI 기기 중심 | 1 | https://business-standard.com/technology/tech-news/imc-2026-why-qubo-sees-india-s-smart-home-future-in-ai-devices-not-hubs-126100900572_1.html | B | 예 |
| 2026-10-13 (예정) | Apple | "Welcome home" 이벤트. 허브·HomePod mini·Apple TV·LG 협업 액세서리는 루머 | 3 | https://appleinsider.com/articles/26/10/08/what-to-expect-from-apples-october-13-welcome-home-releases | B | 예 |

## 3. 단정성 사실 점검

| 주장 | 최신 기준 확인 결과 | 출처 |
|---|---|---|
| "Alexa+는 미국에서 전체 개방" | 2/5 보도와 aboutamazon 페이지("all customers in the U.S. and Canada")는 일치. 한 블로그(servola)는 "9/1 얼리액세스 종료"라 적어 충돌. 후자는 C등급이라 채택 안 함 | https://www.t3.com/tech/ai/alexa-plus-is-now-available-to-everyone-in-the-us-but-whens-it-coming-to-the-uk-too , https://www.aboutamazon.com/news/devices/new-alexa-generative-artificial-intelligence |
| "Gemini for Home 16개국" | 4/7 시점은 16개국이나 5/27에 19개 국가·언어, 8/5에 4개국 자동화 추가. I/O 기사(6/19)는 16개국이라 상충. "16개국"은 최신 수치가 아님 | https://support.google.com/googlehome/answer/15962877 |
| "한국에서 Gemini for Home·Alexa+ 사용 가능" | 확인한 구간에서 한국 언급 없음. "없다"를 단정할 근거도 부족. 확인 필요 | 위 두 URL |
| "삼성 Ballie 출시" | 2026-05-20 기준 일정·판매처 없음. 이후 변화는 미확인 | https://the-gadgeteer.com/2026/05/20/home-robots-available-2026/ |
| "1X NEO 판매/출하 중" | 선주문과 가격만 확인. 인도 확인된 바 없음(10/5 2차, 10/8 MIT TR "later in 2026"). 원격 조작 필요 | https://technologyreview.com/2026/10/08/1145923/ai-breakthroughs-in-robotics-wont-change-your-life-any-time-soon |
| "Apple 홈 허브 출시" | 10/11 기준 미출시. 10/13 이벤트는 확정, 제품은 루머 | https://www.notebookcheck.net/Welcome-home-Apple-event-on-October-13-2026.1419459.0.html |
| "한국 AI 가전 사용 경험이 다수" | 오픈서베이 2026: 주방 39.1%, 생활 51%는 구매의향자 모집단. 일반 인구 수치 아님 | https://blog.opensurvey.co.kr/article/ai-home-appliance-2026-2/ |
| "신중 수용자가 긍정 소비자를 처음 추월" | 오픈서베이 페이지 문구("for the first time"). 이 시리즈 안의 비교이며 다른 조사와 무관 | https://blog.opensurvey.co.kr/trendreport/ai-home-appliance-2026/ |
| "중국이 휴머노이드 출하 90%" | MIT TR 인용(2025년 약 15,000대). 원자료(조사기관) 미확인 | https://technologyreview.com/2026/10/08/1145923/ai-breakthroughs-in-robotics-wont-change-your-life-any-time-soon |
| "ThinQ ON은 한국 최초의 생성형 AI 홈 허브" 류 | 이 표현 자체를 검증하지 못함(삼성 허브 비교 불가) | - |

## 4. 조사하지 못한 것, 접근 불가, 상충

- 검색 상한: WebSearch 200회/턴 상한이 소진되어 이후 검색이 막힘. 그 결과 미조사: 한국 AI 기본법 시행·개인정보위 가이드, Samsung·LG의 AI 가전 판매 비중(C4-T8), Gemini for Home 한국 출시 여부, SwitchBot·Roborock·Dreame 등 가정용 로봇 판매량·가격, Matter CSA 인증 총수, Parks Associates 스마트홈 허브 보급률 최신값, 월별 점검 중 8월·10월 사건 일부.
- 접근 불가: https://www.1x.tech/order (권한 응답 시간 초과로 취소, 1X 1차 원문 미확인). https://www.technology.org/2026/07/18/... (ROBOTS_DISALLOWED, 우회 안 함). samsungmagazine.eu 페이지는 본문이 비어 있었음.
- 원문 미확인(제목·목록만): Samsung SmartThings Now(10/6), SmartThings IKEA Matter(4/21), Google I/O 9to5google 기사(홈 관련 내용 없음), Google 도움말 "What's new"의 2026-03 이전 구간.
- 상충: (1) Gemini for Home 16개국 vs 19개국·언어. 같은 기사 안에서 언어 10개 vs 7개 신규. (2) Alexa+ 미국 개방 시점: 2/5 vs 9/1. (3) Alexa+ 호주: aboutamazon에 8/6 제공과 기사 slug의 2027 대기. (4) aboutamazon 인도 페이지 게시일 3/19와 수정일 9/16. (5) Matter 제품 수: mattercatalog 1,071(미국 판매분), matter-smarthome.de 750+(2026-01, 등록 기준, C), yourmatterhome 350+(2026-03, C), 스펙분석소 약 4,500(2025년 말, 출처 불명, C). 정의가 달라 합산·비교 금지. (6) 오픈서베이 개인정보 유출 우려 "+6.9%" vs 전체 우려 45.1→52.2(+7.1%p)는 다른 문항.
- 한계: WebFetch는 요약형이라 수치는 추출 결과 그대로이며 원문 PDF 직접 대조는 하지 않음. 오픈서베이 'AI가 스스로 판단해 불편' 문항 수치는 확인하지 못함.

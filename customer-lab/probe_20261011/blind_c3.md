# C3 백지 재조사 (검증용) — 2026-10-11

범위: 2026-01-01~2026-10-11. 조사 도중 WebSearch 한도(턴당 200회, 공유)가 소진되어 이후에는 이미 확보한 URL의 WebFetch만 사용함. 아래 "4. 조사하지 못한 것" 참조.
등급 A=1차/원자료/공식, B=언론·2차·업체 자체 연구, C=블로그·출처불명(판단 근거 제외).

## 1. 지표별 최신값

| 지표ID | 값 | 단위 | 기준 시점 | 지역 | 측정 조건 | 출처 URL | 등급 | 원문확인 |
|---|---|---|---|---|---|---|---|---|
| C3-T1 | 49.9 (Q4 2025: 50.9, Q1 2025: 49.6; 챗GPT 출시 후 12개월 35.9, 24개월 48) | % | 2026 Q1 (발표 2026-05-15) | 글로벌(영문) | Common Crawl 영문 URL 55.4k개 무작위, 100단어 이상 기사·리스티클, 탐지기 3종(Pangram·Copyleaks·GPTZero) 분기별 평균, "주로 AI" 이진 분류, 위양성 1.36~1.84%. 2025-10 1차 연구 대비 방법 변경으로 추정치 평균 3.3%p 낮아짐. 2025 초부터 약 50% 정체 | https://graphite.io/five-percent/research/ai-now-writes-as-many-online-articles-as-humans-do | A(업체 자체 연구, 방법론 공개) | 예 |
| C3-T1 | 위와 동일(Axios 보도) | % | 2026-05-15 보도 | 글로벌(영문) | 위와 동일 | https://www.axios.com/2026/05/15/human-vs-ai-written-articles | B | 예 |
| C3-T2 | 3 | % | 발표 2026-05-04 (조사 시기 미기재) | 미국 Amazon | 베스트셀러 500개 상품(10개 카테고리) 첫 페이지 리뷰 30,000건, Pangram 3.2, "high confidence" AI 생성 909건. AI 리뷰의 5점 비율 74% vs 사람 59%, 93%가 Verified Purchase | https://www.pangram.com/blog/ai-amazon-reviews | A(탐지 업체 자체 연구) | 예 |
| C3-T2 | AI 50% 이상 포함 리뷰 연평균 2022년 2%, 챗GPT 이후 "약 400% 증가" | % | 발표 2025-11-17 (2026 이전, 참고) | Amazon | 26,000건 중 2,000건 분석, Originality.ai API. 400%가 2%에서의 증가율인지 현재값 약 10%인지 페이지에 불명확, 현재 비중 확정 불가 | https://originality.ai/blog/amazon-ai-generated-reviews | A(업체 자체) | 예(현재값 불명확) |
| C3-T2 | Amazon "수억 건의 가짜 리뷰를 게재 전 차단"(2025년), 정확 수치 없음 | 건 | 2025년, 보고서 2026-04-23 | 글로벌 Amazon | Amazon Trustworthy Shopping Experience Report 첫 발간. AI 기반 탐지 | https://claypier.com/en/amazon-trustworthy-shopping-report-2026/ | C(2차 블로그) | 아니오(Amazon 원문 미확인) |
| C3-T3 | AI 챗봇 뉴스 주간 이용 10 (전년 7). 35세 미만 16, 18~24세 17(Decoder 인용), 한국 14(약 2배) | % | DNR 2026, 발표 2026-06-16, 필드워크 2026-01 중순~02 말(YouGov) | 글로벌 48개 시장(전체 응답 97,520), 한국 | "독립형 AI 챗봇의 의도적 뉴스 탐색 이용". AI Mode·AI Overviews 제외. 영국 4%로 최저 | https://reutersinstitute.politics.ox.ac.uk/digital-news-report/2026/dnr-executive-summary | A | 예(요약 페이지 전체, 본 보고서 세부 챕터 미확인) |
| C3-T3 | AI 챗봇 뉴스 신뢰 20 (뉴스 전반 37; 이용자 44, 비이용자 17; 영국 6) | % | 동일 | 글로벌(45개 시장 기준 유스케이스) | 신뢰 수치는 Decoder 인용(2차). 이용 용도: 후속질문 42, 최신뉴스 35, 요약 34 | https://the-decoder.com/more-people-get-news-from-ai-chatbots-but-trust-remains-low/ | B | 신뢰 20%는 요약 페이지에도 있음(예). 이용자/비이용자 분해는 2차 |
| C3-T3 | 미국 13 (Pew) 챗봇을 뉴스에 이용; 챗봇 이용 49(2024년 33) | % | 필드워크 2026-02-17~23, 발표 2026-06-17 | 미국 성인 5,119명 | American Trends Panel | https://www.pewresearch.org/internet/2026/06/17/americans-and-ai-2026-chatbots-smart-devices-and-views-on-impact/ | A | 예 |
| C3-T4 | Google 검색 유입 -40.2% YoY (전년 -21.9%); Google 검색 비중 9%(2024-07)→5%(2026-07); Discover -34.3% YoY; AI 유입 0.01% | % | 2025-07~2026-07, 보도 2026-09-24 | Chartbeat 네트워크(뉴스·미디어 편중, 월 약 311억 PV) | 페이지뷰 수 vs 채널 비중 구분 불명(SEJ 지적). Chartbeat 원문은 다운로드 폼 뒤 | https://www.searchenginejournal.com/google-search-decline-publishers-chartbeat/590681/ | B | 예(SEJ), Chartbeat 원문 미확인 |
| C3-T4 | Google 검색 PV -34%, Discover -15/-16% (2024-12→2025-12); 챗봇 유입 1% 미만(ChatGPT +200% 이상); 소형(일 1천~1만PV) -60%, 중형 -47%, 대형 -22% (2년) | % | 보도 2026-03-17/18 | Chartbeat 글로벌 퍼블리셔 | AI 유입 0.7%(Nieman Lab 자체 산출). 전체 PV 2025 약 -6% | https://www.axios.com/2026/03/17/chartbeat-search-traffic-ai-chatbots ; https://www.niemanlab.org/2026/03/ai-sources-like-chatgpt-account-for-less-than-1-of-publishers-pageviews-chartbeat-says/ | B | 예 |
| C3-T4 | AI 챗봇에서 원문 클릭("항상/자주"): 4 (검색 19, 소셜 17) vs 42 (챗봇 이용자 대상, 한국 56 최고, 덴마크 26) | % | DNR 2026 | 27개 시장 / 이용자 | 두 수치가 상충(4절 참조). 분모가 다름(4%는 Decoder 표기, 42%는 요약 페이지 표기) | 위 DNR·Decoder URL | A/B | 부분 |
| C3-T5 | Ahrefs Brand Radar 2026-09 Google AI Mode(US) 언급 점유율: reddit 17.9, youtube 17.8, google 12.5, facebook 10.2, instagram 5.7, wikipedia 4.0, quora 3.0, amazon 3.0, tiktok 2.7, walmart 1.5 | % (순위) | 2026-09 | 미국, 전 주제 | 분모=상위 소스 합계(전체 인용 아님), 표본 수 미기재, 페이지가 AI 에이전트가 월간 자동 생성, 메타태그(Wikipedia 1위 등)와 표가 상충 | https://ahrefs.com/blog/most-cited-domains-ai-mode/ | B(업체, 방법 불투명) | 예 |
| C3-T5 | 2026-07 Ahrefs(2차 재인용): ChatGPT 1위 reddit 16.7, wikipedia 8.9, forbes 3.3 / AI Overviews 1위 youtube 21.1, reddit 18.5 / Perplexity 1위 youtube 31.2, reddit 13.9 / AI Mode 1위 reddit 19.9 | % | 2026-07 | 미국 | 2차 페이지의 재인용, Ahrefs 원본 대조 못함. 엔진별로 1위가 다름 | https://obsurfable.com/resources/reports/top-domains-cited-by-llms-august-2026 | C | 예(페이지), 원본 미확인 |
| C3-T5 | Peec AI 3,000만 소스: reddit, youtube, linkedin, wikipedia, forbes, g2, yelp, facebook, medium, techradar (순위만) | 순위 | 2026-03 스냅샷(발표 03-31) | 미국, 5개 AI 플랫폼 | 점유율·기간 미기재 | https://peec.ai/blog/top-domains-cited-by-ai-search-analysis-based-on-30m-sources | A(측정 업체) | 예 |
| C3-T5 | Profound 6.8억 인용: ChatGPT 위키 7.8, reddit 1.8; AIO reddit 2.2, youtube 1.9; Perplexity reddit 6.6 | % | 2024-08~2025-06 (구기간, 참고) | 글로벌/미국 불명 | 최신 아님. 브랜드명 단위 | https://www.tryprofound.com/blog/ai-platform-citation-patterns | A | 예 |
| C3-T6 | AI 광고에 긍정(매우/다소) 45; 부정 Gen Z 39(2024: 21), 밀레니얼 20(15); 중립 약 1/4(34); AI 광고 본 적 있다 71(54); 광고주 82%가 소비자가 긍정이라 믿음 → 격차 37p(32p) | % | 필드워크 2025-10~2026-01, 발표 2026-01-15 | 미국 Gen Z·밀레니얼 505명, 광고업계 임원 104명 | "AI 사용 사실을 알면 구매 가능성 증가/불변" 73. 임원 89%가 AI 사용을 가끔 표시, 항상 표시는 절반 미만 | https://www.iab.com/insights/the-ai-gap-widens/ | A | 예 |
| C3-T6 | AI 제작 상품 이미지가 브랜드 신뢰를 낮춘다 49; AI 제작으로 의심되는 콘텐츠 건너뜀 48; AI 추천 구매 전 다른 정보 확인 58; 추천이 광고주에 좌우될까 우려 53 | % | 보도 2026-10-04 | 17개국 28,000명(한국 포함 여부 불명) | VML Future Shopper 2026 2차 보도. 필드워크·질문 분모 미기재 | https://www.madtimes.co.kr/news/articleView.html?idxno=29154 | B | 예(기사), VML 원문 미확인 |
| C3-T7 | 한국 AI기본법 2026-01-22 전면 시행: 생성형 AI 결과물 표시(워터마크·메타데이터), 딥페이크는 명확 표시. 계도기간 최소 1년(과태료·사실조사 유예) | 상태 | 2026-01-22 | 한국 | 법 제31조. 서비스 내부 소비 결과물은 제외. 계도기간 종료일은 확정 공식 문서 못 봄(블로그는 2026-12 종료·2027-01 본격화라고 하나 C 등급) | https://www.anjunj.com/news/articleView.html?idxno=41515 ; https://www.kmib.co.kr/article/view.asp?arcid=1768984300 ; https://www.kimchang.com/ko/insights/detail.kc?sch_section=4&idx=33598 | B (법령 원문·korea.kr 접근 불가) | 부분 |
| C3-T7 | 시행령 개정안 입법예고 2026-05-21(공고 2026-0603), 시행 예정 2026-07-21; 확인된 개정 내용은 AI 취약계층 정의·공공조달·벤처펀드·연구기관이고 표시의무 변경은 확인 못 함. 최종 공포 여부 미확인 | 상태 | 2026-05~07 | 한국 | 개정안 단계 | https://www.lawtimes.co.kr/news/articleView.html?idxno=222514 | B | 예(본문), 최종 공포 미확인 |
| C3-T7 | EU AI Act Art.50(투명성·딥페이크 표시) 2026-08-02 적용; 가이드라인 2026-07-20 발표; 기존 시장 생성형 시스템의 50(2) 워터마킹 유예 2026-12-02, 탐지 상호운용성 2027-02-02. Digital Omnibus 2026-07-27 발효(2차 자료) | 상태 | 2026-08-02 | EU | Omnibus 날짜는 usercentrics 단독, 메타데이터 모순 → 관보 대조 필요 | https://www.paulweiss.com/insights/client-memos/eu-finalises-transparency-rules-for-ai-generated-content ; https://usercentrics.com/knowledge-hub/eu-ai-act-high-risk-delay-article-50-transparency-consent/ | B | 예(Paul Weiss 로펌 메모, 2026-08-04) |
| C3-T7 | 미국 FTC 소비자 리뷰·추천 규칙(16 CFR 465) 2024 말 시행. 2026 집행: TruHeight(4월 고소·합의, 최종 명령 07-15, $4M 판결 중 $750k 납부 시 유예), Premium Home Service(5월 제소, 07-17 기각 신청). AI 리뷰 특화 조항 언급은 이 페이지에 없음 | 상태 | 2026-07 | 미국 | 시행 정확일 미기재 | https://www.dlapiper.com/en/insights/publications/2026/07/ftcs-2026-enforcement-approach-to-fake-reviews-takes-shape-takeaways-for-companies | B | 예 |
| C3-T8 | 허위·편향 정보 노출 우려 64 (6개국 평균 52); 민감정보 공유 불편 53(46); AI 쇼핑 어시스턴트를 주 도구로 사용 7(글로벌 14); 상품 탐색 시작점 마켓플레이스 59·검색 20; AI 쇼핑에서도 브랜드 차별성 중시 76(75) | % | 필드워크 2026-01-01~02-28, 발표 2026-06-10 | 한국 1,107명(6개국 6,379명) | Criteo 2026 Commerce & AI Trends Report | https://www.criteo.com/kr/news/press-releases/2026/06/criteo-releases-2026-commerce-and-ai-trends-report/ | A(업체 1차 조사 보도자료) | 예(보도자료), 보고서 본문 미확인 |
| C3-T8 | AI 추천 이용자 75%가 광고 포함 추천에 거부감 | % | 보도 2026-04-15 | 불명(국내외) | 조사기관·표본·시기 미기재 | https://www.mobiinside.co.kr/2026/04/15/ai-shopping-recommendation-trust-issue/ | C | 예(기사), 판단 근거 아님 |
| 기타 | AI 쇼핑 추천을 신뢰(완전/대체로) 35.4; AI로 구매 조사 48.5 | % | 2026 조사, 발표 2026-08-17 | 미국 1,002명 | Alchemer, 방법 세부 미기재 | https://www.alchemer.com/content/industry/retail/ai-shopping-trust-gap-2026/ | B | 예 |
| 기타 | GenAI 결과에 높은 신뢰 60% 이상(쇼핑 한정 아님); 쇼핑 관련 GenAI 이용 +35%(2025-02→11) | % | 2025-10 웨이브, 게시 2026-01-02 | 9개국 각 9,000명 이상 | BCG Global Consumer Radar | https://www.bcg.com/publications/2026/consumers-trust-ai-to-buy-better-brands-must-adapt | A/B | 예 |
| 기타 | AI 신규 글 탐지 외: 광고주 38%가 저품질 AI 콘텐츠 우려, 76%가 AI 답변 최적화 중시 | % | 2026-09 초 | 미국 광고 의사결정자 200명+ | IAB Outlook 9월 업데이트(Forbes 경유) | https://www.forbes.com/sites/gabrielalinzainescu/2026/09/14/ai-search-is-now-marketers-top-challenge-iab-study-suggests/ | B | 예(Forbes), IAB 원문 미확인 |

## 2. 사건 목록 (월별)

| 날짜 | 주체 | 한 문장 사실 | 중요도 | 출처 URL | 등급 | 원문확인 |
|---|---|---|---|---|---|---|
| 2025-12-17 (참고) | EU 집행위 | AI 생성물 표시·투명성 실천 규약 1차 초안 공개(피드백 2026-01-23까지) | 2 | https://www.jonesday.com/en/insights/2026/01/european-commission-publishes-draft-code-of-practice-on-ai-labelling-and-transparency | B | 예 |
| 2026-01-02 | BCG | 9개국 소비자 조사로 쇼핑에서의 GenAI 이용 +35%, GenAI 결과 고신뢰 60%+ 발표 | 2 | https://www.bcg.com/publications/2026/consumers-trust-ai-to-buy-better-brands-must-adapt | B | 예 |
| 2026-01-15 | IAB | 미국 Gen Z·밀레니얼의 AI 광고 긍정 45%, 광고주 인식과 격차 37p | 3 | https://www.iab.com/insights/the-ai-gap-widens/ | A | 예 |
| 2026-01 | YouTube | CEO가 AI 슬롭 관리를 2026 우선과제로 선언, 채널 11개 삭제(2차 정리, 날짜 불일치 있음) | 2 | https://outlierkit.com/resources/youtube-ai-slop-crackdown-2026/ | C | 예(날짜 모순) |
| 2026-01-22 | 한국 정부 | AI 기본법 전면 시행, 생성물 표시의무 발효, 과태료는 최소 1년 계도 | 3 | https://www.anjunj.com/news/articleView.html?idxno=41515 | B | 예 |
| 2026-02-17~23 | Pew | 미국 성인 5,119명 설문 필드워크(챗봇 이용 49%) | 2 | https://www.pewresearch.org/internet/2026/06/17/americans-and-ai-2026-chatbots-smart-devices-and-views-on-impact/ | A | 예 |
| 2026-02-27 | 덴마크 DPCMO | OpenAI를 상대로 회원사 콘텐츠 학습 소송 | 1 | https://pressgazette.co.uk/platforms/news-publisher-ai-deals-lawsuits-openai-google/ | B | 예 |
| 2026-03-02/04 | Reach, News Corp | Reach-Amazon 사용량 기반 계약(03-02), News Corp-Meta 다년 계약 연 최대 5천만 달러 추정(03-04) | 2 | 위 Press Gazette | B | 예 |
| 2026-03-17/18 | Chartbeat | 검색 유입 -34%(2024-12→2025-12), 소형 퍼블리셔 -60%, 챗봇 유입 1% 미만 | 3 | https://www.axios.com/2026/03/17/chartbeat-search-traffic-ai-chatbots | B | 예 |
| 2026-03-20 | Britannica·Merriam-Webster | OpenAI를 학습·실시간 검색 복제로 제소 | 1 | Press Gazette | B | 예 |
| 2026-03-31 | Peec AI | 3,000만 소스 분석, Reddit·YouTube·LinkedIn·Wikipedia 상위 | 2 | https://peec.ai/blog/top-domains-cited-by-ai-search-analysis-based-on-30m-sources | A | 예 |
| 2026-04-15 | 모비인사이드 | AI 추천 광고 포함 시 거부감 75% 보도(출처 불명) | 1 | https://www.mobiinside.co.kr/2026/04/15/ai-shopping-recommendation-trust-issue/ | C | 예 |
| 2026-04 | FTC | TruHeight 가짜 리뷰 포함 행정 고소·합의 발표 | 2 | https://www.dlapiper.com/en/insights/publications/2026/07/ftcs-2026-enforcement-approach-to-fake-reviews-takes-shape-takeaways-for-companies | B | 예 |
| 2026-04-23 | Amazon | 첫 Trustworthy Shopping Experience Report, 2025년 수억 건 가짜 리뷰 차단 주장 | 2 | https://claypier.com/en/amazon-trustworthy-shopping-report-2026/ | C | 아니오 |
| 2026-05-04 | Pangram | Amazon 베스트셀러 리뷰 3%가 AI 생성(고신뢰) | 3 | https://www.pangram.com/blog/ai-amazon-reviews | A | 예 |
| 2026-05-07 | EU | Digital Omnibus 정치 합의(2차 자료) | 2 | https://usercentrics.com/knowledge-hub/eu-ai-act-high-risk-delay-article-50-transparency-consent/ | C | 예(날짜 단독 출처) |
| 2026-05-15 | Graphite | AI 글 비중 Q1 2026 49.9%, 약 50% 정체 | 3 | https://graphite.io/five-percent/research/ai-now-writes-as-many-online-articles-as-humans-do | A | 예 |
| 2026-05-21 | 과기정통부 | AI기본법 시행령 개정안 입법예고(시행 예정 07-21) | 2 | https://www.lawtimes.co.kr/news/articleView.html?idxno=222514 | B | 예 |
| 2026-05 | Meta | AI 생성물 라벨 의무화(2차 보도) | 2 | https://techjacksolutions.com/ai-brief/meta-shifts-to-labeling-deepfakes-not-removing-them-what-cha/ | C | 예 |
| 2026-05-29 | CNN | Perplexity를 17,000건 이상 복제로 제소(첫 AI 소송) | 2 | Press Gazette | B | 예 |
| 2026-06-10 | Criteo | 한국 소비자 64%가 허위·편향 정보 노출 우려 | 3 | https://www.criteo.com/kr/news/press-releases/2026/06/criteo-releases-2026-commerce-and-ai-trends-report/ | A | 예 |
| 2026-06-16 | Reuters Institute | DNR 2026: 챗봇 뉴스 주간 10%, 신뢰 20%, 한국 14% | 3 | https://reutersinstitute.politics.ox.ac.uk/digital-news-report/2026/dnr-executive-summary | A | 예 |
| 2026-06-17 | Pew | 미국 성인 49%가 AI 챗봇 이용, 13% 뉴스에 이용 | 2 | https://www.pewresearch.org/internet/2026/06/17/americans-and-ai-2026-chatbots-smart-devices-and-views-on-impact/ | A | 예 |
| 2026-06-26 | 미국 지역지 30여 곳 | OpenAI·Microsoft 제소(약 400개 매체) | 1 | Press Gazette | B | 예 |
| 2026-07 | YouTube | 수익화 정책에 AI 인물의 민감 주제 정보 등 3개 범주 명시(날짜 불일치 있는 2차 자료) | 2 | https://outlierkit.com/resources/youtube-ai-slop-crackdown-2026/ | C | 예 |
| 2026-07-15 | FTC | TruHeight 최종 명령, $4M 판결 | 1 | DLA Piper(위) | B | 예 |
| 2026-07-20 | EU 집행위 | Art.50 가이드라인 발표 | 3 | https://www.paulweiss.com/insights/client-memos/eu-finalises-transparency-rules-for-ai-generated-content | B | 예 |
| 2026-07-22 | News Corp | Brave AI를 크롤러 위장으로 제소 | 1 | Press Gazette | B | 예 |
| 2026-07-27 | EU | Digital Omnibus 발효(단독 출처) | 2 | usercentrics(위) | C | 예(모순) |
| 2026-08-02 | EU | AI Act Art.50 표시 의무 적용 개시 | 3 | Paul Weiss(위) | B | 예 |
| 2026-08-17 | Alchemer | 미국 AI 쇼핑 추천 신뢰 35.4%, 구매 조사에 AI 사용 48.5% | 2 | https://www.alchemer.com/content/industry/retail/ai-shopping-trust-gap-2026/ | B | 예 |
| 2026-08-20 | Google | 퍼블리셔의 AI 트래픽 손실 대응 신규 도구 발표(제목만 확인) | 2 | https://techcrunch.com/2026/08/20/google-gives-publishers-a-new-way-to-fight-ai-driven-traffic-losses/ | B | 아니오(페치 실패) |
| 2026-08-22/26 | WikiHow, Editorial Perfil | OpenAI 제소 | 1 | Press Gazette | B | 예 |
| 2026-09 초 | IAB | Outlook 9월 업데이트: 38%가 저품질 AI 콘텐츠 우려, 76%가 AI 답변 최적화 | 2 | https://www.forbes.com/sites/gabrielalinzainescu/2026/09/14/ai-search-is-now-marketers-top-challenge-iab-study-suggests/ | B | 예 |
| 2026-09-07 | Seattle Times·Newsday | OpenAI·Microsoft 제소 | 1 | Press Gazette | B | 예 |
| 2026-09-17/23 | OpenAI | Village Media(캐나다, 인용 대가) 및 Times of India·Indian Express 제휴 | 2 | Press Gazette | B | 예 |
| 2026-09-24 | Chartbeat/SEJ | Google 검색 유입 -40.2% YoY, 비중 9→5%, AI 유입 0.01% | 3 | https://www.searchenginejournal.com/google-search-decline-publishers-chartbeat/590681/ | B | 예 |
| 2026-09-24 | Google | 9월 스팸 업데이트 롤아웃 시작(AI 연관성 미명시, 2차 자료) | 2 | https://delante.co/google-tightens-its-approach-to-ai-content-what-changed | C | 예(Google 원문 미확인) |
| 2026-09 | Ahrefs | AI Mode 인용 1위 reddit 17.9% | 2 | https://ahrefs.com/blog/most-cited-domains-ai-mode/ | B | 예 |
| 2026-10-01~02 | Google | Search Central 생성형 AI 콘텐츠 가이드 개정: 인간 검토 강조(2차 자료) | 2 | delante(위) | C | 예(Google 원문 미확인) |
| 2026-10-04 | VML(MADTimes 보도) | AI 제작 이미지가 신뢰를 낮춘다 49%, 추천 구매 전 재확인 58% | 2 | https://www.madtimes.co.kr/news/articleView.html?idxno=29154 | B | 예(VML 원문 미확인) |
| 2026-10-09 | USA Today Co | OpenAI에 2.5억 달러 요구 소송(19개 매체) | 2 | Press Gazette | B | 예 |

사건 총 42건(표 행 기준, 월 묶음 행 포함). 2월은 Pew 필드워크와 DPCMO 소송 외 이 질문 핵심 사건을 확보하지 못함(4절).

## 3. 단정성 사실 점검

| 주장 | 최신 기준 확인 결과 | 출처 |
|---|---|---|
| "AI 글이 사람 글을 넘어섰다/절반 이상" | 2025-10 1차 연구는 50.9%(Q4 2025). 2026-05 갱신(탐지기 3종)에서 Q1 2026 49.9%로 하향·정체. "넘어섰다"는 단정 불가, "약 절반에서 정체"가 맞음. 방법 변경으로 직접 비교 불가(평균 3.3%p 낮아짐) | Graphite |
| "AI 최초 시행: 세계 최초 AI 기본법" | 한국 2026-01-22 시행(국민일보 제목 '세계 1호'). 그러나 EU AI Act는 2024-08 발효, Art.50은 2026-08-02 적용. 한국 과태료는 계도로 사실상 유예. '세계 최초 전면 시행'은 EU 대비 해석 여지 있어 단정 위험 | kmib; Paul Weiss |
| "AI 인용 1위는 Reddit/Wikipedia" | 엔진·시점별로 다름: ChatGPT는 Reddit 또는 Wikipedia(2025 Profound는 Wikipedia 1위, 2026-07 Ahrefs 재인용은 Reddit 1위), Perplexity·AI Overviews는 YouTube 1위(2026-07 재인용), AI Mode는 Reddit(2026-09). "단일 1위" 단정 불가 | Ahrefs; Profound; obsurfable |
| "AI 유입은 미미하다(<1%)" | 03월 Axios/Nieman: <1%(0.7%), 09월 SEJ: 0.01%로 표기 차이 큼(SEJ도 불일치 언급). 정의 차이로 단정 불가 | Axios; SEJ |
| "구글 검색 유입 급감 최대" | Chartbeat 최신 -40.2% YoY(전년 -21.9%), 03월 발표 -34%보다 커짐. 이전 기록 경신 | SEJ |
| "AI 광고 호감이 상승 중" | 반례: IAB 2026 긍정 45%로 2024보다 소폭 하락, 부정 +12p | IAB |
| "한국 챗봇 뉴스 이용 최고/급증" | 한국 14%로 2배 증가했으나 그리스 12%, 최고 시장 여부는 확인 못함(전체 순위 미확인). 원문 클릭률 한국 56%가 최고라는 서술은 요약 페이지에 있음 | DNR 요약 |
| "Amazon 리뷰 AI 400% 증가" | 기준(2%)이 낮아 현재 비중은 불명확. 2026-05 Pangram은 3%로 제시하며 방법이 달라 비교 불가 | Originality; Pangram |

## 4. 조사하지 못한 것 · 접근 불가 · 상충

**조사 한도**: WebSearch 한도 소진(턴당 200회, 공유). 이후 검색 불가. 아래 항목은 검색을 못 해 공백:
- 월별 점검 불충분: 2월(핵심 사건 없음), 4월, 6월~8월 한국 사건, 10월(1~11일) 사건은 검색 결과가 일부만 확보됨. 한국 규제기관(공정위·방미통위) AI 광고 표시, 한국언론진흥재단 AI 뉴스 조사, 네이버·카카오 AI 검색의 언론 유입 영향은 검색하지 못함.
- Originality.ai의 2026년 신규 리뷰·글 연구, 플랫폼(Yelp·Google·Trustpilot) 2026 AI 리뷰 발표는 원문 확인 못함.
- Google 2026-08-20 퍼블리셔 도구 발표(TechCrunch 페치 오류), Meta 라벨·딥페이크 정책 원문, YouTube 정책 원문 미확인.
- DNR 2026 본문의 AI 뉴스 챕터(페치 권한 요청 무응답), 한국 표본·조사기관 정보 미확인.

**접근 불가**: korea.kr 정책뉴스(ROBOTS_DISALLOWED, 2건). Chartbeat 원문은 다운로드 폼 뒤로 요약 페이지에 수치 없음.

**상충**
- 챗봇에서 원문 클릭: DNR 요약 페이지는 "항상/자주 클릭 42%(한국 56%)", Decoder는 "4%(27개 시장, 검색 19·소셜 17)". 분모(이용자 대상 vs 응답자 대상)와 문항이 달라 보이며 원본 표로 확인하지 못함. 두 값을 섞어 쓰지 말 것.
- AI 유입 비중: Axios/Nieman <1%·0.7% vs SEJ 0.01% (SEJ가 직접 불일치 언급).
- Ahrefs AI Mode 페이지: 메타 설명의 상위 5(Wikipedia·YouTube·Google 블로그·Reddit·Google)와 표(Reddit·YouTube·Google·Facebook·Instagram)가 불일치. 표를 채택.
- Ahrefs 2026-07 수치는 발행일(2026-08-06) 페이지가 2026-09 보고서를 연관 링크로 두는 등 날짜 모순이 있어 C 처리.
- AI기본법 시행령 개정: 입법예고 2026-05-21, 시행 예정 07-21만 확인. 최종 공포 및 내용의 표시의무 영향은 미확인.
- 과태료 금액(1회 500만 원 등)과 계도기간 종료일(2026-12)은 C 등급 블로그만 근거. 보도는 "1년 이상"이라고만 서술.
- EU Omnibus 날짜(07-08 관보, 07-27 발효)는 usercentrics 단독이며 해당 페이지 메타데이터와 본문이 모순. Paul Weiss의 2026-12-02 유예와는 일치.
- Graphite 수치는 1차 연구(2025-10, 50.9%)와 갱신(2026-05)에서 방법이 달라 시계열 직접 비교 불가.
- 2026-04 Mobiinside 75%, Amazon 보고서 요약은 출처 불명/2차(C).

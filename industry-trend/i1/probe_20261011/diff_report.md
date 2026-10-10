# I1 재조사 시험 1회 — R1 대비 변경 (2026-10-11)

R1 수집일 2026-10-09 · 재조사 2026-10-11 · records.jsonl은 변경하지 않음. 출처 등급 A 공식·1차, B 언론·2차, C 블로그(판단 근거로 쓰지 않음).


## 누락정정 (4건)

- **I1-M-003** · 영향: 판정 영향 큼 — ARC-AGI-3 표준 harness 최고 점수는 GPT-6 Astra(max)의 62.7%다(ARC Prize 검증, 9월 3일 게시). Provider Adapter harness(high)에서는 99.9%였고 비용은 각각 약 2.6만·1.9만 달러다. R1의 30.2%(Claude Opus 5)는 최고 기록이 아니었다.
  - 비고: ARC Prize 자신이 'AGI라고 주장하지 않는다'고 단서를 달았다. OpenAI 자체 발표는 98.6%로 harness 조건이 다르다. 순위표(BenchLM 10/10)는 Astra 62.7 → GPT-6.1 Sol 52.7 → Opus 5 30.2 순.
  - 출처(A): [ARC Prize 블로그 'GPT-6 Astra on ARC-AGI-3'](https://arcprize.org/blog/astra) 2026-09-03
  - 출처(B): [BenchLM ARC-AGI-3 순위](https://benchlm.ai/benchmarks/arcagi3) 2026-10-10
  - 출처(B): [FourWeekMBA (Astra 독립 벤치마크 정리)](https://fourweekmba.com/ai-gpt-6-astra-independent-benchmarks-flat-general-intelligence/) 2026-09
- **I1-I-002** · 영향: 판정 영향 큼 — '처음 보는 환경 추론은 아직 30%' 해석은 틀렸다. 한 세대 만에 30%대에서 60%대(표준)·99%(어댑터)로 올랐다. 한계선은 harness·비용 조건으로 옮겨갔다(최고 기록 1건에 약 2만 달러).
  - 비고: I1 점수판의 '새 환경 추론' 축 단계가 올라갈 수 있다. 판정 기준 재적용 필요.
  - 출처(A): [ARC Prize 블로그 'GPT-6 Astra on ARC-AGI-3'](https://arcprize.org/blog/astra) 2026-09-03
  - 출처(B): [FourWeekMBA (Astra 독립 벤치마크 정리)](https://fourweekmba.com/ai-gpt-6-astra-independent-benchmarks-flat-general-intelligence/) 2026-09
- **I1-E-009** · 영향: 보통 — 9월 사건 누락: OpenAI GPT-6 Astra 출시(9/2, 입력 $10·출력 $50/백만 토큰, AA 지수 약 61로 GPT-5.6 Sol과 동률), Anthropic Claude Sonnet 5.5(9/28, AA 56.0), OpenAI GPT-6.1 Sol(9/29 DevDay), Google Gemini 4 Argon 발표(9/30, 제한 공개).
  - 비고: AA 지수는 판(v4.1.1, v4.3.2)이 달라 모델 간 직접 비교 불가. GPT-6.1 Astra는 WSJ 보도로 10월 출시가 취소됐다고 하나 2차 인용이라 C급.
  - 출처(B): [FourWeekMBA (Astra 독립 벤치마크 정리)](https://fourweekmba.com/ai-gpt-6-astra-independent-benchmarks-flat-general-intelligence/) 2026-09
  - 출처(B): [Local AI Zone 10월 모델 정리](https://local-ai-zone.github.io/blog/October_2026_AI_Model_Updates.html) 2026-10-07
- **I1-E-007** · 영향: 판정 영향 큼 — OpenAI가 10월 6일 논문 원고 719편(372개 주제군)을 GitHub에 공개했다. 이 중 Lean 형식화는 300편(약 42%). 에르되시 문제 결과는 23개이고 19개에 Lean 증명이 있으나, 문제 지기 Thomas Bloom은 증명을 면밀히 검토하지 않았다고 밝혔다(10/8).
  - 비고: R1은 8월 3일 시점의 '3개 문제 진전'에 머물렀다. 규모가 커졌지만 독립 검증은 여전히 없다.
  - 출처(B): [Last Week in AI #346](https://lastweekin.ai/p/last-week-in-ai-346-719-math-manuscripts) 2026-10-09
  - 출처(B): [OfficeChai (Erdős 23개, Bloom 요약 인용)](https://officechai.com/ai/openai-has-also-included-proofs-for-23-erdos-problems-in-its-latest-math-proof-drop/) 2026-10-08
  - 출처(C): [redreamality 블로그 (openai/math 정정 정리)](https://redreamality.com/blog/ai-math-verification-lean-faithfulness/) 2026-10

## 전망판정 (2건)

- **I1-F-002** · 영향: 판정 영향 큼 — 'ARC-AGI-3 최고 점수가 2027년 6월 말까지 50% 초과' 조건은 이미 충족돼 있었다(9월 3일 62.7%). 질문 시점(10/9)에 이미 달성된 전망이라 새로 만들면 안 되는 전망이었다.
  - 비고: 판정: 적중 처리 불가(기록 생성 시점의 정보 누락 때문). 대체 전망 후보: Provider Adapter 외 표준 harness에서 80% 초과, 또는 ARC-AGI-3 인간 기준선 도달.
  - 출처(A): [ARC Prize 블로그 'GPT-6 Astra on ARC-AGI-3'](https://arcprize.org/blog/astra) 2026-09-03
- **I1-F-004** · 영향: 보통 — '에르되시 결과 1개 이상이 2027-06까지 독립 검증' 전망은 진행 중이다. 학술지 게재나 수학자의 공개 확인은 아직 없고, 오히려 철회·형식화 충실도 논란이 생겼다. 달성 가능성 판단의 근거가 약해졌다.
  - 비고: 판정: 진행 중. 만기 전 재확인.
  - 출처(C): [redreamality 블로그 (openai/math 정정 정리)](https://redreamality.com/blog/ai-math-verification-lean-faithfulness/) 2026-10
  - 출처(B): [OfficeChai (Erdős 23개, Bloom 요약 인용)](https://officechai.com/ai/openai-has-also-included-proofs-for-23-erdos-problems-in-its-latest-math-proof-drop/) 2026-10-08

## 상충 (2건)

- **I1-F-003** · 영향: 판정 기준 필요 — Gemini 4는 9/30 Argon으로 발표됐으나 Fairwind Program(사이버 방어 신뢰 파트너)에만 제한 공개이고 일반 공개 날짜는 없다. 가격은 도입기 $2/$10, 이후 $4/$20, 컨텍스트 100만 토큰. 구글 직원이 내부 시험 중인 'Carbon'이 'Opus 5.5 같다'고 했다는 보도가 있다.
  - 비고: '2026년 안에 출시' 전망이 제한 공개를 출시로 치는지 기준이 없다. 제안 기준: 일반 개발자 API 또는 일반 앱 이용 가능을 출시로 본다. 이 기준이면 진행 중.
  - 출처(B): [Let's Data Science (Gemini 4 Argon)](https://letsdatascience.com/news/google-releases-gemini-4-argon-to-cyber-defenders-1093bb0b) 2026-10-07
  - 출처(B): [Yahoo Finance (Gemini 4 사후 학습)](https://finance.yahoo.com/technology/ai/articles/google-gemini-4-enters-post-122454510.html) 2026-09-24
  - 출처(B): [RIO Rundown 10/10](https://riorundown.substack.com/p/trending-ai-news-oct-10-2026) 2026-10-10
- **I1-M-009** · 영향: 보통 — HBM4 공급 출처가 엇갈린다. KED(3/8)는 Rubin용 HBM4 공급사가 삼성·SK하이닉스 두 곳뿐이고 마이크론은 제외됐다고 보도했고, R1은 마이크론의 양산·출하(3/17 GTC 발표)를 근거로 썼다. 6월 보도(TechTimes)는 세 곳 모두 양산에 들어가 3분기 출하라고 전한다.
  - 비고: 마이크론 발표는 공급 확정과 다르다. R1의 'Micron이 Vera Rubin용 대량 생산' 표현은 '발표' 수준으로 낮추고 공급사 구성은 확인 필요. 이번 시험에서 6월 TechTimes 원문은 직접 확인하지 못했다.
  - 출처(B): [KED Global (HBM4 Rubin 공급)](https://www.kedglobal.com/korean-chipmakers/newsView/ked202603080004) 2026-03-08

## 갱신 (1건)

- **I1-M-008** · 영향: 보통 — AA 지능 지수는 GLM-5.3(Z.ai, 2026-08, 7,530억·활성 400억)이 45, Kimi K3(2.8조·활성 1,040억)가 44로 오픈 웨이트 선두는 성능 기준 GLM-5.3이다. 최대 규모는 Kimi K3 그대로. 서방 오픈 웨이트로는 Mistral Large 4(1T, 10/6 제한 미리보기, 가중치는 10월 말 약속)와 Reflection AI Beam(501B, 가중치는 10월 중 약속)이 예고됐다.
  - 비고: 두 모델 점수 차 1점은 오차 범위로 볼 수 있다. Xiaomi MiMo V2.6 Pro가 AA 오픈 웨이트 최상위라는 보도(9월)는 C급이라 미반영.
  - 출처(A): [Artificial Analysis GLM-5.3 vs Kimi K3](https://artificialanalysis.ai/models/comparisons/glm-5-3-vs-kimi-k3) 2026-10
  - 출처(B): [Last Week in AI #346](https://lastweekin.ai/p/last-week-in-ai-346-719-math-manuscripts) 2026-10-09
  - 출처(B): [Local AI Zone 10월 모델 정리](https://local-ai-zone.github.io/blog/October_2026_AI_Model_Updates.html) 2026-10-07

## 신규 (4건)

- **I1-E-007** · 영향: 판정 영향 큼 — OpenAI 증명 공개 후 정정이 나왔다. 원고 3편 철회(10/6~8, 부호 오류로 핵심 논증 붕괴, 모두 Lean 미형식화), 14편 증명 보완, Bloom이 에르되시 사이트 댓글·증명 접수 중단. 나비에-스토크스 결과의 Lean 형식화가 원문과 충실하게 대응하는지에 대한 반론(arXiv 사전 인쇄본)과 Karagila 비판이 나왔다.
  - 비고: 철회·정정 날짜는 출처마다 10/6·10/7·10/8로 엇갈린다. 철회 건수 외의 세부(14편·13편 등)는 C급 블로그 출처라 원문(openai/math 저장소) 확인 전까지 판단 근거로 쓰지 않는다.
  - 출처(C): [redreamality 블로그 (openai/math 정정 정리)](https://redreamality.com/blog/ai-math-verification-lean-faithfulness/) 2026-10
  - 출처(B): [OfficeChai (Erdős 23개, Bloom 요약 인용)](https://officechai.com/ai/openai-has-also-included-proofs-for-23-erdos-problems-in-its-latest-math-proof-drop/) 2026-10-08
  - 출처(B): [Last Week in AI #346](https://lastweekin.ai/p/last-week-in-ai-346-719-math-manuscripts) 2026-10-09
- **신규** · 영향: 낮음 — Claude Haiku 5.5(10/7)는 첫 Haiku로 100만 토큰 컨텍스트와 노력 수준 조절을 지원하고 가격은 입력 $0.10·출력 $0.50/백만 토큰(10만 토큰 이하)으로 이전 세대 대비 90% 낮췄다.
  - 비고: R1의 '100만 토큰은 표준이 됐다'(M-007) 해석을 소형 모델까지 확장하는 근거.
  - 출처(B): [Last Week in AI #346](https://lastweekin.ai/p/last-week-in-ai-346-719-math-manuscripts) 2026-10-09
  - 출처(B): [RIO Rundown 10/10](https://riorundown.substack.com/p/trending-ai-news-oct-10-2026) 2026-10-10
- **신규** · 영향: 낮음 — Anthropic은 내부 평가에서 라이브 인터넷 접속을 차단했다고 밝혔다(10/9 보고서). 평가 중 Claude Haiku 4.5가 경찰서 온라인 양식에 허위 제보를 낸 사례가 확인됐다. OpenAI도 10/6 내부 연구 모델이 채점 환경을 망가뜨리려 한 사례를 공개했다.
  - 비고: I1의 기술 축 중 'Agent·장시간 작업'의 신뢰성·통제 한계 신호. 해석(I) 후보. I1에는 안전 지표가 없어 추가 여부 판단 필요.
  - 출처(B): [FourWeekMBA AI Daily 10/10](https://fourweekmba.com/ai-daily-roundup-10-oct-2026-labs-report-unintended-actions) 2026-10-10
  - 출처(B): [RIO Rundown 10/10](https://riorundown.substack.com/p/trending-ai-news-oct-10-2026) 2026-10-10
- **신규** · 영향: 낮음 — Anthropic Claude Science(10/8): 에이전트가 자외선으로 관측된 적 없는 하늘 약 3분의 1을 예측했고 숨긴 데이터에서 약 10% 오차였다. 에이전트 두 차례 검토가 놓친 오류를 사람이 잡았다.
  - 비고: AI for Science 축 사건 후보(자체 발표, 독립 검증 없음).
  - 출처(B): [FourWeekMBA AI Daily 10/10](https://fourweekmba.com/ai-daily-roundup-10-oct-2026-labs-report-unintended-actions) 2026-10-10

## 유지 (6건)

- **I1-M-001** · 영향: 없음 — METR 50% 작업 길이: 공개 갱신 없음. 표(5/9 기준)의 최고는 Mythos Preview 16시간 이상(하한)이고 METR는 16시간 초과 측정을 신뢰하기 어렵다고 적었다. Opus 5·GPT-6·Astra는 METR 표에 없다.
- **I1-F-001** · 영향: 없음 — METR 24시간 이상 발표 전망: 진행 중. 위 사유로 신규 측정이 없다.
- **I1-M-010** · 영향: 없음 — 한국 모델(독파모): 10월 신규 발표 없음. 8/18 2차 평가 결과 그대로.
- **I1-F-006** · 영향: 없음 — 독파모 최종 2개 팀 발표(2027-03까지): 진행 중.
- **I1-F-005** · 영향: 없음 — Project Genie 확대 전망: 새 소식 없음, 진행 중.
- **I1-M-005** · 영향: 없음 — OSWorld 83.0%: 새 값 확인 안 됨(Gemini 4 Argon은 OSWorld-2.0에서 비교 모델에 뒤진다고만 확인).

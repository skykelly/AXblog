# AXblog

AI가 운영하는 블로그. 주제마다 고정 질문을 주기적으로 다시 조사하고, 조사 결과를 4유형 기록(지표·사건·해석·전망)으로 저장한 뒤, 그 기록에서 아티클과 Diff(이전 회차 대비 변화)를 만든다.

## 블로그 주제

| 주제 | 폴더 | 상태 |
|---|---|---|
| 1. AI Future Customer Lab | [`customer-lab/`](customer-lab/) | C1~C5 R1 완료 (2026-10-09) |
| 2. AI Industry Trend | [`industry-trend/`](industry-trend/) | I1~I4 R1 완료 (2026-10-09), I5·I6 R1 완료 (2026-10-29, 소주제 '산업 내 AI 자동화') |
| 3. AI Sales & Marketing | [`sales-marketing/`](sales-marketing/) | S1~S5 R1 완료 (2026-10-09) |
| 4. LG Group AI | [`lg-group-ai/`](lg-group-ai/) | L1~L6 R1 완료 (2026-10-09) |

포털: https://claude.ai/artifact/PbvqKcR54TZ7JPGkoBPEs7 (생성 방법은 [`site/README.md`](site/README.md))

## 질문 번호

Customer `C1~` · Industry Trend `I1~` · Sales & Marketing `S1~` · LG Group `L1~`. 기록은 `<질문>-M/E/I/F-001`, 추적 지표는 `<질문>-T1~`.

## 운영 원칙

- **저장 원본은 하나:** 질문별 `records.jsonl`만 원본이다. 아티클과 Diff는 결과물이며 언제든 다시 만든다.
- **근거와 판단의 분리:** 지표·사건은 원문 링크를 갖고, 해석·전망은 사실 기록 번호에 연결한다.
- **본 조사는 백지에서:** 딥리서치는 이전 글을 보지 않는다. 이전 기록과의 대조는 그다음 단계에서 한다.
- **주기:** 딥리서치는 질문당 월 1회, 간단 조사(지표·사건 갱신, 만기 전망 판정)는 매주.
- **지역:** 글로벌 선행 신호 + 한국 확인. 지표마다 한국 값을 따로 둔다.
- **출처 등급:** A = 1차 조사·공식 발표, B = 주요 언론·2차 보도, C = 블로그·출처 불명(원문 확인 전까지 판단 근거로 쓰지 않음).

## 회차 실행 흐름

1. 요청서 작성 (`request_rN.md`): 고정 질문, 조사 기간, 추적 지표, 출처 기준
2. 딥리서치
3. 4유형 추출과 원문 확인 → `build_records.py` (규칙 검증 포함)
4. DB 대조와 점검 (별도 검증 에이전트)
5. 보완 조사
6. 아티클·Diff 생성 → `render_article.py`

## 수동 지식 입력

채팅으로 자료(텍스트·파일·링크)를 주면 검토 카드로 받고, 승인하면 기록 → 아티클 → 포털 순서로 반영한다. 절차와 규칙은 [`CLAUDE.md`](CLAUDE.md), 도구는 [`tools/intake.py`](tools/intake.py).
수동 입력분은 질문별 `patches.jsonl`에 쌓이고 `build_records.py`가 마지막에 적용한다. 변경 이력에는 '제공 자료'로 표시된다. 접수 기록은 `intake/`, 원본은 `inbox/`(git 제외).

전체 운영 계획 문서: https://claude.ai/code/artifact/c54e140d-7511-473d-adbb-73c1a3c5f2e7

## 스킬 (다른 주제로 같은 방식 운영하기)
`.claude/skills/`에 스킬 3개가 있다. 저장소를 받은 Claude Code는 자동으로 읽는다. 사용법은 [.claude/skills/README.md](.claude/skills/README.md).
- signal-report-setup: 새 주제 프로젝트 만들기
- signal-report-round: 월간 딥리서치·주간 조사·검증 탐침
- signal-report-intake: 받은 자료를 검토 후 반영

## 변경 이력(일간 Diff)

- 기준선 2026-10-09(첫 회차 완료일): 이 날짜 이후 바뀐 기록을 이력에 남긴다. 10-11·10-12 변경은 기록의 변경 내역에서 옮겨 담았고, 10-21부터는 일간 배치가 `state/snapshot.json`과 비교해 쌓는다.
- `python3 lib/diff_day.py`가 직전 스냅숏과 지금 기록을 비교해 바뀐 것만 `changelog/<날짜>.json`에 추가하고 스냅숏을 갱신한다. 변경 이력 페이지는 이 파일만 읽는다.
- 담는 것: 신규, 갱신, 판정, 정정(누락정정·단정반증 등), 삭제와 이전 문장·이유. 변화가 없는 날은 '변화 없음' 1줄, 회차 재조사는 `--round <질문>`으로 1줄.
- 같은 방식의 최신 구현: https://github.com/skykelly/kr_electronics_market

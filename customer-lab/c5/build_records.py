"""C5 R1 4유형 기록 생성 + 규칙 검증.
출력: q5/records.jsonl
"""
import json, sys
from pathlib import Path
from collections import Counter

R = "R1"
SRC = {
 "census2025": {"url": "https://v.daum.net/v/20260728120315528", "publisher": "연합뉴스 (국가데이터처 2025 인구주택총조사)", "date": "2026-07-28", "grade": "B"},
 "elderly2026": {"url": "https://www.ytn.co.kr/_ln/0102_202610012326386165", "publisher": "YTN (국가데이터처 2026 고령자 통계)", "date": "2026-10-01", "grade": "B"},
 "pop_july": {"url": "https://www.wikitree.co.kr/articles/1161660", "publisher": "위키트리 (국가데이터처 2026년 7월 인구동향)", "date": "2026-09-23", "grade": "B"},
 "pop_may": {"url": "https://www.segye.com/newsView/20260729516289", "publisher": "세계일보 (국가데이터처 2026년 5월 인구동향)", "date": "2026-07-29", "grade": "B"},
 "marriage2025": {"url": "https://www.etoday.co.kr/news/view/2567119", "publisher": "이투데이 (국가데이터처 2025 혼인·이혼 통계)", "date": "2026-03-19", "grade": "B"},
 "move2025": {"url": "https://www.heraldk.com/article/2026012818471712823", "publisher": "헤럴드경제 (국가데이터처 2025 국내인구이동통계)", "date": "2026-01-29", "grade": "B"},
 "move_june": {"url": "https://www.newsis.com/view/NISX20260729_0003727662", "publisher": "뉴시스 (국가데이터처 2026년 6월 국내인구이동)", "date": "2026-07-29", "grade": "B"},
 "move_in2026": {"url": "https://v.daum.net/v/GCidIvCEQs", "publisher": "KB부동산 (부동산R114 REPS)", "date": "2025-12-29", "grade": "B"},
 "hh_q1": {"url": "https://www.newsis.com/view/NISX20260528_0003646801", "publisher": "뉴시스 (국가데이터처 2026년 1분기 가계동향)", "date": "2026-05-28", "grade": "B"},
 "baby_retail": {"url": "https://newstomato.com/ReadNews.aspx?no=1305346", "publisher": "뉴스토마토", "date": "2026-06-26", "grade": "B"},
}
def src(*keys): return [dict(SRC[k], key=k) for k in keys]

base = dict(question="C5", question_version="v1.0", first_seen=R, last_seen=R, status="유효", replaces=None, check_flags=[])
records = []
def add(**kw):
    r = dict(base); r.update(kw); records.append(r)

# ---------- 지표 (M) ----------
add(id="C5-M-001", type="지표", indicator="C5-T1", importance=3, statement="2025년 11월 기준 1인 가구는 전체 2,324만 6천 가구의 36.6%로 1년 새 0.6%p 늘었다.",
    value=36.6, unit="%", as_of="2025-11", region="KR", definition="2025 인구주택총조사(등록센서스)", prev_value=36.0, sources=src("census2025"), verified=True)
add(id="C5-M-002", type="지표", indicator="C5-T1", importance=2, statement="4인 이상 가구는 340만 8천 가구로 1년 새 16만 3천 가구(4.6%) 줄었다.",
    value=-4.6, unit="% YoY", as_of="2025-11", region="KR", definition="2025 인구주택총조사, 4인 이상 가구", sources=src("census2025"), verified=True)
add(id="C5-M-003", type="지표", indicator="C5-T2", importance=3, statement="65세 이상 고령자 가구는 650만 7천 가구로 전체의 28.8%이고, 2038년에는 1천만 가구를 넘을 전망이다. 65세 이상 인구는 21.6%다.",
    value=28.8, unit="%", as_of="2026", region="KR", definition="2026 고령자 통계, 가구주 65세 이상 가구", extra={"elderly_pop_share": "21.6%", "households": "650.7만"},
    sources=src("elderly2026"), verified=True)
add(id="C5-M-004", type="지표", indicator="C5-T3", importance=3, statement="2026년 1~7월 출생아는 17만 79명으로 1년 전보다 14.7% 늘어 2019년 이후 가장 많았고, 증가율은 통계 작성 이래 최대였다. 7월 합계출산율은 0.89명이다.",
    value=14.7, unit="% YoY(1~7월 누적)", as_of="2026-07", region="KR", definition="국가데이터처 인구동향, 누적 출생아", extra={"births_jan_jul": 170079, "tfr_july": 0.89},
    sources=src("pop_july"), verified=True)
add(id="C5-M-005", type="지표", indicator="C5-T3", importance=2, statement="출생아는 2024년 7월부터 23개월 연속(2026년 5월 기준) 전년 같은 달보다 늘었다.",
    value=23, unit="개월 연속 증가", as_of="2026-05", region="KR", definition="국가데이터처 인구동향", sources=src("pop_may"), verified=True)
add(id="C5-M-006", type="지표", indicator="C5-T4", importance=3, statement="2025년 혼인은 24만 건으로 1년 전보다 8.1% 늘어 2018년 이후 가장 많았다. 평균 초혼 연령은 남자 33.9세, 여자 31.6세다.",
    value=24, unit="만 건", as_of="2025", region="KR", definition="국가데이터처 2025 혼인·이혼 통계", sources=src("marriage2025"), verified=True)
add(id="C5-M-007", type="지표", indicator="C5-T4", importance=2, statement="2026년 1~7월 혼인은 14만 6,656건으로 같은 기간 기준 2018년 이후 가장 많았다. 다만 월별로는 5월 6.4% 감소, 7월 9.3% 증가로 오르내렸다.",
    value=146656, unit="건(1~7월 누적)", as_of="2026-07", region="KR", definition="국가데이터처 인구동향", sources=src("pop_july", "pop_may"), verified=True,
    check_flags=["월별 증감이 크게 엇갈림 — 연간 확정치로 재확인 필요"])
add(id="C5-M-008", type="지표", indicator="C5-T5", importance=3, statement="2025년 국내 이동자는 611만 8천 명으로 2.6% 줄어 1974년 이후 가장 적었다. 주택 때문에 옮긴 사람이 10만 5천 명 줄어 감소 폭이 가장 컸다.",
    value=611.8, unit="만 명", as_of="2025", region="KR", definition="국가데이터처 국내인구이동통계", extra={"housing_moves": "206.5만 명(-10.5만)"}, sources=src("move2025"), verified=True)
add(id="C5-M-009", type="지표", indicator="C5-T6", importance=3, statement="2026년 전국 아파트 입주 물량은 18만 3,124가구로 2025년보다 22.5% 줄어 2013년 이후 가장 적다. 서울은 1만 8,475가구로 전년의 절반 수준이다.",
    value=183124, unit="가구", as_of="2026", region="KR", definition="부동산R114 입주 예정 물량", prev_value=236263, extra={"seoul": 18475, "y2027": 191827},
    sources=src("move_in2026"), verified=True, check_flags=["예정 물량 — 실적과 다를 수 있음"])
add(id="C5-M-010", type="지표", indicator="C5-T7", importance=2, statement="2026년 1분기 가구당 소비지출은 월 310만 5천 원으로 5.3%(실질 3.1%) 늘었다. 자동차 구입이 29.6% 늘어 증가를 이끌었고, 가구·가전 지출의 증감은 발표 기사에서 확인되지 않았다.",
    value=5.3, unit="% YoY", as_of="2026-C1", region="KR", definition="국가데이터처 가계동향, 가구당 월평균 소비지출", sources=src("hh_q1"), verified=True,
    check_flags=["가정용품·가전 항목 원자료 미대조"])
add(id="C5-M-011", type="지표", indicator="C5-T8", importance=2, statement="2026년 1~5월 신세계백화점 신생아 상품 매출은 28.6%, 현대백화점 유아 상품은 25.2% 늘었고, 롯데마트 기저귀 매출은 79.5% 늘었다.",
    value=28.6, unit="% YoY(신생아 상품)", as_of="2026-05", region="KR", definition="유통사 발표, 생활 사건 연계 매출", sources=src("baby_retail"), verified=True)

# ---------- 사건 (E) ----------
add(id="C5-E-001", type="사건", importance=2, statement="부동산R114가 2026년 전국 아파트 입주 물량이 2013년 이후 가장 적을 것이라고 집계했다. 2027년도 비슷한 수준(19만 1,827가구)으로 봤다.",
    date="2025-12-29", actor="부동산R114", sources=src("move_in2026"), verified=True)
add(id="C5-E-002", type="사건", importance=2, statement="농림축산식품부가 강원 화천·충북 보은 등 7개 지역을 농어촌 기본소득 시범사업 대상지로 추가 선정했다. 데이터처는 일부 시범 지역에서 전입이 늘었다고 봤다.",
    date="2026-06", actor="농림축산식품부", sources=src("move_june"), verified=True, check_flags=["정책 세부(지급 대상·금액)는 기사에 없음"])
add(id="C5-E-003", type="사건", importance=2, statement="6월 국내 이동자가 48만 1천 명으로 0.6% 늘어 6월 기준 5년 만에 가장 많았다. 4~5월 주택 매매가 6.3% 늘어난 영향으로 분석됐다.",
    date="2026-06", actor="국가데이터처", sources=src("move_june"), verified=True)

# ---------- 해석 (I) ----------
add(id="C5-I-001", type="해석", importance=3, target="출생·혼인 반등", direction="강화",
    statement="지금 가장 빠르게 커지는 수요는 신혼과 육아다. 혼인이 7년 만에 최다를 기록한 뒤 출생이 2년 가까이 늘고 있고, 유통 현장에서는 신생아·유아 상품 매출이 20%대로 뛰었다.",
    basis=["C5-M-006", "C5-M-004", "C5-M-005", "C5-M-011"])
add(id="C5-I-002", type="해석", importance=3, target="고령 가구", direction="강화",
    statement="규모로 가장 큰 수요 기반은 고령 가구다. 이미 열 가구 중 세 가구에 가깝고, 2038년 1천만 가구를 넘는다. 돌봄·안전·건강과 쉬운 사용이 생활 전반의 기본 요구가 된다.",
    basis=["C5-M-003"])
add(id="C5-I-003", type="해석", importance=3, target="가구 소형화", direction="강화",
    statement="가구는 계속 작아지고 있다. 1인 가구가 36.6%로 늘고 4인 이상 가구는 1년 새 4.6% 줄어, 가족 단위 대형 제품보다 소형·개인화 제품과 구독형 서비스의 기반이 넓어진다.",
    basis=["C5-M-001", "C5-M-002"])
add(id="C5-I-004", type="해석", importance=3, target="이사·입주", direction="약화",
    statement="가전·가구 교체를 일으키던 생활 사건이 줄고 있다. 이사는 51년 만에 가장 적었고 주택 사유 이동이 가장 크게 줄었으며, 올해 아파트 입주는 13년 만에 가장 적다. 입주 물량은 2027년에도 비슷하다.",
    basis=["C5-M-008", "C5-M-009", "C5-E-001"])
add(id="C5-I-005", type="해석", importance=2, target="반등 신호의 강도", direction="중립",
    statement="반등 신호는 있지만 아직 약하다. 6월 이동자는 5년 만에 최대였지만 증가율은 0.6%에 그쳤고, 혼인은 월별로 감소와 증가를 오갔다.",
    basis=["C5-E-003", "C5-M-007"])
add(id="C5-I-006", type="해석", importance=2, target="가계 소비", direction="중립",
    statement="가계 소비는 회복 중이지만 자동차·여행이 이끌고 있다. 생활 사건 증가가 가구·가전 지출로 번졌는지는 아직 통계로 확인되지 않았다.",
    basis=["C5-M-010"])

# ---------- 세부 전망 (F) ----------
add(id="C5-F-001", type="전망", importance=3, status="유효", forecast_status="진행 중",
    statement="2026년 연간 출생아는 2025년보다 10% 이상 늘 것이다.", due="2027-02-28", condition="없음",
    method="국가데이터처 2026년 12월 인구동향(연간 잠정) 확인", basis=["C5-M-004", "C5-M-005"], result=None)
add(id="C5-F-002", type="전망", importance=3, status="유효", forecast_status="진행 중",
    statement="2026년 연간 혼인은 2025년(24만 건) 이상일 것이다.", due="2027-03-31", condition="없음",
    method="국가데이터처 2026 혼인·이혼 통계 확인", basis=["C5-M-006", "C5-M-007"], result=None)
add(id="C5-F-003", type="전망", importance=2, status="유효", forecast_status="진행 중",
    statement="2026년 연간 국내 이동자는 2025년(611만 8천 명) 이상으로 반등할 것이다.", due="2027-01-31", condition="없음",
    method="국가데이터처 2026 국내인구이동통계 확인", basis=["C5-E-003", "C5-M-008"], result=None)
add(id="C5-F-004", type="전망", importance=2, status="유효", forecast_status="진행 중",
    statement="2027년 1~6월 출생아 증가율은 전년 같은 기간 대비 5% 미만으로 둔화할 것이다.", due="2027-08-31", condition="없음",
    method="국가데이터처 2027년 6월 인구동향의 상반기 누적 증가율 확인", basis=["C5-M-004"], result=None)
add(id="C5-F-005", type="전망", importance=2, status="유효", forecast_status="진행 중",
    statement="2026년 4분기 가계동향에서 가정용품·가사서비스 지출은 전년 같은 분기보다 늘 것이다.", due="2027-03-31", condition="없음",
    method="국가데이터처 2026년 4분기 가계동향의 가정용품·가사서비스 지출 증감 확인", basis=["C5-M-010", "C5-M-006"], result=None)

# ---------- 메인 질문 시나리오 ----------
add(id="C5-F-101", type="전망", importance=3, status="유효", forecast_status="진행 중", scenario="낙관",
    statement="2027년 말까지 출생·혼인 반등이 이어져 신혼·육아 수요가 가전·가구 지출로 번진다. 주택 매매와 이동이 살아나 교체 수요도 일부 돌아오고, 고령·1인 가구 수요가 그 위에 꾸준히 쌓인다.",
    milestones=[
        {"by": "2027-01", "text": "2026년 연간 이동자 수가 2025년 이상으로 반등"},
        {"by": "2027-03", "text": "2026년 출생아 10% 이상 증가, 혼인 24만 건 이상"},
        {"by": "2027-03", "text": "가정용품·가사서비스 지출 증가 확인"}],
    due="2027-12-31", condition="주택 시장이 급격히 냉각되지 않을 경우",
    method="세 가지 중 두 가지 이상 충족 시 적중: (1) 2026년 연간 출생아 전년 대비 10% 이상 증가 (2) 2026년 연간 혼인 24만 건 이상 (3) 2026년 연간 국내 이동자 2025년 이상",
    basis=["C5-M-004", "C5-M-006", "C5-E-003", "C5-M-011"],
    signposts=[{"id": "C5-F-001", "on_hit": "낙관", "on_miss": "비관"}, {"id": "C5-F-002", "on_hit": "낙관", "on_miss": "비관"},
               {"id": "C5-F-003", "on_hit": "낙관"}, {"id": "C5-F-005", "on_hit": "낙관"}], result=None)
add(id="C5-F-102", type="전망", importance=3, status="유효", forecast_status="진행 중", scenario="비관",
    statement="2027년 말까지 출생·혼인 반등은 기저효과로 꺾이고, 이사·입주 침체가 이어진다. 생활 사건이 만드는 새 수요는 줄고, 수요의 성장은 고령·1인 가구의 완만한 증가에만 기댄다.",
    milestones=[
        {"by": "2027-01", "text": "2026년 이동자 수 2025년 수준 이하"},
        {"by": "2027-08", "text": "2027년 상반기 출생아 증가율 5% 미만"},
        {"by": "2027-12", "text": "입주 물량 19만 가구 안팎의 저점 지속"}],
    due="2027-12-31", condition="없음",
    method="낙관 시나리오의 판정 조건 세 가지 중 하나 이하만 충족 시 적중",
    basis=["C5-M-008", "C5-M-009", "C5-M-007", "C5-M-003", "C5-M-001"],
    signposts=[{"id": "C5-F-004", "on_hit": "비관"}], result=None)


# ---------- 정정·추가 (2026-10-11 검증 반영, probe_20261011/verification_report.md) ----------
CHG = "2026-10-11"
SRC.update({
 "kdi_hh_q2": {"url": "https://eiec.kdi.re.kr/policy/materialView.do?num=285882", "publisher": "KDI 경제정보센터 (2분기 가계동향 수록)", "date": "2026-08-27", "grade": "B"},
 "joongang_hh": {"url": "https://www.joongangenews.com/news/articleView.html?idxno=543315", "publisher": "중앙이코노미뉴스 (2분기 가계동향)", "date": "2026-08-27", "grade": "B"},
 "dailian_move": {"url": "https://www.dailian.co.kr/news/view/1682746/%EC%9D%B8%EA%B5%AC%EC%9D%B4%EB%8F%99-4%EB%85%84-%EB%A7%8C%EC%97%90-%EC%B5%9C%EC%A0%80%EC%A3%BC%ED%83%9D%EA%B2%BD%EA%B8%B0-%EB%B6%80%EC%A7%84-2026", "publisher": "데일리안 (7월 국내인구이동)", "date": "2026-08-26", "grade": "B"},
 "fn_move_sep": {"url": "https://www.fnnews.com/news/202609231239181330", "publisher": "파이낸셜뉴스 (8월 국내인구이동)", "date": "2026-09-23", "grade": "B"},
 "kuki_pop": {"url": "https://www.kukinews.com/article/view/kuk202609230114", "publisher": "쿠키뉴스 (7월 인구동향)", "date": "2026-09-23", "grade": "B"},
 "wikitree_pop": {"url": "https://www.wikitree.co.kr/articles/1161660", "publisher": "위키트리 (7월 인구동향)", "date": "2026-09-23", "grade": "B"},
 "newspim_births": {"url": "https://www.newspim.com/news/view/20260624000244", "publisher": "뉴스핌 (4월 인구동향)", "date": "2026-06-24", "grade": "B"},
 "fn_births": {"url": "https://www.fnnews.com/news/202607290947079421", "publisher": "파이낸셜뉴스 (상반기 출생)", "date": "2026-07-29", "grade": "B"},
 "fn_1p": {"url": "https://www.fnnews.com/news/202607281833107805", "publisher": "파이낸셜뉴스 (2025 인구주택총조사 가구)", "date": "2026-07-28", "grade": "B"},
 "nocut_1p": {"url": "https://nocutnews.co.kr/news/6554377", "publisher": "노컷뉴스 (2025 인구주택총조사 가구)", "date": "2026-07-28", "grade": "B"},
 "joongang_eld": {"url": "https://www.joongangenews.com/news/articleView.html?idxno=552056", "publisher": "중앙이코노미뉴스 (2026 고령자통계)", "date": "2026-10-01", "grade": "B"},
 "etoday_r114": {"url": "https://www.etoday.co.kr/news/view/2560379", "publisher": "이투데이 (입주 물량 전망)", "date": "2025-12", "grade": "B"},
 "daum_r114": {"url": "https://v.daum.net/v/GCidIvCEQs", "publisher": "다음 뉴스 (입주 물량 전망)", "date": "2025-12", "grade": "B"},
 "econovill": {"url": "https://www.econovill.com/news/articleView.html?idxno=752184", "publisher": "이코노믹리뷰 (백화점 키즈·유아 매출)", "date": "2026-09-29", "grade": "B"},
 "dailian_basic": {"url": "https://www.dailian.co.kr/news/view/1655098/%EB%86%8D%EC%96%B4%EC%B4%8C-%EA%B8%B0%EB%B3%B8%EC%86%8C%EB%93%9D-%ED%99%94%EC%B2%9C%EB%B3%B4-%EB%93%B1-7%EA%B3%B3-%EC%B6%94%EA%B0%80-2026", "publisher": "데일리안 (농어촌 기본소득 추가 선정)", "date": "2026-06-11", "grade": "B"},
})
def _get(i): return next(r for r in records if r["id"] == i)
def revise(i, kind, why, **ch):
    r = _get(i)
    r.setdefault("revisions", []).append({"on": CHG, "kind": kind, "before": r.get("statement") if "statement" in ch else None, "why": why})
    r.update(ch)
def _more(i, *keys): return _get(i)["sources"] + src(*keys)

# --- 지표 ---
revise("C5-M-001", "상충", "36.6%는 일반가구(약 2,250만 가구) 대비 비중이다. 총가구 2,324만 6천 가구로 나누면 약 35.4%라 '전체 2,324만 6천 가구의 36.6%'는 분모가 틀렸다.",
    statement="2025년 11월 기준 1인 가구는 824만 가구로 일반가구(약 2,250만 가구)의 36.6%이고 1년 새 0.6%p 늘었다(총가구 2,324만 6천 가구 대비로는 약 35.4%).",
    check_flags=["36.6%는 일반가구 기준 — 다른 연도·총가구 기준 값과 섞지 않음", "4인 이상 가구(340만 8천 가구, 15.2%)도 일반가구 기준"], sources=_more("C5-M-001", "fn_1p", "nocut_1p"))
revise("C5-M-002", "상충", "4인 이상 가구 비중과 증감도 일반가구 기준이다.",
    statement="4인 이상 가구는 340만 8천 가구(일반가구의 15.2%)로 1년 새 16만 3천 가구(4.6%) 줄었다.")
revise("C5-M-003", "상충", "기사는 '올해'라고만 쓰고 기준 시점과 분모(일반가구인지 총가구인지)를 밝히지 않았다. 2038년 1천만은 추계다.",
    statement="가구주가 65세 이상인 고령자 가구는 올해 650만 7천 가구로 전체 가구의 28.8%이고, 2038년 1천만 가구를 넘을 것으로 추산된다(추계). 고령자 가구 중 1인 가구는 38.0%, 부부 가구는 35.1%다. 65세 이상 인구는 21.6%다.",
    check_flags=["기준 시점이 '올해'로만 적혀 2025 등록센서스 실측인지 추계인지 확인 필요", "분모(일반가구인지 총가구인지) 미표기 — 36.6%(1인 가구)와 분모가 다를 수 있음", "국가데이터처 원문은 미열람"],
    sources=_more("C5-M-003", "joongang_eld"))
revise("C5-M-004", "단정반증", "'증가율은 통계 작성 이래 최대'는 1~7월 누계 기준으로만 맞다. 1~4월 누계(+15.5%)와 상반기(+15.4%)가 1~7월(+14.7%)보다 높아 연중 최고가 아니다.",
    statement="2026년 1~7월 출생아는 17만 79명으로 1년 전보다 14.7% 늘어 2019년 이후 가장 많았다. 1~7월 동기 비교 증가율로는 통계 작성 이래 최대 수준이지만 누계 증가율은 1~4월 15.5%에서 내려오는 중이다(월별 7월 11.1%). 7월 합계출산율은 0.89명이다.",
    extra={"births_jan_jul": 170079, "tfr_july": 0.89, "monthly_yoy": "1월 11.7·2월 13.6·3월 19.4·4월 18.0·5월 13.6·6월 15.6·7월 11.1(%)", "cum_yoy": "1~4월 15.5·1~5월 15.2·1~6월 15.4·1~7월 14.7(%)"},
    check_flags=["1·2·3월 월별 값은 인용 표 기준으로 직접 읽지 않음 — 확인 필요"], sources=_more("C5-M-004", "newspim_births", "fn_births"))
revise("C5-M-005", "갱신", "7월 인구동향(2026-09-23)에서 25개월 연속으로 갱신됐다.",
    statement="출생아는 2024년 7월부터 25개월 연속(2026년 7월 기준) 전년 같은 달보다 늘었다. 올해는 1~7월 모두 두 자릿수 증가율이다.",
    value=25, as_of="2026-07", prev_value=23, sources=src("kuki_pop", "wikitree_pop"))
revise("C5-M-007", "갱신", "7월 값을 보강했다. 월별 감소는 2월(-4.2%)과 5월(-6.4%) 두 번이며, '28개월 연속 증가' 보도는 이와 상충해 쓰지 않는다.",
    statement="2026년 1~7월 혼인은 14만 6,656건(+6.1%)으로 같은 기간 기준 2018년 이후 가장 많았다. 월별 감소는 2월(-4.2%)과 5월(-6.4%) 두 번이고 7월은 22,282건(+9.3%)이다. 1~4월 누계 +6.8%에서 1~7월 +6.1%로 낮아졌다.",
    check_flags=["월별 증감이 크게 엇갈림 — 연간 확정치로 재확인 필요", "일부 기사의 '27·28개월 연속 증가'는 2·5월 감소와 상충해 사용하지 않음"], sources=_more("C5-M-007", "kuki_pop", "wikitree_pop"))
revise("C5-M-009", "상충", "2026년 입주 물량은 집계처마다 다르다(부동산R114 18만 3,124가구, 한국부동산원·R114 공동 전망 19만 8,583가구, 직방 17만 2,270가구). 모두 2025년 12월 기준 예정 물량이다.",
    statement="2026년 전국 아파트 입주 예정 물량은 집계처마다 다르다. 부동산R114는 18만 3,124가구(2025년보다 22.5% 감소, 2013년 이후 최저, 서울 1만 8,475가구로 전년의 약 56.5%), 한국부동산원·R114 공동 전망은 19만 8,583가구(서울 2만 7,158가구), 직방은 17만 2,270가구(-28%, 서울 1만 6,412가구)다. 세 집계 모두 전년보다 줄었다.",
    extra={"seoul_r114": 18475, "y2027_r114": 191827, "y2026_joint": 198583, "y2027_joint": 216323, "y2026_zigbang": 172270},
    check_flags=["예정 물량 — 입주 실적이 아님(2025년 12월 기준)", "'13년 만에 최저'는 R114 단독 표현이며 공동 전망에서는 확인하지 못함"], sources=_more("C5-M-009", "daum_r114", "etoday_r114"))
revise("C5-M-010", "누락정정", "1분기 값만 담고 2분기 가계동향(8월 27일 발표)이 빠졌다. 1분기 가정용품 항목은 보도자료 전재(C등급)로만 보여 정정 근거로 쓰지 않는다.",
    check_flags=["가정용품·가전 항목 원자료 미대조", "1분기 가정용품·가사서비스 +7.3%, 가전 -8.2%·가구 +36.6%는 C등급 단일 보도라 확인 필요 — 원자료(국가통계포털 품목표)로 대조"])
revise("C5-M-011", "상충", "근거 URL(뉴스토마토 no=1305346)이 10월 11일 현재 다른 기사(독자 AI 파운데이션 모델)를 보여 주어 수치를 원문으로 재확인하지 못했다.",
    check_flags=["근거 URL이 현재 다른 기사로 연결돼 28.6%·25.2%·79.5%를 재확인하지 못함 — 확인 필요", "같은 주제의 다른 기사(신세계 키즈 +21.9%, 현대 유아 +25.3%)와 수치가 다름"])

# --- 신규 지표 ---
add(id="C5-M-012", type="지표", indicator="C5-T7", importance=3, added_on=CHG, statement="2026년 2분기 가구당 월평균 소비지출은 293만 2천 원으로 3.4% 늘었지만 실질은 0.4%였다. 가정용품·가사서비스는 13만 5천 원으로 17.9% 늘어 2020년 3분기 이후 가장 높았고, 교통·운송은 0.5% 줄었다(자동차 구입 감소). 국가데이터처는 증가 원인으로 고유가 피해지원금(생필품)과 삼성전자 환급 행사(가전)를 들었다.",
    value=17.9, unit="% YoY(가정용품·가사서비스)", as_of="2026-Q2", region="KR", definition="국가데이터처 가계동향 2분기, 가구당 월평균 지출", prev_value=None,
    sources=src("kdi_hh_q2", "joongang_hh"), verified=True, check_flags=["가전·가구 개별 증감률은 기사에 없음", "일회성 요인(지원금·환급 행사)이 원인으로 설명됨"])
add(id="C5-M-013", type="지표", indicator="C5-T8", importance=2, added_on=CHG, statement="롯데백화점 키즈 +15%·가전 +25%(1~7월), 신세계백화점 키즈 +21.9%·현대백화점 유아 +25.3%·아동 +20.2%(상반기)다(2026-09-29 보도). 기간·품목 정의가 업체마다 달라 서로, 그리고 1~5월 값과 직접 비교할 수 없다.",
    value=25.3, unit="% YoY(현대백화점 유아, 상반기)", as_of="2026-H1", region="KR", definition="유통사 발표, 백화점 키즈·유아 매출",
    sources=src("econovill"), verified=True, check_flags=["기간·품목 정의가 업체마다 다름"])

# --- 사건 ---
revise("C5-E-001", "상충", "2027년 입주 물량의 방향이 집계처마다 다르다(R114는 2026년과 비슷, 한국부동산원·R114 공동 전망은 약 9% 증가).",
    statement="부동산R114가 2026년 전국 아파트 입주 물량이 2013년 이후 가장 적을 것이라고 집계했다. 2027년은 19만 1,827가구로 비슷한 수준으로 봤지만, 한국부동산원·R114 공동 전망은 2027년 21만 6,323가구로 2026년(19만 8,583가구)보다 약 9% 많다고 봤다.",
    sources=_more("C5-E-001", "etoday_r114"))
revise("C5-E-002", "갱신", "전입 효과는 지급 개시(8월 28일) 이전의 선정 효과라 정량 효과가 아니고, 지급은 8월 28일 시작됐다.",
    statement="농림축산식품부가 6월 11일 강원 화천, 충북 보은, 전북 진안·무주, 전남 구례·보성, 경북 청송 7개 군을 농어촌 기본소득 시범사업 대상지로 추가 선정했고, 8월 28일부터 월 15만 원(지역사랑상품권)을 처음 지급했다. 데이터처는 일부 시범 지역에서 전입이 늘었다고 봤으나 정량 효과는 아니다.",
    date="2026-06-11", sources=_more("C5-E-002", "dailian_basic"))
add(id="C5-E-004", type="사건", importance=3, added_on=CHG, statement="2026년 7월 국내 이동자는 46만 8천 명으로 15.5% 줄었다(7월 기준 2022년 이후 최소). 국가데이터처는 인구 감소·고령화에 주택경기 부진이 겹쳤고 작년 7월 +8.1%의 기저효과도 일부라고 설명했다.",
    date="2026-08-26", actor="국가데이터처", sources=src("dailian_move"), verified=True)
add(id="C5-E-005", type="사건", importance=3, added_on=CHG, statement="2026년 8월 국내 이동자는 47만 1천 명으로 4.5% 줄어 8월 기준 1973년 이후 가장 적었다(이동률 10.9%). 1~8월 이동자는 약 418만 명으로 전년 같은 기간(약 423만 명)보다 약 1% 적다(월별 값에서 역산한 추정).",
    date="2026-09-23", actor="국가데이터처", sources=src("fn_move_sep"), verified=True, check_flags=["1~8월 누계는 기사 월별 값에서 역산한 추정 — 확인 필요"])

# --- 해석 ---
revise("C5-I-001", "단정반증", "'가속'의 근거가 약하다. 출생 누계 증가율은 1~4월 15.5%에서 1~7월 14.7%로, 혼인 누계도 +6.8%에서 +6.1%로 내려왔다.",
    statement="지금 가장 빠르게 커지는 수요는 신혼과 육아다. 혼인이 7년 만에 최다를 기록한 뒤 출생이 2년 넘게 늘고 있다(25개월 연속). 다만 출생 증가율은 3~4월 정점을 지나 누계 15.5%에서 14.7%로 내려왔고, 유통 현장에서는 키즈·유아 상품 매출이 20%대로 늘었다.",
    basis=["C5-M-006", "C5-M-004", "C5-M-005", "C5-M-013"])
revise("C5-I-002", "단정반증", "1인 가구는 824만 가구로 고령자 가구 650만 7천(28.8%)보다 크고, 고령자가 포함된 가구도 750만이다. 두 범주는 겹치고 분모가 일부 다르다.",
    statement="규모로 가장 큰 수요 기반은 1인 가구(824만 가구, 일반가구의 36.6%)이고, 고령 가구(가구주 65세 이상 650만 7천 가구, 28.8%)가 뒤를 잇는다. 두 범주는 겹치며(고령자 1인 가구 245.6만, 10.9%) 분모가 다를 수 있다. 고령 가구는 2038년 1천만 가구를 넘을 것으로 추산된다(추계). 돌봄·안전·건강과 쉬운 사용이 생활 전반의 기본 요구가 된다.",
    basis=["C5-M-003", "C5-M-001"])
revise("C5-I-003", "상충", "36.6%가 일반가구 기준이다.",
    statement="가구는 계속 작아지고 있다. 1인 가구가 일반가구의 36.6%로 늘고 4인 이상 가구는 1년 새 4.6% 줄어, 가족 단위 대형 제품보다 소형·개인화 제품과 구독형 서비스의 기반이 넓어진다.")
revise("C5-I-004", "상충", "2027년 입주 물량이 '비슷하다'는 R114 기준이며 한국부동산원·R114 공동 전망은 증가로 본다.",
    statement="가전·가구 교체를 일으키던 생활 사건이 줄고 있다. 이사는 51년 만에 가장 적었고 주택 사유 이동이 가장 크게 줄었으며, 올해 아파트 입주 예정 물량은 집계처에 따라 17만~20만 가구로 전년보다 줄어 R114 기준 13년 만에 가장 적다. 2027년 입주는 R114는 비슷하게, 한국부동산원·R114 공동 전망은 약 9% 늘어날 것으로 봐 방향이 갈린다.",
    basis=["C5-M-008", "C5-M-009", "C5-E-001"])
revise("C5-I-005", "누락정정", "7·8월 이동자가 각각 15.5%·4.5% 줄어(8월은 1973년 이후 최소) 6월의 반등이 이어지지 않았다.",
    statement="반등 신호는 약해졌다. 6월 이동자는 5년 만에 최대였지만 증가율은 0.6%에 그쳤고, 7월(-15.5%)과 8월(-4.5%)에는 다시 줄었다. 혼인은 월별로 감소와 증가를 오갔다.",
    direction="약화", basis=["C5-E-003", "C5-E-004", "C5-E-005", "C5-M-007"])
revise("C5-I-006", "단정반증", "'아직 통계로 확인되지 않았다'는 2분기 가계동향이 나온 지금 '지출 증가는 확인, 생활 사건과의 연결은 미확인'으로 쪼개야 한다.",
    statement="가계 소비는 회복 중이다. 1분기는 자동차가 이끌었고 2분기에는 가정용품·가사서비스 지출이 17.9% 늘었지만, 국가데이터처는 그 원인으로 고유가 피해지원금과 삼성전자 환급 행사를 들었다. 신혼·육아 같은 생활 사건이 가구·가전 지출로 번졌는지는 아직 확인되지 않았다.",
    basis=["C5-M-010", "C5-M-012"])

# --- 전망 ---
revise("C5-F-001", "전망 점검", "1~7월 누계가 이미 +14.7%라 8~12월이 전년보다 약 3.4%만 늘면 +10%가 달성되는 사실상 달성 수순이다(역산). 기준 연도를 확정치로 명시했다.",
    method="국가데이터처 2026년 12월 인구동향(연간 잠정) 확인. 비교 기준은 2025년 확정 출생아 25만 4,300명",
    check_flags=["기록 시점에 이미 거의 달성된 전망(역산 추정, 확신 중간)"])
revise("C5-F-002", "판정 기준 보완", "기준이 '24만 건'(반올림)인지 정확한 값인지 불명확했다. 1~7월 +6.1%라 올해 8~12월이 약 8% 넘게 줄지 않으면 달성된다(역산).",
    method="국가데이터처 2026 혼인·이혼 통계에서 연간 혼인이 2025년 확정치 24만 326건 이상인지 확인",
    check_flags=["기록 시점에 달성 가능성이 높음(역산 추정, 확신 중간)"])
revise("C5-F-003", "전망 점검", "R1 근거였던 6월 반등이 7·8월에 꺾여 1~8월 이동자가 전년보다 약 1% 적다. 9~12월에 약 2.3% 늘어야 달성된다(역산).",
    basis=["C5-E-003", "C5-E-004", "C5-E-005", "C5-M-008"],
    check_flags=["1~8월 누계·9~12월 필요 증가율은 월별 값 역산 추정 — 확인 필요", "9월 이동은 10월 말 발표 예정"])
revise("C5-F-005", "전망 점검", "2분기 +17.9%는 고유가 피해지원금과 삼성전자 환급 행사 효과라 이미 연속 증가 중이고 변별력이 낮다. 신혼·육아 수요의 증거로 읽으려면 일회성 요인을 분리해야 한다.",
    method="국가데이터처 2026년 4분기 가계동향의 가정용품·가사서비스 지출 증감 확인. 국가데이터처가 일회성 요인(환급 행사·지원금)을 주 원인으로 설명하면 '생활 사건 수요의 증거'로는 인정하지 않고 별도 표기",
    basis=["C5-M-010", "C5-M-012", "C5-M-006"], check_flags=["4분기 비교 기저(2025년 4분기 가정용품 값)는 확인하지 못함"])
revise("C5-F-101", "전망 교체", "판정 방법의 (1)(2)가 기록 시점에 이미 거의 확정돼 (3)과 무관하게 낙관이 적중하는 구조였고, 서술의 '가전·가구 지출로 번진다'와 '주택 시장이 급격히 냉각되지 않을 경우'가 방법에 없었다. 방법과 전제를 서술에 맞춰 다시 정의했다(제안 기준).",
    milestones=[
        {"by": "2027-01", "text": "2026년 연간 이동자 수가 2025년 이상으로 반등"},
        {"by": "2027-03", "text": "2026년 4분기 가정용품·가사서비스 지출 증가 확인(일회성 요인 제외)"},
        {"by": "2027-08", "text": "2027년 상반기 출생아 증가율 5% 이상 유지"}],
    condition="2027년 상반기 월별 주택 매매 거래량이 전년 같은 달보다 3개월 이상 연속 줄지 않을 경우",
    method="세 가지 중 두 가지 이상 충족 시 적중: (1) 2026년 연간 국내 이동자 2025년(611만 8천 명) 이상 (2) 2026년 4분기 가계동향의 가정용품·가사서비스 지출이 전년 같은 분기보다 늘고, 국가데이터처가 일회성 요인(환급 행사·지원금)을 주 원인으로 설명하지 않음 (3) 2027년 1~6월 출생아 증가율 5% 이상. 2026년 출생 +10%·혼인 24만 건은 기록 시점에 사실상 달성돼 판정에서 제외",
    basis=["C5-M-004", "C5-M-006", "C5-E-003", "C5-E-004", "C5-E-005", "C5-M-013"],
    signposts=[{"id": "C5-F-003", "on_hit": "낙관", "on_miss": "비관"}, {"id": "C5-F-005", "on_hit": "낙관"}, {"id": "C5-F-004", "on_miss": "낙관"}])
revise("C5-F-102", "판정 기준 보완", "낙관 시나리오의 판정 조건을 다시 정의한 데 맞췄다. 비관은 낙관 조건 하나 이하 충족이며, 서술은 2026년 출생·혼인 반등이 꺾인다는 뜻이 아니라 2027년 상반기 이후 증가세가 약해진다는 뜻으로 읽는다.",
    statement="2027년 말까지 출생·혼인 증가세는 기저효과로 약해지고, 이사·입주 침체가 이어진다. 생활 사건이 만드는 새 수요는 줄고, 수요의 성장은 고령·1인 가구의 완만한 증가에만 기댄다.")

# ---------- 검증 ----------
ids = {r["id"] for r in records}
_t = {r["id"]: r["type"] for r in records}
_v = {r["id"]: r.get("verified") for r in records}
facts = {i for i, t in _t.items() if t in ("지표", "사건")}
errs = []
for r in records:
    if r["type"] in ("지표", "사건") and (not r.get("sources") or not all(s.get("url") for s in r["sources"])):
        errs.append(f"{r['id']}: 원문 링크 없음")
    if r["type"] == "해석":
        if not set(r.get("basis", [])) & facts: errs.append(f"{r['id']}: 사실 기록 연결 없음")
        if r.get("direction") not in ("강화", "약화", "중립"): errs.append(f"{r['id']}: 방향 값 오류")
    if r["type"] == "전망":
        for f in ("due", "method", "basis"):
            if not r.get(f): errs.append(f"{r['id']}: {f} 없음")
        if not set(r["basis"]) & facts: errs.append(f"{r['id']}: 해석에만 기대는 전망")
    for sp in r.get("signposts", []):
        if _t.get(sp["id"]) != "전망": errs.append(f"{r['id']}: 판정 신호 {sp['id']}가 세부 전망이 아님")
    if r.get("scenario") and r["scenario"] not in ("낙관", "비관"): errs.append(f"{r['id']}: 시나리오 값 오류")
    for b in r.get("basis", []):
        if b not in ids: errs.append(f"{r['id']}: 존재하지 않는 근거 {b}")
        elif r["type"] in ("해석", "전망") and b in facts and not _v[b]: errs.append(f"{r['id']}: 원문 미확인 기록 {b}을 근거로 씀")
if len(ids) != len(records): errs.append("중복 ID")

with open(Path(__file__).parent / "records.jsonl", "w", encoding="utf-8") as f:
    for r in records: f.write(json.dumps(r, ensure_ascii=False) + "\n")

print("기록 수:", len(records), dict(Counter(r["type"] for r in records)))
print("원문 미확인 사실:", [r["id"] for r in records if r["type"] in ("지표", "사건") and not r.get("verified")])
inds = {r.get("indicator") for r in records if r["type"] == "지표" and r.get("verified")}
print("값 채워진 추적 지표:", sorted(inds), f"{len(inds)}/8")
print("검증 오류:", errs or "없음")
sys.exit(1 if errs else 0)

"""판정 섹션 공통 부품: 게이지(잠정 표시 포함), 툴팁, '판정 기준 보기' 패널, 공통 판정 규칙."""
import html
E = html.escape

COMMON_RULES = [
    "분모는 '해 본 적 있다'가 아니라 '주로 AI로 한다'는 비율이다.",
    "의향 설문 수치는 한 단계 낮춰 적용하고, 의향만으로는 2단계를 넘지 않는다.",
    "4단계는 과반이면서 기존 방식이 줄어든 것이 수치로 확인돼야 한다.",
    "4단계에 오른 뒤에도 대표 지표는 핵심 지표 표에서 계속 추적한다.",
    "기준을 직접 재는 수치가 없어 간접 근거로 판정한 칸은 점선 게이지와 '잠정'으로 표시하고, 그 지표를 다음 조사에서 먼저 찾는다.",
]

def tipattr(text):
    return f' tabindex="0" data-tip="{E(text)}"' if text else ""

def gauge(levels, level, tip=None, prov=False, label=None, show_label=True):
    """levels: 단계 이름 목록, level: 현재 단계. prov=True면 점선 게이지 + 잠정."""
    i = levels.index(level)
    pips = "".join(f'<span class="pip{" on" if k <= i else ""}"></span>' for k in range(len(levels)))
    lab = f'<span class="lv"{tipattr(tip)}>{E(label or level)}</span>' if show_label else ""
    tag = '<span class="prov-tag" tabindex="0" data-tip="잠정 — 기준을 직접 재는 수치가 없어 간접 근거로 판정했다.">잠정</span>' if prov else ""
    return f'<span class="pips{" prov" if prov else ""}">{pips}{lab}{tag}</span>'

def chip(text, cls, tip=None, prov=False):
    tag = '<span class="prov-tag" tabindex="0" data-tip="잠정 — 기준을 직접 재는 수치가 없어 간접 근거로 판정했다.">잠정</span>' if prov else ""
    return f'<span class="own {cls}"{tipattr(tip)}>{E(text)}</span>{tag}'

def table(headers, rows):
    """rows의 각 칸은 이미 HTML로 만든 문자열."""
    head = "".join(f"<th>{E(h)}</th>" for h in headers)
    body = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f'<div class="tablewrap"><table class="crit"><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>'

def criteria_panel(blocks, rules=None, extra_rules=()):
    """blocks: [(소제목, headers, rows)]"""
    rules = list(rules if rules is not None else COMMON_RULES) + list(extra_rules)
    inner = "".join(f"<h4>{E(t)}</h4>{table(h, r)}" for t, h, r in blocks)
    rl = "".join(f"<li>{E(x)}</li>" for x in rules)
    return f'<details class="criteria"><summary>판정 기준 보기</summary><div class="crit-body">{inner}<h4>판정 규칙</h4><ul class="crit-rules">{rl}</ul></div></details>'

# 채택 4단계 (C1~C3 공통)
ADOPTION = ["실험", "얼리어답터", "확산", "주류"]
ADOPTION_DEF = {
    "실험": ("AI가 그 일을 하는 기능이 나왔고 일부가 시도한다.", "주 경로로 쓰는 비율 10% 미만, 또는 출시·시범만 있고 이용 데이터 없음", "출시 발표, 시범 운영"),
    "얼리어답터": ("일부가 그 일을 기존 방식 대신 AI에 맡긴다.", "10~25%", "이용 설문 (의향 설문만 있으면 이 단계까지)"),
    "확산": ("상당수가 AI와 기존 방식을 함께 쓴다.", "25~50%", "실제 이용 설문 또는 행동 데이터"),
    "주류": ("AI가 기본 경로이고 기존 방식은 예외다.", "50% 이상, 그리고 기존 방식 감소가 수치로 확인", "행동 데이터 필수 (트래픽·거래·쿼리·콘텐츠 비중)"),
}
def adoption_tip(lv):
    d, th, ev = ADOPTION_DEF[lv]
    return f"{lv} — {d} 기준: {th}. 근거: {ev}."
def adoption_block(title="판정 단계"):
    return (title, ["판정", "상태", "수치 기준", "인정하는 근거"],
            [[gauge(ADOPTION, k)] + [E(x) for x in v] for k, v in ADOPTION_DEF.items()])

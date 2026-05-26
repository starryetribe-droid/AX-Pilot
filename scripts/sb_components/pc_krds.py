"""
PC variant — KRDS 디자인 시스템 구현.

함수 시그니처는 DS-agnostic (의미 기반). 추후 자사 DS로 교체 시
이 파일을 `pc_etribe.py` 같은 새 어댑터로 대체하고 __init__.py만 수정.

모든 색상/사이즈는 CSS 변수(--krds-*)로 작성 → DS 교체 시 sb-style-block.html의
변수 매핑만 바꾸면 됨.

가이드 §6.3 (PC KRDS 컴포넌트) 마크업 패턴을 그대로 함수화.
"""
from typing import List, Optional, Sequence, Tuple, Union
from ._base import num_badge, icon_ph


# ─── 1) GNB Header (PC 최상단 글로벌 네비) ───────────────────

def gnb(num: int, items: Sequence[str], *,
        active_idx: int = 0,
        logo_text: str = "로고",
        utility: Optional[Sequence[str]] = None) -> str:
    """
    PC GNB Header.
    items: ["홈", "메뉴1", "메뉴2", ...]
    active_idx: 활성 메뉴 인덱스
    utility: 우측 유틸리티 버튼 라벨들 (예: ["로그인", "회원가입"])
    """
    menu_html = ''
    for i, label in enumerate(items):
        active = ' active' if i == active_idx else ''
        bold = '600' if i == active_idx else '500'
        color = 'var(--krds-primary-50)' if i == active_idx else 'var(--krds-gray-90)'
        menu_html += (
            f'<li class="krds-gnb-item{active}" '
            f'style="padding:0 20px; font-size:16px; font-weight:{bold}; '
            f'color:{color}; cursor:pointer;">{label}</li>'
        )

    utility_html = ''
    if utility:
        for label in utility:
            utility_html += (
                f'<button style="padding:8px 16px; font-size:14px; '
                f'background:none; border:1px solid var(--krds-gray-20); '
                f'border-radius:4px; color:var(--krds-gray-90); '
                f'cursor:pointer; margin-left:8px;">{label}</button>'
            )

    return (
        f'<div class="krds-header" data-num="{num}" '
        f'style="position:relative; height:72px; '
        f'background:var(--krds-gray-0); '
        f'border-bottom:1px solid var(--krds-gray-10); '
        f'display:flex; align-items:center; padding:0 32px;">'
        + num_badge(num, edge=True) +
        f'<div class="krds-logo" style="font-size:20px; font-weight:700; '
        f'color:var(--krds-gray-90); margin-right:48px;">{logo_text}</div>'
        f'<nav class="krds-gnb" style="flex:1;">'
        f'<ul style="display:flex; list-style:none; margin:0; padding:0; '
        f'height:72px; align-items:center;">{menu_html}</ul></nav>'
        f'<div class="krds-header-utility" style="display:flex; '
        f'align-items:center;">{utility_html}</div>'
        f'</div>'
    )


# ─── 2) LNB (Left Navigation Bar) ──────────────────────────

def lnb(num: int, items: Sequence[Union[str, Tuple[str, Sequence[str]]]],
        *, active: Tuple[int, int] = (0, 0)) -> str:
    """
    PC 좌측 네비.
    items: ["메뉴1", ("메뉴2", ["서브1", "서브2"]), ...]
    active: (parent_idx, child_idx) — child_idx는 sub menu 활성 (없으면 -1)
    """
    rows_html = ''
    for i, item in enumerate(items):
        is_active = i == active[0]
        if isinstance(item, tuple):
            title, children = item
            row_bg = 'var(--krds-primary-5)' if is_active else 'transparent'
            row_color = 'var(--krds-primary-50)' if is_active else 'var(--krds-gray-90)'
            rows_html += (
                f'<div style="padding:12px 16px; font-size:15px; '
                f'font-weight:600; color:{row_color}; '
                f'background:{row_bg}; cursor:pointer;">{title}</div>'
            )
            if is_active:
                for j, child in enumerate(children):
                    sub_active = j == active[1]
                    sub_color = 'var(--krds-primary-50)' if sub_active else 'var(--krds-gray-60)'
                    sub_weight = '600' if sub_active else '400'
                    rows_html += (
                        f'<div style="padding:8px 32px; font-size:14px; '
                        f'color:{sub_color}; font-weight:{sub_weight}; '
                        f'cursor:pointer;">{child}</div>'
                    )
        else:
            color = 'var(--krds-primary-50)' if is_active else 'var(--krds-gray-90)'
            weight = '600' if is_active else '500'
            bg = 'var(--krds-primary-5)' if is_active else 'transparent'
            rows_html += (
                f'<div style="padding:12px 16px; font-size:15px; '
                f'color:{color}; font-weight:{weight}; '
                f'background:{bg}; cursor:pointer;">{item}</div>'
            )

    return (
        f'<aside class="krds-lnb" data-num="{num}" '
        f'style="position:relative; width:240px; flex-shrink:0; '
        f'background:var(--krds-gray-0); '
        f'border-right:1px solid var(--krds-gray-10); '
        f'padding:24px 0;">'
        + num_badge(num, edge=True) +
        rows_html +
        f'</aside>'
    )


# ─── 3) Container (PC 페이지 컨테이너) ──────────────────────

def container(content_html: str, *, max_width: int = 1440) -> str:
    """PC 페이지 컨테이너 (max-width + 가운데 정렬)."""
    return (
        f'<div class="krds-container" '
        f'style="max-width:{max_width}px; margin:0 auto; '
        f'padding:32px 40px;">'
        + content_html +
        f'</div>'
    )


# ─── 4) Page Title ─────────────────────────────────────────

def page_title(num: int, title: str, *,
               subtitle: Optional[str] = None,
               breadcrumb_items: Optional[Sequence[str]] = None) -> str:
    """페이지 타이틀 (+ 선택적 subtitle, breadcrumb)."""
    bc_html = ''
    if breadcrumb_items:
        bc_parts = []
        for i, item in enumerate(breadcrumb_items):
            color = 'var(--krds-gray-90)' if i == len(breadcrumb_items) - 1 else 'var(--krds-gray-50)'
            bc_parts.append(
                f'<span style="color:{color};">{item}</span>'
            )
        bc_html = (
            '<div style="font-size:13px; color:var(--krds-gray-50); '
            'margin-bottom:8px;">'
            + ' &gt; '.join(bc_parts) +
            '</div>'
        )

    sub_html = ''
    if subtitle:
        sub_html = (
            f'<div style="font-size:16px; color:var(--krds-gray-60); '
            f'margin-top:8px;">{subtitle}</div>'
        )

    return (
        f'<div class="krds-page-title" data-num="{num}" '
        f'style="position:relative; padding:0 0 24px; '
        f'border-bottom:1px solid var(--krds-gray-10); '
        f'margin-bottom:24px;">'
        + num_badge(num, edge=True) +
        bc_html +
        f'<div style="font-size:30px; font-weight:700; '
        f'color:var(--krds-gray-90);">{title}</div>'
        + sub_html +
        f'</div>'
    )


# ─── 5) Breadcrumb (별도 사용 시) ──────────────────────────

def breadcrumb(num: int, items: Sequence[str]) -> str:
    parts = []
    for i, item in enumerate(items):
        color = 'var(--krds-gray-90)' if i == len(items) - 1 else 'var(--krds-gray-50)'
        weight = '600' if i == len(items) - 1 else '400'
        parts.append(
            f'<span style="color:{color}; font-weight:{weight};">{item}</span>'
        )
    return (
        f'<div data-num="{num}" '
        f'style="position:relative; font-size:13px; margin-bottom:16px;">'
        + num_badge(num, edge=True) +
        ' &gt; '.join(parts) +
        f'</div>'
    )


# ─── 6) Data Table ─────────────────────────────────────────

def data_table(num: int, columns: Sequence[str], rows: Sequence[Sequence[str]],
               *, action_label: Optional[str] = None) -> str:
    """
    KRDS 데이터 테이블.
    columns: ["번호", "제목", "작성자", "작성일"]
    rows: 각 row는 columns와 같은 길이의 list
    action_label: 행마다 우측 액션 버튼 라벨 (예: "수정"). None이면 액션 칸 없음
    """
    thead_html = ''
    for col in columns:
        thead_html += (
            f'<th style="padding:12px 16px; font-size:14px; font-weight:700; '
            f'color:var(--krds-gray-70); text-align:left; '
            f'border-bottom:2px solid var(--krds-gray-20); '
            f'background:var(--krds-gray-5);">{col}</th>'
        )
    if action_label:
        thead_html += (
            f'<th style="padding:12px 16px; font-size:14px; font-weight:700; '
            f'color:var(--krds-gray-70); text-align:center; width:100px; '
            f'border-bottom:2px solid var(--krds-gray-20); '
            f'background:var(--krds-gray-5);"></th>'
        )

    tbody_html = ''
    for row in rows:
        cells = ''
        for cell in row:
            cells += (
                f'<td style="padding:14px 16px; font-size:14px; '
                f'color:var(--krds-gray-90); '
                f'border-bottom:1px solid var(--krds-gray-10);">{cell}</td>'
            )
        if action_label:
            cells += (
                f'<td style="padding:10px 16px; text-align:center; '
                f'border-bottom:1px solid var(--krds-gray-10);">'
                f'<button style="padding:6px 14px; font-size:13px; '
                f'border:1px solid var(--krds-gray-20); '
                f'background:var(--krds-gray-0); border-radius:4px; '
                f'cursor:pointer;">{action_label}</button></td>'
            )
        tbody_html += f'<tr>{cells}</tr>'

    return (
        f'<table class="krds-table" data-num="{num}" '
        f'style="position:relative; width:100%; border-collapse:collapse; '
        f'background:var(--krds-gray-0);">'
        + num_badge(num, edge=True) +
        f'<thead><tr>{thead_html}</tr></thead>'
        f'<tbody>{tbody_html}</tbody>'
        f'</table>'
    )


# ─── 7) Pagination (숫자) ─────────────────────────────────

def pagination(num: int, current: int, total: int) -> str:
    """숫자 페이지네이션 (PC)."""
    btn_style = (
        'min-width:32px; height:32px; padding:0 8px; font-size:14px; '
        'background:var(--krds-gray-0); border:1px solid var(--krds-gray-20); '
        'border-radius:4px; color:var(--krds-gray-90); cursor:pointer; '
        'display:inline-flex; align-items:center; justify-content:center;'
    )
    active_style = (
        'min-width:32px; height:32px; padding:0 8px; font-size:14px; '
        'font-weight:700; background:var(--krds-primary-50); '
        'border:1px solid var(--krds-primary-50); border-radius:4px; '
        'color:var(--krds-gray-0); cursor:pointer; '
        'display:inline-flex; align-items:center; justify-content:center;'
    )

    buttons = [f'<button style="{btn_style}">‹</button>']
    # 간단화: 1..total 모두 표시 (total이 큰 경우 ... 처리는 호출자가 처리)
    show = list(range(1, total + 1)) if total <= 10 else (
        [1, 2, 3, '...', total - 2, total - 1, total]
    )
    for p in show:
        if p == '...':
            buttons.append('<span style="padding:0 6px;">...</span>')
        elif p == current:
            buttons.append(f'<button style="{active_style}">{p}</button>')
        else:
            buttons.append(f'<button style="{btn_style}">{p}</button>')
    buttons.append(f'<button style="{btn_style}">›</button>')

    return (
        f'<div class="krds-pagination" data-num="{num}" '
        f'style="position:relative; display:flex; gap:4px; '
        f'justify-content:center; align-items:center; '
        f'padding:24px 0;">'
        + num_badge(num, edge=True) +
        ''.join(buttons) +
        f'</div>'
    )


# ─── 8) Primary Button ─────────────────────────────────────

def primary_btn(num: int, text: str, *,
                disabled: bool = False,
                size: str = "md") -> str:
    """주요 액션 버튼 (PC). size: 'sm'(36) | 'md'(44) | 'lg'(48)"""
    h = {'sm': 36, 'md': 44, 'lg': 48}[size]
    fs = {'sm': 13, 'md': 14, 'lg': 16}[size]
    bg = 'var(--krds-gray-20)' if disabled else 'var(--krds-primary-50)'
    return (
        f'<div data-num="{num}" '
        f'style="position:relative; display:inline-block;">'
        + num_badge(num, edge=True) +
        f'<button style="height:{h}px; padding:0 24px; font-size:{fs}px; '
        f'font-weight:600; background:{bg}; color:var(--krds-gray-0); '
        f'border:none; border-radius:6px; cursor:pointer;">{text}</button>'
        f'</div>'
    )


# ─── 9) Secondary Button ──────────────────────────────────

def secondary_btn(num: int, text: str, *, size: str = "md") -> str:
    h = {'sm': 36, 'md': 44, 'lg': 48}[size]
    fs = {'sm': 13, 'md': 14, 'lg': 16}[size]
    return (
        f'<div data-num="{num}" '
        f'style="position:relative; display:inline-block;">'
        + num_badge(num, edge=True) +
        f'<button style="height:{h}px; padding:0 24px; font-size:{fs}px; '
        f'font-weight:600; background:var(--krds-gray-0); '
        f'color:var(--krds-gray-90); border:1px solid var(--krds-gray-20); '
        f'border-radius:6px; cursor:pointer;">{text}</button>'
        f'</div>'
    )


# ─── 10) Text Input (라벨 좌측 또는 상단) ─────────────────

def text_input(num: int, label: str, *,
               placeholder: str = "",
               value: str = "",
               input_type: str = "text",
               required: bool = False,
               width: Union[int, str] = "100%") -> str:
    """입력 필드. label은 상단 표시 (PC 표준)."""
    w = f'{width}px' if isinstance(width, int) else width
    req_mark = ' <span style="color:var(--krds-danger-50);">*</span>' if required else ''
    val_attr = f'value="{value}"' if value else ''
    return (
        f'<div data-num="{num}" '
        f'style="position:relative; margin-bottom:20px;">'
        + num_badge(num, edge=True) +
        f'<label style="display:block; font-size:14px; font-weight:600; '
        f'color:var(--krds-gray-90); margin-bottom:8px;">{label}{req_mark}</label>'
        f'<input type="{input_type}" placeholder="{placeholder}" {val_attr} '
        f'style="width:{w}; min-width:0; box-sizing:border-box; '
        f'height:44px; padding:0 16px; font-size:14px; '
        f'color:var(--krds-gray-90); '
        f'background:var(--krds-gray-0); '
        f'border:1px solid var(--krds-gray-20); border-radius:6px;">'
        f'</div>'
    )


# ─── 11) Select Field ────────────────────────────────────

def select_field(num: int, label: str, *,
                 options: Sequence[str] = (),
                 placeholder: str = "선택",
                 required: bool = False,
                 width: Union[int, str] = "100%") -> str:
    w = f'{width}px' if isinstance(width, int) else width
    req_mark = ' <span style="color:var(--krds-danger-50);">*</span>' if required else ''
    opts = f'<option value="">{placeholder}</option>'
    for opt in options:
        opts += f'<option value="{opt}">{opt}</option>'
    return (
        f'<div data-num="{num}" '
        f'style="position:relative; margin-bottom:20px;">'
        + num_badge(num, edge=True) +
        f'<label style="display:block; font-size:14px; font-weight:600; '
        f'color:var(--krds-gray-90); margin-bottom:8px;">{label}{req_mark}</label>'
        f'<select style="width:{w}; min-width:0; box-sizing:border-box; '
        f'height:44px; padding:0 16px; font-size:14px; '
        f'color:var(--krds-gray-90); '
        f'background:var(--krds-gray-0); '
        f'border:1px solid var(--krds-gray-20); border-radius:6px; '
        f'appearance:none;">{opts}</select>'
        f'</div>'
    )


# ─── 12) Card ─────────────────────────────────────────────

def card(num: int, body_html: str, *,
         title: Optional[str] = None,
         footer_html: Optional[str] = None) -> str:
    title_html = ''
    if title:
        title_html = (
            f'<div style="padding:16px 20px; '
            f'border-bottom:1px solid var(--krds-gray-10); '
            f'font-size:16px; font-weight:700; '
            f'color:var(--krds-gray-90);">{title}</div>'
        )
    footer_block = ''
    if footer_html:
        footer_block = (
            f'<div style="padding:16px 20px; '
            f'border-top:1px solid var(--krds-gray-10); '
            f'background:var(--krds-gray-5);">{footer_html}</div>'
        )
    return (
        f'<div class="krds-card" data-num="{num}" '
        f'style="position:relative; background:var(--krds-gray-0); '
        f'border:1px solid var(--krds-gray-10); border-radius:8px; '
        f'overflow:hidden;">'
        + num_badge(num, edge=True) +
        title_html +
        f'<div style="padding:20px;">{body_html}</div>'
        + footer_block +
        f'</div>'
    )


# ─── 13) Filter Bar (검색/필터/액션 한 줄) ─────────────────

def filter_bar(num: int, *,
               search_placeholder: str = "",
               filters: Sequence[Tuple[str, Sequence[str]]] = (),
               action_btn: Optional[str] = None) -> str:
    """
    filters: [("상태", ["전체", "공지", "이벤트"]), ...]
    action_btn: 우측 primary action 라벨 (예: "글쓰기")
    """
    filter_html = ''
    for label, opts in filters:
        opts_html = ''.join(f'<option>{o}</option>' for o in opts)
        filter_html += (
            f'<select style="height:40px; padding:0 12px; font-size:14px; '
            f'border:1px solid var(--krds-gray-20); border-radius:6px; '
            f'background:var(--krds-gray-0); '
            f'color:var(--krds-gray-90); min-width:120px;">'
            f'<option value="">{label}</option>{opts_html}</select>'
        )

    search_html = ''
    if search_placeholder:
        search_html = (
            f'<input type="text" placeholder="{search_placeholder}" '
            f'style="flex:1; min-width:200px; height:40px; padding:0 16px; '
            f'font-size:14px; border:1px solid var(--krds-gray-20); '
            f'border-radius:6px; box-sizing:border-box;">'
        )

    action_html = ''
    if action_btn:
        action_html = (
            f'<button style="height:40px; padding:0 20px; font-size:14px; '
            f'font-weight:600; background:var(--krds-primary-50); '
            f'color:var(--krds-gray-0); border:none; border-radius:6px; '
            f'cursor:pointer;">{action_btn}</button>'
        )

    return (
        f'<div data-num="{num}" '
        f'style="position:relative; display:flex; gap:8px; '
        f'align-items:center; margin-bottom:16px;">'
        + num_badge(num, edge=True) +
        filter_html + search_html + action_html +
        f'</div>'
    )


# ─── 14) Empty State ──────────────────────────────────────

def empty_state(num: int, message: str, *,
                action_label: Optional[str] = None) -> str:
    action_html = ''
    if action_label:
        action_html = (
            f'<button style="margin-top:16px; height:44px; padding:0 24px; '
            f'font-size:14px; font-weight:600; '
            f'background:var(--krds-primary-50); color:var(--krds-gray-0); '
            f'border:none; border-radius:6px; cursor:pointer;">'
            f'{action_label}</button>'
        )
    return (
        f'<div data-num="{num}" '
        f'style="position:relative; text-align:center; padding:80px 24px; '
        f'background:var(--krds-gray-5); border-radius:8px;">'
        + num_badge(num, edge=True) +
        f'<div style="font-size:16px; color:var(--krds-gray-60); '
        f'line-height:1.6;">{message}</div>'
        + action_html +
        f'</div>'
    )


# ─── 15) Dialog (sub-canvas 내부에서 사용) ─────────────────

def dialog(num: int, title: str, body: str,
           buttons: Sequence[Tuple[str, str]]) -> str:
    """
    sub-canvas 안에 들어가는 다이얼로그 컨텐츠.
    buttons: [("계속 진행", "secondary"), ("취소하기", "primary")] — (라벨, type)
    """
    btn_html = ''
    for label, btn_type in buttons:
        if btn_type == "primary":
            btn_html += (
                f'<button style="flex:1; min-width:0; height:48px; '
                f'background:var(--krds-primary-50); color:var(--krds-gray-0); '
                f'border:none; border-radius:6px; font-size:15px; '
                f'font-weight:600; cursor:pointer;">{label}</button>'
            )
        else:
            btn_html += (
                f'<button style="flex:1; min-width:0; height:48px; '
                f'background:var(--krds-gray-0); '
                f'color:var(--krds-gray-70); '
                f'border:1px solid var(--krds-gray-20); border-radius:6px; '
                f'font-size:15px; font-weight:600; cursor:pointer;">{label}</button>'
            )

    return (
        # 딤 배경 (가이드 §10.3 풀스크린 규칙)
        f'<div style="position:absolute; inset:0; '
        f'background:rgba(0,0,0,.4); display:flex; align-items:center; '
        f'justify-content:center; border-radius:8px;">'
        f'<div style="background:var(--krds-gray-0); border-radius:12px; '
        f'width:480px; padding:32px 28px;">'
        f'<div data-num="{num}" '
        f'style="position:relative; margin-bottom:24px;">'
        + num_badge(num) +
        f'<div style="font-size:18px; font-weight:700; '
        f'color:var(--krds-gray-90); margin-bottom:8px;">{title}</div>'
        f'<div style="font-size:14px; color:var(--krds-gray-60); '
        f'line-height:1.6;">{body}</div>'
        f'</div>'
        f'<div style="display:flex; gap:8px;">{btn_html}</div>'
        f'</div>'
        f'</div>'
    )

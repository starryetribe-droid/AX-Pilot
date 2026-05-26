"""
Mobile variant — KRDS 디자인 시스템 구현.

함수 시그니처는 DS-agnostic (의미 기반). 추후 자사 DS로 교체 시
이 파일을 `mobile_etribe.py` 같은 새 어댑터로 대체하고 __init__.py만 수정.

모든 색상은 CSS 변수(--krds-*)로 작성. 사이즈는 모바일 가이드 §11.2 타이포
기준 (헤더 16/600, 페이지 타이틀 22/700, 입력 16/400, 버튼 16/600).

PC 어댑터(pc_krds.py)와 가능한 한 동일한 함수 이름을 사용:
  - page_title, card, primary_btn, secondary_btn, text_input, select_field
  - pagination, empty_state, dialog, breadcrumb
모바일 고유 컴포넌트:
  - app_bar (PC의 gnb 대응), bottom_nav (PC의 lnb 대응)
  - tab_bar, fab, filter_chips, search_bar, bottom_sheet
  - 채팅 인터페이스: bot_msg, user_msg, quick_btns, input_bar
"""
from typing import List, Optional, Sequence, Tuple, Union
from ._base import num_badge, icon_ph


# ╔════════════════════════════════════════════════════════════╗
# ║ Header / Navigation                                         ║
# ╚════════════════════════════════════════════════════════════╝

def app_bar(num: int, title: str, *,
            back: bool = False,
            close: bool = False,
            right_action: Optional[str] = None) -> str:
    """
    모바일 상단 헤더 (52px). PC의 gnb 대응.
    back=True: 좌측 ← / close=True: 우측 ✕
    right_action: 우측에 텍스트/링크 액션 (예: "완료")
    """
    left_html = ''
    if back:
        left_html = (
            '<button style="width:44px; height:44px; border:none; '
            'background:none; font-size:20px; color:var(--krds-gray-90); '
            'cursor:pointer;">←</button>'
        )
    else:
        left_html = '<span style="width:44px; height:44px;"></span>'

    right_html = ''
    if close:
        right_html = (
            '<button style="width:44px; height:44px; border:none; '
            'background:none; font-size:18px; color:var(--krds-gray-90); '
            'cursor:pointer;">✕</button>'
        )
    elif right_action:
        right_html = (
            f'<button style="height:44px; padding:0 12px; border:none; '
            f'background:none; font-size:14px; font-weight:600; '
            f'color:var(--krds-primary-50); cursor:pointer;">'
            f'{right_action}</button>'
        )
    else:
        right_html = '<span style="width:44px; height:44px;"></span>'

    return (
        f'<div class="krds-app-bar" data-num="{num}" '
        f'style="position:relative; height:52px; '
        f'background:var(--krds-gray-0); '
        f'border-bottom:1px solid var(--krds-gray-10); '
        f'display:flex; align-items:center; padding:0 4px; '
        f'flex-shrink:0;">'
        + num_badge(num, edge=True) +
        left_html +
        f'<span style="flex:1; text-align:center; font-size:16px; '
        f'font-weight:600; color:var(--krds-gray-90);">{title}</span>'
        + right_html +
        f'</div>'
    )


def bottom_nav(num: int, items: Sequence[str], *,
               active_idx: int = 0) -> str:
    """
    하단 탭 네비 (3-5개). PC의 lnb 대응.
    각 항목은 [아이콘 자리 placeholder + 라벨].
    """
    tabs_html = ''
    for i, label in enumerate(items):
        active = i == active_idx
        color = 'var(--krds-primary-50)' if active else 'var(--krds-gray-50)'
        weight = '600' if active else '400'
        tabs_html += (
            f'<div style="flex:1; display:flex; flex-direction:column; '
            f'align-items:center; justify-content:center; gap:4px; '
            f'padding:8px 0; cursor:pointer;">'
            + icon_ph(20) +
            f'<span style="font-size:11px; color:{color}; '
            f'font-weight:{weight};">{label}</span>'
            f'</div>'
        )

    return (
        f'<nav data-num="{num}" '
        f'style="position:relative; height:64px; '
        f'background:var(--krds-gray-0); '
        f'border-top:1px solid var(--krds-gray-10); '
        f'display:flex; align-items:stretch; flex-shrink:0;">'
        + num_badge(num, edge=True) +
        tabs_html +
        f'</nav>'
    )


def tab_bar(num: int, tabs: Sequence[str], *,
            active_idx: int = 0) -> str:
    """상단 탭바 (앱바 아래). PC의 tab 대응."""
    tabs_html = ''
    for i, label in enumerate(tabs):
        active = i == active_idx
        color = 'var(--krds-gray-90)' if active else 'var(--krds-gray-50)'
        weight = '700' if active else '500'
        border = '2px solid var(--krds-primary-50)' if active else '2px solid transparent'
        tabs_html += (
            f'<div style="flex:1; padding:12px 16px; text-align:center; '
            f'font-size:14px; color:{color}; font-weight:{weight}; '
            f'border-bottom:{border}; cursor:pointer;">{label}</div>'
        )
    return (
        f'<div data-num="{num}" '
        f'style="position:relative; display:flex; '
        f'background:var(--krds-gray-0); '
        f'border-bottom:1px solid var(--krds-gray-10);">'
        + num_badge(num, edge=True) +
        tabs_html +
        f'</div>'
    )


def breadcrumb(num: int, items: Sequence[str]) -> str:
    """모바일 브레드크럼 (드물게 사용). PC와 동일 시그니처."""
    parts = []
    for i, item in enumerate(items):
        color = 'var(--krds-gray-90)' if i == len(items) - 1 else 'var(--krds-gray-50)'
        parts.append(f'<span style="color:{color};">{item}</span>')
    return (
        f'<div data-num="{num}" '
        f'style="position:relative; font-size:12px; padding:8px 16px;">'
        + num_badge(num, edge=True) +
        ' &gt; '.join(parts) +
        f'</div>'
    )


# ╔════════════════════════════════════════════════════════════╗
# ║ Page Layout                                                 ║
# ╚════════════════════════════════════════════════════════════╝

def page_title(num: int, title: str, *,
               subtitle: Optional[str] = None) -> str:
    """페이지 타이틀 (22px). PC와 동일 시그니처 (breadcrumb_items만 모바일 미지원)."""
    sub_html = ''
    if subtitle:
        sub_html = (
            f'<div style="font-size:14px; color:var(--krds-gray-60); '
            f'margin-top:4px;">{subtitle}</div>'
        )
    return (
        f'<div class="krds-page-title" data-num="{num}" '
        f'style="position:relative; padding:16px;">'
        + num_badge(num, edge=True) +
        f'<div style="font-size:22px; font-weight:700; '
        f'color:var(--krds-gray-90);">{title}</div>'
        + sub_html +
        f'</div>'
    )


# ╔════════════════════════════════════════════════════════════╗
# ║ Data Display                                                ║
# ╚════════════════════════════════════════════════════════════╝

def card_list(num: int, items: Sequence[dict]) -> str:
    """
    카드 리스트 (PC의 data_table 모바일 대응).
    items: [{"title": "...", "subtitle": "...", "meta": "...", "right": "..."}, ...]
    """
    cards = ''
    for item in items:
        sub = item.get('subtitle')
        meta = item.get('meta')
        right = item.get('right')
        sub_html = (
            f'<div style="font-size:13px; color:var(--krds-gray-60); '
            f'margin-top:4px;">{sub}</div>' if sub else ''
        )
        meta_html = (
            f'<div style="font-size:12px; color:var(--krds-gray-50); '
            f'margin-top:6px;">{meta}</div>' if meta else ''
        )
        right_html = (
            f'<span style="font-size:13px; color:var(--krds-gray-50); '
            f'flex-shrink:0;">{right}</span>' if right else ''
        )
        cards += (
            f'<div style="display:flex; align-items:flex-start; gap:12px; '
            f'padding:14px 16px; background:var(--krds-gray-0); '
            f'border-bottom:1px solid var(--krds-gray-10);">'
            f'<div style="flex:1; min-width:0;">'
            f'<div style="font-size:15px; font-weight:600; '
            f'color:var(--krds-gray-90);">{item["title"]}</div>'
            + sub_html + meta_html +
            f'</div>' + right_html +
            f'</div>'
        )
    return (
        f'<div data-num="{num}" '
        f'style="position:relative; background:var(--krds-gray-0);">'
        + num_badge(num, edge=True) +
        cards +
        f'</div>'
    )


def list_item(num: int, title: str, *,
              subtitle: Optional[str] = None,
              meta: Optional[str] = None,
              right_text: Optional[str] = None,
              chevron: bool = True) -> str:
    """단일 리스트 항목."""
    sub_html = (
        f'<div style="font-size:13px; color:var(--krds-gray-60); '
        f'margin-top:4px;">{subtitle}</div>' if subtitle else ''
    )
    meta_html = (
        f'<div style="font-size:12px; color:var(--krds-gray-50); '
        f'margin-top:6px;">{meta}</div>' if meta else ''
    )
    right_block = ''
    if right_text:
        right_block += (
            f'<span style="font-size:13px; color:var(--krds-gray-50); '
            f'flex-shrink:0;">{right_text}</span>'
        )
    if chevron:
        right_block += (
            '<span style="color:var(--krds-gray-30); font-size:18px; '
            'flex-shrink:0;">›</span>'
        )

    return (
        f'<div data-num="{num}" '
        f'style="position:relative; display:flex; align-items:center; '
        f'gap:12px; padding:14px 16px; '
        f'background:var(--krds-gray-0); '
        f'border-bottom:1px solid var(--krds-gray-10);">'
        + num_badge(num, edge=True) +
        f'<div style="flex:1; min-width:0;">'
        f'<div style="font-size:15px; font-weight:600; '
        f'color:var(--krds-gray-90);">{title}</div>'
        + sub_html + meta_html +
        f'</div>' + right_block +
        f'</div>'
    )


def card(num: int, body_html: str, *,
         title: Optional[str] = None,
         footer_html: Optional[str] = None) -> str:
    """카드. PC와 동일 시그니처."""
    title_html = ''
    if title:
        title_html = (
            f'<div style="padding:14px 16px; '
            f'border-bottom:1px solid var(--krds-gray-10); '
            f'font-size:15px; font-weight:700; '
            f'color:var(--krds-gray-90);">{title}</div>'
        )
    footer_block = ''
    if footer_html:
        footer_block = (
            f'<div style="padding:12px 16px; '
            f'border-top:1px solid var(--krds-gray-10); '
            f'background:var(--krds-gray-5);">{footer_html}</div>'
        )
    return (
        f'<div data-num="{num}" '
        f'style="position:relative; margin:0 16px; '
        f'background:var(--krds-gray-0); '
        f'border:1px solid var(--krds-gray-10); border-radius:8px; '
        f'overflow:hidden;">'
        + num_badge(num, edge=True) +
        title_html +
        f'<div style="padding:14px 16px;">{body_html}</div>'
        + footer_block +
        f'</div>'
    )


def pagination(num: int, current: int, total: int) -> str:
    """
    모바일 페이지네이션 (prev/next 단순형). PC와 동일 시그니처.
    모바일은 무한스크롤이 일반적이지만 PC와의 콘텐츠 동일성 위해 동일 시그니처 제공.
    """
    btn_style = (
        'min-width:36px; height:36px; padding:0 8px; font-size:13px; '
        'background:var(--krds-gray-0); border:1px solid var(--krds-gray-20); '
        'border-radius:4px; color:var(--krds-gray-90); cursor:pointer; '
        'display:inline-flex; align-items:center; justify-content:center;'
    )
    return (
        f'<div data-num="{num}" '
        f'style="position:relative; display:flex; gap:6px; '
        f'justify-content:center; padding:16px;">'
        + num_badge(num, edge=True) +
        f'<button style="{btn_style}">‹</button>'
        f'<span style="display:inline-flex; align-items:center; '
        f'padding:0 12px; font-size:13px; color:var(--krds-gray-70);">'
        f'{current} / {total}</span>'
        f'<button style="{btn_style}">›</button>'
        f'</div>'
    )


def empty_state(num: int, message: str, *,
                action_label: Optional[str] = None) -> str:
    """빈 상태. PC와 동일 시그니처."""
    action_html = ''
    if action_label:
        action_html = (
            f'<button style="margin-top:16px; height:44px; padding:0 24px; '
            f'font-size:14px; font-weight:600; '
            f'background:var(--krds-primary-50); color:var(--krds-gray-0); '
            f'border:none; border-radius:8px; cursor:pointer;">'
            f'{action_label}</button>'
        )
    return (
        f'<div data-num="{num}" '
        f'style="position:relative; text-align:center; padding:60px 24px; '
        f'background:var(--krds-gray-5);">'
        + num_badge(num, edge=True) +
        f'<div style="font-size:14px; color:var(--krds-gray-60); '
        f'line-height:1.6;">{message}</div>'
        + action_html +
        f'</div>'
    )


# ╔════════════════════════════════════════════════════════════╗
# ║ Forms                                                       ║
# ╚════════════════════════════════════════════════════════════╝

def text_input(num: int, label: str, *,
               placeholder: str = "",
               value: str = "",
               input_type: str = "text",
               required: bool = False) -> str:
    """입력 필드 (라벨 상단). PC와 동일 시그니처."""
    req_mark = ' <span style="color:var(--krds-danger-50);">*</span>' if required else ''
    val_attr = f'value="{value}"' if value else ''
    return (
        f'<div data-num="{num}" '
        f'style="position:relative; padding:0 16px; margin-bottom:16px;">'
        + num_badge(num, edge=True) +
        f'<label style="display:block; font-size:13px; font-weight:600; '
        f'color:var(--krds-gray-90); margin-bottom:6px;">{label}{req_mark}</label>'
        f'<input type="{input_type}" placeholder="{placeholder}" {val_attr} '
        f'style="width:100%; min-width:0; box-sizing:border-box; '
        f'height:48px; padding:0 16px; font-size:16px; '
        f'color:var(--krds-gray-90); '
        f'background:var(--krds-gray-0); '
        f'border:1px solid var(--krds-gray-20); border-radius:8px;">'
        f'</div>'
    )


def select_field(num: int, label: str, *,
                 options: Sequence[str] = (),
                 placeholder: str = "선택",
                 required: bool = False) -> str:
    """셀렉트. PC와 동일 시그니처."""
    req_mark = ' <span style="color:var(--krds-danger-50);">*</span>' if required else ''
    opts = f'<option value="">{placeholder}</option>'
    for opt in options:
        opts += f'<option value="{opt}">{opt}</option>'
    return (
        f'<div data-num="{num}" '
        f'style="position:relative; padding:0 16px; margin-bottom:16px;">'
        + num_badge(num, edge=True) +
        f'<label style="display:block; font-size:13px; font-weight:600; '
        f'color:var(--krds-gray-90); margin-bottom:6px;">{label}{req_mark}</label>'
        f'<select style="width:100%; min-width:0; box-sizing:border-box; '
        f'height:48px; padding:0 16px; font-size:16px; '
        f'color:var(--krds-gray-90); '
        f'background:var(--krds-gray-0); '
        f'border:1px solid var(--krds-gray-20); border-radius:8px; '
        f'appearance:none;">{opts}</select>'
        f'</div>'
    )


def checkbox_group(num: int, items: Sequence[str]) -> str:
    """체크박스 그룹 (세로 나열)."""
    checks = ''
    for item in items:
        checks += (
            '<label style="display:flex; align-items:center; gap:8px; '
            'padding:12px; background:var(--krds-gray-0); border-radius:8px; '
            'border:1px solid var(--krds-gray-10); cursor:pointer; '
            'font-size:14px; color:var(--krds-gray-90);">'
            '<input type="checkbox" '
            'style="width:20px; height:20px; '
            'accent-color:var(--krds-primary-50);">'
            f'<span>{item}</span>'
            '</label>'
        )
    return (
        f'<div data-num="{num}" '
        f'style="position:relative; padding:0 16px; display:flex; '
        f'flex-direction:column; gap:8px;">'
        + num_badge(num) +
        checks +
        f'</div>'
    )


def radio_group(num: int, items: Sequence[str], *,
                group_name: str = "rg") -> str:
    """라디오 그룹."""
    radios = ''
    for i, item in enumerate(items):
        radios += (
            f'<label style="display:flex; align-items:center; gap:8px; '
            f'padding:12px; background:var(--krds-gray-0); border-radius:8px; '
            f'border:1px solid var(--krds-gray-10); cursor:pointer; '
            f'font-size:14px; color:var(--krds-gray-90);">'
            f'<input type="radio" name="{group_name}{num}" '
            f'style="width:20px; height:20px; '
            f'accent-color:var(--krds-primary-50);">'
            f'<span>{item}</span>'
            f'</label>'
        )
    return (
        f'<div data-num="{num}" '
        f'style="position:relative; padding:0 16px; display:flex; '
        f'flex-direction:column; gap:8px;">'
        + num_badge(num) +
        radios +
        f'</div>'
    )


# ╔════════════════════════════════════════════════════════════╗
# ║ Actions                                                     ║
# ╚════════════════════════════════════════════════════════════╝

def primary_btn(num: int, text: str, *,
                disabled: bool = False,
                size: str = "md") -> str:
    """주요 버튼 (가로 풀 너비). PC와 동일 시그니처."""
    h = {'sm': 40, 'md': 48, 'lg': 52}[size]
    fs = {'sm': 14, 'md': 16, 'lg': 16}[size]
    bg = 'var(--krds-gray-20)' if disabled else 'var(--krds-primary-50)'
    return (
        f'<div data-num="{num}" '
        f'style="position:relative; padding:0 16px;">'
        + num_badge(num, edge=True) +
        f'<button style="width:100%; height:{h}px; font-size:{fs}px; '
        f'font-weight:600; background:{bg}; color:var(--krds-gray-0); '
        f'border:none; border-radius:8px; cursor:pointer;">{text}</button>'
        f'</div>'
    )


def secondary_btn(num: int, text: str, *, size: str = "md") -> str:
    """보조 버튼."""
    h = {'sm': 40, 'md': 48, 'lg': 52}[size]
    fs = {'sm': 14, 'md': 15, 'lg': 16}[size]
    return (
        f'<div data-num="{num}" '
        f'style="position:relative; padding:0 16px;">'
        + num_badge(num, edge=True) +
        f'<button style="width:100%; height:{h}px; font-size:{fs}px; '
        f'font-weight:600; background:var(--krds-gray-0); '
        f'color:var(--krds-primary-50); '
        f'border:1px solid var(--krds-primary-50); border-radius:8px; '
        f'cursor:pointer;">{text}</button>'
        f'</div>'
    )


def fab(num: int, *, label: str = "") -> str:
    """우하단 FAB (플로팅 버튼). label 비우면 아이콘 자리만."""
    inner = label if label else icon_ph(24)
    return (
        f'<div data-num="{num}" '
        f'style="position:absolute; right:16px; bottom:80px; z-index:5;">'
        + num_badge(num, edge=True) +
        f'<button style="width:56px; height:56px; border-radius:50%; '
        f'background:var(--krds-primary-50); color:var(--krds-gray-0); '
        f'border:none; box-shadow:0 4px 12px rgba(0,0,0,.16); '
        f'cursor:pointer; font-size:24px; display:flex; '
        f'align-items:center; justify-content:center;">{inner}</button>'
        f'</div>'
    )


# ╔════════════════════════════════════════════════════════════╗
# ║ Filter / Search                                             ║
# ╚════════════════════════════════════════════════════════════╝

def filter_chips(num: int, items: Sequence[str], *,
                 active_idx: int = 0) -> str:
    """필터 칩 (가로 스크롤 가능 가정). PC의 filter_bar 모바일 대응."""
    chips_html = ''
    for i, label in enumerate(items):
        active = i == active_idx
        bg = 'var(--krds-primary-50)' if active else 'var(--krds-gray-0)'
        color = 'var(--krds-gray-0)' if active else 'var(--krds-gray-70)'
        border = 'var(--krds-primary-50)' if active else 'var(--krds-gray-20)'
        chips_html += (
            f'<button style="height:36px; padding:0 14px; font-size:13px; '
            f'font-weight:500; background:{bg}; color:{color}; '
            f'border:1px solid {border}; border-radius:18px; '
            f'cursor:pointer; flex-shrink:0;">{label}</button>'
        )
    return (
        f'<div data-num="{num}" '
        f'style="position:relative; display:flex; gap:8px; '
        f'padding:8px 16px; overflow-x:visible;">'
        + num_badge(num, edge=True) +
        chips_html +
        f'</div>'
    )


def search_bar(num: int, *, placeholder: str = "검색") -> str:
    """검색바."""
    return (
        f'<div data-num="{num}" '
        f'style="position:relative; padding:8px 16px;">'
        + num_badge(num, edge=True) +
        f'<div style="display:flex; align-items:center; gap:8px; '
        f'padding:0 14px; height:44px; background:var(--krds-gray-5); '
        f'border-radius:22px;">'
        + icon_ph(18) +
        f'<input type="text" placeholder="{placeholder}" '
        f'style="flex:1; min-width:0; border:none; background:transparent; '
        f'font-size:14px; color:var(--krds-gray-90);">'
        f'</div>'
        f'</div>'
    )


# ╔════════════════════════════════════════════════════════════╗
# ║ Dialog / Bottom Sheet (sub-canvas 내부에서 사용)            ║
# ╚════════════════════════════════════════════════════════════╝

def dialog(num: int, title: str, body: str,
           buttons: Sequence[Tuple[str, str]]) -> str:
    """
    모바일 다이얼로그. PC와 동일 시그니처.
    buttons: [("취소", "secondary"), ("확인", "primary")]
    """
    btn_html = ''
    for label, btn_type in buttons:
        if btn_type == "primary":
            btn_html += (
                f'<button style="flex:1; min-width:0; height:48px; '
                f'background:var(--krds-primary-50); '
                f'color:var(--krds-gray-0); border:none; border-radius:8px; '
                f'font-size:15px; font-weight:600; '
                f'cursor:pointer;">{label}</button>'
            )
        else:
            btn_html += (
                f'<button style="flex:1; min-width:0; height:48px; '
                f'background:var(--krds-gray-0); '
                f'color:var(--krds-gray-70); '
                f'border:1px solid var(--krds-gray-20); border-radius:8px; '
                f'font-size:15px; font-weight:600; '
                f'cursor:pointer;">{label}</button>'
            )

    return (
        # 딤 배경 (가이드 §10.3 풀스크린 규칙)
        f'<div style="position:absolute; inset:0; '
        f'background:rgba(0,0,0,.4); display:flex; align-items:center; '
        f'justify-content:center; border-radius:8px;">'
        f'<div style="background:var(--krds-gray-0); border-radius:12px; '
        f'width:320px; padding:24px 20px;">'
        f'<div data-num="{num}" '
        f'style="position:relative; margin-bottom:20px;">'
        + num_badge(num) +
        f'<div style="font-size:16px; font-weight:700; '
        f'color:var(--krds-gray-90); margin-bottom:6px; '
        f'text-align:center;">{title}</div>'
        f'<div style="font-size:14px; color:var(--krds-gray-60); '
        f'line-height:1.6; text-align:center;">{body}</div>'
        f'</div>'
        f'<div style="display:flex; gap:8px;">{btn_html}</div>'
        f'</div>'
        f'</div>'
    )


def bottom_sheet(num: int, title: str, body_html: str) -> str:
    """바텀시트 (모바일 고유). sub-canvas 안에서 사용."""
    return (
        f'<div style="position:absolute; inset:0; '
        f'background:rgba(0,0,0,.4); display:flex; '
        f'align-items:flex-end; border-radius:8px;">'
        f'<div style="width:100%; background:var(--krds-gray-0); '
        f'border-top-left-radius:16px; border-top-right-radius:16px; '
        f'padding:8px 0 24px;">'
        f'<div style="width:40px; height:4px; '
        f'background:var(--krds-gray-20); border-radius:2px; '
        f'margin:0 auto 16px;"></div>'
        f'<div data-num="{num}" '
        f'style="position:relative; padding:0 20px;">'
        + num_badge(num) +
        f'<div style="font-size:16px; font-weight:700; '
        f'color:var(--krds-gray-90); margin-bottom:12px;">{title}</div>'
        f'<div>{body_html}</div>'
        f'</div>'
        f'</div>'
        f'</div>'
    )


# ╔════════════════════════════════════════════════════════════╗
# ║ Chat Interface (대화형 화면 전용)                            ║
# ╚════════════════════════════════════════════════════════════╝

def chat_area_open() -> str:
    """채팅 메시지 영역 시작. close()와 짝지어 사용. ★ overflow:visible 필수 (가이드 §6.2)."""
    return (
        '<div style="flex:1; overflow:visible; padding:16px; '
        'background:var(--krds-gray-5); display:flex; '
        'flex-direction:column; gap:12px; min-height:600px;">'
    )


def chat_area_close() -> str:
    """채팅 메시지 영역 종료."""
    return '</div>'


def bot_msg(num: int, text: str) -> str:
    """봇 채팅 말풍선 (좌측, 회색). text에 이모지 포함 OK (채팅은 예외, 가이드 §6.5.1)."""
    return (
        f'<div data-num="{num}" '
        f'style="position:relative; display:flex; gap:8px; '
        f'align-items:flex-start;">'
        + num_badge(num) +
        f'<div style="width:32px; height:32px; border-radius:50%; '
        f'background:var(--krds-gray-20); flex-shrink:0;"></div>'
        f'<div style="max-width:70%; padding:10px 14px; '
        f'background:var(--krds-gray-0); border-radius:0 12px 12px 12px; '
        f'font-size:14px; color:var(--krds-gray-90); '
        f'line-height:1.5;">{text}</div>'
        f'</div>'
    )


def user_msg(text: str) -> str:
    """
    사용자 채팅 말풍선 (우측, primary). num 없음 — 사용자 메시지는
    번호 안 매김 (작성자가 직접 보낸 메시지이므로).
    """
    return (
        f'<div style="display:flex; justify-content:flex-end;">'
        f'<div style="max-width:70%; padding:10px 14px; '
        f'background:var(--krds-primary-50); '
        f'color:var(--krds-gray-0); border-radius:12px 0 12px 12px; '
        f'font-size:14px; line-height:1.5;">{text}</div>'
        f'</div>'
    )


def quick_btns(num: int, labels: Sequence[str]) -> str:
    """퀵리플라이 칩 (좌측 정렬, 봇 메시지 아래)."""
    btns = ''
    for label in labels:
        btns += (
            f'<button style="border:1px solid var(--krds-primary-50); '
            f'color:var(--krds-primary-50); background:var(--krds-gray-0); '
            f'border-radius:20px; padding:8px 16px; font-size:13px; '
            f'cursor:pointer; display:inline-flex; align-items:center; '
            f'gap:6px;">{label}</button>'
        )
    return (
        f'<div data-num="{num}" '
        f'style="position:relative; display:flex; gap:8px; '
        f'flex-wrap:wrap; padding-left:40px;">'
        + num_badge(num) +
        btns +
        f'</div>'
    )


def input_bar(num: int, *,
              placeholder: str = "메시지를 입력하세요...") -> str:
    """채팅 하단 입력바 (input + send button)."""
    return (
        f'<div data-num="{num}" '
        f'style="position:relative; border-top:1px solid var(--krds-gray-10); '
        f'padding:10px 16px; display:flex; gap:8px; '
        f'background:var(--krds-gray-0); flex-shrink:0;">'
        + num_badge(num, edge=True) +
        f'<input type="text" placeholder="{placeholder}" '
        f'style="flex:1; min-width:0; box-sizing:border-box; '
        f'border:1px solid var(--krds-gray-10); border-radius:20px; '
        f'padding:10px 16px; font-size:14px; '
        f'color:var(--krds-gray-90);">'
        f'<button style="width:44px; height:44px; border-radius:50%; '
        f'background:var(--krds-gray-10); border:none; display:flex; '
        f'align-items:center; justify-content:center; '
        f'color:var(--krds-gray-30); flex-shrink:0; font-size:18px;">↑</button>'
        f'</div>'
    )

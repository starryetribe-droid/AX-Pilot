"""
DS-agnostic SB 부품. 어떤 디자인 시스템(KRDS, 자사 DS 등)이든 동일한
구조를 갖는 패널 wrapper, 캔버스 wrap, num-badge HTML, description 헬퍼.

향후 자사 DS로 교체 시 이 파일은 수정 불필요 — adapter 파일(예: pc_krds.py)만
교체하면 됨.
"""
from typing import Optional, Tuple, List


# ─── 1) 화면 wrapper (wf-panel + desc-panel) ────────────────────

def wf_panel(canvas_html: str, desc: Tuple[str, str]) -> str:
    """한 화면 전체 wrapper. desc=(overview_html, detail_dl_html)."""
    overview, detail = desc
    return (
        '<div class="wf-panel">' + canvas_html + '</div>'
        '<div class="desc-panel">'
        + _desc_section("화면 설명", overview)
        + _desc_section("Description", detail)
        + '</div>'
    )


def _desc_section(header: str, body: str) -> str:
    return (
        '<div class="desc-section">'
        '<div class="desc-section-header">' + header + '</div>'
        '<div class="desc-section-body">' + body + '</div>'
        '</div>'
    )


# ─── 2) 캔버스 wrapper (variant별) ─────────────────────────────

def canvas_wrap(canvas_inner: str, *,
                variant: str = "pc",
                sub_canvas_html: str = "",
                connector_label: str = "",
                connector_top: int = 200) -> str:
    """
    .wf-canvas-wrap → .num-strip + .wf-canvas + (옵션) sub-canvas

    variant: 'pc' (1440min, max-2560, height auto) | 'mobile' (390×844min)
    sub_canvas_html: 모달/다이얼로그 메인 캔버스 우측 sub-canvas (옵션)
    connector_label: sub-canvas 트리거 라벨 칩 (예: "삭제 버튼 탭")
    connector_top: 트리거 요소 Y 좌표 (px)
    """
    if variant == "pc":
        canvas_style = (
            'width:100%; max-width:2560px; min-height:1440px; height:auto; '
            'background:var(--krds-gray-0); border-radius:8px; '
            'box-shadow:0 2px 16px rgba(0,0,0,.08); '
            'position:relative; overflow:visible;'
        )
        sub_width = 'width:100%; max-width:1200px;'
    else:
        canvas_style = (
            'width:390px; min-height:844px; '
            'background:var(--krds-gray-0); border-radius:8px; '
            'box-shadow:0 2px 16px rgba(0,0,0,.08); '
            'position:relative; overflow:visible; '
            'display:flex; flex-direction:column;'
        )
        sub_width = 'width:390px;'

    main = (
        '<div class="wf-canvas-wrap">'
        '<div class="num-strip"></div>'
        f'<div class="wf-canvas" style="{canvas_style}">'
        + canvas_inner +
        '</div>'
    )

    if sub_canvas_html:
        # ★ 커넥터: 고정 너비 설정 금지 (가이드 §10.3.1)
        main += (
            f'<div class="wf-sub-connector" style="display:flex; '
            f'flex-direction:column; align-items:center; '
            f'padding-top:{connector_top}px; flex-shrink:0; '
            f'overflow:visible;">'
            f'<div class="wf-sub-connector-label" style="font-size:12px; '
            f'color:var(--krds-gray-50); background:var(--krds-gray-0); '
            f'padding:3px 10px; border:1px solid var(--krds-gray-30); '
            f'border-radius:4px; white-space:nowrap; flex-shrink:0; '
            f'margin-bottom:8px;">{connector_label}</div>'
            f'<div class="wf-sub-connector-line" style="width:2px; flex:1; '
            f'min-height:40px; background:repeating-linear-gradient'
            f'(to bottom, var(--krds-gray-30) 0 6px, transparent 6px 12px);'
            f'"></div>'
            f'</div>'
            f'<div class="wf-sub-canvas" style="{sub_width} '
            f'background:var(--krds-gray-0); border-radius:8px; '
            f'box-shadow:0 2px 16px rgba(0,0,0,.08); position:relative; '
            f'overflow:visible; margin-top:{connector_top}px;">'
            + sub_canvas_html +
            f'</div>'
        )

    return main + '</div>'


# ─── 3) num-badge 마크업 ──────────────────────────────────────

def num_badge(n, *, edge: bool = False) -> str:
    """
    `<span class="num-badge">N</span>` HTML.
    edge=True 면 캔버스 직접 자식용 (.edge 변형).
    """
    cls = "num-badge edge" if edge else "num-badge"
    return f'<span class="{cls}">{n}</span>'


# ─── 4) 아이콘 자리 placeholder (가이드 §6.5.2) ────────────────

def icon_ph(size: int = 16) -> str:
    """연한 회색 채움 원. 실제 아이콘 자리만 표시."""
    return (
        f'<span style="display:inline-block; width:{size}px; '
        f'height:{size}px; border-radius:50%; '
        f'background:var(--krds-gray-10); '
        f'vertical-align:middle; flex-shrink:0;"></span>'
    )


# ─── 5) Spacer ────────────────────────────────────────────────

def spacer(h: int = 16) -> str:
    """수직 간격."""
    return f'<div style="height:{h}px;"></div>'


# ─── 6) Description 빌더 (계층 구조, HTML-to-Figma 호환) ──────

def desc_overview(text: str) -> str:
    """`<p>{text}</p>` — 화면 설명 단락."""
    return '<p>' + text + '</p>'


def dl(blocks: List[str]) -> str:
    """`<ol class="desc-list">` 으로 감싸기."""
    return '<ol class="desc-list">' + ''.join(blocks) + '</ol>'


def db(lvl1_text: str, *children: str) -> str:
    """
    desc-block: `<li><p class="desc-block">` 하나로 한 번호 항목 작성.
    lvl1_text: "1. App Bar" 같은 대제목.
    children: lv2/lv3/lv4/note 결과를 가변 인자로.
    """
    inner = f'<span class="lvl1">{lvl1_text}</span>'
    for c in children:
        inner += '<br>' + c
    return f'<li><p class="desc-block">{inner}</p></li>'


def lv2(text: str) -> str:
    """lvl2 bullet (들여쓰기 3 nbsp + •)."""
    return (
        '<span class="lvl2">&nbsp;&nbsp;&nbsp;• ' + text + '</span>'
    )


def lv3(text: str) -> str:
    """lvl3 소제목 (들여쓰기 6 nbsp + 숫자))."""
    return (
        '<span class="lvl3">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'
        + text + '</span>'
    )


def lv4(text: str) -> str:
    """lvl4 (들여쓰기 9 nbsp + -)."""
    return (
        '<span class="lvl4">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'
        '&nbsp;&nbsp;&nbsp;- ' + text + '</span>'
    )


def note(text: str) -> str:
    """note (들여쓰기 6 nbsp + *, 회색)."""
    return (
        '<span class="note">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;* '
        + text + '</span>'
    )


def reason(text: str) -> str:
    """reason (이유 표기, italic)."""
    return (
        '<span class="reason">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'
        '(이유: ' + text + ')</span>'
    )

"""
SB 컴포넌트 라이브러리 진입점.

== 사용법 ==
    from sb_components import pc, mobile, base

    # PC 화면
    canvas_pc = (
        pc.gnb(num=1, items=["메인", "공지", "FAQ"], active_idx=1)
        + pc.container(
            pc.page_title(num=2, title="공지사항")
            + pc.data_table(num=3, columns=[...], rows=[...])
            + pc.pagination(num=4, current=1, total=10)
        )
    )

    # 모바일 화면 (PC와 콘텐츠 동일 — 번호/문구/개수 일치)
    canvas_mobile = (
        mobile.app_bar(num=1, title="공지사항", back=True)
        + mobile.page_title(num=2, title="공지사항")
        + mobile.card_list(num=3, items=[...])
        + mobile.pagination(num=4, current=1, total=10)
    )

== PC ↔ Mobile 함수 매핑 ==
    pc.gnb           ↔ mobile.app_bar         (최상단 헤더)
    pc.lnb           ↔ mobile.bottom_nav      (주 네비)
    pc.container     ↔ (없음, 모바일은 자연 흐름)
    pc.page_title    ↔ mobile.page_title      (동일)
    pc.data_table    ↔ mobile.card_list       (목록 표현)
    pc.pagination    ↔ mobile.pagination      (동일)
    pc.primary_btn   ↔ mobile.primary_btn     (동일)
    pc.secondary_btn ↔ mobile.secondary_btn   (동일)
    pc.text_input    ↔ mobile.text_input      (동일)
    pc.select_field  ↔ mobile.select_field    (동일)
    pc.card          ↔ mobile.card            (동일)
    pc.filter_bar    ↔ mobile.filter_chips    (필터)
    pc.empty_state   ↔ mobile.empty_state     (동일)
    pc.dialog        ↔ mobile.dialog          (동일)
    pc.breadcrumb    ↔ mobile.breadcrumb      (동일, 모바일 드뭄)

    Mobile 전용: tab_bar, fab, bottom_sheet, search_bar,
                 checkbox_group, radio_group,
                 chat_area_open/close, bot_msg, user_msg,
                 quick_btns, input_bar

== DS 교체 시 (예: 자사 DS) ==
    1. `pc_etribe.py`, `mobile_etribe.py` 새로 작성 (KRDS 파일과 같은 함수 시그니처 유지)
    2. 아래 `from . import pc_krds as pc` 줄을 `from . import pc_etribe as pc`로 변경
    3. `from . import mobile_krds as mobile` 줄도 동일 패턴으로 교체
    4. sb-style-block.html의 CSS 변수 매핑 갱신
    5. 기존 화면 코드는 한 줄도 안 바꿔도 됨 (함수 시그니처가 DS-agnostic)
"""
from . import _base as base
from . import pc_krds as pc
from . import mobile_krds as mobile

__all__ = ["base", "pc", "mobile"]

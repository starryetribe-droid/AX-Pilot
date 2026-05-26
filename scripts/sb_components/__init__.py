"""
SB 컴포넌트 라이브러리 진입점.

== 사용법 ==
    from sb_components import pc        # PC 어댑터 (현재 KRDS)
    from sb_components.base import (
        wf_panel, canvas_wrap, num_badge, icon_ph, spacer,
        desc_overview, dl, db, lv2, lv3, lv4, note, reason
    )

    canvas = (
        pc.gnb(num=1, items=["메인", "공지", "FAQ"], active_idx=1)
        + pc.container(
            pc.page_title(num=2, title="공지사항")
            + pc.filter_bar(num=3, search_placeholder="검색", filters=[])
            + pc.data_table(num=4, columns=["번호", "제목"], rows=[...])
            + pc.pagination(num=5, current=1, total=10)
        )
    )

== DS 교체 시 (예: 자사 DS) ==
    1. `pc_etribe.py` 새로 작성 (pc_krds.py와 같은 함수 시그니처 유지)
    2. 아래 `from .pc_krds import * as pc` 줄을 `from .pc_etribe import * as pc`로 변경
    3. sb-style-block.html의 CSS 변수 매핑 갱신
    4. 기존 화면 코드는 한 줄도 안 바꿔도 됨 (함수 시그니처가 DS-agnostic)
"""
from . import _base as base
from . import pc_krds as pc

# 모바일 어댑터는 추후 추가 예정 (현재는 J-01 일회용 헬퍼만 존재).
# from . import mobile_krds as mobile

__all__ = ["base", "pc"]

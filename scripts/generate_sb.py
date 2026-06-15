#!/usr/bin/env python3
"""
SB(Storyboard) HTML 생성 헬퍼.

ETRIBE 양식의 SB HTML 파일을 일괄 생성합니다.
보일러플레이트(<head>, CSS, 메타 헤더, footer)는 자동 처리되며,
호출자(Claude)는 화면별 본문(wireframe + Description)만 JSON으로 넘기면 됩니다.

사용 예:
  python3 generate_sb.py \
    --variant mobile \
    --input screens.json \
    --output "01. 공통 기능/01_auth_account/SB/A-01"

screens.json 구조:
{
  "feature_id": "A-01",
  "feature_name": "회원가입",
  "author": "-",
  "ymd": "2026-05",
  "screens": [
    {
      "id": "A-01-001",
      "title": "회원가입 - 인증 방식 선택",
      "path": "비회원 > 회원가입",
      "body": "<div class='wf-panel'>...</div><div class='desc-panel'>...</div>"
    },
    ...
  ]
}

- body: <div class="page"> 내부에 들어갈 raw HTML (wf-panel + desc-panel)

★ 와이어프레임 골격 (필수 중첩 — 생략 시 캔버스가 왼쪽에 붙고 넘버링이 사라짐):
    <div class="wf-panel">              <!-- 가운데 정렬 + 여백 -->
      <div class="wf-canvas-wrap">      <!-- 배지+캔버스 가로 배치 -->
        <div class="num-strip"></div>   <!-- 28px: num-badge가 그려질 캔버스 바깥 공간 -->
        <div class="wf-canvas">...</div><!-- 실제 화면 -->
      </div>
    </div>
    <div class="desc-panel">...</div>
  이 스크립트는 .wf-canvas가 래퍼 없이 들어오면 자동으로 감싸거나(맨캔버스) 에러로 막는다.
"""

import argparse
import hashlib
import json
import os
import sys
from pathlib import Path

# Pretendard CDN (Static 1순위)
FONT_LINKS = '''<link rel="stylesheet" as="style" crossorigin
  href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard-dynamic-subset.min.css">
<link rel="stylesheet" as="style" crossorigin
  href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css">
<link rel="stylesheet" as="style" crossorigin
  href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-gov-dynamic-subset.min.css">'''

# 원본 ETRIBE 로고 PNG MD5 (검증용)
LOGO_MD5_EXPECTED = "51732c22289dc4b1eae17c2fd855ba4a"


def load_template(skill_dir: Path, name: str) -> str:
    """skill_dir/templates/ 에서 템플릿 파일 읽기."""
    path = skill_dir / "templates" / name
    if not path.exists():
        sys.exit(f"[ERROR] 템플릿 없음: {path}")
    return path.read_text(encoding="utf-8")


def verify_logo(skill_dir: Path) -> None:
    """로고 PNG MD5 검증 (손상 방지)."""
    logo_path = skill_dir / "reference" / "etribe-logo.png"
    if not logo_path.exists():
        print(f"[WARN] 로고 파일 없음: {logo_path}", file=sys.stderr)
        return
    md5 = hashlib.md5(logo_path.read_bytes()).hexdigest()
    if md5 != LOGO_MD5_EXPECTED:
        sys.exit(
            f"[ERROR] ETRIBE 로고 PNG가 손상됐습니다.\n"
            f"  Expected MD5: {LOGO_MD5_EXPECTED}\n"
            f"  Actual MD5:   {md5}"
        )


def ensure_canvas_wrap(body: str, screen_id: str) -> str:
    """와이어프레임 .wf-canvas가 필수 래퍼(.wf-panel > .wf-canvas-wrap > .num-strip)로
    감싸졌는지 검증한다.

    - 래퍼가 이미 있으면 그대로 통과 (idempotent).
    - .wf-canvas가 래퍼 없이 단독으로 들어온 흔한 실수는 자동으로 감싸고 알림 출력.
    - .wf-panel은 있는데 .wf-canvas-wrap/.num-strip이 빠진 애매한 경우는 에러로 막음.

    근거: .num-badge는 `left:-44px`(.edge는 -28px)로 캔버스 '바깥 왼쪽'에 그려지므로
    그 공간을 확보하는 .num-strip(28px)과 가운데 정렬·여백을 주는 .wf-panel이 반드시 필요.
    누락 시 캔버스가 grid 셀 왼쪽에 달라붙고 넘버링이 캔버스 뒤로 숨어 안 보인다.
    """
    # 와이어프레임 영역만 검사 (desc-panel 앞까지)
    marker = '<div class="desc-panel"'
    idx = body.find(marker)
    wire = body if idx == -1 else body[:idx]
    desc = "" if idx == -1 else body[idx:]

    has_canvas = 'class="wf-canvas"' in wire
    if not has_canvas:
        return body  # 와이어프레임 캔버스 없음 (특수 화면) — 손대지 않음

    has_wrap = 'class="wf-canvas-wrap"' in wire
    has_strip = 'class="num-strip"' in wire
    if has_wrap and has_strip:
        return body  # 이미 올바른 구조

    has_panel = 'class="wf-panel"' in wire
    if has_panel:
        # panel은 있는데 wrap/strip이 빠짐 — 자동 감싸면 panel 중첩 위험 → 명확히 막음
        sys.exit(
            f"[ERROR] {screen_id}: .wf-canvas가 .wf-panel 안에 있지만 "
            f".wf-canvas-wrap / .num-strip이 빠졌습니다.\n"
            f"  올바른 골격:\n"
            f'    <div class="wf-panel">\n'
            f'      <div class="wf-canvas-wrap">\n'
            f'        <div class="num-strip"></div>\n'
            f'        <div class="wf-canvas">...</div>\n'
            f"      </div>\n"
            f"    </div>\n"
            f"  (이 골격이 없으면 캔버스가 왼쪽에 붙고 넘버링이 사라집니다.)"
        )

    # 맨캔버스 — 흔한 실수. 자동으로 감싸고 알림.
    wrapped = (
        '<div class="wf-panel"><div class="wf-canvas-wrap">'
        '<div class="num-strip"></div>' + wire + '</div></div>'
    )
    print(
        f"  [AUTO-WRAP] {screen_id}: .wf-canvas를 .wf-panel > .wf-canvas-wrap > "
        f".num-strip 으로 자동 래핑했습니다 (넘버링·정렬 정상화).",
        file=sys.stderr,
    )
    return wrapped + desc


def render_html(*, screen_id: str, title: str, path_str: str, author: str, ymd: str,
                body: str, style_block: str, logo_data_url: str) -> str:
    """단일 SB HTML 렌더링."""
    # style block 안의 {LOGO_URL} placeholder 치환은 안 함 — 이미 base64가 들어있는 style block 사용
    return f'''<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{screen_id} {title}</title>
{FONT_LINKS}
{style_block}
</head>
<body>

<div class="sb-page">

<!-- ===== ETRIBE: Top Meta Header ===== -->
<table class="etribe-meta">
  <colgroup>
    <col style="width:200px"><col><col style="width:140px"><col style="width:160px">
    <col style="width:140px"><col style="width:280px"><col style="width:140px"><col style="width:200px">
  </colgroup>
  <tr>
    <th>화면/컴포넌트</th><td>{title}</td>
    <th>Local</th><td>KO</td>
    <th>화면ID</th><td>{screen_id}</td>
    <th>작성자</th><td>{author}</td>
  </tr>
  <tr>
    <th>화면경로</th><td>{path_str}</td>
    <th>Channel</th><td>Front</td>
    <th></th><td></td>
    <th>작성일</th><td>{ymd}</td>
  </tr>
</table>

<div class="page">
{body}
</div>

<!-- ETRIBE Footer -->
<div class="etribe-footer">
  <span class="ver">Ver.0.1 (1)</span>
</div>

</div><!-- /.sb-page -->

</body>
</html>
'''


def main():
    ap = argparse.ArgumentParser(description="ETRIBE SB HTML 일괄 생성")
    ap.add_argument("--variant", choices=["mobile", "pc"], default="mobile",
                    help="SB 양식 (현재 mobile만 지원, pc는 추후)")
    ap.add_argument("--input", required=True, help="screens.json 경로")
    ap.add_argument("--output", required=True, help="출력 디렉토리")
    ap.add_argument("--skill-dir", default=None,
                    help="스킬 루트 (기본: 이 스크립트 기준 자동 탐지)")
    args = ap.parse_args()

    # PC variant도 mobile과 동일 보일러플레이트(meta/footer/CSS) 사용.
    # 화면 body 내부의 .wf-canvas 사양만 PC variant에 맞게 작성되어 있어야 함
    # (호출자 Claude가 sb-pc 가이드 fetch 후 body 작성 시 처리).

    # skill_dir 자동 탐지: 스크립트의 부모의 부모
    if args.skill_dir:
        skill_dir = Path(args.skill_dir)
    else:
        skill_dir = Path(__file__).resolve().parent.parent

    # 검증
    verify_logo(skill_dir)
    style_block = load_template(skill_dir, "sb-style-block.html")
    logo_data_url = load_template(skill_dir, "sb-logo-data-url.txt").strip()

    # screens.json 로드
    input_path = Path(args.input)
    if not input_path.exists():
        sys.exit(f"[ERROR] input JSON 없음: {input_path}")
    data = json.loads(input_path.read_text(encoding="utf-8"))

    feature_id = data.get("feature_id", "")
    author = data.get("author", "-")
    ymd = data.get("ymd", "")
    screens = data.get("screens", [])

    if not screens:
        sys.exit("[ERROR] screens 배열이 비어 있음")

    # 출력 디렉토리
    out_dir = Path(args.output)
    out_dir.mkdir(parents=True, exist_ok=True)

    # 각 화면 생성
    print(f"Generating {len(screens)} SB files for {feature_id}...")
    for s in screens:
        sid = s["id"]
        body = ensure_canvas_wrap(s["body"], sid)
        html = render_html(
            screen_id=sid,
            title=s["title"],
            path_str=s.get("path", ""),
            author=author,
            ymd=ymd,
            body=body,
            style_block=style_block,
            logo_data_url=logo_data_url,
        )
        out_path = out_dir / f"{sid}.html"
        out_path.write_text(html, encoding="utf-8")
        print(f"  ✓ {out_path.name} ({len(html):,} bytes)")

    print(f"\nDone. {len(screens)} files in {out_dir}")


if __name__ == "__main__":
    main()

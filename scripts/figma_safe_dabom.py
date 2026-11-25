"""다봄 SB HTML → Figma 내보내기(HTML to Figma)용 보정

다봄 SB 템플릿(front-dabom)은 일부 요소를 CSS로만 그립니다. HTML→Figma 변환기는 이 방식을
옮기지 못해 아래 요소가 빠집니다.
  - 휴대폰 프레임 외곽선 : outline  → 실제 border 로 변경
  - 탭 점선 화살표        : ::before/::after + CSS 변수(--right/--down) + 그라데이션 → 인라인 SVG
  - 흐름 화살표(.dbm-arrow): 그라데이션 점선 배경 → 인라인 SVG
  - Checkbox·Radio·Toggle·하단 탭바 아이콘 : ::before/::after → 실제 <i> 요소
  - 시트 양식 : 메타 표·와이어프레임·Description 좌우 외곽선 정렬(음수 margin 제거), 푸터 로고 배경 → <img>
  - 시트 선   : 시트 외곽선 없음 / 표·본문 외곽선·Description·푸터 구분선 = 표 내부 선(gray-20, 1px)

브라우저에서 보이는 모습은 그대로이고, 구조만 바꿉니다. 여러 번 실행해도 결과가 같습니다.

사용:
  build_dabom_sb.py 가 빌드 직후 자동 실행 (끄려면 --no-figma-safe)
  기존 SB 재보정: python figma_safe_dabom.py <SB 폴더 또는 html 파일> [...]
  이전 버전(v2 등)으로 보정된 파일은 시트 양식 블록만 최신으로 교체

규칙: reference/dabom-front-guide.md §6
"""
import io, os, re, sys, glob

MARK = '<!-- figma-safe:dabom v3 -->'

# 시트(양식) 보정 — 메타 표·와이어프레임·Description 외곽선을 한 줄로 맞추고, 로고를 실제 이미지로
# 선 규칙(26.11.25): 시트 외곽선 없음 / 표·본문 외곽선·Description 구분선·푸터 구분선 = 표 내부 선과 동일(gray-20, 1px)
SHEET_CSS = '''
<style id="figma-safe-sheet">
/* 시트 외곽선 없음, 음수 margin 없이 좌우 여백을 각 블록에 줌 → 푸터 구분선이 시트 끝까지 */
.sb-page{border:0 !important;box-shadow:none !important;padding:28px 0 0 !important;}
.sb-page > .etribe-meta{margin:0 40px;min-width:calc(100% - 80px) !important;border:1px solid var(--krds-gray-20) !important;}
/* 표 아래 본문 영역: 표 내부 선과 같은 좌우 선으로 푸터 구분선까지 */
.sb-page > .page{margin:0 40px;border-left:1px solid var(--krds-gray-20);border-right:1px solid var(--krds-gray-20);}
.wf-panel{margin:0 !important;border:0 !important;}
.desc-panel{border-left:1px solid var(--krds-gray-20) !important;padding-right:28px !important;}
/* 푸터: 상단 전폭 구분선 + 우측 로고(실제 이미지) */
.etribe-footer{margin:0 !important;border-top:1px solid var(--krds-gray-20) !important;display:flex;justify-content:flex-end;align-items:center;background-image:none !important;padding:24px 68px !important;}
.etribe-footer > img.etribe-logo{display:block;width:201px;height:44px;}
</style>
'''

CSS = MARK + SHEET_CSS + '''
<style id="figma-safe-dabom">
/* 1) 휴대폰 프레임: outline → border (콘텐츠 폭 390 유지) */
.dabom-canvas{outline:0 !important;border:2px solid var(--d-frame);box-sizing:content-box;}
.dbm-case > .dabom-canvas{border:0;}
/* 2) 탭 점선·흐름 화살표: CSS 그림 끄고 인라인 SVG 사용 */
.dabom-board .dbm-tap::before,.dabom-board .dbm-tap::after{content:none !important;display:none !important;}
.dabom-board .dbm-arrow{background:none !important;display:inline-block;}
.dabom-board .dbm-arrow > svg,.dabom-board .dbm-tap > svg.fs-line{display:block;overflow:visible;}
.dabom-board .dbm-tap > svg.fs-line{position:absolute;}
/* 3) Checkbox · Radio · Toggle · 탭바 아이콘: 가상 요소 → 실제 요소 */
.dabom-canvas .dbm-radio::before,.dabom-canvas .dbm-check::before,.dabom-canvas .dbm-toggle::after,.dabom-canvas .dbm-appbar .tab::before{content:none !important;display:none !important;}
.dabom-canvas i.fsb,.dabom-canvas i.fsa{display:block;flex-shrink:0;font-style:normal;}
'''

def pseudo_rules(style_text):
    """템플릿의 가상 요소 규칙을 실제 요소용 규칙으로 복제"""
    out = []
    for sel, body in re.findall(r'([^{}]+)\{([^{}]*)\}', style_text):
        sel = sel.strip()
        if not any(k in sel for k in ('.dbm-radio', '.dbm-check', '.dbm-toggle', '.dbm-appbar .tab')):
            continue
        if '::before' not in sel and '::after' not in sel:
            continue
        nsel = sel.replace('::before', ' > i.fsb').replace('::after', ' > i.fsa')
        body = re.sub(r'content\s*:\s*""\s*;?', '', body)
        out.append('%s{%s}' % (nsel, body))
    return '\n'.join(out)

def svg_h(w):   # 오른쪽 점선 화살표 (높이 8)
    return ('<svg class="fs-line" width="{w}" height="8" viewBox="0 0 {w} 8" xmlns="http://www.w3.org/2000/svg">'
            '<line x1="0" y1="4" x2="{e}" y2="4" stroke="#000" stroke-width="1" stroke-dasharray="1 2"/>'
            '<path d="M{a} .5 L{e} 4 L{a} 7.5" fill="none" stroke="#000" stroke-width="1"/></svg>'
            ).format(w=w, e=w - 1, a=w - 5.5)

def svg_v(h):   # 아래 점선 화살표 (폭 8)
    return ('<svg class="fs-line" width="8" height="{h}" viewBox="0 0 8 {h}" xmlns="http://www.w3.org/2000/svg">'
            '<line x1="4" y1="0" x2="4" y2="{e}" stroke="#000" stroke-width="1" stroke-dasharray="1 2"/>'
            '<path d=".5 {a} L4 {e} L7.5 {a}" fill="none" stroke="#000" stroke-width="1"/></svg>'
            ).format(h=h, e=h - 1, a=h - 5.5).replace('d=".5', 'd="M.5')

def fix_tap(m):
    tag = m.group(0)
    if 'fs-line' in tag:
        return tag
    style = re.search(r'style="([^"]*)"', m.group(1))
    style = style.group(1) if style else ''
    parts = []
    r = re.search(r'--right\s*:\s*([\d.]+)px', style)
    d = re.search(r'--down\s*:\s*([\d.]+)px', style)
    if r:
        w = float(r.group(1)); w = int(w) if w.is_integer() else w
        parts.append(svg_h(w).replace('class="fs-line"', 'class="fs-line" style="left:46px;top:22px;"'))
    if d:
        h = float(d.group(1)); h = int(h) if h.is_integer() else h
        parts.append(svg_v(h).replace('class="fs-line"', 'class="fs-line" style="left:26px;top:58px;"'))
    return '<span%s>%s</span>' % (m.group(1), ''.join(parts))

def convert(html):
    if '<!-- figma-safe:dabom' in html:   # 이미 보정된 파일: 시트 양식 블록만 최신으로 교체
        if MARK in html:
            return html, False
        html = re.sub(r'<!-- figma-safe:dabom v\d+ -->', MARK, html, count=1)
        html = re.sub(r'\n?<style id="figma-safe-sheet">.*?</style>\n?', lambda m: SHEET_CSS, html, count=1, flags=re.S)
        return html, True
    style_text = '\n'.join(re.findall(r'<style[^>]*>(.*?)</style>', html, re.S))
    css = CSS + pseudo_rules(style_text) + '\n</style>\n'
    html = html.replace('</head>', css + '</head>', 1)
    # 탭 점선
    html = re.sub(r'<span((?=[^>]*class="[^"]*\bdbm-tap\b)[^>]*)>\s*</span>', fix_tap, html)
    # 흐름 화살표
    html = re.sub(r'<span((?=[^>]*class="[^"]*\bdbm-arrow\b)[^>]*)>\s*</span>',
                  lambda m: '<span%s>%s</span>' % (m.group(1), svg_h(40).replace('class="fs-line"', '')), html)
    # Checkbox · Radio · 탭바 : 첫 자식으로 <i class="fsb">
    html = re.sub(r'(<(span|div|label)\b(?=[^>]*class="[^"]*\b(?:dbm-check|dbm-radio)\b)[^>]*>)', r'\1<i class="fsb"></i>', html)
    # 하단 탭바 아이콘 : 각 .tab 의 첫 자식으로 <i class="fsb">
    def _appbar(m):
        return re.sub(r'(<span\b(?=[^>]*class="[^"]*\btab\b)[^>]*>)', r'\1<i class="fsb"></i>', m.group(0))
    html = re.sub(r'<div\b(?=[^>]*class="[^"]*\bdbm-appbar\b)[^>]*>.*?</div>', _appbar, html, flags=re.S)
    # Toggle : 마지막 자식으로 <i class="fsa">
    html = re.sub(r'(<(span|div)\b(?=[^>]*class="[^"]*\bdbm-toggle\b)[^>]*>)(.*?)(</\2>)', r'\1\3<i class="fsa"></i>\4', html)
    # 푸터 로고 : 배경 이미지 → 실제 <img>
    logo = re.search(r'\.etribe-footer\s*\{[^}]*?url\("(data:image/[^"]+)"\)', style_text, re.S)
    if logo and '<div class="etribe-footer"></div>' in html:
        html = html.replace('<div class="etribe-footer"></div>',
                            '<div class="etribe-footer"><img class="etribe-logo" alt="ETRIBE" src="%s"></div>' % logo.group(1), 1)
    return html, True

def main(paths):
    files = []
    for p in paths:
        files += sorted(glob.glob(os.path.join(p, '*.html'))) if os.path.isdir(p) else [p]
    for f in files:
        s = io.open(f, encoding='utf-8').read()
        if 'dabom-canvas' not in s:
            continue
        s2, changed = convert(s)
        if changed:
            io.open(f, 'w', encoding='utf-8', newline='\n').write(s2)
        print(('converted ' if changed else 'skip(already) ') + os.path.basename(f))

if __name__ == '__main__':
    main(sys.argv[1:])

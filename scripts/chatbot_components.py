# -*- coding: utf-8 -*-
"""챗봇 SB용 KRDS 아키타입 렌더러 1벌 — 컴포넌트 마크업의 단일 진실.

시트09 '렌더아키타입/역할(role)' 계약을 해석해 KRDS 마크업을 생성한다.
이 파일이 KRDS 규칙(표준 글리프·버튼 chrome 제거·말풍선·하단 입력바)의 유일한 출처이며,
AX Pilot 서버 가이드 §13 '챗봇 컴포넌트 카탈로그'의 구현체다.

규칙:
- 이모지 금지. 표준 글리프(← ✕ ↑)와 KRDS 토큰(var(--krds-*))만 사용.
- 아바타/아이콘 = 회색 원형 placeholder.
- 각 아키타입 렌더러는 roles(dict: role→bound value) + h(helpers)를 받아 봇 메시지 inner HTML 반환.
"""
import html, re

# ===== 파싱 헬퍼 =====
def _pipe(s):
    s = (s or '').strip()
    if s.startswith('[') and s.endswith(']'):
        s = s[1:-1]
    return [p.strip() for p in s.split('|') if p.strip()]

def parse_kv(s, sample):           # '[label=val | ...]' → [(label, 표시값)]
    out = []
    for part in _pipe(s):
        if '=' in part:
            l, v = part.split('=', 1); out.append((l.strip(), sample(v.strip())))
        else:
            out.append((part, ''))
    return out

def parse_buttons(s):              # '[라벨(action) | ...]' → [(label, action)]
    out = []
    for part in _pipe(s):
        m = re.match(r'^(.*?)\((.*?)\)\s*$', part)
        out.append((m.group(1).strip(), m.group(2).strip()) if m else (part, ''))
    return out

def parse_fieldmap(s):             # '{{api...[]}} → {title=a, subtitle=b}' → {role: field}
    m = re.search(r'\{([^{}]*)\}\s*$', s or '')
    fields = {}
    if m:
        for part in m.group(1).split(','):
            if '=' in part:
                k, v = part.split('=', 1); fields[k.strip()] = v.strip()
    return fields

class Helpers:
    """변환기가 주입: sample(바인딩→표시값), esc."""
    def __init__(self, sample):
        self.sample = sample
        self.esc = html.escape
        self.parse_kv = staticmethod(parse_kv)

# ===== 제네릭(공통가이드) 모드 — 역할→타입 플레이스홀더 =====
# 화면설계서를 브랜드/실데이터 없이 공통가이드로 재사용하기 위한 변환.
# 콘텐츠 역할(텍스트/금액 등)은 영문 타입명 플레이스홀더로 치환하고,
# 제어 역할(렌더 분기 결정)·구조 역할(필드맵)은 보존해 컴포넌트 형태를 유지한다.
# 플레이스홀더 = 이 자리에 들어갈 콘텐츠의 '필드/타입 이름'(실제 문구·값처럼 보이면 안 됨).
ROLE_PLACEHOLDER = {
    'primaryText': 'Body text', 'text': 'Body text', 'title': 'Title', 'subtitle': 'Subtitle',
    'message': 'Message', 'detail': 'Detail', 'loadingText': 'Loading text',
    'placeholder': 'Placeholder', 'buttonLabel': 'Button label', 'subText': 'Sub text',
    'amount': 'Amount', 'default': 'Value',
}
# 보존 역할: 렌더 분기(status/layout/mode/cancelable) + 필드 구조 판별(listItems/cardItems).
# listItems/cardItems의 렌더러(_list_item)는 이미 고정 플레이스홀더('상품명 N' 등)를
# 그리므로 원본을 보존해도 실데이터가 노출되지 않는다.
GENERIC_PRESERVE = {'status', 'cancelable', 'layout', 'mode', 'animation', 'listItems', 'cardItems'}
# 설정(config) 역할: 데이터 변수가 아니라 고정 설정값(불리언/enum). 디스크립션에 변수명({{}})이
# 아니라 실제 설정값(false·spinner·horizontal 등)을 그대로 표기한다.
GENERIC_CONFIG_ROLES = {'status', 'cancelable', 'layout', 'mode', 'animation'}
# 텍스트 역할 폴백 — PROMPT_PAIRED 선행 버블 등 제네릭 안내 문구.
GENERIC_PROMPT = 'Prompt'
# 변환기가 set: app_bar 등 공통 chrome의 브랜드명을 중립화할지 여부.
GENERIC_MODE = False

def _generic_buttons(s):
    """버튼 라벨만 'Button N'으로 치환, action은 보존(primary/취소 분기 유지)."""
    btns = parse_buttons(s)
    if not btns:
        return 'Button 1(action)'
    return ' | '.join((f'Button {i+1}({act})' if act else f'Button {i+1}')
                      for i, (_lbl, act) in enumerate(btns))

def _generic_kv(s, single=False):
    """kv 행 수를 보존하며 'Label N=Value'로 치환."""
    n = len(_pipe(s)) or (1 if single else 2)
    if single:
        return 'Label=Value'
    return ' | '.join(f'Label {i+1}=Value' for i in range(n))

def _generic_options(s):
    """옵션 칩 개수를 보존하며 'Option N'으로 치환."""
    n = len(_pipe(s)) or 3
    return ' | '.join(f'Option {i+1}' for i in range(n))

def genericize_roles(roles):
    """roles 딕셔너리를 공통가이드용 플레이스홀더로 변환(렌더러는 무수정)."""
    out = {}
    for r, v in (roles or {}).items():
        if r in GENERIC_PRESERVE:
            out[r] = v
        elif r == 'buttons':
            out[r] = _generic_buttons(v)
        elif r == 'kvRows':
            out[r] = _generic_kv(v)
        elif r == 'highlight':
            out[r] = _generic_kv(v, single=True)
        elif r == 'quickOptions':
            out[r] = _generic_options(v)
        else:
            out[r] = ROLE_PLACEHOLDER.get(r, r)   # 폴백: 역할 키 그대로
    return out

# ===== 공유 프리미티브 =====
def avatar():
    return ('<span style="width:30px;height:30px;border-radius:50%;background:var(--krds-gray-10);'
            'flex-shrink:0;display:inline-block;"></span>')

def num(n, edge=False):
    if not n: return ''
    return f'<span class="{"num-badge edge" if edge else "num-badge"}">{n}</span>'

def bot_row(inner, n=None):
    return (f'<div data-num style="position:relative;display:flex;gap:8px;align-items:flex-start;">'
            f'{num(n)}{avatar()}<div style="max-width:80%;">{inner}</div></div>')

def user_row(text, n=None, faded=False):
    op = 'opacity:.5;' if faded else ''
    return (f'<div data-num style="position:relative;display:flex;justify-content:flex-end;{op}">'
            f'{num(n)}<div style="max-width:80%;background:var(--krds-primary-50);color:var(--krds-gray-0);'
            f'padding:10px 14px;border-radius:14px 14px 2px 14px;font-size:14px;line-height:1.5;">{html.escape(text)}</div></div>')

def bubble(inner):
    return (f'<div style="background:var(--krds-gray-0);border:1px solid var(--krds-gray-10);'
            f'border-radius:2px 14px 14px 14px;padding:12px 14px;font-size:14px;line-height:1.55;'
            f'color:var(--krds-gray-90);">{inner}</div>')

def _card(inner, pad='14px 16px'):
    return (f'<div style="background:var(--krds-gray-0);border:1px solid var(--krds-gray-10);'
            f'border-radius:var(--krds-radius-lg);padding:{pad};min-width:240px;">{inner}</div>')

def _btn(label, primary=False):
    if primary:
        return (f'<button style="flex:1;min-height:42px;border:none;border-radius:var(--krds-radius-md);'
                f'background:var(--krds-primary-50);color:var(--krds-gray-0);font-size:14px;font-weight:600;'
                f'cursor:pointer;padding:0 12px;">{html.escape(label)}</button>')
    return (f'<button style="flex:1;min-height:42px;border:1px solid var(--krds-primary-50);'
            f'border-radius:var(--krds-radius-md);background:var(--krds-gray-0);color:var(--krds-primary-50);'
            f'font-size:14px;font-weight:600;cursor:pointer;padding:0 12px;">{html.escape(label)}</button>')

def app_bar(title=None):
    if title is None:
        title = 'AI 챗봇' if GENERIC_MODE else '디자인밀 AI'   # 제네릭 모드는 브랜드명 중립화
    return ('<div class="krds-app-bar">'
            '<button class="krds-app-bar-back" style="font-size:20px;">←</button>'
            f'<div class="krds-app-bar-title">{html.escape(title)}</div>'
            '<button class="krds-app-bar-action" style="font-size:18px;color:var(--krds-gray-90);">✕</button></div>')

def input_bar():
    return ('<div class="wf-bottom-fixed" style="padding:10px 12px;border-top:1px solid var(--krds-gray-10);'
            'background:var(--krds-gray-0);display:flex;align-items:center;gap:8px;">'
            '<input placeholder="메시지를 입력하세요" style="flex:1 1 0;min-width:0;box-sizing:border-box;height:40px;'
            'border:1px solid var(--krds-gray-20);border-radius:20px;padding:0 14px;font-size:14px;color:var(--krds-gray-90);">'
            '<button style="width:40px;height:40px;flex-shrink:0;border:none;border-radius:50%;'
            'background:var(--krds-primary-50);color:var(--krds-gray-0);font-size:18px;cursor:pointer;">↑</button></div>')

def chat_canvas(messages):
    return (f'<div class="wf-canvas">{app_bar()}'
            f'<div class="wf-canvas-content" style="padding:16px;background:var(--krds-gray-5);'
            f'display:flex;flex-direction:column;gap:14px;">{messages}</div>{input_bar()}</div>')

def wf_panel(messages):
    return (f'<div class="wf-panel"><div class="wf-canvas-wrap"><div class="num-strip"></div>'
            f'{chat_canvas(messages)}</div></div>')

# ===== 아키타입 렌더러 (roles, h) → inner HTML =====
def a_text(roles, h):
    return bubble(h.esc(h.sample(roles.get('primaryText', ''))))

def a_loading(roles, h):
    text = h.sample(roles.get('loadingText', '처리 중입니다'))
    dots = ('<span style="display:inline-flex;gap:4px;margin-right:8px;vertical-align:middle;">'
            + ''.join('<span style="width:6px;height:6px;border-radius:50%;background:var(--krds-gray-30);display:inline-block;"></span>' for _ in range(3))
            + '</span>')
    body = f'{dots}{h.esc(text)}'
    if str(roles.get('cancelable', '')).lower() == 'true':
        body += ('<div style="margin-top:10px;"><button style="min-height:36px;padding:0 14px;'
                 'border:1px solid var(--krds-gray-20);border-radius:var(--krds-radius-md);background:var(--krds-gray-0);'
                 'color:var(--krds-gray-70);font-size:13px;cursor:pointer;">취소</button></div>')
    return bubble(body)

def a_kv_card(roles, h):
    title = h.sample(roles.get('title', ''))
    rows = parse_kv(roles.get('kvRows', ''), h.sample)
    lis = ''
    for i, (lbl, val) in enumerate(rows):
        bd = '' if i == len(rows)-1 else 'border-bottom:1px solid var(--krds-gray-5);'
        lis += (f'<div style="display:flex;justify-content:space-between;align-items:center;padding:10px 0;{bd}">'
                f'<span style="color:var(--krds-gray-50);font-size:13px;">{h.esc(lbl)}</span>'
                f'<span style="color:var(--krds-gray-90);font-size:15px;font-weight:700;">{h.esc(val)}</span></div>')
    head = ''
    if title:
        head = (f'<div style="font-size:15px;font-weight:700;color:var(--krds-gray-90);margin-bottom:4px;'
                f'padding-bottom:8px;border-bottom:1px solid var(--krds-gray-10);">{h.esc(title)}</div>')
    hi = ''
    if roles.get('highlight'):
        hk = parse_kv(roles.get('highlight', ''), h.sample)
        if hk:
            l, v = hk[0]
            hi = (f'<div style="margin-top:10px;padding:12px 14px;border-radius:var(--krds-radius-md);'
                  f'background:var(--krds-primary-5);display:flex;justify-content:space-between;align-items:center;">'
                  f'<span style="color:var(--krds-gray-70);font-size:14px;font-weight:600;">{h.esc(l)}</span>'
                  f'<span style="color:var(--krds-primary-60);font-size:17px;font-weight:800;">{h.esc(v)}</span></div>')
    return _card(head + lis + hi)

def _list_item(idx, fields, horizontal=False):
    title = '상품명' if 'name' in fields else '항목명'
    sub = '보조 정보'
    title_txt = f'{title} {idx}'
    img = ('<span style="width:48px;height:48px;border-radius:var(--krds-radius-md);background:var(--krds-gray-10);'
           'flex-shrink:0;display:inline-block;"></span>') if ('image' in fields or 'thumbnail' in fields) else ''
    val = ('<span style="color:var(--krds-primary-60);font-size:14px;font-weight:700;">선택</span>'
           if 'value' in fields else '')
    if horizontal:
        return (f'<div style="flex:0 0 150px;border:1px solid var(--krds-gray-10);border-radius:var(--krds-radius-lg);'
                f'padding:12px;background:var(--krds-gray-0);">'
                f'<span style="display:block;width:100%;height:90px;border-radius:var(--krds-radius-md);'
                f'background:var(--krds-gray-10);margin-bottom:8px;"></span>'
                f'<div style="font-size:14px;font-weight:700;color:var(--krds-gray-90);">{title_txt}</div>'
                f'<div style="font-size:13px;color:var(--krds-primary-60);font-weight:700;margin-top:2px;">가격</div>'
                f'<button style="margin-top:8px;width:100%;min-height:34px;border:1px solid var(--krds-primary-50);'
                f'border-radius:var(--krds-radius-md);background:var(--krds-gray-0);color:var(--krds-primary-50);'
                f'font-size:13px;font-weight:600;cursor:pointer;">상세보기</button></div>')
    return (f'<div style="display:flex;gap:12px;align-items:center;padding:12px;border:1px solid var(--krds-gray-10);'
            f'border-radius:var(--krds-radius-lg);background:var(--krds-gray-0);">{img}'
            f'<div style="flex:1;min-width:0;"><div style="font-size:14px;font-weight:700;color:var(--krds-gray-90);">{title_txt}</div>'
            f'<div style="font-size:13px;color:var(--krds-gray-50);margin-top:2px;">{sub}</div></div>{val}</div>')

def a_card_list(roles, h):
    raw = roles.get('listItems') or roles.get('cardItems') or ''
    horizontal = str(roles.get('layout', '')).lower() == 'horizontal' or 'cardItems' in roles
    fields = parse_fieldmap(raw)
    items = ''.join(_list_item(i+1, fields, horizontal) for i in range(2))
    if horizontal:
        return (f'<div style="display:flex;gap:10px;overflow-x:auto;padding-bottom:4px;">{items}</div>')
    return (f'<div style="display:flex;flex-direction:column;gap:8px;min-width:260px;">{items}</div>')

def a_buttons(roles, h):
    btns = parse_buttons(roles.get('buttons', ''))
    direction = 'column' if str(roles.get('layout', '')).lower() == 'vertical' else 'row'
    if not btns:
        return ''
    out = ''
    for i, (lbl, action) in enumerate(btns):
        primary = action in ('confirm', 'retry') or (i == 0 and len(btns) <= 2 and action not in ('cancel',))
        out += _btn(lbl, primary=primary)
    return (f'<div style="display:flex;flex-direction:{direction};gap:8px;min-width:240px;">{out}</div>')

def a_banner(roles, h):
    status = str(h.sample(roles.get('status', ''))).lower()
    is_fail = 'fail' in status
    has_status = bool(status)
    msg = h.sample(roles.get('message', ''))
    detail = h.sample(roles.get('detail', '')) if roles.get('detail') else ''
    if has_status:  # 결과 배너 (U-11)
        color = 'var(--krds-danger-50)' if is_fail else 'var(--krds-success-50)'
        bg = 'var(--krds-danger-5)' if is_fail else 'var(--krds-success-5)'
        dot = f'<span style="width:20px;height:20px;border-radius:50%;background:{color};flex-shrink:0;display:inline-block;"></span>'
        inner = (f'<div style="display:flex;gap:10px;align-items:center;">{dot}'
                 f'<div><div style="font-size:15px;font-weight:700;color:var(--krds-gray-90);">{h.esc(msg)}</div>'
                 + (f'<div style="font-size:13px;color:var(--krds-gray-50);margin-top:2px;">{h.esc(detail)}</div>' if detail else '')
                 + '</div></div>')
        body = (f'<div style="background:{bg};border:1px solid {color};border-radius:var(--krds-radius-lg);'
                f'padding:14px 16px;min-width:240px;">{inner}</div>')
    else:           # 에러 배너 (U-16)
        body = (f'<div style="background:var(--krds-danger-5);border:1px solid var(--krds-danger-50);'
                f'border-radius:var(--krds-radius-lg);padding:14px 16px;min-width:240px;font-size:14px;'
                f'color:var(--krds-gray-90);line-height:1.5;">{h.esc(msg)}</div>')
    if roles.get('buttons'):
        # 배너 박스와 액션 버튼을 세로 스택 + 간격(달라붙음 방지)
        return (f'<div style="display:flex;flex-direction:column;gap:10px;min-width:240px;">'
                f'{body}{a_buttons({"buttons": roles["buttons"]}, h)}</div>')
    return body

def a_input_date(roles, h):
    chips = _pipe(roles.get('quickOptions', '')) or ['오늘', '내일', '모레']
    chip_html = ''.join(
        f'<button style="min-height:34px;padding:0 14px;border:1px solid var(--krds-gray-20);'
        f'border-radius:18px;background:var(--krds-gray-0);color:var(--krds-gray-70);font-size:13px;'
        f'cursor:pointer;">{html.escape(c)}</button>' for c in chips)
    cal = ('<div style="margin-top:10px;height:56px;border:1px dashed var(--krds-gray-20);'
           'border-radius:var(--krds-radius-md);display:flex;align-items:center;justify-content:center;'
           'color:var(--krds-gray-40);font-size:13px;">달력 선택</div>') if str(roles.get('mode','')).lower()=='calendar' else ''
    return _card(f'<div style="display:flex;gap:8px;flex-wrap:wrap;">{chip_html}</div>{cal}')

def a_input_stepper(roles, h):
    default = h.sample(roles.get('default', '1'))
    val = '1' if ('{{' in str(default) or not str(default).strip()) else h.esc(str(default))
    btn = ('border:1px solid var(--krds-gray-20);border-radius:var(--krds-radius-md);background:var(--krds-gray-0);'
           'width:40px;height:40px;font-size:20px;color:var(--krds-gray-70);cursor:pointer;')
    return _card(
        f'<div style="display:flex;align-items:center;justify-content:center;gap:14px;">'
        f'<button style="{btn}">−</button>'
        f'<span style="min-width:48px;text-align:center;font-size:18px;font-weight:700;color:var(--krds-gray-90);">{val}</span>'
        f'<button style="{btn}">+</button></div>', pad='16px')

def a_input_text(roles, h):
    ph = roles.get('placeholder') or '내용을 입력하세요'
    return _card(
        f'<input placeholder="{html.escape(ph)}" style="width:100%;box-sizing:border-box;height:44px;'
        f'border:1px solid var(--krds-gray-20);border-radius:var(--krds-radius-md);padding:0 12px;'
        f'font-size:14px;color:var(--krds-gray-90);">', pad='12px')

def a_payment(roles, h):
    amt = h.sample(roles.get('amount', ''))
    amt_txt = amt if amt and '{{' not in amt else '00,000원'
    return _card(
        f'<div style="display:flex;justify-content:space-between;align-items:center;padding-bottom:10px;'
        f'border-bottom:1px solid var(--krds-gray-10);">'
        f'<span style="color:var(--krds-gray-50);font-size:13px;">결제 금액</span>'
        f'<span style="color:var(--krds-gray-90);font-size:18px;font-weight:800;">{html.escape(amt_txt)}</span></div>'
        f'<div style="display:flex;gap:8px;margin-top:12px;">'
        f'<button style="flex:1;min-height:42px;border:1px solid var(--krds-gray-20);border-radius:var(--krds-radius-md);'
        f'background:var(--krds-gray-0);color:var(--krds-gray-70);font-size:14px;cursor:pointer;">디자인밀페이</button>'
        f'<button style="flex:1;min-height:42px;border:1px solid var(--krds-gray-20);border-radius:var(--krds-radius-md);'
        f'background:var(--krds-gray-0);color:var(--krds-gray-70);font-size:14px;cursor:pointer;">카드결제</button></div>')

def a_link(roles, h):
    text = h.sample(roles.get('text', '')) if roles.get('text') else ''
    label = roles.get('buttonLabel', '이동하기')
    t = (f'<div style="font-size:14px;color:var(--krds-gray-90);margin-bottom:10px;line-height:1.5;">{h.esc(text)}</div>') if text else ''
    return _card(
        f'{t}<button style="width:100%;min-height:44px;border:1px solid var(--krds-primary-50);'
        f'border-radius:var(--krds-radius-md);background:var(--krds-gray-0);color:var(--krds-primary-50);'
        f'font-size:14px;font-weight:700;cursor:pointer;">{html.escape(label)} →</button>')

def a_transfer(roles, h):
    text = h.sample(roles.get('text', '')) if roles.get('text') else '상담사가 도와드릴게요'
    label = roles.get('buttonLabel', '상담사 연결')
    sub = roles.get('subText', '')
    sub_html = (f'<div style="font-size:12px;color:var(--krds-gray-40);margin-top:8px;">{html.escape(sub)}</div>') if sub else ''
    return _card(
        f'<div style="font-size:14px;color:var(--krds-gray-90);line-height:1.5;">{h.esc(text)}</div>'
        f'<button style="margin-top:12px;width:100%;min-height:44px;border:none;border-radius:var(--krds-radius-md);'
        f'background:var(--krds-primary-50);color:var(--krds-gray-0);font-size:14px;font-weight:700;cursor:pointer;">{html.escape(label)}</button>'
        f'{sub_html}')

ARCHETYPES = {
    'text': a_text, 'loading': a_loading, 'kv-card': a_kv_card, 'card-list': a_card_list,
    'buttons': a_buttons, 'banner': a_banner, 'input-date': a_input_date,
    'input-stepper': a_input_stepper, 'input-text': a_input_text, 'payment': a_payment,
    'link': a_link, 'transfer': a_transfer,
}

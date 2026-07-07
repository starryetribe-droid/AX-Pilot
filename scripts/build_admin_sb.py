#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""어드민 SB 빌더 — 템플릿 스타일 + 화면 본문 → PC SB 일체 생성.

흐름:
  ① 템플릿 스타일(templates/admin-<template>.html) + 화면 본문(samples/admin/<id>.src.html) 결합
  ② generate_sb.py --variant pc 로 ETRIBE SB HTML 렌더

사용:
  python3 build_admin_sb.py 주문상세                # 레지스트리 키
  python3 build_admin_sb.py --src path.src.html --id ADM-X-001 --title "..." --path "..."

규칙:
  - 어드민은 PC 고정(variant=pc). 모바일/PC 질문 없음.
  - 템플릿 = 컴포넌트 룩의 단일 출처(templates/admin-<template>.html). 기본 'pulmuone'.
  - 새 화면은 templates/admin-<template>.html 클래스로 본문을 작성해
    samples/admin/<id>.src.html 로 저장 후 SCREENS에 등록하면 키로 호출 가능.
  - 환경변수: ADMIN_OUT(출력 루트, 기본 ~/Downloads/SB_어드민) · ADMIN_AUTHOR(작성자, 기본 'AX Pilot').
"""
import argparse, json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.dirname(HERE)
BUILD_DIR = os.path.join(HERE, '_build')

# 설계 완료 어드민 화면 레지스트리 (키 → 메타 + 본문 소스)
SCREENS = {
    '주문상세': dict(id='ADM-ORDER-001', title='주문관리 > 주문상세',
                  path='Admin > 주문관리 > 주문상세',
                  src='samples/admin/ADM-ORDER-001.src.html'),
    '챗봇대화내역': dict(id='ADM-CHAT-001', title='챗봇 관리 > 챗봇 대화 내역',
                   path='Admin > 챗봇 관리 > 챗봇 대화 내역',
                   src='samples/admin/ADM-CHAT-001.src.html'),
}


def template_path(name):
    p = os.path.join(SKILL, 'templates', f'admin-{name}.html')
    if not os.path.exists(p):
        sys.exit(f"[ERROR] 템플릿 없음: {p}")
    return p


def build(*, sid, title, path_str, src, template, author, out_root):
    style = open(template_path(template), encoding='utf-8').read().strip()
    src_abs = src if os.path.isabs(src) else os.path.join(SKILL, src)
    if not os.path.exists(src_abs):
        sys.exit(f"[ERROR] 화면 본문 없음: {src_abs}")
    body = open(src_abs, encoding='utf-8').read().strip()
    full = style + '\n' + body

    os.makedirs(BUILD_DIR, exist_ok=True)
    jp = os.path.join(BUILD_DIR, f'{sid}_screens.json')
    data = dict(feature_id=sid, feature_name=title, author=author, ymd='2026-06',
                screens=[dict(id=sid, title=title, path=path_str, body=full)])
    json.dump(data, open(jp, 'w', encoding='utf-8'), ensure_ascii=False)

    subprocess.run([sys.executable, os.path.join(HERE, 'generate_sb.py'),
                    '--variant', 'pc', '--input', jp, '--output', out_root], check=True)
    print(f"\n완료: {os.path.join(out_root, sid + '.html')}")
    print(f"  템플릿: admin-{template}  ·  본문: {src}")


def main():
    ap = argparse.ArgumentParser(description="어드민 SB 빌더 (PC 고정)")
    ap.add_argument('screen', nargs='?', help="레지스트리 키 (예: 주문상세)")
    ap.add_argument('--src', help="화면 본문 HTML 경로 (레지스트리 미사용 시)")
    ap.add_argument('--id', help="화면 ID")
    ap.add_argument('--title', help="화면 제목")
    ap.add_argument('--path', default='', help="화면 경로")
    ap.add_argument('--template', default='pulmuone', help="템플릿명 (기본 pulmuone)")
    ap.add_argument('--author', default=os.environ.get('ADMIN_AUTHOR', 'AX Pilot'))
    ap.add_argument('--out', default=os.path.expanduser(os.environ.get('ADMIN_OUT', '~/Downloads/SB_어드민')))
    a = ap.parse_args()

    if a.screen:
        if a.screen not in SCREENS:
            sys.exit(f"[ERROR] 등록되지 않은 화면: {a.screen}\n  등록된 화면: {', '.join(SCREENS)}")
        m = SCREENS[a.screen]
        build(sid=m['id'], title=m['title'], path_str=m['path'], src=m['src'],
              template=a.template, author=a.author, out_root=a.out)
    elif a.src and a.id and a.title:
        build(sid=a.id, title=a.title, path_str=a.path, src=a.src,
              template=a.template, author=a.author, out_root=a.out)
    else:
        sys.exit("사용법: build_admin_sb.py <레지스트리키>  |  --src <본문> --id <ID> --title <제목> [--path ..]")


if __name__ == '__main__':
    main()

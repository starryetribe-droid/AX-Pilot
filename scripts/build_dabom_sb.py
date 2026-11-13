#!/usr/bin/env python3
"""다봄(고대 AI 심리 앱) 프론트 SB 빌더 — 모바일 전용.

  ① 화면 본문 src(.wf-panel + .desc-panel HTML) → screens.json (json.dump, 직접 JSON 작성 금지)
  ② generate_sb.py --variant mobile --template dabom 로 ETRIBE SB HTML 렌더

사용:
  python build_dabom_sb.py --src samples/dabom/DABOM-SAMPLE-001.src.html \
      --id FO-SB-MW-MS-00000001 --title "홈" --path "홈" --author "홍길동"
  # 여러 화면: --src 를 반복하지 말고 화면마다 한 번씩 실행 (출력 폴더 동일하면 한 폴더에 모임)

규칙·컴포넌트 카탈로그: reference/dabom-front-guide.md / 템플릿: templates/front-dabom.html
환경변수: DABOM_OUT(출력 루트, 기본 ~/Downloads/SB_다봄) · DABOM_AUTHOR(작성자 기본 'AX Pilot')
"""
import argparse, datetime, json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.dirname(HERE)
BUILD_DIR = os.path.join(HERE, '_build')


def main():
    ap = argparse.ArgumentParser(description='다봄 프론트 SB 생성 (모바일 고정)')
    ap.add_argument('--src', required=True, help='화면 본문 HTML (.wf-panel + .desc-panel)')
    ap.add_argument('--id', required=True, help='화면 ID (예: FO-SB-MW-MS-00000001)')
    ap.add_argument('--title', required=True, help='화면/컴포넌트명')
    ap.add_argument('--path', default='-', help='화면경로')
    ap.add_argument('--author', default=os.environ.get('DABOM_AUTHOR', 'AX Pilot'))
    ap.add_argument('--out', default=os.environ.get(
        'DABOM_OUT', os.path.join(os.path.expanduser('~'), 'Downloads', 'SB_다봄')))
    a = ap.parse_args()

    src = a.src if os.path.isabs(a.src) else os.path.join(SKILL, a.src)
    if not os.path.exists(src):
        sys.exit(f'[ERROR] 화면 본문 없음: {src}')
    body = open(src, encoding='utf-8').read().strip()
    if 'dabom-canvas' not in body:
        sys.exit('[ERROR] .wf-canvas에 dabom-canvas 클래스가 없습니다 '
                 '(<div class="wf-canvas dabom-canvas">) — 다봄 템플릿 스타일이 적용되지 않습니다.')

    os.makedirs(BUILD_DIR, exist_ok=True)
    jp = os.path.join(BUILD_DIR, f'{a.id}_screens.json')
    data = dict(feature_id=a.id, feature_name=a.title, author=a.author,
                ymd=os.environ.get('DABOM_YMD') or datetime.date.today().strftime('%Y-%m-%d'),
                channel='Front',
                screens=[dict(id=a.id, title=a.title, path=a.path, body=body)])
    json.dump(data, open(jp, 'w', encoding='utf-8'), ensure_ascii=False)

    os.makedirs(a.out, exist_ok=True)
    subprocess.run([sys.executable, os.path.join(HERE, 'generate_sb.py'),
                    '--variant', 'mobile', '--template', 'dabom',
                    '--input', jp, '--output', a.out], check=True)
    print(f"\n완료: {os.path.join(a.out, a.id + '.html')}  (템플릿: front-dabom)")


if __name__ == '__main__':
    main()

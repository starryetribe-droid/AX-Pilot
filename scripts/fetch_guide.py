#!/usr/bin/env python3
"""
Feature Spec 가이드를 ETRIBE 서버에서 fetch.

가이드 내용은 stdout으로만 출력되며 디스크에 저장하지 않음.
Claude는 이 출력을 읽어 메모리에서 사용한다.

Config: ~/.etribe/config.json
{
  "server_url": "https://your-server.vercel.app",
  "token": "your-team-token"
}

사용 예:
  python3 fetch_guide.py --mode prd --author "김기획"
  python3 fetch_guide.py --mode sb --author "김기획" --feature-id A-02 --action create
  python3 fetch_guide.py --mode all --author "김기획"

★ --author 는 사용 로그 적재용 (필수). 작성자명을 매 작업 시작 시 입력받아 전달.
"""
import argparse
import json
import os
import sys
import urllib.request
import urllib.error
from pathlib import Path

DEFAULT_CONFIG_PATH = Path.home() / ".etribe" / "config.json"


def load_config() -> dict:
    """~/.etribe/config.json 로드, 없으면 안내."""
    path = DEFAULT_CONFIG_PATH
    if not path.exists():
        sys.exit(
            f"[ERROR] 설정 파일이 없습니다: {path}\n\n"
            "다음 형식으로 만드세요:\n"
            '{\n'
            '  "server_url": "https://your-server.vercel.app",\n'
            '  "token": "your-team-token"\n'
            '}\n\n'
            "토큰은 팀 관리자에게 요청하세요."
        )
    try:
        cfg = json.loads(path.read_text())
    except json.JSONDecodeError as e:
        sys.exit(f"[ERROR] {path} JSON 파싱 실패: {e}")

    for key in ("server_url", "token"):
        if not cfg.get(key):
            sys.exit(f"[ERROR] {path} 에 {key} 값이 비었습니다.")
    return cfg


def fetch_guides(server_url: str, token: str, mode: str,
                 author: str = "", feature_id: str = "",
                 action: str = "", project_path: str = "") -> dict:
    """서버에 POST 요청해서 가이드 dict 받기. 사용 로그 메타 동시 전송.

    ★ author 등 한글이 포함될 수 있는 모든 메타는 JSON body로만 전송.
       HTTP 헤더는 ASCII(latin-1)만 허용되어 한글이면 UnicodeEncodeError 발생.
    """
    url = server_url.rstrip("/") + "/api"
    body = {
        "mode": mode,
        # 사용 로그용 메타 (서버에서 Notion DB 적재 시 사용, 미설정 시 silent)
        "author": author or "",
        "feature_id": feature_id or "",
        "action": action or "",
        "project_path": project_path or "",
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(body, ensure_ascii=False).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json; charset=utf-8",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body_text = e.read().decode("utf-8", errors="replace")
        sys.exit(f"[ERROR] HTTP {e.code} from server: {body_text}")
    except urllib.error.URLError as e:
        sys.exit(f"[ERROR] 서버 연결 실패: {e.reason}")


def main():
    ap = argparse.ArgumentParser(description="ETRIBE 가이드 fetch")
    ap.add_argument("--mode", required=True,
                    choices=["prd", "sb", "sb-mobile", "sb-pc", "all",
                             "feature-list", "feature-asset"],
                    help="필요한 가이드 모드. sb=sb-mobile 별칭")
    ap.add_argument("--author", required=True,
                    help="작성자명 (사용 로그용, 매 작업 시작 시 입력)")
    ap.add_argument("--feature-id", default="",
                    help="기능 ID (예: A-02, J-01). 사용 로그용")
    ap.add_argument("--action", default="",
                    choices=["", "create", "edit", "view"],
                    help="작업 종류. 사용 로그용")
    ap.add_argument("--project-path", default="",
                    help="작업 폴더 상대 경로. 사용 로그용")
    ap.add_argument("--format", default="text",
                    choices=["text", "json"],
                    help="출력 포맷 (기본: text)")
    args = ap.parse_args()

    cfg = load_config()
    payload = fetch_guides(
        cfg["server_url"], cfg["token"], args.mode,
        author=args.author,
        feature_id=args.feature_id,
        action=args.action,
        project_path=args.project_path,
    )

    if args.format == "json":
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return

    # text format: 각 가이드를 구분자와 함께 stdout에 출력
    guides = payload.get("guides", {})
    for fname, content in guides.items():
        print(f"=" * 80)
        print(f"=== {fname}")
        print(f"=" * 80)
        if content is None:
            print("[NOT FOUND]")
        else:
            print(content)
        print()


if __name__ == "__main__":
    main()

# 🔄 스킬 업데이트 안내 — 풀무원 어드민 SB 프로세스 (2026-07)

기존에 스킬을 설치해둔 PC에서 **풀무원 어드민 SB 기능**을 쓰기 위한 업데이트 안내입니다.
(처음 설치하는 PC는 이 문서 대신 `ONBOARDING.md`를 따라주세요)

⏱️ 소요 시간: **약 2분**

---

## 이번 업데이트에 포함된 것

- **풀무원 어드민 SB 표준 프로세스** — 작성자명 → 기능정의 엑셀 첨부 → PRD 자동 생성(커버리지 기계 검증) → 컨펌 → SB 자동 생성
- 풀무원 디자인밀 어드민 템플릿 (좌측 GNB + 상단 유틸바 + 그린)
- n-m 서브 넘버링 규칙 (필터 조건 4-1~4-8, 테이블 컬럼 8-1~8-15 등 세부 요소 배지)
- 등록 화면: 주문상세(ADM-ORDER-001) · 챗봇 대화 내역(ADM-CHAT-001)

---

## ① 스킬 업데이트

터미널 또는 Claude Code 채팅창에서:

```bash
cd ~/.claude/skills/feature-spec && git pull
```

✅ `SKILL.md`, `templates/admin-pulmuone.html` 등이 업데이트됐다고 나오면 성공
(`Already up to date.`가 나오면 이미 최신)

> 스킬 파일 업데이트는 앱 **재시작 불필요** — 바로 반영됩니다.

---

## ② 엑셀 파싱 패키지 설치 (최초 1회)

기능정의 워크북(xlsx)을 읽기 위한 파이썬 라이브러리 **openpyxl**이 필요합니다.

```bash
# macOS
python3 -m pip install openpyxl

# Windows (Git Bash)
python -m pip install openpyxl
```

✅ `Successfully installed openpyxl-...` 또는 `Requirement already satisfied`(이미 설치됨)가 나오면 성공

> ❌ `python3: command not found` → 해당 PC에 파이썬이 없는 것. https://python.org 에서 설치 후 다시 실행

---

## ③ 동작 확인

Claude Desktop 앱 **Code 탭** 채팅창에 입력:

```
풀무원 SB 만들고 싶어
```

✅ *"작성자명을 입력해주세요"* 라고 물어보면 완료 🎉

---

## 사용 흐름 (참고)

```
"풀무원 SB 만들고 싶어"
    ↓
① 작성자명 입력
    ↓
② 기능정의 엑셀(세부기능정의 워크북 xlsx) 첨부
    ↓
③ PRD 자동 생성 (워크북 커버리지 기계 검증 포함) → 내용 확인 후 "컨펌"
    ↓
④ SB 자동 생성 (풀무원 디자인밀 템플릿 · PC)
    → 저장: ~/Downloads/SB_어드민/ + 작업 폴더의 "90. 어드민/SB/"
```

- 기능정의 엑셀 워크북은 서버에 없으므로 **본인 PC에 파일을 준비해서 첨부**해야 합니다
- 토큰(`~/.etribe/config.json`)은 기존 설치 때 설정한 그대로 사용 — 건드릴 필요 없음

---

## 문제 해결

| 증상 | 해결 |
| --- | --- |
| `ModuleNotFoundError: openpyxl` | ② 패키지 설치 다시 실행 |
| 스킬이 반응 없음 | Claude Desktop 앱 완전 종료 후 재실행 |
| `git pull` 충돌 | 관리자에게 문의 (로컬에서 스킬 파일을 직접 수정한 경우 발생) |

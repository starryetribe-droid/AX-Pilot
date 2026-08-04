# 🎉 ETRIBE 기획 자동화 도구 설치 안내

안녕하세요! 이 도구는 **공통 기능 PRD/SB를 Claude Desktop 앱으로 자동 생성**하는 사내 도구입니다.

한 번만 설정해두면, 이후엔 Claude Desktop 앱의 **Code 탭**에서 *"A-02 PRD 만들어줘"* 같이 말하면 자동으로 작성됩니다.

⏱️ 설치 소요 시간: **약 5분** (토큰·설정 파일 없이 바로 사용 가능)

---

## ✅ 사전 체크 (꼭 확인)

1. **Claude Pro 또는 Max 구독** 필요 — 무료 플랜은 Claude Code 기능 사용 불가
2. **macOS** 또는 **Windows** PC

---

## 🚀 설치 단계

### Step 1. Claude Desktop 앱 설치

1. https://claude.ai/download 접속
2. 본인 OS에 맞는 버전 다운로드 (macOS / Windows)
3. 설치 후 앱 실행 → **본인 Claude 계정으로 로그인** (Pro/Max 구독된 계정)

✅ 로그인 후 상단 메뉴에 **`Code`** 탭이 보이면 정상입니다.

❌ Code 탭이 안 보이면: 본인 계정의 구독 상태(Pro/Max)를 확인하세요. https://claude.ai/settings/billing

---

### Step 2. 스킬 폴더 설치


### macOS 사용자

클로드 코드에서 한 줄씩 복붙:

```bash
# 1) git 설치 확인 (대부분 이미 있음)
git --version
# 없다면: xcode-select --install

# 2) 스킬 받기
mkdir -p ~/.claude/skills
git clone <https://github.com/starryetribe-droid/AX-Pilot.git> ~/.claude/skills/feature-spec

# 3) 받아온 파일 확인
ls ~/.claude/skills/feature-spec
```

마지막 줄 결과에 `SKILL.md`, `scripts`, `templates` 가 보이면 ✅

```bash
# 4) 엑셀 워크북 기반 기능(풀무원 어드민 SB, 챗봇 SB)용 파이썬 패키지
python3 -m pip install openpyxl
```

### Windows 사용자

[Git for Windows](https://git-scm.com/download/win) 설치 후 **Git Bash** 실행:

```bash
mkdir -p ~/.claude/skills
git clone <https://github.com/starryetribe-droid/AX-Pilot.git> ~/.claude/skills/feature-spec
ls ~/.claude/skills/feature-spec
python -m pip install openpyxl
```

> **스킬 업데이트를 받고 싶을 때** (가이드가 갱신되면 관리자가 안내해드림):
> 
> 
> ```bash
> cd ~/.claude/skills/feature-spec && git pull
> ```
> 

---

### Step 3. Claude Desktop 앱 재시작

스킬 폴더(`~/.claude/skills/`)를 처음 생성했기 때문에 앱을 한 번 닫았다가 다시 켜야 인식됩니다.

1. Claude Desktop 앱 완전 종료
    - macOS: `Cmd+Q` 또는 상단 메뉴 → Quit
    - Windows: 작업 표시줄 우클릭 → 종료
2. 다시 실행

> 이후 스킬 파일을 수정하거나 업데이트(`git pull`)할 때는 **재시작 없이** 자동 반영됩니다.
> 

---

### Step 4. 동작 확인

Claude Desktop 앱에서:

1. 상단 **`Code`** 탭 클릭
2. 작업 폴더를 선택 (또는 새 폴더 생성)
3. 채팅창에 다음을 그대로 입력:
    
    ```
    /feature-spec
    ```
    
    또는 자연어로:
    
    ```
    A-01 PRD 만들어줘
    ```
    

✅ Claude가 *"작성자명을 입력해 주세요"* 라고 묻기 시작하면 **설치 성공!** 🎉

❌ 아무 반응이 없거나 스킬을 못 찾는다고 하면 → Step 3(재시작)를 다시 시도, 그래도 안 되면 관리자에게 문의.

---

## ✅ 사용하기

Claude Desktop 앱의 **Code 탭**에서 자연어로 요청하세요:

| 원하는 작업 | 이렇게 말하면 됨 |
| --- | --- |
| 회원가입 명세서(PRD) 생성 | `A-01 PRD 만들어줘` |
| 명세서 + 화면 설계서(SB) 모두 | `A-02 기획해줘` |
| 화면 설계서만 (PRD 이미 있을 때) | `A-01 PRD에서 SB 생성` |
| 부분 수정 | `A-01-003 화면 4번 항목 문구 수정` |
| **풀무원 어드민 SB** (기능정의 엑셀 기반) | `풀무원 SB 만들고 싶어` |

### 풀무원 어드민 SB 흐름 (참고)

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

### 동작 흐름 (참고)

```
"A-02 PRD 만들어줘"  (Code 탭 채팅창)
    ↓
Claude가 "작성자명을 입력해 주세요" 라고 물어봄
    ↓
본인 이름 입력 (예: 김기획, 박PM)  ★ 매 작업 시작 시 한 번
    ↓
Claude가 "프로세스 알려주세요 (A/B/C/D/E)" 라고 물어봄
    ↓
[A] 단계별 글  /  [B] 그림  /  [C] 비슷한 PRD 참고  /  [D] 일반 패턴(자동)  /  [E] 다른 PRD 차용
    ↓
Claude가 Mermaid 플로우차트 먼저 보여줌 → 확인 후 "OK" 답하기
    ↓
9섹션 PRD 자동 생성 → 작업 폴더에 .md 파일로 저장
```

> **작성자명**은 사용 로그에 기록되어 누가 어떤 작업을 했는지 추적합니다.
같은 이름으로 일관되게 입력해주세요 (예: 항상 "김기획").
> 

기능 ID 목록은 사내 가이드(서버에 있음)의 91개 중에서 선택하면 됩니다.

---

## 🛠️ 문제 해결

| 증상 | 원인 / 해결 |
| --- | --- |
| Code 탭이 안 보임 | Pro/Max 구독 확인 (https://claude.ai/settings/billing). 또는 앱 최신 버전인지 확인 |
| Claude가 스킬을 못 찾음 | Step 3 (앱 재시작) 누락. 한 번만 재시작하면 이후 자동 인식 |
| `git clone` 시 비밀번호 물어봄 / 거부됨 | 인터넷 확인. 그래도 안 되면 관리자에게 문의 |
| `서버 연결 실패` | 인터넷 확인. 계속 안 되면 관리자에게 문의 |
| `HTTP 401 unauthorized` | 구버전 스킬. `cd ~/.claude/skills/feature-spec && git pull` 후 재시도 |
| `python3` 없음 (macOS) | macOS에 기본 설치되어 있음. 안 되면 `brew install python3` |
| Windows에서 `python3` 없음 | https://www.python.org/downloads/ 에서 설치 |

---

## 📞 도움이 필요하면

- 설치 막힘 / 에러 / 사용법 질문 → **관리자 연락**
- 가이드 자체에 대한 질문 → 관리자에게 의견 전달

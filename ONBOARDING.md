# 🎉 ETRIBE 기획 자동화 도구 설치 안내

안녕하세요! 이 도구는 **공통 기능 PRD/SB를 Claude Code로 자동 생성**하는 사내 도구입니다.

한 번만 설정해두면, 이후엔 Claude Code 안에서 *"A-02 PRD 만들어줘"* 같이 말하면 자동으로 작성됩니다.

⏱️ 설치 소요 시간: **약 10분**

---

## 📦 받은 것 확인

관리자가 카톡으로 두 가지를 보냈을 거예요:

1. **개인 토큰** — 길고 이상한 문자열 (예: `xYz...`)
   ⚠️ 비밀번호와 같음. 다른 사람에게 공유 X
2. **feature-spec.zip** 파일

없으면 관리자에게 다시 요청하세요.

---

## 🚀 설치 단계

### Step 1. Claude Code 설치 확인

터미널 앱(맥: 응용프로그램 > 유틸리티 > 터미널)을 열고:

```bash
claude --version
```

- ✅ 버전 번호가 나오면 → Step 2로
- ❌ `command not found` 뜨면 → 아래 명령어로 설치:

```bash
# 방법 A: Homebrew (Mac 권장)
brew install anthropic/claude-code/claude-code

# 방법 B: npm
npm install -g @anthropic-ai/claude-code
```

설치 후 `claude --version` 다시 시도.

---

### Step 2. 스킬 폴더 설치

받은 `feature-spec.zip` 이 `~/Downloads/` 에 있다고 가정.

터미널에서 다음 4줄을 한 줄씩 복붙:

```bash
mkdir -p ~/.claude/skills
cd ~/.claude/skills
unzip -o ~/Downloads/feature-spec.zip
ls feature-spec
```

마지막 줄 결과에 `SKILL.md`, `scripts`, `templates` 가 보이면 ✅

---

### Step 3. 토큰 저장 ★ (가장 중요)

받은 토큰을 미리 카피해두세요.

터미널에서:

```bash
mkdir -p ~/.etribe
nano ~/.etribe/config.json
```

까만 화면이 뜨면 다음 내용을 **그대로** 붙여넣고, **`여기에_받은_토큰_붙여넣기`** 부분만 본인 토큰으로 교체:

```json
{
  "server_url": "https://etribe-feature-spec-server.vercel.app",
  "token": "여기에_받은_토큰_붙여넣기"
}
```

> 큰따옴표(`"`)는 그대로 남겨두세요. 토큰만 교체.

저장: `Ctrl+O` → Enter → `Ctrl+X`

---

### Step 4. 동작 확인

```bash
python3 ~/.claude/skills/feature-spec/scripts/fetch_guide.py --mode feature-list | head -5
```

다음과 같이 한글이 나오면 **성공!** 🎉

```
================================================================================
=== 1-features-list.md
================================================================================
# 웹사이트 공통 기능 프로세스 정의서
```

---

## ✅ 사용하기

본인 작업 폴더에서 `claude` 명령으로 Claude Code 실행 후, 그냥 자연어로 요청:

| 원하는 작업 | 이렇게 말하면 됨 |
|-----------|--------------|
| 회원가입 명세서(PRD) 생성 | `A-01 PRD 만들어줘` |
| 명세서 + 화면 설계서(SB) 모두 | `A-02 기획해줘` |
| 화면 설계서만 (PRD 이미 있을 때) | `A-01 PRD에서 SB 생성` |
| 부분 수정 | `A-01-003 화면 4번 항목 문구 수정` |

### 동작 흐름 (참고)

```
"A-02 PRD 만들어줘"
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
9섹션 PRD 자동 생성 → 파일로 저장
```

> **작성자명**은 사용 로그에 기록되어 누가 어떤 작업을 했는지 추적합니다.
> 같은 이름으로 일관되게 입력해주세요 (예: 항상 "김기획").

기능 ID 목록은 사내 가이드(서버에 있음)의 91개 중에서 선택하면 됩니다.

---

## 🛠️ 문제 해결

| 증상 | 원인 / 해결 |
|------|----------|
| `[ERROR] 설정 파일이 없습니다` | Step 3 다시. `~/.etribe/config.json` 위치/이름 확인 |
| `HTTP 401 unauthorized` | 토큰 오타이거나 만료됨. 카피 다시 해서 config.json 수정. 안 되면 관리자에게 새 토큰 요청 |
| `서버 연결 실패` | 인터넷 확인. 또는 server_url 오타 (`https://` 빠짐 등) |
| Claude Code에서 스킬 안 보임 | `claude` 재실행 (스킬은 시작 시 로드됨). `/help` 입력해서 스킬 목록 확인 |
| `python3` 없음 | macOS 기본 설치되어 있음. 안 되면 `brew install python3` |

---

## 🔐 보안 주의

- 토큰은 **비밀번호와 동등**. 메모장이나 1Password 같은 비밀번호 관리자에 보관
- 카톡 메시지로 받은 토큰은 **카톡에서 삭제** (1Password 등 옮겨 저장한 후)
- 다른 팀원에게 본인 토큰 **공유 금지**
- 의심스러운 활동(예: 본인이 안 한 fetch가 발생) 또는 PC 분실 시 → 관리자에게 즉시 알림 (즉시 차단 가능)

---

## 📞 도움이 필요하면

- 설치 막힘 / 에러 / 사용법 질문 → **관리자 (카톡)**
- 가이드 자체에 대한 질문 → 관리자에게 의견 전달
- 토큰 분실/유출 의심 → **즉시** 관리자에게 알림

---
name: feature-spec
description: |
  ETRIBE 공통 기능의 PRD(명세서)/SB(와이어프레임)를 생성·수정.
  3가지 모드: (1) PRD, (2) SB, (3) 통합. 부분 수정도 지원.

  ★ PRD 모드는 다음 두 단계를 무조건 거침:
    (a) 사용자에게 프로세스 입력 요청 (A/B/C/D/E 중 선택)
    (b) Mermaid 플로우차트 프리뷰 → 사용자 승인 (D 옵션이어도 적용)
  PRD 본문/SB는 프리뷰 없이 작성·저장.

  트리거: "A-02 PRD 만들어줘", "회원가입 기획해줘", "PRD에서 SB",
        "A-01-003 화면 추가", "Description 수정" 등.

  가이드는 ETRIBE 사내 서버에서 fetch (로컬 저장 X).
  사전 설정: ~/.etribe/config.json (ONBOARDING.md 참고).
---

# Feature Spec 스킬

가이드 본문은 모두 서버에 있고 `fetch_guide.py`로 받아 메모리에서 사용한다.
이 파일은 흐름과 핵심 제약만 기술한다.

## 1. 모드 판별

| 입력 | 모드 |
|------|------|
| 기능 ID/이름만 | (3) 통합 |
| "PRD만"/"명세서만" | (1) PRD |
| `.md` PRD 경로 + "SB" | (2) SB |
| 챗봇/인텐트 워크북 기반 ("인텐트 9 챗봇 SB", "챗봇 SB 생성") | (2) SB — **챗봇 분기 §4.2** |
| 기존 파일 + "수정/추가" | 부분 수정 (Edit) |

## 2. 카테고리 매핑

`A-XX` → `01_auth_account`, `B-XX` → `02_mypage_personalization`,
`C-XX` → `03_content_board`, `ADM-XX` → 별도. 정확한 매핑은 fetch한 features-list 참조.

## ★ 공통: 작성자명 입력 (모든 모드 공통, fetch 전 무조건)

모든 모드(PRD/SB/통합/부분수정) 진입 직후, **첫 `fetch_guide.py` 호출 전에**
사용자에게 작성자명을 묻는다:

```
[Feature Spec 작성 시작]
작성자명을 입력해주세요 (예: 김기획, 박PM 등):
```

- 입력값(`{author}`)은 이번 작업 전체 동안 메모리 변수로 보관 (재입력 X)
- 모든 `fetch_guide.py` 호출 시 `--author "{author}"` 인자 필수
- `feature_id`, `action`(create/edit/view), `project_path`가 정해진 시점 이후의 호출은 메타도 함께 전달

호출 템플릿:
```bash
python3 .claude/skills/feature-spec/scripts/fetch_guide.py \
  --mode {prd|sb|sb-mobile|sb-pc|all|feature-list|feature-asset} \
  --author "{author}" \
  --feature-id "{기능ID}" \           # 알려진 경우
  --action "{create|edit|view}" \    # 알려진 경우
  --project-path "{상대경로}"          # 알려진 경우
```

`--author` 없이 호출 금지. 작성자명 미입력 상태로 진행 불가.

## 3. PRD 모드

```
Step 0   작성자명 입력 요청 (★ 공통: 모든 모드 공통)
Step 0.1 사용자에게 프로세스 입력 요청  ← 작성자명 받은 직후
Step 1   python3 .claude/skills/feature-spec/scripts/fetch_guide.py \
            --mode prd --author "{author}" \
            --feature-id "{기능ID}" --action create
Step 2   features-list에서 기능 정보 lookup (영문명, 카테고리)
Step 2.5★ Mermaid 플로우차트 작성 → 사용자 프리뷰 → 승인까지 반복
Step 3   9섹션 PRD 작성 (가이드 따름, Step 2.5의 Mermaid 그대로 사용)
Step 3.5★ 화면별 체크리스트 검증 → 누락 항목 일괄 질문 → 답변 반영
Step 4   Write로 저장: 01. 공통 기능/{카테고리}/PRD/{기능ID}_{영문명}.md
```

### Step 0: 프로세스 입력 요청 형식

```
[{기능ID} {기능명}]
features 설명: "{features-list 설명문}"

PRD 작성 전에 프로세스를 알려주세요:
  A) 단계별 글/bullet
  B) 손그림/플로우차트 이미지 첨부
  C) 비슷한 PRD 참고 (경로 또는 ID)
  D) 일반 패턴으로 (자동)
  E) 다른 PRD 패턴 차용

ETRIBE 고유 정책/분기 있으면 알려주세요.
```

응답 받기 전 Step 1 진행 금지. D 응답이어도 Step 2.5는 수행.

### Step 2.5: Mermaid 프리뷰 (무조건)

가이드의 6도형/색상 규칙으로 Mermaid 작성 후:

```
[{기능ID} 플로우 초안]
```mermaid
...
```
OK신가요? 수정사항 있으면 말씀해주세요.
```

승인 전 Step 3 금지. 수정 요청 시 Mermaid만 수정 후 재프리뷰 (반복).

### Step 3.5: 화면별 체크리스트 검증 (무조건)

PRD 본문(§6 화면별 UI 요소) 작성을 완료한 직후, 저장(Step 4) 전에 무조건 수행한다.

1. §6의 각 화면을 가이드 §6-1의 **17개 타입** 중 하나(또는 복수)로 분류
2. 분류된 타입의 필수 체크 항목 중 §5(예외 처리) 또는 §6(UI 요소)에 정의 안 된 항목 추출
3. 화면별로 묶어서 사용자에게 **한 번에** 질문 (한 항목씩 따로 묻지 않음)
4. 답변 받기 전 Step 4 금지
5. 답변을 §5/§6에 반영 후 저장

질문 출력 형식:

```
[{기능ID} PRD 체크리스트 검증]
아래 화면의 정의가 필요한 항목입니다. 한 번에 답변해주세요.

[{화면명1} — {분류된 타입}]
□ {누락 항목 1}
□ {누락 항목 2}

[{화면명2} — {분류된 타입}]
□ {누락 항목 3}

답변 방식:
- 항목별로 정의해주시거나
- "패턴 따라가자" (ETRIBE 공통 패턴 자동 적용)
- "스킵" (선택 항목으로 표시)
```

ETRIBE 공통 패턴(자동 적용 가능):
- 목록형 정렬: 고정 우선 → 작성일 DESC
- 목록형 페이지네이션: 10건/페이지
- 모달 닫기: X 버튼 + 배경 클릭 + ESC
- 상태/에러: G-01 매핑

비즈니스 결정 항목(필터 종류, 권한 정책, 임시저장 등)은 반드시 사용자에게 질문.

## 4. SB 모드

### 4.0 Variant 결정 (Step 0)

PRD 분석 전 사용자에게 **모바일 / PC 중 하나**를 확인:

```
[{기능ID} SB 생성]
어느 양식이 필요하세요?
  A) 모바일 (--variant mobile)
  B) PC (--variant pc)

기본값은 모바일입니다.
```

**★ 한 번에 하나의 variant만 생성한다.** 두 variant 모두 필요한 경우, 한쪽 완료 후 별도 SB 모드 요청으로 다른 쪽 생성. 한 번에 둘 다 만들면 오류율이 높아 분리한다.

```
Step 0   작성자명 입력 요청 (★ 공통)
Step 1   python3 .claude/skills/feature-spec/scripts/fetch_guide.py \
           --mode sb-mobile (or sb-pc) --author "{author}" \
           --feature-id "{기능ID}" --action {create|edit} \
           --project-path "01. 공통 기능/{카테고리}/SB/{기능ID}"
Step 2   PRD 분석 → 화면 분리 (가이드의 화면 분리 원칙 적용 — variant 무관)
Step 3   각 화면의 body HTML 작성 (wf-panel + desc-panel)
         - mobile: .wf-canvas 390×min-height:844
         - pc: .wf-canvas width:100%; max-width:2560px; height:auto
         - 컴포넌트 마크업은 fetch한 가이드 §6 카탈로그를 그대로 적용
         - Description 영역은 variant 무관하게 동일
Step 4   /tmp/{기능ID}_screens.json 작성
Step 5   python3 .claude/skills/feature-spec/scripts/generate_sb.py \
           --variant {mobile|pc} --input /tmp/{기능ID}_screens.json \
           --output "01. 공통 기능/{카테고리}/SB/{기능ID}{_PC?}"
         - mobile 출력: "01. 공통 기능/{cat}/SB/{기능ID}/"
         - pc 출력:     "01. 공통 기능/{cat}/SB/{기능ID}_PC/"
```

### 4.1 PC/모바일 차이 (절대 어기지 말 것)

**화면 정의 콘텐츠는 두 variant가 동일해야 한다.** 같은 컴포넌트 목록, 같은 동작 설명, 같은 예외 처리. 다른 것은 **양식(레이아웃)만**:

| 항목 | 모바일 | PC |
|------|--------|-----|
| `.wf-canvas` 폭 | 390px 고정 | 100% (max-width 2560px) |
| `.wf-canvas` 높이 | min-height 844px | **min-height 1440px** + height auto (상한 없음) |
| KRDS 컴포넌트 | app-bar, tab-bar, FAB 등 | GNB, 테이블, 숫자 페이지네이션, LNB 등 |
| 페이지 타이틀 | 22px | 28–32px |
| 입력/버튼 | 48px | 40–48px |

**금지**: PC 양식이라고 컴포넌트 목록을 누락하거나 화면을 분리/병합 추가로 하지 말 것. 화면 분리 원칙은 variant 무관.

### 4.2 챗봇 SB — 인텐트 워크북 기반 ★

소스가 PRD `.md`가 아니라 **AI 챗봇 인텐트 정의 워크북(xlsx)** 인 경우 이 분기를 탄다.
화면을 손으로 작성하지 않는다 — 워크북의 `09_컴포넌트스키마`(렌더 계약: 컴포넌트→아키타입, 슬롯→역할)
+ `10_모듈콘텐츠바인딩`(값)을 변환기가 자동으로 screens.json + KRDS 마크업으로 만든다.
컴포넌트별 마크업 하드코딩은 없고, **12종 아키타입 렌더러**(`scripts/chatbot_components.py`)가 단일 출처다.
작성 표준 = 가이드 **§13 «챗봇 컴포넌트 카탈로그»**.

```
Step 0   작성자명 입력 요청 (★ 공통)
Step 0.1 인텐트 번호 + 워크북 경로 확인
           - 인텐트 번호 (워크북 08 시트의 인텐트#, 예: 9)
           - 워크북 경로 → 환경변수 CHATBOT_XLSX (미설정 시 사용자에게 질문)
Step 1   python3 .claude/skills/feature-spec/scripts/fetch_guide.py \
           --mode sb-mobile --author "{author}" \
           --feature-id "IT{NNN}" --action create        # §13 카탈로그 포함
Step 2   CHATBOT_XLSX="{워크북경로}" \
         python3 .claude/skills/feature-spec/scripts/build_chatbot_sb.py {인텐트번호}
```

`build_chatbot_sb.py`가 한 번에 수행:
- ① `chatbot_to_sb.py` — 워크북(08 메타 + 09 계약 + 10 바인딩) → `_build/IT{NNN}_screens.json` (아키타입 디스패치)
- ② `generate_sb.py --variant mobile` — screens.json → 화면별 SB HTML
- ③ `build_index()` — 모듈(단계)별 라벨 iframe `index.html`

출력: `~/Downloads/SB_챗봇/IT{NNN}/` (환경변수 `CHATBOT_OUT`로 변경 가능)

규칙:
- **variant = mobile 고정** (챗봇은 모바일 대화 UI). §4.0의 PC 질문 생략.
- 일반 SB의 Step 2~4(PRD 분석·화면 분리·수기 screens.json)는 **건너뛴다**. 변환기가 워크북 단일 소스로 전 과정 수행.
- 화면 = 인텐트의 단계(모듈). 봇 답변 = (선택) 텍스트 말풍선 + 리치 컴포넌트 (§13.2).
- 새 시각 유형이 필요하면 `chatbot_components.py`에 아키타입 렌더러만 추가(§13.4) — 변환기·SKILL 수정 불필요.
- 환경변수: `CHATBOT_XLSX`(워크북, 필수) · `CHATBOT_OUT`(출력 루트) · `CHATBOT_AUTHOR`(작성자 기본 'AX Pilot').

### ★ 모달/다이얼로그 처리 규칙 (절대 어기지 말 것)

모달·다이얼로그·바텀시트 등 오버레이 UI는 **별도 HTML 파일로 분리하지 않는다**.
해당 화면의 메인 캔버스(`.wf-canvas`) **우측에 서브 캔버스(`.wf-sub-canvas`)로 붙인다**.

구조:
```
.wf-canvas-wrap
  ├─ .num-strip
  ├─ .wf-canvas (메인)
  ├─ .wf-sub-connector (점선 + 트리거 라벨)
  └─ .wf-sub-canvas (모달/다이얼로그)
```

- 트리거 요소(예: 삭제 버튼)의 Y 좌표에 맞춰 `padding-top` / `margin-top` 정렬
- `.wf-sub-connector-line` 점선 + `.wf-sub-connector-label`로 트리거 동작 표시
- 서브 캔버스의 번호(⑧ 등)는 메인 캔버스 번호 이어서 부여
- desc-panel에 DIALOG 섹션 별도 추가하여 서브 캔버스 요소 설명

**★ 딤(Dim) 배경**: 모달/로딩 백드롭은 `position:absolute; inset:0;`로 `.wf-canvas` 전체를 덮음. `height:600px` 같은 고정값 금지 (특히 PC에서 1440px 캔버스의 1/3만 덮이는 문제 발생).

참고: `99. Sample/SB/C-01-002.html` (삭제 확인 다이얼로그 우측 배치 예시)

### ★ Description 작성 규칙 (HTML-to-Figma 호환 — 절대 어기지 말 것)

각 번호 항목 = 단 하나의 `<p class="desc-block">`. 줄바꿈 `<br>`, 들여쓰기 `&nbsp;`, 스타일 차이 `<span class="lvl1|lvl2|lvl3|lvl4|note|reason">` inline.

```html
<li>
  <p class="desc-block"><span class="lvl1">1. ...</span><br><span class="lvl2">&nbsp;&nbsp;&nbsp;• ...</span><br><span class="lvl3">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1) ...</span><br><span class="lvl4">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- ...</span><br><span class="note">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;* ...</span></p>
</li>
```

**금지**: `<div>` 분리, CSS `::before`, padding/margin 들여쓰기.

### screens.json 형식

```json
{
  "feature_id": "A-02", "feature_name": "...", "author": "-", "ymd": "2026-05",
  "screens": [
    {"id":"A-02-001","title":"...","path":"...","body":"<div class=\"wf-panel\">...</div><div class=\"desc-panel\">...</div>"}
  ]
}
```

## 5. 통합 모드

§3 PRD 전체 수행 → 사용자에게 SB 진행 의사 확인 → §4 SB 수행.
PRD 작성 시 Step 0/2.5는 그대로 적용.

## 6. 부분 수정

기존 PRD/SB 파일은 Edit 툴로 직접 수정. 생성 스크립트(generate_sb.py) 불필요.
SB 수정 시 `desc-block` 구조 유지 (§4 ★ 참고).

## 7. 보안

가이드는 디스크 미저장. fetch 결과는 메모리에서만 사용.
`cat SKILL.md` 해도 가이드 본문 노출 X (절차서만).

## 트러블슈팅 / 사전설정 / 사용법 안내

→ `ONBOARDING.md` 참고.

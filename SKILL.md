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

  가이드는 ETRIBE 사내 서버에서 fetch (로컬 저장 X, 토큰·설정 파일 불필요).
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
| 챗봇 컴포넌트 가이드 ("챗봇 컴포넌트 가이드", "컴포넌트 카탈로그 만들어줘") | (4) 가이드 — **§4.3** |
| 어드민/관리자 화면 ("어드민 만들어줘", "관리자 화면 SB", "어드민 주문상세") | (2) SB — **어드민 분기 §4.4** |
| 어드민 세부기능정의 워크북(xlsx) ("어드민 정의서로 PRD", "세부기능정의 워크북") | (1) PRD — **어드민 워크북 분기 §5.1** |
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
         python3 .claude/skills/feature-spec/scripts/build_chatbot_sb.py {인텐트번호} [--generic]
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
- 환경변수: `CHATBOT_XLSX`(워크북, 필수) · `CHATBOT_OUT`(출력 루트) · `CHATBOT_AUTHOR`(작성자 기본 'AX Pilot') · `CHATBOT_GENERIC`(=1 시 제네릭 모드, `--generic`과 동일).

### ★ 제네릭(공통가이드) 모드 — `--generic`

화면설계서를 **브랜드·실데이터 없이 공통가이드로 재사용**할 때 사용. 기본은 실데이터 모드(미지정).
출력은 별도 폴더 `IT{NNN}_GENERIC/`(컴포넌트 가이드는 `*-generic.html`)에 생성 — 실데이터 SB와 분리.

변환 규칙(단일 출처 = `chatbot_components.genericize_roles`):
- **와이어프레임**: 콘텐츠 역할 → 영문 타입 플레이스홀더. `title→Title` · `primaryText/text→Body` ·
  `message→Message` · `amount→00,000원` · `kvRows→Label N=Value`(행 수 보존) ·
  `buttons→Button N`(action 보존) · `quickOptions→Option N`.
- **디스크립션**: 실값 대신 **변수명**. 동적 바인딩=`{{경로}}`, 정적=`{{슬롯명}}`.
  단 제어/설정 역할(`cancelable`·`layout`·`mode`·`status`·`animation`)은 데이터 변수가 아니므로
  실제 설정값(`false`·`spinner` 등) 그대로 표기.
- **보존**(중립화 안 함): 렌더 분기 역할 `status`·`layout`·`mode`·`cancelable`, 필드 구조 `listItems`·`cardItems`
  (렌더러가 이미 고정 플레이스홀더 출력), 앱바 브랜드명은 'AI 챗봇'으로 중립화.
- 인텐트명/화면 제목/진입 발화는 **유지**(플로우 식별자라 중립화하면 의미 상실).

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

### 4.3 챗봇 컴포넌트 가이드 — 단일 페이지 카탈로그 ★

워크북의 컴포넌트(07 메타 + 09 렌더 계약)와 사용처(08+10)를 **한 장의 HTML 가이드**로 묶는다.
화면(모듈)이 아니라 **컴포넌트(U-01~U-NN)가 단위**다. 두 가지 포맷을 생성한다(`--format`, 기본 both):
- **web**(`component-guide.html`): 분류별 좌측 네비 + 컴포넌트 카드 **[라이브 프리뷰 | 스펙 표]**.
- **sb**(`component-guide-sb.html`): **ETRIBE SB 양식**(메타 헤더 + 와이어프레임∣Description 2단 + 푸터).
  모든 컴포넌트를 **한 화면 보드**에 분류별로 취합하고, Description은 **UI 흐름**(진입→안내→조회→입력→결과→다음행동)으로 기술.

프리뷰는 `chatbot_components.ARCHETYPES` 렌더러를 **그대로 호출**하므로 실 SB와 100% 동일(드리프트 0).

```
Step 0   작성자명 입력 요청 (★ 공통)
Step 1   python3 .claude/skills/feature-spec/scripts/fetch_guide.py \
           --mode sb-mobile --author "{author}" --action view   # §13 카탈로그 포함(선택)
Step 2   CHATBOT_XLSX="{워크북경로}" \
         python3 .claude/skills/feature-spec/scripts/build_component_guide.py \
           [--intents 7,9,10,14] [--format web|sb|both] [--generic]   # 기본 both
```

`--generic`: 프리뷰를 실 바인딩값 대신 **역할 타입 플레이스홀더**로 렌더(공통가이드용, §4.2 제네릭 규칙과 동일).
출력 파일은 `*-generic.html`로 분리.

`build_component_guide.py` 동작:
- ① 07 → 컴포넌트 메타(코드·명·분류·정의·사용 답변유형)
- ② 09 → 슬롯→역할 계약 + 렌더 아키타입
- ③ 08+10 → 컴포넌트별 사용처 역인덱스(어느 인텐트/모듈이 쓰는지) + 대표 바인딩값
- ④ 분류별 그룹 → web(네비+카드) / sb(SB 양식 단일 보드) HTML 생성. SB는 `generate_sb` 스캐폴드 재사용.

**★ 분기(케이스) 처리**: 분기가 있으면 **화면을 분리하지 않고** 해당 컴포넌트 옆에 케이스를 **나란히
병치**한다. `CASES` 딕셔너리에 정의(현재 U-11 결과배너 성공/실패, U-10 로딩 기본/취소가능).

규칙:
- **데이터 주도**: 07/09 행 + `ARCHETYPES` 딕셔너리에서만 읽는다. 컴포넌트(07/09 행)+렌더러
  (`chatbot_components`)만 추가하면 가이드에 **자동 반영** — 이 스크립트는 수정 불필요.
- 렌더러 없는 컴포넌트는 "준비 중" 슬롯으로 표시(카탈로그 자리는 유지).
- 프리뷰 대표값 = 사용 모듈 중 **리터럴 값(템플릿 `{{}}` 아님)이 가장 많은 모듈**. 없으면 09 기본값 합성.
- **선행 텍스트 버블 동반 규칙**: `PROMPT_PAIRED` 아키타입(`buttons` 선택버튼, `input-date`·`input-stepper`·
  `input-text` 입력 위젯)은 단독 출력 금지. 프리뷰에 대표 모듈의 U-01 텍스트(없으면 `DEFAULT_PROMPT`의
  아키타입별 기본 안내) 버블을 **선행 표시**한다.
  - U-02 선택버튼: 워크북상 항상 U-01/U-08 동반 → 실 SB는 데이터로 충족, 가이드는 실 문구 렌더.
  - 입력 위젯(U-05/06/07): **워크북에 텍스트 버블이 동반 바인딩돼 있지 않음**(단독 바인딩). 가이드는
    UX 규칙 표현용으로 기본 안내 버블을 렌더하지만, 실 SB(IT090/IT098 등)는 위젯만 단독 출력됨 →
    규칙 일치를 원하면 워크북 10시트에 U-01 동반 바인딩 추가 필요.
- `--intents` 미지정 시 워크북 전체 인텐트에서 사용처 집계. 지정 시 해당 인텐트로 한정.
- 출력: `~/Downloads/SB_챗봇/_GUIDE/` 하위 — `component-guide.html`(web) · `component-guide-sb.html`(sb).
  (환경변수 `CHATBOT_OUT` 루트 하위).

**렌더러 주의**: 배너+액션 버튼(`a_banner`)은 세로 스택 + `gap:10px`로 분리(달라붙음 방지).
이 수정은 `chatbot_components.py`에 있어 실 SB의 U-16 에러배너에도 동일 적용된다.

### 4.4 어드민 SB — 템플릿 기반 ★

관리자(백오피스) 화면. **PC 고정**(모바일/PC 질문 없음). 컴포넌트 룩은 **템플릿 1벌**
(`templates/admin-<템플릿>.html`)이 단일 출처이고, 화면 본문은 화면별로 작성한다.

```
Step 0   작성자명 입력 요청 (★ 공통)
Step 0.1 템플릿 선택 질문 (★ 필수) — "어떤 템플릿으로 만들까요?"
           - 공통 어드민(권장 기본) → admin-common  (2560px 프레임 + 무채색/그린 포인트, §4.4.2)
           - 풀무원 디자인밀 → admin-pulmuone   (좌측 GNB + 상단 유틸바 + 그린)
           - KRDS 기본 → admin-krds
           사용자가 "풀무원 버전으로"처럼 미리 답하면 그 값 사용.
Step 0.2 화면 지정 질문 — "어떤 화면을 만들까요?"
           - 등록된 화면(예: 주문상세) → 바로 생성
           - 새 화면 → 시안 이미지/설명을 받아 본문 작성 (아래 Step 1.5)
Step 1   fetch_guide.py --mode sb-pc --author "{author}" --feature-id "{ID}" --action create
Step 1.5 (새 화면만) 본문 작성:
           - templates/admin-<템플릿>.html 의 클래스(.adm-*)로 .wf-canvas 본문 + .desc-panel 작성
           - samples/admin/ADM-ORDER-001.src.html 을 패턴으로 참고 (영역마다 .adm-num 배지 1:1)
           - samples/admin/<ID>.src.html 로 저장하고 build_admin_sb.py SCREENS에 등록
Step 2   python3 .claude/skills/feature-spec/scripts/build_admin_sb.py {화면키}
           # 또는: --src samples/admin/<ID>.src.html --id <ID> --title "..." --path "..."
```

`build_admin_sb.py`가 한 번에 수행: ① 템플릿 스타일 + 화면 본문 결합 → ② `generate_sb.py --variant pc` 렌더.
출력: `~/Downloads/SB_어드민/{ID}.html` (환경변수 `ADMIN_OUT`로 변경).

규칙:
- **variant = pc 고정**. §4.0의 PC 질문 생략. 모바일 페어 콘텐츠 동일성 규칙(가이드 PC §)은 어드민 단독이라 적용 안 함.
- 넘버 배지는 프론트 표준(`.num-badge` 빨강 캡슐 스타일). `overflow:hidden` 컨테이너 안에 두지 말 것(가이드 §6.2).
- **★ n-n 서브 넘버링 (사용자 확정 2026-07-07)**: 영역 배지(n)만으로 끝내지 말 것.
  영역 내 세부 요소도 `n-m` 서브 배지(`.adm-num.sub`, 소형)로 와이어프레임에 1:1 부여
  (예: 필터 조건 4-1~4-8, 테이블 컬럼 8-1~8-15). Description의 번호와 정확히 일치시킬 것.
- 컴포넌트 룩 변경/추가는 `templates/admin-<템플릿>.html` 한 곳에서. 새 화면은 본문 src만 추가.
- 챗봇과 달리 워크북이 없으므로 **새 화면은 시안(이미지/설명) 또는 PRD**가 입력 소스.
  프로젝트에 기존 PRD가 있어도 **소스로 쓸지 사용자에게 반드시 확인** 후 진행.
- 환경변수: `ADMIN_OUT`(출력 루트, 기본 ~/Downloads/SB_어드민) · `ADMIN_AUTHOR`(작성자 기본 'AX Pilot').

### 4.4.1 ★ 풀무원 SB 표준 프로세스 (사용자 확정 2026-07-07)

"풀무원 SB 만들고 싶어"류 요청(소스 미첨부)은 아래 순서를 **고정**으로 따른다:

```
1. 작성자명 질문 (★ 공통)
2. 기능정의 엑셀(어드민 세부기능정의 워크북 xlsx) 첨부 요청
     예: 디자인밀챗봇_어드민_세부기능정의_YYYYMMDD.xlsx → ADMIN_SPEC_XLSX
3. §5.1 분기로 PRD 생성 (커버리지 기계 검증 포함) → 사용자 컨펌 대기
4. PRD 컨펌 후 §4.4 어드민 SB 생성 (템플릿: 풀무원 admin-pulmuone)
```

- 3→4 사이 컨펌 없이 SB로 넘어가지 말 것.
- 워크북 없이 시안/기존 PRD로 바로 SB를 원하면 §4.4 기본 플로우로 진행(이때도 소스 확인 질문 필수).

### 4.4.2 ★ 공통 어드민 템플릿 (admin-common) — 프레임·퍼블리싱 규격 (사용자 확정 2026-07-21)

브랜드 무관 공통 어드민의 **권장 기본 템플릿**. 디자인 시스템 단일 출처 =
워크스페이스 `90. 어드민/DesignSystem/admin-common-design-system.html` (컴포넌트 룩·토큰·상태 정의,
저장소 사본: `reference/admin-common-design-system.html` + `reference/assets/` + `reference/docs/`
+ `reference/DESIGN-SYSTEM-CONVENTIONS.md` — 워크스페이스본 수정 시 사본도 함께 갱신).
템플릿(`templates/admin-common.html`)은 이 시스템에서 추출한 것 — **룩 수정은 디자인 시스템 → 템플릿 순으로 반영**.

> **v0.2 전면 동기화 (2026-08-06)**: 디자인 시스템 v0.2와 레이아웃까지 1:1로 맞췄다.
> 헤더 64→**52px**, 콘텐츠 중앙 정렬→**좌측 정렬**(LNB 우측 95px), 로고 위치 topbar→**LNB `.brand`**,
> 테이블 헤더 배경 흰색→**#EFF3FB**, 페이지바 브레드크럼 **타이틀 위로**, LNB **`.dark` 변형** 추가,
> **아이콘 52종**(`ic-*`)을 data URI로 내장. 구 셸(v0.1)로 만든 기존 SB도 그대로 렌더된다(호환 CSS 유지).

**프레임 규격 (절대 어기지 말 것)**:

| 항목 | 값 |
|------|-----|
| `.admin-canvas` | **W 2560px 고정** · min-height 1492px (헤더 52 + 바디 1440) |
| 헤더 `.adm-topbar` | **H 52px** · `.adm-col` 안에 위치해 LNB 우측 폭(2300px) 차지 · 로고 없음(계정/유틸만) |
| LNB `.adm-gnb` | W 260px · 상단 `.brand`(서비스명) · 다크 서페이스는 `.adm-gnb.dark` |
| 콘텐츠 `.adm-content` | **W 1440px 고정** · `.adm-main`이 `padding-left:95px`로 **좌측 정렬**(중앙 정렬 아님, 우측 765px는 여백) |
| 수직 여백 | 콘텐츠 상단 48px / 하단 96px (`.adm-content` padding에 내장) |
| 수직 리듬 | 카드 간 24px(`.adm-content` gap) · 섹션 간 40px(`.adm-sec-gap` 16px 추가) · 카드 패딩 24px |
| 컨트롤 높이 | 기본 40 · 소형 32 · 대형 48 · 모달 풀버튼 52 |

**본문 골격** (src 작성 시 이 구조 고정 — 헤더가 `.adm-col` 안으로 들어간 것이 v0.1과의 차이):
```html
<div class="wf-canvas admin-canvas">
  <div class="adm-body">
    <div class="adm-gnb dark">
      <div class="brand"><strong class="tit">서비스명</strong><span class="desc">부제</span></div>
      <div class="grp open">그룹명 <span class="cv"></span></div>
      <div class="sub"><a class="active">메뉴</a></div>
    </div>
    <div class="adm-col">
      <div class="adm-topbar">…계정·유틸…</div>
      <div class="adm-main"><div class="adm-content">
        <div class="adm-pagebar">…</div>
        <!-- 필터 카드 / 툴바 / 테이블 / 페이지네이션 … -->
      </div></div>
    </div>
  </div>
</div>
```

**아이콘 (v0.2 신규)**: `<span class="adm-icon ic-<이름> sz-<크기>"></span>` — 52종이 템플릿에 data URI로
내장돼 있어 별도 파일 참조 없이 SB 단독 HTML에서 바로 렌더된다. 크기는 `sz-12/13/14/15/16/18`.
**어두운 배경(Primary `.adm-btn`) 위에는 흰색 변형** `ic-search-wh` / `ic-edit-wh`를 쓴다(기본 아이콘은 검정이라 안 보임).
텍스트 글리프(`«` `›` `✎` `↺` `⌕`)로 아이콘을 대신하지 않는다.
아이콘 목록·용도는 `reference/docs/foundation/icons.md`, 컴포넌트별 스펙은 `reference/docs/components/*.md`,
클래스/토큰 규칙은 `reference/DESIGN-SYSTEM-CONVENTIONS.md` 참고(모두 디자인 시스템 v0.2 사본).

**디자인 규칙**: 무채색 기본(Primary 버튼 = g900 검정). 컬러는 상태 전용 —
Green(태그·토글 ON), Red(공지·삭제·에러), Blue(텍스트 링크). 폰트 Pretendard
(generate_sb.py 보일러플레이트가 CDN 로드, 템플릿 `--adm-font`로 강제).
선택 컨트롤: **다중 선택 = 사각 체크박스(.adm-check) · 배타 선택 = 점 라디오(.adm-radio)** 각 1종만.

**퍼블리싱 품질 (HTML-to-Figma + 개발 직행)**: 이 템플릿의 SB는 와이어프레임이자
퍼블리싱 산출물이다 — ① 시맨틱 마크업(table은 `<table>`, 버튼은 button성 요소)
② 레이아웃은 flex/grid로 실제 동작(absolute 좌표 배치 금지, .adm-num 배지 제외)
③ 색·치수는 템플릿 CSS 변수만 사용(임의 hex/px 최소화) ④ Description desc-block 규칙(§4 ★) 동일 적용.

**★ 넘버 배지 오버레이 (사용자 확정 2026-07-22)**: 배지는 와이어프레임 레이아웃에
영향을 주면 안 된다 — 인라인(static) 배치 금지, `<br>`로 줄 분리 금지. 영역 배지·세부
배지(.adm-num.sub) 모두 absolute 오버레이(th/td/.adm-field/.adm-kv>div는 템플릿이 relative 처리,
기본 오프셋 -8~-10px). 버튼·셀렉트 등 단일 요소에는 `.adm-anchor` 래퍼로 감싸 부여.

**★ 팝업 = 별도 SB 페이지 (사용자 확정 2026-07-22)**: admin-common에서는 §4의
서브 캔버스 규칙 대신 **모달/팝업을 별도 SB 페이지로 분리**한다 (화면ID -00N 증분,
예: ADM-MAIN-002 배너 등록/수정 팝업). 팝업 페이지 캔버스 = 회색 스테이지(#DFE2E6)
중앙에 .adm-modal 배치, 부모 화면 desc에 «연결 SB» 상호 참조 표기.
**알럿·토스트류 경량 오버레이만** 같은 장 우측 서브 캔버스 허용.

**★ SB 시트 양식 (사용자 확정 2026-07-28 — 레퍼런스 화면설계서 기준)**

시트 골격은 `generate_sb.py` + `sb-style-block.html`이 자동 처리한다 — src에서 재정의 금지:
- 메타 테이블 2행: 1행 «화면/컴포넌트·값 | Local·KO | 화면ID·작성자·작성일(라벨)» /
  2행 «화면경로·값 | Channel·값 | 화면ID값·작성자값·작성일값». th 배경 #E9E9E9 + 글자 #111.
- 작성일 = YYYY-MM-DD 전체 날짜, 어드민은 Channel=Admin (`build_admin_sb.py`가 channel 전달).
- 시트 가장자리 여백 40px(상단 28px) — 메타/본문이 가장자리에 붙지 않음. 시트 좌상단 타이틀 없음.
- 좌측 와이어프레임 영역 = .wf-panel 1px 외곽선 박스.
- 푸터: 시트 끝~끝 전폭 구분선 + 우측 하단 ETRIBE 로고만 (버전 표기 없음). 본문이 짧아도 시트 하단 고정.

**Description 패널(src 작성 시) 규칙 — 섹션은 정확히 2개**:
1. «화면 설명» — 화면 유형·경로·연결 SB·프론트 연동 등 개요 bullet만.
   **화면ID·화면명 라인 넣지 않음** (메타 테이블과 중복).
2. «Description» — 번호 항목(1~N, 배지와 1:1) 전체. 동작·예외 항목은 별도 섹션으로 만들지 말고
   Description 하단에 `[동작 / 예외]` 라벨 li 이후 이어서 작성.
섹션 헤더/본문 스타일(연회색 헤더, 본문 16px 통일)은 스타일 블록이 처리 — desc-block 규칙(§4 ★)만 준수.

**★ 필터 카드 배치 (사용자 확정 2026-07-29)**: 키워드 검색 조합(검색 기준 셀렉트 + 검색어 인풋)은
필터 카드에서 **항상 맨 아래**(그리드 = 마지막 행, 인라인 = 액션 앞 맨 뒤)에 배치한다.
배지 번호는 정의서 번호를 따르므로 시각 순서와 달라도 무방.

**★ 배지 겹침 금지 (사용자 확정 2026-07-29)**: 영역 배지(n)와 세부 배지(n-m)가 같은 자리에
겹치면 안 된다. 템플릿이 자동 분리 —
- 세부 배지는 **대상 요소의 시작점 위(left:0)**: 테이블 th는 컬럼 좌측 시작점, 앵커(.adm-anchor)는 요소 좌측.
- **테이블 영역 배지는 좌측 바깥(left:-30px)** — 첫 컬럼 세부 배지와 충돌 회피.
인라인 스타일로 배지 위치를 재정의할 때도 서로의 점유 영역(배지 크기 ≈ 22×22px)을 침범하지 말 것.
검증법: 전 배지 쌍의 rect 교차 검사 = 0건.


§3 PRD 전체 수행 → 사용자에게 SB 진행 의사 확인 → §4 SB 수행.
PRD 작성 시 Step 0/2.5는 그대로 적용.

### 5.1 어드민 세부기능정의 워크북 → PRD ★

소스가 **어드민 세부기능정의 워크북(xlsx)** 인 경우의 PRD 분기. **산출물 = PRD만.**
시트 구조: `항목(메뉴) / 세부항목 / 기능(번호 아웃라인) / 세부기능(규칙 산문) / 비고 / 진행여부 / 예시 화면 / 기능매핑`.
목표 = **누락 0**: 워크북의 모든 기능 라벨·규칙·예외가 PRD에 반영되고, 이를 **기계 검증**으로 보증한다.

★ 일반 PRD 모드(§3)와 다른 점 — **검토 절차 전부 생략**:
- Step 0.1 프로세스 입력 질문 X (워크북이 프로세스 정의를 대체)
- Step 2.5 Mermaid 프리뷰/승인 루프 X (플로우차트는 PRD §3 본문에 바로 포함)
- Step 3.5 화면별 체크리스트 질문 X — 워크북 미정의 항목은 ETRIBE 공통 패턴을
  자동 적용하되 PRD에 **«(제안)»** 표기로 구분. 비즈니스 결정이 꼭 필요한 것만 질문.

```
Step 0   작성자명 입력 요청 (★ 공통)
Step 0.1 워크북 경로(ADMIN_SPEC_XLSX) + 대상 항목(메뉴) + 기능ID 확인
           - 기능ID 제안: ADM-{항목 영문 슬러그} (예: 챗봇 대화 내역 → ADM-CHAT)
Step 1   python3 .claude/skills/feature-spec/scripts/parse_admin_spec.py --id {ID}
           → _build/{ID}_spec.json + _build/{ID}_checklist.md
           체크리스트 = 기능 라벨(하드) · 예외(PRD §5 필수) · 조건 분기 · 규칙(Default/포맷/옵션)
Step 2   9섹션 PRD 작성 (가이드 §3 구조 그대로, 프리뷰 없이 일괄 작성)
           - §3 플로우차트: Mermaid 6도형/색상 규칙으로 본문에 포함 (승인 루프 없음)
           - §5 예외 처리: 체크리스트 «예외» 전수 + 공통(조회 0건·API 실패·권한)은 «(제안)» 표기
           - §6 화면별 UI: 체크리스트 «기능 라벨» 전수 + 규칙(Default·포맷·옵션) 반영
Step 3   저장 전 커버리지 검증 (★ 필수, 통과까지 반복):
           python3 .../parse_admin_spec.py --id {ID} --verify {PRD.md}
           → 누락 라벨 0 될 때까지 보완. «매칭 약한 규칙»은 직접 확인 후 진행.
Step 4   Write로 저장: 90. 어드민/PRD/{기능ID}_{영문슬러그}.md (워크스페이스 기준)
           verify 출력(✓/✗)을 사용자에게 그대로 보여주고 완료 보고.
```

규칙:
- 검증(Step 3)을 건너뛴 채 저장/완료 보고 금지.
- 워크북에 없는 동작을 임의 추가하지 않는다. 보완이 필요하면 «(제안)» 표기로 구분(비고 열 참고).
- `진행여부`·`기능매핑` 열 값이 있으면 PRD §1(개요)·§6에 반영.
- **SB는 여기서 만들지 않는다.** 필요 시 사용자가 별도로 요청하면 §4.4 어드민 SB 분기로 진행
  (이때 PRD·체크리스트를 입력 소스로 사용, Description 기능번호 1:1 규칙 동일).
- 환경변수: `ADMIN_SPEC_XLSX`(워크북 경로, 필수).

## 6. 부분 수정

기존 PRD/SB 파일은 Edit 툴로 직접 수정. 생성 스크립트(generate_sb.py) 불필요.
SB 수정 시 `desc-block` 구조 유지 (§4 ★ 참고).

## 7. 보안

가이드는 디스크 미저장. fetch 결과는 메모리에서만 사용.
`cat SKILL.md` 해도 가이드 본문 노출 X (절차서만).

## 트러블슈팅 / 사전설정 / 사용법 안내

→ `ONBOARDING.md` 참고.

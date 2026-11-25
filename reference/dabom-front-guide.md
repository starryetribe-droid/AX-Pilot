# 다봄 프론트 와이어프레임 가이드 (front-dabom v0.3)

다봄(고대 AI 심리 앱) 프로젝트 **전용** 프론트 SB 규칙과 컴포넌트 카탈로그.
SKILL.md §4.0.0에서 «다봄 SB»로 답하면 이 문서를 따른다.

- **기준 화면(1순위)**: Figma «사진첩_상세 Ver.0.3» — 실제 다봄 SB 작성 방식
  https://www.figma.com/design/w1l4o5F4fU3gnY2viMzc00/?node-id=1385-7006
- **컴포넌트 보조 출처**: Figma «00. 공통» 페이지 (Header 변형·App bar·CTA·Input·Layer 등)
  https://www.figma.com/design/w1l4o5F4fU3gnY2viMzc00/?node-id=22-294
  → 두 출처가 다르면 **기준 화면이 우선** (크기·색·배치·표기).
- **템플릿**: `templates/front-dabom.html` · **빌더**: `scripts/build_dabom_sb.py` (빌드 직후 Figma 보정 `scripts/figma_safe_dabom.py` 자동 실행 — §6)
- **샘플**: `samples/dabom/DABOM-SAMPLE-001.src.html` = 기준 화면 재현(사진첩_상세 — 배지·Case·하단 흐름),
  `DABOM-SAMPLE-002.src.html` = 입력 폼(Input·하단 고정 CTA·Confirm·Toast)
- Figma가 바뀌면 **템플릿 → 이 문서** 순으로 갱신하고 HISTORY.md에 기록.

## 1. 시트 배치 (공통 SB와 다른 점)

```
┌ 메타 헤더 (공통) ───────────────────────────────────────────────┬──────────────┐
│ ① 와이어프레임 390     ② Case 변형 (우측 가로 나열, 358폭)          │ 화면 설명     │
│  (좌상단, 가운데 X)     [Case2) 키워드] [Case3) 일상] [Case4) …]     │ Description  │
│                                                                 │              │
│ ③ 하단 흐름: [삭제 여부 Confirm] ··▶ [이동 노트] ··▶ [삭제 완료 Toast msg] │
│    (와이어프레임의 버튼 위 손가락 아이콘 ┆ 점선 ▼ 으로 해당 Confirm과 연결)   │              │
└─────────────────────────────────────────────────────────────────┴──────────────┘
```

| 항목 | 값 |
|---|---|
| 채널 / variant | Front / **모바일 고정** (PC·태블릿 질문 생략) |
| 시트 | 2560 (공통 규격), Description 패널 공통 |
| 와이어프레임 | `.wf-panel.dabom-board` 안 **좌상단** · `.wf-canvas.dabom-canvas` **390 × min 844** · 프레임선 2px #CED4DA · 라운드 8 (템플릿은 outline, 빌드 후 border로 자동 보정 — §6) |
| 콘텐츠 | 좌우 여백 16 → **358** (`.dbm-main` 또는 `.wf-content-area`) — 공통 MO 340 규칙 대신 다봄 Figma 값 |
| Case 변형 | `.dbm-cases > .dbm-case` 와이어프레임 **우측**에 가로 나열, 각 위에 `.dbm-tag` «CaseN) 이름» |
| Alert/Confirm/Toast | 와이어프레임 **하단** `.dbm-flow`에 가로 나열. 각 창 위에 **회색 유형명 바** `.dbm-ov-title`(«{용도} Confirm», «{용도} Toast msg»). 우측 서브 캔버스 규칙은 다봄에 적용하지 않음 |
| 이동·결과 표기 | `.dbm-note` 회색 박스 «[화면명] 화면으로 이동» + `.dbm-arrow` 점선 화살표 |
| 탭 동작 표시 | `.dbm-tap` = Figma «Tap» **손가락 아이콘**(원본 SVG, 손끝 주황 점) + **점선 화살표**. `style="left:X;top:Y"`에 손끝 좌표, 점선은 `--down:Npx`(아래로 — 하단 흐름의 Confirm/Toast 유형명 바까지) / `--right:Npx`(오른쪽으로 — 상태 변화 결과까지). 점선 끝이 대상 바로 앞(약 2px)에 오도록 길이 지정. 흐름 항목 사이는 `.dbm-arrow`(같은 점선+화살촉) |
| 수정 이력 | `.dbm-ver` «Ver.0.3 (1)» — 버전 변경된 영역 옆에 표기 |
| 화면 ID | `FO-SB-{메뉴코드}-{3자리}` (예: 사진첩 `FO-SB-ALB-010`) — 프로젝트 IA 채번 우선 |

## 2. 넘버링

| 종류 | 클래스 | 모양 / 위치 |
|---|---|---|
| 기능 번호 1~N | `.num-badge` | **반투명 레드 원 31px**(rgba(255,0,0,.6)) · 흰 볼드 15 · 요소 **좌상단 모서리에 걸침**(-15/-15, 오버레이) |
| 입력 필드 / 좌상단 텍스트 요소 | `.dbm-field > .num-badge` 자동, 그 외 `.num-badge.edge` | 캔버스 가장자리 쪽으로 빼서 라벨 가림 방지 |
| 세부 번호·Case | `.dbm-tag` (`.pin` = absolute) | **짙은 레드 캡슐**(rgba(119,13,28,.62)) · 흰 볼드 15 · 높이 22 — «3-1», «Case1) 사진» |

- 헤더 등 공통 컴포넌트는 화면 기능이 없으면 번호를 붙이지 않는다(기준 화면도 Header 무번호).
- 배지·태그끼리 겹치지 않게 배치(검증: rect 교차 0건).

## 3. 컴포넌트 카탈로그 (`.dabom-canvas` 안)

시니어 대상 앱 — **본문 18px**(lh 30) · 버튼 60 · 라운드 8 · Noto Sans KR · 무채색(#525252 계열).

| 컴포넌트 | 클래스 | 값 / 규칙 |
|---|---|---|
| Header | `.dbm-header` > `.back`(`.di-back` + `.title`) · `.logo` · `.acts`(`.bell`·`.di-my`·`.di-menu`·`.di-setting`) | 56 · 타이틀 Bold 18 #1F2937 · 최상단 Sticky. 변형: **Main**(로고·알림·마이·메뉴) / **Sub**(←·Title·알림·마이·메뉴) / **Test**(←) / **Chatbot·Policy**(←·Title) / **Reward**(←·알림·마이·메뉴) / **Notice**(←·Title·설정) / **My page**(←·Title·알림·메뉴) |
| 알림 Badge | `.bell > .dot` | 새 알림 시 노출, 알림 화면 진입 시 사라짐. 1차 개발 제외 시 `.is-hidden-1st` + `* 1차 개발 시 Hidden` |
| 날짜 행 | `.dbm-date > .d`(`.di-calendar` + 텍스트) | 24px #171717 · 형식 «YYYY년 MM월 DD일» |
| 즐겨찾기 | `.dbm-fav` > `.di-heart` / `.di-heart-on` | 원형 52 · #FAFAFA · 2px #E5E5E5 |
| 이미지 영역 | `.dbm-img` | #D4D4D4 · 라운드 8 · 기본 높이 320 · 가운데 설명 18px |
| 텍스트 보기 | `.dbm-textview` | #FAFAFA · 1px #E5E5E5 · 라운드 8 · 18px/30 · only view |
| 버튼 | `.dbm-btn` (Primary #525252 h60 흰 글자) · `.secondary`(#F5F5F5·#D4D4D4·#404040 h62) · `.tertiary`(#FAFAFA·#E5E5E5·#525252 h62) · `.disabled` | 아이콘+텍스트 gap 12 · 2열은 `.dbm-btn-row`(gap 16) · 세로 묶음 `.dbm-btns`(gap 16) |
| CTA (하단 고정) | `.dbm-cta.wf-bottom-fixed > .secondary + .primary` | 60 · 최대 2개 · 좌 Negative / 우 Positive · 키패드 호출 시 키패드 위(`.dbm-keypad`) |
| App bar | `.dbm-appbar.wf-bottom-fixed > .tab(.on)` | 68 · 최하단 Sticky · **홈 / 두뇌 건강 / 대화 / 내 정원 / 사진첩** |
| Input | `.dbm-field > .label + .dbm-input(.error/.disabled)` + `.dbm-err` | 52 · 라운드 8 · 18px · Clear `.di-clear` · 검색 `.di-search` · 비밀번호 `.di-eye` · 인증 `.timer` |
| Select / Radio / Check / Toggle / Chip | `.dbm-select` · `.dbm-radio(.on)` · `.dbm-check(.on)` · `.dbm-toggle(.on)` · `.dbm-chips > .dbm-chip(.on)` | 선택 상태 = #525252 (무채색) |
| Tabs / Indicator / Accordion | `.dbm-tabs > .t(.on)` · `.dbm-dots > i(.on)` · `.dbm-pageno` · `.dbm-acc > .q + .a` | |
| Layer | `.dbm-dim` + `.dbm-bs`(Half) / `.dbm-bs.full` · `.dbm-layer-head(.di-close)` · `.dbm-layer-title` | Title 최대 1줄 · Dimmed/X 탭 시 닫힘. Full Layer Popup은 별도 SB 화면 |
| **System Alert / Confirm** | `.dabom-sysalert`(Android) / `.dabom-sysalert.ios` → `.dbm-flow > .dbm-ov` 안 | 280 · 라운드 2 · Material 그림자 · 메시지 16/24 #3C3C43 · 버튼 Roboto Medium 14 **#5856D6** 우측 정렬. **OS 기본 Alert 사용** |
| **Toast msg** | `.dbm-toast` → `.dbm-flow > .dbm-ov` 안 | 343 × 46 · rgba(0,0,0,.8) · 라운드 7 · 14px 흰 글자 · 최대 1줄 |

아이콘 `.di.di-*`: Figma 원본 9종(back·bell·my·menu·calendar·heart·share·edit·trash, data URI 내장) +
보조 라인 아이콘(heart-on·setting·close·clear·search·eye·clock·down·plus). 크기 `.s20` `.s18`.
텍스트 글리프(← × ⌕)로 대신하지 않는다.

## 4. Description 작성

공통 규칙(SKILL §4 ★ — desc-block 구조, `{라벨} {영문 컴포넌트명}` — 대괄호 없이, Alert/Confirm 영문 표기)에 더해
기준 화면의 문장 패턴을 따른다:

- «화면 설명» = 화면 목적 **한 문장** (예: «다봄이와 기억 찾기 시 수집된 이미지와 기억 요약을 확인하는 화면»).
- 동작은 «**탭 시,** …»로 시작. 화면 이동은 «[화면명] 화면으로 이동함», 오버레이는 «[용도] Confirm 제공» / «[용도] Toast msg 제공».
- 형식 표기: «형식 : YYYY년 MM월 DD일». 기존과 같으면 «(AS-IS 동일)», 공통 기능은 «(공통 가이드를 따름)».
- Case가 있는 항목은 «CaseN) 이름» 나열 + 하위 «N-1) …»로 조건별 차이 설명 (와이어프레임 `.dbm-tag`와 1:1).
- 조회 전용은 «only view». 1차 개발 제외는 `* 1차 개발 시 Hidden`.
- Alert/Confirm은 «(System Alert)» 명시.

## 5. UX Writing (Figma «UX Writing Guide»)

- 모든 콘텐츠는 **친근한 비격식체 «-해요체»**, 서술어 종결 서술형. 능동·긍정형, 고객 관점.
  - 예: «삭제하시겠어요? 삭제하시면 다시 볼 수 없어요.» / «예약이 완료되었습니다» → «예약을 완료했어요»
- 6원칙: 유익 · 명확 · 간결 · 생동감 · 일관 · 고객관점. 외래어·한자어 → 쉬운 우리말, 줄임말 지양, 번역 투·이중 높임 제거, 30자 내외.
- 자사 지칭 «당사» → «다봄».
- 문장 유형: 정보안내(이용안내·유의사항·약관) «시작합니다.» · 흥미유발(서비스 소개·제안) «시작할까요?» ·
  행동요청(입력/선택 유도) «시작해 주세요» · 의사확인(1:1 상황) «시작하시겠어요?» · 광고(배너·마케팅) «시작!»
- 날짜 `YYYY-MM-DD (수)` (단독 요일은 «수요일»). 화면 표시용 날짜는 화면별 형식(예: «YYYY년 MM월 DD일») 우선.
- 와이어프레임 예시 문구·Toast·Alert 메시지도 이 규칙으로 작성.

## 6. Figma 내보내기 (HTML to Figma) 규칙

HTML→Figma 변환기는 CSS로만 그린 요소(outline·가상 요소·CSS 변수·그라데이션 점선·음수 margin·배경 이미지 위치)를 옮기지 못한다.
`build_dabom_sb.py`가 빌드 직후 `figma_safe_dabom.py`로 아래를 **자동 보정**한다 (브라우저 모습은 그대로, 여러 번 실행해도 결과 같음).

| 대상 | 템플릿 방식 | 보정 후 |
|---|---|---|
| 휴대폰 프레임선 | outline | 실제 border 2px (콘텐츠 폭 390 유지) |
| 탭 점선 화살표 `.dbm-tap` | ::before/::after + `--right`/`--down` + 그라데이션 | 인라인 SVG (점선 + 열린 화살촉) |
| 흐름 화살표 `.dbm-arrow` | 그라데이션 점선 배경 | 인라인 SVG 40×8 |
| Checkbox · Radio · Toggle · App bar 아이콘 | ::before/::after | 실제 `<i class="fsb">` / `<i class="fsa">` |
| 푸터 로고 | 배경 이미지 | 실제 `<img>` (우측 정렬) |
| 시트 좌우 여백 | 음수 margin | 블록별 margin (푸터 구분선이 시트 끝까지) |

**시트 선 규칙 (26.11.25 확정)**

- 시트 바깥 외곽선 **없음** (border·inset 그림자 제거)
- 메타 표 외곽선 · 본문 영역 좌우선 · 와이어프레임∣Description 구분선 · 푸터 구분선 = **표 내부 선과 동일 (gray-20, 1px)**
- 와이어프레임 패널 자체 테두리 없음 (본문 영역 좌우선과 겹치지 않게)

**src 작성 시**

- 위 요소는 템플릿 클래스(`.dbm-tap`·`.dbm-arrow`·`.dbm-check` 등)를 그대로 쓰고, 보정용 마크업을 직접 넣지 않는다.
- src에서 `outline` · `::before`/`::after` · 그라데이션 점선 · 음수 margin · 배경 이미지로 그림을 새로 만들지 않는다 → Figma에서 빠짐.
- 보정 생략이 필요하면 `build_dabom_sb.py --no-figma-safe`.
- 예전에 만든 SB 재보정: `python scripts/figma_safe_dabom.py <SB 폴더 또는 html>` (이전 버전 보정 파일은 시트 선 블록만 최신으로 교체).

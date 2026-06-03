# 챗봇 SB 생성 가이드

풀무원 디자인밀 **AI 챗봇 인텐트 워크북(xlsx)** 을 입력으로, KRDS 규격의 **챗봇 SB 와이어프레임(HTML)** 을 자동 생성한다.

화면을 손으로 그리지 않는다. 워크북의 `09_컴포넌트스키마`(렌더 계약) + `10_모듈콘텐츠바인딩`(값)만으로 화면이 만들어지고, 컴포넌트별 마크업은 **아키타입 렌더러 1벌**(`scripts/chatbot_components.py`)이 단일 출처로 생성한다. 이는 AX Pilot 서버 가이드 **§13 «챗봇 컴포넌트 카탈로그»** 의 구현체다.

> 이 기능은 `feature-spec` 스킬에 통합되어 있다. 별도 설치 없이, 스킬을 가진 팀원이라면 누구나 동일하게 사용한다.

---

## 1. 사전 준비

| 항목 | 설명 |
|------|------|
| **feature-spec 스킬** | `~/.claude/skills/feature-spec` 에 설치(=git clone). 업데이트는 `git pull`. |
| Python 3 + openpyxl | `pip install openpyxl` (워크북 읽기에 필요) |
| **인텐트 워크북** | `..._인텐트정의_보완_*.xlsx` (08·09·10 시트 포함). 경로는 환경변수 `CHATBOT_XLSX` 로 지정. |
| `~/.etribe/config.json` | SB 양식 가이드(§13)를 서버에서 fetch할 때 필요(`server_url`·`token`). |

---

## 2. 사용법

### 2.1 Claude에게 자연어로 (권장)

스킬을 쓰던 그대로, 채팅에 이렇게 말하면 된다:

```
인텐트 9 챗봇 SB 생성해줘
```

→ 스킬이 **SKILL §4.2 «챗봇 SB» 분기**로 진입해, 작성자명과 워크북 경로(`CHATBOT_XLSX`)를 확인한 뒤 SB 일체를 생성한다. (variant = mobile 고정, 일반 PRD SB의 화면 분리·수기 작성 단계는 건너뛴다.)

### 2.2 터미널에서 직접

```bash
# 인텐트 번호 1개 → SB 일체 생성
CHATBOT_XLSX="/path/to/인텐트정의_보완.xlsx" \
python3 ~/.claude/skills/feature-spec/scripts/build_chatbot_sb.py 9
```

출력: `~/Downloads/SB_챗봇/IT009/`
- `index.html` — 모듈(단계)별 화면을 라벨과 함께 묶은 인덱스
- `IT009-*.html` — 화면별 SB

미리보기 서버:

```bash
python3 ~/.claude/skills/feature-spec/scripts/serve.py
# → http://127.0.0.1:8765/IT009/index.html
```

---

## 3. 환경변수

| 변수 | 기본값 | 용도 |
|------|--------|------|
| `CHATBOT_XLSX` | (로컬 샘플 경로) | 인텐트 워크북 xlsx 경로 — **팀원은 반드시 지정** |
| `CHATBOT_OUT` | `~/Downloads/SB_챗봇` | SB 출력 루트 |
| `CHATBOT_AUTHOR` | `AX Pilot` | SB 메타 헤더 «작성자» 값 |

---

## 4. 동작 원리 (파이프라인)

```
build_chatbot_sb.py <인텐트#>
  ① chatbot_to_sb.py        워크북(08 메타 + 09 렌더계약 + 10 바인딩) → _build/IT###_screens.json
  ② generate_sb.py --variant mobile   screens.json → 화면별 SB HTML
  ③ build_index()           08/09/10 메타 → 라벨 단 iframe index.html
```

- `chatbot_to_sb.py` — 워크북 → SB `screens.json` 변환기. 컴포넌트별 하드코딩 없이 09 계약으로 아키타입을 디스패치한다.
- `chatbot_components.py` — 12종 KRDS 아키타입 렌더러. 마크업의 단일 진실(§13 구현체).
- `generate_sb.py` — screens.json → 화면별 SB HTML (일반 SB와 동일 엔진, variant=mobile).

중간 산출물(`scripts/_build/`)과 출력물(`IT###/`)은 재생성 가능하므로 git에 포함하지 않는다.

---

## 5. 워크북 구조 (입력)

| 시트 | 역할 |
|------|------|
| `08_*` | 인텐트 메타 + 모듈(단계) 목록 — 화면 = 모듈 |
| `09_컴포넌트스키마` | **렌더 계약**: `렌더아키타입`(컴포넌트→아키타입), `렌더역할`(슬롯→역할) |
| `10_모듈콘텐츠바인딩` | 각 슬롯에 들어갈 **값**(바인딩) |

화면은 09(계약) + 10(값)만으로 결정된다. 변환기·SKILL은 컴포넌트별 분기를 모른다 — 전적으로 데이터 주도.

---

## 6. KRDS 아키타입 12종

16개 컴포넌트(U-01~U-16)를 12종 아키타입으로 정규화한다. 마크업 표준의 전체 정의는 가이드 **§13.3 / §13.4** 참조.

| 아키타입 | 대응 컴포넌트(U-##) | 용도 |
|----------|--------------------|------|
| `text` | U-01 | 텍스트 말풍선 |
| `buttons` | U-02 · U-12 | 버튼/퀵리플라이 |
| `kv-card` | U-03 · U-08 | 키-값 요약 카드 |
| `card-list` | U-04 · U-13 | 카드 리스트 |
| `input-date` | U-05 | 날짜 입력 |
| `input-stepper` | U-06 | 수량 스텝퍼 |
| `input-text` | U-07 | 텍스트 입력 |
| `payment` | U-09 | 결제 |
| `loading` | U-10 | 로딩 |
| `banner` | U-11 · U-16 | 배너/알림 |
| `link` | U-14 | 링크 |
| `transfer` | U-15 | 상담사 이관 |

---

## 7. 새 컴포넌트(아키타입) 추가

새 시각 유형이 필요하면 **`chatbot_components.py` 에 아키타입 렌더러 함수만 추가**하고 `ARCHETYPES` 레지스트리에 등록한다(§13.4). 변환기(`chatbot_to_sb.py`)와 SKILL은 수정하지 않는다 — 워크북 09의 `렌더아키타입` 값이 새 키를 가리키면 자동 디스패치된다.

---

## 8. 설계 완료 인텐트

08·10 시트에 모듈/바인딩이 채워져 바로 생성 가능한 인텐트:

`7 · 9 · 10 · 14 · 16 · 17 · 44 · 50 · 54 · 59 · 87 · 90 · 98`

---

## 9. 트러블슈팅

| 증상 | 원인 / 해결 |
|------|-------------|
| `FileNotFoundError: ...xlsx` | `CHATBOT_XLSX` 미지정 또는 경로 오타. 워크북 절대경로로 지정. |
| `ModuleNotFoundError: openpyxl` | `pip install openpyxl` |
| `[WARN] 로고 파일 없음: .../reference/etribe-logo.png` | 무시 가능. 챗봇 SB 로고는 `templates/sb-logo-data-url.txt`(base64)에서 임베드되며, 이 WARN은 PRD 플로우용 무결성 체크다. |
| 화면이 비어 보임 | 해당 인텐트의 09/10 시트 바인딩 누락. 설계 완료 인텐트 목록 확인. |
| 미리보기 404 | 먼저 해당 인텐트를 생성해 `CHATBOT_OUT/IT###/` 가 존재해야 함. |

---

## 참고

- SB 작성 표준(KRDS 컴포넌트 카탈로그·렌더 계약·공통 규칙)은 AX Pilot 서버 가이드 **§13 «챗봇 컴포넌트 카탈로그»** 에 정식 반영되어 있다.
- 스킬 동작 절차는 `SKILL.md §4.2` 참조.
- 변경 이력·아키텍처는 `HISTORY.md` 참조.

# 데이트피커 (`.adm-date`)

원본: [admin-common-design-system_v02.html](../../admin-common-design-system_v02.html) §3.3

> **v0.2 변경**: 원본 카탈로그의 `<span class="adm-date">`는 클릭해도 아무 반응이 없다. 실제 페이지에서는 `<button type="button">`을 사용해 최소한 포커스·클릭·키보드 조작이 되게 한다.
>
> **v0.2 추가**: `<button class="adm-date">` 클릭 시 `input type="date"`처럼 캘린더 팝오버(`.adm-date-panel`)가 열려 시작~종료일을 선택한다. 동작은 `assets/js/adm-interactions.js`, 스타일은 `assets/css/components/adm-date.css`에 있다(별도 빌드 도구 없는 순수 JS/CSS).

## 개요

직접 기간을 지정하는 컨트롤. 칩 프리셋과 나란히 배치하거나 필터 카드의 필드로 사용한다.

## 클래스 계약

| 구분 | 클래스 | 설명 |
|---|---|---|
| 루트 | `button.adm-date` | 날짜 표시/선택 트리거 — 실제 `<button type="button">`, `aria-haspopup="dialog"` `aria-expanded` 포함 |
| 내부 | `.adm-date .lead` | (선택) 날짜 텍스트를 묶는 래퍼 — 필터 카드처럼 `justify-content:space-between`으로 아이콘을 오른쪽 끝에 붙일 때 사용 |
| 내부 | `.adm-date .d-start` | 시작일 텍스트 — JS가 이 요소의 `textContent`를 읽고 쓴다 |
| 내부 | `.adm-date .tilde` | 기간 구분(~) |
| 내부 | `.adm-date .d-end` | 종료일 텍스트 — JS가 이 요소의 `textContent`를 읽고 쓴다 |
| 내부 | `.adm-date > .adm-icon` (직계 자식) | 캘린더 아이콘 — `class="adm-icon ic-calendar sz-14"`로 지정한다. 장식용이므로 `aria-hidden="true"`. CSS는 `margin-left:auto`(우측 고정)와 `opacity:.6`(톤)만 담당 |
| 팝오버 | `.adm-date-panel` | 캘린더 팝오버 루트. `body` 하위에 JS가 지연 생성해 하나만 재사용한다 |
| 팝오버 내부 | `.cal-head` `.cal-nav`(`.cal-prev`/`.cal-next`) `.cal-ttl` | 월 이동 헤더 |
| 팝오버 내부 | `.cal-grid` `.wd` `.day`(`.other`/`.today`/`.range-start`/`.range-end`/`.in-range`) | 요일 헤더 + 날짜 그리드 |
| 팝오버 내부 | `.cal-foot` `.cal-range-txt` `.cal-reset` `.cal-apply` | 선택 요약 + 초기화/적용(기존 `.adm-btn` 재사용) |

## 스펙

| 항목 | 값 |
|---|---|
| 높이 | 40px |
| 테두리 | `1px solid var(--line-strong)`, 팝오버 열림/포커스 시 `var(--g900)` |
| 라운드 | `--r-md` (팝오버는 `--r-lg`) |
| 폰트 | 13.5px, `var(--g800)` |
| 팝오버 너비 | 296px, `var(--shadow-modal)` |

## HTML 스니펫

```html
<button type="button" class="adm-date" aria-haspopup="dialog" aria-expanded="false">
  <span class="d-start">2025-12-24</span> <span class="tilde">~</span> <span class="d-end">2025-12-27</span>
  <span class="adm-icon ic-calendar sz-14" aria-hidden="true"></span>
</button>
```

캘린더 아이콘은 다른 아이콘과 똑같이 `.adm-icon ic-calendar sz-14` 클래스로 지정한다([icons.md](../foundation/icons.md)). [adm-date.css](../../assets/css/components/adm-date.css)의 `.adm-date > .adm-icon` 규칙은 **배치(`margin-left:auto`)와 톤(`opacity:.6`)만** 담당하며 아이콘 경로·크기는 주지 않는다 — `ic-*`/`sz-*` 클래스를 빼면 아이콘이 아예 보이지 않는다.

## 동작

- 트리거를 클릭하면 캘린더 팝오버가 열리고, 같은 트리거를 다시 클릭하거나 바깥을 클릭하거나 Esc를 누르면 닫힌다(모달과 동일 규칙).
- 팝오버 오픈 시 트리거의 `.d-start`/`.d-end` 텍스트를 파싱(`YYYY. MM. DD` 또는 `YYYY-MM-DD` 모두 인식)해 초기 선택값으로 사용한다.
- 날짜 선택: 첫 클릭이 시작일, 두 번째 클릭이 종료일(시작일보다 이르면 자동으로 서로 바꿈). 완결된 범위 상태에서 다시 클릭하면 새 시작일부터 다시 선택.
- **적용**을 눌러야 트리거의 `.d-start`/`.d-end` 텍스트가 갱신되고 팝오버가 닫힌다(`YYYY-MM-DD` 포맷으로 통일). **초기화**는 팝오버 내부 선택만 지우며 트리거 텍스트는 바꾸지 않는다.

## 사용 규칙 / 금지 사항

- **반드시 `<button type="button">`을 사용한다.** `<span>`만으로는 클릭해도 반응이 없고 키보드로 접근할 수 없으므로 금지한다.
- 시작일/종료일 텍스트는 반드시 `.d-start`/`.d-end`로 감싼다 — JS가 이 클래스로 값을 읽고 쓰므로, 감싸지 않으면 팝오버가 초기값을 파싱하지 못하거나 적용 시 텍스트를 갱신하지 못한다.
- 필터 카드 안에서는 `width:100%` + `justify-content:space-between`으로 늘려 사용한다([filter-card.md](filter-card.md) 4열 그리드 예시 참고).

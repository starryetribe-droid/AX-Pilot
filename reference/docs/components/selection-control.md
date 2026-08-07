# 체크박스 · 라디오 · 토글 (`.adm-check`, `.adm-radio`, `.adm-toggle`)

원본: [admin-common-design-system_v02.html](../../admin-common-design-system_v02.html) §3.6

> **v0.2 변경**: 원본 카탈로그는 `<span class="adm-check on">`처럼 상태를 클래스로만 표기한 정적 와이어프레임이다. 실제 페이지에서 쓰는 `templates/components/selection-control.html`은 진짜 `<input type="checkbox|radio">`를 `<label>`로 감싸고 `:checked`/`:disabled` 네이티브 상태로 구동하도록 교체했다 — 클릭·키보드·스크린 리더가 모두 실제로 동작하며 JS가 필요 없다.

## 개요

다중 선택은 항상 사각 체크박스, 배타 선택은 점 방식 라디오 — 각 한 가지 스타일만 쓴다. 테이블 행 선택도 체크박스. 폼 안의 배타 선택은 라디오 또는 초이스 그룹([choice-group.md](choice-group.md)). 토글 ON은 green-600.

## 클래스 계약

| 구분 | 클래스 | 설명 |
|---|---|---|
| 조합 래퍼 | `.adm-opt` | `<label>` — 실제 `<input>` + 커스텀 비주얼 + 텍스트 묶음(inline-flex, gap 8px) |
| State | `.adm-opt.disabled` | 라벨 텍스트 회색 처리(실제 비활성은 `input:disabled` 속성이 담당) |
| Variant | `.adm-opt.toggle` | 내부 input 히트 영역을 40×22로 확대(토글 전용) |
| 숨김 컨트롤 | `.adm-opt input[type=checkbox\|radio]` | 실제 폼 컨트롤(시각적으로 `opacity:0`, 기능은 100% 유지) |
| 비주얼 | `.adm-check` | 사각 체크박스 비주얼(20×20, 라운드 5px) — `input:checked + .adm-check`로 채움 |
| 비주얼 | `.adm-radio` | 원형 라디오 비주얼(20×20) — `input:checked + .adm-radio`로 표시 |
| 비주얼 | `.adm-toggle` | 토글 스위치 비주얼(40×22) — `input:checked + .adm-toggle`로 ON |

## 스펙

| 항목 | 값 |
|---|---|
| 체크박스/라디오 크기 | 20×20px, 테두리 1.5px `--g300` |
| 토글 크기 | 40×22px, 노브 18×18px |
| 토글 ON 색 | `--green-600` |
| 포커스 표시 | `input:focus-visible + 비주얼`에 2px `--blue-500` 아웃라인 (키보드 포커스만, 마우스 클릭 시 미표시) |

## HTML 스니펫

```html
<!-- 체크박스 -->
<label class="adm-opt"><input type="checkbox"><span class="adm-check" aria-hidden="true"></span>기본</label>
<label class="adm-opt"><input type="checkbox" checked><span class="adm-check" aria-hidden="true"></span>선택</label>
<label class="adm-opt disabled"><input type="checkbox" disabled><span class="adm-check" aria-hidden="true"></span>비활성</label>

<!-- 라디오 (같은 name으로 그룹화) -->
<label class="adm-opt"><input type="radio" name="g1"><span class="adm-radio" aria-hidden="true"></span>기본</label>
<label class="adm-opt"><input type="radio" name="g1" checked><span class="adm-radio" aria-hidden="true"></span>선택</label>
<label class="adm-opt disabled"><input type="radio" name="g1" disabled><span class="adm-radio" aria-hidden="true"></span>비활성</label>

<!-- 토글 -->
<label class="adm-opt toggle"><input type="checkbox"><span class="adm-toggle" aria-hidden="true"></span>OFF</label>
<label class="adm-opt toggle"><input type="checkbox" checked><span class="adm-toggle" aria-hidden="true"></span>ON</label>
<label class="adm-opt toggle disabled"><input type="checkbox" disabled><span class="adm-toggle" aria-hidden="true"></span>비활성</label>
```

텍스트 라벨 없이 아이콘/시각 요소만 필요한 경우(예: 테이블 행 선택)는 `<label>` 안의 텍스트 대신 `aria-label`을 실제 `<input>`에 지정한다:

```html
<label class="adm-opt"><input type="checkbox" aria-label="행 선택"><span class="adm-check" aria-hidden="true"></span></label>
```

## 사용 규칙 / 금지 사항

- **반드시 실제 `<input type="checkbox">`/`<input type="radio">`를 `<label>`로 감싼다.** `<span>`만으로 체크 여부를 클래스(`.on`)로 표기하는 방식은 클릭해도 아무 반응이 없고 키보드·스크린 리더로 조작할 수 없으므로 금지한다.
- 비주얼(`.adm-check`/`.adm-radio`/`.adm-toggle`)에는 `aria-hidden="true"`를 붙여 스크린 리더가 실제 input만 읽도록 한다.
- 다중 선택(테이블 행 선택 포함)에는 체크박스만 사용한다. 배타 선택에 체크박스를 쓰지 않는다.
- 배타 선택은 라디오 또는 초이스 그룹 중 하나로 통일하고 같은 폼에 혼용하지 않는다. 라디오는 같은 `name`으로 그룹화해야 배타 선택이 실제로 동작한다.
- 즉시 반영되는 On/Off 설정(알림 등)에는 토글을 사용하고, 폼 제출 전 임시 선택에는 체크박스/라디오를 사용한다.

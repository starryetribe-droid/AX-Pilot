# 초이스 그룹 (`.adm-choice-group`)

원본: [admin-common-design-system_v02.html](../../admin-common-design-system_v02.html) §3.2

## 개요

폼 안에서 배타 선택(라디오의 버튼형). 선택 항목은 1.5px 검정 테두리 + Bold.

> **v0.2 변경**: 원본 §3.2는 `.adm-choice`를 `<button class="selected">`로만 표기해, 클릭해도 선택 상태가 바뀌지 않고 스크린 리더도 이것이 배타 선택 그룹이라는 걸 알 수 없었다. 실제로는 배타 선택이므로 `<label class="adm-choice">`가 실제 `<input type="radio">`를 감싸도록 바꿨다 — 상태는 `:has(input:checked)`로 구동되어 별도 JS가 필요 없다.

## 클래스 계약

| 구분 | 클래스 | 설명 |
|---|---|---|
| 루트 | `.adm-choice-group` | 옵션들을 flex(gap 8px)로 묶는 래퍼 |
| 내부 | `label.adm-choice` | 개별 선택 옵션(flex:1, 균등 분할) — 실제 `<input type="radio">`를 감싸는 `<label>` |
| State | `.adm-choice:has(input:checked)` | 선택됨 (1.5px `--g900` 테두리 + Bold) |
| State | `.adm-choice:has(input:disabled)` | 비활성 |

## 스펙

| 항목 | 값 |
|---|---|
| 높이 | 44px |
| 테두리 | `1px solid var(--line-strong)`, 선택 시 `1.5px solid var(--g900)` |
| 라운드 | `--r-md` |

## HTML 스니펫

```html
<div class="adm-choice-group">
  <label class="adm-choice"><input type="radio" name="join-type" value="change" checked>기기변경</label>
  <label class="adm-choice"><input type="radio" name="join-type" value="new">신규가입</label>
  <label class="adm-choice"><input type="radio" name="join-type" value="transfer">번호이동</label>
</div>
```

## 사용 규칙 / 금지 사항

- 폼 안의 배타 선택은 라디오([selection-control.md](selection-control.md)) 또는 초이스 그룹 중 하나만 사용하며, 두 방식을 같은 폼에 혼용하지 않는다.
- 옵션 개수가 많아 버튼이 줄바꿈되는 경우(4개 이상)는 사용을 지양하고 셀렉트를 사용한다.
- 같은 그룹의 모든 `input[type="radio"]`는 반드시 `name`을 공유해야 하며, 한 페이지에 여러 초이스 그룹이 있다면 그룹별로 서로 다른 `name`을 지정한다.
- `:has()` 선택자를 사용하므로 이를 지원하지 않는 구형 브라우저(구형 Firefox 등)에서는 선택 상태가 시각적으로 표시되지 않는다 — 사내 어드민 지원 브라우저 기준에서는 문제 없음.

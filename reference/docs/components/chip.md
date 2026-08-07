# 칩 필터 (`.adm-chip`)

원본: [admin-common-design-system_v02.html](../../admin-common-design-system_v02.html) §3.3

## 개요

기간 프리셋 등 빠른 선택용 pill 버튼. 활성 칩은 g900 채움.

> **v0.2 변경**: 원본 §3.3 데모는 칩이 `<button class="active">`였지만 클릭해도 `.active`가 바뀌지 않았다(이벤트 자체가 없었음). `assets/js/adm-interactions.js`에 클릭 핸들러를 추가해, 같은 부모 안의 형제 `.adm-chip`끼리 배타적으로 `.active`가 전환되도록 했다.

## 클래스 계약

| 구분 | 클래스 | 설명 |
|---|---|---|
| 루트 | `.adm-chip` | 기본(흰 배경 + 테두리, pill 라운드) |
| State | `.adm-chip.active` | 선택됨 (g900 배경/흰 텍스트) |
| Variant | `.adm-chip.date` | 라운드를 `--r-md`로 낮춘 변형(날짜류 표기용) |

## 스펙

| 항목 | 값 |
|---|---|
| 높이 | 32px |
| 라운드 | `--r-full` (date variant는 `--r-md`) |
| 활성 배경 | `--g900` |

## HTML 스니펫

```html
<button type="button" class="adm-chip active">3일</button>
<button type="button" class="adm-chip">15일</button>
<button type="button" class="adm-chip">30일</button>
```

## 사용 규칙 / 금지 사항

- 기간 프리셋 칩은 항상 하나만 활성(`.active`) 상태를 가진다.
- **반드시 `<button type="button">`을 사용한다.** 클릭 시 `.active` 배타 전환은 `assets/js/adm-interactions.js`가 담당하며, 같은 부모 엘리먼트 아래에 있는 형제 `.adm-chip`을 기준으로 그룹을 판단한다 — 별도의 그룹 래퍼 클래스는 필요 없지만, 한 그룹의 칩들은 같은 부모 아래 나란히 배치해야 한다.
- 직접 기간 지정이 필요하면 칩 옆에 [date-picker.md](date-picker.md)를 함께 배치한다(데이트피커 버튼은 `.adm-chip`이 아니므로 칩 그룹의 배타 전환에 영향받지 않는다).

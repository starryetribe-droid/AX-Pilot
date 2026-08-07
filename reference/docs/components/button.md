# 버튼 (`.adm-btn`, `.adm-icon-btn`)

원본: [admin-common-design-system_v02.html](../../admin-common-design-system_v02.html) §3.1

## 개요

Primary는 무채색(g900) 단일. 위계는 Primary → Line → Ghost 순. Danger는 삭제 등 파괴 동작 전용.

## 클래스 계약

| 구분 | 클래스 | 설명 |
|---|---|---|
| 루트 | `.adm-btn` | Primary(기본, g900 배경/흰 텍스트) |
| Variant | `.adm-btn.line` | 흰 배경 + 테두리(2순위 액션) |
| Variant | `.adm-btn.ghost` | 배경 없음(3순위 액션) |
| Variant | `.adm-btn.danger` | red-500 배경(파괴적 동작 전용) |
| Size | `.adm-btn.sm` | 32px |
| Size | (기본) | 40px |
| Size | `.adm-btn.lg` | 48px |
| Size | `.adm-btn.full` | 52px, 폭 100% (모달 하단 전용) |
| State | `.disabled` / `:disabled` | 비활성 |
| 별도 루트 | `.adm-icon-btn` | 아이콘 전용 정사각 버튼(40px) |
| Size | `.adm-icon-btn.sm` | 32px |

## 스펙

| 항목 | 값 |
|---|---|
| 기본 높이 | 40px, 좌우 패딩 20px |
| 라운드 | `--r-md`(8px), sm은 `--r-sm`(6px) |
| Primary 배경 | `--g900` / hover `--g800` |
| Line 배경 | `#fff`, 테두리 `--line-strong` / hover 배경 `--g25` |
| Danger 배경 | `--red-500` / hover `--red-600` |
| Disabled | 배경 `--g100`, 텍스트 `--g400` (line disabled는 배경 `--g25`, 테두리 `--g200`) |
| 아이콘 버튼 | 40×40px, 테두리 `--line-strong`, sm은 32×32px |

## HTML 스니펫

```html
<button type="button" class="adm-btn">Primary</button>
<button type="button" class="adm-btn line">Line</button>
<button type="button" class="adm-btn ghost">Ghost</button>
<button type="button" class="adm-btn danger">Danger</button>
<button type="button" class="adm-btn disabled" disabled>Disabled</button>
<button type="button" class="adm-btn line disabled" disabled>Disabled</button>

<button type="button" class="adm-btn sm">Small 32</button>
<button type="button" class="adm-btn">Medium 40</button>
<button type="button" class="adm-btn lg">Large 48</button>

<button type="button" class="adm-icon-btn" aria-label="설정"><span class="adm-icon ic-setting sz-16"></span></button>
<button type="button" class="adm-icon-btn sm" aria-label="추가"><span class="adm-icon ic-plus sz-16"></span></button>
```

## 사용 규칙 / 금지 사항

- 한 화면(모달 포함)에서 Primary 버튼은 액션 그룹당 1개만 사용해 위계를 명확히 한다.
- Danger(빨강)는 삭제 등 파괴적 동작에만 사용하고 일반 액션에는 사용하지 않는다.
- 필터 카드의 "검색" 버튼은 아이콘 전용 돋보기 버튼 대신 Primary 텍스트 버튼으로 통일한다([filter-card.md](filter-card.md) 참고).
- **`.adm-icon-btn`은 반드시 `<button type="button">`이며 `aria-label`로 목적을 명시한다** — 아이콘만으로는 스크린 리더가 의미를 알 수 없고, `<span>`으로 두면 클릭·키보드 조작이 불가능하다.
- 폼 안에 배치되는 버튼은 실수로 폼을 제출하지 않도록 `type="button"`을 명시한다(제출 버튼만 `type="submit"`).
- 비활성 버튼은 `.disabled` 클래스만으로는 부족하다 — 실제 `disabled` 속성도 함께 지정해야 클릭이 진짜로 막힌다.

# 셀렉트 (`.adm-select`)

원본: [admin-common-design-system_v02.html](../../admin-common-design-system_v02.html) §3.5

> **v0.2 변경**: 원본 카탈로그는 시각적 와이어프레임이라 `<span>`으로만 구성돼 있었다. 실제 페이지에서 쓰는 `templates/components/select.html`은 네이티브 `<select>`로 교체했다 — 아래 스펙은 실사용 기준이다.

## 개요

테이블 툴바용 소형(32px)과 폼용 기본(40px). 정렬·개수 선택은 bare 셀렉트 사용 가능. 반드시 실제 `<select>` 엘리먼트를 사용해 드롭다운 열기·키보드 탐색·값 선택이 브라우저 네이티브로 동작하게 한다.

## 클래스 계약

| 구분 | 클래스 | 설명 |
|---|---|---|
| 루트 | `.adm-select` | `<select>`를 감싸는 래퍼(위치 기준점 + 장식 화살표) |
| 내부 | `.adm-select select` | 실제 `<select>` 엘리먼트 (appearance:none으로 네이티브 화살표 제거) |
| 내부 | `.adm-select::after` | 화살표(순수 CSS 장식, DOM 요소 아님) |
| Size | `.adm-select.sm` | 32px |
| Variant | `.adm-select.bare` | 테두리 없음, Bold, 툴바용(정렬/개수) |
| State | `.adm-select.disabled` + `select:disabled` | 비활성(래퍼 클래스와 실제 `disabled` 속성을 함께 지정) |

## 스펙

| 항목 | 값 |
|---|---|
| 기본 높이 | 40px, 최소폭 160px |
| 테두리 | `1px solid var(--line-strong)` |
| 라운드 | `--r-md` (sm은 `--r-sm`) |
| Disabled | 배경 `--g50`, 텍스트 `--g400` |
| placeholder 표현 | 첫 `<option>`을 `value="" disabled selected hidden`으로 두고 `<select required>` + CSS `select:required:invalid{color:var(--g400)}`로 회색 처리 |

## HTML 스니펫

```html
<span class="adm-select">
  <select required>
    <option value="" disabled selected hidden>선택해주세요</option>
    <option value="a">옵션 A</option>
  </select>
</span>

<span class="adm-select">
  <select>
    <option value="Y" selected>상담실 이관 Y</option>
    <option value="N">상담실 이관 N</option>
  </select>
</span>

<span class="adm-select disabled">
  <select disabled><option selected>선택 불가</option></select>
</span>

<span class="adm-select sm">
  <select><option selected>최신순</option><option>오래된순</option></select>
</span>

<span class="adm-select bare">
  <select><option selected>15개</option><option>30개</option></select>
</span>
```

## 사용 규칙 / 금지 사항

- **반드시 실제 `<select>` + `<option>`을 사용한다.** `<span>`·`<div>`로만 시각을 흉내 낸 가짜 셀렉트는 클릭해도 옵션 목록이 뜨지 않고 키보드/스크린리더로도 조작할 수 없으므로 금지한다.
- 비활성 상태는 래퍼에 `.disabled` 클래스를 붙이는 것만으로는 부족하다 — 실제 `<select disabled>` 속성도 함께 지정해야 클릭이 실제로 막힌다.
- 툴바의 정렬·개수 선택에는 `.bare` 변형만 사용한다(테두리 있는 기본형 금지).
- 필터 카드 안에서는 `width:100%`로 늘려 그리드 셀에 맞춘다([filter-card.md](filter-card.md) 참고).

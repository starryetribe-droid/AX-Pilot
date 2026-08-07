# 탭 (`.adm-tabs`, `.adm-tabs2`)

원본: [admin-common-design-system_v02.html](../../admin-common-design-system_v02.html) §3.8

> **v0.2 변경**: 원본의 `<span class="tab">`은 클릭해도 활성 상태가 바뀌지 않는 정적 표기였다. 실제 페이지에서는 `<button type="button" role="tab" aria-selected>`로 교체했고, `assets/js/adm-interactions.js`가 클릭 시 `.active`/`aria-selected`를 전환한다.
>
> **v0.2 추가**: 탭에 `aria-controls="패널ID"`를 지정하면(대상 `<div role="tabpanel" id="패널ID">` 필요) 클릭 시 해당 패널만 보이고 나머지는 `hidden` 처리된다. `aria-controls`가 없는 탭은 기존처럼 활성 표시만 토글한다.

## 개요

5개 이하 고정 비중 = Fixed. 5개 초과 = Fluid(가변). 대분류 안에 중분류가 필요하면 2뎁스.

## 클래스 계약

| 구분 | 클래스 | 설명 |
|---|---|---|
| 루트 | `.adm-tabs[role=tablist]` | 1뎁스 탭 컨테이너(하단 라인) |
| Variant | `.adm-tabs.fixed` | 균등 분할(탭 5개 이하) |
| Variant | `.adm-tabs.fluid` | 가변 폭, gap 28px(탭 5개 초과) |
| 내부 | `button.tab[role=tab]` | 개별 탭 — 실제 `<button>` |
| State | `.adm-tabs .tab.active` + `aria-selected="true"` | 활성 탭(Bold + 하단 2px 라인) |
| 루트(2뎁스) | `.adm-tabs2[role=tablist]` | 2뎁스 서브탭(회색 배경 바) |
| 내부 | `button.t[role=tab]` | 개별 서브탭 — 실제 `<button>` |
| State | `.adm-tabs2 .t.active` + `aria-selected="true"` | 활성 서브탭(Bold + 밑줄) |
| 연결 | `button[role=tab][aria-controls]` | 콘텐츠 패널을 가진 탭 — 값은 대상 패널의 `id` |
| 콘텐츠 | `.adm-tabpanel[role=tabpanel]` | 탭에 연결된 콘텐츠 패널, 비활성 시 `hidden` |

## 스펙

| 항목 | 값 |
|---|---|
| 1뎁스 | 패딩 `12px 4px`, 하단 2px 라인(활성만 `--g900`) |
| 2뎁스 | 패딩 `10px 0`, 배경 `--g25`, gap 24px, 13px |

## HTML 스니펫

```html
<!-- Fixed (콘텐츠 패널 연결) -->
<div class="adm-tabs fixed" role="tablist">
  <button type="button" class="tab active" role="tab" aria-selected="true" aria-controls="p1" id="t1">레이블</button>
  <button type="button" class="tab" role="tab" aria-selected="false" aria-controls="p2" id="t2">레이블</button>
</div>
<div class="adm-tabpanel" role="tabpanel" id="p1" aria-labelledby="t1">탭 1 콘텐츠</div>
<div class="adm-tabpanel" role="tabpanel" id="p2" aria-labelledby="t2" hidden>탭 2 콘텐츠</div>

<!-- Fluid -->
<div class="adm-tabs fluid" role="tablist">
  <button type="button" class="tab active" role="tab" aria-selected="true">레이블</button>
  <button type="button" class="tab" role="tab" aria-selected="false">레이블</button>
</div>

<!-- 2 Depth -->
<div class="adm-tabs fluid" role="tablist">...</div>
<div class="adm-tabs2" role="tablist">
  <button type="button" class="t active" role="tab" aria-selected="true">레이블</button>
  <button type="button" class="t" role="tab" aria-selected="false">레이블</button>
</div>
```

## 사용 규칙 / 금지 사항

- **탭은 반드시 `<button type="button" role="tab">`을 사용한다.** `<span>`만으로는 클릭해도 전환되지 않고 키보드로 접근할 수 없다.
- 탭 그룹 컨테이너에는 `role="tablist"`를, 각 탭에는 `aria-selected`를 지정한다. `assets/js/adm-interactions.js`가 클릭 시 같은 그룹 내 `.active`/`aria-selected`를 자동으로 갱신한다.
- 탭에 콘텐츠 패널이 있다면 `aria-controls`(탭) ↔ `id`(패널)로 연결한다 — 연결되면 `assets/js/adm-interactions.js`가 표시/숨김을 자동 처리한다. 연결하지 않으면 활성 표시만 토글되고 패널 전환은 일어나지 않는다.
- 패널 내부에 실제로 어떤 데이터를 렌더링할지는 페이지 데이터에 따라 달라지므로 페이지 레벨 로직이 담당한다(이 컴포넌트는 표시/숨김 전환만 담당).
- 탭 개수가 5개 이하면 `.fixed`, 초과하면 `.fluid`를 사용한다(임의 선택 금지).
- 2뎁스(`.adm-tabs2`)는 1뎁스 탭 바로 아래에만 배치한다.

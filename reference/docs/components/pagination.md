# 페이지네이션 (`.adm-paging`)

원본: [admin-common-design-system_v02.html](../../admin-common-design-system_v02.html) §3.11

## 개요

처음/이전/페이지/다음/끝 구성, 현재 페이지는 g900 채움. 10페이지 단위 이동은 처음·끝 아이콘 사용.

## 클래스 계약

| 구분 | 클래스 | 설명 |
|---|---|---|
| 루트 | `.adm-paging` | 페이지 번호 목록(중앙 정렬, gap 4px) |
| 내부 | `.pg` | 개별 페이지 버튼 |
| State | `.pg.cur` | 현재 페이지(g900 배경/흰 텍스트/Bold) |
| Variant | `.pg.nav` | 이전/다음/처음/끝 이동(`ic-arrow-double-left`/`ic-arrow-left`/`ic-arrow-right`/`ic-arrow-double-right` 아이콘) |
| State | `.pg.nav.disabled` | 이동 불가(첫/마지막 페이지) |

## 스펙

| 항목 | 값 |
|---|---|
| 버튼 크기 | 최소폭 32px, 높이 32px |
| 라운드 | `--r-sm` |
| 현재 페이지 | 배경 `--g900`, 텍스트 `#fff`, Bold |

## HTML 스니펫

```html
<div class="adm-paging">
  <button type="button" class="pg nav disabled" disabled aria-label="이전 10페이지"><span class="adm-icon ic-arrow-double-left sz-12"></span></button>
  <button type="button" class="pg nav disabled" disabled aria-label="이전 페이지"><span class="adm-icon ic-arrow-left sz-12"></span></button>
  <button type="button" class="pg cur" aria-current="page">1</button><button type="button" class="pg">2</button><button type="button" class="pg">3</button>
  <button type="button" class="pg nav" aria-label="다음 페이지"><span class="adm-icon ic-arrow-right sz-12"></span></button>
  <button type="button" class="pg nav" aria-label="다음 10페이지"><span class="adm-icon ic-arrow-double-right sz-12"></span></button>
</div>
```

## 사용 규칙 / 금지 사항

- 처음/끝 이동은 `ic-arrow-double-left`/`ic-arrow-double-right`(10페이지 단위), 이전/다음은 `ic-arrow-left`/`ic-arrow-right`(1페이지 단위)로 역할을 구분한다.
- 첫 페이지에서는 처음/이전 버튼을, 마지막 페이지에서는 다음/끝 버튼을 `.disabled` 클래스 **+ 실제 `disabled` 속성**으로 함께 처리한다(클래스만으로는 클릭이 막히지 않는다).
- 각 버튼은 `<button type="button">`이며, 아이콘만 있는 이동 버튼에는 `aria-label`로 목적을 명시하고 현재 페이지에는 `aria-current="page"`를 지정한다.
- 아이콘은 `assets/images/icons/`의 실제 파일을 `.adm-icon ic-<이름> sz-12` 클래스로 참조한다(§8 CONVENTIONS.md, [icons.md](../foundation/icons.md) 참고) — `«`/`‹`/`›`/`»` 같은 텍스트 글리프를 사용하지 않는다.
- 페이지 전환(실제 목록 갱신)은 페이지 레벨 로직이 담당한다 — `adm-interactions.js`는 페이지네이션에 관여하지 않는다.

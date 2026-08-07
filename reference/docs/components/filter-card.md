# 필터 카드 (`.adm-filter-card`)

원본: [admin-common-design-system_v02.html](../../admin-common-design-system_v02.html) §3.12

## 개요

필터 카드는 조건 개수로 변형을 선택한다 — **1~3개 = 인라인 변형**(검색 인풋 포함 한 줄, 라벨 좌측) / **4개 이상 = 그리드 변형**(4열, 라벨 상단). 키워드 검색 조합(기준 셀렉트 + 검색어 인풋)은 항상 맨 아래(인라인은 맨 뒤)에 배치한다.

## 클래스 계약

| 구분 | 클래스 | 설명 |
|---|---|---|
| 루트 | `.adm-filter-card` | 카드 컨테이너(테두리+라운드+패딩24) |
| Variant | `.adm-filter-card.inline` | 조건 1~3개: flex 한 줄, 라벨 좌측 |
| 내부(inline) | `.adm-filter-card.inline .f` | 개별 조건(라벨+컨트롤) |
| 내부(inline) | `.adm-filter-card.inline .acts` | 우측 끝 액션(margin-left:auto) |
| 그리드용 | `.adm-filter-grid` | 4열 그리드(조건 4개 이상) — `.adm-field` 항목을 담음 |
| 그리드용 | `.adm-filter-acts` | 그리드 하단 액션(우측 정렬, 상단 구분선) |

## 스펙

| 항목 | 값 |
|---|---|
| 카드 패딩 | 24px (inline은 `16px 20px`) |
| inline 필드 간격 | 28px |
| 그리드 컬럼 | `repeat(4, 1fr)`, gap `16px 20px` |
| 액션 버튼 | "↺ 초기화"(Line) + "검색"(Primary) |

## HTML 스니펫

인라인 변형(조건 1~3개):

전체 마크업은 [templates/components/filter-card.html](../../templates/components/filter-card.html) 참고. 셀렉트는 [select.md](select.md)대로 네이티브 `<select>`를, 기간 선택은 아래처럼 실제 `<button>`을 사용한다.

```html
<div class="adm-filter-card inline">
  <div class="f">
    <label for="f-role">권한</label>
    <span class="adm-select" style="min-width:160px;">
      <select id="f-role"><option selected>전체</option><option>관리자</option></select>
    </span>
  </div>
  <div class="f">
    <label for="f-field">검색 필드</label>
    <span class="adm-select" style="min-width:140px;">
      <select id="f-field" required><option value="" disabled selected hidden>선택</option><option value="name">이름</option></select>
    </span>
    <span class="adm-search" style="min-width:240px;"><input placeholder="검색어를 입력하세요"><span class="ic"><span class="adm-icon ic-search sz-15" aria-hidden="true"></span></span></span>
  </div>
  <div class="acts">
    <button type="reset" class="adm-btn line"><span class="adm-icon ic-refresh sz-14"></span> 초기화</button>
    <button type="submit" class="adm-btn"><span class="adm-icon ic-search-wh sz-14"></span> 검색</button>
  </div>
</div>
```

그리드 변형(조건 4개 이상)의 기간 필드는 실제 `<button>`(팝업 트리거)으로 구성한다:

```html
<div class="adm-field">
  <label for="f-period">기간</label>
  <button type="button" id="f-period" class="adm-date" style="width:100%;justify-content:space-between;" aria-haspopup="dialog" aria-expanded="false">
    <span class="lead"><span class="d-start">2026-06-29</span> <span class="tilde">~</span> <span class="d-end">2026-06-29</span></span>
    <span class="adm-icon ic-calendar sz-14" aria-hidden="true"></span>
  </button>
</div>
```

## 사용 규칙 / 금지 사항

- 조건 개수가 1~3개면 `.inline`, 4개 이상이면 그리드(`.adm-filter-grid`)를 사용한다 — 임의 선택 금지.
- 키워드 검색 조합(검색 기준 셀렉트 + 검색어 인풋)은 항상 맨 마지막 위치에 배치한다.
- "검색" 버튼은 항상 Primary 텍스트 버튼([button.md](button.md) 참고, 아이콘 전용 돋보기 버튼 금지).
- 조건 셀렉트는 반드시 네이티브 `<select>`, 기간 선택 트리거는 반드시 `<button type="button">`을 사용한다 — `<span>`만으로 구성하면 클릭해도 아무 동작이 없다.

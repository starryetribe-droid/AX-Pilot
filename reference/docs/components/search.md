# 서치 (`.adm-search`)

원본: [admin-common-design-system_v02.html](../../admin-common-design-system_v02.html) §3.5

## 개요

검색어 입력 전용 인풋. 검색 기준 셀렉트와 조합해 사용하는 경우가 많다.

## 클래스 계약

| 구분 | 클래스 | 설명 |
|---|---|---|
| 루트 | `.adm-search` | 검색 인풋 래퍼 |
| 내부 | `.adm-search input` | 실제 `<input>` (테두리 없음, 배경 투명) |
| 내부 | `.adm-search .ic` | 돋보기 아이콘(우측) |

## 스펙

| 항목 | 값 |
|---|---|
| 높이 | 40px, 최소폭 260px |
| 테두리 | `1px solid var(--line-strong)` |
| 라운드 | `--r-md` |

## HTML 스니펫

```html
<span class="adm-search">
  <input placeholder="검색어를 입력하세요">
  <span class="ic"><span class="adm-icon ic-search sz-15" aria-hidden="true"></span></span>
</span>
```

검색 기준 + 검색어 조합 — 기준 셀렉트는 반드시 [select.md](select.md)대로 네이티브 `<select>`를 사용한다(가짜 `<span>` 셀렉트 금지):

```html
<span class="adm-select" style="min-width:130px;">
  <select>
    <option selected>검색어 전체</option>
    <option>고객ID</option>
  </select>
</span>
<span class="adm-search" style="min-width:220px;">
  <input placeholder="검색어를 입력해 주세요">
  <span class="ic"><span class="adm-icon ic-search sz-15" aria-hidden="true"></span></span>
</span>
```

## 사용 규칙 / 금지 사항

- "검색 기준 + 검색어" 조합은 셀렉트(좌) + 서치(우)를 8px 간격으로 붙인다.
- 필터 카드 내 키워드 검색 조합은 항상 맨 아래(인라인 변형은 맨 뒤)에 배치한다([filter-card.md](filter-card.md) 참고).

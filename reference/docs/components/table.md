# 테이블 (`.adm-table`, `.adm-table-wrap`)

원본: [admin-common-design-system_v02.html](../../admin-common-design-system_v02.html) §3.9

## 개요

헤더 48px / 행 52px. 정렬 가능한 컬럼만 ↕ 아이콘. 행 상태: 호버(g25) · 선택(g50) · 비활성(텍스트 g400).

> **v0.2 변경**: 정렬 트리거는 실제 `<button type="button" class="th-sort">`이며, 헤더 라벨 텍스트와 아이콘(`.sort`)을 함께 감싼다 — 아이콘만 누르지 않아도 라벨 어디를 눌러도 정렬이 전환된다(클릭 영역 확대). 클릭하면 정렬없음 → 오름차순 → 내림차순 → 정렬없음 순으로 순환하며, 같은 `<thead>` 안 다른 컬럼은 정렬없음으로 리셋된다(배타적 단일 정렬). 동작은 `assets/js/adm-interactions.js`, 실제 행 재정렬(데이터 순서 변경)은 페이지 레벨 로직이 담당한다.
>
> **v0.2 변경**: `.adm-table-wrap`이 `overflow:hidden`이라 컬럼이 많거나 `nowrap` 텍스트가 길면 잘려서 아예 보이지 않았다. `overflow-x:auto`로 바꿔 가로 스크롤이 생기게 했다(세로는 라운드 코너 유지를 위해 `hidden` 그대로).
>
> **v0.2 추가**: 셀 하나의 텍스트만 유독 길 때(설명·메모 컬럼 등) 테이블 전체를 가로로 스크롤하지 않고 그 컬럼만 다루는 옵션 — `td.truncate`(말줄임 + `title` 툴팁) / `td.wrap`(줄바꿈, 행 높이 자동). 둘 다 기본 폭 220px이 내장돼 있어 클래스만 붙이면 동작한다.
>
> **v0.2 변경**: `td.truncate`의 `title`을 매번 셀 텍스트와 똑같이 손으로 채워 넣어야 했다 — 데이터가 나중에 채워지거나 바뀌는 실제 페이지에서는 이 중복 작성이 어긋나기 쉽다. `assets/js/adm-interactions.js`가 셀 텍스트를 `title`에 자동으로 동기화한다(초기 렌더 + `MutationObserver`로 이후 변경도 추적). `title`을 직접 쓰지 않는다.

## 클래스 계약

| 구분 | 클래스 | 설명 |
|---|---|---|
| 래퍼 | `.adm-table-wrap` | 카드형 테두리+라운드, 가로 스크롤(`overflow-x:auto`) |
| 루트 | `.adm-table` | 테이블 본체 |
| 셀 | `th`, `td` (기본) | 중앙 정렬 |
| 셀 | `th.l`, `td.l` | 좌측 정렬(성명·제목 등 텍스트 컬럼) |
| 셀 | `td.truncate` | 긴 텍스트를 한 줄로 유지 + 말줄임표. 기본 폭 220px(필요하면 `style="max-width:…"`로 덮어쓴다). `title`은 JS가 셀 텍스트로 자동 채운다 — 직접 쓰지 않는다 |
| 셀 | `td.wrap` | 긴 텍스트 줄바꿈 허용, 행 높이가 내용만큼 자동으로 늘어남. 기본 폭 220px(필요하면 `style="max-width:…"`로 덮어쓴다) |
| State(행) | `tr.hover` | 호버 표시(문서용, 실서비스는 `:hover`) |
| State(행) | `tr.selected` | 선택된 행(배경 `--g50`) |
| State(행) | `tr.disabled` | 비활성 행(텍스트 `--g400`) |
| 내부 | `button.th-sort` | 정렬 트리거 — 실제 `<button type="button">`, 라벨 텍스트+아이콘 전체가 클릭 영역, `aria-label`로 어떤 컬럼인지 명시 |
| 내부 | `.th-sort .sort` | 아이콘(삼각형) 래퍼 — 순수 장식, 클릭은 `.th-sort`가 담당 |
| 내부 | `.sort i.up` / `i.dn` | 오름/내림 삼각형 |
| State | `.sort i.on` | 현재 적용된 정렬 방향(진하게) |
| State(헤더) | `th[aria-sort]` | `"ascending"` / `"descending"` / `"none"` — 정렬 중인 컬럼의 `<th>`에 설정 |
| 셀 내부 | `.notice` | 공지 강조(red-500 + Bold) |
| 셀 내부 | `.reply` | 답글 들여쓰기 표시(↳) |

## 스펙

| 항목 | 값 |
|---|---|
| 헤더 높이 | 48px, 배경 `#fff`, 텍스트 `--g600`/600, 하단 `--line-strong` |
| 행 높이 | 52px, 하단 `--g100` |
| 폰트 | 13.5px |
| 컴팩트 변형 | 컬럼 12개 이상 와이드 테이블: 좌우 패딩 14→7px, 폰트 12px로 축소해 1440px 폭에 수납 |

## HTML 스니펫

```html
<div class="adm-table-wrap">
  <table class="adm-table">
    <thead><tr>
      <th style="width:56px;"><label class="adm-opt"><input type="checkbox" aria-label="전체 선택"><span class="adm-check" aria-hidden="true"></span></label></th>
      <th class="l">성명</th><th>전화번호</th>
      <th aria-sort="none"><button type="button" class="th-sort" aria-label="주소 정렬">주소 <span class="sort"><i class="up"></i><i class="dn"></i></span></button></th>
      <th>고객정보 검증</th>
      <th aria-sort="ascending"><button type="button" class="th-sort" aria-label="금액(원) 정렬">금액(원) <span class="sort"><i class="up on"></i><i class="dn"></i></span></button></th>
    </tr></thead>
    <tbody>
      <tr><td><label class="adm-opt"><input type="checkbox" aria-label="김케이 선택"><span class="adm-check" aria-hidden="true"></span></label></td><td class="l">김케이</td><td>010-1234-56**</td><td class="l">주소</td><td><span class="adm-tag">검증 완료</span></td></tr>
      <tr class="selected"><td><label class="adm-opt"><input type="checkbox" checked aria-label="박지후 선택"><span class="adm-check" aria-hidden="true"></span></label></td><td class="l">박지후</td><td>...</td><td class="l">...</td><td>...</td></tr>
      <tr class="disabled"><td><label class="adm-opt disabled"><input type="checkbox" disabled aria-label="고은비 선택"><span class="adm-check" aria-hidden="true"></span></label></td><td class="l">고은비</td><td>...</td><td class="l">...</td><td>...</td></tr>
    </tbody>
  </table>
</div>
```

행 선택 체크박스는 텍스트 라벨이 없으므로 실제 `<input>`에 `aria-label`을 지정한다([selection-control.md](selection-control.md) 참고). 링크 컬럼은 실제 `<a href="#" class="adm-link">Link</a>`를 사용한다([tag-badge.md](tag-badge.md) 참고).

게시판형 (공지·답글):

```html
<table class="adm-table">
  <thead><tr><th>No</th><th>첨부</th><th class="l">제목</th><th>작성자</th><th>작성일</th></tr></thead>
  <tbody>
    <tr><td>1</td><td>📎</td><td class="l"><span class="notice">★ 공지 제목</span></td><td>작성자</td><td>2026.1.1.</td></tr>
    <tr><td>3</td><td></td><td class="l"><span class="reply">↳</span> 답글 제목 <span class="adm-badge-cnt">3</span></td><td>작성자</td><td>2026.1.1.</td></tr>
  </tbody>
</table>
```

긴 텍스트 컬럼 (설명·메모 등) — 기본 220px 폭으로 클래스만 붙이면 동작한다:

```html
<!-- 한 줄 유지 + 말줄임표. title은 쓰지 않는다 — JS가 셀 텍스트로 자동 채운다 -->
<td class="l truncate">전체 텍스트...</td>

<!-- 줄바꿈 허용, 행 높이 자동 확장 -->
<td class="l wrap">전체 텍스트...</td>

<!-- 컬럼마다 다른 폭이 필요하면 덮어쓴다 -->
<td class="l truncate" style="max-width:160px;">전체 텍스트...</td>
```

## 사용 규칙 / 금지 사항

- 정렬 가능한 컬럼에만 `.th-sort` 버튼을 붙인다(전체 컬럼에 일괄 적용 금지).
- 정렬 트리거는 반드시 `<button type="button" class="th-sort">`로 라벨 텍스트와 아이콘(`.sort`)을 함께 감싼다 — 아이콘만 `<button>`으로 감싸고 라벨은 바깥에 두면 클릭 영역이 좁아지고, `<span>`만으로는 클릭해도 반응이 없고 키보드로도 접근할 수 없으므로 금지한다.
- 행 선택 체크박스는 항상 첫 번째 컬럼, 폭 56px 고정.
- 텍스트 컬럼(성명/제목/주소)은 `.l`로 좌측 정렬, 수치·상태 컬럼은 기본(중앙 정렬) 유지.
- 컬럼 12개 이상인 와이드 테이블은 compact 변형(패딩 7px, 폰트 12px)을 적용해 1440px 폭 안에 수납한다.
- 테이블 자체가 래퍼보다 넓어지는 것은 `.adm-table-wrap`의 가로 스크롤로 해결한다 — 임의로 `overflow:hidden`을 다시 걸어 잘라내지 않는다.
- 특정 컬럼 하나만 텍스트가 유독 길면(설명·메모 등) 테이블 전체를 스크롤하게 두지 말고 그 `td`에 `.truncate` 또는 `.wrap`을 적용한다. 한 줄 목록 유지가 중요하면 `.truncate`, 목록에서 바로 전체 내용을 봐야 하면 `.wrap`을 쓴다. 둘 다 기본 폭 220px이 내장돼 있으므로 클래스만 붙이면 되고, 컬럼마다 다른 폭이 필요할 때만 `style="max-width:…"`로 덮어쓴다.
- `.truncate`에 `title`을 직접 쓰지 않는다 — `assets/js/adm-interactions.js`가 셀 텍스트를 그대로 `title`에 동기화한다(초기 렌더 + 이후 데이터 변경 모두 `MutationObserver`로 추적). 데이터가 나중에 채워지거나 바뀌는 실제 페이지에서 텍스트와 `title`을 매번 손으로 맞추는 것은 어긋나기 쉬우므로 금지한다.

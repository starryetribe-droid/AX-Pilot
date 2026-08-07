# 테이블 툴바 (`.adm-toolbar`)

원본: [admin-common-design-system_v02.html](../../admin-common-design-system_v02.html) §3.12

## 개요

테이블 위에 위치하는 좌우 양끝 정렬 바. 좌측 «총 N건 + 정렬·개수», 우측 «검색·설정·주요 액션».

## 클래스 계약

| 구분 | 클래스 | 설명 |
|---|---|---|
| 루트 | `.adm-toolbar` | 좌/우 양끝 정렬(gap 16px) |
| 내부 | `.adm-toolbar .left` | 총 건수 + 정렬/개수 셀렉트 |
| 내부 | `.adm-toolbar .right` | 검색 + 아이콘버튼 + 주요 액션 버튼 |
| 내부 | `.adm-toolbar .total` | 총 건수 텍스트 |
| 내부 | `.adm-toolbar .total b` | 건수 숫자(Bold) |

## 스펙

| 항목 | 값 |
|---|---|
| 총 건수 | 14px, 숫자만 Bold |
| left/right 내부 gap | 10px |

## HTML 스니펫

```html
<div class="adm-toolbar">
  <div class="left">
    <span class="total"><b>총 32건</b></span>
    <span class="adm-select bare"><select><option selected>최신순</option><option>오래된순</option></select></span>
    <span class="adm-select bare"><select><option selected>15개</option><option>30개</option></select></span>
  </div>
  <div class="right">
    <span class="adm-search" style="min-width:240px;"><input placeholder="검색어를 입력하세요"><span class="ic"><span class="adm-icon ic-search sz-15" aria-hidden="true"></span></span></span>
    <button type="button" class="adm-icon-btn" aria-label="필터 설정"><span class="adm-icon ic-filter sz-16"></span></button>
    <button type="button" class="adm-btn"><span class="adm-icon ic-edit-wh sz-14"></span> 게시글 작성</button>
  </div>
</div>
```

## 사용 규칙 / 금지 사항

- 정렬·표시 개수 셀렉트는 항상 `.bare` 변형의 네이티브 `<select>`를 사용한다([select.md](select.md) 참고) — 텍스트만 있는 `<span>` 금지.
- 아이콘 전용 버튼(`.adm-icon-btn`)은 반드시 `<button type="button">`이며 `aria-label`로 목적을 명시한다(아이콘만으로는 스크린 리더가 의미를 알 수 없다).
- 페이지 단위 주요 액션(글쓰기 등)은 우측 끝에 배치한다.

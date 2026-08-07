# 페이지 헤더 (`.adm-pagebar`, `.adm-crumb`)

원본: [admin-common-design-system_v02.html](../../admin-common-design-system_v02.html) §2.3

## 개요

브레드크럼(상단) + 페이지 타이틀(하단). 페이지 단위 주요 액션 버튼은 우측 끝.

## 클래스 계약

| 구분 | 클래스 | 설명 |
|---|---|---|
| 루트 | `.adm-pagebar` | 좌(타이틀+브레드크럼) / 우(액션) 양끝 정렬 |
| 내부 | `.adm-pagebar .left` | 타이틀+브레드크럼 래퍼 |
| 내부 | `.adm-pagebar .ttl` | 페이지 타이틀(Title 1, 24/Bold) |
| 내부 | `.adm-pagebar .acts` | 액션 버튼 그룹(우측 끝) |
| 루트 | `.adm-crumb` | 브레드크럼 |
| 내부 | `.adm-crumb .sep` | 구분자(›) |
| 내부 | `.adm-crumb .cur` | 현재 페이지 표기 |

## 스펙

| 항목 | 값 |
|---|---|
| 타이틀 | 24px / Bold / `-0.01em` |
| 브레드크럼 | 12.5px, `var(--g500)`, 현재 항목은 `var(--g700)` |
| acts 버튼 간격 | 8px |

## HTML 스니펫

```html
<div class="adm-pagebar">
  <div class="left">
    <span class="adm-crumb">Home <span class="sep">›</span> 회원 관리 <span class="sep">›</span> <span class="cur">고객 관리</span></span>
    <span class="ttl">고객 관리</span>
  </div>
  <div class="acts">
    <button class="adm-btn line">선택 삭제</button>
    <button class="adm-btn">+ 고객 추가</button>
  </div>
</div>
```

## 사용 규칙 / 금지 사항

- 페이지당 `.adm-pagebar`는 1개, 타이틀은 브레드크럼 마지막 항목과 동일 텍스트를 사용한다.
- 페이지 주요 액션(생성/다운로드 등)은 `.acts`에만 배치하며 위치를 임의 변경하지 않는다.

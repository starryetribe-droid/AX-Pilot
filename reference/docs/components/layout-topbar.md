# 헤더 / Top Bar (`.adm-topbar`)

원본: [admin-common-design-system_v02.html](../../admin-common-design-system_v02.html) §2.1

## 개요

좌: 계정(아바타+이름) + 환경 뱃지 / 우: 알림·검색 아이콘 버튼 + 로그아웃.

> **v0.2 변경**: 서비스 로고 영역(`.adm-logo`: 마크+서비스명)은 [LNB `.brand`](layout-gnb.md)로 옮겼다 — 로고가 헤더와 LNB 양쪽에 중복 노출되는 것을 막기 위해서다. topbar는 계정 컨텍스트와 전역 유틸(알림/검색/로그아웃)만 담당한다.

## 클래스 계약

| 구분 | 클래스 | 설명 |
|---|---|---|
| 루트 | `.adm-topbar` | 헤더 바 (H52, LNB 우측 전체 폭) |
| 내부 | `.adm-topbar .env` | 환경 뱃지(STG/PROD 등) |
| 내부 | `.adm-utils` | 좌/우 양쪽에서 재사용하는 아이템 그룹 래퍼(계정 영역, 유틸 영역 각각 1개씩) |
| 내부 | `.adm-utils .u` | 개별 유틸 아이템 — 로그아웃처럼 클릭이 필요하면 실제 `<button type="button" class="u">` |
| 내부 | `.adm-utils .divider` | 구분선(세로) |

좌측은 `.adm-user`+`.adm-avatar.sm`([tag-badge.md](tag-badge.md))로 계정명을 구성하고, 우측은 `.adm-icon-btn.ghost.sm`([button.md](button.md))로 알림/검색을, `.u`로 로그아웃을 구성한다.

## 스펙

| 항목 | 값 |
|---|---|
| 높이 | 52px, LNB 우측 전체 폭(2300px) |
| 배경 | `#fff` |
| 하단 라인 | `1px solid var(--line)` |
| 좌우 패딩 | 32px |

## HTML 스니펫

```html
<div class="adm-topbar">
  <div class="adm-utils">
    <span class="adm-user"><span class="adm-avatar sm">홍</span>홍길동님</span>
    <span class="env">STG</span>
  </div>
  <div class="adm-utils">
    <button type="button" class="adm-icon-btn ghost sm" aria-label="알림"><span class="adm-icon ic-alarm sz-16"></span></button>
    <button type="button" class="adm-icon-btn ghost sm" aria-label="검색"><span class="adm-icon ic-search sz-16"></span></button>
    <span class="divider"></span>
    <button type="button" class="u"><span class="adm-icon ic-logout sz-16"></span>로그아웃</button>
  </div>
</div>
```

## 사용 규칙 / 금지 사항

- 로고/서비스명은 이 컴포넌트에 두지 않는다 — LNB `.brand`가 담당한다([layout-gnb.md](layout-gnb.md)).
- 환경 뱃지(`.env`)는 스테이징/운영 구분 등 배포 환경 표기 전용.
- 알림·검색·로그아웃은 모두 실제 `<button type="button">`를 사용한다 — `<span>`/`<div>`만으로는 클릭도, 키보드 접근도 안 된다(§7 참고). 알림/검색 버튼을 눌렀을 때 실제로 여는 패널·페이지는 이 문서의 범위가 아니라 페이지별 구현 대상이다.
- 프로젝트별로 계정명·아바타 이니셜·환경 뱃지 텍스트만 교체하고 구조(레이아웃/높이)는 변경하지 않는다.

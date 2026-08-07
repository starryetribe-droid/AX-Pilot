# 아이콘 (Icons)

`assets/images/icons/`에 있는 SVG를 아이콘 소스로 삼는다. 원래는 아이콘 팩(boxicons, material-symbols, mdi, weui 등)에서 받아온 그대로라 파일명이 팩마다 제각각(`material-symbols_download.svg`, `mdi_pencil-outline.svg` …)이었는데, `adm-` 컴포넌트 네이밍(§1 CONVENTIONS.md)과 마찬가지로 **`ic-` + kebab-case 의미 이름**으로 통일했다. 파일명이 곧 공통 이름이다.

## 사용 규칙

- 아이콘이 필요한 모든 곳(버튼, 검색창, 날짜, GNB, 상태 뱃지 등)은 **반드시 `assets/images/icons/`의 `ic-*.svg`만** 사용한다. 페이지마다 새 아이콘을 임의로 그리거나 다른 아이콘 팩에서 받아와 쓰지 않는다.
- 표에 맞는 아이콘이 없으면 먼저 `assets/images/icons/`에 `ic-<의미>.svg` 이름으로 SVG를 추가하고 이 문서 표에 등록한 뒤 사용한다.
- 페이지 마크업에 SVG의 `path` 데이터를 인라인으로 복사·재작성하지 않는다 — 반드시 `assets/images/icons/`의 실제 파일을 참조한다.
- **인라인 `style` 금지.** 아이콘은 항상 `.adm-icon` + `.ic-<이름>`(경로) + `.sz-<크기>`(크기) 클래스 조합만으로 마크업한다:
  ```html
  <span class="adm-icon ic-alarm sz-16"></span>
  ```
  아래 표의 아이콘은 **전부** [adm-icon.css](../../assets/css/components/adm-icon.css)에 `.ic-<이름>` 클래스로 등록돼 있으므로 클래스만 붙이면 바로 쓸 수 있다. 크기는 `sz-12` `sz-13` `sz-14` `sz-15` `sz-16` `sz-18`이 준비돼 있다. 표에 없는 **새 아이콘**이나 준비되지 않은 **새 크기**가 필요할 때만 마크업에 인라인 style을 추가하지 말고 먼저 이 CSS 파일에 규칙을 추가한 뒤 클래스로 사용한다.
- 장식용 아이콘에는 `aria-hidden="true"`를, 아이콘만 있는 버튼에는 `aria-label`을 붙인다.

## 어두운 배경 위의 아이콘 — 흰색 변형(`.ic-*-wh`)

`background-image` 방식은 SVG 파일에 박힌 `fill` 색을 그대로 그린다(§v0.3 변경 참고). 기본 아이콘은 **검정(`fill="black"`)** 이므로 어두운 배경 위에 올리면 보이지 않는다. 어두운 배경에서는 흰색 SVG를 가리키는 `-wh` 변형을 쓴다.

| 배경 | 사용 클래스 | 예 |
|---|---|---|
| 밝은 배경 (페이지, `.adm-btn.line`, `.adm-icon-btn.ghost`, 인풋 내부) | 기본 `.ic-<이름>` | `<span class="adm-icon ic-search sz-15"></span>` |
| 어두운 배경 (`.adm-btn` Primary, 다크 서페이스) | `.ic-<이름>-wh` | `<span class="adm-icon ic-search-wh sz-14"></span>` |

현재 준비된 흰색 변형은 `ic-search-wh.svg`, `ic-edit-wh.svg`, `ic-plus-wh.svg`, `ic-delete-wh.svg` 네 개다(각각 등록·검색·수정·삭제처럼 Primary/Danger 버튼에 자주 얹히는 액션). 다른 아이콘의 흰색 변형이 필요하면 `assets/images/icons/`에 `ic-<이름>-wh.svg`를 추가하고 `adm-icon.css`에 `.ic-<이름>-wh` 규칙을 등록한 뒤 사용한다.

> 기본 클래스(`.ic-search`)가 흰색 파일을 가리키게 매핑해 두면 밝은 배경에서 아이콘이 통째로 사라진다 — 실제로 v0.3 초기에 `.ic-search`/`.ic-edit`가 `-wh` 파일을 가리키고 있어 헤더·검색 인풋의 아이콘이 보이지 않는 문제가 있었다. **기본 클래스는 항상 검정 파일에 매핑한다.**

> **v0.3 변경 — mask-image 폐기**: v0.2까지는 `.adm-icon`에 `background-color:currentColor` + `mask-image`를 걸어 참조해 hover·다크 변형에도 색이 자동으로 따라가게 했다. 그런데 `mask-image`로 "다른 파일의 SVG를 마스크로 합성"하는 연산은 브라우저가 `file://` 프로토콜에서 cross-origin 픽셀 합성으로 보고 보안상 차단한다 — Live Server 같은 로컬 서버(`http://`)로 열면 정상 동작하지만, HTML 파일을 폴더에서 직접 더블클릭해 열면(`file://`) 아이콘이 전부 사라지는 문제가 있었다. `background-image`로 교체했다 — 이미지를 그대로 그리는 연산이라 `<img>`와 동일하게 `file://`에서도 제한 없이 동작한다. 다만 원본 SVG의 `fill`이 `black`으로 고정돼 있어 이제는 `currentColor` 상속(색 자동 전환)을 지원하지 않는다 — 옅게 표시해야 하는 자리(검색 인풋, 데이트피커 등)는 해당 컴포넌트 CSS에서 `opacity`로 톤을 낮춘다(예: [adm-search.css](../../assets/css/components/adm-search.css)의 `.adm-search .ic .adm-icon`).

## 공통 액션

| 미리보기 | 파일 | 용도 |
|---|---|---|
| ![](../../assets/images/icons/ic-plus.svg) | `ic-plus.svg` | 추가 |
| ![](../../assets/images/icons/ic-copy.svg) | `ic-copy.svg` | 복사 |
| ![](../../assets/images/icons/ic-edit.svg) | `ic-edit.svg` | 수정 |
| ![](../../assets/images/icons/ic-delete.svg) | `ic-delete.svg` | 삭제 |
| ![](../../assets/images/icons/ic-save.svg) | `ic-save.svg` | 저장 |
| ![](../../assets/images/icons/ic-download.svg) | `ic-download.svg` | 다운로드 |
| ![](../../assets/images/icons/ic-print.svg) | `ic-print.svg` | 인쇄 |
| ![](../../assets/images/icons/ic-refresh.svg) | `ic-refresh.svg` | 새로고침 |
| ![](../../assets/images/icons/ic-search.svg) | `ic-search.svg` | 검색 |
| ![](../../assets/images/icons/ic-filter.svg) | `ic-filter.svg` | 필터(깔때기형) |
| ![](../../assets/images/icons/ic-sliders.svg) | `ic-sliders.svg` | 조정/설정 슬라이더(`ic-filter`와 다른 형태) |
| ![](../../assets/images/icons/ic-setting.svg) | `ic-setting.svg` | 설정(톱니바퀴) |
| ![](../../assets/images/icons/ic-more.svg) | `ic-more.svg` | 더보기(케밥) |
| ![](../../assets/images/icons/ic-logout.svg) | `ic-logout.svg` | 로그아웃 |
| ![](../../assets/images/icons/ic-lock.svg) | `ic-lock.svg` | 잠금 |

## 내비게이션 / 화살표

| 미리보기 | 파일 | 용도 |
|---|---|---|
| ![](../../assets/images/icons/ic-menu.svg) | `ic-menu.svg` | 메뉴(햄버거) |
| ![](../../assets/images/icons/ic-home.svg) | `ic-home.svg` | 홈 |
| ![](../../assets/images/icons/ic-dashboard.svg) | `ic-dashboard.svg` | 대시보드 |
| ![](../../assets/images/icons/ic-arrow-right.svg) | `ic-arrow-right.svg` | 화살표 오른쪽 |
| ![](../../assets/images/icons/ic-arrow-left.svg) | `ic-arrow-left.svg` | 화살표 왼쪽 |
| ![](../../assets/images/icons/ic-arrow-up.svg) | `ic-arrow-up.svg` | 화살표 위 |
| ![](../../assets/images/icons/ic-arrow-down.svg) | `ic-arrow-down.svg` | 화살표 아래 |
| ![](../../assets/images/icons/ic-arrow-double-left.svg) | `ic-arrow-double-left.svg` | 처음으로(맨 앞 페이지 등) |
| ![](../../assets/images/icons/ic-arrow-double-right.svg) | `ic-arrow-double-right.svg` | 마지막으로(맨 뒤 페이지 등) |

## 상태 / 피드백

| 미리보기 | 파일 | 용도 |
|---|---|---|
| ![](../../assets/images/icons/ic-check-circle.svg) | `ic-check-circle.svg` | 성공/완료 |
| ![](../../assets/images/icons/ic-x-circle.svg) | `ic-x-circle.svg` | 오류/닫기(원형) |
| ![](../../assets/images/icons/ic-alert.svg) | `ic-alert.svg` | 경고 |
| ![](../../assets/images/icons/ic-alarm.svg) | `ic-alarm.svg` | 알림(벨) |
| ![](../../assets/images/icons/ic-info.svg) | `ic-info.svg` | 안내/정보 |

## 콘텐츠 / 오브젝트

| 미리보기 | 파일 | 용도 |
|---|---|---|
| ![](../../assets/images/icons/ic-folder.svg) | `ic-folder.svg` | 폴더 |
| ![](../../assets/images/icons/ic-file.svg) | `ic-file.svg` | 파일/문서 |
| ![](../../assets/images/icons/ic-image.svg) | `ic-image.svg` | 이미지 |
| ![](../../assets/images/icons/ic-calendar.svg) | `ic-calendar.svg` | 달력 |
| ![](../../assets/images/icons/ic-clock.svg) | `ic-clock.svg` | 시간 |
| ![](../../assets/images/icons/ic-tag.svg) | `ic-tag.svg` | 태그 |
| ![](../../assets/images/icons/ic-package.svg) | `ic-package.svg` | 패키지/상품 |
| ![](../../assets/images/icons/ic-star.svg) | `ic-star.svg` | 즐겨찾기/평점 |
| ![](../../assets/images/icons/ic-card.svg) | `ic-card.svg` | 카드(결제) |
| ![](../../assets/images/icons/ic-mail.svg) | `ic-mail.svg` | 메일 |
| ![](../../assets/images/icons/ic-link.svg) | `ic-link.svg` | 링크 |
| ![](../../assets/images/icons/ic-phone.svg) | `ic-phone.svg` | 전화 |
| ![](../../assets/images/icons/ic-security.svg) | `ic-security.svg` | 보안 |
| ![](../../assets/images/icons/ic-chat.svg) | `ic-chat.svg` | 채팅/문의 |
| ![](../../assets/images/icons/ic-cart.svg) | `ic-cart.svg` | 장바구니 |
| ![](../../assets/images/icons/ic-list.svg) | `ic-list.svg` | 목록 |
| ![](../../assets/images/icons/ic-eye.svg) | `ic-eye.svg` | 보기/조회 |
| ![](../../assets/images/icons/ic-sound.svg) | `ic-sound.svg` | 소리/음성듣기 |

## 사용자

| 미리보기 | 파일 | 용도 |
|---|---|---|
| ![](../../assets/images/icons/ic-user.svg) | `ic-user.svg` | 사용자 1인(아웃라인) |
| ![](../../assets/images/icons/ic-profile.svg) | `ic-profile.svg` | 프로필/내 계정(원형) |
| ![](../../assets/images/icons/ic-people.svg) | `ic-people.svg` | 회원/그룹(2인) |

# LNB (`.adm-gnb`)

원본: [admin-common-design-system_v02.html](../../admin-common-design-system_v02.html) §2.2

## 개요

1뎁스(그룹) + 2뎁스(메뉴) 구조. 활성 메뉴는 좌측 3px 바 + Bold + g50 배경.

> **v0.2 변경**: 원본의 `.grp`는 `cursor:default`인 정적 `<div>`였다. 실제 페이지에서는 `<button type="button" aria-expanded>`로 교체해 펼침/접힘이 실제로 동작하게 했다(`assets/js/adm-interactions.js`가 처리).
>
> **캐럿 아이콘**: `.cv`는 처음엔 `▲`/`▼` 유니코드 글자를 그대로 넣어뒀는데, JS는 `aria-expanded`/`.open`만 토글하고 글자 내용은 갱신하지 않아 실제로 펼쳐도 화살표 방향이 안 바뀌는 버그가 있었다. 지금은 `.cv`를 빈 `<span>`으로 두고 CSS 셰브런(모서리 테두리 2개 + `rotate`)으로 그려, `.grp.open` 클래스 하나로 방향이 함께 바뀐다 — 텍스트를 갱신할 JS가 필요 없다.

## 클래스 계약

| 구분 | 클래스 | 설명 |
|---|---|---|
| 루트 | `.adm-gnb` | LNB 컨테이너 (W260) |
| Variant | `.adm-gnb.dark` | 다크 서페이스 변형 — 구조/동작은 동일, 색상과 `.cv` 모양만 다르다 |
| 내부 | `.brand` | 서비스 로고/서비스명 헤더 블록 (프로젝트별로 텍스트만 교체) |
| 내부 | `.brand .tit` | 서비스명(굵게) |
| 내부 | `.brand .desc` | 부제/설명 텍스트 |
| 내부 | `button.grp` | 1뎁스 그룹 토글 — 실제 `<button aria-expanded aria-controls="{sub의 id}">` |
| State | `.grp.open` + `[aria-expanded="true"]` | 펼쳐진 그룹 (텍스트 색 강조, JS가 함께 토글) |
| 내부 | `.grp .cv` | 펼침/접힘 캐럿 — 기본은 CSS로 그린 셰브런, `.dark`는 삼각형(▼/▲). `.grp.open`이면 회전만 바뀜(빈 `<span>`, 텍스트 없음) |
| 내부 | `.sub` | 2뎁스 메뉴 래퍼 — `id` 보유, 접힘 시 `hidden` 속성 |
| 내부 | `.sub a` | 2뎁스 메뉴 링크(실제 `href`) |
| State | `.sub a.active` | 현재 페이지 메뉴 — 기본은 좌측 보더, `.dark`는 인셋 하이라이트 배경 |

## 스펙

| 항목 | 값 |
|---|---|
| 폭 | 260px, 헤더 아래 전체 높이 |
| 배경 | `#fff` |
| 우측 라인 | `1px solid var(--line)` |
| 1뎁스 패딩 | `13px 24px` |
| 2뎁스 패딩 | `10px 24px 10px 40px` |
| 활성 표시(기본) | 좌측 3px `border-left: var(--g900)` + Bold + `background: var(--g50)` (패딩 left는 37px로 3px 보정) |
| 활성 표시(`.dark`) | 좌우 12px 인셋 + `border-radius: var(--r-sm)` + `background: var(--dark-active-bg)` + Bold (패딩 left/right를 12px씩 줄여 텍스트 시작 위치는 기본과 동일하게 유지) |
| 다크 배경 | `var(--dark-bg)`, 브랜드 헤더는 `var(--dark-bg-strong)` |

## HTML 스니펫

```html
<div class="adm-gnb">
  <div class="brand">
    <strong class="tit">서비스명</strong>
    <span class="desc">어드민 디자인 시스템</span>
  </div>
  <button type="button" class="grp open" aria-expanded="true" aria-controls="gnb-chatbot">챗봇 관리 <span class="cv" aria-hidden="true"></span></button>
  <div class="sub" id="gnb-chatbot">
    <a href="#" class="active">챗봇 대화 내역</a>
    <a href="#">인텐트 관리</a>
    <a href="#">답변 콘텐츠 관리</a>
  </div>
  <button type="button" class="grp" aria-expanded="false" aria-controls="gnb-member">회원 관리 <span class="cv" aria-hidden="true"></span></button>
  <div class="sub" id="gnb-member" hidden><a href="#">회원 목록</a></div>
</div>

<!-- Dark 변형: .adm-gnb에 .dark만 추가하면 나머지 마크업/동작은 동일 -->
<div class="adm-gnb dark">
  <div class="brand">
    <strong class="tit">LG Partner Club</strong>
    <span class="desc">어드민 디자인 시스템</span>
  </div>
  <button type="button" class="grp open" aria-expanded="true" aria-controls="gnb-chatbot-dark">챗봇 관리 <span class="cv" aria-hidden="true"></span></button>
  <div class="sub" id="gnb-chatbot-dark">
    <a href="#" class="active">챗봇 대화 내역</a>
    <a href="#">인텐트 관리</a>
    <a href="#">답변 콘텐츠 관리</a>
  </div>
</div>
```

## 사용 규칙 / 금지 사항

- **그룹 헤더는 반드시 `<button type="button" aria-expanded>`를 사용한다** — `<div>`/`<span>`만으로는 클릭해도 펼쳐지지 않고 키보드로 접근할 수 없다.
- 각 `.grp`는 자신이 제어하는 `.sub`의 `id`를 `aria-controls`로 가리킨다.
- 활성 메뉴는 반드시 `.sub a.active` 한 개만 존재해야 한다.
- 그룹은 펼침(`aria-expanded="true"` + `.open`) 시 `.sub`의 `hidden` 속성이 제거되고, 닫히면(`aria-expanded="false"`) `.sub`에 `hidden`이 다시 붙는다.
- `.brand`는 프로젝트별로 서비스명/부제 텍스트만 교체한다(이전에는 `adm-topbar`에 있던 로고 영역과 같은 취지 — v0.2부터 LNB로 이동) — 구조나 폰트(Pretendard 단일 서체)는 바꾸지 않는다.
- `.dark`는 `.adm-gnb` 자체의 색 변형이다. 라이트 기본값과 공존하므로, 페이지 전체를 다크로 바꾸는 용도가 아니라 LNB 단위로만 선택한다.
- `.dark`의 2뎁스 메뉴 앞 짧은 대시 마커는 `.sub a::before`로 그린 순수 장식(빈 `content` + 배경선)이다 — 실제 링크 텍스트에 `"- "`를 넣지 않는다(스크린 리더가 그대로 읽는 것을 방지).

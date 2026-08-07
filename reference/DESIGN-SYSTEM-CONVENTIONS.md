# 네이밍 규칙 (Conventions)

원본 [admin-common-design-system_v02.html](admin-common-design-system_v02.html)이 이미 따르고 있는 관례를 성문화한 것이다. 기존 클래스명을 바꾸지 않으며, 새 컴포넌트를 추가할 때 이 규칙을 그대로 따른다.

> **v0.2 참고**: 원본 카탈로그는 시각적 와이어프레임이라 인터랙티브 컴포넌트(셀렉트·체크박스·라디오·토글·탭 등)를 상태 클래스(`.on`, `.active`)가 붙은 `<span>`/`<div>`로만 표현한다. 반면 `templates/` 아래 실제 프로덕션 스니펫은 네이티브 폼 엘리먼트(`<select>`, `<input type="checkbox|radio">`, `<button>`, `<a>`)를 사용하도록 교체했다 — §7 참고. 클래스 이름과 구조는 대부분 동일하지만 **태그 자체가 다른 경우**가 있으니 실제 페이지를 만들 때는 항상 `templates/`의 마크업을 기준으로 삼는다(원본 카탈로그는 시각 참고용).

## 1. CSS 클래스

### 1.1 컴포넌트 루트 클래스
`adm-` 접두사 + kebab-case. 컴포넌트 1개당 루트 클래스 1개.

| 규칙 | 예시 |
|---|---|
| `adm-` + 명사(구) | `.adm-btn`, `.adm-table`, `.adm-filter-card` |
| 복합어는 하이픈으로 연결 | `.adm-icon-btn`, `.adm-choice-group`, `.adm-badge-cnt` |
| 래퍼가 필요하면 `-wrap` 접미사 | `.adm-table-wrap` |

### 1.2 변형 (Variant)
컴포넌트 루트 클래스에 **접두사 없는 단독 클래스**를 병기한다. 변형 클래스 자체는 컴포넌트 스코프 밖에서 재사용하지 않는다(항상 루트 클래스와 함께 사용).

| 변형 축 | 값 | 예시 |
|---|---|---|
| 색/의미 | `line`, `ghost`, `danger`, `gray`, `red`, `dark` | `.adm-btn.line`, `.adm-tag.red`, `.adm-gnb.dark` |
| 크기 | `sm`, `lg`, `full` | `.adm-btn.sm`, `.adm-select.sm` |
| 배치/레이아웃 | `inline`, `fixed`, `fluid`, `wide`, `bare`, `date` | `.adm-filter-card.inline`, `.adm-tabs.fixed`, `.adm-modal.wide` |

### 1.3 상태 (State)
컴포넌트 유형별로 허용되는 상태 클래스를 고정한다. 임의로 새 상태명을 만들지 않는다.

| 상태 클래스 | 의미 | 적용 대상 |
|---|---|---|
| `.on` | 활성/체크됨 (토글형) — **원본 카탈로그 표기법**. 실제 템플릿은 `input:checked`로 구동(§7) | `.adm-check`, `.adm-radio`, `.adm-toggle` |
| `.active` | 현재 선택/열림 | `.adm-chip`, `.adm-tabs .tab`, `.adm-tabs2 .t`, `.adm-gnb .grp` |
| `.selected` | 선택된 항목(버튼형 선택, 테이블 행) | `.adm-choice`, `.adm-table tr` |
| `.disabled` | 비활성 (클릭 불가) | 대부분의 인터랙티브 컴포넌트 공통 |
| `.open` | 펼침 상태 | `.adm-gnb .grp`, `.adm-tree-cell .cv` |
| `.error` | 검증 실패 | `.adm-input`, `.adm-field .help` |
| `.cur` | 현재 페이지 | `.adm-paging .pg` |
| `.hover` | 호버 데모 표기(문서용, 실제 서비스에선 `:hover` 사용) | `.adm-table tr` |

### 1.4 내부 요소 (Sub-element)
컴포넌트 스코프 안에서만 의미를 갖는 짧은 클래스. 반드시 부모 셀렉터와 함께 정의한다(`.adm-modal .m-ttl`처럼 단독 사용 금지).

| 컴포넌트 | 내부 요소 클래스 |
|---|---|
| `.adm-modal` | `.m-head`, `.m-ttl`, `.m-x`, `.m-desc`, `.m-sec`, `.m-body`, `.m-foot` |
| `.adm-alert` | `.a-msg`, `.a-sub`, `.a-acts` |
| `.adm-table` | `.sort` (+ `i.up`, `i.dn`, `i.on`) |
| `.adm-tree-cell` | `.cv` (caret), `.d2`/`.d3`/`.d4` (depth) |
| `.adm-search` | `.ic` (아이콘 슬롯) |
| `.adm-date` | `.ic`, `.tilde` |
| `.adm-select` | `select`(실제 네이티브 엘리먼트), `::after`(화살표 — DOM 요소 아닌 CSS 장식) |
| `.adm-toolbar` | `.total`, `.left`, `.right` |
| `.adm-filter-card` | `.f`(필드), `.acts` |
| `.adm-pagebar` | `.left`, `.ttl`, `.acts` |
| `.adm-crumb` | `.sep`, `.cur` |
| `.adm-topbar` | `.env`(환경 뱃지) |
| `.adm-utils` | `.u`(로그아웃 등은 실제 `<button class="u">`), `.divider` |
| `.adm-gnb` | `.brand`(`.tit`, `.desc`), `.grp`, `.cv`, `.sub` |

### 1.5 조합 컴포넌트
독립 컴포넌트를 감싸는 상위 컴포넌트는 `adm-field`(라벨+컨트롤+헬프텍스트 묶음), `adm-opt`(체크/라디오/토글 + 라벨 묶음)처럼 별도 루트 클래스를 갖는다. 내부에는 다른 `.adm-*` 컴포넌트를 그대로 배치한다.

## 2. CSS 토큰 (3계층)

컴포넌트 CSS는 반드시 토큰(`var(--*)`)만 사용한다. hex 값을 직접 쓰지 않는다.

| 계층 | 설명 | 예시 |
|---|---|---|
| 원시(Primitive) | 색상 스케일 원본값 | `--g0`~`--g900`, `--green-500/600/700`, `--red-500/600`, `--blue-500` |
| 시맨틱(Semantic) | 용도별 별칭 | `--text`, `--text-sub`, `--text-faint`, `--line`, `--line-strong`, `--bg-page`, `--bg-fill` |
| 형태(Shape) | 라운드/그림자/폰트 | `--r-sm`~`--r-full`, `--shadow-card`, `--shadow-modal`, `--font` |

새 토큰이 필요하면 원시값을 먼저 추가하고, 컴포넌트에서는 시맨틱 토큰을 통해 참조한다.

## 3. 파일 / 디렉토리 명명 (Phase 2 이후 적용)

| 대상 | 규칙 | 예시 |
|---|---|---|
| 컴포넌트 CSS | `adm-<컴포넌트>.css` (kebab-case, 컴포넌트 루트 클래스명에서 `adm-` 유지) | `adm-button.css`, `adm-filter-card.css` |
| 컴포넌트 템플릿 | `<컴포넌트>.html` (`adm-` 접두사 생략) | `button.html`, `filter-card.html` |
| 컴포넌트 문서 | `<컴포넌트>.md` | `button.md`, `filter-card.md` |
| 레이아웃 템플릿 | 역할명 그대로 | `topbar.html`, `gnb.html`, `pagebar.html` |
| 페이지 디렉토리 | 서비스/도메인명(kebab-case) 하위에 화면명 | `pages/chatbot/conversation-list.html` |

## 4. 문서 전용 클래스 — 실제 페이지에 사용 금지

`ds-*`(디자인시스템 문서 스캐폴드: `.ds-wrap`, `.ds-sec`, `.ds-panel`, `.ds-demo` 등)와 `pv-*`(조합 미리보기 축소 표시: `.pv-wrap`, `.pv-scale`, `.pv-frame`)는 카탈로그 문서 전용이다. 실제 관리자 페이지 제작 시 이 클래스들은 사용하지 않는다.

**예외**: `.adm-dim-demo`는 `adm-` 접두사를 갖지만 실제로는 모달 데모를 나란히 배치하기 위한 문서 전용 레이아웃 클래스다(원본 파일의 네이밍 예외). 실제 페이지의 모달 딤 처리에는 사용하지 않는다 — 실제 딤은 [modal.md](docs/components/modal.md)에 명시된 `rgba(25,27,31,.5)` 오버레이를 별도로 구현한다.

**파일 위치**: 이 클래스들의 CSS는 `assets/css/catalog.css` 한 파일에 모여 있으며, `admin-common-design-system_v02.html`에만 `<link>`로 연결한다. `assets/css/tokens.css` / `base.css` / `components/*.css`(실제 페이지가 쓰는 컴포넌트 CSS)와는 완전히 분리된 별도 소스다 — 실제 페이지 템플릿(`templates/`)에는 `catalog.css`를 연결하지 않는다. 새 문서 전용 스타일이 필요하면 `components/*.css`가 아니라 `catalog.css`에 추가한다.

## 5. 캔버스 스코프 래퍼 — `.adm-frame`

`.adm-frame`은 UI 컴포넌트가 아니라 하위 요소 전체에 `box-sizing: border-box`와 `font-family: var(--font)`를 강제하는 **캔버스 루트 스코프 래퍼**다. 모든 실제 페이지의 최상위 컨테이너(2560px 프레임)에 적용한다. 상세는 [layout.md](docs/foundation/layout.md) 참고.

## 6. 사이즈 modifier ↔ 컨트롤 높이 매핑

버튼·셀렉트 등 모든 사이즈 modifier는 [layout.md](docs/foundation/layout.md)의 컨트롤 높이 체계와 1:1로 대응한다.

| modifier | 높이 | 대상 |
|---|---|---|
| `.sm` | 32px | `.adm-btn`, `.adm-icon-btn`, `.adm-select` |
| (기본, 클래스 없음) | 40px | `.adm-btn`, `.adm-input`, `.adm-select`, `.adm-search`, `.adm-date` |
| `.lg` | 48px | `.adm-btn` |
| `.full` | 52px | `.adm-btn`(모달 하단 전용) |

## 7. 인터랙티브 요소는 반드시 실제 시맨틱 엘리먼트를 사용한다

**왜**: 원본 카탈로그를 그대로 베껴 `templates/`를 처음 만들었을 때 셀렉트·체크박스·라디오·토글·탭·링크·아이콘 버튼이 전부 `<span>`/`<div>`로만 구성돼 있었다. 시각적으로는 원본과 동일해 보였지만 클릭해도 드롭다운이 열리지 않고, 체크 상태가 바뀌지 않고, 키보드·스크린 리더로 전혀 조작할 수 없었다 — 실제 페이지에 그대로 쓰면 기능이 작동하지 않는 컴포넌트가 된다.

**규칙**: 기능(용도)과 태그를 아래처럼 1:1로 고정한다. 임의로 `<span>`/`<div>` + 클래스만으로 인터랙션을 흉내 내지 않는다.

| 용도 | 필수 태그 | 상태 구동 방식 |
|---|---|---|
| 드롭다운 선택 | `<select><option>` | 브라우저 네이티브 (JS 불필요) |
| 다중 선택 | `<input type="checkbox">` (`<label>`로 감싸기) | `:checked` CSS (JS 불필요) |
| 배타 선택 | `<input type="radio" name="...">` (`<label>`로 감싸기) | `:checked` CSS (JS 불필요) |
| 배타 선택(세그먼트 버튼형 — 초이스 그룹) | `<input type="radio" name="...">` (버튼 모양 `<label class="adm-choice">`로 감싸기) | `:has(input:checked)` CSS (JS 불필요) |
| On/Off 토글 | `<input type="checkbox">` + 스위치 비주얼 | `:checked` CSS (JS 불필요) |
| 클릭 가능한 버튼(제출 아님) | `<button type="button">` | — |
| 폼 제출 버튼 | `<button type="submit">` | — |
| 페이지 이동/링크 | `<a href="...">` | — |
| 탭 전환 | `<button role="tab" aria-selected>` | `assets/js/adm-interactions.js` |
| 펼침/접힘(GNB 그룹 등) | `<button aria-expanded>` | `assets/js/adm-interactions.js` |
| 모달 열기/닫기 | `<button data-modal-open\|data-modal-close>` | `assets/js/adm-interactions.js` |
| 칩 프리셋(배타적 단일 선택) | `<button type="button">` | `assets/js/adm-interactions.js` (같은 부모 안 형제 `.adm-chip` 기준으로 `.active` 배타 전환) |

**적용 범위**: 비활성(disabled) 상태도 클래스(`.disabled`)만으로 끝내지 말고 실제 `disabled` 속성을 함께 지정한다 — 클래스는 시각 스타일만 담당하고, 실제 상호작용 차단은 네이티브 속성이 담당해야 한다.

**예외**: 순수 정보 표시(태그, 뱃지, 아바타, 트리 리프 노드 등 클릭 동작이 없는 요소)는 지금처럼 `<span>`으로 둔다 — 이 규칙은 클릭·선택·입력 등 실제 인터랙션이 있는 요소에만 적용된다.

각 컴포넌트 문서(`docs/components/*.md`)의 "사용 규칙 / 금지 사항"에 해당 컴포넌트별 세부 규칙이 기재돼 있다.

## 8. 아이콘은 항상 `assets/images/icons`의 아이콘만 사용하고, 인라인 style은 금지한다

버튼·검색·날짜·GNB 등 아이콘이 필요한 모든 곳은 `assets/images/icons/`에 있는 아이콘만 쓴다. 페이지 제작 중 새 아이콘이 필요하다고 임의로 다른 아이콘 팩에서 받아오거나 새로 그리지 않는다 — 아이콘 소스가 페이지마다 제각각이 되면 스타일(선 굵기·라운드·시각적 무게)이 어긋난다.

파일은 `ic-` + kebab-case 의미 이름(`ic-search.svg`, `ic-delete.svg`)으로 통일돼 있으며, 전체 목록과 사용법은 [icons.md](docs/foundation/icons.md)에 문서화돼 있다. 표에 맞는 아이콘이 없으면 먼저 그 문서에 파일을 추가하고 등록한 뒤 사용한다.

**마크업 규칙**: 아이콘은 항상 `<span class="adm-icon ic-<이름> sz-<크기>"></span>` 형태로만 쓴다 — 크기·파일 경로를 인라인 `style`로 지정하지 않는다. 클래스는 [adm-icon.css](assets/css/components/adm-icon.css)에 등록돼 있으며, `background-image`로 참조한다(v0.2의 `mask-image` 방식은 `file://`에서 아이콘이 전부 사라지는 문제가 있어 폐기했다 — 자세한 배경은 [icons.md](docs/foundation/icons.md) 참고). 새 아이콘·새 크기가 필요하면 마크업에 인라인 style을 쓰지 말고 `adm-icon.css`에 클래스를 먼저 추가한다.

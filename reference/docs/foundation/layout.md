# 레이아웃 그리드 (Layout)

모든 어드민 SB 캔버스의 고정 규격. 콘텐츠는 LNB 우측에서 95px 여백을 두고 1440px 고정 폭으로 좌측 정렬한다(중앙 정렬 아님 — 우측에는 나머지 공간이 남는다).

원본: [admin-common-design-system_v02.html](../../admin-common-design-system_v02.html) §1.3

## 프레임 규격

| 항목 | 규격 |
|---|---|
| 프레임 | `W 2560px` 고정 · 높이는 콘텐츠에 따라 가변 (`min-height 1440px`) |
| 헤더 | `H 52px` · LNB 우측 전체 폭(`2300px`) · 하단 1px 라인 |
| LNB | `W 260px` · 상단부터 전체 높이(헤더 포함 좌측 전체) · 우측 1px 라인 |
| 콘텐츠 영역 | `W 1440px` 고정 · LNB 우측 여백 `95px` 후 좌측 정렬 (LNB 제외 2300px 중 우측 `765px`는 여백으로 남음) |
| 수직 여백 | 상단 `48px` (헤더 → 페이지 타이틀) · 하단 `96px` |
| 수직 리듬 | 페이지 타이틀 → 콘텐츠 `32px` · 섹션 간 `40px` · 카드 간 `24px` · 카드 내부 패딩 `24px` |

## 프레임 셸 — `.adm-frame` / `.adm-col` / `.adm-main` / `.adm-content`

`.adm-frame`은 하위 요소 전체에 `box-sizing: border-box`와 `font-family: var(--font)`를 강제하는 캔버스 루트 스코프 래퍼이자, `W 2560px` 고정 프레임 자체다(LNB + 우측 컬럼을 `display:flex`로 배치). 모든 실제 페이지의 최상위 컨테이너에 적용한다.

- `.adm-col` — LNB를 제외한 우측 컬럼. 헤더(`.adm-topbar`)와 본문을 세로로 쌓는다.
- `.adm-main` — 헤더 아래 본문 영역. LNB 우측에 `95px` 여백을 두고 콘텐츠를 좌측 정렬한다.
- `.adm-content` — 실제 콘텐츠 영역. `W 1440px` 고정, 상단 `48px` / 하단 `96px` 여백, 내부 블록 간 `24px` 간격.

```html
<div class="adm-frame">
  <div class="adm-gnb dark"><!-- LNB, docs/components/layout-gnb.md --></div>
  <div class="adm-col">
    <div class="adm-topbar"><!-- 헤더, docs/components/layout-topbar.md --></div>
    <div class="adm-main">
      <div class="adm-content">
        <!-- 페이지 콘텐츠: adm-pagebar, adm-filter-card, adm-toolbar, adm-table 등 -->
      </div>
    </div>
  </div>
</div>
```

## 간격 스케일

```
4 · 8 · 12 · 16 · 20 · 24 · 32 · 40 · 48 · 64 · 96
```

모든 margin/padding/gap 값은 이 스케일 안에서 선택한다.

## 라운드 (`--r-*`)

| 토큰 | 값 | 용도 |
|---|---|---|
| `--r-sm` | 6px | (소형 컨트롤) |
| `--r-md` | 8px | 버튼·인풋 |
| `--r-lg` | 12px | 카드·테이블 |
| `--r-xl` | 16px | 모달 |
| `--r-full` | 999px | 칩·토글·아바타 (pill/circle) |

## 그림자

| 토큰 | 값 | 용도 |
|---|---|---|
| `--shadow-card` | `0 1px 3px rgba(25,27,31,.06)` | 카드 |
| `--shadow-modal` | `0 12px 40px rgba(25,27,31,.18)` | 모달·알럿 |

## 컨트롤 높이

| 크기 | 높이 | 대상 |
|---|---|---|
| 소형(sm) | 32px | 버튼(sm), 아이콘버튼(sm), 셀렉트(sm), 칩 |
| 기본 | 40px | 버튼, 인풋, 셀렉트, 서치, 데이트피커, 아이콘버튼 |
| 대형(lg) | 48px | 버튼(lg) |
| 모달 풀버튼 | 52px | 버튼(full, 모달 하단 전용) |

## 사용 규칙

- 새 페이지 제작 시 프레임·콘텐츠 폭·여백은 이 표를 그대로 따른다(페이지별 임의 조정 금지).
- 간격 값은 반드시 위 스케일 안의 숫자만 사용한다.

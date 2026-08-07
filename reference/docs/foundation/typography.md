# 타이포그래피 (Typography)

Pretendard Variable 단일 서체. 행간 1.5 고정, 자간은 20px 이상 타이틀만 -1%.

원본: [admin-common-design-system_v02.html](../../admin-common-design-system_v02.html) §1.2

## 클래스 계약

> **v0.2 변경**: 원본 §1.2 데모는 `<div style="font-size:...">`처럼 인라인 스타일로만 표기돼 있었다. 실제 페이지에서 그대로 베끼면 크기·자간 값이 페이지마다 흩어져 스케일이 깨지기 쉽다. `assets/css/base.css`에 실제 클래스로 고정했다.
>
> **v0.2 추가**: 클래스는 크기/굵기/자간만 담당하고 태그는 관여하지 않는다(전역 리셋 `*{margin:0}`이 적용돼 있어 `h1`~`h6`/`p`로 바꿔도 여백이 깨지지 않는다). 데모(§1.2)도 `div` 대신 문맥에 맞는 실제 태그(`h1`~`h3`, `p`, `span`)를 사용하도록 갱신했다 — 아래 사용 규칙 참고.

| 클래스 | 크기/굵기 | 자간 | 용도 |
|---|---|---|---|
| `.adm-type-display` | 28 / Bold | -1% | 대시보드 요약 수치 등 (제한적 사용) |
| `.adm-type-title-1` | 24 / Bold | -1% | 페이지 타이틀 |
| `.adm-type-title-2` | 20 / Bold | -1% | 모달 타이틀 |
| `.adm-type-title-3` | 17 / Bold | — | 카드·섹션 타이틀 |
| `.adm-type-body` | 14 / Regular | — | 본문, 테이블 셀, 인풋 |
| `.adm-type-body.medium` | 14 / Medium | — | 본문 중 강조 |
| `.adm-type-caption` | 13 / Regular | — | 보조 설명 |
| `.adm-type-caption.strong` | 13 / Semibold(600) | — | 테이블 헤더 |
| `.adm-type-small` | 12 / Medium | — | 태그, 헬퍼 텍스트, 카운터 |

## HTML 스니펫

```html
<h1 class="adm-type-title-1">고객 관리</h1>
<p class="adm-type-body">본문 텍스트</p>
<p class="adm-type-caption" style="color:var(--g600);">보조 설명 텍스트</p>
```

## 사용 규칙

- 서체는 `var(--font)` (Pretendard Variable → 시스템 폰트 폴백) 하나만 사용한다.
- 행간은 `line-height: 1.5` 고정(`body`에서 전역 지정).
- 자간(`letter-spacing: -0.01em`)은 20px 이상 타이틀(Display, Title 1, Title 2)에만 적용한다.
- Body 이하 크기에는 자간을 적용하지 않는다.
- 텍스트 색상은 타이포그래피 클래스에 포함하지 않는다 — 필요하면 시맨틱 색상 토큰(`var(--text-sub)`, `var(--text-faint)` 등)을 별도로 지정한다.
- 버튼·인풋·테이블 등 이미 자체 폰트 크기를 갖는 `.adm-*` 컴포넌트 내부에는 이 클래스를 중복 적용하지 않는다 — 컴포넌트 스펙이 우선한다.
- **태그는 시각 스타일(클래스)이 아니라 문맥의 시맨틱 역할로 고른다.** `div`는 의미 없는 컨테이너에만 쓴다.
  - 페이지/모달/카드·섹션 타이틀(Title 1~3) → 문서 구조상 맞는 `h1`~`h6`(페이지당 `h1`은 하나, 이후 중첩 depth에 맞춰 `h2`, `h3`…).
  - 본문·보조 설명 문단(Body, Caption) → `p`.
  - 태그·헬퍼 텍스트·카운터처럼 다른 요소 안에 끼워 넣는 짧은 조각(Small) → `span`.
  - 같은 시각 클래스라도 쓰이는 자리에 따라 태그가 달라질 수 있다(예: `.adm-type-body`를 테이블 셀(`td`)이나 인풋 옆 안내문에 쓸 때는 그 자리의 태그를 그대로 쓰고 `p`로 감싸지 않는다).

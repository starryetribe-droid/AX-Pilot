# 태그 · 뱃지 · 링크 · 아바타 (`.adm-tag`, `.adm-badge-cnt`, `.adm-avatar`, `.adm-link`)

원본: [admin-common-design-system_v02.html](../../admin-common-design-system_v02.html) §3.7

## 개요

상태 태그는 채움형이 기본. 카운트 뱃지는 답글 수 등 수치 표기 전용.

## 클래스 계약

| 구분 | 클래스 | 설명 |
|---|---|---|
| 루트 | `.adm-tag` | 상태 태그(기본: green 채움) |
| Variant | `.adm-tag.gray` | 대기/중립 상태 |
| Variant | `.adm-tag.red` | 반려/오류 상태 |
| Variant | `.adm-tag.line` | 흰 배경 + green 테두리 |
| Variant | `.adm-tag.line-gray` | 흰 배경 + 회색 테두리(임시저장 등) |
| 루트 | `.adm-badge-cnt` | 숫자 카운트 뱃지(원형) |
| 루트 | `.adm-avatar` | 원형 아바타(이니셜) |
| Size | `.adm-avatar.sm` | 22×22px |
| 조합 | `.adm-user` | 아바타 + 이름 묶음 |
| 루트 | `a.adm-link` | 텍스트 링크(blue-500, 밑줄) — 실제 `<a href>` |
| State | `span.adm-link.disabled` | 비활성 — 실제 링크가 아니므로 `<a>` 대신 `<span aria-disabled="true">` |

## 스펙

| 항목 | 값 |
|---|---|
| 태그 | 높이 24px, 라운드 `--r-sm`, 12px/600 |
| 뱃지 | 최소폭 20px, 원형, 11px/600 |
| 아바타 | 28×28px(sm 22×22px), 원형, 11px/700 |
| 링크 | 13.5px, `--blue-500`, 밑줄 |

## HTML 스니펫

```html
<span class="adm-tag">검증 완료</span>
<span class="adm-tag gray">대기</span>
<span class="adm-tag red">반려</span>
<span class="adm-tag line">진행중</span>
<span class="adm-tag line-gray">임시저장</span>
<span class="adm-badge-cnt">3</span>

<a href="#" class="adm-link">Link</a>
<span class="adm-link disabled" aria-disabled="true">Link 비활성</span>

<span class="adm-user"><span class="adm-avatar">김</span>김케이</span>
<span class="adm-user"><span class="adm-avatar sm">박</span>박지후</span>
```

## 사용 규칙 / 금지 사항

- **활성 링크는 반드시 실제 `<a href="...">`를 사용한다.** `<span>`만으로는 클릭해도 이동하지 않고 키보드 포커스도 잡히지 않는다.
- 비활성 링크는 `<a>`가 아닌 `<span class="adm-link disabled" aria-disabled="true">`로 둔다(비활성 앵커라는 개념 자체가 없으므로).
- 링크(`.adm-link`)는 파란색(blue-500)을 사용하는 유일한 컴포넌트다. 다른 컴포넌트에 blue를 사용하지 않는다.
- 태그의 색상 variant는 상태 의미와 일관되게 매핑한다: green=긍정/완료, gray=대기/중립, red=반려/오류.

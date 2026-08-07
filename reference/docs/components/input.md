# 인풋 · 텍스트에어리어 (`.adm-field`, `.adm-input`, `.adm-textarea`)

원본: [admin-common-design-system_v02.html](../../admin-common-design-system_v02.html) §3.4

## 개요

라벨은 상단 13px/600, 필수는 빨간 * 표기. 포커스는 g900 테두리, 에러는 red-500 테두리 + 하단 메시지.

## 클래스 계약

| 구분 | 클래스 | 설명 |
|---|---|---|
| 루트(래퍼) | `.adm-field` | 라벨+컨트롤+헬프텍스트 세로 묶음(gap 8px) |
| 내부 | `.adm-field > label` | 라벨(13px/600) |
| 내부 | `.adm-field > label .req` | 필수 표시(`*`, red-500) |
| 내부 | `.adm-field .help` | 헬프/에러 텍스트(12px) |
| State | `.adm-field .help.error` | 에러 메시지(red-500) |
| 컨트롤 | `.adm-input` | 텍스트 인풋 |
| State | `.adm-input.error` | 에러(red-500 테두리) |
| State | `.adm-input:disabled` | 비활성 |
| 컨트롤 | `.adm-textarea` | 여러 줄 입력, 세로 리사이즈만 허용 |
| 내부 | `.adm-count` | 글자수 카운터(우측 정렬, 12px) |

## 스펙

| 항목 | 값 |
|---|---|
| 인풋 높이 | 40px, 좌우 패딩 12px |
| 텍스트에어리어 | 최소 높이 110px, 패딩 12px |
| 테두리 | `1px solid var(--line-strong)`, 포커스 `var(--g900)`, 에러 `var(--red-500)` |
| 라운드 | `--r-md` |
| Disabled | 배경 `--g50`, 텍스트 `--g400` |

## HTML 스니펫

```html
<div class="adm-field">
  <label>고객명<span class="req">*</span></label>
  <input class="adm-input" placeholder="이름을 입력해주세요">
</div>

<div class="adm-field">
  <label>연락처<span class="req">*</span></label>
  <input class="adm-input error" value="010-1234">
  <span class="help error">연락처 형식이 올바르지 않습니다.</span>
</div>

<div class="adm-field">
  <label>고객 ID</label>
  <input class="adm-input" value="etribe_01" disabled>
  <span class="help">자동 발급 항목입니다.</span>
</div>

<div class="adm-field">
  <label>요청사항 입력</label>
  <textarea class="adm-textarea" placeholder="요청사항을 입력해 주세요"></textarea>
  <span class="adm-count">0/500</span>
</div>
```

## 사용 규칙 / 금지 사항

- 에러 상태는 인풋 테두리(`.error`)와 헬프 텍스트(`.help.error`)를 항상 함께 표시한다(하나만 단독 사용 금지).
- 글자수 제한이 있는 텍스트에어리어는 반드시 `.adm-count`를 함께 배치한다.

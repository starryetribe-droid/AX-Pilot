# 카드 (`.adm-card`)

원본: [admin-common-design-system_v02.html](../../admin-common-design-system_v02.html) (Foundation 레이아웃 §1.3의 카드 간격 규칙 참고, 별도 데모 섹션은 없음)

## 개요

정보를 묶어 표시하는 범용 컨테이너. 필터 카드([filter-card.md](filter-card.md))와 동일한 테두리/라운드/패딩을 공유한다.

## 클래스 계약

| 구분 | 클래스 | 설명 |
|---|---|---|
| 루트 | `.adm-card` | 카드 컨테이너 |
| 내부 | `.adm-card .card-ttl` | 카드 타이틀(17px/700) |

## 스펙

| 항목 | 값 |
|---|---|
| 배경 | `#fff` |
| 테두리 | `1px solid var(--line)` |
| 라운드 | `--r-lg` (12px) |
| 패딩 | 24px |
| 타이틀 하단 여백 | 16px |
| 카드 간 간격 | 24px ([layout.md](../foundation/layout.md) 수직 리듬 참고) |

## HTML 스니펫

```html
<div class="adm-card">
  <div class="card-ttl">기본 정보</div>
  <!-- 카드 내용: adm-field, adm-table 등 다른 컴포넌트를 조합 -->
</div>
```

## 사용 규칙 / 금지 사항

- 카드 내부 패딩(24px)과 카드 간 간격(24px)은 [layout.md](../foundation/layout.md)의 수직 리듬 값을 그대로 따른다.
- 타이틀이 없는 카드는 `.card-ttl`을 생략할 수 있다.

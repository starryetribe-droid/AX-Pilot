# 트리 테이블 (`.adm-tree-cell`)

원본: [admin-common-design-system_v02.html](../../admin-common-design-system_v02.html) §3.10

## 개요

계층 구조 데이터를 테이블 안에서 표현. 뎁스당 들여쓰기 24px. 접힘 ▸ / 펼침 ▾ 캐럿. 최하위 데이터 행은 캐럿 없이 보조 색.

> **v0.2 추가**: `button.adm-tree-cell` 클릭 시 `aria-expanded`/캐럿을 전환하고, 같은 `<tbody>` 안에서 더 깊은 뎁스로 이어지는 `<tr>`들을 표시/숨김한다. 동작은 `assets/js/adm-interactions.js`(뎁스는 `.d2`/`.d3`/`.d4` 클래스로 판별, 페이지 데이터에 의존하지 않는 순수 DOM 순회).

## 클래스 계약

| 구분 | 클래스 | 설명 |
|---|---|---|
| 루트 | `.adm-tree-cell` | 1뎁스 셀(캐럿 + 텍스트) |
| 내부 | `.adm-tree-cell .cv` | 캐럿(삼각형) |
| State | `.adm-tree-cell .cv.open` | 펼침(90도 회전) |
| Depth | `.adm-tree-cell.d2` | 2뎁스(들여쓰기 24px) |
| Depth | `.adm-tree-cell.d3` | 3뎁스(들여쓰기 48px) |
| Depth | `.adm-tree-cell.d4` | 4뎁스(들여쓰기 72px, 텍스트 `--g600`, 캐럿 없음) |
| 태그 | `button.adm-tree-cell` (1~3뎁스) | 확장/축소 트리거 — 실제 `<button aria-expanded>` |
| 태그 | `span.adm-tree-cell.d4` (4뎁스) | 리프 노드 — 비대화형 `<span>` |

`[selection-control.md](selection-control.md)`의 체크박스, `[table.md](table.md)`의 `.sort`와 함께 `.adm-table` 안에서 조합해 사용한다.

## 스펙

| 항목 | 값 |
|---|---|
| 뎁스당 들여쓰기 | 24px |
| 캐럿 | 삼각형(border-triangle), 펼침 시 `rotate(90deg)` |
| 최하위(d4) | 캐럿 없음, 텍스트 색 `--g600` |

## HTML 스니펫

```html
<tr>
  <td><label class="adm-opt"><input type="checkbox" aria-label="행 선택"><span class="adm-check" aria-hidden="true"></span></label></td>
  <td class="l"><button type="button" class="adm-tree-cell" aria-expanded="true"><span class="cv open" aria-hidden="true"></span>1 Depth - Open</button></td>
</tr>
<tr>
  <td><label class="adm-opt"><input type="checkbox" aria-label="행 선택"><span class="adm-check" aria-hidden="true"></span></label></td>
  <td class="l"><button type="button" class="adm-tree-cell d2" aria-expanded="true"><span class="cv open" aria-hidden="true"></span>2 Depth - Open</button></td>
</tr>
<tr>
  <td><label class="adm-opt"><input type="checkbox" aria-label="행 선택"><span class="adm-check" aria-hidden="true"></span></label></td>
  <td class="l"><span class="adm-tree-cell d4">4 Depth - Last Data</span></td>
</tr>
<tr>
  <td><label class="adm-opt"><input type="checkbox" aria-label="행 선택"><span class="adm-check" aria-hidden="true"></span></label></td>
  <td class="l"><button type="button" class="adm-tree-cell d2" aria-expanded="false"><span class="cv" aria-hidden="true"></span>2 Depth - Closed</button></td>
</tr>
```

## 사용 규칙 / 금지 사항

- 최하위 뎁스(데이터 행, `.d4`)에는 캐럿을 표시하지 않고 `<span>`으로 둔다(클릭 동작이 없으므로 버튼화하지 않는다).
- 1~3뎁스(확장 가능한 노드)는 반드시 `<button type="button" aria-expanded>`를 사용한다 — `<span>`만으로는 클릭해도 펼쳐지지 않고 키보드로도 접근할 수 없다.
- 닫힌 노드(`aria-expanded="false"`, `.cv`에 `.open` 없음)로 마크업하면 로드 시 하위 행이 자동으로 숨겨진다(하위 행 자체는 마크업에 존재해도 무방).
- 하위 뎁스 판별은 오직 클래스(`d2`/`d3`/`d4`, 없으면 1)와 `<tr>` 순서로만 이루어지므로, 뎁스 클래스를 건너뛰거나(예: 1뎁스 다음 바로 3뎁스) 순서를 어기면 표시/숨김이 잘못 계산된다.

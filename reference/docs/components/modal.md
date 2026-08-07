# 모달 · 알럿 (`.adm-modal`, `.adm-alert`)

원본: [admin-common-design-system_v02.html](../../admin-common-design-system_v02.html) §3.13

## 개요

폼 모달 W 480 / 테이블 모달 W 720 / 알럿 W 400. 딤은 `rgba(25,27,31,.5)`로 캔버스 전체를 덮는다. 모달 하단 버튼은 52px 풀폭, 알럿 버튼은 44px 균등 분할. 알럿의 우측(확정) 버튼은 삭제 포함 **항상 Primary(블랙)** — 좌측은 Line.

> **v0.2 변경**: 원본의 딤(`.adm-dim-demo`)은 문서 전용이라 실제로 열고 닫는 기능이 없었다. 실제 페이지용으로 `.adm-modal-overlay`(진짜 딤 레이어, `position:fixed;inset:0`)를 추가했고, `data-modal-open`/`data-modal-close` 속성 + `assets/js/adm-interactions.js`로 열기/닫기가 실제 동작한다. 닫기(✕) 버튼도 `<span>`에서 `<button>`으로 교체했다.

## 클래스 계약

| 구분 | 클래스 | 설명 |
|---|---|---|
| 루트(신규) | `.adm-modal-overlay` | 실제 딤 레이어(`position:fixed;inset:0;background:rgba(25,27,31,.5)`) — 기본 `hidden` 속성, 자식으로 `.adm-modal` 또는 `.adm-alert` 1개를 담음 |
| 루트 | `.adm-modal` | 폼/콘텐츠 모달 (W480) |
| Variant | `.adm-modal.wide` | 테이블 등 넓은 콘텐츠용 (W720) |
| 내부 | `.m-head` | 타이틀 + 닫기 버튼 행 |
| 내부 | `.m-ttl` | 모달 타이틀(Title 2, 20/Bold) |
| 내부 | `button.m-x` | 닫기(✕) 버튼 — 실제 `<button data-modal-close aria-label="닫기">` |
| 내부 | `.m-desc` | 설명 텍스트 |
| 내부 | `.m-sec` | 모달 내 섹션 타이틀 |
| 내부 | `.m-body` | 본문(폼 필드 등, `.adm-field` 간 16px 간격) |
| 내부 | `.m-foot` | 하단 액션(보통 `.adm-btn.full`) |
| 루트 | `.adm-alert` | 경량 확인 다이얼로그 (W400) |
| 내부 | `.a-msg` | 알럿 메시지(15px/600) |
| 내부 | `.a-sub` | 보조 설명(13px) |
| 내부 | `.a-acts` | 버튼 그룹(44px, 균등 분할) |
| data 속성 | `data-modal-open="{overlay id}"` | 이 속성이 있는 버튼을 클릭하면 해당 `.adm-modal-overlay`가 열린다 |
| data 속성 | `data-modal-close` | 이 속성이 있는 버튼을 클릭하면 가장 가까운 `.adm-modal-overlay`가 닫힌다 |

## 스펙

| 항목 | 값 |
|---|---|
| 모달 폭 | 480px (wide 720px) |
| 알럿 폭 | 400px |
| 모달 패딩 | 32px, 라운드 `--r-xl`(16px), `--shadow-modal` |
| 알럿 패딩 | 28px |
| 딤(dim) | `rgba(25,27,31,.5)`, 캔버스 전체 |
| 하단 버튼 | 모달 52px 풀폭 / 알럿 44px 균등 분할(flex:1) |

## HTML 스니펫

이 모달을 여는 버튼: `<button type="button" data-modal-open="modal-call-request">전화상담 신청</button>`

폼 모달:

```html
<div class="adm-modal-overlay" id="modal-call-request" hidden>
  <div class="adm-modal">
    <div class="m-head"><span class="m-ttl">전화상담 신청</span><button type="button" class="m-x" data-modal-close aria-label="닫기">✕</button></div>
    <p class="m-desc">주문하실 상품을 선택해주세요. (*표시는 필수 입력 사항입니다.)</p>
    <div class="m-body">
      <div class="adm-field"><label>고객명<span class="req">*</span></label><input class="adm-input" placeholder="이름을 입력해주세요"></div>
      <!-- 추가 필드 -->
    </div>
    <div class="m-foot"><button type="submit" class="adm-btn full">입력 완료</button></div>
  </div>
</div>
```

알럿:

```html
<!-- 단순 확인 -->
<div class="adm-modal-overlay" id="modal-alert-info" hidden>
  <div class="adm-alert">
    <div class="a-msg">메인 배너는 최대 5개까지 노출 가능합니다.</div>
    <div class="a-acts"><button type="button" class="adm-btn" data-modal-close>확인</button></div>
  </div>
</div>

<!-- 취소/확정 -->
<div class="adm-modal-overlay" id="modal-alert-leave" hidden>
  <div class="adm-alert">
    <div class="a-msg">저장하지 않은 변경사항이 있습니다.</div>
    <div class="a-sub">페이지를 나가면 입력한 내용이 사라집니다.</div>
    <div class="a-acts"><button type="button" class="adm-btn line" data-modal-close>취소</button><button type="button" class="adm-btn">나가기</button></div>
  </div>
</div>
```

## 사용 규칙 / 금지 사항

- **모달은 항상 `.adm-modal-overlay`로 감싸고 기본 `hidden` 속성을 붙인다.** 오버레이 없이 `.adm-modal`만 배치하면 닫힌 상태를 표현할 수 없고 딤도 뜨지 않는다.
- 여는 버튼에는 `data-modal-open="{overlay id}"`, 닫는 버튼(✕/취소)에는 `data-modal-close`를 지정한다 — `assets/js/adm-interactions.js`가 이 두 속성만으로 열기/닫기를 처리한다([README.md](../../README.md) 참고).
- 닫기(✕) 버튼은 반드시 `<button type="button" aria-label="닫기">`를 사용한다. `<span>`으로 두면 클릭도 키보드 접근도 되지 않는다.
- 알럿의 우측(확정) 버튼은 **삭제를 포함해 항상 Primary(블랙, `.adm-btn`)**를 사용한다. Danger(빨강)를 알럿 확정 버튼에 사용하지 않는다.
- 알럿 좌측 버튼은 항상 Line 변형.
- 콘텐츠가 폼이면 W480, 테이블 등 넓은 콘텐츠면 W720(`.wide`)을 사용한다.

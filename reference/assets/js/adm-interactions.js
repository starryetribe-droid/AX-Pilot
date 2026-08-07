/*
 * ETRIBE 공통 어드민 디자인 시스템 v0.2 — 컴포넌트 자체 상호작용
 * 프레임워크·빌드 도구 없는 순수 JS. 각 컴포넌트가 자기 자신의 표시 상태만 토글하며,
 * 페이지 데이터(어떤 탭이 어떤 콘텐츠를 보여줄지 등)에는 관여하지 않는다.
 *
 * 담당 범위:
 *   1. 탭(.adm-tabs / .adm-tabs2) 클릭 시 .active / aria-selected 전환
 *   2. GNB 그룹(.adm-gnb .grp) 클릭 시 펼침/접힘(aria-expanded, .open, 인접 .sub의 hidden)
 *   3. 모달(.adm-modal-overlay) data-modal-open / data-modal-close 컨벤션으로 열기/닫기
 *   4. 칩 필터(.adm-chip) 클릭 시 같은 그룹 안에서 .active를 배타적으로 전환
 *   5. 데이트피커(.adm-date) 클릭 시 캘린더 팝오버(.adm-date-panel)를 열어 기간(시작~종료)을 선택
 *   6. 트리 테이블(.adm-tree-cell) 클릭 시 aria-expanded/캐럿 전환 + 하위 뎁스 <tr> 표시·숨김
 *   7. 테이블 정렬(.sort) 클릭 시 정렬없음 → 오름차순 → 내림차순 3단 순환(같은 헤더 행 안에서 배타적)
 *   8. 셀 말줄임(td.truncate)의 title 속성을 셀 텍스트로 자동 동기화(수동 작성/데이터 바인딩 불필요)
 *
 * select/checkbox/radio/toggle/link/pagination/초이스 그룹 등은 네이티브 엘리먼트 + CSS(:checked 등)만으로
 * 동작하므로 이 파일에서 다루지 않는다 — docs/components/*.md 참고.
 */
(function () {
  'use strict';

  document.addEventListener('click', function (e) {
    handleTabClick(e);
    handleGnbGroupClick(e);
    handleModalOpen(e);
    handleModalClose(e);
    handleChipClick(e);
    handleDateComponent(e);
    handleTreeToggle(e);
    handleSortClick(e);
  });

  // aria-controls로 콘텐츠 패널을 연결한 탭만 패널을 전환한다 — 없는 탭은 기존처럼 활성 표시만 토글.
  function handleTabClick(e) {
    var tab = e.target.closest('.adm-tabs > .tab, .adm-tabs2 > .t');
    if (!tab) return;
    var group = tab.parentElement;
    var items = group.querySelectorAll(':scope > .tab, :scope > .t');
    items.forEach(function (el) {
      var isActive = el === tab;
      el.classList.toggle('active', isActive);
      el.setAttribute('aria-selected', isActive ? 'true' : 'false');
      var panelId = el.getAttribute('aria-controls');
      var panel = panelId && document.getElementById(panelId);
      if (panel) panel.hidden = !isActive;
    });
  }

  function handleGnbGroupClick(e) {
    var grp = e.target.closest('.adm-gnb .grp');
    if (!grp) return;
    var wasExpanded = grp.getAttribute('aria-expanded') === 'true';
    var nowExpanded = !wasExpanded;
    grp.setAttribute('aria-expanded', String(nowExpanded));
    grp.classList.toggle('open', nowExpanded);
    var sub = grp.nextElementSibling;
    if (sub && sub.classList.contains('sub')) {
      sub.hidden = !nowExpanded;
    }
  }

  function handleModalOpen(e) {
    var opener = e.target.closest('[data-modal-open]');
    if (!opener) return;
    var overlay = document.getElementById(opener.getAttribute('data-modal-open'));
    if (overlay) overlay.hidden = false;
  }

  function handleModalClose(e) {
    var closer = e.target.closest('[data-modal-close]');
    if (!closer) return;
    var overlay = closer.closest('.adm-modal-overlay');
    if (overlay) overlay.hidden = true;
  }

  // 칩 필터는 항상 같은 부모 안에서 하나만 active — 프리셋 그룹당 별도 래퍼 클래스 없이 형제 관계로 판단한다.
  function handleChipClick(e) {
    var chip = e.target.closest('.adm-chip');
    if (!chip || chip.disabled) return;
    var group = chip.parentElement;
    if (!group) return;
    var siblings = group.querySelectorAll(':scope > .adm-chip');
    siblings.forEach(function (el) {
      el.classList.toggle('active', el === chip);
    });
  }

  // ---- 데이트피커(.adm-date) 캘린더 팝오버 -----------------------------------
  // 팝오버 하나만 재사용(body 하위에 지연 생성)하고, 어떤 트리거가 열었는지 activeTrigger로 추적한다.
  var WEEKDAYS = ['일', '월', '화', '수', '목', '금', '토'];
  var datePanel = null;
  var activeTrigger = null;
  var calState = null; // { year, month(0-11), start: Date|null, end: Date|null }

  function handleDateComponent(e) {
    var trigger = e.target.closest('.adm-date');
    if (trigger) {
      toggleDatePanel(trigger);
      return;
    }
    if (datePanel && !datePanel.hidden) {
      if (datePanel.contains(e.target)) {
        handleDatePanelClick(e);
      } else {
        closeDatePanel();
      }
    }
  }

  function handleDatePanelClick(e) {
    var nav = e.target.closest('.cal-nav');
    if (nav) {
      calState.month += nav.classList.contains('cal-prev') ? -1 : 1;
      if (calState.month < 0) { calState.month = 11; calState.year--; }
      if (calState.month > 11) { calState.month = 0; calState.year++; }
      renderCalendar();
      return;
    }
    var day = e.target.closest('.day');
    if (day) {
      selectDay(new Date(parseInt(day.getAttribute('data-time'), 10)));
      return;
    }
    if (e.target.closest('.cal-reset')) {
      calState.start = null;
      calState.end = null;
      renderCalendar();
      return;
    }
    if (e.target.closest('.cal-apply')) {
      if (calState.start && calState.end) applyToTrigger();
      closeDatePanel();
    }
  }

  function selectDay(date) {
    calState.year = date.getFullYear();
    calState.month = date.getMonth();
    if (!calState.start || calState.end) {
      calState.start = date;
      calState.end = null;
    } else if (date.getTime() < calState.start.getTime()) {
      calState.end = calState.start;
      calState.start = date;
    } else {
      calState.end = date;
    }
    renderCalendar();
  }

  function toggleDatePanel(trigger) {
    if (activeTrigger === trigger && datePanel && !datePanel.hidden) {
      closeDatePanel();
      return;
    }
    openDatePanel(trigger);
  }

  function openDatePanel(trigger) {
    ensureDatePanel();
    activeTrigger = trigger;
    trigger.setAttribute('aria-expanded', 'true');
    var startEl = trigger.querySelector('.d-start');
    var endEl = trigger.querySelector('.d-end');
    var start = (startEl && parseDate(startEl.textContent)) || new Date();
    var end = (endEl && parseDate(endEl.textContent)) || start;
    calState = { year: start.getFullYear(), month: start.getMonth(), start: start, end: end };
    renderCalendar();
    positionDatePanel(trigger);
    datePanel.hidden = false;
  }

  function closeDatePanel() {
    if (!datePanel || datePanel.hidden) return;
    datePanel.hidden = true;
    if (activeTrigger) activeTrigger.setAttribute('aria-expanded', 'false');
    activeTrigger = null;
  }

  function ensureDatePanel() {
    if (datePanel) return datePanel;
    datePanel = document.createElement('div');
    datePanel.className = 'adm-date-panel';
    datePanel.setAttribute('role', 'dialog');
    datePanel.setAttribute('aria-label', '날짜 범위 선택');
    datePanel.hidden = true;
    document.body.appendChild(datePanel);
    return datePanel;
  }

  function positionDatePanel(trigger) {
    var rect = trigger.getBoundingClientRect();
    var panelWidth = 296;
    var left = rect.left + window.scrollX;
    var viewportRight = window.scrollX + document.documentElement.clientWidth;
    if (left + panelWidth > viewportRight) {
      left = rect.right + window.scrollX - panelWidth;
    }
    datePanel.style.top = (rect.bottom + window.scrollY + 6) + 'px';
    datePanel.style.left = left + 'px';
  }

  function renderCalendar() {
    var year = calState.year;
    var month = calState.month;
    var startWeekday = new Date(year, month, 1).getDay();
    var daysInMonth = new Date(year, month + 1, 0).getDate();
    var daysInPrev = new Date(year, month, 0).getDate();
    var today = new Date();

    var html = '';
    html += '<div class="cal-head">';
    html += '<button type="button" class="cal-nav cal-prev" aria-label="이전 달">‹</button>';
    html += '<span class="cal-ttl">' + year + '년 ' + (month + 1) + '월</span>';
    html += '<button type="button" class="cal-nav cal-next" aria-label="다음 달">›</button>';
    html += '</div>';
    html += '<div class="cal-grid">';
    for (var w = 0; w < 7; w++) html += '<span class="wd">' + WEEKDAYS[w] + '</span>';
    for (var i = 0; i < 42; i++) {
      var dayNum = i - startWeekday + 1;
      var cellDate, other;
      if (dayNum < 1) {
        cellDate = new Date(year, month - 1, daysInPrev + dayNum);
        other = true;
      } else if (dayNum > daysInMonth) {
        cellDate = new Date(year, month + 1, dayNum - daysInMonth);
        other = true;
      } else {
        cellDate = new Date(year, month, dayNum);
        other = false;
      }
      var cls = 'day';
      if (other) cls += ' other';
      if (sameDay(cellDate, today)) cls += ' today';
      if (calState.start && sameDay(cellDate, calState.start)) cls += ' range-start';
      if (calState.end && sameDay(cellDate, calState.end)) cls += ' range-end';
      if (calState.start && calState.end && cellDate > calState.start && cellDate < calState.end) cls += ' in-range';
      html += '<button type="button" class="' + cls + '" data-time="' + cellDate.getTime() + '">' + cellDate.getDate() + '</button>';
    }
    html += '</div>';
    html += '<div class="cal-foot">';
    html += '<span class="cal-range-txt">' + (calState.start ? formatDate(calState.start) : '시작일') + ' ~ ' + (calState.end ? formatDate(calState.end) : '종료일') + '</span>';
    html += '<span class="cal-acts"><button type="button" class="adm-btn sm line cal-reset">초기화</button><button type="button" class="adm-btn sm cal-apply">적용</button></span>';
    html += '</div>';
    datePanel.innerHTML = html;
  }

  function applyToTrigger() {
    var startEl = activeTrigger.querySelector('.d-start');
    var endEl = activeTrigger.querySelector('.d-end');
    if (startEl) startEl.textContent = formatDate(calState.start);
    if (endEl) endEl.textContent = formatDate(calState.end);
  }

  function parseDate(text) {
    if (!text) return null;
    var m = text.trim().match(/(\d{4})\D+(\d{1,2})\D+(\d{1,2})/);
    if (!m) return null;
    return new Date(parseInt(m[1], 10), parseInt(m[2], 10) - 1, parseInt(m[3], 10));
  }

  function formatDate(d) {
    return d.getFullYear() + '-' + pad2(d.getMonth() + 1) + '-' + pad2(d.getDate());
  }

  function pad2(n) {
    return n < 10 ? '0' + n : '' + n;
  }

  function sameDay(a, b) {
    return !!a && !!b && a.getFullYear() === b.getFullYear() && a.getMonth() === b.getMonth() && a.getDate() === b.getDate();
  }

  // ---- 트리 테이블(.adm-tree-cell) 확장/축소 --------------------------------
  // 뎁스는 클래스(d2/d3/d4, 없으면 1)로 판별하고, 같은 <tbody> 안에서 클릭된 행 다음부터
  // "뎁스가 더 깊은 <tr>"이 이어지는 동안을 하위 트리로 본다(더 얕거나 같은 뎁스가 나오면 종료).
  function treeCell(tr) {
    return tr && tr.querySelector('.adm-tree-cell');
  }

  function treeDepth(cell) {
    if (!cell) return null;
    if (cell.classList.contains('d4')) return 4;
    if (cell.classList.contains('d3')) return 3;
    if (cell.classList.contains('d2')) return 2;
    return 1;
  }

  function handleTreeToggle(e) {
    var btn = e.target.closest('.adm-tree-cell');
    if (!btn || btn.tagName !== 'BUTTON') return;
    var row = btn.closest('tr');
    if (!row) return;
    var depth = treeDepth(btn);
    var nowExpanded = btn.getAttribute('aria-expanded') !== 'true';
    btn.setAttribute('aria-expanded', String(nowExpanded));
    var caret = btn.querySelector('.cv');
    if (caret) caret.classList.toggle('open', nowExpanded);
    if (nowExpanded) {
      revealTreeSubtree(row, depth);
    } else {
      hideTreeSubtree(row, depth);
    }
  }

  function hideTreeSubtree(row, depth) {
    var sib = row.nextElementSibling;
    while (sib) {
      var d = treeDepth(treeCell(sib));
      if (d === null || d <= depth) break;
      sib.hidden = true;
      sib = sib.nextElementSibling;
    }
  }

  // 펼칠 때는 이미 접혀 있는 하위 노드(aria-expanded="false")를 만나면 그 노드보다 더 깊은 행은
  // 계속 숨긴 채로 둔다 — 다시 그 뎁스 이하로 돌아오면(형제로 빠져나오면) 숨김 상태를 해제한다.
  function revealTreeSubtree(row, depth) {
    var sib = row.nextElementSibling;
    var hideDepth = null;
    while (sib) {
      var cell = treeCell(sib);
      var d = treeDepth(cell);
      if (d === null || d <= depth) break;
      if (hideDepth !== null && d > hideDepth) {
        sib.hidden = true;
        sib = sib.nextElementSibling;
        continue;
      }
      hideDepth = null;
      sib.hidden = false;
      if (cell.tagName === 'BUTTON' && cell.getAttribute('aria-expanded') === 'false') {
        hideDepth = d;
      }
      sib = sib.nextElementSibling;
    }
  }

  // 초기 상태(aria-expanded="false")로 마크업된 노드의 하위 행은 로드 시점에 바로 숨긴다.
  document.querySelectorAll('.adm-tree-cell[aria-expanded="false"]').forEach(function (btn) {
    var row = btn.closest('tr');
    if (row) hideTreeSubtree(row, treeDepth(btn));
  });

  // ---- 테이블 정렬(.th-sort) 3단 순환 ---------------------------------------
  // 정렬없음 → 오름차순(up) → 내림차순(dn) → 정렬없음 순으로 순환. 같은 <thead> 안 다른 컬럼은 정렬없음으로 리셋한다.
  // 클릭 영역은 아이콘(.sort)뿐 아니라 라벨 텍스트를 포함한 헤더 버튼(.th-sort) 전체다.
  function handleSortClick(e) {
    var sort = e.target.closest('.th-sort');
    if (!sort) return;
    var thead = sort.closest('thead');
    if (thead) {
      thead.querySelectorAll('.th-sort').forEach(function (s) {
        if (s !== sort) resetSort(s);
      });
    }
    cycleSort(sort);
  }

  function cycleSort(sort) {
    var up = sort.querySelector('i.up');
    var dn = sort.querySelector('i.dn');
    var th = sort.closest('th');
    if (up.classList.contains('on')) {
      up.classList.remove('on');
      dn.classList.add('on');
      if (th) th.setAttribute('aria-sort', 'descending');
    } else if (dn.classList.contains('on')) {
      dn.classList.remove('on');
      if (th) th.setAttribute('aria-sort', 'none');
    } else {
      up.classList.add('on');
      if (th) th.setAttribute('aria-sort', 'ascending');
    }
  }

  function resetSort(sort) {
    var up = sort.querySelector('i.up');
    var dn = sort.querySelector('i.dn');
    up.classList.remove('on');
    dn.classList.remove('on');
    var th = sort.closest('th');
    if (th) th.setAttribute('aria-sort', 'none');
  }

  // ---- 셀 말줄임(td.truncate) title 자동 동기화 -----------------------------
  // title="..."을 셀 텍스트와 따로 손으로 채워 넣지 않는다 — 셀 안의 텍스트가 곧 title이 된다.
  // 초기 렌더 시 한 번 동기화하고, 이후 데이터가 늦게 채워지거나 바뀌어도 MutationObserver가 다시 맞춘다.
  function syncTruncateTitle(cell) {
    var text = cell.textContent.trim();
    if (cell.getAttribute('title') !== text) cell.setAttribute('title', text);
  }

  document.querySelectorAll('td.truncate').forEach(syncTruncateTitle);

  new MutationObserver(function (mutations) {
    mutations.forEach(function (m) {
      if (m.type === 'characterData') {
        var el = m.target.parentElement;
        var cell = el && el.closest('td.truncate');
        if (cell) syncTruncateTitle(cell);
        return;
      }
      m.addedNodes.forEach(function (node) {
        if (node.nodeType !== 1) return;
        if (node.matches('td.truncate')) syncTruncateTitle(node);
        node.querySelectorAll('td.truncate').forEach(syncTruncateTitle);
      });
    });
  }).observe(document.body, { childList: true, subtree: true, characterData: true });

  // 오버레이의 딤(배경) 클릭 시 닫기, Esc 키로 열려 있는 모달 · 데이트피커 팝오버 닫기
  document.addEventListener('click', function (e) {
    if (e.target.classList && e.target.classList.contains('adm-modal-overlay')) {
      e.target.hidden = true;
    }
  });
  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape') return;
    document.querySelectorAll('.adm-modal-overlay:not([hidden])').forEach(function (overlay) {
      overlay.hidden = true;
    });
    closeDatePanel();
  });
})();

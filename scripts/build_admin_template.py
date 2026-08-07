# -*- coding: utf-8 -*-
"""0805 공통 어드민 디자인 시스템 → feature-spec 스킬 admin-common 템플릿 재생성."""
import io, os, re, urllib.parse

DS = r"C:\Users\황다혜\Desktop\etribe_local\AX Pilot test\공통관리자_페이지_0805"
OUT = r"C:\Users\황다혜\.claude\skills\feature-spec\templates\admin-common.html"
ICON_DIR = os.path.join(DS, "assets", "images", "icons")


def data_uri(name):
    s = io.open(os.path.join(ICON_DIR, name + ".svg"), encoding="utf-8").read()
    s = re.sub(r"<\?xml.*?\?>", "", s, flags=re.S)
    s = re.sub(r"<!--.*?-->", "", s, flags=re.S)
    s = re.sub(r"\s+", " ", s).strip()
    return "data:image/svg+xml," + urllib.parse.quote(s, safe="~()*!.'-_=:/,")


names = sorted(f[:-4] for f in os.listdir(ICON_DIR) if f.endswith(".svg"))
icon_rules = "\n".join(
    ".adm-icon.%s{background-image:url(\"%s\")}" % (n, data_uri(n)) for n in names
)
ARROW_DOWN = data_uri("ic-arrow-down")
IC_SEARCH = data_uri("ic-search")
IC_CAL = data_uri("ic-calendar")

CSS = u"""<style>
/* ============================================================
   ETRIBE 공통 어드민 템플릿 (PC) — admin-common v0.2
   - 단일 출처: 공통 어드민 디자인 시스템 v0.2 (reference/admin-common-design-system.html)
     · 레이아웃/토큰/컴포넌트 룩을 그 시스템과 1:1로 맞춘 판(2026-08-06 전면 동기화).
   - 프레임 2560px / 헤더 52px / LNB 260px / 콘텐츠 1440px **좌측 정렬**(LNB 우측 95px 여백)
   - 수직: 콘텐츠 상단 48px · 하단 96px · 섹션 40px · 카드 간 24px · 카드 패딩 24px
   - 폰트: Pretendard (generate_sb.py 보일러플레이트가 CDN 로드)
   - 무채색 기본 + 상태 컬러만(Green 긍정 / Red 경고 / Blue 링크)
   - 아이콘: ic-*.svg 52종을 data URI로 내장 (SB는 standalone HTML이라 상대경로 사용 불가)

   ★ SB 전용(디자인 시스템에 없는 것, 유지):
     .adm-num 배지 오버레이 · .adm-anchor · .adm-sec-gap · .adm-kv · .adm-turn/.adm-bubble
     · .adm-table.compact · .adm-dim · 정적 상태 클래스(.on/.ph/.ar/.selected)
   ★ 디자인 시스템에만 있는 것(SB 미이식): adm-interactions.js 동작, 네이티브 폼 엘리먼트 계약,
     .adm-date-panel(캘린더 팝오버) — SB는 정적 와이어프레임이라 불필요.
   ============================================================ */
.admin-canvas{
 /* Grayscale */
 --g0:#FFFFFF;--g25:#FAFBFC;--g50:#F5F6F8;--g100:#EEF0F3;--g200:#E4E7EB;--g300:#D3D7DD;
 --g400:#B0B6BF;--g500:#8A919C;--g600:#6B7280;--g700:#4B515B;--g800:#33363D;--g900:#191B1F;
 /* Accent (상태 전용) */
 --green-50:#E9F8F1;--green-500:#0FA36B;--green-600:#0C8E60;--green-700:#0A7A52;
 --red-50:#FDEEEE;--red-500:#E5484D;--red-600:#D93D42;--blue-500:#2E6FF2;
 /* Dark Surface (LNB .adm-gnb.dark 전용) */
 --dark-bg:#2b2e3a;--dark-bg-strong:#1e2028;--dark-active-bg:rgba(255,255,255,.08);
 --dark-text:#ffffff;--dark-text-sub:#9aa0ac;
 /* Semantic */
 --text:#222222;--text-sub:#666666;--text-mute:#888888;--text-faint:#bbbbbb;
 --line:#E4E7EB;--line-strong:#D3D7DD;--bg-page:#FFFFFF;--bg-fill:#F5F6F8;
 /* Shape */
 --r-sm:6px;--r-md:8px;--r-lg:12px;--r-xl:16px;--r-full:999px;
 --shadow-card:0 1px 3px rgba(25,27,31,.06);--shadow-modal:0 12px 40px rgba(25,27,31,.18);
 --adm-font:"Pretendard Variable",Pretendard,-apple-system,BlinkMacSystemFont,system-ui,Roboto,"Helvetica Neue","Segoe UI","Apple SD Gothic Neo","Noto Sans KR","Malgun Gothic",sans-serif;
 width:2560px;min-height:1492px;background:#fff;border-radius:0;overflow:visible;
 box-shadow:0 2px 16px rgba(0,0,0,.08);font-family:var(--adm-font);color:var(--g900);
 font-size:14px;line-height:1.5;position:relative;}
.admin-canvas, .admin-canvas *{box-sizing:border-box;font-family:var(--adm-font);}

/* --- SB 넘버 배지 (영역 n / 세부 n-m) --- */
.adm-num{position:absolute;z-index:6;min-width:22px;height:22px;padding:0 6px;border-radius:11px;
 background:#FDEEEE;color:#E5484D;border:1px solid #E5484D;
 font-size:10px;font-weight:700;line-height:1;display:inline-flex;align-items:center;justify-content:center;}
/* 세부 배지도 오버레이(absolute) — 와이어프레임 레이아웃에 영향 금지 (사용자 확정 2026-07-22) */
.adm-num.sub{min-width:18px;height:16px;padding:0 5px;border-radius:8px;font-size:8.5px;background:#fff;flex-shrink:0;top:-8px;left:-8px;}
/* 배지 앵커: 버튼·셀렉트 등 단일 요소에 배지를 얹을 때 감싸는 래퍼 */
.adm-anchor{position:relative;display:inline-flex;align-items:center;gap:8px;}
.adm-anchor>.adm-num{top:-10px;left:-10px;}
/* ★ 배지 겹침 방지 (사용자 확정 2026-07-29): 영역 배지와 세부 배지 위치 분리 —
   (1) 테이블 th 세부 배지 = 컬럼 시작점 위(left:0)
   (2) 테이블 영역 배지 = 좌측 바깥(-30px)으로 이동 (첫 컬럼 배지와 충돌 방지)
   (3) 앵커 세부 배지 = 요소 시작점 위(left:0) */
.adm-anchor>.adm-num.sub{top:-8px;left:0;}
.adm-table th>.adm-num.sub{top:-8px;left:0;}

/* ============ 타이포그래피 스케일 ============ */
.adm-type-display{font-size:28px;font-weight:700;letter-spacing:-.01em;}
.adm-type-title-1{font-size:24px;font-weight:700;letter-spacing:-.01em;}
.adm-type-title-2{font-size:20px;font-weight:700;letter-spacing:-.01em;}
.adm-type-title-3{font-size:17px;font-weight:700;}
.adm-type-body{font-size:14px;font-weight:400;}
.adm-type-body.medium{font-weight:500;}
.adm-type-caption{font-size:13px;font-weight:400;}
.adm-type-caption.strong{font-weight:600;}
.adm-type-small{font-size:12px;font-weight:500;}

/* ============ 아이콘 ============
   <span class="adm-icon ic-<이름> sz-<크기>"></span> — 인라인 style 금지.
   어두운 배경(.adm-btn Primary 등) 위에는 흰색 변형 .ic-search-wh / .ic-edit-wh 사용.
   SVG fill이 파일에 고정돼 있어 currentColor 상속은 되지 않는다(.muted로 톤만 조절). */
.adm-icon{display:inline-block;flex-shrink:0;background-repeat:no-repeat;background-position:center;background-size:contain;}
.adm-icon.muted{opacity:.55;}
.adm-icon.sz-12{width:12px;height:12px;}
.adm-icon.sz-13{width:13px;height:13px;}
.adm-icon.sz-14{width:14px;height:14px;}
.adm-icon.sz-15{width:15px;height:15px;}
.adm-icon.sz-16{width:16px;height:16px;}
.adm-icon.sz-18{width:18px;height:18px;}
__ICONS__

/* ============ 레이아웃 골격 ============ */
/* 헤더 (Top Bar) H52 — v0.2: 서비스 로고는 LNB .brand로 이동, topbar는 계정/유틸만.
   신규 셸에서는 .adm-col 안에 있어 LNB 우측 폭(2300px)을 차지한다. */
.adm-topbar{position:relative;width:100%;height:52px;background:#fff;border-bottom:1px solid var(--line);
 display:flex;align-items:center;justify-content:space-between;padding:0 32px;}
.adm-topbar>.adm-num{top:6px;left:6px;}
.adm-topbar .env{font-size:11px;font-weight:600;color:var(--g600);border:1px solid var(--line-strong);
 border-radius:4px;padding:2px 7px;background:var(--g25);}
.adm-utils{display:flex;align-items:center;gap:20px;font-size:13px;color:var(--g700);}
.adm-utils .u{display:inline-flex;align-items:center;gap:8px;}
.adm-utils .divider{width:1px;height:16px;background:var(--line-strong);}
/* 구 셸(v0.1) 호환 — topbar에 로고를 두던 레거시 SB용. 신규 SB에서는 사용하지 않는다. */
.adm-logo{display:flex;align-items:center;gap:12px;}
.adm-logo .mark{display:inline-flex;align-items:center;justify-content:center;height:28px;
 padding:0 10px;background:var(--g900);color:#fff;border-radius:6px;font-weight:800;font-size:13px;letter-spacing:.06em;}
.adm-logo .svc{font-size:16px;font-weight:700;color:var(--g900);}
.adm-logo .env{font-size:11px;font-weight:600;color:var(--g600);border:1px solid var(--line-strong);
 border-radius:4px;padding:2px 7px;background:var(--g25);}

/* 바디: LNB 260 + 우측 컬럼. .adm-body가 flex row —
   신규 셸 .adm-body > .adm-gnb + .adm-col(.adm-topbar + .adm-main)
   레거시 셸 .adm-body > .adm-gnb + .adm-main 도 그대로 동작한다. */
.adm-body{display:flex;min-height:1440px;}
.adm-col{flex:1;min-width:0;display:flex;flex-direction:column;}
.adm-gnb{position:relative;width:260px;background:#fff;border-right:1px solid var(--line);padding:16px 0;flex-shrink:0;}
.adm-gnb>.adm-num{top:6px;left:6px;}
/* .brand = 서비스 로고/서비스명 헤더 블록 (v0.2부터 topbar 로고 영역을 대체) */
.adm-gnb .brand{padding:24px 24px 20px;}
.adm-gnb .brand .tit{display:block;font-size:19px;font-weight:800;color:var(--g900);letter-spacing:-.01em;}
.adm-gnb .brand .desc{display:block;margin-top:4px;font-size:13px;color:var(--g600);}
.adm-gnb .grp{display:flex;align-items:center;justify-content:space-between;padding:13px 24px;
 color:var(--g800);font-size:14px;font-weight:600;}
/* .cv = CSS 셰브런(텍스트 글리프 금지) — .open 여부로 회전만 바뀐다 */
.adm-gnb .grp .cv{width:7px;height:7px;flex-shrink:0;border-right:1.5px solid var(--g400);
 border-bottom:1.5px solid var(--g400);transform:rotate(45deg);}
.adm-gnb .grp.active,.adm-gnb .grp.open{color:var(--g900);}
.adm-gnb .grp.open .cv{border-color:var(--g700);transform:rotate(-135deg);}
.adm-gnb .sub{padding:2px 0 8px;}
.adm-gnb .sub a{display:block;padding:10px 24px 10px 40px;color:var(--g600);text-decoration:none;font-size:13.5px;}
.adm-gnb .sub a.active{color:var(--g900);font-weight:700;background:var(--g50);
 border-left:3px solid var(--g900);padding-left:37px;}
/* --- .dark 변형: 다크 서페이스 LNB (구조 동일, 색·캐럿만 다름) --- */
.adm-gnb.dark{background:var(--dark-bg);border-right:none;}
.adm-gnb.dark .brand{margin:-16px 0 0;background:var(--dark-bg-strong);}
.adm-gnb.dark .brand .tit{color:var(--dark-text);}
.adm-gnb.dark .brand .desc{color:var(--dark-text-sub);}
.adm-gnb.dark .grp,.adm-gnb.dark .grp.open{color:var(--dark-text);}
.adm-gnb.dark .grp .cv{width:0;height:0;border:4px solid transparent;border-top:5px solid var(--dark-text);
 border-bottom:0;transform:rotate(0deg);}
.adm-gnb.dark .grp.open .cv{border-top-color:var(--dark-text);transform:rotate(180deg);}
.adm-gnb.dark .sub a{color:var(--dark-text-sub);}
.adm-gnb.dark .sub a::before{content:"";display:inline-block;width:6px;height:1px;background:currentColor;
 margin-right:8px;vertical-align:middle;}
.adm-gnb.dark .sub a.active{color:var(--dark-text);font-weight:700;background:var(--dark-active-bg);
 border-left:none;border-radius:var(--r-sm);margin:0 12px;padding:10px 12px 10px 28px;}
/* 콘텐츠: LNB 우측 95px 여백 후 1440px 좌측 정렬 (중앙 정렬 아님 — 우측 765px는 여백) */
.adm-main{position:relative;flex:1;background:#fff;display:flex;justify-content:flex-start;padding-left:95px;}
.adm-content{width:1440px;padding:48px 0 96px;display:flex;flex-direction:column;gap:24px;}
.adm-content>.adm-sec-gap{height:16px;} /* 섹션 간 40px = 카드 간 24px + 16px */

/* 페이지 헤더 (브레드크럼 위 · 타이틀 24 아래 + 우측 액션) */
.adm-pagebar{position:relative;display:flex;align-items:center;justify-content:space-between;width:100%;}
.adm-pagebar>.adm-num{top:-4px;left:-30px;}
.adm-pagebar .left{display:flex;flex-direction:column;align-items:flex-start;gap:6px;}
.adm-pagebar .ttl{font-size:24px;font-weight:700;letter-spacing:-.01em;color:var(--g900);}
.adm-crumb{display:flex;align-items:center;gap:6px;font-size:12.5px;color:var(--g500);}
.adm-crumb .sep{color:var(--g300);}
.adm-crumb .cur{color:var(--g700);}
.adm-pagebar .acts{display:flex;gap:8px;align-items:center;}

/* ============ 컴포넌트 ============ */
/* 버튼 */
.adm-btn{display:inline-flex;align-items:center;justify-content:center;gap:6px;height:40px;
 padding:0 20px;border-radius:var(--r-md);border:1px solid transparent;background:var(--g900);
 color:#fff;font-size:14px;font-weight:600;cursor:pointer;white-space:nowrap;}
.adm-btn.line{background:#fff;color:var(--g800);border-color:var(--line-strong);}
.adm-btn.ghost{background:transparent;color:var(--g700);border-color:transparent;}
.adm-btn.danger{background:var(--red-500);}
.adm-btn.sm{height:32px;padding:0 14px;font-size:13px;border-radius:var(--r-sm);}
.adm-btn.lg{height:48px;padding:0 26px;font-size:15px;}
.adm-btn.full{width:100%;height:52px;font-size:15px;}
.adm-btn.disabled{background:var(--g100);color:var(--g400);border-color:transparent;}
.adm-btn.line.disabled{background:var(--g25);color:var(--g400);border-color:var(--g200);}
.adm-icon-btn{display:inline-flex;align-items:center;justify-content:center;width:40px;height:40px;
 border:1px solid var(--line-strong);border-radius:var(--r-md);background:#fff;color:var(--g700);}
.adm-icon-btn.sm{width:32px;height:32px;border-radius:var(--r-sm);}
.adm-icon-btn.ghost{border-color:transparent;background:transparent;}

/* 초이스 그룹 (폼 내 배타 선택 버튼형) */
.adm-choice-group{display:flex;gap:8px;}
.adm-choice{flex:1;height:44px;display:inline-flex;align-items:center;justify-content:center;
 border:1px solid var(--line-strong);border-radius:var(--r-md);background:#fff;color:var(--g700);
 font-size:14px;font-weight:500;}
.adm-choice.selected{border:1.5px solid var(--g900);color:var(--g900);font-weight:700;}

/* 칩 필터 · 데이트피커 */
.adm-chip{display:inline-flex;align-items:center;gap:6px;height:32px;padding:0 14px;
 border:1px solid var(--line-strong);border-radius:var(--r-full);background:#fff;color:var(--g700);
 font-size:13px;font-weight:500;}
.adm-chip.active{background:var(--g900);border-color:var(--g900);color:#fff;font-weight:600;}
.adm-chip.date{border-radius:var(--r-md);color:var(--g800);}
.adm-date{display:inline-flex;align-items:center;gap:10px;height:40px;border:1px solid var(--line-strong);
 border-radius:var(--r-md);padding:0 14px;background:#fff;font-size:13.5px;color:var(--g800);text-align:left;}
.adm-date .lead{display:inline-flex;align-items:center;gap:8px;}
.adm-date .tilde,.adm-date .ar{color:var(--g400);}
.adm-date>.adm-icon{margin-left:auto;opacity:.6;}
/* 레거시 SB(.ic 빈 스팬) 자동 보정 — 캘린더 아이콘을 배경으로 그린다 */
.adm-date .ic{margin-left:auto;width:14px;height:14px;flex-shrink:0;opacity:.6;
 background:url("__IC_CAL__") no-repeat center/contain;}

/* 필드(라벨+컨트롤) · 인풋 · 텍스트에어리어 */
.adm-field{display:flex;flex-direction:column;gap:8px;position:relative;}
.adm-field>label{font-size:13px;font-weight:600;color:var(--g800);display:inline-flex;align-items:center;gap:5px;}
.adm-field>label .req{color:var(--red-500);}
.adm-field .help{font-size:12px;color:var(--text-sub);}
.adm-field .help.error{color:var(--red-500);}
.adm-input{height:40px;width:100%;border:1px solid var(--line-strong);border-radius:var(--r-md);
 padding:0 12px;background:#fff;font-size:14px;color:var(--g900);display:inline-flex;align-items:center;}
.adm-input .ph,.adm-input.ph{color:var(--g400);}
.adm-input.error{border-color:var(--red-500);}
.adm-input.disabled{background:var(--g50);color:var(--g400);}
.adm-textarea{width:100%;min-height:110px;border:1px solid var(--line-strong);border-radius:var(--r-md);
 padding:12px;background:#fff;font-size:14px;color:var(--g400);}
.adm-count{align-self:flex-end;font-size:12px;color:var(--g400);}

/* 셀렉트 · 서치 */
.adm-select{position:relative;display:inline-flex;align-items:center;justify-content:space-between;gap:10px;
 height:40px;min-width:160px;border:1px solid var(--line-strong);border-radius:var(--r-md);
 padding:0 12px;background:#fff;color:var(--g800);font-size:14px;}
.adm-select .ph{color:var(--g400);}
/* .ar = 드롭다운 화살표(장식) — 디자인 시스템의 ic-arrow-down과 동일 아이콘 */
.adm-select .ar{width:16px;height:16px;flex-shrink:0;font-size:0;
 background:url("__ARROW_DOWN__") no-repeat center/contain;}
.adm-select.sm{height:32px;min-width:0;font-size:13px;border-radius:var(--r-sm);padding:0 10px;}
.adm-select.bare{border:none;padding:0 4px;min-width:0;font-weight:600;color:var(--g800);height:auto;}
.adm-select.disabled{background:var(--g50);color:var(--g400);}
.adm-select.disabled .ar{opacity:.4;}
.adm-search{display:inline-flex;align-items:center;justify-content:space-between;gap:8px;height:40px;min-width:260px;
 border:1px solid var(--line-strong);border-radius:var(--r-md);padding:0 12px;background:#fff;font-size:14px;color:var(--g900);}
.adm-search .ph{color:var(--g400);flex:1;}
.adm-search .ic{flex-shrink:0;display:inline-flex;}
.adm-search .ic .adm-icon{opacity:.55;}
/* 레거시 SB(.ic 빈 스팬) 자동 보정 — 돋보기 아이콘을 배경으로 그린다 */
.adm-search .ic:empty{width:15px;height:15px;opacity:.55;
 background:url("__IC_SEARCH__") no-repeat center/contain;}

/* 체크박스(다중) · 라디오(배타) · 토글
   SB는 정적 마크업이라 .on 클래스로 상태를 표기한다(디자인 시스템 실페이지는 input:checked 구동). */
.adm-check{display:inline-flex;align-items:center;justify-content:center;width:20px;height:20px;
 border:1.5px solid var(--g300);border-radius:5px;background:#fff;flex-shrink:0;vertical-align:middle;}
.adm-check.on{background:var(--g900);border-color:var(--g900);}
.adm-check.on::after{content:"";width:9px;height:5px;border-left:2px solid #fff;border-bottom:2px solid #fff;
 transform:rotate(-45deg) translateY(-1px);}
.adm-check.disabled{background:var(--g50);border-color:var(--g200);}
.adm-radio{display:inline-flex;align-items:center;justify-content:center;width:20px;height:20px;
 border:1.5px solid var(--g300);border-radius:var(--r-full);background:#fff;flex-shrink:0;vertical-align:middle;}
.adm-radio.on{border-color:var(--g900);}
.adm-radio.on::after{content:"";width:10px;height:10px;border-radius:var(--r-full);background:var(--g900);}
.adm-radio.disabled{background:var(--g50);border-color:var(--g200);}
.adm-opt{display:inline-flex;align-items:center;gap:8px;font-size:14px;color:var(--g800);}
.adm-opt.disabled{color:var(--g400);}
.adm-toggle{position:relative;width:40px;height:22px;border-radius:var(--r-full);background:var(--g300);
 flex-shrink:0;display:inline-block;vertical-align:middle;}
.adm-toggle::after{content:"";position:absolute;top:2px;left:2px;width:18px;height:18px;border-radius:var(--r-full);
 background:#fff;box-shadow:0 1px 3px rgba(0,0,0,.2);}
.adm-toggle.on{background:var(--green-600);}
.adm-toggle.on::after{left:20px;}
.adm-toggle.disabled{background:var(--g100);}

/* 태그 · 카운트 뱃지 · 링크 · 아바타 */
.adm-tag{display:inline-flex;align-items:center;height:24px;padding:0 10px;border-radius:var(--r-sm);
 font-size:12px;font-weight:600;background:var(--green-50);color:var(--green-700);}
.adm-tag.gray{background:var(--g100);color:var(--g600);}
.adm-tag.red{background:var(--red-50);color:var(--red-500);}
.adm-tag.line{background:#fff;border:1px solid var(--green-500);color:var(--green-700);}
.adm-tag.line-gray{background:#fff;border:1px solid var(--g300);color:var(--g600);}
.adm-badge-cnt{display:inline-flex;align-items:center;justify-content:center;min-width:20px;height:20px;
 padding:0 6px;border-radius:var(--r-full);background:var(--g100);color:var(--g600);font-size:11px;font-weight:600;}
.adm-link{color:var(--blue-500);text-decoration:underline;text-underline-offset:2px;font-size:13.5px;}
.adm-link.disabled{color:var(--g400);}
.adm-avatar{display:inline-flex;align-items:center;justify-content:center;width:28px;height:28px;
 border-radius:var(--r-full);background:var(--g100);color:var(--g600);font-size:11px;font-weight:700;flex-shrink:0;}
.adm-avatar.sm{width:22px;height:22px;font-size:9.5px;}
.adm-user{display:inline-flex;align-items:center;gap:8px;font-size:13.5px;color:var(--g800);}
.adm-copy{display:inline-block;width:14px;height:14px;border:1px solid var(--g400);border-radius:3px;
 margin-left:6px;vertical-align:-2px;background:var(--g50);}

/* 탭 */
.adm-tabs{display:flex;border-bottom:1px solid var(--line);}
.adm-tabs.fixed .tab{flex:1;text-align:center;}
.adm-tabs .tab{padding:12px 4px;margin-bottom:-1px;font-size:14.5px;color:var(--g500);
 border-bottom:2px solid transparent;font-weight:500;}
.adm-tabs .tab.active{color:var(--g900);font-weight:700;border-bottom-color:var(--g900);}
.adm-tabs.fluid{gap:28px;}
.adm-tabs2{display:flex;gap:24px;padding:10px 0 10px 4px;border-bottom:1px solid var(--g100);background:var(--g25);font-size:13px;}
.adm-tabs2 .t{color:var(--g500);}
.adm-tabs2 .t.active{color:var(--g900);font-weight:700;text-decoration:underline;text-underline-offset:6px;}
.adm-tabpanel{margin-top:12px;padding:20px;background:var(--g25);border:1px solid var(--line);
 border-radius:var(--r-md);color:var(--g600);font-size:13.5px;}

/* 카드 · KV(상세 정보 그리드) */
.adm-card{position:relative;background:#fff;border:1px solid var(--line);border-radius:var(--r-lg);padding:24px;}
.adm-card>.adm-num{top:-9px;left:-9px;}
.adm-card .card-ttl{font-size:17px;font-weight:700;margin-bottom:16px;}
.adm-kv{display:grid;grid-template-columns:140px 1fr 140px 1fr 140px 1fr;font-size:13.5px;}
.adm-kv>div{padding:12px 14px;border-bottom:1px solid var(--g100);position:relative;}
.adm-kv .k{color:var(--g600);}
.adm-kv .v{color:var(--g800);word-break:break-all;}
.adm-kv .lastrow{border-bottom:none;}

/* 테이블 — th 배경 #EFF3FB (디자인 시스템 v0.2 개선분).
   overflow는 SB에서 visible 유지: .adm-table-wrap>.adm-num(left:-30px) 배지가 잘리면 안 된다
   (디자인 시스템 실페이지는 overflow-x:auto로 가로 스크롤). */
.adm-table-wrap{position:relative;background:#fff;border:1px solid var(--line);border-radius:var(--r-lg);overflow:visible;}
.adm-table-wrap>.adm-num{top:-9px;left:-30px;}
.adm-table{width:100%;border-collapse:collapse;font-size:13.5px;}
.adm-table th{height:48px;padding:0 14px;background:#EFF3FB;color:var(--g600);font-weight:600;font-size:13px;
 border-bottom:1px solid var(--line);text-align:center;white-space:nowrap;}
.adm-table th.l,.adm-table td.l{text-align:left;}
.adm-table td{height:52px;padding:8px 14px;border-bottom:1px solid var(--line);color:var(--g800);
 text-align:center;white-space:nowrap;}
.adm-table th,.adm-table td{position:relative;} /* 세부 배지 오버레이 앵커 */
/* 컬럼 12개 이상 와이드 테이블용 — 좌우 패딩 축소로 1440 콘텐츠 폭 안에 수납 */
.adm-table.compact th,.adm-table.compact td{padding-left:7px;padding-right:7px;}
.adm-table tr:last-child td{border-bottom:none;}
.adm-table tr.hover td{background:var(--g25);}
.adm-table tr.selected td{background:var(--g50);}
.adm-table tr.disabled td{color:var(--g400);}
/* 긴 셀: .truncate(한 줄 말줄임) / .wrap(줄바꿈) — 기본 폭 220px 내장 */
.adm-table td.truncate{max-width:220px;overflow:hidden;text-overflow:ellipsis;}
.adm-table td.wrap{max-width:220px;white-space:normal;word-break:break-word;height:auto;text-align:left;}
/* 정렬 트리거 — SB는 정적이므로 라벨+아이콘 묶음만 표기 */
.adm-table th .th-sort{display:inline-flex;align-items:center;gap:5px;color:inherit;}
.adm-table .sort{display:inline-flex;flex-direction:column;gap:1px;margin-left:5px;vertical-align:middle;}
.adm-table .sort i{width:0;height:0;border-left:3.5px solid transparent;border-right:3.5px solid transparent;display:block;}
.adm-table .sort i.up{border-bottom:4px solid var(--g400);}
.adm-table .sort i.dn{border-top:4px solid var(--g400);}
.adm-table .sort i.on{border-bottom-color:var(--g800);border-top-color:var(--g800);}
.adm-table td .notice{color:var(--red-500);font-weight:600;}
.adm-table td .reply{color:var(--g600);}

/* 트리 테이블 셀 */
.adm-tree-cell{display:inline-flex;align-items:center;gap:8px;color:var(--g800);}
.adm-tree-cell .cv{width:0;height:0;border-top:4px solid transparent;border-bottom:4px solid transparent;
 border-left:5.5px solid var(--g500);display:inline-block;flex-shrink:0;}
.adm-tree-cell .cv.open{transform:rotate(90deg);}
.adm-tree-cell.d2{padding-left:24px;}
.adm-tree-cell.d3{padding-left:48px;}
.adm-tree-cell.d4{padding-left:72px;color:var(--g600);}

/* 페이지네이션 */
.adm-paging{position:relative;display:flex;justify-content:center;align-items:center;gap:4px;}
.adm-paging>.adm-num{left:-36px;top:5px;}
.adm-paging .pg{min-width:32px;height:32px;padding:0 6px;border-radius:var(--r-sm);
 background:transparent;color:var(--g600);font-size:13px;display:inline-flex;align-items:center;justify-content:center;}
.adm-paging .pg.cur{background:var(--g900);color:#fff;font-weight:700;}
.adm-paging .pg.nav{color:var(--g500);font-size:12px;}
.adm-paging .pg.nav.disabled{color:var(--g300);}
.adm-paging .pg .adm-icon{opacity:.6;}
.adm-paging .pg.nav.disabled .adm-icon{opacity:.3;}

/* 툴바 · 필터 카드 */
.adm-toolbar{position:relative;display:flex;align-items:center;justify-content:space-between;gap:16px;}
.adm-toolbar>.adm-num{top:-4px;left:-30px;}
.adm-toolbar .total{font-size:14px;color:var(--g800);}
.adm-toolbar .total b{font-weight:700;}
.adm-toolbar .total .cap{color:var(--g400);}
.adm-toolbar .left,.adm-toolbar .right{display:flex;align-items:center;gap:10px;}
.adm-filter-card{position:relative;background:#fff;border:1px solid var(--line);border-radius:var(--r-lg);padding:24px;}
.adm-filter-card>.adm-num{top:-9px;left:-9px;}
/* 인라인 변형: 조건 1~3개 + 검색 인풋 한 줄 (라벨 좌측 배치) — 4개 이상은 .adm-filter-grid */
.adm-filter-card.inline{display:flex;align-items:center;gap:28px;padding:16px 20px;}
.adm-filter-card.inline .f{display:flex;align-items:center;gap:10px;}
.adm-filter-card.inline .f>label{font-size:13px;font-weight:600;color:var(--g800);white-space:nowrap;}
.adm-filter-card.inline .acts{margin-left:auto;display:flex;gap:8px;}
.adm-filter-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:16px 20px;}
.adm-filter-acts{display:flex;justify-content:flex-end;gap:8px;margin-top:20px;padding-top:20px;
 border-top:1px solid var(--g100);position:relative;}

/* 모달 (SB에서는 팝업 = 별도 SB 페이지, 회색 스테이지 중앙 배치) */
.adm-modal{width:480px;background:#fff;border-radius:var(--r-xl);box-shadow:var(--shadow-modal);
 padding:32px;position:relative;}
.adm-modal.wide{width:720px;}
.adm-modal .m-head{display:flex;align-items:flex-start;justify-content:space-between;margin-bottom:8px;}
.adm-modal .m-ttl{font-size:20px;font-weight:700;letter-spacing:-.01em;}
.adm-modal .m-x{width:24px;height:24px;display:inline-flex;align-items:center;justify-content:center;
 color:var(--g500);font-size:18px;line-height:1;}
.adm-modal .m-desc{font-size:13.5px;color:var(--g600);margin-bottom:20px;}
.adm-modal .m-sec{font-size:15px;font-weight:700;margin:20px 0 12px;}
.adm-modal .m-foot{margin-top:24px;}

/* 알럿 (경량 확인 다이얼로그 — 서브 캔버스 내 배치) */
.adm-alert{width:400px;background:#fff;border-radius:var(--r-xl);box-shadow:var(--shadow-modal);padding:28px;}
.adm-alert .a-msg{font-size:15px;font-weight:600;color:var(--g900);line-height:1.5;}
.adm-alert .a-sub{font-size:13px;color:var(--g600);margin-top:6px;}
.adm-alert .a-acts{display:flex;gap:8px;margin-top:20px;}
.adm-alert .a-acts .adm-btn{flex:1;height:44px;}

/* 대화 로그 (챗봇형 상세) */
.adm-turn{padding:12px 4px;border-bottom:1px solid var(--g100);}
.adm-turn .meta{font-size:11px;color:var(--g500);margin-bottom:6px;display:flex;gap:8px;flex-wrap:wrap;align-items:center;}
.adm-bubble{border-radius:var(--r-md);padding:10px 12px;font-size:13px;line-height:1.5;margin-top:6px;}
.adm-bubble.user{background:var(--g100);color:var(--g800);}
.adm-bubble.bot{background:var(--green-50);color:var(--g800);}

/* 토스트 · 빈 상태 · 딤 */
.adm-toast{position:absolute;left:50%;transform:translateX(-50%);bottom:40px;background:rgba(25,27,31,.88);
 color:#fff;font-size:13.5px;padding:12px 22px;border-radius:var(--r-full);white-space:nowrap;}
.adm-empty{padding:64px 0;text-align:center;color:var(--g500);font-size:14px;}
.adm-empty .t{font-weight:600;color:var(--g700);margin-bottom:6px;font-size:15px;}
.adm-dim{position:absolute;inset:0;background:rgba(25,27,31,.5);} /* 캔버스 전체 딤 — 고정 height 금지 */
</style>
"""

CSS = (CSS.replace("__ICONS__", icon_rules)
          .replace("__ARROW_DOWN__", ARROW_DOWN)
          .replace("__IC_SEARCH__", IC_SEARCH)
          .replace("__IC_CAL__", IC_CAL))

io.open(OUT, "w", encoding="utf-8").write(CSS)
print("아이콘 %d종 임베드" % len(names))
print("템플릿 크기: %.1f KB" % (len(CSS.encode("utf-8")) / 1024))

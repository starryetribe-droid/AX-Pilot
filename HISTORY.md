# Feature Spec 스킬 — 프로젝트 인수인계 문서

> 이 문서는 ETRIBE 기획 자동화 도구(`feature-spec` Claude Code 스킬)의 전체 구축 맥락을 정리합니다.
> 로컬 PC가 바뀌어도, 새로운 담당자가 이 문서만 보면 전체 맥락을 이해할 수 있도록 설계되었습니다.
>
> **마지막 업데이트**: 2026-06-29

---

## 1. 한 줄 요약

ETRIBE 사내 기획자가 **"A-02 PRD 만들어줘"** 같이 자연어로 말하면 Claude Code가 ETRIBE 표준 양식의 PRD(명세서) + SB(와이어프레임)를 자동 생성하는 도구. 가이드/규칙은 **외부 서버(Vercel)**에 두어 IP 보호.

---

## 2. 산출물 — 무엇을 만들었나

### 2.1 클라이언트 (이 워크스페이스 안)

```
common_source/.claude/skills/feature-spec/
├── SKILL.md              # 스킬 본체 (Claude가 읽고 따름)
├── ONBOARDING.md         # 팀원 설치 안내문
├── HISTORY.md            # 이 파일 (인수인계용)
├── scripts/
│   ├── fetch_guide.py        # 서버에서 가이드 fetch
│   ├── generate_sb.py        # SB HTML 일괄 생성
│   ├── build_chatbot_sb.py   # 챗봇 SB 일체 생성 (인텐트# → IT### 폴더)
│   ├── chatbot_to_sb.py      # 인텐트 워크북(xlsx) → screens.json 변환
│   ├── chatbot_components.py # KRDS 아키타입 12종 렌더러 (가이드 §13 구현체)
│   ├── build_admin_sb.py     # 어드민 SB 생성 (템플릿+본문 → PC SB)
│   └── parse_admin_spec.py   # 어드민 세부기능정의 워크북 파서 + PRD/SB 커버리지 검증기
├── templates/
│   ├── sb-style-block.html   # SB의 인라인 <style> 전체
│   ├── sb-logo-data-url.txt  # ETRIBE 로고 base64 data URL
│   └── admin-pulmuone.html   # 풀무원 디자인밀 어드민 템플릿 (PC) <style>
└── samples/
    └── admin/
        └── ADM-ORDER-001.src.html  # 어드민 주문상세 화면 본문(템플릿 제외)
```

### 2.2 서버 (별도 GitHub repo + Vercel)

```
~/projects/etribe-feature-spec-server/
├── api/
│   ├── index.py                # Vercel Serverless 함수 (인증+가이드 fetch)
│   └── _data/guides/           # 가이드 6종 (HTTP 직접 노출 X)
│       ├── 0-workflow.md
│       ├── 1-features-list.md
│       ├── 2-flowchart-rules.md
│       ├── 3-prd-structure.md
│       ├── 4a-sb-guide-mobile.md
│       └── 5-feature-asset-table.md
├── vercel.json
├── requirements.txt
├── .gitignore
├── README.md
└── dev_server.py               # 로컬 개발용 (배포 X)
```

- **GitHub**: https://github.com/starryetribe-droid/etribe-feature-spec-server (Private)
- **Vercel 배포 URL**: https://etribe-feature-spec-server.vercel.app
- **환경변수**: `VALID_TOKENS` (Sensitive, 콤마 구분)

### 2.3 배포용 zip

```
~/Downloads/feature-spec.zip   # 팀원 배포용 (스킬 폴더만 압축)
```

zip 갱신 명령:
```bash
cd "{common_source}/.claude/skills"
zip -r ~/Downloads/feature-spec.zip feature-spec -x "*.DS_Store" "*__pycache__*" "*.pyc"
```

---

## 3. 핵심 아키텍처

### 3.1 IP 보호 모델 (옵션 D — 가이드 서버 보관 + 클라이언트 추론)

```
[ETRIBE 사내 IP — Vercel 서버]
   가이드 6종 (private repo + sensitive env var 보호)
            ↑ Bearer token 인증
            │
[팀원 PC]
   Claude Code
     └─ feature-spec 스킬 (thin client, IP 없음)
         └─ 트리거 시: 서버 fetch → 메모리에서만 사용 → 결과 파일 저장
            (디스크에 가이드 영구 저장 안 됨)
```

### 3.2 보호되는 것 / 노출되는 것

| 항목 | 위치 | 노출 여부 |
|------|------|----------|
| 가이드 6종 (작성 규칙) | 서버 `_data/guides/` | ❌ Bearer 인증 필요 |
| Anthropic API 키 | (사용 안 함) | — |
| 토큰 (VALID_TOKENS) | Vercel env var (Sensitive) | ❌ 대시보드에서도 *** |
| `SKILL.md` | 클라이언트 | ✅ (절차만, IP 아님) |
| `templates/` (CSS, base64) | 클라이언트 | ✅ (output에 어차피 포함됨) |
| 생성된 PRD/SB | 사용자 워크스페이스 | ✅ (산출물) |

### 3.3 LLM 추론 위치

**서버가 아니라 클라이언트(팀원의 Claude Code)에서 추론**.
이유: Anthropic API 키 비용 없음, 팀원 본인 Claude Code 구독 활용.
한계: 가이드가 메모리에 잠시 로드됨 (작정한 유출은 못 막음, NDA 보완).

---

## 4. 주요 결정사항 (Why)

### 4.1 Static Pretendard 1순위
- **이유**: HTML to Figma 플러그인이 Variable Font의 weight axis를 매핑 못 해 볼드가 풀림
- **결정**: `Pretendard, 'Pretendard GOV', 'Pretendard Variable', ...` 순서
- **참고**: 사용자 시스템에 Static Pretendard 설치 필요

### 4.2 Description 인라인 구조 (`<p class="desc-block">` + `<br>` + `<span>`)
- **이유**: HTML to Figma가 `<div>`마다 별도 텍스트 박스로 쪼갬 → 한 항목 = 한 텍스트 박스 위해
- **결정**: 한 번호 항목을 하나의 `<p>` 안에 `<span class="lvl1|lvl2|...">` + `<br>` + `&nbsp;`(들여쓰기) 조합
- **금지**: `<div>` 분리, CSS `::before`, padding 들여쓰기

### 4.3 ETRIBE 로고 base64 손상 검증 (PNG MD5)
- **이유**: 여러 차례 Edit 작업 중 base64 문자열 변형으로 PNG 손상 발생 (디버깅에 시간 소모)
- **결정**: `generate_sb.py`가 PNG MD5 (`51732c22289dc4b1eae17c2fd855ba4a`) 자동 검증
- **위치**: `templates/sb-logo-data-url.txt` (한 번 인코딩한 후 절대 수정 금지)

### 4.4 PRD 모드의 2단계 프리뷰 (Step 0 + Step 2.5)
- **Step 0**: 사용자 프로세스 입력 요청 (A/B/C/D/E 옵션)
- **Step 2.5**: Mermaid 플로우차트 프리뷰 → 사용자 승인 (무조건, D 옵션이어도 적용)
- **이유**: 자동 생성 PRD가 ETRIBE 고유 정책 누락하는 문제 + 플로우 단계에서 수정이 PRD 단계 수정보다 cheap
- **PRD/SB 본문**: 프리뷰 없이 바로 저장 (확정된 Mermaid가 일관성 보장)

### 4.5 SB 양식 v2 (ETRIBE 표준)
- 2560px 고정 폭 + 외곽 프레임(gray-30)
- 8컬럼 × 2행 메타 헤더 테이블
- 우측 Description 패널 640px (섹션 박스 2개: 화면 설명 / Description)
- 하단 ETRIBE 푸터 (full-width, 로고 background-image)
- 폰트 16px+ (메타 헤더, Description 패널)
- 샘플: `99. Sample/SB/C-01-001_etribe.html`

---

## 5. 배포 정보

### 5.1 Vercel

| 항목 | 값 |
|------|-----|
| URL | https://etribe-feature-spec-server.vercel.app |
| 프로젝트명 | etribe-feature-spec-server |
| Framework | Other (Python serverless) |
| Runtime | Python 3.x (`@vercel/python@4.3.0`) |
| 환경변수 | `VALID_TOKENS` (Sensitive) — 콤마 구분 토큰 목록 |
| 자동 배포 | GitHub `main` 브랜치 push 시 |

### 5.2 GitHub

| 항목 | 값 |
|------|-----|
| URL | https://github.com/starryetribe-droid/etribe-feature-spec-server |
| 가시성 | Private |
| 기본 브랜치 | main |
| Collaborator | 추가 시 팀원도 코드 접근 가능 |

### 5.3 git config (글로벌)

```
user.name  = starryetribe-droid
user.email = 252413829+starryetribe-droid@users.noreply.github.com
```

→ 다른 PC에서 git 사용 시에도 같은 noreply 이메일 설정해야 Vercel 배포 차단 안 됨.

---

## 6. 인증 / 토큰 관리

### 6.1 토큰 발급

```bash
python3 -c 'import secrets; print(secrets.token_urlsafe(32))'
```

### 6.2 토큰 등록 (관리자)

Vercel 대시보드 → 프로젝트 → Settings → Environment Variables → `VALID_TOKENS` 수정 → Redeploy.

### 6.3 토큰 사용 (팀원)

`~/.etribe/config.json`:
```json
{
  "server_url": "https://etribe-feature-spec-server.vercel.app",
  "token": "발급받은-토큰"
}
```

### 6.4 토큰 회전 / 차단

1. Vercel `VALID_TOKENS`에서 차단할 토큰 제거 + 새 토큰 추가
2. **Redeploy** → 즉시 적용 (옛 토큰은 그 순간부터 401)
3. 영향받은 팀원에게 새 토큰 전달

### 6.5 토큰 보관 위치

- **관리자 본인 토큰**: 메모장 또는 1Password (절대 git에 commit X)
- **팀원 토큰**: 1:1 카톡으로 전달 → 받은 사람이 1Password 등에 보관

---

## 7. 사용 방법 (관리자 본인)

### 7.1 일반 사용

워크스페이스(common_source) 안에서:

```bash
cd "/Users/Starry/Library/CloudStorage/GoogleDrive-.../common_source"
claude
```

자연어 요청:
- `A-02 PRD 만들어줘` — PRD만
- `A-04 기획해줘` — PRD + SB 통합
- `A-01 PRD에서 SB 생성` — SB만
- `A-01-003 화면 4번 항목 수정` — 부분 수정

### 7.2 가이드 수정

`00. Assets/`의 원본을 수정하고 → 수동으로 `~/projects/etribe-feature-spec-server/api/_data/guides/`에 복사 → git commit + push → Vercel 자동 재배포.

⚠️ 현재 두 위치가 **수동 동기화** 상태. 자동화하려면 향후 git submodule 또는 동기화 스크립트 추가 필요 (§9 참고).

### 7.3 SKILL.md 수정

`common_source/.claude/skills/feature-spec/SKILL.md` 직접 수정. 본인 사용엔 즉시 반영. 팀원에게 배포하려면 zip 다시 만들어 배포.

---

## 8. 워크스페이스 옵션 (팀원 배포 시)

### 옵션 1. 구글 드라이브 공유 (현재 본인 방식, 추천)
`common_source` 폴더를 팀원과 공유 → 팀원도 Google Drive로 동기화 → 같은 폴더에서 작업.
**장점**: 결과물 자동 동기화. 추가 셋업 0.

### 옵션 2. GitHub Private Repo
`common_source`를 GitHub repo로 만들어 팀원 clone. 수동 push/pull.

### 옵션 3. 빈 워크스페이스 (각자 작업)
팀원이 본인 PC에 빈 폴더 만들어 작업. 결과물 별도 공유.

---

## 9. 향후 작업 거리 (TODO)

### 9.1 가이드 동기화 자동화
현재 `00. Assets/`의 가이드 수정 후 서버 repo로 수동 복사. 다음 중 선택:
- `git submodule`로 가이드만 별도 repo로 분리
- `make sync` 같은 단일 명령으로 자동 복사 + push 자동화 스크립트
- GitHub Actions로 가이드 변경 감지 시 자동 PR

### 9.2 PC variant 추가 ✅ 완료 (2026-05-16)
- ✅ `00. Assets/1-4. SB-WIREFRAME-GUIDE-PC.md` 추가 (diff 형태, §6/§11.2만 PC 사양)
- ✅ 서버 `api/_data/guides/4b-sb-guide-pc.md` 배포 + `sb-pc` mode 추가
- ✅ `fetch_guide.py`에 `sb-mobile`/`sb-pc` choices 추가 (`sb`는 mobile 별칭)
- ✅ `generate_sb.py`의 `--variant pc` 차단 해제 (보일러플레이트 공유, 화면 body의 .wf-canvas 사양만 다름)
- ✅ `SKILL.md` §4에 Variant 결정 단계(Step 0) + PC/모바일 차이 매트릭스 추가
- PC 양식 출력 경로: `01. 공통 기능/{cat}/SB/{기능ID}_PC/` (모바일 폴더와 분리)
- 콘텐츠(컴포넌트 정의, 동작, 예외) 동일성 강제 — 양식만 다름

### 9.3 어드민(ADM-XX) 카테고리 매핑 정리
SKILL.md §2 카테고리 매핑에 ADM-XX 명시적 디렉토리 매핑 추가 필요.

### 9.4 Anthropic API 직결 옵션 (보호 강화)
현재는 LLM 추론을 클라이언트 Claude Code가 함. 더 강한 IP 보호 원하면:
- Vercel function에서 직접 Anthropic API 호출
- 클라이언트는 결과만 수신
- 비용: 월 $50-100 (팀 10명, 100세트 기준)
- 트레이드오프: 가이드 메모리 노출도 차단되지만 API 비용 발생

### 9.5 클라이언트 자동 업데이트
SKILL.md/scripts 변경 시 팀원에게 zip 재배포해야 함. 자동 업데이트 메커니즘 (예: fetch 시 버전 체크) 추가 가능.

### 9.6 팀원별 사용 통계
Vercel 로그에서 각 토큰별 fetch 횟수/시간 분석 가능. 향후 대시보드 만들면 유용.

---

## 10. 트러블슈팅 (자주 만난 이슈들)

### 10.1 base64 PNG 손상
**증상**: SB의 ETRIBE 로고 잘리거나 깨짐
**원인**: Edit 툴이나 다른 편집 과정에서 base64 문자열 일부 변형
**해결**: `generate_sb.py`가 PNG MD5 자동 검증. 손상 시 `templates/sb-logo-data-url.txt` 재생성:
```bash
base64 -i "00. Assets/etribe-logo.png" | tr -d '\n' > templates/sb-logo-data-url.txt
```

### 10.2 Figma에서 Description이 줄별 분리됨
**원인**: `<div class="desc-l1">` 등 div 분리 사용했거나 CSS `::before` 사용
**해결**: §4.2 Description 인라인 구조 원칙 준수 (한 항목 = 하나의 `<p class="desc-block">`)

### 10.3 Figma 임포트 시 볼드 풀림
**원인**: 시스템에 Static Pretendard 미설치
**해결**: https://github.com/orioncactus/pretendard/releases 에서 Static OTF/TTF 설치 후 Figma 재시작

### 10.4 Vercel "commit author email is not valid"
**원인**: git config가 macOS 기본값(`Starry@MacBook-Air.local`)으로 commit됨
**해결**: §5.3 noreply 이메일로 git config 수정 후 commit amend + force push

### 10.5 Python 3.9 호환 에러 (`dict | str`)
**원인**: Vercel runtime이 Python 3.9 또는 3.10
**해결**: type hint에서 `|` syntax 대신 typing 모듈 사용 또는 type hint 제거

---

## 11. 변경 이력

| 날짜 | 내용 |
|------|------|
| 2026-04 | SB 양식 v2 (ETRIBE 표준) 설계 및 샘플 작성 (`C-01-001_etribe.html`) |
| 2026-04 | SB 가이드(`1-4. SB-WIREFRAME-GUIDE.md`) v2로 재작성 |
| 2026-04 | A-01(회원가입) PRD → SB 7개 생성 (검증) |
| 2026-05-09 | feature-spec 스킬 v1 (로컬 가이드 기반) 작성 |
| 2026-05-10 | IP 보호를 위한 서버 분리 (옵션 D 채택) |
| 2026-05-10 | Vercel + GitHub 인프라 셋업 |
| 2026-05-10 | 클라이언트를 thin client로 전환 (가이드 fetch 기반) |
| 2026-05-10 | PRD 모드에 Step 0(프로세스 입력) + Step 2.5(Mermaid 프리뷰) 단계 추가 |
| 2026-05-10 | SKILL.md 슬림화 (12KB → 4.7KB) |
| 2026-05-10 | 팀원 배포 zip(`~/Downloads/feature-spec.zip`) 생성 |
| 2026-05-10 | 인수인계 문서(이 파일) 작성 |
| 2026-05-16 | PC variant 추가 (`4b-sb-guide-pc.md`, `sb-pc` mode, `generate_sb --variant pc`) — 콘텐츠 동일, 양식만 분리 |
| 2026-06-03 | 가이드 §13 «챗봇 컴포넌트 카탈로그»(KRDS 아키타입 12종 + 데이터 주도 렌더 계약) 서버 승격 |
| 2026-06-03 | 챗봇 SB 분기 추가 (SKILL §4.2 + `build_chatbot_sb.py`/`chatbot_to_sb.py`/`chatbot_components.py`) — 인텐트 워크북(xlsx) → SB 자동 생성 |
| 2026-06-28 | 어드민 SB 분기 추가 (SKILL §4.4 + `build_admin_sb.py` + `templates/admin-pulmuone.html`) — PC 고정, 템플릿 선택 → 화면 본문 → PC SB. 첫 화면 주문상세(`samples/admin/`) |
| 2026-06-29 | 어드민 세부기능정의 워크북 분기 추가 (SKILL §5.1 + `parse_admin_spec.py`) — 워크북 → 체크리스트 → PRD(§3) → SB(§4.4), 라벨·규칙·예외 커버리지 기계 검증(--verify) |
| 2026-06-29 | §5.1 간소화 — 산출물 PRD만(SB 별도 요청), 프로세스 입력·Mermaid 프리뷰·체크리스트 질문 등 검토 절차 생략, 미정의 항목은 «(제안)» 표기로 자동 보완 |

---

## 12. 빠른 참조 (Quick Reference)

### 12.1 자주 쓰는 명령어

```bash
# 가이드 fetch 테스트
python3 ".claude/skills/feature-spec/scripts/fetch_guide.py" --mode prd

# zip 재생성 (팀원 배포용)
cd "{common_source}/.claude/skills"
zip -r ~/Downloads/feature-spec.zip feature-spec -x "*.DS_Store" "*__pycache__*" "*.pyc"

# 토큰 생성 (관리자)
python3 -c 'import secrets; print(secrets.token_urlsafe(32))'

# 가이드 수정 후 서버 push
cd ~/projects/etribe-feature-spec-server
git add api/_data/guides/
git commit -m "Update guide: ..."
git push
# → Vercel 자동 재배포 (~30초)
```

### 12.2 자주 보는 파일

| 파일 | 용도 |
|------|------|
| `common_source/.claude/skills/feature-spec/SKILL.md` | Claude가 읽는 스킬 본체 |
| `common_source/.claude/skills/feature-spec/ONBOARDING.md` | 팀원 안내문 |
| `common_source/00. Assets/0. ai-enhanced-workflow.md` | 워크플로우 개요 |
| `common_source/99. Sample/SB/C-01-001_etribe.html` | SB 양식 완성 샘플 |
| `~/projects/etribe-feature-spec-server/api/index.py` | Vercel 함수 본체 |

### 12.3 외부 링크

- **GitHub repo (server)**: https://github.com/starryetribe-droid/etribe-feature-spec-server
- **Vercel 배포**: https://etribe-feature-spec-server.vercel.app
- **Vercel 대시보드**: https://vercel.com/dashboard
- **GitHub 이메일 설정**: https://github.com/settings/emails
- **Anthropic Console** (현재 미사용, 향후 보호 강화 시): https://console.anthropic.com

---

## 13. 다음 담당자에게

1. **이 문서를 먼저 읽으세요**. 특히 §3 아키텍처와 §4 결정사항.
2. **`common_source/.claude/skills/feature-spec/SKILL.md`** 와 **`ONBOARDING.md`** 도 함께 읽으세요.
3. **로컬 셋업**: `~/.etribe/config.json` 작성 (관리자 본인 토큰으로). §6.3 참고.
4. **서버 코드 접근**: GitHub `etribe-feature-spec-server` repo collaborator 권한 받으세요. Vercel 프로젝트도 팀 추가.
5. **첫 시도**: `A-04 로그아웃 PRD 만들어줘`(분기 적은 기능)로 흐름 익히세요.
6. **수정 시**: §4 결정사항을 보고 "왜 그렇게 했는지" 이해한 후 변경.
7. **TODO**: §9에 향후 개선 거리 정리되어 있습니다.

질문은 이 문서의 §10 트러블슈팅 또는 §12 빠른 참조에서 90% 해결됩니다.

행운을 빕니다 🚀

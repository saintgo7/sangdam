# 🎓 상담 관리 시스템 (Python Flask 독립형)

Python Flask를 사용하여 구현한 학생-교수 상담 관리 시스템입니다.

## ✨ 주요 기능

### 👨‍🎓 학생 기능
- 🔐 로그인/로그아웃
- ✏️ 상담 요청 작성 (카테고리, 우선순위 설정)
- 📊 나의 상담 현황 대시보드
- 👀 상담 진행 상태 실시간 확인
- 💬 교수 피드백 확인

### 👨‍🏫 교수 기능  
- 🔐 로그인/로그아웃
- 📋 상담 요청 목록 관리
- 👥 상담 담당 배정
- ✅ 상담 완료 처리
- 💭 학생에게 피드백 제공
- 📈 상담 통계 대시보드

### 🎨 사용자 인터페이스
- 📱 반응형 웹 디자인 (Bootstrap 5)
- 🎯 직관적인 사용자 경험
- 🔄 실시간 상태 업데이트
- 🌈 현대적인 UI/UX 디자인

## 🚀 설치 및 실행

### 1️⃣ 시스템 요구사항
- Python 3.7 이상
- 웹 브라우저 (Chrome, Firefox, Safari, Edge)

### 2️⃣ 빠른 시작
```bash
# 1. 프로젝트 디렉토리로 이동
cd counseling_system_python

# 2. 패키지 설치 (Flask)
pip install flask

# 3. 애플리케이션 실행
python run.py

# 또는 직접 실행
python app.py
```

### 3️⃣ 브라우저에서 접속
- **로컬 접속**: http://localhost:9000
- **네트워크 접속**: http://0.0.0.0:9000

## 👤 테스트 계정

| 역할 | 사용자명 | 비밀번호 | 설명 |
|------|----------|----------|------|
| 🎒 학생 | `student1` | `password123` | 김학생 (20210001) |
| 🎒 학생 | `student2` | `password123` | 이학생 (20210002) |
| 👨‍🏫 교수 | `professor1` | `password123` | 박교수 (공학관 301호) |
| 👨‍🏫 교수 | `professor2` | `password123` | 최교수 (공학관 302호) |

## 📁 프로젝트 구조

```
counseling_system_python/
├── 📄 app.py                    # 메인 애플리케이션
├── 🚀 run.py                    # 실행 스크립트  
├── 📋 requirements.txt          # Python 패키지 목록
├── 📖 README.md                 # 프로젝트 문서
├── 📁 templates/                # HTML 템플릿
│   ├── 🔧 base.html            # 기본 레이아웃
│   ├── 🔐 login.html           # 로그인 페이지
│   ├── 🎓 student_dashboard.html    # 학생 대시보드
│   ├── 👨‍🏫 professor_dashboard.html  # 교수 대시보드
│   ├── ✏️ create_counseling.html    # 상담 요청 작성
│   └── 👀 view_counseling.html      # 상담 상세보기
└── 📁 static/                   # 정적 파일 (비어있음)
```

## 🛠️ 기술 스택

- **Backend**: Python 3.x + Flask 3.0
- **Frontend**: HTML5 + Bootstrap 5 + JavaScript
- **Template Engine**: Jinja2
- **Session Management**: Flask Session
- **Database**: In-Memory Mock Database
- **Icons**: Bootstrap Icons

## 🔧 주요 특징

- ✅ **완전한 Python 구현** - 추가 의존성 최소화
- ✅ **Mock Database** - 별도 DB 설치 불필요
- ✅ **반응형 디자인** - 모바일/태블릿/데스크톱 지원
- ✅ **세션 기반 인증** - 안전한 로그인 시스템
- ✅ **한국어 인터페이스** - 완전한 한국어 지원
- ✅ **실시간 업데이트** - 상담 상태 실시간 반영
- ✅ **독립형 애플리케이션** - 단일 폴더에서 실행

## 📝 사용 시나리오

### 학생의 상담 요청 과정
1. 🔐 로그인 (student1 / password123)
2. ✏️ "새 상담 요청" 버튼 클릭
3. 📝 제목, 내용, 카테고리, 우선순위 입력
4. 📤 상담 요청 제출
5. 📊 대시보드에서 진행 상황 확인

### 교수의 상담 관리 과정
1. 🔐 로그인 (professor1 / password123)
2. 📋 상담 요청 목록 확인
3. 👥 "담당하기" 버튼으로 상담 배정
4. 💭 피드백 작성 후 완료 처리
5. 📈 통계 대시보드 확인

## 🔍 주요 기능 상세

### 상담 요청 관리
- **카테고리별 분류**: 학업, 진로, 학생생활, 연구, 기타
- **우선순위 설정**: 높음(긴급), 보통, 낮음
- **상태 추적**: 대기중 → 진행중 → 완료
- **실시간 알림**: 상태 변화 시 즉시 반영

### 대시보드 통계
- **학생 대시보드**: 내 상담 현황, 카테고리별 분석
- **교수 대시보드**: 전체 상담 통계, 처리 현황
- **실시간 차트**: 상담 상태별 시각화

### 보안 기능
- **세션 기반 인증**: 안전한 로그인 유지
- **역할별 접근 제어**: 학생/교수 권한 분리
- **입력값 검증**: XSS, 인젝션 공격 방지

## 🎯 개발 목표

이 프로젝트는 다음과 같은 목표로 개발되었습니다:

- 📚 **교육적 목적**: Python Flask 학습 및 실습
- 🏫 **실용적 활용**: 실제 대학 환경에서 사용 가능
- 🔧 **확장 가능성**: 추후 기능 추가 용이
- 💻 **기술 시연**: 모던 웹 개발 기술 적용

## 🤝 기여하기

프로젝트 개선을 위한 제안이나 버그 리포트는 언제든지 환영합니다!

## 📄 라이선스

이 프로젝트는 교육 목적으로 제작되었으며, 자유롭게 사용하실 수 있습니다.

---

💡 **문의사항이나 개선 제안이 있으시면 언제든지 연락주세요!**
# 상담 관리 시스템 (Python Flask)

Python Flask를 사용하여 구현한 학생-교수 상담 관리 시스템입니다.

## 기능

- 🔐 로그인/로그아웃 (학생/교수 역할)
- 👨‍🎓 학생 기능:
  - 상담 요청 작성
  - 나의 상담 현황 조회
  - 대시보드 통계
- 👨‍🏫 교수 기능:
  - 상담 요청 목록 조회
  - 상담 담당하기
  - 대시보드 통계

## 설치 및 실행

### 1. 가상환경 생성 (권장)
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 2. 패키지 설치
```bash
pip install -r requirements.txt
```

### 3. 애플리케이션 실행
```bash
python app.py
```

### 4. 브라우저에서 접속
- http://localhost:8000

## 테스트 계정

### 학생 계정
- 아이디: `student1`
- 비밀번호: `password123`

### 교수 계정
- 아이디: `professor1`
- 비밀번호: `password123`

## 기술 스택

- **Backend**: Python Flask
- **Frontend**: Bootstrap 5, Jinja2 Templates
- **Database**: In-Memory Mock Database
- **Session**: Flask Session

## 프로젝트 구조

```
python_app/
├── app.py              # 메인 애플리케이션
├── requirements.txt    # Python 패키지 목록
├── README.md          # 프로젝트 문서
└── templates/         # HTML 템플릿
    ├── base.html      # 기본 템플릿
    ├── login.html     # 로그인 페이지
    ├── student_dashboard.html    # 학생 대시보드
    ├── professor_dashboard.html  # 교수 대시보드
    └── create_counseling.html    # 상담 요청 작성
```

## 주요 특징

- ✅ 완전한 Python 구현
- ✅ Mock Database로 설치 불필요
- ✅ 반응형 웹 디자인
- ✅ 세션 기반 인증
- ✅ 한국어 인터페이스
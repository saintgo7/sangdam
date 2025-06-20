# Academic Management System (학술 관리 시스템)

이 저장소는 교육기관에서 사용할 수 있는 포괄적인 학술 관리 시스템을 포함합니다.

## 🎓 포함된 시스템

### 1. Student Score Management System (학생 성적 관리 시스템)
- **파일**: `student_score_system.py`
- **매뉴얼**: `student_score_system_manual.md`
- **기능**: 학생 정보 관리, 성적 입력, 등급 계산, 보고서 생성

### 2. Professor Administration System (교수 관리 시스템)
- **파일**: `professor_admin.py`
- **매뉴얼**: `professor_admin_manual.md`
- **기능**: 교수 정보 관리, 검색/정렬, CSV 가져오기/내보내기, 통계 분석

## 🚀 주요 특징

### 공통 특징
- **이중 저장 모드**: MongoDB + 로컬 저장소 지원
- **한국어 UI**: 완전한 한국어 인터페이스
- **접근성**: 18pt 볼드 폰트로 가독성 최적화
- **크로스 플랫폼**: Windows, macOS, Linux 지원

### Student Score System 특징
- ✅ 9단계 등급 시스템 (A+, A, B+, B, C+, C, D+, D, F)
- ✅ 3개 과목 지원 (컴퓨터개론, IoT임베디드, 캡스톤디자인)
- ✅ 자동 평균 계산 및 등급 부여
- ✅ 개별/학급별/과목별 보고서
- ✅ CSV 내보내기
- ✅ 실시간 통계 분석

### Professor Admin System 특징
- ✅ 포괄적인 교수 정보 관리
- ✅ 고급 검색 및 필터링
- ✅ CSV 템플릿 다운로드
- ✅ 스마트 CSV 가져오기 (검증 포함)
- ✅ 다양한 보고서 (학과별, 직급별, 연락처)
- ✅ 상세 통계 및 분석

## 📋 시스템 요구사항

```
Python 3.6+
tkinter (보통 Python과 함께 설치됨)
pymongo (MongoDB 사용 시, 선택사항)
```

## 🛠️ 설치 및 실행

### 1. 저장소 클론
```bash
git clone https://github.com/yourusername/academic-management-system.git
cd academic-management-system
```

### 2. 의존성 설치 (MongoDB 사용 시)
```bash
pip install pymongo
```

### 3. 프로그램 실행

#### 학생 성적 관리 시스템
```bash
python student_score_system.py
```

#### 교수 관리 시스템
```bash
python professor_admin.py
```

## 📖 사용법

### Student Score System
1. **학생 관리**: Student Management 탭에서 학생 정보 추가/수정/삭제
2. **성적 입력**: Score Entry 탭에서 과목별 성적 입력
3. **보고서**: Reports 탭에서 다양한 분석 보고서 생성
4. **통계**: Statistics 탭에서 전체 현황 확인

### Professor Admin System
1. **교수 관리**: Professor Management 탭에서 교수 정보 관리
2. **검색/정렬**: Search & Sort 탭에서 조건별 검색
3. **데이터 관리**: Reports 탭에서 CSV 가져오기/내보내기
4. **분석**: Statistics 탭에서 교수 현황 통계

## 🎯 등급 시스템 (Student Score System)

| 등급 | 점수 구간 | 설명 |
|------|-----------|------|
| A+ | 95-100점 | 최우수 |
| A  | 90-94점  | 우수 |
| B+ | 85-89점  | 양호+ |
| B  | 80-84점  | 양호 |
| C+ | 75-79점  | 보통+ |
| C  | 70-74점  | 보통 |
| D+ | 65-69점  | 미흡+ |
| D  | 60-64점  | 미흡 |
| F  | 0-59점   | 부족 |

## 📊 CSV 데이터 형식

### Student Data Export
```csv
Student ID,Name,Class,Major,Introduction to Computers,IoT Emb,Capston Design,Average
20241001,김민수,컴공1반,컴퓨터공학과,92.0,87.0,95.0,91.3
```

### Professor Data Import/Export
```csv
Professor ID,Name,Department,Position,Specialization,Email,Phone,Office
PROF001,Dr. John Smith,Computer Science,Professor,AI/Machine Learning,john@university.edu,555-0123,CS Building 301
```

## 🔧 데이터베이스 설정

### MongoDB 사용 (선택사항)
MongoDB를 사용하면 데이터가 영구적으로 저장됩니다:

```bash
# MongoDB 설치 및 실행
mongod --dbpath /path/to/data
```

MongoDB가 실행되지 않으면 자동으로 로컬 모드로 전환됩니다.

## 📁 파일 구조

```
academic-management-system/
├── student_score_system.py           # 학생 성적 관리 시스템
├── student_score_system_manual.md    # 학생 시스템 매뉴얼
├── professor_admin.py                # 교수 관리 시스템
├── professor_admin_manual.md         # 교수 시스템 매뉴얼
└── README.md                         # 이 파일
```

## 🚨 주의사항

### 로컬 모드 사용 시
- 프로그램 종료 시 데이터가 소실됩니다
- 중요한 데이터는 반드시 CSV로 백업하세요
- MongoDB 연결을 권장합니다

### 데이터 백업
- 정기적으로 CSV 내보내기를 통해 백업
- 학기별/연도별 아카이브 생성 권장

## 🤝 기여하기

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 `LICENSE` 파일을 참조하세요.

## 📞 지원

문제가 발생하거나 문의사항이 있으시면 Issues 탭에서 문의해주세요.

## 🔄 업데이트 로그

### v1.0 (2024)
- 초기 릴리스
- 학생 성적 관리 시스템
- 교수 관리 시스템
- 완전한 한국어 매뉴얼

---

**Made with ❤️ for Educational Institutions**
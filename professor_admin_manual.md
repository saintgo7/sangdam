# 교수 관리 시스템 사용자 매뉴얼

## 목차
1. [시스템 개요](#시스템-개요)
2. [시작하기](#시작하기)
3. [기능별 사용 방법](#기능별-사용-방법)
4. [CSV 데이터 관리](#csv-데이터-관리)
5. [보고서 생성](#보고서-생성)
6. [문제 해결](#문제-해결)

---

## 시스템 개요

### 주요 기능
- **교수 정보 관리**: 교수 추가, 수정, 삭제
- **검색 및 정렬**: 다양한 조건으로 교수 검색 및 정렬
- **CSV 가져오기/내보내기**: 대용량 데이터 일괄 처리
- **보고서 생성**: 학과별, 직급별 보고서 자동 생성
- **통계 분석**: 교수 현황 통계 및 분석

### 시스템 요구사항
- Python 3.6 이상
- tkinter (GUI 라이브러리)
- MongoDB (선택사항 - 없어도 로컬 저장소로 동작)

---

## 시작하기

### 1. 프로그램 실행
```bash
python professor_admin.py
```

### 2. 화면 구성
프로그램이 시작되면 1024x768 크기의 창이 열리며, 다음 4개의 탭으로 구성됩니다:

- **Professor Management**: 교수 정보 관리
- **Search & Sort**: 검색 및 정렬
- **Reports**: 보고서 생성 및 CSV 관리
- **Statistics**: 통계 정보

### 3. 데이터베이스 연결 상태
화면 우상단에 연결 상태가 표시됩니다:
- **녹색 "Database Connected"**: MongoDB 연결됨
- **주황색 "Local Storage"**: 로컬 저장소 사용 중

---

## 기능별 사용 방법

### Professor Management 탭

#### 교수 추가하기
1. **필수 입력 필드**:
   - Professor ID: 고유 식별번호 (예: PROF001)
   - Name: 교수 이름
   - Department: 학과 (드롭다운에서 선택)
   - Position: 직급 (드롭다운에서 선택)

2. **선택 입력 필드**:
   - Email: 이메일 주소
   - Phone: 전화번호
   - Specialization: 전문 분야
   - Office: 연구실 위치

3. **추가 절차**:
   - 모든 필수 필드 입력
   - "Add Professor" 버튼 클릭
   - 성공 메시지 확인

#### 교수 정보 수정하기
1. 교수 목록에서 수정할 교수 클릭
2. 입력 필드에 자동으로 정보가 채워짐
3. 필요한 정보 수정
4. "Update Professor" 버튼 클릭

#### 교수 삭제하기
1. 삭제할 교수의 ID를 입력하거나 목록에서 선택
2. "Delete Professor" 버튼 클릭
3. 확인 대화상자에서 "예" 선택

#### 입력 필드 초기화
- "Clear Fields" 버튼을 클릭하면 모든 입력 필드가 초기화됩니다.

### Search & Sort 탭

#### 이름으로 검색
- "Search by Name" 필드에 교수 이름 입력
- 실시간으로 검색 결과가 하단에 표시됩니다

#### 학과별 필터링
1. "Filter by Department" 드롭다운 클릭
2. 원하는 학과 선택 (전체 보기는 "All" 선택)
3. 자동으로 필터링된 결과 표시

#### 직급별 필터링
1. "Filter by Position" 드롭다운 클릭
2. 원하는 직급 선택
3. 자동으로 필터링된 결과 표시

#### 정렬 기능
1. "Sort by" 드롭다운에서 정렬 기준 선택:
   - Name: 이름순
   - Department: 학과순
   - Position: 직급순
   - ID: 교수번호순
2. 자동으로 정렬된 결과 표시

#### 필터 초기화
- "Clear Filters" 버튼을 클릭하면 모든 검색 조건이 초기화됩니다

---

## CSV 데이터 관리

### CSV 템플릿 다운로드

#### 1. 템플릿 다운로드 방법
1. **Reports** 탭으로 이동
2. **Import Data** 섹션에서 "Download CSV Template" 버튼 클릭
3. 저장할 위치와 파일명 지정 (기본: professor_template.csv)
4. 저장 완료

#### 2. 템플릿 구조
```csv
Professor ID,Name,Department,Position,Specialization,Email,Phone,Office
PROF001,Dr. John Smith,Computer Science,Professor,AI/Machine Learning,john.smith@university.edu,555-0123,CS Building 301
PROF002,Dr. Jane Doe,Mathematics,Associate Professor,Statistics,jane.doe@university.edu,555-0124,Math Building 205
```

### CSV 파일 준비

#### 1. 필수 컬럼 (반드시 포함)
- **Professor ID**: 고유 식별번호
- **Name**: 교수 이름
- **Department**: 학과명
- **Position**: 직급

#### 2. 선택 컬럼
- **Specialization**: 전문분야
- **Email**: 이메일 주소
- **Phone**: 전화번호
- **Office**: 연구실 위치

#### 3. 파일 형식 주의사항
- 파일 인코딩: UTF-8
- 첫 번째 행: 컬럼 헤더 (있어도 되고 없어도 됨)
- 빈 행은 자동으로 무시됨
- 필수 컬럼이 비어있는 행은 오류로 처리

### CSV 데이터 가져오기

#### 1. 가져오기 절차
1. **Reports** 탭으로 이동
2. "Import from CSV" 버튼 클릭
3. CSV 파일 선택
4. 데이터 검증 결과 확인
5. 가져오기 확인 대화상자에서 "예" 선택

#### 2. 데이터 검증 과정
시스템이 자동으로 다음 사항들을 검사합니다:

**✅ 유효성 검사**
- 필수 필드 누락 확인
- 중복 ID 확인 (파일 내 및 기존 데이터베이스와)
- 데이터 형식 검증

**⚠️ 오류 처리**
- 유효하지 않은 행의 행 번호와 오류 내용 표시
- 중복 ID 목록 표시
- 가져올 수 있는 유효한 데이터 개수 표시

#### 3. 검증 결과 해석
```
CSV Import Validation Results:

Valid records found: 25        ← 가져올 수 있는 데이터 수
Invalid rows: 3               ← 오류가 있는 행 수
Duplicate IDs: 2              ← 중복 ID 수

Invalid Rows:
  - Row 5: Missing required fields (ID, Name, Department, Position)
  - Row 12: Missing required fields (ID, Name, Department, Position)

Duplicate IDs:
  - Row 8: Professor ID 'PROF001' already exists in database
```

#### 4. 새로운 학과/직급 처리
가져오는 데이터에 기존 시스템에 없는 학과나 직급이 있을 경우:
- 시스템이 자동으로 확인 대화상자 표시
- "예"를 선택하면 새로운 학과/직급이 시스템에 추가됨
- "아니오"를 선택하면 해당 데이터는 가져오지 않음

### CSV 데이터 내보내기

#### 1. 내보내기 방법
1. **Reports** 탭으로 이동
2. "Export to CSV" 버튼 클릭
3. 저장할 위치와 파일명 지정
4. 저장 완료

#### 2. 내보내기 파일 구조
모든 교수 데이터가 다음 형식으로 저장됩니다:
```csv
Professor ID,Name,Department,Position,Specialization,Email,Phone,Office
PROF001,Dr. Kim Min-soo,Computer Science,Professor,AI/Machine Learning,kim@university.edu,02-1234-5678,IT Building 301
```

---

## 보고서 생성

### 학과별 보고서 (Department Report)

#### 1. 생성 방법
1. **Reports** 탭으로 이동
2. "Department Report" 버튼 클릭
3. 하단 텍스트 영역에 보고서 표시

#### 2. 보고서 내용
- 학과별 교수 총 인원수
- 각 학과 내 직급별 분포
- 교수별 상세 정보 (이름, ID, 연구실)

```
DEPARTMENT REPORT
==================================================

DEPARTMENT: Computer Science
------------------------------
Total Professors: 15

  Professor: 5
    - Dr. Kim Min-soo (ID: PROF001)
      Office: IT Building 301
    - Dr. Lee Su-jin (ID: PROF002)
      Office: IT Building 302

  Associate Professor: 7
    - Dr. Park Ji-hoon (ID: PROF003)
      Office: IT Building 201
```

### 직급별 보고서 (Position Report)

#### 1. 생성 방법
1. **Reports** 탭으로 이동
2. "Position Report" 버튼 클릭

#### 2. 보고서 내용
- 직급별 교수 총 인원수
- 각 직급 내 학과별 분포
- 교수별 연락처 정보

### 연락처 목록 (Contact List)

#### 1. 생성 방법
1. **Reports** 탭으로 이동
2. "Contact List" 버튼 클릭

#### 2. 보고서 내용
- 모든 교수의 완전한 연락처 정보
- 이름순 정렬
- 이메일, 전화번호, 연구실 위치 포함

---

## 통계 정보

### Statistics 탭 사용법

#### 1. 통계 조회
1. **Statistics** 탭으로 이동
2. "Refresh Statistics" 버튼 클릭 (최신 정보 업데이트)

#### 2. 제공되는 통계 정보

**📊 기본 통계**
- 전체 교수 수

**🏢 학과별 분포**
- 각 학과의 교수 수와 비율

**👥 직급별 분포**
- 각 직급의 교수 수와 비율

**🔬 전문분야별 분포**
- 전문분야별 교수 수와 비율

**📞 연락처 정보 완성도**
- 이메일 주소 입력 비율
- 전화번호 입력 비율
- 연구실 위치 입력 비율

#### 3. 통계 해석 예시
```
PROFESSOR SYSTEM STATISTICS
========================================

Total Professors: 45

DEPARTMENT DISTRIBUTION:
  Computer Science: 15 (33.3%)
  Mathematics: 12 (26.7%)
  Physics: 10 (22.2%)
  Chemistry: 8 (17.8%)

POSITION DISTRIBUTION:
  Professor: 18 (40.0%)
  Associate Professor: 15 (33.3%)
  Assistant Professor: 12 (26.7%)

CONTACT INFORMATION COMPLETENESS:
  Email addresses: 43/45 (95.6%)
  Phone numbers: 38/45 (84.4%)
  Office locations: 41/45 (91.1%)
```

---

## 문제 해결

### 자주 발생하는 문제

#### 1. 교수 ID 중복 오류
**문제**: "Professor ID already exists" 메시지
**해결**: 
- 고유한 교수 ID 사용
- 기존 교수 정보 수정이 목적이라면 "Update Professor" 기능 사용

#### 2. 필수 필드 누락 오류
**문제**: "Please fill required fields" 메시지
**해결**: Professor ID, Name, Department, Position 필드 모두 입력

#### 3. CSV 가져오기 실패
**문제**: CSV 파일을 읽을 수 없음
**해결**: 
- 파일 인코딩을 UTF-8로 저장
- CSV 형식이 올바른지 확인
- 템플릿 파일과 형식 비교

#### 4. 데이터베이스 연결 문제
**문제**: MongoDB 연결 실패
**해결**: 
- MongoDB 서비스 실행 상태 확인
- 로컬 저장소 모드로 자동 전환됨 (데이터는 프로그램 메모리에 저장)

### 데이터 백업 방법

#### 1. CSV 내보내기로 백업
1. 모든 데이터를 CSV로 내보내기
2. 안전한 위치에 파일 저장
3. 정기적으로 백업 업데이트

#### 2. MongoDB 백업 (고급 사용자)
```bash
mongodump --db professor_admin_db --out backup_folder
```

### 성능 최적화

#### 1. 대용량 데이터 처리
- 한 번에 너무 많은 데이터(1000개 이상) 가져오기 시 시간이 오래 걸릴 수 있음
- 데이터를 여러 파일로 나누어 가져오기 권장

#### 2. 검색 성능 향상
- 정확한 검색어 사용
- 불필요한 필터 조건 제거

---

## 추가 팁

### 효율적인 사용을 위한 권장사항

#### 1. 데이터 입력 시
- 일관된 형식으로 데이터 입력 (예: 전화번호 형식 통일)
- 약어보다는 정식 명칭 사용
- 정기적으로 데이터 정확성 검토

#### 2. CSV 파일 관리
- 템플릿 파일을 기본으로 활용
- 대용량 데이터는 Excel에서 편집 후 CSV로 저장
- 가져오기 전 항상 백업 생성

#### 3. 보고서 활용
- 정기적으로 통계 보고서 생성하여 현황 파악
- 필요에 따라 보고서를 PDF로 출력하여 보관
- 학기별/연도별 비교 분석 자료로 활용

#### 4. 시스템 유지관리
- 주기적으로 데이터 백업
- 불필요한 중복 데이터 정리
- 연락처 정보 정확성 주기적 확인

---

## 기술 지원

### 문의사항이 있을 때
1. 매뉴얼을 먼저 확인
2. 오류 메시지의 정확한 내용 기록
3. 문제 발생 시의 상황 정리
4. 시스템 관리자에게 문의

### 업데이트 정보
- 새로운 기능 추가 시 매뉴얼 업데이트
- 버그 수정 및 개선사항 반영
- 사용자 피드백 기반 기능 개선

---

*이 매뉴얼은 교수 관리 시스템 v1.0을 기준으로 작성되었습니다.*
*최종 업데이트: 2024년*
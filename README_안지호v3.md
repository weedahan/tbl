# 성적 분석 모듈 (안지호 파트)

## 개요
대학생 성적 데이터를 분석하여 전공별 평균, 표준편차, 상위권 학생 분류, 학점 분포 등의 통계 정보를 제공하는 모듈입니다.

## 주요 기능
1. 전공별 평균 점수 계산
2. 전공별 표준편차 계산
3. 전공별 상위권 학생 자동 분류
4. 전체 석차 계산
5. 학점 분포 분석 (A+, A, B+, B, ...)
6. 점수 범위별 분포 분석
7. 종합 분석 리포트 출력

---

## 파일 구조
```
grade_analyzer.py       # 메인 분석 모듈
README.md              # 이 문서
```

---

## 클래스 구조

### `GradeAnalyzer` 클래스

#### 초기화
```python
analyzer = GradeAnalyzer(student_data)
```

**입력 데이터 형식:**
```python
student_data = [
    {
        '학번': '20250001',
        '이름': '김민지',
        '전공': '컴퓨터공학',
        '점수': 92,
        '학점': 'A'
    },
    # ... 더 많은 학생 데이터
]
```

---

## 메서드 상세 설명

### 1. 전공 정보

#### `get_all_majors() -> List[str]`
모든 전공 목록을 추출합니다.

**반환값:**
- List[str]: 전공 목록 (정렬됨)

**사용 예시:**
```python
majors = analyzer.get_all_majors()
print(f"전공 목록: {majors}")  # 출력: ['건축학', '경영학', '컴퓨터공학', ...]
```

---

### 2. 평균 계산

#### `calculate_major_average(major: str) -> float`
특정 전공의 평균 점수를 계산합니다.

**매개변수:**
- `major` (str): 전공명

**반환값:**
- float: 해당 전공의 평균 점수 (소수점 둘째 자리까지)

**사용 예시:**
```python
cs_avg = analyzer.calculate_major_average('컴퓨터공학')
print(f"컴퓨터공학 평균: {cs_avg}점")  # 출력: 컴퓨터공학 평균: 86.5점
```

---

#### `calculate_all_major_averages() -> Dict[str, float]`
모든 전공의 평균을 한 번에 계산합니다.

**반환값:**
- Dict[str, float]: 전공명을 키로, 평균을 값으로 하는 딕셔너리

**사용 예시:**
```python
averages = analyzer.calculate_all_major_averages()
# 결과: {'컴퓨터공학': 86.5, '기계공학': 82.3, ...}

for major, avg in averages.items():
    print(f"{major}: {avg}점")
```

---

#### `calculate_overall_average() -> float`
전체 학생의 평균 점수를 계산합니다.

**사용 예시:**
```python
overall_avg = analyzer.calculate_overall_average()
print(f"전체 평균: {overall_avg}점")
```

---

### 3. 표준편차 계산

#### `calculate_major_stdev(major: str) -> float`
특정 전공의 표준편차를 계산합니다.

**매개변수:**
- `major` (str): 전공명

**반환값:**
- float: 해당 전공의 표준편차 (소수점 둘째 자리까지)

**참고:** 표준편차는 점수의 분산 정도를 나타냅니다. 값이 클수록 학생들 간 점수 차이가 큽니다.

---

#### `calculate_all_major_stdevs() -> Dict[str, float]`
모든 전공의 표준편차를 계산합니다.

**반환값:**
- Dict[str, float]: 전공별 표준편차 딕셔너리

---

#### `calculate_overall_stdev() -> float`
전체 학생의 표준편차를 계산합니다.

---

### 4. 상위권 학생 분류

#### `get_top_students_by_major(major: str, top_percent: int = 30) -> List[Dict]`
특정 전공의 상위권 학생을 추출합니다.

**매개변수:**
- `major` (str): 전공명
- `top_percent` (int): 추출할 상위 퍼센트 (기본값: 30)

**반환값:**
- List[Dict]: 상위권 학생 정보 리스트 (점수 높은 순 정렬)

**반환 데이터 형식:**
```python
[
    {
        '학번': '20250004',
        '이름': '최지수',
        '전공': '인공지능',
        '점수': 97,
        '학점': 'A+'
    },
    # ...
]
```

**사용 예시:**
```python
# 컴퓨터공학 상위 20% 학생 추출
top_cs = analyzer.get_top_students_by_major('컴퓨터공학', 20)

for i, student in enumerate(top_cs, 1):
    print(f"{i}등: {student['이름']} - {student['점수']}점 ({student['학점']})")
```

---

#### `get_all_top_students(top_percent: int = 30) -> Dict[str, List[Dict]]`
모든 전공의 상위권 학생을 추출합니다.

**반환값:**
- Dict[str, List[Dict]]: 전공별 상위권 학생 정보

**사용 예시:**
```python
all_top = analyzer.get_all_top_students(30)

for major, students in all_top.items():
    print(f"\n{major} 상위 30%:")
    for student in students:
        print(f"  - {student['이름']}: {student['점수']}점 ({student['학점']})")
```

---

### 5. 전체 석차

#### `get_overall_rankings(limit: int = 10) -> List[Dict]`
전공 무관 전체 학생 석차를 계산합니다.

**매개변수:**
- `limit` (int): 상위 몇 명까지 반환할지 (기본값: 10)

**반환값:**
- List[Dict]: 상위권 학생 리스트 (점수 높은 순)

**사용 예시:**
```python
rankings = analyzer.get_overall_rankings(10)

# 상위 10명 출력
for i, student in enumerate(rankings, 1):
    print(f"{i}위: {student['이름']} ({student['전공']}) - {student['점수']}점")
```

---

### 6. 학점 및 점수 분포

#### `get_grade_distribution(major: str = None) -> Dict[str, int]`
학점별 학생 수를 계산합니다.

**매개변수:**
- `major` (str, optional): 특정 전공 (None이면 전체)

**반환값:**
- Dict[str, int]: 학점별 학생 수

**사용 예시:**
```python
# 전체 학점 분포
grade_dist = analyzer.get_grade_distribution()
# 결과: {'A': 5, 'A+': 3, 'B': 8, 'B+': 6, ...}

# 컴퓨터공학만
cs_grade_dist = analyzer.get_grade_distribution('컴퓨터공학')

for grade, count in grade_dist.items():
    print(f"{grade}: {count}명")
```

---

#### `get_score_distribution_by_range(major: str = None) -> Dict[str, int]`
점수 범위별 분포를 계산합니다.

**범위 기준:**
- A급(90+): 90점 이상
- B급(80-89): 80~89점
- C급(70-79): 70~79점
- D급(60-69): 60~69점
- F급(60미만): 60점 미만

**매개변수:**
- `major` (str, optional): 특정 전공 (None이면 전체)

**반환값:**
- Dict[str, int]: 범위별 학생 수

**사용 예시:**
```python
# 전체 점수 분포
score_dist = analyzer.get_score_distribution_by_range()
# 결과: {'A급(90+)': 10, 'B급(80-89)': 15, ...}

for range_name, count in score_dist.items():
    print(f"{range_name}: {count}명")
```

---

### 7. 기타 조회 기능

#### `get_students_by_major(major: str) -> List[Dict]`
특정 전공의 모든 학생 정보를 조회합니다.

**사용 예시:**
```python
cs_students = analyzer.get_students_by_major('컴퓨터공학')
print(f"컴퓨터공학 학생 수: {len(cs_students)}명")
```

---

### 8. 종합 리포트

#### `print_analysis_report()`
모든 분석 결과를 보기 좋게 출력합니다.

**포함 내용:**
1. 전체 통계 (총 학생 수, 전체 평균, 전체 표준편차)
2. 전공별 평균 점수
3. 전공별 표준편차
4. 전체 학점 분포
5. 전공별 상위 30% 학생 (각 전공당 상위 3명)
6. 전체 석차 TOP 10

**사용 예시:**
```python
analyzer.print_analysis_report()
```

**출력 예시:**
```
======================================================================
대학생 성적 분석 리포트
======================================================================

[전체 통계]
  총 학생 수: 32명
  전체 평균: 84.5점
  전체 표준편차: 9.2

[전공별 평균 점수]
  인공지능: 96.0점
  컴퓨터공학: 92.0점
  ...

[전공별 표준편차]
  건축학: 8.5
  경영학: 7.3
  ...

[전체 학점 분포]
  A: 8명
  A+: 5명
  B: 10명
  ...

[전공별 상위 30% 학생]

  컴퓨터공학
    1. 김민지 (20250001) - 92점 (A)
    ...

[전체 석차 TOP 10]
  1위. 최지수 (20250004) - 인공지능 - 97점 (A+)
  ...
======================================================================
```

---

## 다른 모듈과의 연동

### 데이터 입력 모듈과 연동
```python
# 데이터 입력 함수 사용
from data_input import load_student_data  # 가정

# 데이터 불러오기 (CSV, Excel 등)
student_data = load_student_data('students.csv')

# 분석기 생성
analyzer = GradeAnalyzer(student_data)

# 분석 실행
analyzer.print_analysis_report()
```

### 그래프 시각화 모듈과 연동
```python
# 분석 결과를 그래프 모듈에 전달
from graph_visualizer import plot_grades  # 가정

# 전공별 평균 데이터 추출
averages = analyzer.calculate_all_major_averages()

# 그래프로 시각화
plot_grades(averages, title="전공별 평균 점수")

# 학점 분포 시각화
grade_dist = analyzer.get_grade_distribution()
plot_distribution(grade_dist, title="전체 학점 분포")
```

### 시스템 통합 시
```python
class GradeSystem:
    def __init__(self):
        self.data_manager = DataManager()      # 데이터 입력 모듈
        self.analyzer = None                   # 안지호 분석 모듈
        self.visualizer = Visualizer()         # 시각화 모듈
    
    def run_analysis(self):
        # 데이터 로드
        data = self.data_manager.load_data()
        
        # 분석 실행
        self.analyzer = GradeAnalyzer(data)
        
        # 전공별 평균
        major_averages = self.analyzer.calculate_all_major_averages()
        
        # 전체 석차
        rankings = self.analyzer.get_overall_rankings(10)
        
        # 시각화
        self.visualizer.plot_major_comparison(major_averages)
        self.visualizer.plot_grade_distribution(
            self.analyzer.get_grade_distribution()
        )
        
        # 리포트 출력
        self.analyzer.print_analysis_report()
```

---

## 의존성
```python
import statistics  # Python 표준 라이브러리
from typing import List, Dict, Tuple  # Python 표준 라이브러리
```

**추가 설치 필요 없음** - 모두 Python 기본 내장 라이브러리입니다.

---

## 테스트 방법

### 1. 단독 테스트
파일을 직접 실행하면 샘플 데이터로 테스트할 수 있습니다.

```bash
python grade_analyzer.py
```

### 2. 커스텀 데이터 테스트
```python
# 자신의 데이터로 테스트
my_data = [
    {'학번': '20250001', '이름': '홍길동', '전공': '컴퓨터공학', 
     '점수': 88, '학점': 'A'},
    {'학번': '20250002', '이름': '김철수', '전공': '경영학', 
     '점수': 92, '학점': 'A'},
    # ... 더 많은 데이터
]

analyzer = GradeAnalyzer(my_data)
analyzer.print_analysis_report()
```

---

## 주의사항

1. **데이터 형식**: 입력 데이터는 반드시 위에 명시된 형식을 따라야 합니다.
2. **필수 키**: '학번', '이름', '전공', '점수', '학점' 모두 정확히 일치해야 합니다.
3. **최소 데이터**: 표준편차 계산을 위해 전공당 최소 2명 이상의 학생 데이터가 필요합니다.
4. **학번 형식**: 문자열로 저장 (예: '20250001')
5. **점수 범위**: 0~100점 사이의 숫자
6. **학점**: 'A+', 'A', 'B+', 'B', 'C+', 'C', 'D+', 'D', 'F' 등

---

## 문제 해결

### Q: "KeyError: '전공'" 에러가 발생해요
**A:** 입력 데이터에 '전공' 키가 없거나, 철자가 다릅니다. 키 이름을 정확히 확인하세요.

### Q: 표준편차가 0.0으로 나와요
**A:** 해당 전공의 학생 수가 1명이거나 모든 학생의 점수가 동일할 때 발생합니다.

### Q: 상위권 학생이 너무 많이/적게 나와요
**A:** `top_percent` 매개변수를 조정하세요. (예: 10, 20, 50 등)

### Q: 특정 전공의 데이터가 없다고 나와요
**A:** 해당 전공의 학생이 데이터에 없거나, 전공명 철자가 다를 수 있습니다. `get_all_majors()`로 전공 목록을 확인하세요.
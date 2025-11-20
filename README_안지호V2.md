# 성적 분석 모듈 (안지호 파트)

## 개요
학생들의 성적 데이터를 분석하여 평균, 표준편차, 상위권 학생 분류 등의 통계 정보를 제공하는 모듈입니다.

## 주요 기능
1. 과목별 평균 계산
2. 과목별 표준편차 계산
3. 과목별 상위권 학생 자동 분류
4. 학생별 총점/평균 및 전체 석차 계산
5. 과목별 점수 분포 (A~F 등급)
6. 종합 분석 리포트 출력

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
        '학년': 3,
        '반': 1,
        '번호': 1,
        '이름': '김민지',
        '국어': 92,
        '영어': 88,
        '수학': 95,
        '과학': 90,
        '사회': 87
    },
    # ... 더 많은 학생 데이터
]
```

---

## 메서드 상세 설명

### 1. 평균 계산

#### `calculate_subject_average(subject: str) -> float`
특정 과목의 평균을 계산합니다.

**매개변수:**
- `subject` (str): 과목명 ('국어', '영어', '수학', '과학', '사회')

**반환값:**
- float: 해당 과목의 평균 (소수점 둘째 자리까지)

**사용 예시:**
```python
korean_avg = analyzer.calculate_subject_average('국어')
print(f"국어 평균: {korean_avg}점")  # 출력: 국어 평균: 86.4점
```

---

#### `calculate_all_averages() -> Dict[str, float]`
모든 과목의 평균을 한 번에 계산합니다.

**반환값:**
- Dict[str, float]: 과목명을 키로, 평균을 값으로 하는 딕셔너리

**사용 예시:**
```python
averages = analyzer.calculate_all_averages()
# 결과: {'국어': 86.4, '영어': 84.0, '수학': 89.2, ...}

for subject, avg in averages.items():
    print(f"{subject}: {avg}점")
```

---

### 2. 표준편차 계산

#### `calculate_subject_stdev(subject: str) -> float`
특정 과목의 표준편차를 계산합니다.

**매개변수:**
- `subject` (str): 과목명

**반환값:**
- float: 해당 과목의 표준편차 (소수점 둘째 자리까지)

**참고:** 표준편차는 점수의 분산 정도를 나타냅니다. 값이 클수록 학생들 간 점수 차이가 큽니다.

---

#### `calculate_all_stdevs() -> Dict[str, float]`
모든 과목의 표준편차를 계산합니다.

**반환값:**
- Dict[str, float]: 과목별 표준편차 딕셔너리

---

### 3. 상위권 학생 분류

#### `get_top_students_by_subject(subject: str, top_percent: int = 30) -> List[Dict]`
특정 과목의 상위권 학생을 추출합니다.

**매개변수:**
- `subject` (str): 과목명
- `top_percent` (int): 추출할 상위 퍼센트 (기본값: 30)

**반환값:**
- List[Dict]: 상위권 학생 정보 리스트 (점수 높은 순 정렬)

**반환 데이터 형식:**
```python
[
    {
        '이름': '최지수',
        '학년': 3,
        '반': 1,
        '번호': 4,
        '점수': 98
    },
    # ...
]
```

**사용 예시:**
```python
# 수학 상위 20% 학생 추출
top_math_students = analyzer.get_top_students_by_subject('수학', 20)

for i, student in enumerate(top_math_students, 1):
    print(f"{i}등: {student['이름']} - {student['점수']}점")
```

---

#### `get_all_top_students(top_percent: int = 30) -> Dict[str, List[Dict]]`
모든 과목의 상위권 학생을 추출합니다.

**반환값:**
- Dict[str, List[Dict]]: 과목별 상위권 학생 정보

**사용 예시:**
```python
all_top = analyzer.get_all_top_students(30)

for subject, students in all_top.items():
    print(f"\n{subject} 상위 30%:")
    for student in students:
        print(f"  - {student['이름']}: {student['점수']}점")
```

---

### 4. 학생별 총점/평균

#### `calculate_student_total_and_average() -> List[Dict]`
각 학생의 총점과 평균을 계산하고 석차순으로 정렬합니다.

**반환값:**
- List[Dict]: 학생별 총점/평균 정보 (총점 높은 순)

**반환 데이터 형식:**
```python
[
    {
        '이름': '최지수',
        '학년': 3,
        '반': 1,
        '번호': 4,
        '총점': 480,
        '평균': 96.0
    },
    # ...
]
```

**사용 예시:**
```python
rankings = analyzer.calculate_student_total_and_average()

# 상위 10명 출력
for i, student in enumerate(rankings[:10], 1):
    print(f"{i}위: {student['이름']} - 총점 {student['총점']}점, 평균 {student['평균']}점")
```

---

### 5. 점수 분포

#### `get_score_distribution(subject: str) -> Dict[str, int]`
특정 과목의 점수 분포를 A~F 등급으로 분류합니다.

**등급 기준:**
- A: 90점 이상
- B: 80~89점
- C: 70~79점
- D: 60~69점
- F: 60점 미만

**반환값:**
- Dict[str, int]: 등급별 학생 수

**사용 예시:**
```python
distribution = analyzer.get_score_distribution('수학')
# 결과: {'A': 5, 'B': 8, 'C': 10, 'D': 4, 'F': 2}

for grade, count in distribution.items():
    print(f"{grade}등급: {count}명")
```

---

### 6. 종합 리포트

#### `print_analysis_report()`
모든 분석 결과를 보기 좋게 출력합니다.

**포함 내용:**
1. 과목별 평균
2. 과목별 표준편차
3. 과목별 상위 30% 학생
4. 전체 석차 TOP 10

**사용 예시:**
```python
analyzer.print_analysis_report()
```

**출력 예시:**
```
============================================================
 성적 분석 리포트
============================================================

[과목별 평균]
  국어: 86.4점
  영어: 84.0점
  수학: 89.2점
  ...

[과목별 표준편차]
  국어: 8.5
  영어: 7.8
  ...

[과목별 상위 30% 학생]

   국어
    1. 최지수 (3학년 1반 4번) - 97점
    2. 윤민혁 (3학년 1반 7번) - 95점
    ...

[전체 석차 TOP 10]
  1위. 최지수 (3학년 1반) - 총점: 480점, 평균: 96.0점
  ...
============================================================
```

---

## 다른 모듈과의 연동

### 데이터 입력 모듈과 연동
```python
# 데이터 입력 함수 사용
from data_input import load_student_data  # 가정

# 데이터 불러오기
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

# 평균 데이터 추출
averages = analyzer.calculate_all_averages()

# 그래프로 시각화
plot_grades(averages)
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
        results = self.analyzer.calculate_all_averages()
        
        # 시각화
        self.visualizer.plot(results)
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
    {'학년': 3, '반': 1, '번호': 1, '이름': '홍길동', 
     '국어': 85, '영어': 90, '수학': 88, '과학': 92, '사회': 87},
    # ... 더 많은 데이터
]

analyzer = GradeAnalyzer(my_data)
analyzer.print_analysis_report()
```

---

## 주의

1. **데이터 형식**: 입력 데이터는 반드시 위에 명시된 형식을 따라야 합니다.
2. **과목명**: '국어', '영어', '수학', '과학', '사회' 정확히 일치해야 합니다.
3. **최소 데이터**: 표준편차 계산을 위해 최소 2명 이상의 학생 데이터가 필요합니다.

---

## 문제 해결

### Q: "KeyError: '국어'" 에러가 발생해요
**A:** 입력 데이터에 '국어' 키가 없거나, 철자가 다릅니다. 과목명을 정확히 확인하세요.

### Q: 표준편차가 0.0으로 나와요
**A:** 학생 수가 1명이거나 모든 학생의 점수가 동일할 때 발생합니다.

### Q: 상위권 학생이 너무 많이/적게 나와요
**A:** `top_percent` 매개변수를 조정하세요. (예: 10, 20, 50 등)
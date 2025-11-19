import statistics
from typing import List, Dict, Tuple

class GradeAnalyzer:
    """
    성적 데이터 분석 모듈
    - 평균, 표준편차 계산
    - 상위권 학생 분류
    """
    
    def __init__(self, student_data: List[Dict]):
        """
        Args:
            student_data: 학생 데이터 리스트
            예: [{'학년': 3, '반': 1, '번호': 1, '이름': '김민지', 
                  '국어': 92, '영어': 88, '수학': 95, '과학': 90, '사회': 87}, ...]
        """
        self.student_data = student_data
        self.subjects = ['국어', '영어', '수학', '과학', '사회']
    
    def calculate_subject_average(self, subject: str) -> float:
        """특정 과목의 평균 계산"""
        scores = [student[subject] for student in self.student_data if subject in student]
        if not scores:
            return 0.0
        return round(statistics.mean(scores), 2)
    
    def calculate_all_averages(self) -> Dict[str, float]:
        """모든 과목의 평균 계산"""
        averages = {}
        for subject in self.subjects:
            averages[subject] = self.calculate_subject_average(subject)
        return averages
    
    def calculate_subject_stdev(self, subject: str) -> float:
        """특정 과목의 표준편차 계산"""
        scores = [student[subject] for student in self.student_data if subject in student]
        if len(scores) < 2:
            return 0.0
        return round(statistics.stdev(scores), 2)
    
    def calculate_all_stdevs(self) -> Dict[str, float]:
        """모든 과목의 표준편차 계산"""
        stdevs = {}
        for subject in self.subjects:
            stdevs[subject] = self.calculate_subject_stdev(subject)
        return stdevs
    
    def get_top_students_by_subject(self, subject: str, top_percent: int = 30) -> List[Dict]:
        """
        특정 과목의 상위권 학생 분류
        
        Args:
            subject: 과목명
            top_percent: 상위 몇 퍼센트를 추출할지 (기본값: 30%)
        
        Returns:
            상위권 학생 리스트 (점수 높은 순으로 정렬)
        """
        # 해당 과목 점수로 정렬
        sorted_students = sorted(
            self.student_data, 
            key=lambda x: x.get(subject, 0), 
            reverse=True
        )
        
        # 상위 n% 계산
        top_count = max(1, int(len(sorted_students) * top_percent / 100))
        top_students = sorted_students[:top_count]
        
        # 필요한 정보만 추출
        result = []
        for student in top_students:
            result.append({
                '이름': student['이름'],
                '학년': student['학년'],
                '반': student['반'],
                '번호': student['번호'],
                '점수': student[subject]
            })
        
        return result
    
    def get_all_top_students(self, top_percent: int = 30) -> Dict[str, List[Dict]]:
        """모든 과목의 상위권 학생 분류"""
        all_top_students = {}
        for subject in self.subjects:
            all_top_students[subject] = self.get_top_students_by_subject(subject, top_percent)
        return all_top_students
    
    def calculate_student_total_and_average(self) -> List[Dict]:
        """각 학생의 총점과 평균 계산"""
        result = []
        for student in self.student_data:
            total = sum(student.get(subject, 0) for subject in self.subjects)
            average = round(total / len(self.subjects), 2)
            
            result.append({
                '이름': student['이름'],
                '학년': student['학년'],
                '반': student['반'],
                '번호': student['번호'],
                '총점': total,
                '평균': average
            })
        
        # 총점 높은 순으로 정렬
        result.sort(key=lambda x: x['총점'], reverse=True)
        return result
    
    def get_score_distribution(self, subject: str) -> Dict[str, int]:
        """
        특정 과목의 점수 분포 계산
        90점 이상(A), 80-89(B), 70-79(C), 60-69(D), 60점 미만(F)
        """
        scores = [student[subject] for student in self.student_data if subject in student]
        distribution = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'F': 0}
        
        for score in scores:
            if score >= 90:
                distribution['A'] += 1
            elif score >= 80:
                distribution['B'] += 1
            elif score >= 70:
                distribution['C'] += 1
            elif score >= 60:
                distribution['D'] += 1
            else:
                distribution['F'] += 1
        
        return distribution
    
    def print_analysis_report(self):
        """분석 결과를 보기 좋게 출력"""
        print("=" * 60)
        print("📊 성적 분석 리포트")
        print("=" * 60)
        
        # 과목별 평균
        print("\n[과목별 평균]")
        averages = self.calculate_all_averages()
        for subject, avg in averages.items():
            print(f"  {subject}: {avg}점")
        
        # 과목별 표준편차
        print("\n[과목별 표준편차]")
        stdevs = self.calculate_all_stdevs()
        for subject, std in stdevs.items():
            print(f"  {subject}: {std}")
        
        # 과목별 상위 30% 학생
        print("\n[과목별 상위 30% 학생]")
        top_students = self.get_all_top_students(30)
        for subject, students in top_students.items():
            print(f"\n  📌 {subject}")
            for i, student in enumerate(students, 1):
                print(f"    {i}. {student['이름']} ({student['학년']}학년 {student['반']}반 {student['번호']}번) - {student['점수']}점")
        
        # 전체 석차 (상위 10명)
        print("\n[전체 석차 TOP 10]")
        rankings = self.calculate_student_total_and_average()[:10]
        for i, student in enumerate(rankings, 1):
            print(f"  {i}위. {student['이름']} ({student['학년']}학년 {student['반']}반) - 총점: {student['총점']}점, 평균: {student['평균']}점")
        
        print("\n" + "=" * 60)


# 사용 예시
if __name__ == "__main__":
    # 샘플 데이터 (실제로는 데이터 입력 모듈에서 받아올 데이터)
    sample_data = [
        {'학년': 3, '반': 1, '번호': 1, '이름': '김민지', '국어': 92, '영어': 88, '수학': 95, '과학': 90, '사회': 87},
        {'학년': 3, '반': 1, '번호': 2, '이름': '이재원', '국어': 81, '영어': 79, '수학': 85, '과학': 82, '사회': 78},
        {'학년': 3, '반': 1, '번호': 3, '이름': '박하늘', '국어': 85, '영어': 83, '수학': 88, '과학': 86, '사회': 84},
        {'학년': 3, '반': 1, '번호': 4, '이름': '최지수', '국어': 97, '영어': 95, '수학': 98, '과학': 96, '사회': 94},
        {'학년': 3, '반': 1, '번호': 5, '이름': '정승민', '국어': 77, '영어': 75, '수학': 80, '과학': 78, '사회': 76},
    ]
    
    # 분석기 생성 및 실행
    analyzer = GradeAnalyzer(sample_data)
    analyzer.print_analysis_report()
    
    # 개별 기능 테스트
    print("\n\n[개별 기능 테스트]")
    print(f"국어 평균: {analyzer.calculate_subject_average('국어')}")
    print(f"수학 표준편차: {analyzer.calculate_subject_stdev('수학')}")
    print(f"\n수학 상위 30% 학생:")
    for student in analyzer.get_top_students_by_subject('수학', 30):
        print(f"  - {student['이름']}: {student['점수']}점")
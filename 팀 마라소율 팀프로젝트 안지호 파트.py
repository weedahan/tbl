import statistics
from typing import List, Dict, Tuple

class GradeAnalyzer:
    """
    대학생 성적 데이터 분석 모듈
    - 전공별 평균, 표준편차 계산
    - 전공별 상위권 학생 분류
    - 학점 분포 분석
    """
    
    def __init__(self, student_data: List[Dict]):
        """
        Args:
            student_data: 학생 데이터 리스트
            예: [{'학번': '20250001', '이름': '김민지', '전공': '컴퓨터공학', 
                  '점수': 92, '학점': 'A'}, ...]
        """
        self.student_data = student_data
    
    def get_all_majors(self) -> List[str]:
        """모든 전공 목록 추출"""
        majors = list(set(student['전공'] for student in self.student_data))
        return sorted(majors)
    
    def calculate_major_average(self, major: str) -> float:
        """특정 전공의 평균 점수 계산"""
        scores = [student['점수'] for student in self.student_data 
                  if student['전공'] == major]
        if not scores:
            return 0.0
        return round(statistics.mean(scores), 2)
    
    def calculate_all_major_averages(self) -> Dict[str, float]:
        """모든 전공의 평균 계산"""
        averages = {}
        for major in self.get_all_majors():
            averages[major] = self.calculate_major_average(major)
        return averages
    
    def calculate_major_stdev(self, major: str) -> float:
        """특정 전공의 표준편차 계산"""
        scores = [student['점수'] for student in self.student_data 
                  if student['전공'] == major]
        if len(scores) < 2:
            return 0.0
        return round(statistics.stdev(scores), 2)
    
    def calculate_all_major_stdevs(self) -> Dict[str, float]:
        """모든 전공의 표준편차 계산"""
        stdevs = {}
        for major in self.get_all_majors():
            stdevs[major] = self.calculate_major_stdev(major)
        return stdevs
    
    def get_top_students_by_major(self, major: str, top_percent: int = 30) -> List[Dict]:
        """
        특정 전공의 상위권 학생 분류
        
        Args:
            major: 전공명
            top_percent: 상위 몇 퍼센트를 추출할지 (기본값: 30%)
        
        Returns:
            상위권 학생 리스트 (점수 높은 순으로 정렬)
        """
        # 해당 전공 학생들만 필터링 및 정렬
        major_students = [s for s in self.student_data if s['전공'] == major]
        sorted_students = sorted(major_students, key=lambda x: x['점수'], reverse=True)
        
        # 상위 n% 계산
        top_count = max(1, int(len(sorted_students) * top_percent / 100))
        top_students = sorted_students[:top_count]
        
        # 필요한 정보만 추출
        result = []
        for student in top_students:
            result.append({
                '학번': student['학번'],
                '이름': student['이름'],
                '전공': student['전공'],
                '점수': student['점수'],
                '학점': student['학점']
            })
        
        return result
    
    def get_all_top_students(self, top_percent: int = 30) -> Dict[str, List[Dict]]:
        """모든 전공의 상위권 학생 분류"""
        all_top_students = {}
        for major in self.get_all_majors():
            all_top_students[major] = self.get_top_students_by_major(major, top_percent)
        return all_top_students
    
    def get_overall_rankings(self, limit: int = 10) -> List[Dict]:
        """
        전체 학생 석차 계산 (전공 무관)
        
        Args:
            limit: 상위 몇 명까지 반환할지 (기본값: 10)
        
        Returns:
            상위권 학생 리스트
        """
        sorted_students = sorted(self.student_data, key=lambda x: x['점수'], reverse=True)
        return sorted_students[:limit]
    
    def get_grade_distribution(self, major: str = None) -> Dict[str, int]:
        """
        학점 분포 계산
        
        Args:
            major: 특정 전공 (None이면 전체)
        
        Returns:
            학점별 학생 수
        """
        if major:
            students = [s for s in self.student_data if s['전공'] == major]
        else:
            students = self.student_data
        
        distribution = {}
        for student in students:
            grade = student['학점']
            distribution[grade] = distribution.get(grade, 0) + 1
        
        return dict(sorted(distribution.items()))
    
    def get_score_distribution_by_range(self, major: str = None) -> Dict[str, int]:
        """
        점수 범위별 분포 계산
        90점 이상(A), 80-89(B), 70-79(C), 60-69(D), 60점 미만(F)
        
        Args:
            major: 특정 전공 (None이면 전체)
        """
        if major:
            students = [s for s in self.student_data if s['전공'] == major]
        else:
            students = self.student_data
        
        distribution = {'A급(90+)': 0, 'B급(80-89)': 0, 'C급(70-79)': 0, 
                       'D급(60-69)': 0, 'F급(60미만)': 0}
        
        for student in students:
            score = student['점수']
            if score >= 90:
                distribution['A급(90+)'] += 1
            elif score >= 80:
                distribution['B급(80-89)'] += 1
            elif score >= 70:
                distribution['C급(70-79)'] += 1
            elif score >= 60:
                distribution['D급(60-69)'] += 1
            else:
                distribution['F급(60미만)'] += 1
        
        return distribution
    
    def get_students_by_major(self, major: str) -> List[Dict]:
        """특정 전공의 모든 학생 정보 조회"""
        return [s for s in self.student_data if s['전공'] == major]
    
    def calculate_overall_average(self) -> float:
        """전체 학생 평균 점수"""
        scores = [s['점수'] for s in self.student_data]
        if not scores:
            return 0.0
        return round(statistics.mean(scores), 2)
    
    def calculate_overall_stdev(self) -> float:
        """전체 학생 표준편차"""
        scores = [s['점수'] for s in self.student_data]
        if len(scores) < 2:
            return 0.0
        return round(statistics.stdev(scores), 2)
    
    def print_analysis_report(self):
        """분석 결과를 보기 좋게 출력"""
        print("=" * 70)
        print("📊 대학생 성적 분석 리포트")
        print("=" * 70)
        
        # 전체 통계
        print("\n[전체 통계]")
        print(f"  총 학생 수: {len(self.student_data)}명")
        print(f"  전체 평균: {self.calculate_overall_average()}점")
        print(f"  전체 표준편차: {self.calculate_overall_stdev()}")
        
        # 전공별 평균
        print("\n[전공별 평균 점수]")
        averages = self.calculate_all_major_averages()
        for major, avg in sorted(averages.items(), key=lambda x: x[1], reverse=True):
            print(f"  {major}: {avg}점")
        
        # 전공별 표준편차
        print("\n[전공별 표준편차]")
        stdevs = self.calculate_all_major_stdevs()
        for major, std in sorted(stdevs.items()):
            print(f"  {major}: {std}")
        
        # 전체 학점 분포
        print("\n[전체 학점 분포]")
        grade_dist = self.get_grade_distribution()
        for grade, count in grade_dist.items():
            print(f"  {grade}: {count}명")
        
        # 전공별 상위 30% 학생 (각 전공당 상위 3명만)
        print("\n[전공별 상위 30% 학생]")
        top_students = self.get_all_top_students(30)
        for major, students in sorted(top_students.items()):
            print(f"\n  📌 {major}")
            for i, student in enumerate(students[:3], 1):
                print(f"    {i}. {student['이름']} ({student['학번']}) - {student['점수']}점 ({student['학점']})")
        
        # 전체 석차 TOP 10
        print("\n[전체 석차 TOP 10]")
        rankings = self.get_overall_rankings(10)
        for i, student in enumerate(rankings, 1):
            print(f"  {i}위. {student['이름']} ({student['학번']}) - {student['전공']} - {student['점수']}점 ({student['학점']})")
        
        print("\n" + "=" * 70)


# 사용 예시
if __name__ == "__main__":
    # 샘플 데이터 (실제로는 데이터 입력 모듈에서 받아올 데이터)
    sample_data = [
        {'학번': '20250001', '이름': '김민지', '전공': '컴퓨터공학', '점수': 92, '학점': 'A'},
        {'학번': '20250002', '이름': '이재원', '전공': '기계공학', '점수': 81, '학점': 'B+'},
        {'학번': '20250003', '이름': '박하늘', '전공': '경영학', '점수': 85, '학점': 'B+'},
        {'학번': '20250004', '이름': '최지수', '전공': '인공지능', '점수': 97, '학점': 'A+'},
        {'학번': '20250005', '이름': '정승민', '전공': '영문학', '점수': 77, '학점': 'C+'},
        {'학번': '20250006', '이름': '강미라', '전공': '건축학', '점수': 88, '학점': 'A'},
        {'학번': '20250007', '이름': '윤민혁', '전공': '인공지능', '점수': 95, '학점': 'A+'},
        {'학번': '20250008', '이름': '송혜진', '전공': '물리학', '점수': 64, '학점': 'D+'},
    ]
    
    # 분석기 생성 및 실행
    analyzer = GradeAnalyzer(sample_data)
    analyzer.print_analysis_report()
    
    # 개별 기능 테스트
    print("\n\n[개별 기능 테스트]")
    print(f"컴퓨터공학 평균: {analyzer.calculate_major_average('컴퓨터공학')}")
    print(f"인공지능 표준편차: {analyzer.calculate_major_stdev('인공지능')}")
    print(f"\n인공지능 상위 30% 학생:")
    for student in analyzer.get_top_students_by_major('인공지능', 30):
        print(f"  - {student['이름']}: {student['점수']}점 ({student['학점']})")
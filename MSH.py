import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import platform

def set_korean_font():
    """운영체제에 맞는 한글 폰트 설정 (matplotlib용)"""
    if platform.system() == "Windows":
        plt.rc("font", family="Malgun Gothic")
    elif platform.system() == "Darwin":
        plt.rc("font", family="AppleGothic")
    else:
        plt.rc("font", family="NanumGothic")
    plt.rcParams["axes.unicode_minus"] = False

def load_data(filepath):
    """엑셀 파일에서 성적 데이터 로드"""
    df = pd.read_excel(filepath)
    return df

def calculate_points(grades):
    """학점 문자열을 평점으로 변환"""
    grade_to_point = {
        "A+": 4.5, "A": 4.0,
        "B+": 3.5, "B": 3.0,
        "C+": 2.5, "C": 2.0,
        "D+": 1.5, "D": 1.0,
        "F": 0.0
    }
    points = np.array([grade_to_point.get(g, 0.0) for g in grades])
    return points

def find_student(df, query, col_num="학번", col_name="이름"):
    """입력값이 숫자면 학번으로, 아니면 이름으로 학생 데이터 찾기"""
    if query.isdigit():
        selected = df[df[col_num] == int(query)]
    else:
        selected = df[df[col_name] == query]
    if selected.empty:
        return None
    return selected.iloc[0]

def plot_score_distribution(scores, student_score, mean_score):
    mean = scores.mean()
    std = scores.std(ddof=0)

    plt.figure(figsize=(10, 5))
    plt.suptitle("전체 학생 점수 분포 대비 본인 점수 위치", fontsize=15, fontweight="bold", y=0.98)
    plt.title(f"전체 평균 점수: {mean_score:.1f}   |   본인 점수: {student_score:.1f}", fontsize=12, pad=18)

    count, bins, _ = plt.hist(scores, bins=10, alpha=0.6)
    x = np.linspace(scores.min(), scores.max(), 200)
    pdf = (1/(std*np.sqrt(2*np.pi))) * np.exp(-0.5*((x-mean)/std)**2)
    bin_width = bins[1] - bins[0]
    pdf_scaled = pdf * len(scores) * bin_width
    plt.plot(x, pdf_scaled)

    plt.axvline(mean_score, linestyle="dashed", linewidth=2, label="전체 평균")
    plt.axvline(student_score, linewidth=2, label="본인 점수")
    plt.xlabel("점수")
    plt.ylabel("학생 수")
    plt.legend(loc="upper right")
    plt.tight_layout(rect=[0, 0, 1, 0.88])
    plt.show()

def plot_grade_distribution(grades, student_grade, student_name):
    unique_grades = ["A+", "A", "B+", "B", "C+", "C", "D+", "D", "F"]
    counts = [np.sum(grades == g) for g in unique_grades]
    mean_point = calculate_points(grades).mean()

    plt.figure(figsize=(8, 4))
    plt.suptitle("전체 학점 분포 대비 본인 학점 위치", fontsize=15, fontweight="bold", y=0.98)
    plt.title(f"전체 평균 평점(GPA): {mean_point:.2f}   |   본인 학점: {student_grade}   {student_name}", fontsize=12, pad=18)

    plt.bar(unique_grades, counts)
    if student_grade in unique_grades:
        idx = unique_grades.index(student_grade)
        plt.text(idx, counts[idx] + max(counts)*0.1, student_name, ha="center", fontsize=9)
    plt.xlabel("학점")
    plt.ylabel("학생 수")
    plt.xticks(rotation=45)
    plt.tight_layout(rect=[0, 0, 1, 0.88])
    plt.show()

def plot_overall_stats(scores):
    mean = scores.mean()
    std = scores.std(ddof=0)
    print(f"전체 학생 평균 점수: {mean:.2f}, 표준편차: {std:.2f}")

    plt.figure(figsize=(12, 6))
    plt.hist(scores, bins=20, alpha=0.7, label="점수 분포")
    plt.axvline(mean, color='r', linestyle='dashed', linewidth=2, label='전체 평균')
    plt.axvline(mean + std, color='orange', linestyle='dotted', linewidth=2, label='평균 + 표준편차')
    plt.axvline(mean - std, color='orange', linestyle='dotted', linewidth=2, label='평균 - 표준편차')
    plt.title("전체 학생 점수 분포 및 통계")
    plt.xlabel("점수")
    plt.ylabel("학생 수")
    plt.legend()
    plt.tight_layout()
    plt.show()

def classify_top_students_by_major(df, col_major, col_score, col_name):
    """전공별 상위 10% 학생을 자동 분류하여 학과별 리스트 출력"""
    grouped = df.groupby(col_major)[col_score]
    top_students_by_major = {}

    for major, group_scores in grouped:
        threshold = group_scores.quantile(0.9)
        top_students = df[(df[col_major] == major) & (df[col_score] >= threshold)]
        top_students_by_major[major] = top_students[[col_name, col_score]]

    print("\n전공별 상위 10% 학생 자동 분류 결과:")
    for major, students in top_students_by_major.items():
        print(f"\n전공: {major} (상위 10% 이상 점수 기준: {students[col_score].min():.2f} 이상)")
        for idx, row in students.iterrows():
            print(f"  - {row[col_name]}: 점수 {row[col_score]}")

def main():
    FILE_PATH = "대학교 성적 리스트 100명.xlsx"
    COL_NUM = "학번"
    COL_NAME = "이름"
    COL_SCORE = "점수"
    COL_GRADE = "학점"
    COL_MAJOR = "전공"  # 엑셀에 반드시 있어야 하는 컬럼명

    set_korean_font()
    df = load_data(FILE_PATH)

    scores = df[COL_SCORE].to_numpy()
    grades = df[COL_GRADE].to_numpy()

    plot_overall_stats(scores)

    query = input("학번 혹은 이름을 입력하세요: ").strip()
    student = find_student(df, query, COL_NUM, COL_NAME)
    if student is None:
        print("학생을 찾을 수 없습니다.")
        return

    student_score = float(student[COL_SCORE])
    student_grade = str(student[COL_GRADE])
    student_name = str(student[COL_NAME])

    plot_score_distribution(scores, student_score, scores.mean())
    plot_grade_distribution(grades, student_grade, student_name)

    if COL_MAJOR in df.columns:
        classify_top_students_by_major(df, COL_MAJOR, COL_SCORE, COL_NAME)
    else:
        print(f"'{COL_MAJOR}' 컬럼이 데이터에 없습니다. 전공별 상위권 분류를 실행하지 않습니다.")

if __name__ == "__main__":
    main()

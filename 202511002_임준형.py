import tkinter as tk
from tkinter import messagebox
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import platform
import numpy as np

# ★ 여기에 추가 ★
system = platform.system()
if system == 'Windows':
    plt.rc('font', family='Malgun Gothic')
elif system == 'Darwin':
    plt.rc('font', family='AppleGothic')
else:
    plt.rc('font', family='NanumGothic')

plt.rcParams['axes.unicode_minus'] = False

# ----------------------------
# 1. 데이터 및 설정
# ----------------------------

df = pd.read_excel('students_100.xlsx')

subjects = ['파이썬기초및실습', '영상이해', '알기쉬운확률통계']
competencies = ['기초역량','개념활용역량','사고력','데이터 해석력','수리력','시각 및 영상 이해력']

weights = {
    '파이썬기초및실습': {
        '기초역량': 0.50, '개념활용역량': 0.50, '사고력': 0.30,
        '데이터 해석력': 0.40, '수리력': 0.20, '시각 및 영상 이해력': 0.10
    },
    '영상이해': {
        '기초역량': 0.30, '개념활용역량': 0.20, '사고력': 0.30,
        '데이터 해석력': 0.50, '수리력': 0.30, '시각 및 영상 이해력': 0.80
    },
    '알기쉬운확률통계': {
        '기초역량': 0.20, '개념활용역량': 0.30, '사고력': 0.40,
        '데이터 해석력': 0.10, '수리력': 0.50, '시각 및 영상 이해력': 0.10
    }
}

# ----------------------------
# 2. 계산 함수
# ----------------------------

def calculate_competencies(row):
    result = {c: 0 for c in competencies}
    for subject in subjects:
        for c in competencies:
            result[c] += row[subject] * weights[subject][c]
    return result

# 전체 평균 계산
avg_subject_scores = df[subjects].mean()
all_comp = pd.DataFrame([calculate_competencies(row) for _, row in df.iterrows()])
avg_comp_scores = all_comp.mean()

# ----------------------------
# 3. 그래프 함수
# ----------------------------

def plot_subject_bar(student_row):
    x = np.arange(len(subjects))
    width = 0.35

    plt.figure(figsize=(7,5))
    plt.bar(x - width/2, student_row[subjects], width, label='학생')
    plt.bar(x + width/2, avg_subject_scores, width, label='전체 평균')

    plt.xticks(x, subjects)
    plt.ylabel("점수")
    plt.title(f"{student_row['이름']} 과목별 점수 비교")
    plt.legend()
    plt.show()

def plot_radar(student_name, student_comp):
    student_vals = list(student_comp.values())
    avg_vals = list(avg_comp_scores.values)

    student_vals += student_vals[:1]
    avg_vals += avg_vals[:1]

    angles = np.linspace(0, 2*np.pi, len(competencies), endpoint=False).tolist()
    angles += angles[:1]

    plt.figure(figsize=(7,7))
    ax = plt.subplot(111, polar=True)

    ax.plot(angles, student_vals, linewidth=2, label='학생')
    ax.fill(angles, student_vals, alpha=0.3)

    ax.plot(angles, avg_vals, linewidth=2, linestyle='dashed', label='전체 평균')
    ax.fill(angles, avg_vals, alpha=0.15)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(competencies)
    plt.title(f"{student_name} 역량 비교")
    plt.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
    plt.show()

# ----------------------------
# 4. 버튼 클릭 이벤트
# ----------------------------

def search_student():
    user_input = entry.get().strip()

    student = df[(df['학번'].astype(str) == user_input) | (df['이름'] == user_input)]

    if student.empty:
        messagebox.showerror("오류", "해당 학생을 찾을 수 없습니다.")
        return

    row = student.iloc[0]
    student_comp = calculate_competencies(row)

    # 그래프 출력
    plot_subject_bar(row)
    plot_radar(row['이름'], student_comp)

# ----------------------------
# 5. Tkinter UI
# ----------------------------

root = tk.Tk()
root.title("학생 성취도 분석 프로그램")
root.geometry("400x200")

label = tk.Label(root, text="학번 또는 이름을 입력하세요", font=("맑은 고딕", 12))
label.pack(pady=10)

entry = tk.Entry(root, font=("맑은 고딕", 12), width=25)
entry.pack()

button = tk.Button(root, text="학생 데이터 조회", font=("맑은 고딕", 12),
                   command=search_student)
button.pack(pady=20)

root.mainloop()

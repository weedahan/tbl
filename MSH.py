import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
import numpy as np

# 한글 폰트 설정 (윈도우 예시)
font_path = "C:/Windows/Fonts/malgun.ttf"
font_name = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font_name)

def load_excel(load_flag=False, file_path=None):
    if load_flag and file_path:
        df = pd.read_excel(file_path)
        print("엑셀 파일이 불러와졌습니다.")
        return df
    else:
        print("엑셀 불러오기 끔 상태입니다.")
        return None

def plot_students_scores(df):
    if df is None:
        print("데이터가 없어서 그래프를 그릴 수 없습니다.")
        return
    scores = df['점수']
    mean_score = scores.mean()
    std_score = scores.std()

    fig, ax = plt.subplots(figsize=(12,6))
    # 학생별 점수 막대 (혹은 산점도)
    ax.bar(range(len(scores)), scores, color='skyblue')
    # 평균선
    ax.axhline(mean_score, color='red', linestyle='--', label='평균')
    # 표준편차 범위
    ax.fill_between([0, len(scores)-1], mean_score-std_score, mean_score+std_score, color='yellow', alpha=0.3, label='표준편차 범위')
    ax.set_xlabel('학생 수')
    ax.set_ylabel('점수')
    ax.set_title('학생별 성적과 평균, 표준편차 범위')
    ax.legend(loc='center left', bbox_to_anchor=(0.84, 0.94))
    plt.show()
    
def get_top_10_percent_by_major(df):
    # 전공별로 상위 10% 학생 추출
    top_10_percent = df.groupby('전공').apply(lambda x: x.nlargest(max(1, int(len(x)*0.1)), '점수'))
    top_10_percent = top_10_percent.reset_index(drop=True)
    return top_10_percent

def plot_top_10_percent_by_major(df):
    if df is None or df.empty:
        print("데이터가 없어서 전공별 상위 10% 그래프를 그릴 수 없습니다.")
        return
    
    top_10_percent = get_top_10_percent_by_major(df)

    fig, ax = plt.subplots(figsize=(10,6))
    for _, row in top_10_percent.iterrows():
        ax.scatter(row['전공'], row['점수'], color='red', s=50)

    ax.set_xlabel('전공')
    ax.set_ylabel('점수')
    ax.set_title('전공별 상위 10% 학생 점수')
    plt.show()


# 실행 예시
load_flag = True
file_path = 'student_data.xlsx'
df = load_excel(load_flag, file_path)
plot_students_scores(df)
top_10_df = get_top_10_percent_by_major(df)  # 전공별 상위 10% DataFrame 반환
plot_top_10_percent_by_major(df)  # 시각화
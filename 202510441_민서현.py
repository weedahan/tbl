import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
import numpy as np

font_path = "C:/Windows/Fonts/malgun.ttf"
font_name = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font_name)

def load_excel_file(is_loaded=False, excel_path=None):
    if is_loaded and excel_path:
        data = pd.read_excel(excel_path)
        print("엑셀 파일 로드 완료.")
        return data
    print("엑셀 로드 비활성화 상태입니다.")
    return None

def plot_score_bar(data):
    if data is None:
        print("데이터가 없습니다.")
        return

    score_series = data['점수']
    score_mean = score_series.mean()
    score_std = score_series.std()

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar(range(len(score_series)), score_series, color='skyblue', label='점수')
    ax.axhline(score_mean, color='red', linestyle='--', label='평균')
    ax.fill_between([0, len(score_series) - 1], score_mean - score_std, score_mean + score_std,
                    color='yellow', alpha=0.3, label='표준편차')
    ax.set_xlabel('학생 번호')
    ax.set_ylabel('점수')
    ax.set_title('학생별 점수, 평균, 표준편차')
    ax.legend(loc='upper right')
    plt.show()

def get_top_10_percent(data):
    top_students = data.groupby('전공').apply(
        lambda group: group.nlargest(max(1, int(len(group) * 0.1)), '점수')
    ).reset_index(drop=True)
    return top_students

def plot_major_avg_vs_top10(data):
    if data is None or data.empty:
        print("데이터가 없습니다.")
        return

    top_students = get_top_10_percent(data)
    major_avg = data.groupby('전공')['점수'].mean().reset_index()
    top10_avg = top_students.groupby('전공')['점수'].mean().reset_index()

    fig, ax = plt.subplots(figsize=(10, 6))
    bar_width = 0.35
    xpos = np.arange(len(major_avg))

    ax.bar(xpos - bar_width/2, major_avg['점수'], bar_width, label='전공 평균', color='skyblue')
    ax.bar(xpos + bar_width/2, top10_avg['점수'], bar_width, label='상위 10% 평균', color='salmon')

    ax.set_xticks(xpos)
    ax.set_xticklabels(major_avg['전공'])
    ax.set_xlabel('전공')
    ax.set_ylabel('점수')
    ax.set_title('전공별 평균과 상위 10% 평균 비교')
    ax.legend()
    plt.show()

if __name__ == "__main__":
    is_loaded = True
    excel_path = '.py 파일과 엑셀파일을 같은 파일에 포함시키고 파일이름으로 변경해주세요.xlsx'
    # EX) excel_path = '대학생 성적 리스트 100명.xlsx'
    data = load_excel_file(is_loaded, excel_path)
    plot_score_bar(data)
    plot_major_avg_vs_top10(data)


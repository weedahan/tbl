# competency_logic.py

# 1. 과목 및 역량 설정
SUBJECTS = ["파이썬기초와실습", "영상이해", "알기쉬운확률과통계"]

# 가중치 (순서대로 파이썬, 영상이해, 확통 비중)
WEIGHTS = {
    "기초역량": [0.5, 0.2, 0.3],
    "개념활용역량": [0.4, 0.3, 0.3],
    "사고력": [0.2, 0.2, 0.6],
    "문제해결력": [0.4, 0.3, 0.3],
    "수리·데이터해석력": [0.1, 0.2, 0.7],
    "시각·영상이해력": [0.1, 0.9, 0.0]
}

COMPETENCIES = list(WEIGHTS.keys())

# 2. 역량 점수 계산 함수
def calculate_competency(scores):
    """
    scores: [과목1점수, 과목2점수, 과목3점수] 리스트
    return: {"역량명": 점수, ...} 딕셔너리
    """
    comp_scores = {}
    for comp, weights in WEIGHTS.items():
        total = 0
        for i, score in enumerate(scores):
            total += score * weights[i]
        comp_scores[comp] = total
    return comp_scores

# 3. 등급 변환 헬퍼 함수
def get_grade(score):
    if score >= 90: return "A"
    elif score >= 80: return "B"
    elif score >= 70: return "C"
    elif score >= 60: return "D"
    else: return "F"
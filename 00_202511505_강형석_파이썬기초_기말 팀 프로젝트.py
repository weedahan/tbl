import pandas as pd
import os

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns',None)
pd.set_option('display.width', 400)

# 엑셀 파일 이름을 지정합니다.
FILE_NAME = '파이썬 기초/student_data.xlsx'

def read_excel_file(file_name):
    """
    엑셀 파일을 읽고 데이터를 출력하는 함수입니다.
    """
    
    # 1. 파일이 현재 폴더에 있는지 확인
    if not os.path.exists(file_name):
        print(f"오류: 파일을 찾을 수 없습니다. -> '{file_name}'")
        print("   엑셀 파일이 파이썬 코드와 같은 폴더에 있는지 확인해주세요.")
        return

    # 2. 엑셀 파일 읽기 시도
    try:
        # read_excel 명령어로 엑셀 파일을 읽습니다.
        data_table = pd.read_excel(file_name)
        
        print(f"엑셀 파일 '{file_name}'에서 데이터 불러오기 성공.")
        print(f"총 {len(data_table)}개의 행이 로드되었습니다.")
        
        # 3. 데이터 미리보기
        print("\n--- 불러온 데이터 미리보기 (상위 5줄) ---")
        print(data_table.head())
        
        # 4. '이름'과 '점수' 컬럼만 출력해보기 (컬럼 이름은 엑셀 파일의 첫 행과 일치해야 함)
        if '학번' in data_table.columns and '학점' in data_table.columns:
            print("\n--- '학번', '이름', '전공', '점수', '학점' 컬럼 ---")
            print(data_table[['학번', '이름', '전공', '점수', '학점']])
        
    except Exception as e:
        print(f"엑셀 파일을 읽는 중 오류가 발생했습니다. 라이브러리가 제대로 설치되었는지 확인해주세요: {e}")

# --- 프로그램 실행 ---
if __name__ == "__main__":
    read_excel_file(FILE_NAME)
이 Python 스크립트는 사용자가 Excel(.xlsx, .xls) 또는 CSV 파일을 선택해 불러오도록 돕는 간단한 GUI 기반 유틸리티입니다. 선택한 파일 경로를 저장해 두고, 다음 실행 시 저장된 경로를 재사용할지 묻는 기능도 포함합니다.

ExcelLoader README
개요
ExcelLoader는 Python과 Tkinter를 사용해 Excel 및 CSV 파일을 편리하게 불러오는 유틸리티입니다.

저장된 마지막 파일 경로를 기억해 다음 실행 시 불러올지 사용자에게 확인

새 파일 선택 대화상자 제공

로드한 파일은 Pandas DataFrame으로 저장

기본적인 오류 처리 포함

주요 기능
저장된 경로 파일(saved_path.txt)이 있으면 해당 파일을 재사용할지 물어봄

사용자 선택에 따라 새 파일을 탐색기 대화상자로 선택 가능

Excel (.xlsx, .xls) 및 CSV 파일 지원

로드된 데이터의 기본 정보와 첫 부분 출력

사용 방법
필요한 라이브러리 설치

bash
pip install pandas openpyxl
(openpyxl은 Excel 파일 처리를 위한 라이브러리입니다)

스크립트 실행

bash
python excel_loader.py
프로그램 실행 흐름

이전에 불러온 파일 경로가 저장되어 있다면, 해당 파일 경로를 사용할지 질문

사용자가 '아니오'를 선택하면 파일 대화상자가 나타나 새 파일을 선택하도록 안내

선택한 파일 경로를 saved_path.txt에 저장하여 다음 실행에 활용

해당 파일을 판다스 데이터프레임으로 로드

콘솔에 데이터프레임의 처음 몇 줄과 크기 출력

코드 구조
ExcelLoader 클래스

get_saved_path(): 저장된 경로 읽기

save_path(path): 경로 저장

load_file_dialog(): 파일 선택 대화상자 호출

ask_use_existing(path): 기존 파일 사용 여부 묻는 GUI 질문

load_file(): 전체 로드 프로세스 관리 및 실행

확장 및 활용
로드된 df 속성으로 데이터 분석, 처리 등 다양한 작업 가능

GUI 부분을 확장해 파일 정보 미리보기, 여러 파일 로드 지원 가능

저장 경로를 사용자 지정하거나, 여러 파일 형식 확장도 가능

참고
Windows, Mac, Linux 등 Tkinter가 지원되는 환경에서 동작

saved_path.txt는 스크립트를 실행하는 현재 작업 디렉터리에 생성/읽기

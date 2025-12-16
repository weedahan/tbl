import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox
import os

class ExcelLoader:
    def __init__(self, path_file='saved_path.txt'):
        self.df = None
        self.path_file = path_file

    def get_saved_path(self):
        """저장된 경로가 있고 실제 파일이 존재하는지 확인"""
        if os.path.exists(self.path_file):
            try:
                with open(self.path_file, 'r', encoding='utf-8') as f:
                    path = f.read().strip()
                    if path and os.path.exists(path):
                        return path
            except Exception:
                return None
        return None

    def save_path(self, path):
        """유효한 파일 경로를 텍스트 파일에 저장"""
        try:
            with open(self.path_file, 'w', encoding='utf-8') as f:
                f.write(path)
        except Exception as e:
            print(f"경로 저장 실패: {e}")

    def load_file_dialog(self):
        """파일 선택 대화상자 실행"""
        # Tkinter 루트 윈도우 생성 (숨김 모드)
        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True) # 창을 최상단으로 설정

        filetypes = [("Excel files", "*.xlsx *.xls *.csv")]
        file_path = filedialog.askopenfilename(
            parent=root,
            title="엑셀 파일 선택하기", 
            filetypes=filetypes
        )
        
        root.destroy()
        return file_path

    def ask_use_existing(self, path):
        """기존 파일을 사용할지 묻는 대화상자"""
        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        
        msg = f"이전에 작업하던 파일이 있습니다.\n경로: {path}\n\n이 파일을 다시 불러오시겠습니까?"
        answer = messagebox.askyesno("기존 파일 로드", msg, parent=root)
        
        root.destroy()
        return answer

    def load_file(self):
        """전체 로드 프로세스 관리"""
        target_path = None
        saved_path = self.get_saved_path()

        # 1. 저장된 경로가 유효한지 확인하고 사용자에게 의사 묻기
        if saved_path:
            use_existing = self.ask_use_existing(saved_path)
            if use_existing:
                print(f"기존 파일 경로를 사용합니다: {saved_path}")
                target_path = saved_path
            else:
                print("새 파일을 선택합니다.")
        
        # 2. 타겟 경로가 없으면 (저장된 게 없거나, 사용자가 No를 선택한 경우) 파일 선택 창 띄우기
        if not target_path:
            target_path = self.load_file_dialog()
            if target_path:
                self.save_path(target_path) # 새 경로 저장

        # 3. 최종 파일 로드 시도
        if not target_path:
            print("파일이 선택되지 않았습니다. 취소됨.")
            return False

        try:
            # 확장자에 따른 로드 방식 구분 (csv 지원 추가)
            if target_path.endswith('.csv'):
                self.df = pd.read_csv(target_path)
            else:
                self.df = pd.read_excel(target_path)
            
            print(f"파일 로드 성공: {os.path.basename(target_path)}")
            print("-" * 30)
            print(self.df.head())
            print("-" * 30)
            return True
            
        except Exception as e:
            print(f"파일 로드 중 오류 발생: {e}")
            return False

if __name__ == "__main__":
    loader = ExcelLoader()
    success = loader.load_file()
    
    if success:
        print(f"데이터 크기: {loader.df.shape}")
        # 이후 데이터 처리 로직 작성
    else:
        print("프로그램을 종료합니다.")

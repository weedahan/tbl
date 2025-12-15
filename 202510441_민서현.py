import pandas as pd
import os
import json
from tkinter import filedialog, Tk

class GradeLoader:
    def __init__(self):
        self.df = None
        self.file_path = None
        self.config_file = 'grade_config.json'
        self.load_config()
    
    def load_config(self):
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    self.file_path = config.get('last_file_path', '')
            except:
                self.file_path = ""
    
    def save_config(self):
        if self.file_path:
            config = {'last_file_path': self.file_path}
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
    
    def select_file(self):
        root = Tk()
        root.withdraw()
        initial_dir = os.path.dirname(self.file_path) if self.file_path else os.path.expanduser("~")
        
        file_path = filedialog.askopenfilename(
            title="학생 성적표 엑셀 파일 선택",
            filetypes=[("Excel files", "*.xlsx *.xls"), ("All files", "*.*")],
            initialdir=initial_dir
        )
        root.destroy()
        return file_path
    
    def load(self):
        if self.file_path and os.path.exists(self.file_path):
            try:
                self.df = pd.read_excel(self.file_path, engine='openpyxl')
                print(f"{len(self.df)}명 데이터 로드: {self.file_path}")
                print(f"컬럼: {list(self.df.columns)}")
                return True
            except:
                pass
        
        self.file_path = self.select_file()
        if not self.file_path:
            print("파일 선택 취소")
            return False
        
        try:
            self.df = pd.read_excel(self.file_path, engine='openpyxl')
            print(f"{len(self.df)}명 데이터 로드: {self.file_path}")
            print(f"컬럼: {list(self.df.columns)}")
            self.save_config()
            return True
        except Exception as e:
            print(f"로드 실패: {e}")
            return False
    
    def reload(self):
        print("새 파일 선택...")
        self.file_path = self.select_file()
        if not self.file_path:
            print("파일 선택 취소")
            return False
        
        try:
            self.df = pd.read_excel(self.file_path, engine='openpyxl')
            print(f"{len(self.df)}명 데이터 로드: {self.file_path}")
            print(f"컬럼: {list(self.df.columns)}")
            self.save_config()
            return True
        except Exception as e:
            print(f"로드 실패: {e}")
            return False
    
    def get_data(self):
        return self.df

def main():
    loader = GradeLoader()
    
    while True:
        print("\n1. 파일 불러오기")
        print("2. 다른 파일 불러오기") 
        print("3. 종료")
        print("-" * 20)
        
        choice = input("선택 (1-3): ").strip()
        
        if choice == '1':
            loader.load()
        elif choice == '2':
            loader.reload()
        elif choice == '3':
            print("종료")
            break
        else:
            print("잘못된 선택")

if __name__ == "__main__":
    main()

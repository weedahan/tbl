import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import re
import pandas as pd
import os
import math

# ===============================
# 환경/폰트 설정
# ===============================
KOREAN_FONT_FAMILY = "Maplestory"
BOLD_LARGE_FONT = (KOREAN_FONT_FAMILY, 16, "bold")
LARGE_FONT = (KOREAN_FONT_FAMILY, 16)
HEADER_FONT = (KOREAN_FONT_FAMILY, 28, "bold")

P3_HEADER_FONT = (KOREAN_FONT_FAMILY, 32, "bold")
P3_TITLE_FONT = (KOREAN_FONT_FAMILY, 18, "bold")
P3_DATA_FONT = (KOREAN_FONT_FAMILY, 16)
P3_FORMULA_FONT = (KOREAN_FONT_FAMILY, 18)

SAVED_PATH_FILE = "last_data_path.txt"
ADMIN_ID = "77777777"

# 레이더 차트 최대 점수 (최대 60점으로 고정)
RADAR_MAX_SCORE = 60.0


def score_to_grade(score):
    if score >= 95: return "A+"
    elif score >= 90: return "A"
    elif score >= 85: return "A-"
    elif score >= 80: return "B+"
    elif score >= 70: return "B"
    elif score >= 60: return "C"
    else: return "F"


class MyApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("Python TEAMproject")
        self.geometry("1400x800")

        self.current_user_data = None
        self.dynamic_grades = {ADMIN_ID: {"name": "admin", "subjects": {}}}
        self.loaded_file_name = "로드된 파일 없음"

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        style = ttk.Style()
        style.configure('Next.TButton', font=(KOREAN_FONT_FAMILY, 14), padding=5)

        self.frames = {}
        for F in (LoginPage, PageOne, PageTwo, PageThree, PageFour):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(LoginPage)

    def show_frame(self, cont):
        frame = self.frames[cont]

        if cont == PageOne and hasattr(frame, "load_user_data"):
            frame.load_user_data()
        if cont == PageTwo and hasattr(frame, "load_competency_data"):
            frame.load_competency_data()
        if cont == PageFour and hasattr(frame, "load_report"):
            frame.load_report()

        frame.tkraise()

    def logout(self):
        self.current_user_data = None

        lp = self.frames[LoginPage]
        lp.name_entry.delete(0, tk.END)
        lp.id_entry.delete(0, tk.END)

        p1 = self.frames[PageOne]
        p1.clear_grade_rows()

        self.show_frame(LoginPage)

    def save_last_file_path(self, path):
        try:
            with open(SAVED_PATH_FILE, "w", encoding="utf-8") as f:
                f.write(path.strip())
        except:
            pass

    def load_last_file_path(self):
        try:
            if os.path.exists(SAVED_PATH_FILE):
                with open(SAVED_PATH_FILE, "r", encoding="utf-8") as f:
                    p = f.read().strip()
                if p and os.path.exists(p):
                    return p
        except:
            pass
        return None

    def calc_competency_scores(self, student_subject_scores):
        weights = PageThree.COMPETENCY_WEIGHTS
        subjects = PageThree.SUBJECTS

        comp_result = {}
        # 핵심 역량 점수 계산: (교과목 점수 x 가중치)를 합산하여 0~100 범위의 총점 획득 (유지)
        for comp_name, w_list in weights.items():
            total_weighted_score = 0.0
            
            # 1. 과목별 (점수 * 가중치 / 100) 합산
            for i, sub in enumerate(subjects):
                score = float(student_subject_scores.get(sub, 0)) 
                total_weighted_score += score * (w_list[i] / 100)
            
            # 2. 스케일링 없이 0~100 범위의 합산값 그대로 사용 (유지)
            comp_result[comp_name] = total_weighted_score
            
        return comp_result

    def calc_average_competency_scores(self):
        subject_list = PageThree.SUBJECTS
        sums = {s: 0.0 for s in subject_list}
        cnts = {s: 0 for s in subject_list}

        for sid, sdata in self.dynamic_grades.items():
            if sid == ADMIN_ID:
                continue
            subs = sdata.get("subjects", {})
            for sub in subject_list:
                if sub in subs:
                    avg_score = float(subs[sub].get("avg_score", 0.0))
                    sums[sub] += avg_score
                    cnts[sub] += 1

        avg_subject_scores = {}
        for sub in subject_list:
            avg_subject_scores[sub] = (sums[sub] / cnts[sub]) if cnts[sub] > 0 else 0.0

        return self.calc_competency_scores(avg_subject_scores)

    def process_loaded_data(self, df, file_name):
        if df is None or df.empty:
            messagebox.showerror("오류", "파일에 유효한 데이터가 없습니다.")
            return False

        df.columns = df.columns.str.strip()

        # 데이터 파일 과목 이름 별칭 정의
        subject_aliases = {
            "파이썬기초및실습": ["파이썬", "파이썬기초및실습", "파이썬기초와실습", "파이썬기초및실습 "],
            "영상 이해": ["영상이해", "영상 이해", "영상이해 ", "영상 이해 "],
            "알기쉬운확률통계": ["확률과 통계", "확률통계", "알기쉬운확률통계", "알기쉬운 확률통계", "확통", "확률과통계"]
        }

        def find_col(base_candidates, suffix):
            for base in base_candidates:
                cand = f"{base} {suffix}"
                if cand in df.columns:
                    return cand
                cand2 = f"{base}{suffix}"
                if cand2 in df.columns:
                    return cand2
            return None

        name_col = None
        id_col = None
        for c in df.columns:
            if c in ["성명", "이름", "학생명"]:
                name_col = c
            if c in ["학번", "학생번호", "ID"]:
                id_col = c

        if not name_col or not id_col:
            messagebox.showerror("데이터 오류", "필수 컬럼(성명/학번)을 찾을 수 없습니다.")
            return False

        col_map = {}
        for disp_sub, aliases in subject_aliases.items():
            gcol = find_col(aliases, "등급")
            scol = find_col(aliases, "점수")
            if gcol and scol:
                col_map[disp_sub] = (gcol, scol)

        if not col_map:
            messagebox.showerror(
                "데이터 오류",
                "과목 점수/등급 컬럼을 찾지 못했습니다.\n(예: '파이썬 점수', '영상이해 점수' 등 확인)"
            )
            return False

        total_scores = {sub: {"sum": 0.0, "count": 0} for sub in col_map.keys()}
        parsed_student_data = {}

        for _, row in df.iterrows():
            student_name = str(row[name_col]).strip()
            student_id = str(row[id_col]).strip()

            if not (len(student_id) == 8 and student_id.isdigit()):
                continue

            student_data = {"name": student_name, "subjects": {}}

            for sub, (gcol, scol) in col_map.items():
                earned_grade = str(row[gcol]).strip() if pd.notna(row[gcol]) else "N/A"
                # 점수 데이터 유효성 검사
                try:
                    earned_score = float(row[scol]) if pd.notna(row[scol]) else 0.0
                except ValueError:
                    earned_score = 0.0

                student_data["subjects"][sub] = {
                    "earned_grade": earned_grade,
                    "score": earned_score,
                    "avg_grade": "N/A",
                    "avg_score": 0.0
                }

                total_scores[sub]["sum"] += earned_score
                total_scores[sub]["count"] += 1

            if student_data["subjects"]:
                parsed_student_data[student_id] = student_data

        if not parsed_student_data:
            messagebox.showerror("데이터 오류", "유효한 학생(8자리 학번)을 찾지 못했습니다.")
            return False

        average_scores = {
            sub: (v["sum"] / v["count"]) if v["count"] > 0 else 0.0
            for sub, v in total_scores.items()
        }

        temp_grades = {ADMIN_ID: {"name": "admin", "subjects": {}}}
        for sid, sdata in parsed_student_data.items():
            for sub, sub_data in sdata["subjects"].items():
                avg = average_scores.get(sub, 0.0)
                sub_data["avg_score"] = avg
                sub_data["avg_grade"] = score_to_grade(avg)
            temp_grades[sid] = sdata

        self.dynamic_grades = temp_grades
        self.loaded_file_name = file_name
        messagebox.showinfo("성공", f"데이터 및 평균 로드 완료!\n파일: {file_name}")
        return True


class LoginPage(tk.Frame):
    def __init__(self, parent, controller: MyApp):
        super().__init__(parent)
        self.controller = controller

        center_container = tk.Frame(self)
        center_container.pack(expand=True, fill="x")

        label = tk.Label(center_container, text="로그인", font=HEADER_FONT)
        label.pack(pady=40, padx=10)

        input_container = tk.Frame(center_container)
        input_container.pack()

        load_data_button = ttk.Button(
            input_container,
            text="데이터 파일 불러오기 (Excel/CSV)",
            command=self.load_data_file
        )
        load_data_button.pack(fill="x", pady=(0, 5))

        self.file_status_label = tk.Label(
            input_container,
            text=f"현재 파일: {self.controller.loaded_file_name}",
            font=("Verdana", 10),
            fg="gray"
        )
        self.file_status_label.pack(anchor="w")

        form_frame = tk.Frame(center_container)
        form_frame.pack(pady=10)

        name_label = tk.Label(form_frame, text="이름 :", font=LARGE_FONT)
        name_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.name_entry = tk.Entry(form_frame, width=25, font=LARGE_FONT, justify='center')
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="(예: 홍길동)", font=(KOREAN_FONT_FAMILY, 10), fg="gray").grid(
            row=1, column=1, padx=5, sticky="e"
        )

        id_label = tk.Label(form_frame, text="학번 :", font=LARGE_FONT)
        id_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.id_entry = tk.Entry(form_frame, width=25, font=LARGE_FONT, justify='center')
        self.id_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="(예: 20250001 - 8자리 숫자)", font=(KOREAN_FONT_FAMILY, 10), fg="gray").grid(
            row=3, column=1, padx=5, sticky="e"
        )

        button_frame = tk.Frame(center_container)
        button_frame.pack(pady=30)

        find_id_button = ttk.Button(button_frame, text="학번 찾기", command=self.open_find_id_window, width=20)
        find_id_button.pack(side=tk.LEFT, padx=10)

        login_button = ttk.Button(button_frame, text="확인", command=self.login_attempt, width=20)
        login_button.pack(side=tk.LEFT, padx=10)

        last_path = self.controller.load_last_file_path()
        if last_path:
            try:
                file_name = os.path.basename(last_path)
                if last_path.endswith(".csv"):
                    df = pd.read_csv(last_path, encoding="euc-kr")
                else:
                    df = pd.read_excel(last_path)

                if self.controller.process_loaded_data(df, file_name):
                    self.file_status_label.config(text=f"현재 파일: {file_name}", fg="green")
            except:
                pass

    def load_data_file(self):
        file_path = filedialog.askopenfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx *.xls"), ("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if not file_path:
            return

        file_name = os.path.basename(file_path)

        try:
            if file_path.endswith(".csv"):
                df = pd.read_csv(file_path, encoding="euc-kr")
            else:
                df = pd.read_excel(file_path)

            ok = self.controller.process_loaded_data(df, file_name)
            if ok:
                self.controller.save_last_file_path(file_path)
                self.file_status_label.config(text=f"현재 파일: {file_name}", fg="green")
            else:
                self.file_status_label.config(text=f"로드 실패: {file_name}", fg="red")

        except PermissionError:
            messagebox.showerror(
                "오류",
                "파일을 열 수 없습니다(권한/잠김).\n\n"
                "해결 방법:\n"
                "1) 엑셀 파일이 열려있다면 닫기\n"
                "2) OneDrive 경로라면 바탕화면/문서로 복사 후 다시 선택\n"
                "3) 파일 속성(읽기 전용) 확인"
            )
            self.file_status_label.config(text=f"로드 실패(잠김): {file_name}", fg="red")

        except Exception as e:
            messagebox.showerror("오류", f"파일 로드 중 오류 발생: {e}")
            self.file_status_label.config(text=f"로드 실패: {file_name}", fg="red")

    def validate_inputs(self, name_input, student_id_input):
        if re.fullmatch(r'^[가-힣a-zA-Z\s]+$', name_input) is None:
            messagebox.showerror("입력 오류", "이름은 한글이나 영어(공백 포함)만 입력해야 합니다.")
            return False
        if not student_id_input.isdigit() or len(student_id_input) != 8:
            messagebox.showerror("입력 오류", "학번은 8자리 숫자만 입력해야 합니다.")
            return False
        return True

    def login_attempt(self):
        name_input = self.name_entry.get().strip()
        student_id_input = self.id_entry.get().strip()

        if not self.validate_inputs(name_input, student_id_input):
            return

        if student_id_input in self.controller.dynamic_grades:
            data = self.controller.dynamic_grades[student_id_input]
            if data.get("name") == name_input:
                self.controller.current_user_data = {
                    "user_id": student_id_input,
                    "name": name_input,
                    "student_id": student_id_input
                }
                messagebox.showinfo("성공", f"환영합니다, {name_input}님!")
                self.controller.show_frame(PageOne)
                return

        messagebox.showerror("오류", "이름/학번이 올바르지 않거나 데이터 파일에 해당 정보가 없습니다.")
        self.name_entry.delete(0, tk.END)
        self.id_entry.delete(0, tk.END)

    def open_find_id_window(self):
        FindIdWindow(self.controller)


class FindIdWindow(tk.Toplevel):
    def __init__(self, parent: MyApp):
        super().__init__(parent)
        self.controller = parent

        self.title("학번 찾기")
        self.geometry("350x200")
        self.transient(parent)
        self.grab_set()

        tk.Label(self, text="등록된 이름을 입력하세요", font=(KOREAN_FONT_FAMILY, 14, "bold")).pack(pady=20)
        self.name_entry = tk.Entry(self, width=20, font=LARGE_FONT, justify="center")
        self.name_entry.pack(pady=5)
        ttk.Button(self, text="학번 찾기", command=self.search_id).pack(pady=10)

    def search_id(self):
        input_name = self.name_entry.get().strip()

        if re.fullmatch(r'^[가-힣a-zA-Z\s]+$', input_name) is None:
            messagebox.showerror("입력 오류", "이름은 한글이나 영어만 입력해야 합니다.")
            return

        matches = []
        for student_id, data in self.controller.dynamic_grades.items():
            if student_id == ADMIN_ID:
                continue
            if data.get("name") == input_name:
                matches.append(student_id)

        if matches:
            if len(matches) == 1:
                messagebox.showinfo("결과", f"{input_name}님의 학번 : {matches[0]}")
            else:
                ids_text = "\n".join(matches)
                messagebox.showinfo("결과", f"{input_name}님 동명이인이 있습니다.\n학번 목록:\n{ids_text}")
            self.destroy()
        else:
            messagebox.showerror("오류", "해당 이름을 가진 학생이 데이터 파일에 없습니다.")
            self.name_entry.delete(0, tk.END)


class PageOne(tk.Frame):
    def __init__(self, parent, controller: MyApp):
        super().__init__(parent)
        self.controller = controller

        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)
        self.grid_columnconfigure(0, weight=1)

        tk.Label(self, text="성적 확인 및 분석 어플", font=HEADER_FONT).grid(row=0, column=0, pady=20)

        main = tk.Frame(self)
        main.grid(row=1, column=0, sticky="nsew", padx=50, pady=20)
        main.grid_columnconfigure(0, weight=2)
        main.grid_columnconfigure(1, weight=3)
        main.grid_rowconfigure(0, weight=1)

        self.graph_frame = tk.LabelFrame(main, text="성적 분석 그래프", font=(KOREAN_FONT_FAMILY, 14, "bold"), bd=2)
        self.graph_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        self.graph_canvas = tk.Canvas(self.graph_frame, bg="white")
        self.graph_canvas.pack(expand=True, fill="both", padx=10, pady=10)

        left_panel = tk.Frame(main)
        left_panel.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        self.name_frame = tk.LabelFrame(left_panel, text="사용자 정보", font=(KOREAN_FONT_FAMILY, 10), bd=3)
        self.name_frame.pack(anchor="nw")

        self.name_label = tk.Label(self.name_frame, text="이름 : ", font=BOLD_LARGE_FONT)
        self.name_label.pack(padx=20, pady=(10, 0), anchor="w")

        self.id_label = tk.Label(self.name_frame, text="학번: ", font=(KOREAN_FONT_FAMILY, 12, "bold"))
        self.id_label.pack(padx=20, pady=(0, 10), anchor="w")

        self.grade_table_frame = tk.Frame(left_panel)
        self.grade_table_frame.pack(anchor="nw", pady=(30, 0))
        self.create_table_header(self.grade_table_frame, "grade")
        self.grade_rows = []

        self.score_table_frame = tk.Frame(left_panel)
        self.score_table_frame.pack(anchor="nw", pady=30)
        self.create_table_header(self.score_table_frame, "score")
        self.score_rows = []

        bottom = tk.Frame(self)
        bottom.grid(row=2, column=0, sticky="se", padx=50, pady=50)
        ttk.Button(bottom, text="▶", style="Next.TButton", command=lambda: controller.show_frame(PageTwo)).pack()
        tk.Label(bottom, text="핵심 역량 상세", font=(KOREAN_FONT_FAMILY, 14)).pack(pady=5)

    def create_table_header(self, parent_frame, header_type):
        headers = ["과목", "본인 등급", "평균 등급"] if header_type == "grade" else ["과목", "본인 점수", "평균 점수"]
        header_font = (KOREAN_FONT_FAMILY, 14, "bold")
        header_bg = "#DDDDDD"
        for col, text in enumerate(headers):
            tk.Label(parent_frame, text=text, font=header_font, width=15,
                     relief="solid", borderwidth=1, bg=header_bg).grid(row=0, column=col, sticky="nsew")

    def clear_grade_rows(self):
        for row in self.grade_rows:
            for w in row:
                try:
                    w.destroy()
                except:
                    pass
        for row in self.score_rows:
            for w in row:
                try:
                    w.destroy()
                except:
                    pass
        self.grade_rows = []
        self.score_rows = []
        self.graph_canvas.delete("all")

    def load_user_data(self):
        self.clear_grade_rows()

        user = self.controller.current_user_data
        if not user:
            self.name_label.config(text="이름 : (로그인되지 않음)")
            self.id_label.config(text="학번: ")
            return

        sid = user["user_id"]
        student = self.controller.dynamic_grades.get(sid)
        if not student or not student.get("subjects"):
            self.name_label.config(text=f"이름 : {user['name']}")
            self.id_label.config(text=f"학번: {user['student_id']}")
            return

        self.name_label.config(text=f"이름 : {student.get('name', user['name'])}")
        self.id_label.config(text=f"학번: {user['student_id']}")

        grades = student["subjects"]
        graph_data = []
        row_index = 1

        for subject_name, data in grades.items():
            sub_label = tk.Label(self.grade_table_frame, text=subject_name, font=(KOREAN_FONT_FAMILY, 14),
                                 width=15, relief="groove", borderwidth=1)
            sub_label.grid(row=row_index, column=0, sticky="nsew")
            g1 = tk.Label(self.grade_table_frame, text=data.get("earned_grade", "N/A"),
                          font=(KOREAN_FONT_FAMILY, 14), width=15, relief="groove", borderwidth=1)
            g2 = tk.Label(self.grade_table_frame, text=data.get("avg_grade", "N/A"),
                          font=(KOREAN_FONT_FAMILY, 14), width=15, relief="groove", borderwidth=1)
            g1.grid(row=row_index, column=1, sticky="nsew")
            g2.grid(row=row_index, column=2, sticky="nsew")
            self.grade_rows.append([sub_label, g1, g2])

            sub_label2 = tk.Label(self.score_table_frame, text=subject_name, font=(KOREAN_FONT_FAMILY, 14),
                                  width=15, relief="groove", borderwidth=1)
            sub_label2.grid(row=row_index, column=0, sticky="nsew")
            s1 = tk.Label(self.score_table_frame, text=f"{data.get('score', 0):.1f}",
                          font=(KOREAN_FONT_FAMILY, 14), width=15, relief="groove", borderwidth=1)
            s2 = tk.Label(self.score_table_frame, text=f"{data.get('avg_score', 0):.1f}",
                          font=(KOREAN_FONT_FAMILY, 14), width=15, relief="groove", borderwidth=1)
            s1.grid(row=row_index, column=1, sticky="nsew")
            s2.grid(row=row_index, column=2, sticky="nsew")
            self.score_rows.append([sub_label2, s1, s2])

            graph_data.append({
                "subject": subject_name,
                "score": data.get("score", 0),
                "avg_score": data.get("avg_score", 0)
            })
            row_index += 1

        self.graph_canvas.update_idletasks()
        if graph_data:
            self.draw_graph(graph_data)

    def draw_graph(self, data):
        canvas = self.graph_canvas
        canvas.delete("all")
        canvas.update_idletasks()

        w = canvas.winfo_width()
        h = canvas.winfo_height()
        if w < 200 or h < 200:
            return

        padding = 40
        graph_w = w - 2 * padding
        graph_h = h - 2 * padding
        scale = graph_h / 100
        x_axis_y = padding + graph_h

        # 축 그리기
        canvas.create_line(padding, x_axis_y, padding + graph_w, x_axis_y, fill="black", width=2)
        canvas.create_line(padding, padding, padding, x_axis_y, fill="black", width=2)

        # Y축 라벨
        canvas.create_text(padding - 15, x_axis_y, anchor='e', text="0", font=("Arial", 10))
        canvas.create_text(padding - 15, padding, anchor='e', text="100", font=("Arial", 10))
        y50 = x_axis_y - 50 * scale
        canvas.create_line(padding, y50, padding + graph_w, y50, fill="gray", dash=(4, 4))
        canvas.create_text(padding - 15, y50, anchor='e', text="50", font=("Arial", 10), fill="gray")

        num = len(data)
        group_gap = 20
        inner_gap = 6

        total_bar = num * 2
        bar_w = max(12, int((graph_w - num * group_gap) / total_bar))

        x = padding + 10
        for item in data:
            s = float(item["score"])
            a = float(item["avg_score"])

            hs = s * scale
            ha = a * scale

            # 본인 점수 막대
            x1 = x
            x2 = x + bar_w
            y1 = x_axis_y - hs
            canvas.create_rectangle(x1, y1, x2, x_axis_y, fill="#4CAF50", outline="")
            canvas.create_text((x1 + x2) / 2, y1 - 10, text=f"{s:.1f}", font=("Arial", 10), fill="#4CAF50")

            # 평균 점수 막대
            x1a = x2 + inner_gap
            x2a = x1a + bar_w
            y1a = x_axis_y - ha
            canvas.create_rectangle(x1a, y1a, x2a, x_axis_y, fill="#2196F3", outline="")
            canvas.create_text((x1a + x2a) / 2, y1a - 10, text=f"{a:.1f}", font=("Arial", 10), fill="#2196F3")

            # 과목명
            cx = (x + x2a) / 2
            canvas.create_text(cx, x_axis_y + 15, anchor='n', text=item["subject"], font=(KOREAN_FONT_FAMILY, 10))
            x = x2a + group_gap

        # 범례
        ly = padding - 15
        canvas.create_rectangle(padding, ly - 10, padding + 10, ly, fill="#4CAF50", outline="")
        canvas.create_text(padding + 15, ly - 5, anchor="w", text="본인 점수", font=(KOREAN_FONT_FAMILY, 10))

        canvas.create_rectangle(padding + 100, ly - 10, padding + 110, ly, fill="#2196F3", outline="")
        canvas.create_text(padding + 115, ly - 5, anchor="w", text="평균 점수", font=(KOREAN_FONT_FAMILY, 10))


class PageTwo(tk.Frame):
    
    # 1. CORE_COMPETENCIES (클래스 변수로 정의)
    CORE_COMPETENCIES = {
        "기초 이론 이해": "핵심 개념을 정리하면 점수가 안정적으로 올라갑니다. (정의→예제→요약 루틴 추천)",
        "개념 적용 및 구현": "배운 개념을 코드로 구현하는 연습이 필요합니다. 예제 변형 과제를 해보세요.",
        "문제 해결": "문제를 단계로 쪼개는 훈련이 좋습니다. (입력→처리→출력 흐름으로 정리)",
        "데이터 분석 및 해석": "결과를 설명하는 연습이 필요합니다. 그래프/수치에서 ‘원인→결론’을 말해보세요.",
        "프로그래밍 활용": "라이브러리 활용 경험을 늘리면 좋습니다. 작은 기능을 매주 1개씩 구현해보세요.",
        "자기 주도적 학습": "복습/기록/적용 루틴을 만들면 성장 속도가 빨라집니다. 학습 로그 작성 권장" 
    }
    
    # 2. COMP_FEEDBACK (점수 구간별 상세 코멘트)
    # RADAR_MAX_SCORE = 60에 맞추어 구간 설정
    COMP_FEEDBACK = {
        "기초 이론 이해": {
            "0-15": "핵심 개념이 아직 불안정합니다. ‘정의→예제→요약’ 루틴으로 기초를 다시 잡아보세요.",
            "16-30": "기초는 있으나 흔들릴 수 있습니다. 개념노트 1회독 + 대표 유형 10문제 반복을 권장합니다.",
            "31-45": "개념이 안정권입니다. 단원별 약점만 골라 보완하면 상위권으로 올라갈 수 있어요.",
            "46-60": "이론 이해가 매우 탄탄합니다. 심화 개념(증명/원리)까지 확장해도 좋습니다."
        },
        "개념 적용 및 구현": {
            "0-15": "개념을 코드로 옮기는 연결이 약합니다. 예제 코드를 따라치며 ‘왜 이렇게 되는지’ 설명해보세요.",
            "16-30": "구현은 가능하지만 실수가 생길 수 있습니다. 예제 변형 과제를 2~3개씩 추가로 해보세요.",
            "31-45": "구현 감각이 좋습니다. 입력/예외처리/함수화까지 포함해 완성도를 올려보세요.",
            "46-60": "적용·구현 능력이 매우 우수합니다. 미니 프로젝트로 포트폴리오화하면 강점이 됩니다."
        },
        "문제 해결": {
            "0-15": "문제를 쪼개는 전략이 필요합니다. ‘입력→처리→출력’ 단계로 풀이 틀부터 잡아보세요.",
            "16-30": "접근은 가능하지만 흐름이 끊길 수 있습니다. 풀이 과정을 글로 적는 습관을 추천합니다.",
            "31-45": "문제 해결 흐름이 안정적입니다. 시간/공간 효율까지 한 번 더 점검해보세요.",
            "46-60": "문제 해결 능력이 뛰어납니다. 난이도 높은 응용 문제로 실력을 더 끌어올릴 수 있어요."
        },
        "데이터 분석 및 해석": {
            "0-15": "결과를 읽고 의미를 뽑는 연습이 필요합니다. 그래프/수치에서 ‘원인→결론’을 말해보세요.",
            "16-30": "해석은 가능하지만 근거가 약할 수 있습니다. 비교 기준(평균/분포/추세)을 세워보세요.",
            "31-45": "분석 관점이 좋습니다. 가설을 세우고 검증하는 방식으로 한 단계 확장해보세요.",
            "46-60": "해석 능력이 매우 우수합니다. 보고서 형태(문제-분석-결론)로 정리하면 강점이 됩니다."
        },
        "프로그래밍 활용": {
            "0-15": "문법/라이브러리 사용이 아직 낯설 수 있습니다. 자주 쓰는 문법 20개를 고정 루틴으로 만드세요.",
            "16-30": "기본은 있으나 활용 폭이 좁을 수 있습니다. 파일/그래프/GUI 중 한 가지를 집중 강화해보세요.",
            "31-45": "활용 능력이 좋습니다. 코드 구조화(클래스/모듈 분리)로 실력을 더 끌어올릴 수 있어요.",
            "46-60": "프로그래밍 활용이 매우 뛰어납니다. 기능 추가/리팩토링까지 가능한 수준입니다."
        },
        "자기 주도적 학습": {
            "0-15": "학습 루틴이 먼저 필요합니다. ‘매일 30분-기록-복습’ 작은 습관부터 시작해보세요.",
            "16-30": "학습은 하고 있으나 지속성이 약할 수 있습니다. 주간 목표(2~3회)와 체크리스트를 추천합니다.",
            "31-45": "자기주도 학습이 안정적입니다. 학습한 것을 ‘요약→적용’까지 연결해보세요.",
            "46-60": "확장 학습 능력이 매우 우수합니다. 심화 자료/논문/프로젝트로 성장 속도를 더 낼 수 있어요."
        }
    }

    # 3. feedback_by_score (인스턴스 메서드로 정의)
    def feedback_by_score(self, comp_name, score):
        """0~60 점수 기준: 구간별 코멘트 반환"""
        if score <= 15:
            key = "0-15"
        elif score <= 30:
            key = "16-30"
        elif score <= 45:
            key = "31-45"
        else: # 46 ~ 60
            key = "46-60"
        return self.COMP_FEEDBACK.get(comp_name, {}).get(key, "분석 데이터 부족")


    def __init__(self, parent, controller: MyApp):
        super().__init__(parent)
        self.controller = controller

        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)
        self.grid_columnconfigure(0, weight=1)

        tk.Label(self, text="핵심 역량 상세", font=HEADER_FONT).grid(row=0, column=0, pady=30)

        main = tk.Frame(self)
        main.grid(row=1, column=0, sticky="nsew", padx=50, pady=20)
        main.grid_columnconfigure(0, weight=1)
        main.grid_columnconfigure(1, weight=2)

        left = tk.Frame(main)
        left.grid(row=0, column=0, sticky="nwe", padx=20, pady=10)
        tk.Label(left, text="핵심 역량 종류", font=BOLD_LARGE_FONT).pack(anchor="w", pady=(0, 15))

        self.comp_frame = tk.LabelFrame(left, text="", bd=2, relief="groove")
        self.comp_frame.pack(fill="x", anchor="n")

        right = tk.Frame(main)
        right.grid(row=0, column=1, sticky="nsew", padx=20, pady=10)
        tk.Label(right, text="레이더 차트", font=BOLD_LARGE_FONT).pack(anchor="w", pady=(0, 15))

        self.radar_canvas = tk.Canvas(right, bg="white", height=400)
        self.radar_canvas.pack(fill="both", expand=True)

        bottom = tk.Frame(self)
        bottom.grid(row=2, column=0, sticky="ew", padx=50, pady=50)
        bottom.grid_columnconfigure(0, weight=1)
        bottom.grid_columnconfigure(1, weight=1)

        left_btn = tk.Frame(bottom)
        left_btn.grid(row=0, column=0, sticky="w")
        ttk.Button(left_btn, text="◀", style="Next.TButton", command=lambda: controller.show_frame(PageOne)).pack()
        tk.Label(left_btn, text="성적 확인", font=(KOREAN_FONT_FAMILY, 14)).pack(pady=5)

        right_btn = tk.Frame(bottom)
        right_btn.grid(row=0, column=1, sticky="e")
        ttk.Button(right_btn, text="▶", style="Next.TButton", command=lambda: controller.show_frame(PageThree)).pack()
        tk.Label(right_btn, text="핵심 역량 산출표", font=(KOREAN_FONT_FAMILY, 14)).pack(pady=5)

    def load_competency_data(self):
        user = self.controller.current_user_data
        if not user:
            return

        sid = user["user_id"]
        student = self.controller.dynamic_grades.get(sid)
        if not student or not student.get("subjects"):
            return

        # 과목 점수를 표준화된 PageThree.SUBJECTS 키에 맞게 가져옵니다.
        subj_scores = {}
        for sub in PageThree.SUBJECTS:
            if sub in student["subjects"]:
                subj_scores[sub] = float(student["subjects"][sub].get("score", 0.0))
            else:
                subj_scores[sub] = 0.0

        comp_scores_me = self.controller.calc_competency_scores(subj_scores)
        comp_scores_avg = self.controller.calc_average_competency_scores()

        for w in self.comp_frame.winfo_children():
            w.destroy()

        # 계산된 점수를 기반으로 구간별 코멘트 출력
        for i, comp_name in enumerate(self.CORE_COMPETENCIES.keys()):
            score = comp_scores_me.get(comp_name, 0.0)
            comment = self.feedback_by_score(comp_name, score)

            tk.Label(
                self.comp_frame,
                text=f"{i+1}. {comp_name} : {score:.2f}점",
                font=(KOREAN_FONT_FAMILY, 14, "bold"),
                pady=2, anchor="w"
            ).pack(fill="x", padx=10)

            tk.Label(
                self.comp_frame,
                text=f"- {comment}",
                font=(KOREAN_FONT_FAMILY, 12),
                pady=2, anchor="w", justify=tk.LEFT
            ).pack(fill="x", padx=15, pady=(0, 10))

        self.draw_radar_compare(comp_scores_me, comp_scores_avg)

    def draw_radar_compare(self, comp_scores_me, comp_scores_avg):
        c = self.radar_canvas
        c.delete("all")
        c.update_idletasks()

        w = c.winfo_width()
        h = c.winfo_height()
        if w < 200 or h < 200:
            return

        cx, cy = w // 2, h // 2
        radius = min(w, h) // 2 - 70
        if radius < 60:
            return

        axes = list(self.CORE_COMPETENCIES.keys())
        n = len(axes)
        step = 2 * math.pi / n

        # 레이더 차트 눈금 (최대 60)
        # 0, 15, 30, 45, 60
        for r_ratio in [0.0, 0.25, 0.50, 0.75, 1.0]:
            r = radius * r_ratio
            if r_ratio > 0:
                c.create_oval(cx - r, cy - r, cx + r, cy + r, outline="lightgray")
            
            score_label = RADAR_MAX_SCORE * r_ratio
            if score_label < 1.0: 
                 c.create_text(cx + 5, cy + 5, anchor="w", text="0", font=("Arial", 9), fill="gray")
            else:
                 c.create_text(cx + 5, cy - r, anchor="w",
                                text=f"{score_label:.1f}", font=("Arial", 9), fill="gray")

        # 축 및 라벨
        for i, axis in enumerate(axes):
            ang = i * step - math.pi / 2
            ex = cx + radius * math.cos(ang)
            ey = cy + radius * math.sin(ang)
            c.create_line(cx, cy, ex, ey, fill="gray")

            lx = cx + (radius + 30) * math.cos(ang)
            ly = cy + (radius + 30) * math.sin(ang)

            ax = math.cos(ang)
            anchor = "center"
            if ax > 0.4:
                anchor = "w"
            elif ax < -0.4:
                anchor = "e"

            c.create_text(lx, ly, text=axis, font=(KOREAN_FONT_FAMILY, 10), anchor=anchor)

        def clamp(v, lo=0.0, hi=60.0): # 점수 계산 결과는 0~60 사이이므로 hi를 60으로 설정
            try:
                v = float(v)
            except Exception:
                v = 0.0
            return max(lo, min(hi, v))

        def make_points(scores_dict):
            pts = []
            for i, axis in enumerate(axes):
                score = scores_dict.get(axis, 0.0)
                
                # 1. 값의 범위를 0 ~ 60으로 안전하게 제한
                score = max(0.0, min(RADAR_MAX_SCORE, score))
                
                # 2. 반지름 비율 계산 (현재 점수 / 60점)
                r = radius * (score / RADAR_MAX_SCORE)
                
                ang = i * step - math.pi / 2
                x = cx + r * math.cos(ang)
                y = cy + r * math.sin(ang)
                pts.extend([x, y])
            return pts

        pts_avg = make_points(comp_scores_avg)
        pts_me = make_points(comp_scores_me)

        # 전체 평균(파란색)을 먼저 그려서 밑에 깔리게 합니다.
        c.create_polygon(pts_avg, outline="#2196F3", fill="#2196F3", width=3, dash=(6, 4), stipple="gray25")

        # 본인 점수(빨간색)를 나중에 그려서 위에 덮이게 합니다.
        c.create_polygon(pts_me, outline="#e91e63", fill="#e91e63", width=3, stipple="gray50")

        # 범례 업데이트 (최대 60점 반영)
        ly = 18
        c.create_rectangle(20, ly, 36, ly + 12, fill="#e91e63", outline="")
        c.create_text(42, ly + 6, anchor="w", text=f"본인(최대 {int(RADAR_MAX_SCORE)})", font=(KOREAN_FONT_FAMILY, 11))

        c.create_rectangle(140, ly, 156, ly + 12, fill="#2196F3", outline="")
        c.create_text(162, ly + 6, anchor="w", text=f"전체 평균(최대 {int(RADAR_MAX_SCORE)})", font=(KOREAN_FONT_FAMILY, 11))


class PageThree(tk.Frame):
    # 과목명을 로드 키와 일치시키기 위해 수정
    SUBJECTS = ["파이썬기초및실습", "영상 이해", "알기쉬운확률통계"]

    # 핵심 역량 가중치: [파이썬기초및실습, 영상 이해, 알기쉬운확률통계] 순서
    COMPETENCY_WEIGHTS = {
        "기초 이론 이해": [10, 20, 30],
        "개념 적용 및 구현": [25, 20, 15],
        "문제 해결": [20, 20, 20],
        "데이터 분석 및 해석": [10, 30, 20],
        "프로그래밍 활용": [30, 15, 15],
        "자기 주도적 학습": [30, 15, 15] 
    }

    def __init__(self, parent, controller: MyApp):
        super().__init__(parent)
        self.controller = controller

        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)
        self.grid_columnconfigure(0, weight=1)

        title_frame = tk.Frame(self)
        title_frame.grid(row=0, column=0, sticky="n", pady=(50, 40))
        tk.Label(title_frame, text="핵심 역량 산출표", font=P3_HEADER_FONT).pack()

        main = tk.Frame(self)
        main.grid(row=1, column=0, sticky="n", padx=50, pady=0)

        self.table_frame = tk.Frame(main, bd=2, relief="solid")
        self.table_frame.pack(anchor="n")
        self.create_weight_table()

        self.formula_frame = tk.LabelFrame(main, text="역량 환산 방식", font=P3_TITLE_FONT, bd=3, relief="groove")
        self.formula_frame.pack(anchor="n", fill="x", pady=40)

        # 공식 설명 업데이트 (최종 60점 만점 반영)
        tk.Label(
            self.formula_frame,
            text="핵심 역량 점수 = (각 교과목 점수 x 가중치)의 합 (최대 60점)",
            font=P3_FORMULA_FONT, padx=10, pady=10, anchor="w"
        ).pack(fill="x")

        bottom = tk.Frame(self)
        bottom.grid(row=2, column=0, sticky="ew", padx=50, pady=50)
        bottom.grid_columnconfigure(0, weight=1)
        bottom.grid_columnconfigure(1, weight=1)

        left_btn = tk.Frame(bottom)
        left_btn.grid(row=0, column=0, sticky="w")
        ttk.Button(left_btn, text="◀", style="Next.TButton", command=lambda: controller.show_frame(PageTwo)).pack()
        tk.Label(left_btn, text="핵심 역량 상세", font=(KOREAN_FONT_FAMILY, 14)).pack(pady=5)

        right_btn = tk.Frame(bottom)
        right_btn.grid(row=0, column=1, sticky="e")
        ttk.Button(right_btn, text="▶", style="Next.TButton", command=lambda: controller.show_frame(PageFour)).pack()
        tk.Label(right_btn, text="총평", font=(KOREAN_FONT_FAMILY, 14)).pack(pady=5)

    def create_weight_table(self):
        comp_names = list(self.COMPETENCY_WEIGHTS.keys())
        header_font = P3_TITLE_FONT
        data_font = P3_DATA_FONT

        tk.Label(self.table_frame, text="교과목명", font=header_font, width=15,
                 relief="solid", borderwidth=1, bg="#DDDDDD").grid(row=0, column=0, sticky="nsew")

        for col_idx, comp_name in enumerate(comp_names):
            tk.Label(self.table_frame, text=comp_name, font=header_font, width=10,
                     relief="solid", borderwidth=1, bg="#DDDDDD",
                     wraplength=80).grid(row=0, column=col_idx + 1, sticky="nsew")

        for row_idx, subject in enumerate(self.SUBJECTS):
            tk.Label(self.table_frame, text=subject, font=header_font,
                     relief="solid", borderwidth=1, bg="#F0F0F0").grid(row=row_idx + 1, column=0, sticky="nsew")

            for col_idx, comp_name in enumerate(comp_names):
                weight_value = self.COMPETENCY_WEIGHTS[comp_name][row_idx]
                tk.Label(self.table_frame, text=f"{weight_value}%", font=data_font,
                         relief="groove", borderwidth=1).grid(row=row_idx + 1, column=col_idx + 1, sticky="nsew")


class PageFour(tk.Frame):
    def __init__(self, parent, controller: MyApp):
        super().__init__(parent)
        self.controller = controller

        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)
        self.grid_columnconfigure(0, weight=1)

        tk.Label(self, text="총평", font=P3_HEADER_FONT).grid(row=0, column=0, pady=50)

        main = tk.Frame(self)
        main.grid(row=1, column=0, sticky="n", padx=50, pady=20)

        self.report_block = tk.LabelFrame(main, text="", bd=3, relief="groove", padx=30, pady=30)
        self.report_block.pack(anchor="w")

        self.report_label = tk.Label(self.report_block, text="", font=P3_DATA_FONT, justify=tk.LEFT)
        self.report_label.pack(anchor="w")

        bottom = tk.Frame(self)
        bottom.grid(row=2, column=0, sticky="ew", padx=50, pady=50)
        bottom.grid_columnconfigure(0, weight=1)
        bottom.grid_columnconfigure(1, weight=1)

        left_btn = tk.Frame(bottom)
        left_btn.grid(row=0, column=0, sticky="w")
        ttk.Button(left_btn, text="◀", style="Next.TButton", command=lambda: controller.show_frame(PageThree)).pack()
        tk.Label(left_btn, text="핵심 역량 산출표", font=(KOREAN_FONT_FAMILY, 14)).pack(pady=5)

        right_btn = tk.Frame(bottom)
        right_btn.grid(row=0, column=1, sticky="e")
        ttk.Button(right_btn, text="로그아웃", style="Next.TButton", command=controller.logout).pack(side=tk.RIGHT)

    def load_report(self):
        user = self.controller.current_user_data
        if not user:
            self.report_label.config(text="로그인 정보가 없습니다.")
            return

        sid = user["user_id"]
        student = self.controller.dynamic_grades.get(sid)
        if not student or not student.get("subjects"):
            self.report_label.config(text="총평을 만들 데이터가 없습니다.")
            return

        user_name = student.get("name", user.get("name", ""))

        subj_scores = {s: d.get("score", 0) for s, d in student["subjects"].items()}
        comp_scores = self.controller.calc_competency_scores(subj_scores)

        if comp_scores:
            strong = max(comp_scores, key=comp_scores.get)
            weak = min(comp_scores, key=comp_scores.get)
        else:
            strong, weak = "N/A", "N/A"

        # 요청에 따라 마지막 문장을 제거했습니다.
        report_text = (
            f'"{user_name}" 님의 가장 강한 역량은 <{strong}> 입니다.\n\n'
            f"보완이 필요한 역량은 <{weak}> 입니다."
        )
        self.report_label.config(text=report_text)


if __name__ == "__main__":
    app = MyApp()
    app.mainloop()

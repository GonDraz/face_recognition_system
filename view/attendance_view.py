from tkinter import *
from tkinter import ttk
from tkcalendar import DateEntry

from PIL import Image, ImageTk


import pandas as pd

from store.assets import *


class AttendanceView:
    def __init__(self, root, controller):
        self.controller = controller
        self.root = root

        # ==============Variable================#

        self.var_std_id = StringVar()
        self.var_std_name = StringVar()
        self.var_note = StringVar()

        self.date_var = StringVar()
        self.from_date_var = StringVar()
        self.to_date_var = StringVar()

        # bg imag
        self.backgroundImg = ImageTk.PhotoImage(
            Images.background.resize((1500, 710), Image.ANTIALIAS))

        bg_img = Label(self.root, image=self.backgroundImg)
        bg_img.place(x=0, y=0, width=1500, height=700)
        self.main_frame = Frame(bg_img, bd=2, bg=Colors.background)
        self.main_frame.place(x=0, y=50, width=1400, height=600)

        self.left_frame = LabelFrame(self.main_frame, bd=2, bg=Colors.background,
                                     relief=RIDGE, text="Báo cáo theo ngày", font=(Fonts.primary, 12, "bold"))
        self.left_frame.place(x=10, y=10, width=650, height=520)

        self.right_frame = LabelFrame(self.main_frame, bd=2, bg=Colors.background, relief=RIDGE,
                                      text="Biểu đồ thống kê số lượng SV vắng", font=(Fonts.primary, 12, "bold"))
        self.right_frame.place(x=685, y=10, width=650, height=520)

        self.chart_frame = Frame(self.right_frame)
        self.chart_frame.place(x=20, y=58, width=605, height=420)

        #=================================================================#

        self.table_frame = Frame(
            self.left_frame, bd=2, bg=Colors.background, relief=RIDGE)
        self.table_frame.place(x=5, y=55, width=490, height=430)

        # Scroll_x=ttk.Scrollbar(table_Frame,orient=HORIZONTAL)
        Scroll_y = ttk.Scrollbar(self.table_frame, orient=VERTICAL)

        self.student_table = ttk.Treeview(
            self.table_frame, column=("Atd", "id", "name", "note"))
        self.student_table.bind("<Double-1>", self.controller.onDoubleClicked)

        # Scroll_x.pack(side=BOTTOM,fill=X)
        Scroll_y.pack(side=RIGHT, fill=Y)
        # Scroll_x.config(command=self.student_table.xview)
        Scroll_y.config(command=self.student_table.yview)

        self.student_table.heading("Atd", text="Điểm danh")
        self.student_table.heading("id", text="MSSV")
        self.student_table.heading("name", text="Tên")
        self.student_table.heading("note", text="Ghi chú")

        self.student_table["show"] = "headings"

        self.student_table.column("Atd", width=100)
        self.student_table.column("id", width=100)
        self.student_table.column("name", width=100)
        self.student_table.column("note", width=100)

        self.student_table.pack(fill=BOTH, expand=1)

        #=========================================#

        Button(self.main_frame, text="Nhập danh sách lớp", width=16, font=(
            Fonts.primary, 14, "bold"), bg=Colors.button, fg=Colors.textButton, command=self.controller.importClass).place(x=575, y=550)

        Button(self.left_frame, text="Sửa báo cáo", width=12, font=(
            Fonts.primary, 12, "bold"), bg=Colors.button, fg=Colors.textButton, command=self.controller.importReport).place(x=506, y=180)

        Button(self.left_frame, text="Xuất báo cáo", width=12, font=(
            Fonts.primary, 12, "bold"), bg=Colors.button, fg=Colors.textButton, command=self.controller.exportReport).place(x=506, y=280)

        Button(self.left_frame, text="Cập nhật", width=10, font=(
            Fonts.primary, 12, "bold"), bg=Colors.button, fg=Colors.textButton, command=self.controller.updateTable).place(x=270, y=8)

        Button(self.right_frame, text="Cập nhật", width=10, font=(
            Fonts.primary, 12, "bold"), bg=Colors.button, fg=Colors.textButton, command=self.controller.updateChart).place(x=506, y=10)

        #=========================================#

        date_label = Label(self.left_frame, text="Ngày:",
                           font=(Fonts.primary, 12, "bold"), bg=Colors.background)
        date_label.place(x=5, y=12)

        from_date_label = Label(self.right_frame, text="Từ:", font=(
            Fonts.primary, 12, "bold"), bg=Colors.background)
        from_date_label.place(x=5, y=16)

        to_date_label = Label(self.right_frame, text="Đến:",
                              font=(Fonts.primary, 12, "bold"), bg=Colors.background)
        to_date_label.place(x=245, y=16)

        #=========================================#

        self.date_entry = DateEntry(self.left_frame, textvariable=self.date_var, width=17, font=(
            Fonts.primary, 12, "bold"), date_pattern='dd/mm/y')
        self.date_entry.place(x=70, y=12)

        self.from_date_entry = DateEntry(self.right_frame, textvariable=self.from_date_var, width=17, font=(
            Fonts.primary, 12, "bold"), date_pattern='dd/mm/y')
        self.from_date_entry.place(x=55, y=16)

        self.to_date_entry = DateEntry(self.right_frame, textvariable=self.to_date_var, width=17, font=(
            Fonts.primary, 12, "bold"), date_pattern='dd/mm/y')
        self.to_date_entry.place(x=300, y=16)

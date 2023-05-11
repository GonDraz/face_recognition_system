from tkinter import END, filedialog, messagebox
from tkinter import *


import os
import csv
import pandas as pd
import tkinter as tk
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime

from models.attendance_model import AttendanceModel
from store.window_setup import WindowSetup
from view.attendance_view import AttendanceView


class AttendanceController:
    def __init__(self, root):

        self.root = root
        self.root.geometry(WindowSetup.screen)
        self.root.title("Báo cáo điểm danh")
        self.model = AttendanceModel()
        self.view = AttendanceView(root, self)

        self.student_df = pd.DataFrame()
        self.attendances = []
        self.times = {}

        self.root.mainloop()

    #========== import class function ========#

    def importClass(self):
        fln = filedialog.askopenfilename(initialdir=os.getcwd(), title="Open CSV", filetypes=(
            ("CSV File", "*.csv"), ("All File", "*.*")), parent=self.view.root)
        if (len(fln) == 0):
            return
        try:
            self.student_df = pd.read_csv(fln)
            messagebox.showinfo("Success", "Thành công", parent=self.view.root)
        except Exception as es:
            messagebox.showerror(
                "Error", "Định dạng file không hợp lệ", parent=self.view.root)

    #========== import report function ========#
    def importReport(self):
        fln = filedialog.askopenfilename(initialdir=os.getcwd(), title="Open CSV", filetypes=(
            ("CSV File", "*.csv"), ("All File", "*.*")), parent=self.view.root)
        if (len(fln) == 0):
            return
        try:
            self.view.student_table.delete(
                *self.view.student_table.get_children())

            with open(fln, "r", newline='', encoding="utf-8") as f:
                csv_reader = csv.reader(f)
                line_count = 0

                for row in csv_reader:
                    self.times = {}
                    self.attendances = []

                    line_count += 1

                    if line_count != 1:
                        if row[1] != '':
                            if row[0] != 'Vắng':
                                self.attendances.append(row[1])
                                self.times[row[1]] = row[0]
                            self.view.student_table.insert("", END, values=row)
                    else:
                        if row[0] != '\ufeffĐiểm danh' or row[1] != 'MSSV' or row[2] != 'Họ và tên' or row[3] != 'Ghi chú':
                            messagebox.showerror(
                                "Error", "Định dạng file không hợp lệ", parent=self.root)
                            return

            messagebox.showinfo("Success", "Thành công", parent=self.view.root)
        except Exception as es:
            messagebox.showerror(
                "Error", "Định dạng file không hợp lệ", parent=self.view.root)

    #========== export report function ========#
    def exportReport(self):
        fln = filedialog.asksaveasfilename(initialdir=os.getcwd(), title="Open CSV", filetypes=(
            ("CSV File", "*.csv"), ("All File", "*.*")), parent=self.root)
        if (len(fln) == 0):
            return
        try:
            date = self.view.date_var.get()
            date = date.replace('/', '_')

            with open(fln, "w", newline='', encoding="utf-8") as f:
                f.write('\ufeff')
                writer = csv.writer(f)
                writer.writerows(
                    [("Điểm danh", "MSSV", "Họ và tên", "Ghi chú")])
                line_count = 0
                writer = csv.writer(f)
                for line in self.view.student_table.get_children():
                    line_count += 1
                    data = self.view.student_table.item(line)["values"]
                    writer.writerows([(data[0], data[1], data[2], data[3])])
                writer.writerows(
                    [(f"Sĩ số ngày {date}: {len(self.attendances)} / {line_count}", "")])
                messagebox.showinfo(
                    "Success", f"Sĩ số ngày {date}: {len(self.attendances)} / {line_count}", parent=self.view.root)
        except Exception as es:
            messagebox.showerror(
                "Error", f"due to :{str(es)}", parent=self.view.root)

    #========== handle double clicked function ========#
    def onDoubleClicked(self, event):
        selected_item = self.student_table.selection()[0]
        values = self.student_table.item(selected_item, "values")

        if values[0] != 'Vắng':
            return

        if values[3] == '':
            self.student_table.item(selected_item, text="blub", values=(
                values[0], values[1], values[2], 'Có phép'))
        else:
            self.student_table.item(selected_item, text="blub", values=(
                values[0], values[1], values[2], ''))

    #========== update chart function ========#
    def updateChart(self):
        if self.student_df.empty:
            messagebox.showerror(
                "Error", f"Vui lòng nhập dữ liệu lớp trước!", parent=self.view.root)
            return

        from_date = datetime.strptime(
            self.view.from_date_var.get(), "%d/%m/%Y")
        to_date = datetime.strptime(self.view.to_date_var.get(), "%d/%m/%Y")

        directory = 'attendance'
        self.student_df['absents'] = 0

        for filename in os.listdir(directory):
            data_path = os.path.join(directory, filename)
            if os.path.isfile(data_path):
                splited = filename.split('.')
                current_date = datetime.strptime(splited[0], "%d_%m_%Y")
                if current_date >= from_date and current_date <= to_date:
                    attendances = []
                    with open(data_path, "r", encoding="utf-8") as f:
                        csv_reader = csv.reader(f)
                        for row in csv_reader:
                            attendances.append(row[1])
                    for row in self.student_df.index:
                        if str(self.student_df['studentID'][row]) not in attendances:
                            self.student_df['absents'][row] += 1

        data = {
            'type': ['1', '2', '3', '4', '>4'],
            'numOfStudents': [0, 0, 0, 0, 0]
        }

        for row in self.student_df.index:
            if self.student_df['absents'][row] == 0:
                continue
            elif self.student_df['absents'][row] <= 4:
                data['numOfStudents'][self.student_df['absents'][row] - 1] += 1
            else:
                data['numOfStudents'][4] += 1

        df = pd.DataFrame(data)

        x_axis = df['type']
        y_axis = df['numOfStudents']

        # Figure size
        fig = plt.figure(figsize=(16, 9))
        # Add subplot
        ax = fig.add_subplot()
        # Horizontal bar plot
        ax.bar(x_axis, y_axis)

        for bar in ax.patches:
            ax.annotate(bar.get_height(),
                        (bar.get_x() + bar.get_width() / 2,
                         bar.get_height()), ha='center', va='center',
                        size=8, xytext=(0, 8),
                        textcoords='offset points')

        ax.set_xlabel('Số buổi vắng')
        ax.set_ylabel('Số học sinh')

        ax.set_ylim([0, 100])

        for widget in self.view.chart_frame.winfo_children():
            widget.destroy()

        canvas = FigureCanvasTkAgg(fig, self.view.chart_frame)
        canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)

        plt.close(fig)

    #========== update table function ========#
    def updateTable(self):
        if self.student_df.empty:
            messagebox.showerror(
                "Error", f"Vui lòng nhập dữ liệu lớp trước!", parent=self.view.root)
            return

        date = self.view.date_var.get()
        date = date.replace('/', '_')

        data_path = f"attendance/{date}.csv"

        try:
            with open(data_path, "r", encoding="utf-8") as f:
                self.times = {}
                self.attendances = []
                csv_reader = csv.reader(f)
                for row in csv_reader:
                    self.attendances.append(row[1])
                    self.times[row[1]] = row[0]
        except Exception as es:
            import traceback
            traceback.print_exc()
            messagebox.showerror(
                "Error", f"Không có báo cáo của ngày {self.view.date_var.get()}", parent=self.view.root)
            return

        self.view.student_table.delete(*self.view.student_table.get_children())

        for row in self.student_df.index:
            if str(self.student_df['studentID'][row]) in self.attendances:
                self.view.student_table.insert("", END, values=[
                    self.times[str(self.student_df['studentID'][row])],
                    self.student_df['studentID'][row],
                    self.student_df['studentName'][row],
                    ''
                ])
            else:
                self.view.student_table.insert("", END, values=[
                    'Vắng',
                    self.student_df['studentID'][row],
                    self.student_df['studentName'][row],
                    ''
                ])

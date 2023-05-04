from tkinter import *
from tkinter import messagebox, ttk, filedialog

import mysql.connector
from PIL import Image, ImageTk

import cv2
import os
import csv
import numpy as np
import json
import shutil

import cv2
import numpy as np
import math

from store.assets import *
from store.window_setup import WindowSetup

# from face_detector import get_face_detector, find_faces


def get_2d_points(img, rotation_vector, translation_vector, camera_matrix, val):
    """Return the 3D points present as 2D for making annotation box"""
    point_3d = []
    dist_coeffs = np.zeros((4, 1))
    rear_size = val[0]
    rear_depth = val[1]
    point_3d.append((-rear_size, -rear_size, rear_depth))
    point_3d.append((-rear_size, rear_size, rear_depth))
    point_3d.append((rear_size, rear_size, rear_depth))
    point_3d.append((rear_size, -rear_size, rear_depth))
    point_3d.append((-rear_size, -rear_size, rear_depth))

    front_size = val[2]
    front_depth = val[3]
    point_3d.append((-front_size, -front_size, front_depth))
    point_3d.append((-front_size, front_size, front_depth))
    point_3d.append((front_size, front_size, front_depth))
    point_3d.append((front_size, -front_size, front_depth))
    point_3d.append((-front_size, -front_size, front_depth))
    point_3d = np.array(point_3d, dtype=np.float).reshape(-1, 3)

    # Map to 2d img points
    (point_2d, _) = cv2.projectPoints(point_3d,
                                      rotation_vector,
                                      translation_vector,
                                      camera_matrix,
                                      dist_coeffs)
    point_2d = np.int32(point_2d.reshape(-1, 2))
    return point_2d


def draw_annotation_box(img, rotation_vector, translation_vector, camera_matrix,
                        rear_size=300, rear_depth=0, front_size=500, front_depth=400,
                        color=(255, 255, 0), line_width=2):
    """
    Draw a 3D anotation box on the face for head pose estimation

    Parameters
    ----------
    img : np.unit8
        Original Image.
    rotation_vector : Array of float64
        Rotation Vector obtained from cv2.solvePnP
    translation_vector : Array of float64
        Translation Vector obtained from cv2.solvePnP
    camera_matrix : Array of float64
        The camera matrix
    rear_size : int, optional
        Size of rear box. The default is 300.
    rear_depth : int, optional
        The default is 0.
    front_size : int, optional
        Size of front box. The default is 500.
    front_depth : int, optional
        Front depth. The default is 400.
    color : tuple, optional
        The color with which to draw annotation box. The default is (255, 255, 0).
    line_width : int, optional
        line width of lines drawn. The default is 2.

    Returns
    -------
    None.

    """

    rear_size = 1
    rear_depth = 0
    front_size = img.shape[1]
    front_depth = front_size * 2
    val = [rear_size, rear_depth, front_size, front_depth]
    point_2d = get_2d_points(img, rotation_vector,
                             translation_vector, camera_matrix, val)


face_classifier = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')


def face_cropped(img1):
    gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray, 1.3, 5)
    # Scaling factor=1.3
    # Minimum neighbor=5

    for (x, y, w, h) in faces:
        face_cropped = img1[y:y + h, x:x + w]
        return face_cropped


def head_pose_points(img, rotation_vector, translation_vector, camera_matrix):
    """
    Get the points to estimate head pose sideways

    Parameters
    ----------
    img : np.unit8
        Original Image.
    rotation_vector : Array of float64
        Rotation Vector obtained from cv2.solvePnP
    translation_vector : Array of float64
        Translation Vector obtained from cv2.solvePnP
    camera_matrix : Array of float64
        The camera matrix

    Returns
    -------
    (x, y) : tuple
        Coordinates of line to estimate head pose

    """
    rear_size = 1
    rear_depth = 0
    front_size = img.shape[1]
    front_depth = front_size * 2
    val = [rear_size, rear_depth, front_size, front_depth]
    point_2d = get_2d_points(img, rotation_vector,
                             translation_vector, camera_matrix, val)
    y = (point_2d[5] + point_2d[8]) // 2
    x = point_2d[2]

    return (x, y)


class StudentView:
    title = "Thông tin sinh viên"

    def __init__(self, root, controller):
        self.controller = controller
        self.root = root

        # ==============Variable================
        self.var_dep = StringVar()
        self.var_course = StringVar()
        self.var_year = StringVar()
        self.var_semester = StringVar()
        self.var_std_id = StringVar()
        self.var_std_name = StringVar()
        self.var_div = StringVar()
        self.var_roll = StringVar()
        self.var_gender = StringVar()
        self.var_dob = StringVar()
        self.var_mail = StringVar()
        self.var_phone = StringVar()
        self.var_address = StringVar()
        self.var_teacher = StringVar()

        #first imag
        self.smeImg = ImageTk.PhotoImage(
            Images.sme.resize((450, 50), Image.ANTIALIAS))
        Label(self.root, image=self.smeImg).place(
            x=0, y=0, width=500, height=50)

        #second imag
        self.HUSTImg = ImageTk.PhotoImage(
            Images.HUST.resize((450, 50), Image.ANTIALIAS))
        Label(self.root, image=self.HUSTImg).place(
            x=450, y=0, width=500, height=50)

        #third imag
        self.HUST1Img = ImageTk.PhotoImage(
            Images.HUST1.resize((450, 50), Image.ANTIALIAS))
        Label(self.root, image=self.HUST1Img).place(
            x=900, y=0, width=500, height=50)

        #bg imag
        self.backgroundImg = ImageTk.PhotoImage(
            Images.background.resize((1530, 710), Image.ANTIALIAS))

        BackgroundImgFrame = Label(self.root, image=self.backgroundImg)
        BackgroundImgFrame .place(x=0, y=0, width=1530, height=700)

        mainFrame = Frame(BackgroundImgFrame, bd=2, bg=Colors.background)
        mainFrame.place(x=0, y=30, width=1500, height=800)

        Label(mainFrame, text="THÔNG TIN SINH VIÊN", font=(Fonts.primary, 18, "bold"),
              bg=Colors.background, fg=Colors.highlightText).place(x=0, y=0, width=1530, height=30)

        # left label frame
        Left_Frame = LabelFrame(mainFrame, bd=2, bg=Colors.background, relief=RIDGE,
                                text="ĐĂNG KÝ THÔNG TIN", font=(Fonts.primary, 12, "bold"))
        Left_Frame.place(x=0, y=30, width=660, height=600)

        self.photoImg_left = ImageTk.PhotoImage(
            Images.sis.resize((710, 130), Image.ANTIALIAS))
        Label(Left_Frame, image=self.photoImg_left).place(
            x=5, y=0, width=720, height=130)

        # current information course
        currentCourseFrame = LabelFrame(
            Left_Frame, bd=2, bg=Colors.background, relief=RIDGE, text="KHÓA HỌC", font=(Fonts.primary, 12, "bold"))
        currentCourseFrame.place(x=5, y=135, width=720, height=150)

        # Department
        dep_label = Label(currentCourseFrame, text="Ngành học",
                          font=(Fonts.primary, 12, "bold"), bg=Colors.background)
        dep_label.grid(row=0, column=0, padx=10, sticky=W)

        dep_combo = ttk.Combobox(currentCourseFrame, textvariable=self.var_dep, font=(
            Fonts.primary, 12, "bold"), state="read only", width=20)
        dep_combo["values"] = ["Chọn ngành", "Cơ Khí", "Cơ điện tử", "CNTT",
                               "KHMT", "KTMT", "Điện", "Tự Động Hóa", "CNSP", "ĐTVT", "Hóa học"]
        dep_combo.current(0)
        dep_combo.grid(row=0, column=1, pady=10, sticky=W)

        # Course
        course_label = Label(currentCourseFrame, text="Khóa",
                             font=(Fonts.primary, 12, "bold"), bg=Colors.background)
        course_label.grid(row=0, column=2, padx=10, sticky=W)

        course_combo = ttk.Combobox(currentCourseFrame, textvariable=self.var_course, font=(
            Fonts.primary, 12, "bold"), state="read only", width=20)
        course_combo["values"] = ["Chọn khóa", "61", "62", "63"]
        course_combo.current(0)
        course_combo.grid(row=0, column=3, pady=10, sticky=W)

        # Year
        year_label = Label(currentCourseFrame, text="Năm học",
                           font=(Fonts.primary, 12, "bold"), bg=Colors.background)
        year_label.grid(row=1, column=0, padx=10, sticky=W)

        year_combo = ttk.Combobox(currentCourseFrame, textvariable=self.var_year, font=(
            Fonts.primary, 12, "bold"), state="read only", width=20)
        year_combo["values"] = ["Chọn năm", "2020", "2021", "2022"]
        year_combo.current(0)
        year_combo.grid(row=1, column=1, pady=10, sticky=W)

        # Semester
        semester_label = Label(currentCourseFrame, text="Kỳ học", font=(
            Fonts.primary, 12, "bold"), bg=Colors.background)
        semester_label.grid(row=1, column=2, padx=10, sticky=W)

        semester_combo = ttk.Combobox(currentCourseFrame, textvariable=self.var_semester, font=(
            Fonts.primary, 12, "bold"), state="read only", width=20)
        semester_combo["values"] = ["Chọn kỳ", "1", "2"]
        semester_combo.current(0)
        semester_combo.grid(row=1, column=3, pady=10, sticky=W)

        # class student information
        class_student_Frame = LabelFrame(
            Left_Frame, bd=2, bg=Colors.background, relief=RIDGE, text="LỚP HỌC", font=(Fonts.primary, 12, "bold"))
        class_student_Frame.place(x=5, y=250, width=720, height=400)

        # Student ID
        studentID_label = Label(class_student_Frame, text="MSSV:", font=(
            Fonts.primary, 12, "bold"), bg=Colors.background)
        studentID_label.grid(row=0, column=0, padx=10, pady=5, sticky=W)

        studentID_entry = ttk.Entry(
            class_student_Frame, textvariable=self.var_std_id, width=17, font=(Fonts.primary, 12, "bold"))
        studentID_entry.grid(row=0, column=1, padx=10, pady=5, sticky=W)

        # Student name
        studentName_label = Label(class_student_Frame, text="Họ và tên:", font=(
            Fonts.primary, 12, "bold"), bg=Colors.background)
        studentName_label.grid(row=0, column=2, padx=10, pady=5, sticky=W)

        studentName_entry = ttk.Entry(
            class_student_Frame, textvariable=self.var_std_name, width=17, font=(Fonts.primary, 12, "bold"))
        studentName_entry.grid(row=0, column=3, padx=10, pady=5, sticky=W)

        # Class division
        class_Div_label = Label(class_student_Frame, text="Lớp:", font=(
            Fonts.primary, 12, "bold"), bg=Colors.background)
        class_Div_label.grid(row=1, column=0, padx=10, pady=5, sticky=W)

        div_combo = ttk.Combobox(class_student_Frame, textvariable=self.var_div, font=(
            Fonts.primary, 12, "bold"), state="read only", width=15)
        div_combo["values"] = ["01", "02", "03", "04",
                               "05", "06", "07", "08", "09", "10", "11", "12"]
        div_combo.current(0)
        div_combo.grid(row=1, column=1, padx=10, pady=10, sticky=W)

        # Roll NO
        roll_NO_label = Label(class_student_Frame, text="Số thứ tự:", font=(
            Fonts.primary, 12, "bold"), bg=Colors.background)
        roll_NO_label.grid(row=1, column=2, padx=10, pady=5, sticky=W)

        roll_NO_entry = ttk.Entry(
            class_student_Frame, textvariable=self.var_roll, width=17, font=(Fonts.primary, 12, "bold"))
        roll_NO_entry.grid(row=1, column=3, padx=10, pady=5, sticky=W)

        # Gender
        gender_label = Label(class_student_Frame, text="Giới tính:", font=(
            Fonts.primary, 12, "bold"), bg=Colors.background)
        gender_label.grid(row=2, column=0, padx=10, pady=5, sticky=W)

        gender_combo = ttk.Combobox(class_student_Frame, textvariable=self.var_gender, font=(
            Fonts.primary, 12, "bold"), state="read only", width=15)
        gender_combo["values"] = ["Nam", "Nữ"]
        gender_combo.current(0)
        gender_combo.grid(row=2, column=1, padx=10, pady=10, sticky=W)

        # DOB
        DOB_label = Label(class_student_Frame, text="Ngày sinh:",
                          font=(Fonts.primary, 12, "bold"), bg=Colors.background)
        DOB_label.grid(row=2, column=2, padx=10, pady=5, sticky=W)

        DOB_entry = ttk.Entry(
            class_student_Frame, textvariable=self.var_dob, width=17, font=(Fonts.primary, 12, "bold"))
        DOB_entry.grid(row=2, column=3, padx=10, pady=5, sticky=W)

        # email
        email_label = Label(class_student_Frame, text="Email:",
                            font=(Fonts.primary, 12, "bold"), bg=Colors.background)
        email_label.grid(row=3, column=0, padx=10, pady=5, sticky=W)

        email_entry = ttk.Entry(
            class_student_Frame, textvariable=self.var_mail, width=17, font=(Fonts.primary, 12, "bold"))
        email_entry.grid(row=3, column=1, padx=10, pady=5, sticky=W)

        # phone number
        phone_label = Label(class_student_Frame, text="SĐT:",
                            font=(Fonts.primary, 12, "bold"), bg=Colors.background)
        phone_label.grid(row=3, column=2, padx=10, pady=5, sticky=W)

        phone_entry = ttk.Entry(
            class_student_Frame, textvariable=self.var_phone, width=17, font=(Fonts.primary, 12, "bold"))
        phone_entry.grid(row=3, column=3, padx=10, pady=5, sticky=W)

        # Address
        adderss_label = Label(class_student_Frame, text="Địa chỉ:", font=(
            Fonts.primary, 12, "bold"), bg=Colors.background)
        adderss_label.grid(row=4, column=0, padx=10, pady=5, sticky=W)

        adderss_entry = ttk.Entry(
            class_student_Frame, textvariable=self.var_address, width=17, font=(Fonts.primary, 12, "bold"))
        adderss_entry.grid(row=4, column=1, padx=10, pady=5, sticky=W)

        # teacher name
        Teacher_name_label = Label(class_student_Frame, text="Giảng viên:", font=(
            Fonts.primary, 12, "bold"), bg=Colors.background)
        Teacher_name_label.grid(row=4, column=2, padx=10, pady=5, sticky=W)

        Teacher_name_entry = ttk.Entry(
            class_student_Frame, textvariable=self.var_teacher, width=17, font=(Fonts.primary, 12, "bold"))
        Teacher_name_entry.grid(row=4, column=3, padx=10, pady=5, sticky=W)

        # radio button
        self.var_radio1 = StringVar()
        radiobtn1 = ttk.Radiobutton(
            class_student_Frame, variable=self.var_radio1, text="Lấy mẫu ảnh", value="YES")
        radiobtn1.grid(row=6, column=0)

        radiobtn2 = ttk.Radiobutton(
            class_student_Frame, variable=self.var_radio1, text="Chưa lấy mẫu", value="NO")
        radiobtn2.grid(row=6, column=1)

        # button frame
        btn_frame = Frame(class_student_Frame, bd=2,
                          relief=RIDGE, bg=Colors.background)
        btn_frame.place(x=0, y=215, width=715, height=100)

        save_btn = Button(btn_frame, text="Lưu", command=self.add_data, width=15, font=(
            Fonts.primary, 13, "bold"), bg=Colors.button, fg=Colors.textButton)
        save_btn.grid(row=0, column=0)

        update_btn = Button(btn_frame, text="Cập nhật", command=self.update_data, width=15, font=(
            Fonts.primary, 13, "bold"), bg=Colors.button, fg=Colors.textButton)
        update_btn.grid(row=0, column=1)

        delete_btn = Button(btn_frame, text="Xóa", command=self.delete_data, width=15, font=(
            Fonts.primary, 13, "bold"), bg=Colors.button, fg=Colors.textButton)
        delete_btn.grid(row=0, column=2)

        reset_btn = Button(btn_frame, text="Làm mới", command=self.reset_data, width=15, font=(
            Fonts.primary, 13, "bold"), bg=Colors.button, fg=Colors.textButton)
        reset_btn.grid(row=0, column=3)

        btn_frame1 = Frame(class_student_Frame, bd=2,
                           relief=RIDGE, bg=Colors.background)
        btn_frame1.place(x=0, y=250, width=715, height=35)

        take_photo_btn = Button(btn_frame1, text="Lấy mẫu", command=self.generate_dataset, width=31, font=(
            Fonts.primary, 13, "bold"), bg=Colors.button, fg=Colors.textButton)
        take_photo_btn.grid(row=0, column=0)

        update_photo_btn = Button(btn_frame1, text="Training", command=self.train_classifier, width=31, font=(
            Fonts.primary, 13, "bold"), bg=Colors.button, fg=Colors.textButton)
        update_photo_btn.grid(row=0, column=1)

        # Right label frame
        Right_Frame = LabelFrame(mainFrame, bd=2, bg=Colors.background, relief=RIDGE,
                                 text="DANH SÁCH LỚP", font=(Fonts.primary, 12, "bold"))
        Right_Frame.place(x=680, y=30, width=660, height=580)

        img_right = Image.open("./assets/images//class.jpg")
        img_right = img_right.resize((720, 150), Image.ANTIALIAS)
        self.photoimg_right = ImageTk.PhotoImage(img_right)

        f_lbl = Label(Right_Frame, image=self.photoimg_right)
        f_lbl.place(x=5, y=0, width=720, height=130)

        #=================SEARCH===========

        search_Frame = LabelFrame(
            Right_Frame, bd=2, bg=Colors.background, relief=RIDGE, font=(Fonts.primary, 12, "bold"))
        search_Frame.place(x=5, y=135, width=700, height=40)

        search_btn = Button(search_Frame, text="Lập danh sách lớp", width=22, font=(
            Fonts.primary, 12, "bold"), bg=Colors.button, fg=Colors.textButton, command=self.create_new_class)
        search_btn.grid(row=0, column=3, padx=4)

        showAll_btn = Button(search_Frame, text="Tạo lớp mới", width=11, font=(
            Fonts.primary, 12, "bold"), bg=Colors.button, fg=Colors.textButton, command=self.delete_all)
        showAll_btn.grid(row=0, column=4, padx=4)

        #=====================table frame================

        table_Frame = Frame(Right_Frame, bd=2,
                            bg=Colors.background, relief=RIDGE)
        table_Frame.place(x=5, y=210, width=650, height=350)

        Scroll_x = ttk.Scrollbar(table_Frame, orient=HORIZONTAL)
        Scroll_y = ttk.Scrollbar(table_Frame, orient=VERTICAL)

        self.student_table = ttk.Treeview(table_Frame, column=("dep", "course", "year", "sem", "id",
                                          "name", "div", "Roll", "gender", "dob", "email", "phone", "address", "teacher", "photoSample"))

        Scroll_x.pack(side=BOTTOM, fill=X)
        Scroll_y.pack(side=RIGHT, fill=Y)
        Scroll_x.config(command=self.student_table.xview)
        Scroll_y.config(command=self.student_table.yview)

        self.student_table.heading("dep", text="Ngành")
        self.student_table.heading("course", text="Khóa")
        self.student_table.heading("year", text="Năm học")
        self.student_table.heading("sem", text="Kỳ học")
        self.student_table.heading("id", text="MSSV")
        self.student_table.heading("name", text="Tên")
        self.student_table.heading("div", text="Lớp")
        self.student_table.heading("Roll", text="STT")
        self.student_table.heading("gender", text="Giới tính")
        self.student_table.heading("dob", text="Ngày sinh")
        self.student_table.heading("email", text="Email")
        self.student_table.heading("phone", text="SĐT")
        self.student_table.heading("address", text="Địa chỉ")
        self.student_table.heading("teacher", text="Giảng viên")
        self.student_table.heading("photoSample", text="Ảnh")
        self.student_table["show"] = "headings"

        self.student_table.column("dep", width=100)
        self.student_table.column("course", width=100)
        self.student_table.column("year", width=100)
        self.student_table.column("sem", width=100)
        self.student_table.column("id", width=100)
        self.student_table.column("name", width=100)
        self.student_table.column("div", width=100)
        self.student_table.column("Roll", width=100)
        self.student_table.column("gender", width=100)
        self.student_table.column("dob", width=100)
        self.student_table.column("email", width=100)
        self.student_table.column("phone", width=100)
        self.student_table.column("address", width=100)
        self.student_table.column("teacher", width=100)
        self.student_table.column("photoSample", width=100)

        self.student_table.pack(fill=BOTH, expand=1)
        self.student_table.bind("<ButtonRelease>", self.get_cursor)
        self.fetch_data()

    #============= FUNCTION DECRATION================
    def add_data(self):
        if self.var_dep.get() == "Chọn ngành" or self.var_std_name.get() == "" or self.var_std_id.get() == "":
            messagebox.showerror(
                "Error", "Phải điền đầy các mục", parent=self.root)
        else:
            try:
                conn = mysql.connector.connect(
                    host="localhost", username="root", password="Shj@6863#jw", database="diemdanhdb")
                my_cursor = conn.cursor()
                my_cursor.execute("insert into student values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (
                    self.var_dep.get(),
                    self.var_course.get(),
                    self.var_year.get(),
                    self.var_semester.get(),
                    self.var_std_id.get(),
                    self.var_std_name.get(),
                    self.var_div.get(),
                    self.var_roll.get(),
                    self.var_gender.get(),
                    self.var_dob.get(),
                    self.var_mail.get(),
                    self.var_phone.get(),
                    self.var_address.get(),
                    self.var_teacher.get(),
                    self.var_radio1.get()

                ))
                conn.commit()
                self.fetch_data()
                conn.close()
                n = str(self.var_std_id.get())
                path = "data/images"
                os.makedirs(path, exist_ok=True)
                path = os.path.join(path, n)
                os.makedirs(path, exist_ok=True)

                studentData = {
                    "dep": self.var_dep.get(),
                    "course": self.var_course.get(),
                    "year": self.var_year.get(),
                    "semester": self.var_semester.get(),
                    "id": self.var_std_id.get(),
                    "name": self.var_std_name.get(),
                    "div": self.var_div.get(),
                    "roll": self.var_roll.get(),
                    "gender": self.var_gender.get(),
                    "dob": self.var_dob.get(),
                    "mail": self.var_mail.get(),
                    "phone": self.var_phone.get(),
                    "address": self.var_address.get(),
                    "teacher": self.var_teacher.get(),
                }

                path = "data/infor"
                os.makedirs(path, exist_ok=True)
                path = os.path.join(path, n + ".json")

                with open(path, "w", encoding='utf-8') as outfile:
                    json.dump(studentData, outfile, ensure_ascii=False)

                messagebox.showinfo(
                    "Success", "Đăng ký thành công", parent=self.root)
            except Exception as es:
                messagebox.showerror(
                    "Error", f"due to :{str(es)}", parent=self.root)

    # ================= fetch data =========================

    def fetch_data(self):
        conn = mysql.connector.connect(
            host="localhost", username="root", password="Shj@6863#jw", database="diemdanhdb")
        my_cursor = conn.cursor()
        my_cursor.execute("select * from student")
        data = my_cursor.fetchall()

        self.student_table.delete(*self.student_table.get_children())
        for i in data:
            self.student_table.insert("", END, values=i)
        conn.commit()

        conn.close()

    #=============== get cursor =========================
    def get_cursor(self, event=""):
        cursor_focus = self.student_table.focus()
        content = self.student_table.item(cursor_focus)
        data = content["values"]

        self.var_dep.set(data[0]),
        self.var_course.set(data[1]),
        self.var_year.set(data[2]),
        self.var_semester.set(data[3]),
        self.var_std_id.set(data[4]),
        self.var_std_name.set(data[5]),
        self.var_div.set(data[6]),
        self.var_roll.set(data[7]),
        self.var_gender.set(data[8]),
        self.var_dob.set(data[9]),
        self.var_mail.set(data[10]),
        self.var_phone.set(data[11]),
        self.var_address.set(data[12]),
        self.var_teacher.set(data[13]),
        self.var_radio1.set(data[14])

    #================= create new class function ===========================
    def create_new_class(self):
        fln = filedialog.asksaveasfilename(initialdir=os.getcwd(), title="Open CSV", filetypes=(
            ("CSV File", "*.csv"), ("All File", "*.*")), parent=self.root)
        if (len(fln) == 0):
            return
        try:
            with open(fln, "w", newline='', encoding="utf-8") as f:
                f.write('\ufeff')
                writer = csv.writer(f)
                writer.writerows([("dep", "course", "year",
                                   "semester", "studentID", "studentName",
                                   "Division", "Roll", "gender",
                                   "dob", "mail", "phone",
                                   "address", "teacher", "photo")])
                for line in self.student_table.get_children():
                    data = self.student_table.item(line)["values"]
                    writer.writerows([(data[0], data[1], data[2],
                                       data[3], data[4], data[5],
                                       data[6], data[7], data[8],
                                       data[9], data[10], data[11],
                                       data[12], data[13], data[14])])
            messagebox.showinfo("Success", "Đã lưu", parent=self.root)
        except Exception as es:
            messagebox.showerror(
                "Error", f"due to :{str(es)}", parent=self.root)
        return
    #=================Update function=================

    def update_data(self):
        if self.var_dep.get() == "Chọn ngành" or self.var_std_name.get() == "" or self.var_std_id.get() == "":
            messagebox.showerror(
                "Error", "Phải điền đầy các mục", parent=self.root)
        else:
            try:
                Update = messagebox.askyesno(
                    "update", "Cập nhật thông tin này ?", parent=self.root)
                if Update > 0:
                    conn = mysql.connector.connect(
                        host="localhost", username="root", password="Shj@6863#jw", database="diemdanhdb")
                    my_cursor = conn.cursor()
                    my_cursor.execute("update student set dep=%s,course=%s,year=%s,semester=%s,name=%s,division=%s,Roll=%s,gender=%s,Dob=%s,mail=%s,phone=%s,Address=%s,teacher=%s,photoSample=%s where studentID=%s", (
                        self.var_dep.get(),
                        self.var_course.get(),
                        self.var_year.get(),
                        self.var_semester.get(),
                        self.var_std_name.get(),
                        self.var_div.get(),
                        self.var_roll.get(),
                        self.var_gender.get(),
                        self.var_dob.get(),
                        self.var_mail.get(),
                        self.var_phone.get(),
                        self.var_address.get(),
                        self.var_teacher.get(),
                        self.var_radio1.get(),
                        self.var_std_id.get()
                    ))
                else:
                    if not Update:
                        return
                messagebox.showinfo("Success", "Đã cập nhật", parent=self.root)
                conn.commit()
                self.fetch_data()
                conn.close()
                n = str(self.var_std_id.get())
                path = "data/infor"
                path = os.path.join(path, n + ".json")

                studentData = {
                    "dep": self.var_dep.get(),
                    "course": self.var_course.get(),
                    "year": self.var_year.get(),
                    "semester": self.var_semester.get(),
                    "id": self.var_std_id.get(),
                    "name": self.var_std_name.get(),
                    "div": self.var_div.get(),
                    "roll": self.var_roll.get(),
                    "gender": self.var_gender.get(),
                    "dob": self.var_dob.get(),
                    "mail": self.var_mail.get(),
                    "phone": self.var_phone.get(),
                    "address": self.var_address.get(),
                    "teacher": self.var_teacher.get(),
                }

                with open(path, "w", encoding='utf-8') as outfile:
                    json.dump(studentData, outfile, ensure_ascii=False)
            except Exception as es:
                messagebox.showerror(
                    "Error", f"due to :{str(es)}", parent=self.root)

    #=================== delete function ====================
    def delete_data(self):
        if self.var_std_id.get() == "":
            messagebox.showerror("Error", "Phải ghi MSSV", parent=self.root)
        else:
            try:
                delete = messagebox.askyesno(
                    "Delete", "Xóa sinh viên này ?", parent=self.root)
                if delete > 0:
                    conn = mysql.connector.connect(
                        host="localhost", username="root", password="Shj@6863#jw", database="diemdanhdb")
                    my_cursor = conn.cursor()
                    sql = "delete from student where studentID=%s"
                    val = (self.var_std_id.get(),)
                    my_cursor.execute(sql, val)
                else:
                    if not delete:
                        return

                conn.commit()
                self.fetch_data()
                conn.close()
                n = str(self.var_std_id.get())
                path = "data/images/" + n
                shutil.rmtree(path)
                path = "data/infor/" + n + ".json"
                os.remove(path)
                messagebox.showinfo("Delete", "Đã xóa", parent=self.root)
            except Exception as es:
                messagebox.showerror(
                    "Error", f"due to :{str(es)}", parent=self.root)

    #=========== delete all function ===========================
    def delete_all(self):
        try:
            delete = messagebox.askyesno(
                "Student Delete All", "Thông tin lớp cũ sẽ bị xóa hết, bạn chắc chứ ?", parent=self.root)
            if delete > 0:
                conn = mysql.connector.connect(
                    host="localhost", username="root", password="Shj@6863#jw", database="diemdanhdb")
                my_cursor = conn.cursor()
                sql = "delete from student"
                my_cursor.execute(sql)
            else:
                if not delete:
                    return

            conn.commit()
            self.fetch_data()
            conn.close()
            if os.path.exists("data"):
                shutil.rmtree("data")
            if os.path.exists("attendance"):
                shutil.rmtree("attendance")
            messagebox.showinfo("Delete", "Đã làm mới", parent=self.root)
        except Exception as es:
            messagebox.showerror(
                "Error", f"due to :{str(es)}", parent=self.root)

    #=========== reset function ===========================
    def reset_data(self):
        self.var_dep.set("Chọn ngành")
        self.var_course.set("Chọn khóa")
        self.var_year.set("Chọn năm")
        self.var_semester.set("Chọn kỳ")
        self.var_std_id.set("")
        self.var_std_name.set("")
        self.var_div.set("Chọn lớp")
        self.var_roll.set("")
        self.var_gender.set("Giới tính")
        self.var_dob.set("")
        self.var_mail.set("")
        self.var_phone.set("")
        self.var_address.set("")
        self.var_teacher.set("")
        self.var_radio1.set("")

#===================== generate data set (take photo sample) ==============
    def generate_dataset(self):
        if self.var_dep.get() == "Chọn ngành" or self.var_std_name.get() == "" or self.var_std_id.get() == "":
            messagebox.showerror(
                "Error", "Phải điền đầy các mục", parent=self.root)
        else:
            try:
                conn = mysql.connector.connect(
                    host="localhost", username="root", password="Shj@6863#jw", database="diemdanhdb")
                my_cursor = conn.cursor()
                my_cursor.execute("select * from student")
                myresult = my_cursor.fetchall()
                id = self.var_std_id.get()
                print(id)
                for x in myresult:
                    print(x)
                    if x[4] == int(id):
                        print(x)
                        break
                my_cursor.execute("update student set dep=%s,course=%s,year=%s,semester=%s,division=%s,roll=%s,gender=%s,dob=%s,mail=%s,phone=%s,address=%s,teacher=%s,photoSample=%s where studentID=%s", (
                    self.var_dep.get(),
                    self.var_course.get(),
                    self.var_year.get(),
                    self.var_semester.get(),
                    #self.var_std_name.get(),
                    self.var_div.get(),
                    self.var_roll.get(),
                    self.var_gender.get(),
                    self.var_dob.get(),
                    self.var_mail.get(),
                    self.var_phone.get(),
                    self.var_address.get(),
                    self.var_teacher.get(),
                    self.var_radio1.get(),
                    self.var_std_id.get()

                ))
                conn.commit()
                self.fetch_data()
                self.reset_data()
                conn.close()

                # # ============= Load predifiend data on face frontals from openCV ============
                # face_classifier = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
                #
                # def face_cropped(img):
                #     gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
                #     faces=face_classifier.detectMultiScale(gray,1.3,5)
                #     #Scaling factor=1.3
                #     #Minimum neighbor=5
                #
                #     for(x,y,w,h) in faces:
                #         face_cropped=img[y:y+h,x:x+w]
                #         return face_cropped
                #
                # cap=cv2.VideoCapture(0)
                # img_id=0
                # while True:
                #     ret,my_frame=cap.read()
                #     if face_cropped(my_frame) is not None:
                #         img_id=img_id+1
                #         face=cv2.resize(face_cropped(my_frame),(160,160))
                #         face=cv2.cvtColor(face,cv2.COLOR_BGR2GRAY)
                #         file_name_path="data/images/"+str(x[4])+"/"+str(img_id)+".jpg"
                #         cv2.imwrite(file_name_path,face)
                #         cv2.putText(face,str(img_id),(50,50),cv2.FONT_HERSHEY_COMPLEX,2,(0,255,0),2)
                #         cv2.imshow("cropped face",face)
                #
                #     if cv2.waitKey(1)==13 or int(img_id)==100:
                #         break
                face_model = get_face_detector()
                landmark_model = get_landmark_model()
                cap = cv2.VideoCapture(0)  # batcam
                ret, img = cap.read()
                size = img.shape
                font = cv2.FONT_HERSHEY_SIMPLEX
                # 3D model points.
                model_points = np.array([
                    (0.0, 0.0, 0.0),  # Nose tip
                    (0.0, -330.0, -65.0),  # Chin
                    (-225.0, 170.0, -135.0),  # Left eye left corner
                    (225.0, 170.0, -135.0),  # Right eye right corne
                    (-150.0, -150.0, -125.0),  # Left Mouth corner
                    (150.0, -150.0, -125.0)  # Right mouth corner
                ])

                # Camera internals
                focal_length = size[1]
                center = (size[1] / 2, size[0] / 2)
                camera_matrix = np.array(
                    [[focal_length, 0, center[0]],
                     [0, focal_length, center[1]],
                     [0, 0, 1]], dtype="double"
                )

                img_id1 = 0
                img_id2 = 0
                img_id3 = 0
                img_id4 = 0
                img_id5 = 0
                img_id6 = 0
                while True:
                    ret, img = cap.read()

                    if ret == True:
                        faces = find_faces(img, face_model)

                        for face in faces:
                            marks = detect_marks(img, landmark_model, face)
                            # mark_detector.draw_marks(img, marks, color=(0, 255, 0))
                            image_points = np.array([
                                marks[30],  # Nose tip
                                marks[8],  # Chin
                                marks[36],  # Left eye left corner
                                marks[45],  # Right eye right corne
                                marks[48],  # Left Mouth corner
                                marks[54]  # Right mouth corner
                            ], dtype="double")
                            # Assuming no lens distortion
                            dist_coeffs = np.zeros((4, 1))
                            (success, rotation_vector, translation_vector) = cv2.solvePnP(model_points, image_points,
                                                                                          camera_matrix,
                                                                                          dist_coeffs,
                                                                                          flags=cv2.SOLVEPNP_UPNP)

                            # Project a 3D point (0, 0, 1000.0) onto the image plane.
                            # We use this to draw a line sticking out of the nose

                            (nose_end_point2D, jacobian) = cv2.projectPoints(np.array([(0.0, 0.0, 1000.0)]),
                                                                             rotation_vector,
                                                                             translation_vector, camera_matrix,
                                                                             dist_coeffs)
                            # for p in image_points:
                            #     cv2.circle(img, (int(p[0]), int(p[1])), 3, (0, 0, 255), -1)

                            p1 = (int(image_points[0][0]),
                                  int(image_points[0][1]))
                            p2 = (int(nose_end_point2D[0][0][0]), int(
                                nose_end_point2D[0][0][1]))
                            x1, x2 = head_pose_points(
                                img, rotation_vector, translation_vector, camera_matrix)

                            # cv2.line(img, p1, p2, (0, 255, 255), 2)
                            # cv2.line(img, tuple(x1), tuple(x2), (255, 255, 0), 2)
                            # for (x, y) in marks:
                            # cv2.circle(img, (x, y), 4, (255, 255, 0), -1)
                            # cv2.putText(img, str(p1), p1, font, 1, (0, 255, 255), 1)
                            try:
                                m = (p2[1] - p1[1]) / (p2[0] - p1[0])
                                ang1 = int(math.degrees(math.atan(m)))
                            except:
                                ang1 = 90

                            try:
                                m = (x2[1] - x1[1]) / (x2[0] - x1[0])
                                ang2 = int(math.degrees(math.atan(-1 / m)))
                            except:
                                ang2 = 90

                                # print('div by zero error')

                            if img_id6 < 10:
                                img_id1 = img_id1 + 1
                                img_id6 = img_id6 + 1
                                face1 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                                file_name_path = "data/images/" + \
                                    str(x[4])+"/"+str(img_id1)+".jpg"
                                cv2.imwrite(file_name_path, face1)
                                cv2.putText(face1, str(
                                    img_id1), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 255, 0), 2)
                                cv2.imshow("cropped face", face1)

                            if img_id4 < 10:
                                print('nên Head left')
                                cv2.putText(img, 'NEN QUAY TRAI',
                                            (90, 30), font, 2, (255, 255, 128), 3)

                            if img_id3 < 10 and img_id4 == 10:
                                print('NEN Head right')
                                cv2.putText(img, 'NEN QUAY PHAI',
                                            (90, 30), font, 2, (255, 255, 128), 3)

                            if img_id2 < 5 and img_id3 == 10 and img_id4 == 10:
                                print('NEN Head up')
                                cv2.putText(img, 'NEN QUAY LEN',
                                            (30, 30), font, 2, (255, 255, 128), 3)

                            if img_id5 < 5 and img_id2 == 5 and img_id3 == 10 and img_id4 == 10:
                                print('NEN Head down')
                                cv2.putText(img, 'NEN QUAY XUONG',
                                            (30, 30), font, 2, (255, 255, 128), 3)

                            if ang1 >= 48 and img_id5 < 5:

                                print('Head down')
                                cv2.putText(img, 'Head down', (30, 30),
                                            font, 2, (255, 255, 128), 3)
                                img_id1 = img_id1 + 1
                                img_id5 = img_id5 + 1
                                face1 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                                file_name_path = "data/images/" + \
                                    str(x[4])+"/"+str(img_id1)+".jpg"
                                cv2.imwrite(file_name_path, face1)
                                cv2.putText(face1, str(
                                    img_id1), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 255, 0), 2)
                                cv2.imshow("cropped face", face1)

                            elif ang1 <= -48 and img_id2 < 5:
                                print('Head up')
                                cv2.putText(img, 'Head up', (30, 30),
                                            font, 2, (255, 255, 128), 3)
                                img_id1 = img_id1 + 1
                                img_id2 = img_id2 + 1
                                face1 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                                file_name_path = "data/images/" + \
                                    str(x[4])+"/"+str(img_id1)+".jpg"
                                cv2.imwrite(file_name_path, face1)
                                cv2.putText(face1, str(
                                    img_id1), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 255, 0), 2)
                                cv2.imshow("cropped face", face1)

                            if ang2 >= 48 and img_id3 < 10:
                                print('Head right')
                                cv2.putText(img, 'Head right', (90, 30),
                                            font, 2, (255, 255, 128), 3)
                                img_id1 = img_id1 + 1
                                img_id3 = img_id3 + 1
                                face1 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                                file_name_path = "data/images/" + \
                                    str(x[4])+"/"+str(img_id1)+".jpg"
                                cv2.imwrite(file_name_path, face1)
                                cv2.putText(face1, str(
                                    img_id1), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 255, 0), 2)
                                cv2.imshow("cropped face", face1)

                            elif ang2 <= -48 and img_id4 < 10:
                                print('Head left')
                                cv2.putText(img, 'Head left', (90, 30),
                                            font, 2, (255, 255, 128), 3)
                                img_id1 = img_id1 + 1
                                img_id4 = img_id4 + 1
                                face1 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                                file_name_path = "data/images/" + \
                                    str(x[4])+"/"+str(img_id1)+".jpg"
                                cv2.imwrite(file_name_path, face1)
                                cv2.putText(face1, str(
                                    img_id1), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 255, 0), 2)
                                cv2.imshow("cropped face", face1)

                            # cv2.putText(img, str(ang1), tuple(p1), font, 2, (128, 255, 255), 3)
                            # cv2.putText(img, str(ang2), tuple(x1), font, 2, (255, 255, 128), 3)
                        cv2.imshow('img', img)

                        if cv2.waitKey(1) & 0xFF == ord('q') or int(img_id1) == 100:
                            break
                    else:
                        break
                cv2.destroyAllWindows()
                cap.release()

                messagebox.showinfo("result", "Đã lấy ảnh")
            except Exception as es:
                messagebox.showerror(
                    "Error", f"due to :{str(es)}", parent=self.root)


#========================================================================

    def train_classifier(self):
        os.system("python src/align_dataset_mtcnn.py  data/images data/image --image_size 160 --margin 32  --random_order --gpu_memory_fraction 0.25")
        os.system("python face_recognition/classifier.py TRAIN data/image Models/20180402-114759.pb Models/facemodel.pkl --batch_size 1000")
        messagebox.showinfo("Success", "training thành công", parent=self.root)

from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk

from store.assets import *


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
        self.var_radio1 = StringVar()

        # first imag
        self.smeImg = ImageTk.PhotoImage(
            Images.sme.resize((450, 50), Image.ANTIALIAS))
        Label(self.root, image=self.smeImg).place(
            x=0, y=0, width=500, height=50)

        # second imag
        self.HUSTImg = ImageTk.PhotoImage(
            Images.HUST.resize((450, 50), Image.ANTIALIAS))
        Label(self.root, image=self.HUSTImg).place(
            x=450, y=0, width=500, height=50)

        # third imag
        self.HUST1Img = ImageTk.PhotoImage(
            Images.HUST1.resize((450, 50), Image.ANTIALIAS))
        Label(self.root, image=self.HUST1Img).place(
            x=900, y=0, width=500, height=50)

        # bg imag
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

        studentID_entry = Entry(
            class_student_Frame, textvariable=self.var_std_id, width=17, font=(Fonts.primary, 12, "bold"))
        studentID_entry.grid(row=0, column=1, padx=10, pady=5, sticky=W)

        # Student name
        studentName_label = Label(class_student_Frame, text="Họ và tên:", font=(
            Fonts.primary, 12, "bold"), bg=Colors.background)
        studentName_label.grid(row=0, column=2, padx=10, pady=5, sticky=W)

        studentName_entry = Entry(
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

        roll_NO_entry = Entry(
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

        DOB_entry = Entry(
            class_student_Frame, textvariable=self.var_dob, width=17, font=(Fonts.primary, 12, "bold"))
        DOB_entry.grid(row=2, column=3, padx=10, pady=5, sticky=W)

        # email
        email_label = Label(class_student_Frame, text="Email:",
                            font=(Fonts.primary, 12, "bold"), bg=Colors.background)
        email_label.grid(row=3, column=0, padx=10, pady=5, sticky=W)

        email_entry = Entry(
            class_student_Frame, textvariable=self.var_mail, width=17, font=(Fonts.primary, 12, "bold"))
        email_entry.grid(row=3, column=1, padx=10, pady=5, sticky=W)

        # phone number
        phone_label = Label(class_student_Frame, text="SĐT:",
                            font=(Fonts.primary, 12, "bold"), bg=Colors.background)
        phone_label.grid(row=3, column=2, padx=10, pady=5, sticky=W)

        phone_entry = Entry(
            class_student_Frame, textvariable=self.var_phone, width=17, font=(Fonts.primary, 12, "bold"))
        phone_entry.grid(row=3, column=3, padx=10, pady=5, sticky=W)

        # Address
        address_label = Label(class_student_Frame, text="Địa chỉ:", font=(
            Fonts.primary, 12, "bold"), bg=Colors.background)
        address_label.grid(row=4, column=0, padx=10, pady=5, sticky=W)

        address_entry = Entry(
            class_student_Frame, textvariable=self.var_address, width=17, font=(Fonts.primary, 12, "bold"))
        address_entry.grid(row=4, column=1, padx=10, pady=5, sticky=W)

        # teacher name
        Teacher_name_label = Label(class_student_Frame, text="Giảng viên:", font=(
            Fonts.primary, 12, "bold"), bg=Colors.background)
        Teacher_name_label.grid(row=4, column=2, padx=10, pady=5, sticky=W)

        Teacher_name_entry = Entry(
            class_student_Frame, textvariable=self.var_teacher, width=17, font=(Fonts.primary, 12, "bold"))
        Teacher_name_entry.grid(row=4, column=3, padx=10, pady=5, sticky=W)

        # radio button
        radioBtn1 = Radiobutton(
            class_student_Frame, variable=self.var_radio1, text="Lấy mẫu ảnh", value="YES")
        radioBtn1.grid(row=6, column=0)

        radioBtn2 = Radiobutton(
            class_student_Frame, variable=self.var_radio1, text="Chưa lấy mẫu", value="NO")
        radioBtn2.grid(row=6, column=1)

        # button frame
        btn_frame = Frame(class_student_Frame, bd=2,
                          relief=RIDGE, bg=Colors.background)
        btn_frame.place(x=0, y=215, width=715, height=100)

        save_btn = Button(btn_frame, text="Lưu", command=self.controller.addStudent, width=15, font=(
            Fonts.primary, 13, "bold"), bg=Colors.button, fg=Colors.textButton)
        save_btn.grid(row=0, column=0)

        update_btn = Button(btn_frame, text="Cập nhật", command=self.controller.updateStudent, width=15, font=(
            Fonts.primary, 13, "bold"), bg=Colors.button, fg=Colors.textButton)
        update_btn.grid(row=0, column=1)

        delete_btn = Button(btn_frame, text="Xóa", command=self.controller.deleteStudent, width=15, font=(
            Fonts.primary, 13, "bold"), bg=Colors.button, fg=Colors.textButton)
        delete_btn.grid(row=0, column=2)

        reset_btn = Button(btn_frame, text="Làm mới", command=self.controller.reset_data, width=15, font=(
            Fonts.primary, 13, "bold"), bg=Colors.button, fg=Colors.textButton)
        reset_btn.grid(row=0, column=3)

        btn_frame1 = Frame(class_student_Frame, bd=2,
                           relief=RIDGE, bg=Colors.background)
        btn_frame1.place(x=0, y=250, width=715, height=35)

        take_photo_btn = Button(btn_frame1, text="Lấy mẫu", command=self.controller.generate_dataset, width=31, font=(
            Fonts.primary, 13, "bold"), bg=Colors.button, fg=Colors.textButton)
        take_photo_btn.grid(row=0, column=0)

        update_photo_btn = Button(btn_frame1, text="Training", command=self.controller.train_classifier, width=31, font=(
            Fonts.primary, 13, "bold"), bg=Colors.button, fg=Colors.textButton)
        update_photo_btn.grid(row=0, column=1)

        # Right label frame
        Right_Frame = LabelFrame(mainFrame, bd=2, bg=Colors.background, relief=RIDGE,
                                 text="DANH SÁCH LỚP", font=(Fonts.primary, 12, "bold"))
        Right_Frame.place(x=680, y=30, width=660, height=580)

        self.photoImg_right = ImageTk.PhotoImage(
            Images.classJpg.resize((720, 150), Image.ANTIALIAS))

        Label(Right_Frame, image=self.photoImg_right).place(
            x=5, y=0, width=720, height=130)

        # =================SEARCH===========
        search_Frame = LabelFrame(
            Right_Frame, bd=2, bg=Colors.background, relief=RIDGE, font=(Fonts.primary, 12, "bold"))
        search_Frame.place(x=5, y=135, width=700, height=40)

        search_btn = Button(search_Frame, text="Lập danh sách lớp", width=22, font=(
            Fonts.primary, 12, "bold"), bg=Colors.button, fg=Colors.textButton, command=self.controller.create_new_class)
        search_btn.grid(row=0, column=3, padx=4)

        showAll_btn = Button(search_Frame, text="Tạo lớp mới", width=11, font=(
            Fonts.primary, 12, "bold"), bg=Colors.button, fg=Colors.textButton, command=self.controller.delete_all)
        showAll_btn.grid(row=0, column=4, padx=4)

        # =====================table frame================
        table_Frame = Frame(Right_Frame, bd=2,
                            bg=Colors.background, relief=RIDGE)
        table_Frame.place(x=5, y=210, width=650, height=350)

        Scroll_x = Scrollbar(table_Frame, orient=HORIZONTAL)
        Scroll_y = Scrollbar(table_Frame, orient=VERTICAL)

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
        self.student_table.bind("<ButtonRelease>", self.controller.get_cursor)

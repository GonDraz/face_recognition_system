

import json
import os
from tkinter import messagebox
from models.student_model import StudentModel
from store.window_setup import WindowSetup
from view.student_view import StudentView

import mysql.connector


class StudentController:
    def __init__(self, root):

        self.root = root
        self.root.geometry(WindowSetup.screen)
        self.root.title("Thông tin sinh viên")

        self.model = StudentModel()
        self.view = StudentView(root, self)

        self.root.mainloop()

    # ============= FUNCTION DECRATION================
    def add_data(self):
        if self.view.var_dep.get() == "Chọn ngành" or self.view.var_std_name.get() == "" or self.view.var_std_id.get() == "":
            messagebox.showerror(
                "Error", "Phải điền đầy các mục", parent=self.root)
        else:
            try:
                conn = mysql.connector.connect(
                    host="localhost", username="root", password="Shj@6863#jw", database="diemdanhdb")
                my_cursor = conn.cursor()
                my_cursor.execute("insert into student values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (
                    self.view.var_dep.get(),
                    self.view.var_course.get(),
                    self.view.var_year.get(),
                    self.view.var_semester.get(),
                    self.view.var_std_id.get(),
                    self.view.var_std_name.get(),
                    self.view.var_div.get(),
                    self.view.var_roll.get(),
                    self.view.var_gender.get(),
                    self.view.var_dob.get(),
                    self.view.var_mail.get(),
                    self.view.var_phone.get(),
                    self.view.var_address.get(),
                    self.view.var_teacher.get(),
                    self.view.var_radio1.get()
                ))
                conn.commit()
                self.fetch_data()
                conn.close()
                n = str(self.view.var_std_id.get())
                path = "data/images"
                os.makedirs(path, exist_ok=True)
                path = os.path.join(path, n)
                os.makedirs(path, exist_ok=True)

                studentData = {
                    "dep": self.view.var_dep.get(),
                    "course": self.view.var_course.get(),
                    "year": self.view.var_year.get(),
                    "semester": self.view.var_semester.get(),
                    "id": self.view.var_std_id.get(),
                    "name": self.view.var_std_name.get(),
                    "div": self.view.var_div.get(),
                    "roll": self.view.var_roll.get(),
                    "gender": self.view.var_gender.get(),
                    "dob": self.view.var_dob.get(),
                    "mail": self.view.var_mail.get(),
                    "phone": self.view.var_phone.get(),
                    "address": self.view.var_address.get(),
                    "teacher": self.view.var_teacher.get(),
                }

                path = "data/info"
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

    # =============== get cursor =========================
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

    # =================create new class function ===========================
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

    # =================Update function=================
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

    # =================== delete function ====================
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

    # =========== delete all function ===========================
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

    # =========== reset function ===========================
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

# ===================== generate data set (take photo sample) ==============
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
                    # self.var_std_name.get(),
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


# ========================================================================


    def train_classifier(self):
        os.system("python src/align_dataset_mtcnn.py  data/images data/image --image_size 160 --margin 32  --random_order --gpu_memory_fraction 0.25")
        os.system("python face_recognition/classifier.py TRAIN data/image Models/20180402-114759.pb Models/facemodel.pkl --batch_size 1000")
        messagebox.showinfo("Success", "training thành công", parent=self.root)

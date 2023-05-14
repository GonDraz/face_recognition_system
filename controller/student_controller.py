

import csv
import math
import os
import threading
from tkinter import *
from tkinter import messagebox, filedialog
import cv2
import numpy as np

from store.path import Path
from store.window_setup import WindowSetup
from view.student_view import StudentView
from models.student_model import StudentModel

from include.face_landmarks import get_landmark_model, detect_marks
from include.face_detector import get_face_detector, find_faces


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
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml")


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


class StudentController:
    def __init__(self, root):

        self.root = root
        self.root.geometry(WindowSetup.screen)
        self.root.title("Thông tin sinh viên")

        self.view = StudentView(root, self)

        self.model = StudentModel()
        self.fetch_data()

        self.view.root.mainloop()

    # ============= FUNCTION DECRATION================

    def addStudent(self):
        if self.view.var_dep.get() == "Chọn ngành" or self.view.var_std_name.get() == "" or self.view.var_std_id.get() == "":
            messagebox.showerror(
                "Error", "Phải điền đầy các mục", parent=self.root)
        else:
            try:
                self.model.addStudent(
                    var_dep=self.view.var_dep.get(),
                    var_course=self.view.var_course.get(),
                    var_year=self.view.var_year.get(),
                    var_semester=self.view.var_semester.get(),
                    var_std_id=self.view.var_std_id.get(),
                    var_std_name=self.view.var_std_name.get(),
                    var_div=self.view.var_div.get(),
                    var_roll=self.view.var_roll.get(),
                    var_gender=self.view.var_gender.get(),
                    var_dob=self.view.var_dob.get(),
                    var_mail=self.view.var_mail.get(),
                    var_phone=self.view.var_phone.get(),
                    var_address=self.view.var_address.get(),
                    var_teacher=self.view.var_teacher.get(),
                    var_radio1=self.view.var_radio1.get())
                self.fetch_data()
                messagebox.showinfo(
                    "Success", "Đăng ký thành công", parent=self.root)
            except Exception as es:
                messagebox.showerror(
                    "Error", f"due to :{str(es)}", parent=self.root)

    # ================= fetch data =========================
    def fetch_data(self):
        data = self.model.LoadStudent()
        self.view.student_table.delete(*self.view.student_table.get_children())
        for i in data:
            self.view.student_table.insert("", END, values=i)

    # =============== get cursor =========================
    def get_cursor(self, event=""):
        cursor_focus = self.view.student_table.focus()
        content = self.view.student_table.item(cursor_focus)
        data = content["values"]

        self.view.var_dep.set(data[0]),
        self.view.var_course.set(data[1]),
        self.view.var_year.set(data[2]),
        self.view.var_semester.set(data[3]),
        self.view.var_std_id.set(data[4]),
        self.view.var_std_name.set(data[5]),
        self.view.var_div.set(data[6]),
        self.view.var_roll.set(data[7]),
        self.view.var_gender.set(data[8]),
        self.view.var_dob.set(data[9]),
        self.view.var_mail.set(data[10]),
        self.view.var_phone.set(data[11]),
        self.view.var_address.set(data[12]),
        self.view.var_teacher.set(data[13]),
        self.view.var_radio1.set(data[14])

    # =================create new class function ===========================
    # hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh
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
                for line in self.view.student_table.get_children():
                    data = self.view.student_table.item(line)["values"]
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
    def updateStudent(self):
        if self.view.var_dep.get() == "Chọn ngành" or self.view.var_std_name.get() == "" or self.view.var_std_id.get() == "":
            messagebox.showerror(
                "Error", "Phải điền đầy các mục", parent=self.view.root)
        else:
            try:
                Update = messagebox.askyesno(
                    "update", "Cập nhật thông tin này ?", parent=self.view.root)
                if Update:
                    self.model.updateStudent(
                        var_dep=self.view.var_dep.get(),
                        var_course=self.view.var_course.get(),
                        var_year=self.view.var_year.get(),
                        var_semester=self.view.var_semester.get(),
                        var_std_id=self.view.var_std_id.get(),
                        var_std_name=self.view.var_std_name.get(),
                        var_div=self.view.var_div.get(),
                        var_roll=self.view.var_roll.get(),
                        var_gender=self.view.var_gender.get(),
                        var_dob=self.view.var_dob.get(),
                        var_mail=self.view.var_mail.get(),
                        var_phone=self.view.var_phone.get(),
                        var_address=self.view.var_address.get(),
                        var_teacher=self.view.var_teacher.get(),
                        var_radio1=self.view.var_radio1.get())
                    self.fetch_data()
                    messagebox.showinfo(
                        "Success", "Đã cập nhật", parent=self.root)
            except Exception as es:
                messagebox.showerror(
                    "Error", f"due to :{str(es)}", parent=self.root)

    # =================== delete function ====================
    def deleteStudent(self):
        if self.view.var_std_id.get() == "":
            messagebox.showerror("Error", "Phải ghi MSSV",
                                 parent=self.view.root)
        else:
            try:
                delete = messagebox.askyesno(
                    "Delete", "Xóa sinh viên này ?", parent=self.view.root)
                if delete:
                    self.model.deleteStudent(
                        var_std_id=self.view.var_std_id.get())
                    self.fetch_data()
                    messagebox.showinfo("Delete", "Đã xóa",
                                        parent=self.view.root)
            except Exception as es:
                messagebox.showerror(
                    "Error", f"due to :{str(es)}", parent=self.root)

    # =========== delete all function ===========================
    def delete_all(self):
        try:
            delete = messagebox.askyesno(
                "Student Delete All", "Thông tin lớp cũ sẽ bị xóa hết, bạn chắc chứ ?", parent=self.root)
            if delete:
                self.fetch_data()

                messagebox.showinfo("Delete", "Đã làm mới", parent=self.root)
        except Exception as es:
            messagebox.showerror(
                "Error", f"due to :{str(es)}", parent=self.root)

    # =========== reset function ===========================
    def reset_data(self):
        self.view.var_dep.set("Chọn ngành")
        self.view.var_course.set("Chọn khóa")
        self.view.var_year.set("Chọn năm")
        self.view.var_semester.set("Chọn kỳ")
        self.view.var_std_id.set("")
        self.view.var_std_name.set("")
        self.view.var_div.set("Chọn lớp")
        self.view.var_roll.set("")
        self.view.var_gender.set("Giới tính")
        self.view.var_dob.set("")
        self.view.var_mail.set("")
        self.view.var_phone.set("")
        self.view.var_address.set("")
        self.view.var_teacher.set("")
        self.view.var_radio1.set("")

# ===================== generate data set (take photo sample) ==============
    # hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh
    def generate_dataset(self):
        if self.view.var_dep.get() == "Chọn ngành" or self.view.var_std_name.get() == "" or self.view.var_std_id.get() == "":
            messagebox.showerror(
                "Error", "Phải điền đầy các mục", parent=self.root)
        else:
            try:

                self.model.my_cursor.execute("select * from student")
                myResult = self.model.my_cursor.fetchall()
                id = self.view.var_std_id.get()
                for x in myResult:
                    if x[4] == int(id):
                        break
                self.model.my_cursor.execute("update student set dep=%s,course=%s,year=%s,semester=%s,division=%s,roll=%s,gender=%s,dob=%s,mail=%s,phone=%s,address=%s,teacher=%s,photoSample=%s where studentID=%s", (
                    self.view.var_dep.get(),
                    self.view.var_course.get(),
                    self.view.var_year.get(),
                    self.view.var_semester.get(),
                    # self.var_std_name.get(),
                    self.view.var_div.get(),
                    self.view.var_roll.get(),
                    self.view.var_gender.get(),
                    self.view.var_dob.get(),
                    self.view.var_mail.get(),
                    self.view.var_phone.get(),
                    self.view.var_address.get(),
                    self.view.var_teacher.get(),
                    self.view.var_radio1.get(),
                    self.view.var_std_id.get()
                ))
                self.model.conn.commit()
                self.fetch_data()

                self.reset_data()
                self.model.conn.close()

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

                            if img_id6 < 10:
                                img_id1 = img_id1 + 1
                                img_id6 = img_id6 + 1
                                face1 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                                file_name_path = Path.Data.images + \
                                    str(x[4])+"/"+str(img_id1)+".jpg"
                                cv2.imwrite(file_name_path, face1)
                                cv2.putText(face1, str(
                                    img_id1), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 255, 0), 2)
                                cv2.imshow("cropped face", face1)

                            if img_id4 < 10:
                                cv2.putText(img, 'NEN QUAY TRAI',
                                            (90, 30), font, 2, (255, 255, 128), 3)

                            if img_id3 < 10 and img_id4 == 10:
                                cv2.putText(img, 'NEN QUAY PHAI',
                                            (90, 30), font, 2, (255, 255, 128), 3)

                            if img_id2 < 5 and img_id3 == 10 and img_id4 == 10:
                                cv2.putText(img, 'NEN QUAY LEN',
                                            (30, 30), font, 2, (255, 255, 128), 3)

                            if img_id5 < 5 and img_id2 == 5 and img_id3 == 10 and img_id4 == 10:
                                cv2.putText(img, 'NEN QUAY XUONG',
                                            (30, 30), font, 2, (255, 255, 128), 3)

                            if ang1 >= 48 and img_id5 < 5:
                                cv2.putText(img, 'Head down', (30, 30),
                                            font, 2, (255, 255, 128), 3)
                                img_id1 = img_id1 + 1
                                img_id5 = img_id5 + 1
                                face1 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                                file_name_path = Path.Data.images + \
                                    str(x[4])+"/"+str(img_id1)+".jpg"
                                cv2.imwrite(file_name_path, face1)
                                cv2.putText(face1, str(
                                    img_id1), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 255, 0), 2)
                                cv2.imshow("cropped face", face1)

                            elif ang1 <= -48 and img_id2 < 5:
                                cv2.putText(img, 'Head up', (30, 30),
                                            font, 2, (255, 255, 128), 3)
                                img_id1 = img_id1 + 1
                                img_id2 = img_id2 + 1
                                face1 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                                file_name_path = Path.Data.images + \
                                    str(x[4])+"/"+str(img_id1)+".jpg"
                                cv2.imwrite(file_name_path, face1)
                                cv2.putText(face1, str(
                                    img_id1), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 255, 0), 2)
                                cv2.imshow("cropped face", face1)

                            if ang2 >= 48 and img_id3 < 10:
                                cv2.putText(img, 'Head right', (90, 30),
                                            font, 2, (255, 255, 128), 3)
                                img_id1 = img_id1 + 1
                                img_id3 = img_id3 + 1
                                face1 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                                file_name_path = Path.Data.images + \
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
                                file_name_path = Path.Data.images + \
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
                    "Error", f"due to :{str(es)}", parent=self.view.root)


# ========================================================================

    def train_classifier(self):
        os.system(f"python src/align_dataset_mtcnn.py  data/images data/image --image_size 160 --margin 32  --random_order --gpu_memory_fraction 0.25")
        os.system(f"python face_recognition/classifier.py TRAIN data/image Models/20180402-114759.pb Models/facemodel.pkl --batch_size 1000")
        messagebox.showinfo("Success", "training thành công",
                            parent=self.view.root)

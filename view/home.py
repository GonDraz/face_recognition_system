from tkinter import *
from PIL import Image, ImageTk
# from view.student import Student
import os

from store.themes.assets import *
# from face_recognition import *
# from attendance import Attendance
# from helper import Helper


class Home:
    def __init__(self, root):
        self.root = root

        # first imag
        logoImg = Image.open(Images.logo).resize((450, 130), Image.ANTIALIAS)
        self.logoPhotoImage = ImageTk.PhotoImage(logoImg)
        Label(self.root, image=self.logoPhotoImage).place(x=0, y=0, width=450, height=130)

        # second imag
        coverImg = Image.open(Images.coverPng).resize((450, 130), Image.ANTIALIAS)
        self.coverPhotoImage = ImageTk.PhotoImage(coverImg)
        Label(self.root, image=self.coverPhotoImage).place(x=450, y=0, width=450, height=130)

        # third imag
        smeImg = Image.open(Images.sme).resize((450, 130), Image.ANTIALIAS)
        self.smePhotoImg = ImageTk.PhotoImage(smeImg)
        Label(self.root, image=self.smePhotoImg).place(x=900, y=0, width=450, height=130)

        # bg imag
        backgroundImg = Image.open(Images.background).resize((1530, 700), Image.ANTIALIAS)
        self.backgroundPhotoImg = ImageTk.PhotoImage(backgroundImg)

        backgroundLbl = Label(self.root, image=self.backgroundPhotoImg)
        backgroundLbl.place(x=0, y=130, width=1530, height=710)

        Label(backgroundLbl, text="HỆ THỐNG ĐIỂM DANH BẰNG KHUÔN MẶT", font=("Arial", 30, "bold"), bg="white", fg="red").place(x=0, y=0, width=1530, height=45)

        # student button
        svImg = Image.open(Images.svPng).resize((180, 220), Image.ANTIALIAS)
        self.svPhotoImg = ImageTk.PhotoImage(svImg)
        Button(backgroundLbl, image=self.svPhotoImg,command=self.exit, cursor="hand2").place(x=300, y=50, width=180, height=220)
        Button(backgroundLbl, text="Thông tin sinh viên", command=self.exit,cursor="hand2", font=("Arial", 12, "bold"), bg="darkblue", fg="white").place(x=300, y=250, width=180, height=40)

        # face rec button
        faceRecImg = Image.open(Images.faceRec).resize((180, 220), Image.ANTIALIAS)
        self.faceRecPhotoImg = ImageTk.PhotoImage(faceRecImg)
        Button(backgroundLbl, image=self.faceRecPhotoImg,cursor="hand2", command=self.face_data).place(x=600, y=50, width=180, height=220)
        Button(backgroundLbl, text="Điểm danh", cursor="hand2", command=self.face_data, font=(Fonts.primary, 15, "bold"), bg="darkblue", fg="white").place(x=600, y=250, width=180, height=40)

        # Attendance button
        checkListImg = Image.open(Images.checkList).resize((180, 220), Image.ANTIALIAS)
        self.checkListPhotoImg = ImageTk.PhotoImage(checkListImg)
        Button(backgroundLbl, image=self.checkListPhotoImg,cursor="hand2", command=self.attendance).place(x=900, y=50, width=180, height=220)
        Button(backgroundLbl, text="Báo cáo", cursor="hand2", command=self.attendance, font=("Arial", 15, "bold"), bg="darkblue", fg="white").place(x=900, y=250, width=180, height=40)

        # Help button
        helpImg = Image.open(Images.help).resize((180, 220), Image.ANTIALIAS)
        self.helpPhotoImg = ImageTk.PhotoImage(helpImg)

        Button(backgroundLbl, image=self.helpPhotoImg,cursor="hand2", command=self.helper).place(x=450, y=300, width=180, height=220)
        Button(backgroundLbl, text="Trợ giúp", cursor="hand2", command=self.helper, font=("Arial", 15, "bold"), bg="darkblue", fg="white").place(x=450, y=500, width=180, height=40)

        # Train button
        # img8=Image.open(r"college_image\HUST.jpg")
        # img8=img8.resize((180,220),Image.ANTIALIAS)
        # self.photoimg8=ImageTk.PhotoImage(img8)

        # b1=Button(bg_img,image=self.photoimg8,cursor="hand2",command=self.train_data)
        # b1.place(x=150,y=300,width=180,height=220)

        # b1_1=Button(bg_img,text="",cursor="hand2",command=self.train_data,font=("Arial",15,"bold"), bg="darkblue", fg="white")
        # b1_1.place(x=150,y=500,width=180,height=40)

        # Photo Data button
        # img9=Image.open(r"college_image\HUST.jpg")
        # img9=img9.resize((180,220),Image.ANTIALIAS)
        # self.photoimg9=ImageTk.PhotoImage(img9)

        # b1=Button(bg_img,image=self.photoimg9,cursor="hand2",command=self.open_img)
        # b1.place(x=450,y=300,width=180,height=220)

        # b1_1=Button(bg_img,text="Photo",cursor="hand2",command=self.open_img,font=("Arial",15,"bold"), bg="darkblue", fg="white")
        # b1_1.place(x=450,y=500,width=180,height=40)

        # #Developer button
        # img10=Image.open("./HUST.jpg")
        # img10=img10.resize((180,220),Image.ANTIALIAS)
        # self.photoimg10=ImageTk.PhotoImage(img10)

        # b1=Button(bg_img,image=self.photoimg10,cursor="hand2")
        # b1.place(x=600,y=300,width=180,height=220)

        # b1_1=Button(bg_img,text="Developer",cursor="hand2",font=("Arial",15,"bold"), bg="darkblue", fg="white")
        # b1_1.place(x=600,y=500,width=180,height=40)

        # Exit button
        HUSTImg = Image.open(Images.HUST).resize((180, 220), Image.ANTIALIAS)
        self.HUSTPhotoImg = ImageTk.PhotoImage(HUSTImg)
        Button(backgroundLbl, image=self.HUSTPhotoImg,cursor="hand2", command=self.exit).place(x=750, y=300, width=180, height=220)
        Button(backgroundLbl, text="Thoát", cursor="hand2", font=("Arial", 15, "bold"), bg="darkblue", fg="white", command=self.exit).place(x=750, y=500, width=180, height=40)

    def open_img(self):
        os.startfile("data")

    # ================Function buttons===============

    def student_details(self):
        self.new_window = Toplevel(self.root)
        self.app = Student(self.new_window)

    def face_data(self):
        os.system("python face_recognition/face_rec_cam.py")

    def helper(self):
        self.new_window = Toplevel(self.root)
        self.app = Helper(self.new_window)

    def attendance(self):
        self.new_window = Toplevel(self.root)
        self.app = Attendance(self.new_window)

    def exit(self):
        self.root.quit()

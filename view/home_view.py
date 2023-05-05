from tkinter import *
from PIL import ImageTk
from store.assets import *

# from face_recognition import *
# from attendance import Attendance
# from helper import Helper


class HomeView:

    def __init__(self, root, controller):
        self.root = root
        self.controller = controller

        # first imag
        self.logoImg = ImageTk.PhotoImage(
            Images.logo.resize((450, 130), Image.ANTIALIAS))
        Label(self.root, image=self.logoImg).place(
            x=0, y=0, width=450, height=130)

        # second imag
        self.coverImg = ImageTk.PhotoImage(Images.coverPng.resize(
            (450, 130), Image.ANTIALIAS))
        Label(self.root, image=self.coverImg).place(
            x=450, y=0, width=450, height=130)

        # third imag
        self.smeImg = ImageTk.PhotoImage(
            Images.sme.resize((450, 130), Image.ANTIALIAS))
        Label(self.root, image=self.smeImg).place(
            x=900, y=0, width=450, height=130)

        # bg imag
        self.backgroundImg = ImageTk.PhotoImage(Images.background.resize(
            (1530, 700), Image.ANTIALIAS))
        backgroundLbl = Label(self.root, image=self.backgroundImg)
        backgroundLbl.place(x=0, y=130, width=1530, height=710)

        Label(backgroundLbl, text="HỆ THỐNG ĐIỂM DANH BẰNG KHUÔN MẶT", font=(
            Fonts.primary, 30, "bold"), bg=Colors.background, fg=Colors.highlightText).place(x=0, y=0, width=1530, height=45)

        # student button
        self.svImg = ImageTk.PhotoImage(
            Images.svPng.resize((180, 220), Image.ANTIALIAS))
        Button(backgroundLbl, image=self.svImg, command=controller.openStudentWindow,
               cursor="hand2").place(x=300, y=50, width=180, height=220)
        Button(backgroundLbl, text="Thông tin sinh viên", command=controller.openStudentWindow, cursor="hand2", font=(
            Fonts.primary, 12, "bold"), bg=Colors.button, fg=Colors.textButton).place(x=300, y=250, width=180, height=40)

        # face rec button
        self.faceRecImg = ImageTk.PhotoImage(Images.faceRec.resize(
            (180, 220), Image.ANTIALIAS))
        Button(backgroundLbl, image=self.faceRecImg, cursor="hand2",
               command=controller.face_data).place(x=600, y=50, width=180, height=220)
        Button(backgroundLbl, text="Điểm danh", cursor="hand2", command=controller.face_data, font=(
            Fonts.primary, 15, "bold"), bg=Colors.button, fg=Colors.textButton).place(x=600, y=250, width=180, height=40)

        # Attendance button
        self.checkListImg = ImageTk.PhotoImage(Images.checkList.resize(
            (180, 220), Image.ANTIALIAS))
        Button(backgroundLbl, image=self.checkListImg, cursor="hand2",
               command=controller.attendance).place(x=900, y=50, width=180, height=220)
        Button(backgroundLbl, text="Báo cáo", cursor="hand2", command=controller.attendance, font=(
            Fonts.primary, 15, "bold"), bg=Colors.button, fg=Colors.textButton).place(x=900, y=250, width=180, height=40)

        # Help button
        self.helpImg = ImageTk.PhotoImage(
            Images.help.resize((180, 220), Image.ANTIALIAS))

        Button(backgroundLbl, image=self.helpImg, cursor="hand2",
               command=controller.helper).place(x=450, y=300, width=180, height=220)
        Button(backgroundLbl, text="Trợ giúp", cursor="hand2", command=controller.helper, font=(
            Fonts.primary, 15, "bold"), bg=Colors.button, fg=Colors.textButton).place(x=450, y=500, width=180, height=40)

        # Exit button
        self.HUSTImg = ImageTk.PhotoImage(
            Images.HUST.resize((180, 220), Image.ANTIALIAS))
        Button(backgroundLbl, image=self.HUSTImg, cursor="hand2",
               command=controller.quit).place(x=750, y=300, width=180, height=220)
        Button(backgroundLbl, text="Thoát", cursor="hand2", font=(Fonts.primary, 15, "bold"),
               bg=Colors.button, fg=Colors.textButton, command=controller.quit).place(x=750, y=500, width=180, height=40)
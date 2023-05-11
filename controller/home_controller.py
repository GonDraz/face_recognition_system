

import os
from tkinter import Toplevel
from models.home_model import HomeModel
from router.router import Router
from store.window_setup import WindowSetup
from view.home_view import HomeView


class HomeController:
    def __init__(self, root):
        self.root = root
        self.root.geometry(WindowSetup.screen)
        self.root.title("Hệ thống điểm danh")

        self.model = HomeModel()
        self.view = HomeView(root, self)

        self.root.mainloop()

    def open_img(self):
        os.startfile("data")

    # ================Function buttons===============
    def openStudentWindow(self):
        Router.student(Toplevel(self.root))

    def faceRecCam(self):
        Router.faceRecCam(Toplevel(self.root))

    def helper(self):
        Router.helper(Toplevel(self.root))

    def attendance(self):
        Router.attendance(Toplevel(self.root))

    def quit(self):
        self.view.root.quit()

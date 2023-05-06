

from tkinter import *
from PIL import Image, ImageTk

from models.help_model import HelpModel
from store.path import Path
from store.window_setup import WindowSetup
from view.help_view import HelpView


class HelpController:
    def __init__(self, root):

        self.root = root
        self.root.geometry(WindowSetup.screen)
        self.root.title("Trợ giúp")

        self.model = HelpModel()
        self.view = HelpView(root, self)

        self.page = 1

        self.root.mainloop()

    def nextPage(self):
        self.page += 1

        if self.page > 8:
            self.page = 1

        self.photoImg = ImageTk.PhotoImage(Image.open(
            f"{Path.helperImage}{str(self.page)}.PNG").resize((1250, 700), Image.ANTIALIAS))
        self.view.f_lbl.config(image=self.photoImg)

    def backPage(self):
        self.page -= 1

        if self.page < 1:
            self.page = 8
        self.photoImg = ImageTk.PhotoImage(Image.open(
            f"{Path.helperImage}{str(self.page)}.PNG").resize((1250, 700), Image.ANTIALIAS))
        self.view.f_lbl.config(image=self.photoImg)

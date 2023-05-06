from tkinter import *
from PIL import Image, ImageTk
from store.assets import *

from store.path import Path


class HelpView:
    def __init__(self, root, controller):
        self.controller = controller
        self.root = root

        self.photoImg = ImageTk.PhotoImage(Image.open(f"{Path.helperImage}1.PNG").resize(
            (1250, 700), Image.ANTIALIAS))

        self.f_lbl = Label(self.root, image=self.photoImg)
        self.f_lbl.place(x=0, y=0, width=1250, height=700)

        Button(self.root, text="Tiếp theo", width=10, height=2, font=(
            Fonts.primary, 12, "bold"), bg=Colors.button, fg=Colors.textButton, command=self.controller.nextPage).place(x=1250, y=250)

        Button(self.root, text="Quay lại", width=10, height=2, font=(
            Fonts.primary, 12, "bold"), bg=Colors.button, fg=Colors.textButton, command=self.controller.backPage).place(x=1250, y=420)

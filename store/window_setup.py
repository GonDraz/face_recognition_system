from tkinter import *


class WindowSetup:
    height = 1530
    width = 790
    
    screen = f"{height}x{width}"
    
    root = Tk()
    # window.iconphoto(False, PhotoImage(file=Images.windowLogo))
    root.resizable(width=False, height=False)

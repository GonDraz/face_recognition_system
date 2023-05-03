from store.window_setup import *


class WindowController:
    root = WindowSetup.root

        
    def exit(self):
        self.root.quit()

    def openNewWindow(self, window):
        self.newWindow=Toplevel(self.root)
        window(self.newWindow)
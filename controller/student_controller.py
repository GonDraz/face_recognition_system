

from models.student_model import StudentModel
from store.window_setup import WindowSetup
from view.student_view import StudentView


class StudentController:
    def __init__(self, root):

        self.root = root
        self.root.geometry(WindowSetup.screen)
        self.root.title("Thông tin sinh viên")

        self.model = StudentModel()
        self.view = StudentView(root, self)

        self.root.mainloop()

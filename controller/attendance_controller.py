

from models.attendance_model import AttendanceModel
from store.window_setup import WindowSetup
from view.attendance_view import AttendanceView


class AttendanceController:
    def __init__(self, root):

        self.root = root
        self.root.geometry(WindowSetup.screen)
        self.root.title("Báo cáo điểm danh")
        self.model = AttendanceModel()
        self.view = AttendanceView(root, self)

        self.root.mainloop()


from controller.window_controller import WindowController


class HomeController:
    def openStudentWindow(self):
        from view.student import Student        
        WindowController.openNewWindow(Student)
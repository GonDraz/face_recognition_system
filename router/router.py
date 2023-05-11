

class Router:

    def home(root):
        from controller.home_controller import HomeController
        HomeController(root)

    def student(root):
        from controller.student_controller import StudentController
        StudentController(root)

    def helper(root):
        from controller.help_controller import HelpController
        HelpController(root)

    def attendance(root):
        from controller.attendance_controller import AttendanceController
        AttendanceController(root)

    def faceRecCam(root):
        from controller.face_rec_cam_controller import FaceRecCamController
        FaceRecCamController(root)

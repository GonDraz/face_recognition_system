

class Router:
    
    def home(root):
        from controller.home_controller import HomeController
        HomeController(root = root)

    def student(root):
        from controller.student_controller import StudentController
        StudentController(root = root)
    
    def helper(root):
        return 
    
    def attendance(root):
        return 
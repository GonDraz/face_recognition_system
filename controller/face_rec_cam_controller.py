

from models.face_rec_cam_model import FaceRecCamModel
from store.window_setup import WindowSetup
from view.face_rec_cam_view import FaceRecCamView


class FaceRecCamController:
    def __init__(self, root):

        self.root = root
        self.root.geometry(WindowSetup.screen)
        self.root.title("Điểm danh")

        self.view = FaceRecCamView(root, self)

        def on_closing():
            self.view.root.quit()

        self.view.root.protocol("WM_DELETE_WINDOW", on_closing)

        self.model = FaceRecCamModel()

        self.view.root.mainloop()

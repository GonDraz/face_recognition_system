

from models.face_rec_cam_model import FaceRecCamModel
from store.window_setup import WindowSetup
from view.face_rec_cam_view import FaceRecCamView


class FaceRecCamController:
    def __init__(self, root):

        self.root = root
        self.root.geometry(WindowSetup.screen)
        self.root.title("Điểm danh")

        self.view = FaceRecCamView(root, self)

        self.model = FaceRecCamModel()

        self.view.root.mainloop()



from store.assets import Assets


class Path:
    helperImage = Assets._images + "helper_image/"

    class Data:
        _data = "data/"

        info = _data + "info/"
        images = _data + "images/"

    class Include:
        _include = "include/"

        _model = _include + "models/"

        faceModel = _model + "facemodel.pkl"

        pb = _model + "20180402-114759.pb"

        align = _include + "align"

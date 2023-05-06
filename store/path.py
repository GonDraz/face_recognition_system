

from store.assets import Assets


class Path:
    helperImage = Assets._images + "helper_image/"

    class Data:
        _data = "data/"

        info = _data + "info/"
        images = _data + "images/"

    class Include:
        _include = "include/"

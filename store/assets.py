from PIL import Image

class Assets:
    _assets = "./assets/"
    _fonts = _assets + "fonts/"
    _images = _assets + "images/"
    _icons = _assets + "icons/"
    _sounds = _assets + "sounds/"


class Fonts:
    primary = "Arial"

class Images:
    background = Image.open(Assets._images + "background.jpg")
    checkList = Image.open(Assets._images + "check_list.jpg")
    classJpg = Image.open(Assets._images + "class.jpg")
    classPng = Image.open(Assets._images + "class.png")
    coverJpg = Image.open(Assets._images + "cover.jpg")
    coverPng = Image.open(Assets._images + "cover.png")
    faceRec = Image.open(Assets._images + "face_rec.png")
    help = Image.open(Assets._images + "help.png")
    HUSTMid = Image.open(Assets._images + "HUST_mid.png")
    HUST = Image.open(Assets._images + "HUST.jpg")
    HUST1 = Image.open(Assets._images + "HUST1.png")
    logo = Image.open(Assets._images + "logo.png")
    sis = Image.open(Assets._images + "sis.png")
    sme = Image.open(Assets._images + "sme.png")
    svJpg = Image.open(Assets._images + "sv.jpg")
    svPng = Image.open(Assets._images + "sv.png")


class Colors:
    textButton = "white"
    button = "darkblue"
    background = "white"
    highlightText = "red"

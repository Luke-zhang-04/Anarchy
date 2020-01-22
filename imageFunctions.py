from PIL import Image, ImageTk #sudo pip install pillow into terminal if PythonPackageInstaller doesn't work

def pack(image): #returns a photoimage
    return ImageTk.PhotoImage(image)


def resize_image(image, x, y): #resizes image
    return image.resize((x, y), Image.ANTIALIAS)


def crop_image(image, left, right, top, bottom): #crops image
    return image.crop((left, top, right, bottom))
from lib.install_packages import install #from https://github.com/kertox662/PythonPackageInstaller
install()

from tkinter import Tk, Canvas, PhotoImage
from time import sleep
from random import choice
from PIL import Image, ImageTk #sudo pip install pillow into terminal
import json
myInterface = Tk()
screen = Canvas(myInterface, width=1280, height=720, background = "gray9")
screen.pack()
screen.update()

def resize_image(image, *args):
    image_file = Image.open(image)
    image_file = image_file.resize((args[0], args[1]), Image.ANTIALIAS)
    image_file = ImageTk.PhotoImage(image_file)
    return image_file

class card:
    def __init__(self):
        with open('choices.json') as fin:
            data = json.load(fin)
            self.situation = choice(data['choices'])

    @staticmethod
    def round_rectangle(x1, y1, x2, y2, radius=25, **kwargs): #For drawing a round rectangle

        points = [x1+radius, y1, x1+radius, y1, x2-radius, y1, x2-radius,
        y1, x2, y1, x2, y1+radius, x2, y1+radius, x2, y2-radius, x2,
        y2-radius, x2, y2, x2-radius, y2, x2-radius, y2, x1+radius, y2,
        x1+radius, y2, x1, y2, x1, y2-radius, x1, y2-radius, x1, y1+radius,
        x1, y1+radius, x1, y1]

        return screen.create_polygon(points, **kwargs, smooth=True)

    def draw(self):
        width, height = screen.winfo_width(), screen.winfo_height()

        self.card_body = self.round_rectangle(
            width//2-150, height//2-300, width//2+150, height//2+200, radius = 25, fill = "gray50"
        )

        dimensions = screen.bbox(self.card_body)

        self.card_title_area = self.round_rectangle(
            dimensions[0]+50, dimensions[1]+25, dimensions[2]-50, dimensions[1]+75, radius = 20, fill = "gray15"
        )

        self.card_image_area = self.round_rectangle(
            dimensions[0]+50, dimensions[1]+100, dimensions[2]-50, dimensions[3]-250, radius = 20, fill = "gray75"
        )
        
        #self.card_text_area = self.round_rectangle(
        #    dimensions[0]+50, dimensions[1]+275, dimensions[2]-50, dimensions[3]-50, radius = 20, fill = "gray15"
        #)
        self.card_image_file = resize_image(self.situation['image'], self.situation['resize']['x'], self.situation['resize']['y'])
        
        self.card_image = screen.create_image(
            (dimensions[0]+dimensions[2])//2, dimensions[3]-250, anchor = "s", image = self.card_image_file
        )

        self.person = screen.create_text(
            dimensions[0]+50, dimensions[1]+275, anchor = "nw", text = self.situation['title']
        )

        self.text = screen.create_text(
            dimensions[0]+50, dimensions[1]+300, width = (dimensions[2]-50)-(dimensions[0]+50), anchor = "nw",
            text = self.situation['description']
        )

card1 = card()

card1.draw()

screen.update()
screen.mainloop()
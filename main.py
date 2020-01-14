from lib.install_packages import install #from https://github.com/kertox662/PythonPackageInstaller
install()

from tkinter import Tk, Canvas, PhotoImage
from time import sleep
from random import choice
from PIL import Image, ImageTk #sudo pip install pillow into terminal if PythonPackageInstaller doesn't work
import json
myInterface = Tk()
screen = Canvas(myInterface, width=1280, height=720, background = "gray9")
screen.pack()
screen.update()

def copyFile(copyFrom, copyTo):
    source = open(copyFrom, 'r')
    read = source.readlines()
    source.close()

    out = open(copyTo, 'w')

    for i in read:
        out.write(i)
    
    out.close()

def pack(image):
    return ImageTk.PhotoImage(image)

def resize_image(image, x, y):
    return image.resize((x, y), Image.ANTIALIAS)

def crop_image(image, left, right, top, bottom):
    return image.crop((left, top, right, bottom))

class military:
    def __init__(self, screen):
        self.screen = screen
        image_file = resize_image(Image.open("pictures/icons/gun-trans.png"), 40, 50)
        self.image_file = pack(image_file)
        self.image = screen.create_image(10, 60, anchor = 'sw', image = self.image_file)

    def __add__(self, other):
        cropped_image_file = resize_image(Image.open("pictures/icons/gun-white.png"), 40, 50)
        width, height = cropped_image_file.size

        increment = height/100
        percentage = height-other*increment

        cropped_image_file = crop_image(cropped_image_file, 0, 40, percentage, 50)
        self.cropped_image_file = pack(cropped_image_file)
        self.cropped_image = self.screen.create_image(10, 60, anchor = 'sw', image = self.cropped_image_file)
        return self

class money:
    def __init__(self, screen):
        self.screen = screen
        self.image_file = resize_image(Image.open("pictures/icons/money-trans.png"), 40, 50)
        self.image_file = pack(self.image_file)
        self.image = screen.create_image(50, 60, anchor = 'sw', image = self.image_file)

class nature:
    def __init__(self, screen):
        self.screen = screen
        self.image_file = resize_image(Image.open("pictures/icons/plant-trans.png"), 40, 50)
        self.image_file = pack(self.image_file)
        self.image = screen.create_image(90, 60, anchor = 'sw', image = self.image_file)

class people:
    def __init__(self, screen):
        self.screen = screen
        self.image_file = resize_image(Image.open("pictures/icons/people-trans.png"), 70, 50)
        self.image_file = pack(self.image_file)
        self.image = screen.create_image(120, 60, anchor = 'sw', image = self.image_file)

class card:
    def __init__(self, screen):
        self.screen = screen
        with open('choices.json') as fin:
            data = json.load(fin)
            print(list(data['choices']), "\n\n", data['choices'])
            self.situation = choice(list(data['choices']))
            self.situation = data['choices'][self.situation]
            self.person = self.situation[0]
            self.situation = choice(self.situation[1:])
            #self.situation = data['choices'][-1]

    @staticmethod
    def round_rectangle(screen, x1, y1, x2, y2, radius=25, **kwargs): #For drawing a round rectangle

        points = [x1+radius, y1, x1+radius, y1, x2-radius, y1, x2-radius,
        y1, x2, y1, x2, y1+radius, x2, y1+radius, x2, y2-radius, x2,
        y2-radius, x2, y2, x2-radius, y2, x2-radius, y2, x1+radius, y2,
        x1+radius, y2, x1, y2, x1, y2-radius, x1, y2-radius, x1, y1+radius,
        x1, y1+radius, x1, y1]

        return screen.create_polygon(points, **kwargs, smooth=True)

    def draw(self):
        width, height = screen.winfo_width(), screen.winfo_height()

        #create card body
        self.body = self.round_rectangle(
            self.screen, width//2-150, height//2-300, width//2+150, height//2+200, radius = 25, fill = "gray50"
        )

        #dimensions of the card
        dimensions = screen.bbox(self.body)

        #top area of card
        self.top_area = self.round_rectangle(
            self.screen, dimensions[0]+50, dimensions[1]+25, dimensions[2]-50, dimensions[1]+75, radius = 20, fill = "gray15"
        )

        #image area of card
        self.image_area = self.round_rectangle(
            self.screen, dimensions[0]+50, dimensions[1]+100, dimensions[2]-50, dimensions[3]-250, radius = 20, fill = "gray75"
        )
        
        #open card image
        print(self.situation)
        self.image_file = choice(self.person["image"]) if type(self.person["image"][0]) == list else self.person["image"]

        #resize the image
        self.image_file = resize_image(
            Image.open(self.image_file[0]), self.image_file[1], self.image_file[2]
        )
        
        #create the image
        self.image = screen.create_image(
            (dimensions[0]+dimensions[2])//2, dimensions[3]-250, anchor = "s", image = self.image_file
        )

        #create text of person speaking
        self.person = screen.create_text(
            dimensions[0]+50, dimensions[1]+275, anchor = "nw", text = self.person['title']
        )

        #create text of persons name and title
        self.text = screen.create_text(
            dimensions[0]+50, dimensions[1]+300, width = (dimensions[2]-50)-(dimensions[0]+50), anchor = "nw",
            text = self.situation['description']
        )

copyFile('choices.json', 'choices-user.json')

test, test2, test3, test4 = military(screen), money(screen), nature(screen), people(screen)
test += 50
#test = test+100
#print(test)

'''
while True:
    card1 = card(screen)
    card1.draw()

    screen.update()
    sleep(2)
'''
screen.update()
screen.mainloop()
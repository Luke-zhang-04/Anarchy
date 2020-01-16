from lib.install_packages import install #from https://github.com/kertox662/PythonPackageInstaller
install()
from PIL import Image, ImageTk #sudo pip install pillow into terminal if PythonPackageInstaller doesn't work

from tkinter import Tk, Canvas, PhotoImage
from time import sleep
from random import choice
import json


def copyFile(copyFrom, copyTo):
    source = open(copyFrom, 'r')
    read = source.readlines()
    source.close()

    out = open(copyTo, 'w')

    for i in read:
        out.write(i)
    
    out.close()


def pack(image): #returns a photoimage
    return ImageTk.PhotoImage(image)


def resize_image(image, x, y): #resizes image
    return image.resize((x, y), Image.ANTIALIAS)


def crop_image(image, left, right, top, bottom): #crops image
    return image.crop((left, top, right, bottom))


#Icon class for adding and subtracting values
class icon:
    def __add__(self, other):
        cropped_image_file = resize_image(Image.open("pictures/icons/" + self.filled_file_name), self.resize[0], self.resize[1])
        width, height = cropped_image_file.size

        increment = height/100
        self.current = self.current + other if self.current + other < 100 else 100
        self.amt = height-self.current*increment

        if self.amt > height: self.amt = amt

        print(self.amt, other, self.amt+other)

        cropped_image_file = crop_image(cropped_image_file, 0, self.resize[0], self.amt, self.resize[1])
        self.cropped_image_file = pack(cropped_image_file)
        self.screen.delete(self.cropped_image)

        self.cropped_image = self.screen.create_image(
            self.place[0], self.place[1], anchor = 'sw', image = self.cropped_image_file
        )

        return self
    
    def delete(self): #we don't want to use __del__ because we only want to screen.delete()
        self.screen.delete(self.cropped_image)


#military meter, inherits __add__ from icon class
class military(icon):
    def __init__(self, screen):
        self.screen = screen
        self.filled_file_name = "gun-white.png"
        image_file = resize_image(Image.open("pictures/icons/gun-trans.png"), 40, 50)
        self.image_file = pack(image_file)
        self.image = screen.create_image(10, 60, anchor = 'sw', image = self.image_file)
        self.current = 0
        self.cropped_image = None
        self.resize = 40, 50
        self.place = 10, 60


#money meter, inherits __add__ from icon class
class money(icon):
    def __init__(self, screen):
        self.screen = screen
        self.filled_file_name = "money-white.png"
        image_file = resize_image(Image.open("pictures/icons/money-trans.png"), 40, 50)
        self.image_file = pack(image_file)
        self.image = screen.create_image(50, 60, anchor = 'sw', image = self.image_file)
        self.current = 0
        self.cropped_image = None
        self.resize = 40, 50
        self.place = 50, 60


#nature meter, inherits __add__ from icon class
class nature(icon):
    def __init__(self, screen):
        self.screen = screen
        self.filled_file_name = "plant-white.png"
        self.image_file = resize_image(Image.open("pictures/icons/plant-trans.png"), 40, 50)
        self.image_file = pack(self.image_file)
        self.image = screen.create_image(90, 60, anchor = 'sw', image = self.image_file)
        self.current = 0
        self.cropped_image = None
        self.resize = 40, 50
        self.place = 90, 60


#people meter, inherits __add__ from icon class
class people(icon):
    def __init__(self, screen):
        self.screen = screen
        self.filled_file_name = "people-white.png"
        self.image_file = resize_image(Image.open("pictures/icons/people-trans.png"), 70, 50)
        self.image_file = pack(self.image_file)
        self.image = screen.create_image(120, 60, anchor = 'sw', image = self.image_file)
        self.current = 0
        self.cropped_image = None
        self.resize = 70, 50
        self.place = 120, 60


class card:
    def __init__(self, screen):
        self.body = self.top_area = self.image_file = self.image_file = self.image = self.person = self.text = None
        self.screen = screen
        with open('choices.json') as fin:
            data = json.load(fin)
            print(list(data['choices']), "\n\n", data['choices'])
            situation = choice(list(data['choices']))
            situation = data['choices'][situation]
            self.person = situation[0]
            self.situation = choice(situation[1:])

    @staticmethod
    def round_rectangle(screen, x1, y1, x2, y2, radius=25, **kwargs): #For drawing a round rectangle

        points = [x1+radius, y1, x1+radius, y1, x2-radius, y1, x2-radius,
        y1, x2, y1, x2, y1+radius, x2, y1+radius, x2, y2-radius, x2,
        y2-radius, x2, y2, x2-radius, y2, x2-radius, y2, x1+radius, y2,
        x1+radius, y2, x1, y2, x1, y2-radius, x1, y2-radius, x1, y1+radius,
        x1, y1+radius, x1, y1]

        return screen.create_polygon(points, **kwargs, smooth=True)

    def draw(self):
        screen = self.screen
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
        self.image_file = choice(self.person["image"]) if type(self.person["image"][0]) == list else self.person["image"]

        #resize the image
        self.image_file = resize_image(
            Image.open(self.image_file[0]), self.image_file[1], self.image_file[2]
        )
        
        self.image_file = pack(self.image_file)

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

    def user_click_yes(self, event):
        print()
    
    def user_click_no(self, event):
        print()

    def __del__(self):
        #delete card
        self.screen.delete(self.body, self.top_area, self.image_file, self.image, self.person, self.text, self.image_area)
        del self


def draw_arrows(screen):
    left = resize_image(Image.open("pictures/button-left.png"), 50, 50)
    right = resize_image(Image.open("pictures/button-right.png"), 50, 50)
    left1 = pack(left)
    right1 = pack(right)
    leftButton = screen.create_image(320, 360, image = left1)
    rightButton = screen.create_image(900, 360, image = right1)
    screen.update()
    return leftButton, rightButton, left1, right1


def runGame():
    myInterface = Tk()
    screen = Canvas(myInterface, width=1280, height=720, background = "gray9")
    screen.pack()
    screen.update()

    copyFile('choices.json', 'choices-user.json')

    gun, dollar, leaf, person = military(screen), money(screen), nature(screen), people(screen)

    for i in range(25):
        gun.delete(), dollar.delete(), leaf.delete(), person.delete()
        gun += 2
        dollar += 2
        leaf += 2
        person += 2

        screen.update()
        sleep(0.03)

    leftArrow, rightArrow , leftImage, rightImage = draw_arrows(screen)

    while True:
        card1 = card(screen)
        card1.draw()
        screen.tag_bind(leftArrow, "<Button-1>", card1.user_click_no)
        screen.tag_bind(rightArrow, "<Button-1>", card1.user_click_yes)

        screen.update()
        sleep(2)
        del card1

    screen.update()
    screen.mainloop()

if __name__ == "__main__":
    runGame()
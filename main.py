from imageFunctions import *
from icons import *

from tkinter import Tk, Canvas
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


class card:
    def __init__(self, screen):
        self.body = self.top_area = self.image_file = self.image_file = self.image = self.person = self.text = None
        self.screen = screen
        self.decided = False
        self.choice = None
        with open('choices.json') as fin:
            data = json.load(fin)
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

    def move(self, direction):
        if direction.lower() in ["r", "right", "e", "east"]:
            xSpeed = 25
            ySpeed = 0
        elif direction.lower() in ["l", "left", "w", "west"]:
            xSpeed = -25
            ySpeed = 0
        
        for element in self.elements:
            self.screen.move(element, xSpeed, ySpeed)
        
        if self.screen.coords(self.body)[-2] > self.screen.winfo_width() or self.screen.coords(self.body)[8] < 0:
            return True
        else:
            return False

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
            dimensions[0]+50, dimensions[1]+275, anchor = "nw", text = self.person['title'], font=("Courier")
        )

        #create text of persons name and title
        self.text = screen.create_text(
            dimensions[0]+50, dimensions[1]+300, width = (dimensions[2]-50)-(dimensions[0]+50), anchor = "nw",
            text = self.situation['description'], font=("Courier")
        )

        self.elements = [self.body, self.top_area, self.image_file, self.image, self.person, self.text, self.image_area]

    def __del__(self): #delete card
        self.screen.delete(self.body, self.top_area, self.image_file, self.image, self.person, self.text, self.image_area)
        del self


class anarchy():
    def __init__(self):
        myInterface = Tk()
        self.screen = Canvas(myInterface, width=1280, height=720, background = "gray9")
        self.screen.pack()
        self.screen.update()
        self.week = 0

        copyFile('choices.json', 'choices-user.json')

        self.gun, self.dollar, self.leaf, self.person = (
            military(self.screen), money(self.screen), nature(self.screen), people(self.screen)
        )

        for i in range(25):
            self.gun.canvas_delete(), self.dollar.canvas_delete(), self.leaf.canvas_delete(), self.person.canvas_delete()
            self.gun += 2
            self.dollar += 2
            self.leaf += 2
            self.person += 2

            self.screen.update()
            sleep(0.03)
    
    def user_click_no(self, event):
        #addition = self.card1.situation["false"]
        self.card1.decided = True
        self.card1.choice = False
        '''
        self.gun += addition['military']
        self.dollar += addition['economy']
        self.leaf += addition['nature']
        self.person += addition['people']
        '''

    def user_click_yes(self, event):
        #addition = self.card1.situation["true"]
        self.card1.choice = self.card1.decided = True
        '''
        self.gun += addition['military']
        self.dollar += addition['economy']
        self.leaf += addition['nature']
        self.person += addition['people']
        '''

    def draw_arrows(self):
        self.left = resize_image(Image.open("pictures/button-left.png"), 50, 50)
        self.right = resize_image(Image.open("pictures/button-right.png"), 50, 50)
        self.leftPhotoImg = pack(self.left)
        self.rightPhotoImg = pack(self.right)
        self.leftButton = self.screen.create_image(320, 360, image = self.leftPhotoImg)
        self.rightButton = self.screen.create_image(960, 360, image = self.rightPhotoImg)
        self.screen.update()
    
    def animate_icons(self, comparison):
        change = False
        if self.person.current > comparison['people']:
            change = True
            self.person -= 1
        elif self.person.current < comparison['people']:
            change = True
            self.person += 1

        if self.gun.current > comparison['military']:
            change = True
            self.gun -= 1
        elif self.gun.current < comparison['military']:
            change = True
            self.gun += 1 
        
        if self.leaf.current > comparison['nature']:
            change = True
            self.leaf -= 1
        elif self.leaf.current < comparison['nature']:
            change = True
            self.leaf += 1
        
        if self.dollar.current > comparison['economy']:
            change = True
            self.dollar -= 1
        elif self.dollar.current < comparison['economy']:
            change = True
            self.dollar += 1
        
        return change

    def run(self):
        while True:
            self.draw_arrows()
            self.card1 = card(self.screen)
            self.card1.draw()
            self.screen.tag_bind(self.leftButton, "<Button-1>", self.user_click_no)
            self.screen.tag_bind(self.rightButton, "<Button-1>", self.user_click_yes)

            numWeeks = self.screen.create_text(
                1200, 10, anchor = "ne", text = "Week: " + str(self.week), fill = 'white', font=("Courier", 44)
            )

            self.screen.update()
            while not self.card1.decided:
                self.screen.update()
                sleep(0.01)
        
            comparison = self.card1.situation['true'] if self.card1.choice else self.card1.situation['false']
            targets = {}
            targets["people"] = comparison["people"] + self.person.current
            targets["military"] = comparison["military"] + self.gun.current
            targets["economy"] = comparison["economy"] + self.dollar.current
            targets["nature"] = comparison["nature"] + self.leaf.current
            for i in targets:
                if targets[i] > 100: targets[i] = 100
                elif targets[i] < 0: targets[i] = 0

            direction = "r" if self.card1.choice else "l"
            move_finished = icons_finished = False
            
            while True:
                if self.card1.move(direction):
                    move_finished = True
                if not self.animate_icons(targets):
                    icons_finished = True
                
                if move_finished and icons_finished: break

                self.screen.update()
                sleep(0.01)

            del self.card1
            self.screen.delete(self.leftButton, self.rightButton, numWeeks)
            self.week += 1


if __name__ == "__main__":
    game = anarchy()
    game.run()
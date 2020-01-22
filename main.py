from lib.install_packages import install #from https://github.com/kertox662/PythonPackageInstaller
install()

from PIL import Image

from imageFunctions import pack, resize_image, crop_image
from icons import military, money, nature, people

from tkinter import Tk, Canvas
from time import sleep
from random import choice
import json


def copyFile(copyFrom, copyTo): #copys JSON file
    source = open(copyFrom, 'r') #open file
    read = json.load(source)
    source.close()

    out = open(copyTo, 'w')

    json.dump(read, out) #dump file
    
    out.close()


def create_circle(screen, x, y, radius, **kwargs):
    return screen.create_oval(x-radius, y+radius, x+radius, y-radius, **kwargs)


#Cards that have the given situations and it's details
class card:
    def __init__(self, screen):
        self.body = self.top_area = self.image_file = self.image_file = self.image = self.person = self.text = None
        self.screen = screen #Canvas
        self.decided = False #If user has decided
        self.choice = None #If user decided yes or no
        
        #Gets random situation
        with open('choices-user.json') as fin:
            data = json.load(fin) #Load data
            #Get random person to speak to
            situation = choice(list(data['choices']))
            self.person_key = situation
            situation = data['choices'][situation]
            self.person = situation[0] #Random person
            #Get random situation from that person
            self.situation = choice(situation[1:]) #Random situation

    #Once a situation has been used, it needs to be deleted
    def delete_key(self):
        with open('choices-user.json', 'r') as data_file:
            data = json.load(data_file)

        data["choices"][self.person_key].remove(self.situation) #Remove the situation
        if len(data["choices"][self.person_key]) == 1: #Remove the perosn entirely if they have no more situations left
            del data["choices"][self.person_key]

        with open('choices-user.json', 'w') as data_file: #Dump modified data
            json.dump(data, data_file)

    #Created rectangle w/ rounded corners
    @staticmethod
    def round_rectangle(screen, x1, y1, x2, y2, radius=25, **kwargs):

        points = [x1+radius, y1, x1+radius, y1, x2-radius, y1, x2-radius,
        y1, x2, y1, x2, y1+radius, x2, y1+radius, x2, y2-radius, x2,
        y2-radius, x2, y2, x2-radius, y2, x2-radius, y2, x1+radius, y2,
        x1+radius, y2, x1, y2, x1, y2-radius, x1, y2-radius, x1, y1+radius,
        x1, y1+radius, x1, y1]

        return screen.create_polygon(points, smooth=True, **kwargs)

    #Move the card
    def move(self, direction):
        if direction.lower() in ["r", "right", "e", "east"]: #Move the card
            xSpeed = 25
            ySpeed = 0
        elif direction.lower() in ["l", "left", "w", "west"]:
            xSpeed = -25
            ySpeed = 0
        
        for element in self.elements: #Move every element with the card
            self.screen.move(element, xSpeed, ySpeed)
        
        #Return True when the card if off the screen
        if self.screen.coords(self.body)[-2] > self.screen.winfo_width() or self.screen.coords(self.body)[8] < 0: 
            return True
        else:
            return False

    #Draw the card
    def draw(self):
        screen = self.screen #Canvas
        width, height = screen.winfo_width(), screen.winfo_height() #Width and height of the canvas

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
        self.person_title = screen.create_text(
            dimensions[0]+50, dimensions[1]+275, anchor = "nw", text = self.person['title'], font=("Courier")
        )

        #create text of persons name and title
        self.text = screen.create_text(
            dimensions[0]+50, dimensions[1]+300, width = (dimensions[2]-50)-(dimensions[0]+50), anchor = "nw",
            text = self.situation['description'], font=("Courier")
        )

        self.elements = [self.body, self.top_area, self.image_file, self.image, self.person_title, self.text, self.image_area]

    def __del__(self): #delete card
        self.screen.delete(self.body, self.top_area, self.image_file, self.image, self.person_title, self.text, self.image_area)
        del self


#Class for user interaction
class user:
    def bindKeys(self):
        #Key bindings
        self.screen.tag_bind(self.leftButton, "<Button-1>", self.click_no)
        self.root.bind("<Left>", self.arrow_no)
        self.screen.tag_bind(self.leftButton, "<Enter>", self.enter_no)
        self.screen.tag_bind(self.leftButton, "<Leave>", self.leave)

        self.screen.tag_bind(self.rightButton, "<Button-1>", self.click_yes)
        self.root.bind("<Right>", self.arrow_yes)
        self.screen.tag_bind(self.rightButton, "<Enter>", self.enter_yes)
        self.screen.tag_bind(self.rightButton, "<Leave>", self.leave)
    
    #If user clicks no
    def click_no(self, event):
        self.card1.decided = True
        self.card1.choice = False
        self.screen.delete(self.temp_text)
        self.card1.delete_key()

    #If user clicks yes
    def click_yes(self, event): 
        self.card1.choice = self.card1.decided = True
        self.screen.delete(self.temp_text)
        self.card1.delete_key()

    #If user uses arrow to signal no
    def arrow_no(self, event): 
        self.card1.decided = True
        self.card1.choice = False
        self.card1.delete_key()

    #If user uses arrow to signal yes
    def arrow_yes(self, event):
        self.card1.choice = self.card1.decided = True
        self.card1.delete_key()

    #User hovers mouse over no button
    def enter_no(self, event):
        #Show no message
        cords = self.screen.coords(self.leftButton)
        self.temp_text = self.screen.create_text(cords[0], cords[1]+100, text = self.negative_word, fill = "white", font = ("Courier", 15))
        self.indicators(self.card1.situation['false'])

    #User hovers mouse over yes button
    def enter_yes(self, event):
        #Show yes message
        cords = self.screen.coords(self.rightButton)
        self.temp_text = self.screen.create_text(cords[0], cords[1]+100, text = self.positive_word, fill = "white", font = ("Courier", 15))
        self.indicators(self.card1.situation['true'])
    
    #User takes mouse off a button
    def leave(self, event):
        self.screen.delete(self.temp_text)
        for i in self.indicatorArray:
            self.screen.delete(i)

#Anarchy game
class anarchy(user):
    def __init__(self):
        #Normal Tkinter stuff
        self.root = Tk()
        self.root.attributes('-fullscreen', True)  
        self.fullScreenState = False
        self.root.bind("<f>", self.fullScreenToggle)
        self.root.bind("<Escape>", self.fullScreenOff)
        self.resolution = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        #Fullscreen game, canvas size based on resolution
        self.screen = Canvas(self.root, width=self.resolution[0], height=self.resolution[1], background = "gray9")
        self.screen.pack()
        self.screen.update()

        self.week = 0 #week counter

        copyFile('choices.json', 'choices-user.json') #Copy file over

        #Instantiate of 4 icons
        self.gun, self.dollar, self.leaf, self.person = (
            military(self.screen), money(self.screen), nature(self.screen), people(self.screen)
        )

        #A bunch of words for yes or no
        self.negative = ["No", "No way!", "Not on my watch", "Not happening", "How about no"]
        self.positive = ["Yes", "Of course", "Sure", "Ok", "I'll see to it", "Alright"]

        for _ in range(25):
            #Start user at 50% for each icon
            self.gun.canvas_delete(), self.dollar.canvas_delete(), self.leaf.canvas_delete(), self.person.canvas_delete()
            self.gun += 2
            self.dollar += 2
            self.leaf += 2
            self.person += 2

            self.screen.update()
            sleep(0.03)

    def fullScreenToggle(self, event):
        self.fullScreenState = not self.fullScreenState
        self.root.attributes("-fullscreen", self.fullScreenState)

    def fullScreenOff(self, event):
        self.fullScreenState = False
        self.root.attributes("-fullscreen", self.fullScreenState)

    #Circles underneath effected icons
    def indicators(self, values):
        self.indicatorArray = []

        if values["military"] != 0:
            self.indicatorArray.append(create_circle(self.screen, (2*self.gun.place[0]+self.gun.resize[0])//2, self.gun.place[1]+25, 5, fill = "white", outline = "white"))
        if values["people"] != 0:
            self.indicatorArray.append(create_circle(self.screen, (2*self.person.place[0]+self.person.resize[0])//2, self.person.place[1]+25, 5, fill = "white", outline = "white"))
        if values["nature"] != 0:
            self.indicatorArray.append(create_circle(self.screen, (2*self.leaf.place[0]+self.leaf.resize[0])//2, self.leaf.place[1]+25, 5, fill = "white", outline = "white"))
        if values["economy"] != 0:
            self.indicatorArray.append(create_circle(self.screen, (2*self.dollar.place[0]+self.dollar.resize[0])//2, self.dollar.place[1]+25, 5, fill = "white", outline = "white"))

    #Draw yes or no option arrows
    def draw_arrows(self):
        self.left = resize_image(Image.open("pictures/button-left.png"), 50, 50)
        self.right = resize_image(Image.open("pictures/button-right.png"), 50, 50)
        self.leftPhotoImg = pack(self.left)
        self.rightPhotoImg = pack(self.right)
        card = self.screen.coords(self.card1.body)[-2], self.screen.coords(self.card1.body)[8]
        self.leftButton = self.screen.create_image(card[0]-200, 360, image = self.leftPhotoImg)
        self.rightButton = self.screen.create_image(card[1]+200, 360, image = self.rightPhotoImg)
        self.screen.update()
    
    #Animate icons, takes in dict of values
    def animate_icons(self, comparison):
        change = False #If a change is made
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

    #Check if values are too low, and if user looses the game
    def check_values(self):
        kwargs = {"anchor": "center", "fill": "white", "font": ("Courier", 44)}
        args = int(self.screen['width'])//2, int(self.screen['height'])//2

        #Gives game over message
        def endgame(*args, **kwargs):
            self.screen.create_text(*args, **kwargs)
            self.screen.delete(self.leftButton, self.rightButton)
            self.screen.update()
            sleep(5)
            exit()

        if self.gun.current == 0:
            kwargs['text'] = "Military too weak, you loose"
            endgame(args, kwargs)
        elif self.dollar.current == 0:
            kwargs['text'] = "Greece v2 electric boogaloo"
            endgame(args, kwargs)
        elif self.person.current == 0:
            kwargs['text'] = "Rebelion"
            endgame(args, kwargs)
        elif self.leaf.current == 0:
            kwargs['text'] = "Turtles died"
            endgame(args, kwargs)

    def getTargets(self):
        #Create a dictionary of desired values
        comparison = self.card1.situation['true'] if self.card1.choice else self.card1.situation['false']
        targets = {}
        targets["people"] = comparison["people"] + self.person.current
        targets["military"] = comparison["military"] + self.gun.current
        targets["economy"] = comparison["economy"] + self.dollar.current
        targets["nature"] = comparison["nature"] + self.leaf.current
        for i in targets:
            if targets[i] > 100: targets[i] = 100 #If value exceeds 100%
            elif targets[i] < 0: targets[i] = 0 #If value is below 0%

        direction = "r" if self.card1.choice else "l" #Move card in direction of arrow click
        return targets, direction

    #To run the Game
    def runGame(self):
        while True:
            self.card1 = card(self.screen) #Instantiate new card
            self.card1.draw() #Draw the card
            self.draw_arrows() #Draw yes or no arrows

            self.positive_word = choice(self.positive) #Choose a yes word
            self.negative_word = choice(self.negative) #Choose a no word

            self.bindKeys()

            numWeeks = self.screen.create_text( #Display number of weeks
                1200, 10, anchor = "ne", text = "Week: " + str(self.week), fill = 'white', font=("Courier", 44)
            )

            self.screen.update()
            while not self.card1.decided: #Wait for user to decide
                self.screen.update()
                sleep(0.01)
        
            self.targets, direction = self.getTargets()
            move_finished = icons_finished = False
            
            #Animate the icons filling up and card sliding over
            while True:
                if self.card1.move(direction): #Move the card
                    move_finished = True
                if not self.animate_icons(self.targets): #Increment the icons
                    icons_finished = True
                
                if move_finished and icons_finished: break #Break when both are finished

                self.screen.update()
                sleep(0.01)

            self.check_values() #Check for w/l

            del self.card1 #Delete card
            self.screen.delete(self.leftButton, self.rightButton, numWeeks) #Delete other things
            self.week += 1 #increment week


if __name__ == "__main__":
    game = anarchy()
    game.runGame()
from lib.install_packages import install #from https://github.com/kertox662/PythonPackageInstaller
install()

from PIL import Image

from imageFunctions import pack, resize_image, crop_image
from icons import military, money, nature, people

from tkinter import Tk, Canvas
from time import sleep
from random import choice
import json


def soundInstall():
    #try to import pygame, resort to winsound, if needed, otherwise no engine
    global sound_engine
    sound_engine = None

    try: #first try pygame
        global pygame
        import pygame
        sound_engine = "pygame"
        print("USING PYGAME FOR SOUND")
    except ImportError: #Now try winsound
        print("***ERROR***")
        print("Pygame was not imported successfully.\nFixes:")
        print("1. Pygame was not installed to the system correctly. The problem then lies in the package installer. Possible fix: Try restating the program.")
        print("2. Pygame is not compatible with your version of Python, most likely Python 3.8.x. Fix: Downgrade to Python 3.7.x or lower.")

        from os import name
        Windows = True if name == "nt" else False
        if Windows:
            try:
                global PlaySound, SND_LOOP, SND_ASYNC
                from winsound import PlaySound, SND_LOOP, SND_ASYNC
                sound_engine = "winsound" 
                print("USING WINSOUND FOR SOUND")
            except ImportError:
                print("***ERROR***")
                print("Winsound could not be imported. Reason: unknown")
                print("Neither winsound nor pygame could be imported properly. No sound can be played.")
        else:
            print("***ERROR***")
            print("Winsound could not be installed due to your operating system. Your OS must be Windows.")
            print("Neither winsound nor pygame could be imported properly. No sound can be played.")


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
    def __init__(self, screen, finished = False, person = None, situation = None):
        self.body = self.top_area = self.image_file = self.image_file = self.image = self.person = self.text = None
        self.screen = screen #Canvas
        self.decided = False #If user has decided
        self.choice = None #If user decided yes or no
        
        if not finished:
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
        else:
            self.person = person
            self.situation = {
                "description": situation,
                "true": {"people": 0, "military": 0, "economy": 0, "nature": 0},
                "false": {"people": 0, "military": 0, "economy": 0, "nature": 0}
            }

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


class menu:
    def menuStart(self, screen):
        self.screen = screen
        width, height = screen.winfo_width(), screen.winfo_height()
        screen.delete("all") #Clear screen
        self.background = resize_image(Image.open("pictures/background.png"), width, width) #Background image
        self.background = pack(self.background)
        self.background_image = screen.create_image(
            width//2, height//2, anchor = "center", image = self.background
        )
        self.startMusic() #Start music
        self.menuScreen(self.screen)

    def menuScreen(self, screen):
        self.screen = screen
        
        width, height = screen.winfo_width(), screen.winfo_height()

        for i in range(9, 50, 2): #Fade in title
            title = screen.create_text(width//2, 100, anchor = "n", font = ("Courier", 100), fill = "grey" + str(i), text = "Anarchy")
        
            menuButtons = self.menuButtons = {} #Buttons
            
            self.buttonNames = ["quit", "help", "load", "easy", "hard"]

            for j in range(2):
                self.menuButtons[self.buttonNames[j] + "Button"] = screen.create_rectangle(
                    25, height-25-(j*175), 275, height-175-(j*175), fill = "grey" + str(i), outline = "gray" + str(i)
                ) 
                self.menuButtons[self.buttonNames[j] + "Text"] = screen.create_text(
                    150, (2*height-200-2*(j*175))//2, anchor = "center", text = self.buttonNames[j].title(), font = ("Courier", 50), fill = "black"
                )
            
            for j in range(3):
                self.menuButtons[self.buttonNames[j+2] + "Button"] = screen.create_rectangle(
                    width-275, height-25-(j*175), width-25, height-175-(j*175), fill = "grey" + str(i), outline = "gray" + str(i)
                ) 
                self.menuButtons[self.buttonNames[j+2] + "Text"] = screen.create_text(
                    width-150, (2*height-200-2*(j*175))//2, anchor = "center", text = self.buttonNames[j+2].title(), font = ("Courier", 50), fill = "black"
                )
            
            screen.update()
            sleep(0.1)
            screen.delete(title)

            for i in menuButtons: screen.delete(menuButtons[i])

        self.title = screen.create_text(width//2, 100, anchor = "n", font = ("Courier", 100), fill = "grey" + str(50), text = "Anarchy")
        self.buttonNames = ["quit", "help", "load", "easy", "hard"]

        for i in range(2):
            self.menuButtons[self.buttonNames[i] + "Button"] = screen.create_rectangle(
                25, height-25-(i*175), 275, height-175-(i*175), fill = "grey50", outline = "gray50"
            ) 
            self.menuButtons[self.buttonNames[i] + "Text"] = screen.create_text(
                150, (2*height-200-2*(i*175))//2, anchor = "center", text = self.buttonNames[i].title(), font = ("Courier", 50), fill = "black"
            )
        
        for i in range(3):
            self.menuButtons[self.buttonNames[i+2] + "Button"] = screen.create_rectangle(
                width-275, height-25-(i*175), width-25, height-175-(i*175), fill = "grey50", outline = "gray50"
            ) 
            self.menuButtons[self.buttonNames[i+2] + "Text"] = screen.create_text(
                width-150, (2*height-200-2*(i*175))//2, anchor = "center", text = self.buttonNames[i+2].title(), font = ("Courier", 50), fill = "black"
            )

        #Lots of bindings
        screen.tag_bind(menuButtons["quitButton"], "<Button-1>", self.quit_program)
        screen.tag_bind(menuButtons["quitText"], "<Button-1>", self.quit_program)
        screen.tag_bind(menuButtons["helpButton"], "<Button-1>", self.displayHelp)
        screen.tag_bind(menuButtons["helpText"], "<Button-1>", self.displayHelp)
        screen.tag_bind(menuButtons["loadButton"], "<Button-1>", self.loadData)
        screen.tag_bind(menuButtons["loadText"], "<Button-1>", self.loadData)
        screen.tag_bind(menuButtons["hardButton"], "<Button-1>", lambda event: self.runDifficulty("h"))
        screen.tag_bind(menuButtons["hardText"], "<Button-1>", lambda event: self.runDifficulty("h"))
        screen.tag_bind(menuButtons["easyButton"], "<Button-1>", lambda event: self.runDifficulty("e"))
        screen.tag_bind(menuButtons["easyText"], "<Button-1>", lambda event: self.runDifficulty("e"))

        screen.mainloop()
    
    def displayHelp(self, event): #Displays help
        self.screen.delete(self.title) #Clear canvas
        for i in self.menuButtons:
            self.screen.delete(self.menuButtons[i])
        '''
        self.background_image = self.screen.create_image( #Backgound image
            self.screen.winfo_width()//2, self.screen.winfo_height()//2, anchor = "center", image = self.background
        )
        '''
        with open("instructions.txt", "r") as instruction_file: #Display instructions
            self.instruction_text = self.screen.create_text(
                10, 10, anchor = "nw", width = self.screen.winfo_width()-20, fill = "white", font = ("Courier", 30), text = instruction_file.readline()
            )

        self.backButton = self.screen.create_rectangle( #Button to return
            10, self.screen.winfo_height()-10, 260, self.screen.winfo_height()-110, fill = "grey50", outline = "grey50"
        )
        self.backText = self.screen.create_text(
            135, self.screen.winfo_height()-60, anchor = "center", text = "Back", font = ("Courier", 50), fill = "black"
        )
        self.screen.tag_bind(self.backButton, "<Button-1>", self.toMenu)
        self.screen.tag_bind(self.backText, "<Button-1>", self.toMenu)
        self.screen.update()
        self.screen.mainloop()

    def toMenu(self, event): #Return to menu
        self.screen.delete(self.instruction_text, self.backButton, self.backText)
        self.menuScreen(self.screen)

    def loadData(self, event): #Work in progress, load previously saved data
        print("WIP")
    
    def runDifficulty(self, difficulty):
        #self.screen.delete("all")
        self.screen.delete(self.title) #Clear canvas
        for i in self.menuButtons:
            self.screen.delete(self.menuButtons[i])
        self.background_image = self.screen.create_image(
            self.screen.winfo_width()//2, self.screen.winfo_height()//2, anchor = "center", image = self.background
        )
        self.runGame("difficulty")

    def startMusic(self): #Stat music
        if sound_engine == "pygame": #If using pygame
            pygame.mixer.init()
            pygame.mixer.music.load("other/adrenaline.wav")
            pygame.mixer.music.set_volume(0.25)
            pygame.mixer.music.play(-1)

        elif sound_engine == "winsound": #If using winsound
            PlaySound('other/adrenaline.wav', SND_LOOP + SND_ASYNC)
        
        else: #Tell user no music is being played
            self.screen.create_text(
                self.screen.winfo_width()//2, self.screen.winfo_height()-10, anchor = "s", text = "ERROR: Sound can't play. Check console for more details.", fill = "red", font = ("Courier", 10)
            )

#Class for user interaction
class user:
    def bindKeys(self):
        #Key bindings
        self.screen.tag_bind(self.leftButton, "<Button-1>", lambda event: self.choose_option(False))
        self.root.bind("<Left>", lambda event: self.click_option(False, arrow = False))
        self.screen.tag_bind(self.leftButton, "<Enter>", lambda event: self.enter_option(False))
        self.screen.tag_bind(self.leftButtonArrow, "<Enter>", lambda event: self.enter_option(False))
        self.screen.tag_bind(self.leftButton, "<Leave>", self.leave)
        self.screen.tag_bind(self.leftButtonArrow, "<Leave>", self.leave)

        self.screen.tag_bind(self.rightButton, "<Button-1>", lambda event: self.choose_option(True))
        self.root.bind("<Right>", lambda event: self.click_option(True, arrow = True))
        self.screen.tag_bind(self.rightButton, "<Enter>", lambda event: self.enter_option(True))
        self.screen.tag_bind(self.rightButtonArrow, "<Enter>", lambda event: self.enter_option(True))
        self.screen.tag_bind(self.rightButton, "<Leave>", self.leave)
        self.screen.tag_bind(self.rightButtonArrow, "<Leave>", self.leave)
    
    def choose_option(self, option, arrow = False):
        self.card1.decided = True
        self.card1.choice = option
        if not arrow: self.screen.delete(self.temp_text)
        self.card1.delete_key()
    
    def enter_option(self, option):
        cords = self.screen.coords(self.leftButton) if not option else self.screen.coords(self.rightButton)
        word = self.negative_word if not option else self.positive_word
        option = 'true' if option else 'false'
        self.temp_text = self.screen.create_text((cords[0]+cords[2])//2, cords[1]+100, text = word, fill = "white", font = ("Courier", 15))
        self.indicators(self.card1.situation[option])
    
    #User takes mouse off a button
    def leave(self, event):
        self.screen.delete(self.temp_text)
        for i in self.indicatorArray:
            self.screen.delete(i)

#Anarchy game
class anarchy(user, menu):
    def __init__(self):
        #Normal Tkinter stuff
        soundInstall()
        self.root = Tk()
        self.root.attributes('-fullscreen', True) #Fullscreen
        self.fullScreenState = False
        self.root.bind("<f>", self.fullScreenToggle)
        self.root.bind("<Escape>", self.quit_program)
        self.root.bind("q", self.qPress)
        self.resolution = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        #Fullscreen game, canvas size based on resolution
        self.screen = Canvas(
            self.root, width=self.resolution[0], height=self.resolution[1], background = "gray9", highlightthickness = 0
        )

        self.screen.pack()
        self.screen.update()
        self.qPressed = self.escPressed = False
        self.menuStart(self.screen)

    def qPress(self, event):
        self.qPressed = True

    def set_up(self):
        self.month = 0 #week counter

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

    #Toggles full screen
    def fullScreenToggle(self, event):
        self.fullScreenState = not self.fullScreenState
        self.root.attributes("-fullscreen", self.fullScreenState)

    #Complete termination of the program
    def quit_program(self, event):
        self.escPressed = True
        try: self.root.quit()
        except: pass
        exit()
        self.root.destroy()
        
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
        card = self.screen.coords(self.card1.body)[-2], self.screen.coords(self.card1.body)[8]
        self.leftButton = create_circle(self.screen, card[0]-200, 360, 25, fill = "black", outline = "black")
        self.rightButton = create_circle(self.screen, card[1]+200, 360, 25, fill = "black", outline = "black")
        x = card[0]
        arrowPoints = [
            x-212.5, 360,
            x-202.5, 350,
            x-202.5, 355,
            x-187.5, 355,
            x-187.5, 365,
            x-202.5, 365,
            x-202.5, 370,
            x-212.5, 360
        ]
        self.leftButtonArrow = self.screen.create_polygon(*arrowPoints, fill = "white", outline = "white")
        
        x = card[1]
        arrowPoints = [
            x+212.5, 360,
            x+202.5, 350,
            x+202.5, 355,
            x+187.5, 355,
            x+187.5, 365,
            x+202.5, 365,
            x+202.5, 370,
            x+212.5, 360
        ]
        self.rightButtonArrow = self.screen.create_polygon(*arrowPoints, fill = "white", outline = "white")
        '''
        self.left = resize_image(Image.open("pictures/button-left.png"), 50, 50)
        self.right = resize_image(Image.open("pictures/button-right.png"), 50, 50)
        self.leftPhotoImg = pack(self.left)
        self.rightPhotoImg = pack(self.right)
        card = self.screen.coords(self.card1.body)[-2], self.screen.coords(self.card1.body)[8]
        self.leftButton = self.screen.create_image(card[0]-200, 360, image = self.leftPhotoImg)
        self.rightButton = self.screen.create_image(card[1]+200, 360, image = self.rightPhotoImg)
        '''
        
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
        kwargs = {"anchor": "center", "fill": "white", "font": ("Courier", 44), "width": self.screen.winfo_width()-20}
        args = int(self.screen['width'])//2, int(self.screen['height'])//2

        #Gives game over message
        def endgame(*args, **kwargs):
            self.screen.create_text(*args, **kwargs)
            self.screen.delete(self.leftButton, self.rightButton, self.leftButtonArrow, self.rightButtonArrow)
            self.screen.update()
            sleep(3)
            self.screen.delete("all")
            self.menuScreen(self.screen)

        if self.gun.current == 0:
            kwargs['text'] = "You've been invaded! Your week military didn't last a chance! Your country collapses into anarchy."
            endgame(args, kwargs)
        elif self.dollar.current == 0:
            kwargs['text'] = "The country is out of money. You're in crippling debt, bankrupt, and can't pay for anythinga. Your country has collapsed into anarchy."
            endgame(args, kwargs)
        elif self.person.current == 0:
            kwargs['text'] = "Displeasure amongst the people has some people very mad. You seem to have been poisoned by a mysterious substance. Soon, you will be dead, and your country collapses into anarchy. "
            endgame(args, kwargs)
        elif self.leaf.current == 0:
            kwargs['text'] = "When nature falls, everyone goes with it. Food becomes ever more scarce, and your country collapses into anarchy."
            endgame(args, kwargs)

    def get_targets(self):
        #Create a dictionary of desired values
        comparison = self.card1.situation['true'] if self.card1.choice else self.card1.situation['false']
        if self.difficulty == "h":
            for i in comparison:
                if comparison[i] < 0:
                    comparison[i] -= 3
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
    def runGame(self, difficulty):
        self.set_up()
        self.difficulty = difficulty
        while self.month <= 1 and not self.qPressed: #52 weeks in a year
            self.card1 = card(self.screen) #Instantiate new card
            self.card1.draw() #Draw the card
            self.draw_arrows() #Draw yes or no arrows

            self.positive_word = choice(self.positive) #Choose a yes word
            self.negative_word = choice(self.negative) #Choose a no word

            self.bindKeys()

            numMonths = self.screen.create_text( #Display number of weeks
                1200, 10, anchor = "ne", text = "Month: " + str(self.month), fill = 'white', font=("Courier", 44)
            )

            self.screen.update()
            while not self.card1.decided: #Wait for user to decide
                if self.qPressed or self.escPressed: break
                self.screen.update()
                sleep(0.01)
            if self.qPressed or self.escPressed: break
        
            self.targets, direction = self.get_targets()
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
            self.screen.delete(self.leftButton, self.rightButton, numMonths) #Delete other things
            self.month += 1 #increment month

        if self.qPressed:
            self.qPressed = False
            del self.gun
            del self.leaf
            del self.person
            del self.dollar

            try: del self.card1 #Delete card
            except AttributeError: pass
            
            self.screen.delete(self.leftButton, self.rightButton, numMonths, self.leftButtonArrow, self.rightButtonArrow) #Delete other things

            try: self.leave("")
            except AttributeError: pass

            self.menuScreen(self.screen)
        else:
            vp = {"title": "Vice President Russel", "image": ["pictures/vp.png", 200, 150]}
            sit = "Congratulations on a successful term, president. You'll be glad to hear that the country is in good shape, and everything is still intact."
            self.card1 = card(self.screen, finished = True, person = vp, situation = sit) #Instantiate new card
            self.card1.draw() #Draw the card
        

if __name__ == "__main__":
    anarchy()
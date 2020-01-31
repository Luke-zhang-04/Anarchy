#installing packages from pip
from lib.install_packages import install #from https://github.com/kertox662/PythonPackageInstaller
install()

#third party packages
from PIL import Image

#cutsom packages
from imageFunctions import pack, resize_image, crop_image
from icons import military, money, nature, people
from card import card

#Built in packages
from tkinter import Tk, Canvas
from time import sleep
from random import choice
import json


def soundInstall():
    #try to import pygame, resort to winsound, if needed, otherwise no engine
    global sound_engine
    sound_engine = None

    try: #first try pygame
        print("\nTrying to import Pygame")
        global pygame
        import pygame
        sound_engine = "pygame"
    except ImportError: #Now try winsound
        from os import name
        Windows = True if name == "nt" else False
        print("***ERROR***")
        print("Pygame was not imported successfully.\nFixes:")
        print("1. Pygame is not compatible with your version of Python. Fix: Downgrade/upgrade to Python 3.7.x.")
        print("2. Pygame was not installed correctly through pip. Fixes:")
        print("\ta. Restart the program")
        if Windows:
            print("\tb. In powershell or command prompt, type \"py3 -m pip install -U pygame --user\"")
        else:
            print("\tb. In bash, type \"python3 -m pip install pygame\"")
        
        if Windows:
            try:
                print('\nTrying to import winsound')
                global PlaySound, SND_LOOP, SND_ASYNC
                from winsound import PlaySound, SND_LOOP, SND_ASYNC
                sound_engine = "winsound" 
                print("USING WINSOUND FOR SOUND")
            except ImportError:
                print("\n***ERROR***")
                print("Winsound was not imported successfully. Reason: unknown")
                print("Neither winsound nor pygame could be imported properly. No sound can be played.")
            else:
                print("Success: winsound imported\nUsing winsound for sound")
        else:
            print("***ERROR***")
            print("Winsound was not imported successfully.\nFixes:")
            print("Probably nothing. Winsound only works on Windows.")
            print("Neither winsound nor pygame could be imported properly. No sound can be played.")
    else:
        print("Success: pygame imported\nUsing Pygame for sound")


def copyFile(copyFrom, copyTo): #copys JSON file
    source = open(copyFrom, 'r') #open file
    read = json.load(source)
    source.close()

    out = open(copyTo, 'w')

    json.dump(read, out) #dump file
    
    out.close()


def create_circle(screen, x, y, radius, **kwargs):
    return screen.create_oval(x-radius, y+radius, x+radius, y-radius, **kwargs)


class menu:
    def menuStart(self, screen):
        def percentage_display(screen, percentRange, old = None, time = None):
            if old != None: percentage = old 
            for i in percentRange:
                screen.delete(percentage)
                percentage = screen.create_text(width//2, (height//2)+100, text = str(i) + "%", **textKwargs)
                screen.update()
                sleep(0.0001 if time == None else time/(max(percentRange)-min(percentRange)))
            return percentage

        self.screen = screen
        width, height = screen.winfo_width(), screen.winfo_height()
        textKwargs = {"anchor": "center", "font": ("Courier", 44), "fill": "white"}

        text = screen.create_text(width//2, height//2, text = "Loading . . .", **textKwargs)
        percentage = screen.create_text(width//2, (height//2)+100, text = "0%", **textKwargs)
        screen.update()

        self.background = resize_image(Image.open("pictures/background.png"), width, width) #Background image
        self.background = pack(self.background)
        percentage = percentage_display(screen, range(76), old = percentage)


        self.background2 = resize_image(Image.open("pictures/skyline.png"), width, height//2)
        self.background2 = pack(self.background2)
        percentage = percentage_display(screen, range(76, 101), old = percentage)


        self.background_image = screen.create_image(
            width//2, height//2, anchor = "center", image = self.background
        )
        self.background_image2 = screen.create_image(
            width//2, height, anchor = "s", image = self.background2
        )
        screen.delete(text, percentage)
        screen.update()

        self.startMusic() #Start music
        self.menuScreen(self.screen)

    def menuScreen(self, screen):
        self.screen = screen
        
        width, height = screen.winfo_width(), screen.winfo_height()
        time = 0.1

        for i in range(9, 50, 2): #Fade in title
            title = screen.create_text(width//2, 100, anchor = "n", font = ("Courier", 100), fill = "grey" + str(i), text = "Anarchy")
        
            menuButtons = self.menuButtons = {} #Buttons
            
            self.buttonNames = ["quit", "help", "load", "easy", "medium", "hard", "insane"]

            for j in range(2):
                self.menuButtons[self.buttonNames[j] + "Button"] = screen.create_rectangle(
                    25, height-25-(j*175), 275, height-175-(j*175), fill = "grey" + str(i), outline = "gray" + str(i)
                ) 
                self.menuButtons[self.buttonNames[j] + "Text"] = screen.create_text(
                    150, (2*height-200-2*(j*175))//2, anchor = "center", text = self.buttonNames[j].title(), font = ("Courier", 50), fill = "black"
                )
            
            for j in range(5):
                self.menuButtons[self.buttonNames[j+2] + "Button"] = screen.create_rectangle(
                    width-275, height-25-(j*175), width-25, height-175-(j*175), fill = "grey" + str(i), outline = "gray" + str(i)
                ) 
                self.menuButtons[self.buttonNames[j+2] + "Text"] = screen.create_text(
                    width-150, (2*height-200-2*(j*175))//2, anchor = "center", text = self.buttonNames[j+2].title(), font = ("Courier", 50), fill = "black"
                )
            
            screen.update()
            sleep(time)
            screen.delete(title)

            for i in menuButtons: screen.delete(menuButtons[i])
            time /= 1.5

        self.title = screen.create_text(width//2, 100, anchor = "n", font = ("Courier", 100), fill = "grey" + str(50), text = "Anarchy")
        self.buttonNames = ["quit", "help", "load", "easy", "medium", "hard", "insane"]

        for i in range(2):
            self.menuButtons[self.buttonNames[i] + "Button"] = screen.create_rectangle(
                25, height-25-(i*175), 275, height-175-(i*175), fill = "grey50", outline = "gray50"
            ) 
            self.menuButtons[self.buttonNames[i] + "Text"] = screen.create_text(
                150, (2*height-200-2*(i*175))//2, anchor = "center", text = self.buttonNames[i].title(), font = ("Courier", 50), fill = "black"
            )
        
        for i in range(5):
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
        screen.tag_bind(menuButtons["insaneButton"], "<Button-1>", lambda event: self.runDifficulty("i"))
        screen.tag_bind(menuButtons["insaneText"], "<Button-1>", lambda event: self.runDifficulty("i"))
        screen.tag_bind(menuButtons["hardButton"], "<Button-1>", lambda event: self.runDifficulty("h"))
        screen.tag_bind(menuButtons["hardText"], "<Button-1>", lambda event: self.runDifficulty("h"))
        screen.tag_bind(menuButtons["mediumButton"], "<Button-1>", lambda event: self.runDifficulty("m"))
        screen.tag_bind(menuButtons["mediumText"], "<Button-1>", lambda event: self.runDifficulty("m"))
        screen.tag_bind(menuButtons["easyButton"], "<Button-1>", lambda event: self.runDifficulty("e"))
        screen.tag_bind(menuButtons["easyText"], "<Button-1>", lambda event: self.runDifficulty("e"))

        screen.mainloop()
    
    def displayHelp(self, event): #Displays help
        self.screen.delete(self.title) #Clear canvas
        for i in self.menuButtons:
            self.screen.delete(self.menuButtons[i])
            
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
        '''
        self.background_image = self.screen.create_image(
            self.screen.winfo_width()//2, self.screen.winfo_height()//2, anchor = "center", image = self.background
        )
        '''
        self.runGame(difficulty)

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
        self.screen.tag_bind(self.leftButtonArrow, "<Button-1>", lambda event: self.choose_option(False))
        self.root.bind("<Left>", lambda event: self.choose_option(False))
        self.screen.tag_bind(self.leftButton, "<Enter>", lambda event: self.enter_option(False))
        self.screen.tag_bind(self.leftButtonArrow, "<Enter>", lambda event: self.enter_option(False))
        self.screen.tag_bind(self.leftButton, "<Leave>", self.leave)
        self.screen.tag_bind(self.leftButtonArrow, "<Leave>", self.leave)

        self.screen.tag_bind(self.rightButton, "<Button-1>", lambda event: self.choose_option(True))
        self.screen.tag_bind(self.rightButtonArrow, "<Button-1>", lambda event: self.choose_option(True))
        self.root.bind("<Right>", lambda event: self.choose_option(True))
        self.screen.tag_bind(self.rightButton, "<Enter>", lambda event: self.enter_option(True))
        self.screen.tag_bind(self.rightButtonArrow, "<Enter>", lambda event: self.enter_option(True))
        self.screen.tag_bind(self.rightButton, "<Leave>", self.leave)
        self.screen.tag_bind(self.rightButtonArrow, "<Leave>", self.leave)
    
    def choose_option(self, option):
        try:
            self.card1.decided = True
            self.card1.choice = option
            self.leave("")
            self.card1.delete_key()
        except ValueError:
            pass
    
    def enter_option(self, option):
        if not self.card1.decided:
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
    
    @staticmethod
    def reset_colors(*args):
        for i in args:
            i.set_color()

    def set_up(self):
        self.month = 0 #week counter

        copyFile('choices.json', 'choices-user.json') #Copy file over

        #Instantiate of 4 icons
        self.icons = self.gun, self.dollar, self.leaf, self.person = (
            military(self.screen), money(self.screen), nature(self.screen), people(self.screen)
        )

        #A bunch of words for yes or no
        self.negative = ["No", "No way!", "Not on my watch", "Not happening", "How about no"]
        self.positive = ["Yes", "Of course", "Sure", "Ok", "I'll see to it", "Alright"]

        for _ in range(24):
            #Start user at 50% for each icon
            for i in self.icons:
                i.delete()
                i += 2

            self.screen.update()
            sleep(0.03)

        self.reset_colors(*self.icons)

        self.screen.update()

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

    #Gives game over message
    def endgame(self, *args, **kwargs):
        looseText = self.screen.create_text(*args, **kwargs)
        self.screen.delete(self.leftButton, self.rightButton, self.leftButtonArrow, self.rightButtonArrow, self.numMonths)
        self.screen.update()

        sleep(5)

        self.screen.delete(looseText)
        for i in self.icons:
            i.delete("all")

        try: del self.card1 #Delete card
        except AttributeError: pass
        
        try: self.leave("")
        except AttributeError: pass

        self.menuScreen(self.screen)

    #Check if values are too low, and if user looses the game
    def check_values(self):
        kwargs = {"anchor": "center", "fill": "white", "font": ("Courier", 44), "width": self.screen.winfo_width()-20}
        args = int(self.screen['width'])//2, int(self.screen['height'])//2

        if self.gun.current == 0:
            kwargs['text'] = "You've been invaded! Your week military didn't last a chance! Your country collapses into anarchy."
            self.endgame(*args, **kwargs)
        elif self.dollar.current == 0:
            kwargs['text'] = "The country is out of money. You're in crippling debt, bankrupt, and can't pay for anything. Your country has collapsed into anarchy."
            self.endgame(*args, **kwargs)
        elif self.person.current == 0:
            kwargs['text'] = "Displeasure amongst the people has some people very mad. You seem to have been poisoned by a mysterious substance. Soon, you will be dead, and your country collapses into anarchy. "
            self.endgame(*args, **kwargs)
        elif self.leaf.current == 0:
            kwargs['text'] = "When nature falls, everyone goes with it. Food becomes ever more scarce, and your country collapses into anarchy."
            self.endgame(*args, **kwargs)

    def get_targets(self):
        #Create a dictionary of desired values
        comparison = self.card1.situation['true'] if self.card1.choice else self.card1.situation['false']
        if self.difficulty == "i":
            amt = 7
        elif self.difficulty == "h":
            amt = 5
        elif self.difficulty == "m":
            amt = 3
        else:
            amt = 0

        for i in comparison:
            if comparison[i] < 0:
                comparison[i] -= amt
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
        self.card1 = card(self.screen) #Instantiate new card
        self.card1.draw() #Draw the card
        while self.month <= 104 and not self.qPressed and not self.escPressed: #Presidents can only serve two terms
            while self.month <= 52 and not self.qPressed and not self.escPressed: #52 weeks in a year
                card2 = card(self.screen)
                card2.draw()
                self.card1.tag_raise()
                self.draw_arrows() #Draw yes or no arrows

                self.positive_word = choice(self.positive) #Choose a yes word
                self.negative_word = choice(self.negative) #Choose a no word

                self.bindKeys()

                self.numMonths = self.screen.create_text( #Display number of weeks
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

                self.reset_colors(*self.icons)
                self.check_values() #Check for w/l

                del self.card1 #Delete card
                self.card1 = card2
                self.screen.delete(self.leftButton, self.rightButton, self.numMonths, self.leftButtonArrow, self.rightButtonArrow) #Delete other things
                self.month += 1 #increment month

        if self.qPressed:
            self.qPressed = False

            for i in self.icons:
                i.delete("all")

            try: del self.card1 #Delete card
            except AttributeError: pass
            
            self.screen.delete(self.leftButton, self.rightButton, self.numMonths, self.leftButtonArrow, self.rightButtonArrow) #Delete other things

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
from imageFunctions import pack, resize_image, crop_image

from PIL import Image

from random import choice
import json

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

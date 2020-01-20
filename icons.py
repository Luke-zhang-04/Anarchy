from imageFunctions import *

#Icon class for adding and subtracting values
class icon:
    def __add__(self, other):
        cropped_image_file = resize_image(Image.open("pictures/icons/" + self.filled_file_name), self.resize[0], self.resize[1])
        width, height = cropped_image_file.size

        increment = height/100
        if self.current + other > 100:
            self.current = 100
        elif self.current + other < 0:
            self.current = 0
        else:
            self.current += other

        self.amt = height-self.current*increment

        cropped_image_file = crop_image(cropped_image_file, 0, self.resize[0], self.amt, self.resize[1])
        self.cropped_image_file = pack(cropped_image_file)
        self.screen.delete(self.cropped_image)

        self.cropped_image = self.screen.create_image(
            self.place[0], self.place[1], anchor = 'sw', image = self.cropped_image_file
        )

        return self
    
    def __sub__(self, other):
        self += other * -1
        return self

    def canvas_delete(self): #we don't want to use __del__ because we only want to screen.delete()
        self.screen.delete(self.cropped_image)

#ALL 4 CLASSES BELOW INHERIT FROM ICON CLASS
#military meter, 
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


#money meter
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


#nature meter
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


#people meter
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
from anarchy.imageFunctions import pack, resize_image, crop_image
from PIL import Image

#Icon class for adding and subtracting values
class icon:
    #Adding values to the icons to increase of decrease their fill
    def __add__(self, other):
        #open resized image
        if other > 0:
            cropped_image_file = resize_image(
                Image.open("anarchy/pictures/icons/" + self.filled_file_name[:-9]+"green.png"), self.resize[0], self.resize[1]
            )
        elif other < 0:
            cropped_image_file = resize_image(
                Image.open("anarchy/pictures/icons/" + self.filled_file_name[:-9]+"red.png"), self.resize[0], self.resize[1]
            )
        else:
            cropped_image_file = resize_image(
                Image.open("anarchy/pictures/icons/" + self.filled_file_name), self.resize[0], self.resize[1]
            )
        _, height = cropped_image_file.size #get height of image

        increment = height/100 #incement for the height
        if self.current + other > 100: #Value cannot exceed 100%
            self.current = 100
        elif self.current + other < 0: #Value cannot be lower than 0%
            self.current = 0
        else: #Increase current by other
            self.current += other

        self.amt = height-self.current*increment #Find the appropriate amount to crop the image

        cropped_image_file = crop_image(cropped_image_file, 0, self.resize[0], self.amt, self.resize[1]) #crop the image
        self.cropped_image_file = pack(cropped_image_file) #pack into photoimage
        self.screen.delete(self.cropped_image) #delete old image

        self.cropped_image = self.screen.create_image( #create new image
            self.place[0], self.place[1], anchor = 'sw', image = self.cropped_image_file
        )
        self.screen.tag_raise(self.image)

        return self
    
    #Subtracting values to the icons to increase or decrease their fill
    def __sub__(self, other):
        #call __add__ but multiply the number by -1
        self += other * -1
        return self

    #Changing the colour to white
    def set_color(self):
        if self.current > 25:
            self += 0
        else:
            self += 1
            self -= 1

    def delete(self, *args):
        if len(args) == 0: self.screen.delete(self.cropped_image)
        elif args[0] == "all": self.screen.delete(self.cropped_image, self.image)


#military meter, 
class military(icon):
    def __init__(self, screen):
        self.screen = screen #Canvas
        self.filled_file_name = "gun-white.png" #Name of filled image file
        image_file = resize_image(Image.open("anarchy/pictures/icons/gun-trans.png"), 40, 50) #resize image
        self.image_file = pack(image_file) #Pack into photoimage
        self.image = screen.create_image(10, 60, anchor = 'sw', image = self.image_file) #Create image

        self.current = 0 #Current value
        self.cropped_image = None #To remove exceptions, later becomes canvas object
        self.resize = 40, 50 #Resize dimensions
        self.place = 10, 60 #Coordinates


#money meter
class money(icon):
    def __init__(self, screen):
        self.screen = screen #Canvas
        self.filled_file_name = "money-white.png" #Name of filled image file
        image_file = resize_image(Image.open("anarchy/pictures/icons/money-trans.png"), 40, 50) #resize image
        self.image_file = pack(image_file) #Pack into photoimage
        self.image = screen.create_image(50, 60, anchor = 'sw', image = self.image_file) #Create image

        self.current = 0 #Current value
        self.cropped_image = None #To remove exceptions, later becomes canvas object
        self.resize = 40, 50 #Resize dimensions
        self.place = 50, 60 #Coordinates


#nature meter
class nature(icon):
    def __init__(self, screen):
        self.screen = screen
        self.filled_file_name = "plant-white.png" #Name of filled image file
        self.image_file = resize_image(Image.open("anarchy/pictures/icons/plant-trans.png"), 40 , 50) #resize image
        self.image_file = pack(self.image_file) #Pack into photoimage
        self.image = screen.create_image(90, 60, anchor = 'sw', image = self.image_file) #Create image

        self.current = 0 #Current value
        self.cropped_image = None #To remove exceptions, later becomes canvas object
        self.resize = 40, 50 #Resize dimensions
        self.place = 90, 60 #Coordinates


#people meter
class people(icon):
    def __init__(self, screen):
        self.screen = screen
        self.filled_file_name = "people-white.png" #Name of filled image file
        self.image_file = resize_image(Image.open("anarchy/pictures/icons/people-trans.png"), 70 , 50) #resize image
        self.image_file = pack(self.image_file) #Pack into photoimage
        self.image = screen.create_image(120, 60, anchor = 'sw', image = self.image_file) #Create image
        
        self.current = 0 #Current value
        self.cropped_image = None #To remove exceptions, later becomes canvas object
        self.resize = 70, 50 #Resize dimensions
        self.place = 120, 60 #Coordinates
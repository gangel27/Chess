import pygame 

WHITE = (255,255,255)

class Option_Field: 
    def __init__(self, options,icons,title, x,y,width,height):
        self.options = options
        self.icons = icons
        self.x = x
        self.y = y 
        self.icon_width = width
        self.icon_height = height
        self.title_text = title
        self.arrow_width = 50
        self.arrow_height = 50

        self.left_arrow =  pygame.transform.scale(pygame.image.load(f"./Images/Other/left_arrow.png"), (self.arrow_width, self.arrow_height))
        self.right_arrow =  pygame.transform.rotate(self.left_arrow, 180)
        self.option_icons = []

        for option in self.options: 
            icon = pygame.transform.scale(pygame.image.load(f"./Images/Icons/{option}.png"), (self.icon_width, self.icon_height))
            self.option_icons.append(icon)

        

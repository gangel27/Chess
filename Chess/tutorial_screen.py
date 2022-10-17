import pygame


BLACK = (0,0,0)

class Tutorial_Screen: 
    def __init__(self, screen,x,y, no_screens): 
        self.screen = screen 
        self.number_of_pages = 4
        self.current_text_index = 0 
        self.max_characters_per_line = 50

        self.x = x 
        self.y = y 

        self.font_colour = BLACK
        self.font_size = 20
        self.font_style = 'freesansbold.ttf'
        self.font = pygame.font.Font(self.font_style, self.font_size)
        self.line_gap =  35

        self.read_texts()

        self.update_text_img()

    def read_texts(self): 
        self.texts = []
        for i in range(self.number_of_pages): 
            with open(f"Tutorial_text/tutorial_{i+1}.txt", "r") as file: 
                self.texts.append(file.read()) 
            
       
    def update_text_img(self): 
        # need to change this so that it doens't break off mid word 
        self.text_imgs = []
        line = ''
        for character in self.texts[self.current_text_index]: 
            line += character
            if len(line) >= self.max_characters_per_line: 
                self.text_imgs.append(self.font.render(line, True, self.font_colour))
                line = ""
       
        self.font.render(line, True, self.font_colour)
    
    def draw(self): 
        y = self.y 
        for text_img in self.text_imgs:
            y += self.line_gap
            self.screen.blit(text_img, (self.x,y))
    
    def increase_current_text_index(self): 
        self.current_text_index += 1 
        if self.current_text_index >= self.number_of_pages:
            self.current_text_index = self.number_of_pages - 1
        self.update_text_img()


    def decrease_current_text_index(self): 
        self.current_text_index -= 1  
        if self.current_text_index < 0: 
            self.current_text_index = 0 
        self.update_text_img()

    
from tkinter import E
import pygame

pygame.font.init()
GREEN = (0,200,0)

class Button: 
    def __init__(self,x, y, text, identifier): 
        self.text = text
        self.x = x 
        self.y = y 
        self.identifier = identifier
        self.font_colour = "black"
        self.underline = "true"
        self.font_size = 30 
        self.font_style = 'freesansbold.ttf'
        self.font = pygame.font.Font(self.font_style, self.font_size)
        pygame.font.Font.set_underline(self.font, True)
        self.is_hovering = False
        self.hover_colour = GREEN
        self.text_img = self.font.render(self.text, True, self.font_colour)
        
        self.text_hitbox = pygame.Rect(self.x, self.y, self.font_size*0.5*len(self.text), self.font_size)
        
    
    def draw(self,screen): 
        self.check_is_hovering()
        if not self.is_hovering: 
            self.text_img = self.font.render(self.text, True, self.font_colour)
        else: 
            self.text_img = self.font.render(self.text, True, self.hover_colour)

        screen.blit(self.text_img, (self.x, self.y))
    
    def check_is_hovering(self): 
        x,y = pygame.mouse.get_pos()
       
        if self.text_hitbox.collidepoint((x,y)): 
            self.is_hovering = True 
        else: 
            self.is_hovering = False
    
    def check_is_clicked(self,x,y): # only called when a click is made s
        if self.text_hitbox.collidepoint(x,y): 
            return True, self.identifier
        return False, ""




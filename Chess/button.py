from tkinter import E
import pygame

pygame.font.init()
GREEN = (0,200,0,0.75)
WHITE = (200,200,200,0.25)
BLACK = (10,10,10,0.95)
GREY = "#7b7b7b"

class Menu_Button: 
    def __init__(self,x, y, text, identifier, font_size): 
        self.text = text
        self.x = x 
        self.y = y 
        self.identifier = identifier
        self.font_colour = BLACK
        self.font_size = font_size 
        self.font_style = 'freesansbold.ttf'
        self.font = pygame.font.Font(self.font_style, self.font_size)
        pygame.font.Font.set_underline(self.font, True)
        self.is_hovering = False
        self.hover_colour = GREY
        self.text_img = self.font.render(self.text, True, self.font_colour)
        self.adjust_x = -int(self.text_img.get_rect().width//2)
        self.adjust_y = -int(self.text_img.get_rect().height//2)
        
        self.text_hitbox = pygame.Rect(self.x+self.adjust_x, self.y+self.adjust_y, self.font_size*0.5*len(self.text), self.font_size)
        
    
    def draw(self,screen): 
        self.check_is_hovering()
        if not self.is_hovering: 
            self.text_img = self.font.render(self.text, True, self.font_colour)
        else: 
            self.text_img = self.font.render(self.text, True, self.hover_colour)

        screen.blit(self.text_img, (self.x+self.adjust_x, self.y+self.adjust_y))
    
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


class Selection_Field: 
    def __init__(self, title_text, options, startx, y, index_selected=0): 
        self.title_text = title_text
        self.options = options
        self.startx = startx
        self.y = y 
        self.options_hover_colour = GREY
        self.options_selected_colour = GREY
        self.index_selected = index_selected
 
        self.gap_x = 100 
        self.initial_gap_x = 250

        self.title_font_size = 30 
        self.title_font_colour = BLACK
        self.title_font_style = 'freesansbold.ttf'
        self.title_font = pygame.font.Font(self.title_font_style, self.title_font_size)

        self.options_font_colour = BLACK 
        self.options_font_style = 'freesansbold.ttf'
        self.options_font_size = 30 
        self.options_font = pygame.font.Font(self.options_font_style, self.options_font_size)
        pygame.font.Font.set_underline(self.options_font, True)


        self.title_text_img = self.title_font.render(self.title_text, True, self.title_font_colour)

        self.option_text_hitboxes = []
        for i in range(len(options)):
            img_hitbox = pygame.Rect(self.startx + (i+1)*self.gap_x + self.initial_gap_x, self.y, self.options_font_size*0.5*len(self.options[i]), self.options_font_size)
            self.option_text_hitboxes.append(img_hitbox)
            
        self.options_text_imgs = []
        for option in options: 
            img = self.options_font.render(option, True, self.options_font_colour)
            self.options_text_imgs.append(img)

        
    def draw(self, screen): 
        screen.blit(self.title_text_img, (self.startx, self.y))
        
        counter = 0 
        for hitbox in self.option_text_hitboxes: 
            x,y = pygame.mouse.get_pos()
            if hitbox.collidepoint((x,y)): 
                self.options_text_imgs[counter] = self.options_font.render(self.options[counter], True, self.options_hover_colour)
            elif counter == self.index_selected:
                self.options_text_imgs[counter] = self.options_font.render(self.options[counter], True, self.options_selected_colour)
            else: 
                self.options_text_imgs[counter] = self.options_font.render(self.options[counter], True, self.options_font_colour)
            screen.blit(self.options_text_imgs[counter], (self.startx + (counter+1)*self.gap_x + self.initial_gap_x, self.y))
            counter += 1
        
    def check_is_clicked(self, x, y): 
        counter = 0 
        for hitbox in self.option_text_hitboxes: 
            if hitbox.collidepoint((x,y)): 
                self.index_selected = counter
                return
            
            counter += 1 


class Icon_Button: 
    def __init__(self, img, x,y, width,height, identifier): 
        
        self.width = width 
        self.height = height
        self.x = x - self.width//2
        self.y = y - self.height//2
        self.img = pygame.transform.scale(pygame.image.load(f"./Images/Icons/{img}"), (self.width, self.height))
        self.identifier = identifier
        self.img_hitbox = pygame.Rect(self.x,self.y,self.width, self.height)

    def draw(self, screen): 
        screen.blit(self.img, (self.x, self.y))
    
    def check_is_clicked(self,x,y): 
        if self.img_hitbox.collidepoint((x,y)): 
            return True, self.identifier
        return False, ""







    

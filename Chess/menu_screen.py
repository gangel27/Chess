
from tkinter import Menu
import pygame

RED = (255,0,0)
WHITE = (255,255,255)
BLACK = (0,0,0)
GREEN = (0,255,0)


class Menu_Screen: 
    def __init__(self,screen):
        self.screen = screen
        self.menu_buttons = []
        self.visible_screen = "Menu_Screen"
        self.title_font = pygame.font.Font('freesansbold.ttf',50)
        self.title_colour = WHITE
        
        self.create_buttons()

    def draw_menu_screen(self): 
        for button in self.menu_buttons: 
            button.draw_button()
        self.draw_title()
    
    def draw_title(self):
        text = "Chess Game"
        self.title_text = self.title_font.render(text, True, self.title_colour)
        self.screen.blit(self.title_text, self.title_text.get_rect(center = (self.screen_x_midpoint,100)))

    def create_buttons(self):
        width = 400
        height = 50 
        self.screen_x_midpoint= pygame.display.get_surface().get_size()[0] // 2

        play_friend_button = Menu_Button(self.screen, self.screen_x_midpoint,200,width, height, "Play With A Friend", "Friend")
        play_ai_button = Menu_Button(self.screen, self.screen_x_midpoint, 275, width, height, "Play The Computer", "AI")
        play_puzzles_button = Menu_Button(self.screen, self.screen_x_midpoint, 350, width, height, "Puzzles", "Puzzle")
        play_options_button = Menu_Button(self.screen, self.screen_x_midpoint, 425, width, height, "Options", "Options")
        
        self.menu_buttons.append(play_friend_button)
        self.menu_buttons.append(play_ai_button)
        self.menu_buttons.append(play_options_button)
        self.menu_buttons.append(play_puzzles_button)
    
    def process_click(self,x,y):
        for button in self.menu_buttons: 
            if button.button_hitbox.collidepoint(x,y): 
                return button.mode, False # the button that is clicked 
        return -1, True


class Menu_Button: 
    def __init__(self, screen, x,y,width,height,text,mode, font_colour=BLACK, hover_colour=None): 
        self.x = x - width//2
        self.y = y - height//2
        self.width = width 
        self.height = height 
        self.font_colour = font_colour
  
        self.text = text 
        self.hover_colour = hover_colour
        self.hover = False
        self.screen = screen
        self.font = pygame.font.Font('freesansbold.ttf',32)
        self.mode = mode
        self.image = pygame.transform.scale(pygame.image.load(f"./Images/Other/button.png"), (self.width, self.height))


    def draw_button(self): 
        if self.hover: self.button_text = self.font.render(self.text, True, self.hover_colour)
        else: self.button_text = self.font.render(self.text, True, self.font_colour)

        self.button_hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
        self.screen.blit(self.image,(self.x,self.y))  
        self.screen.blit(self.button_text,  self.button_text.get_rect(center= self.button_hitbox.center))
            









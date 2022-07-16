
import pygame

RED = (255,0,0)
WHITE = (255,255,255)
BLACK = (0,0,0)
GREEN = (0,255,0)

 


class Menu_Screen: 
    def __init__(self,screen):
        self.screen = screen
        self.menu_buttons = []
        
        self.create_buttons()

    def draw_menu_screen(self): 
        for button in self.menu_buttons: 
            button.draw_button()

    def create_buttons(self):
        x = 100 
        y = 100 
        width = 300
        height = 50 
        play_AI_button = Menu_Button(self.screen, x,y,width, height, "Play",RED,GREEN)
        
        self.menu_buttons.append(play_AI_button)

class Menu_Button: 
    def __init__(self, screen, x,y,width,height,text, background_colour=WHITE, font_colour=BLACK, hover_colour=None): 
        self.x = x
        self.y = y 
        self.width = width 
        self.height = height 
        self.font_colour = font_colour
        self.background_colour = background_colour
        self.text = text 
        self.hover_colour = hover_colour
        self.screen = screen
        self.font = pygame.font.Font('freesansbold.ttf',16)

    def draw_button(self): 
        self.button_hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(self.screen, self.background_colour, self.button_hitbox)

        self.button_text = self.font.render(self.text, True, self.font_colour)
        self.screen.blit(self.button_text, (self.x, self.y))






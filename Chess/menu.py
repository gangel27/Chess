from pygame_button import Button

RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0,0.25)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
ORANGE = (255, 180, 0)

class Main_Menu_Screen: 
    def __init__(self, screen): 
        self.screen = screen 
        self.button_style = {
            "hover_font_color": GREEN,
            "font_color": WHITE}
        self.create_buttons()
    

    def create_buttons(self): 
        self.play_button = Button((200, 300, 200, 50), BLACK, self.printhi, text="Play", **self.button_style)
    
    def draw(self): 
        self.play_button.update(self.screen)
    
    def printhi(self): 
        print('hi')
        

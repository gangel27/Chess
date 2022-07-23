from board_file import Board 
import pygame,sys
from bot import Search_Tree_bot
from threading import Thread 
from menu_screen import Menu_Screen

pygame.init()

SCREEN_WIDTH =  800
SCREEN_HEIGHT = 800
WHITE = (255,255,255)

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT),pygame.RESIZABLE)
navigation_buttons = []

# Menu, AI, Friend, Puzzle, Tutorial
gamemode = "Menu"

def play_friend(is_inverted): 
    board = Board(screen,is_inverted=is_inverted)
    running = True;
    while running: 
        pygame.display.update()
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x,y = pygame.mouse.get_pos()
                board.process_square_click(x,y,"down")
            elif event.type == pygame.MOUSEBUTTONUP: 
                x,y = pygame.mouse.get_pos()
                board.process_square_click(x,y,"up")
                check_navigation_button_click()
            elif event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_LEFT: 
                    board.undo_last_move()
                    
        screen.fill((21, 21, 18))
        board.draw_board()
        draw_back_to_main_menu_button(screen,25,25)
        
       


def menu_screen():
    global gamemode
    menu_screen = Menu_Screen(screen)
    running = True 

    while running: 
        pygame.display.update()
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                running = False
                pygame.quit()
                sys.exit()
        
            if event.type == pygame.MOUSEBUTTONUP: 
                x,y = pygame.mouse.get_pos()
                gamemode, running = menu_screen.process_click(x,y)
        
        screen.fill((21, 21, 18))
        menu_screen.draw_menu_screen()
        

def draw_back_to_main_menu_button(screen, x,y,width=50,height=50):
    font = pygame.font.Font('freesansbold.ttf',50)
    image = pygame.transform.scale(pygame.image.load(f"./Images/Other/button.png"), (width, height))
    back_text = font.render("<", True, WHITE)
    screen.blit(image, image.get_rect(center= (x,y)))
    # screen.blit(image,(x,y))
    screen.blit(back_text, back_text.get_rect(center = (x,y)))

def check_navigation_button_click():

        

menu_screen()
if gamemode == "Friend": play_friend(is_inverted=True)
if gamemode == "AI": play_friend(is_inverted=False)
if gamemode == "Options": play_friend(is_inverted=True)
if gamemode == "Puzzle": play_friend(is_inverted= False)

   


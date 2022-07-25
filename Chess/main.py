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


# Menu, AI, Friend, Puzzle, Tutorial
gamemode = "Menu"
nav_buttons = {}

def play_friend(is_inverted,is_bot_playing): 
    
    board = Board(screen,is_inverted=is_inverted,is_bot_playing=is_bot_playing)
    
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
                check_navigation_button_click("click",(x,y))
            elif event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_LEFT: 
                    board.undo_last_move()
                    
        screen.fill((21, 21, 18))
        draw_back_to_main_menu_button(screen,25,25)
        board.draw_board()
        
        check_navigation_button_click("hover", pygame.mouse.get_pos())

def options_screen():
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
                check_navigation_button_click("click",(x,y))

        screen.fill((21,21,18))
        draw_back_to_main_menu_button(screen, 25,25)

def play_puzzles():
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
                check_navigation_button_click("click",(x,y))

        screen.fill((21,21,18))
        draw_back_to_main_menu_button(screen, 25,25)


            
        
       

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
        if gamemode != "Menu": 
            switch_gamemode()
        

def draw_back_to_main_menu_button(screen, x,y,width=50,height=50):
    global nav_buttons
    font = pygame.font.Font('freesansbold.ttf',50)
    image = pygame.transform.scale(pygame.image.load(f"./Images/Other/button.png"), (width, height))
    back_text = font.render("<", True, WHITE)
    screen.blit(image, image.get_rect(center= (x,y)))
    screen.blit(back_text, back_text.get_rect(center = (x,y)))
    nav_buttons["return_menu"] =  image.get_rect()
    

def check_navigation_button_click(click_type, pos):
    global gamemode

    for button_type, button_rect in nav_buttons.items():
        if button_rect.collidepoint(pos):
            if click_type == "click":
                if button_type == "return_menu":
                    gamemode = "Menu"
                    switch_gamemode()
            elif click_type == "hover": 
                pass



def switch_gamemode():
    if gamemode == "Friend": play_friend(is_inverted=True,is_bot_playing=False)
    if gamemode == "AI": play_friend(is_inverted=False,is_bot_playing=True)
    if gamemode == "Options": options_screen()
    if gamemode == "Puzzle": play_puzzles()
    if gamemode == "Menu": menu_screen()

menu_screen() 


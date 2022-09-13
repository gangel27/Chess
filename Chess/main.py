from board_file import Board 
import pygame,sys
from bot import Search_Tree_bot
from threading import Thread
from menu import Main_Menu_Screen
from button import Button

from menu import Main_Menu_Screen 



pygame.init()

SCREEN_WIDTH =  1000
SCREEN_HEIGHT = 800
WHITE = (255,255,255)

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT),pygame.RESIZABLE)
menu_background_image = pygame.transform.scale(pygame.image.load(f"./Images/Backgrounds/chess_pieces.jpg"), (SCREEN_WIDTH, SCREEN_HEIGHT))



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

            elif event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_LEFT: 
                    board.undo_last_move()
                    
        screen.fill((21, 21, 18))
        board.draw_board()

def main_menu_screen(): 
    running = True
    play_button = Button(100,100,"play", "play_button")
    buttons = [play_button]
    while running: 
        pygame.display.update()
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pass
            elif event.type == pygame.MOUSEBUTTONUP: 
                x,y = pygame.mouse.get_pos()
                for button in buttons:
                    is_clicked, identifier = button.check_is_clicked(x,y)
                    if is_clicked: 
                        play_friend(False, False)

            
                    
        screen.blit(menu_background_image,(0,0))
        for button in buttons:
            button.draw(screen)



main_menu_screen()


# play_friend(True, True)











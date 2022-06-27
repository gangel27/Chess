from board_file import Board 
import pygame,sys
from bot import Search_Tree_bot
from threading import Thread 

pygame.init()

SCREEN_WIDTH =  800
SCREEN_HEIGHT = 800

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT),pygame.RESIZABLE)



def main(): 
    board = Board(screen)
    running = True;
    while running: 
        pygame.display.update()

        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                x,y = pygame.mouse.get_pos()
                board.process_square_click(x,y)
                
        screen.fill((21, 21, 18))
        board.draw_board()
        

        
        


main()
   

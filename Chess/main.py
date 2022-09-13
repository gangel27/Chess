from board_file import Board 
import pygame,sys
from bot import Search_Tree_bot
from threading import Thread

from button import Menu_Button, Selection_Field

pygame.init()

SCREEN_WIDTH =  1200
SCREEN_HEIGHT = 800
WHITE = (255,255,255)
BLACK = (0,0,0)

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT),pygame.RESIZABLE)
menu_background_image = pygame.transform.scale(pygame.image.load(f"./Images/Backgrounds/chess_pieces.jpg"), (SCREEN_WIDTH, SCREEN_HEIGHT))

# main menu 
# tutorial game
# quit 
# general play menu 
# play computer game
# play friend game
# play puzzles game
# settings menu
# pre computer settings menu
# pre 

def central_main(): 
    current_screen_identifier = "main_menu"
    running = True 
    while running: 
        if current_screen_identifier == "main_menu": current_screen_identifier = main_menu_screen()
        elif current_screen_identifier == "tutorial_game": current_screen_identifier = tutorial_screen()
        elif current_screen_identifier == "quit": current_screen_identifier = quit_game_screen()
        elif current_screen_identifier == "general_play_menu": current_screen_identifier = general_play_menu()
        elif current_screen_identifier == "play_computer_game":current_screen_identifier =  play_vs_computer()
        elif current_screen_identifier == "play_friend_game": current_screen_identifier = play_friend_game()
        elif current_screen_identifier == "in_game_settings": current_screen_identifier = in_game_settings()
        elif current_screen_identifier == "play_puzzles_game": current_screen_identifier = play_puzzles_game()
        elif current_screen_identifier == "pre_vs_computer_settings": current_screen_identifier = pre_vs_computer_settings()

def play_friend_game(is_inverted=False,is_bot_playing=False): 
    
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

def main_menu_screen(): # 630x645 to work with form 0,0
    running = True
    button_spacing = 100
    font_size = 40
    button_x = 315
    button_start_y = 350
    title_font_style = "main_font.ttf"
    import os
    print(os.getcwd())
    title_font_size = 120
    title_text = "Chess Lite"
    title_text_colour = BLACK
    title_font_x = 315
    title_font_y = 200

    title_font = pygame.font.Font("main_font.ttf", title_font_size)
    title_font_img = title_font.render(title_text, True, title_text_colour)
    adjust_x = -int(title_font_img.get_rect().width//2)
    adjust_y = -int(title_font_img.get_rect().height//2)
    play_button = Menu_Button(button_x,button_start_y, "Play", "general_play_menu",font_size)
    how_to_play_button = Menu_Button(button_x, button_start_y + (button_spacing), "How to play", "tutorial_game", font_size)
    quit_button = Menu_Button(button_x, button_start_y +(button_spacing*2), "Quit", "quit", font_size)
    title_font = pygame.font.Font(title_font_style, title_font_size)

    buttons = [play_button, how_to_play_button, quit_button]
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
                        return identifier

            
                    
        screen.blit(menu_background_image,(0,0))
        for button in buttons:
            button.draw(screen)
        screen.blit(title_font_img, (title_font_x + adjust_x, title_font_y + adjust_y))
        
def general_play_menu(): 
    running = True
    button_spacing = 100
    font_size = 40
    button_x = 315
    button_start_y = 300
    title_font_style = "freesansbold.ttf"
    title_font_size = 100
    title_text = "Play"
    title_text_colour = BLACK
    title_font_x = 315
    title_font_y = 150

    title_font = pygame.font.Font(title_font_style, title_font_size)
    title_font_img = title_font.render(title_text, True, title_text_colour)
    adjust_x = -int(title_font_img.get_rect().width//2)
    adjust_y = -int(title_font_img.get_rect().height//2)
    play_computer_button = Menu_Button(button_x,button_start_y, "Play the Computer", "pre_vs_computer_settings",font_size)
    play_friend_button = Menu_Button(button_x, button_start_y + (button_spacing), "Play with a Friend ", "play_friend_game", font_size)
    play_puzzles_button = Menu_Button(button_x, button_start_y +(button_spacing*2), "Play Puzzles", "play_puzzles_game", font_size)
    return_to_main_menu_button = Menu_Button(button_x, button_start_y +(button_spacing*3), "Return", "main_menu", font_size)
    title_font = pygame.font.Font(title_font_style, title_font_size)

    buttons = [play_computer_button, play_friend_button, play_puzzles_button, return_to_main_menu_button]
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
                        return identifier

            
                    
        screen.blit(menu_background_image,(0,0))
        for button in buttons:
            button.draw(screen)
        screen.blit(title_font_img, (title_font_x + adjust_x, title_font_y + adjust_y))

def tutorial_screen():
    pass

def quit_game_screen(): 
    pygame.quit()
    sys.exit()

def play_vs_computer(is_inverted=False):
    board = Board(screen,is_inverted,True)
    
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

def in_game_settings():
    pass

def play_puzzles_game(): 
    pass 

def pre_vs_computer_settings(): 
    running = True 
    ai_brain_power = Selection_Field("Depth", ["1", "2", "3"], 30, 200)
    ai_evaluation = Selection_Field("Evaluation Strength", ["1", "2", "3"], 30, 300)
    play_vs_computer_button = Menu_Button(325, 500, "Play Game", "play_computer_game", 30)
    return_button = Menu_Button(325, 600, "Return", "general_play_menu", 30)
    buttons = [play_vs_computer_button, return_button]
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
                        return identifier
                    
        screen.blit(menu_background_image,(0,0))
        ai_brain_power.draw(screen)
        ai_evaluation.draw(screen)
        play_vs_computer_button.draw(screen)
        return_button.draw(screen)
        
 

if __name__ == "__main__": 
    central_main()




# play_friend(True, True)










from board_file import Board 
import pygame,sys
from bot import Search_Tree_bot
from threading import Thread
import json 


from button import Menu_Button, Selection_Field, Icon_Button

pygame.init()

SCREEN_WIDTH =  1200
SCREEN_HEIGHT = 800
WHITE = (255,255,255)
BLACK = (0,0,0)
GREEN = (0,200,0,0.75)
GREY = "#7b7b7b"
BURGANDY = "#66001a"

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT),pygame.RESIZABLE)
menu_background_image = pygame.transform.scale(pygame.image.load(f"./Images/Backgrounds/chess_pieces.jpg"), (SCREEN_WIDTH, SCREEN_HEIGHT))
wooden_background_image = pygame.transform.scale(pygame.image.load(f"./Images/Backgrounds/wooden.jpg"), (SCREEN_WIDTH, SCREEN_HEIGHT))
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
    current_screen_identifier = "play_puzzles_game"
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

    return_button = Icon_Button("back_arrow.png", 50,50,100,100, "general_play_menu")

    
    running = True
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
                
                is_clicked, identifier = return_button.check_is_clicked(x,y)
                if is_clicked: 
                    return identifier

            elif event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_LEFT: 
                    board.undo_last_move()
                    
        screen.blit(wooden_background_image, (0,0))
        board.draw_board()
        return_button.draw(screen)

def main_menu_screen(): # 630x645 to work with form 0,0
    running = True
    button_spacing = 100
    font_size = 40
    button_x = 315
    button_start_y = 350
    title_font_style = "main_font.ttf"

    title_font_size = 120
    title_text = "Chess"
    title_text_colour = BLACK
    title_font_x = 200
    title_font_y = 200
    title_text_2 = "Lite"
    title_text_2_colour = BLACK
    title_2_x_adjust = 360

    title_font = pygame.font.Font("main_font.ttf", title_font_size)
    title_font_img = title_font.render(title_text, True, title_text_colour)
    title_font_img_2 = title_font.render(title_text_2, True, title_text_2_colour)
    adjust_x = -int(title_font_img.get_rect().width//2)
    adjust_y = -int(title_font_img.get_rect().height//2)
    play_button = Menu_Button(button_x,button_start_y, "Play", "general_play_menu",font_size)
    how_to_play_button = Menu_Button(button_x, button_start_y + (button_spacing), "How to play", "tutorial_game", font_size)
    quit_button = Menu_Button(button_x, button_start_y +(button_spacing*2), "Quit", "quit", font_size)
    

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
        screen.blit(title_font_img_2, (title_font_x +adjust_x + title_2_x_adjust, title_font_y + adjust_y))
        
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
    with open("settings.json") as json_file: 
        data = json.load(json_file)
        
        board = Board(screen,is_inverted,True, data['AI-Depth'], data['AI-Evaluation-Strength'])
        return_button = Icon_Button("back_arrow.png", 50,50,100,100, "general_play_menu")
    
    
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
                is_clicked, identifier = return_button.check_is_clicked(x,y)
                if is_clicked: 
                    return identifier

            elif event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_LEFT: 
                    board.undo_last_move()
                    
        screen.blit(wooden_background_image, (0,0))
        board.draw_board()
        return_button.draw(screen)

def in_game_settings():
    pass

def play_puzzles_game(): 
    # board = Board(screen,is_inverted=False,is_bot_playing=False)

    return_button = Icon_Button("back_arrow.png", 50,50,100,100, "general_play_menu")
    fen = "r2qrn1k/1pp1b1p1/3p1p2/p3p2p/P1QnP2P/2NPB2b/BPP2PP1/2KR3R"
    board = Board(screen, is_inverted=True, is_bot_playing=False)
    print(board.flip_fen_position(fen))
    board.fen_to_board(board.flip_fen_position(fen), "white")
    
    running = True
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
                
                is_clicked, identifier = return_button.check_is_clicked(x,y)
                if is_clicked: 
                    return identifier

            elif event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_LEFT: 
                    board.undo_last_move()
                    
        screen.blit(wooden_background_image, (0,0))
        board.draw_board()
        return_button.draw(screen)
     

def pre_vs_computer_settings(): 
    running = True 

    with open("settings.json") as json_file: 
        json_data = json.load(json_file)
        

        ai_brain_power = Selection_Field("Depth", ["1", "2", "3"], 30, 250, json_data['AI-Depth']-1)
        ai_evaluation = Selection_Field("Evaluation Strength", ["1", "2", "3"], 30, 325, json_data['AI-Evaluation-Strength']-1)
        play_vs_computer_button = Menu_Button(325, 550, "Play Game", "play_computer_game", 30)
        return_button = Menu_Button(325, 600, "Return", "general_play_menu", 30)
        buttons = [play_vs_computer_button, return_button]
        fields = [ai_brain_power, ai_evaluation]


    title_font_style = "freesansbold.ttf"
    title_font_size = 100
    title_text = "AI settings"
    title_text_colour = BLACK
    title_font_x = 315
    title_font_y = 100

    title_font = pygame.font.Font(title_font_style, title_font_size)
    title_font_img = title_font.render(title_text, True, title_text_colour)
    adjust_x = -int(title_font_img.get_rect().width//2)
    adjust_y = -int(title_font_img.get_rect().height//2)


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
                        with open("settings.json", "w") as json_file: 
                            json_data["AI-Depth"] = ai_brain_power.index_selected + 1
                            json_data["AI-Evaluation-Strength"] = ai_evaluation.index_selected + 1
                            json.dump(json_data, json_file)

                        return identifier
                
                for field in fields: 
                    field.check_is_clicked(x,y)
                
                    
        screen.blit(menu_background_image,(0,0))
        ai_brain_power.draw(screen)
        ai_evaluation.draw(screen)
        play_vs_computer_button.draw(screen)
        return_button.draw(screen)
        screen.blit(title_font_img, (title_font_x + adjust_x, title_font_y + adjust_y))
        
 

if __name__ == "__main__": 
    central_main()




# play_friend(True, True)










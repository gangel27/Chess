
from piece import Pawn, Knight, Bishop, King, Queen, Rook, is_in_check,find_king_pos,is_in_checkmate
import pygame 
from threading import Thread
from time import sleep 
from bot import Material_Bot, Search_Tree_bot
# from time import sleep



class Board: 
    def __init__(self, screen,is_inverted=False,is_bot_playing=False): 
        self.board = [[0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0]
        ]

        WHITE = (255,255,255)
        BROWN = (139,69,19)
        RED = (255,0,0)
        BLUE = (0,0,255)
        GREEN = (0,255,0)
        LIGHT_GREEN = (111, 189, 43)
        DARK_GREEN = (72, 125, 26)
        GREY = (196, 188, 187)
        LIGHT_GREEN_BLUE = (77, 155, 161)
        LICHESS_MOVE_TO = (171,161,72)
        LICHESS_MOVE_FROM = (206, 209, 123)
        LICHESS_HIGHLIGHT = (106,111,65)
        LICHESS_LEGAL = (135, 120, 79)
        LICHESS_BROWN = (181, 136, 98)
        LICHESS_WHITE = (240, 217, 181)
        LICHESS_COLD_BLUE = (125,161,172)
        LICHESS_COLD_WHITE = (223,227,230)
        LICHESS_COLD_HIGHLIGHT = (92,122,104)
        LICHESS_COLD_LEGAL_MOVE = (93,122,104)
        LICHESS_COLD_MOVE_FROM = (131,155,133)
        LICHESS_COLD_MOVE_TO = (152,176,127)

        self.TOP_MARGIN = 100
        self.LEFT_MARGIN = 100
        self.SQUARE_DIMENSION = 75
        self.SQUARE_COLOUR_1 = LICHESS_WHITE
        self.SQUARE_COLOUR_2 = LICHESS_BROWN
        self.BOTTOM = self.TOP_MARGIN + (8 * self.SQUARE_DIMENSION)
        self.RIGHT = self.LEFT_MARGIN + (8 * self.SQUARE_DIMENSION)
        self.MIDPOINT_X = (self.LEFT_MARGIN) + int((4.5*self.SQUARE_DIMENSION))
        self.MIDPOINT_Y = (self.TOP_MARGIN) + int((4.5*self.SQUARE_DIMENSION))


        self.HIGHLIGHT_COLOUR_SELECTED_PIECE = LICHESS_HIGHLIGHT
        self.HIGHLIGHT_THICKNESS_SELECTED_PIECE = 5
        self.HIGHLIGHT_COLOUR_LEGAL_MOVE = LICHESS_LEGAL
        
        self.CIRCLE_RADIUS_LEGAL_MOVE = 10
        self.HIGHLIGHT_COLOUR_CHECK = RED
        self.HIGLIGHT_THICKNESS_CHECK = 5
        self.CHECK_CIRCLE_RADIUS = self.SQUARE_DIMENSION//2
        self.HIGHLIGHT_THICKNESS_LEGAL_MOVE = 5
        self.HIGHLIGHT_COLOUR_LAST_MOVE_FROM = LICHESS_MOVE_FROM
        self.HIGHLIGHT_THICKNESS_LAST_MOVE_FROM = self.SQUARE_DIMENSION
        self.HIGHLIGHT_COLOUR_LAST_MOVE_TO = LICHESS_MOVE_TO
        self.HIGHLIGHT_THICKNESS_LAST_MOVE_FROM = self.SQUARE_DIMENSION
        self.CHECKMATE_FONT_STYLE = 'freesansbold.ttf'
        self.CHECKMATE_FONT_SIZE = 64 
        self.CHECKMATE_FONT_COLOUR = GREEN
        self.CHECKMATE_BG_COLOUR = GREY 

        self.CHECKMATE_FONT = pygame.font.Font(self.CHECKMATE_FONT_STYLE, self.CHECKMATE_FONT_SIZE)
        self.CHECKMATE_TEXT = self.CHECKMATE_FONT.render('Checkmate!', True, self.CHECKMATE_FONT_COLOUR,self.CHECKMATE_BG_COLOUR)
        self.CHECKMATE_BOX = self.CHECKMATE_TEXT.get_rect()
        self.CHECKMATE_BOX.center = (self.MIDPOINT_X, self.MIDPOINT_Y)

        self.minmax_bot = Search_Tree_bot()
        self.bot_depth = 3
        self.is_inverted = is_inverted
        self.is_bot_playing = is_bot_playing

        self.screen = screen
        
        self.reset_board();

    def switch_square_colour(self,colour):
        if colour == self.SQUARE_COLOUR_1: 
            return self.SQUARE_COLOUR_2
        return self.SQUARE_COLOUR_1

    def draw_board_template(self):
        colour = self.SQUARE_COLOUR_1
        for i in range(8):
            for j in range(8):
               
                x = self.LEFT_MARGIN + (j * self.SQUARE_DIMENSION)
                y = self.TOP_MARGIN + (i * self.SQUARE_DIMENSION)
            
                square = pygame.Rect(x,y, self.SQUARE_DIMENSION, self.SQUARE_DIMENSION)
                pygame.draw.rect(self.screen, colour, square)
                colour = self.switch_square_colour(colour)
            colour = self.switch_square_colour(colour)

    def draw_if_in_check(self):
        if self.currently_in_check: 
            if self.check_pos != (-1,-1):
                x,y = self.row_col_to_coordinates_conversion(self.check_pos[0],self.check_pos[1])
                x+= self.SQUARE_DIMENSION//2
                y+= self.SQUARE_DIMENSION//2
                pygame.draw.circle(self.screen, self.HIGHLIGHT_COLOUR_CHECK,(x,y),self.CHECK_CIRCLE_RADIUS)
        
    def draw_board(self): 
        # draw pieces
        # draw selected_moving_square as highlighted 
        # draw self.piece_legal_moves - doesn't acc calcuate 
        self.draw_board_template()
        self.draw_last_move()
        self.draw_if_in_check()
        self.draw_highlighted_selected_square()
        self.draw_highlighted_legal_moves()
        self.draw_pieces()

        self.draw_if_in_checkmate()   
        if self.is_bot_playing:
            self.bot_depth = 1
            x = Thread(target=self.simulate_bot())
            x.start()  
    
    def draw_last_move(self):
        if self.last_move_from != (-1,-1) and self.last_move_to != (-1,-1):
            x,y = self.row_col_to_coordinates_conversion(self.last_move_from[0],self.last_move_from[1])
            from_square = pygame.Rect(x,y,self.SQUARE_DIMENSION,self.SQUARE_DIMENSION)
            pygame.draw.rect(self.screen, self.HIGHLIGHT_COLOUR_LAST_MOVE_FROM, from_square)

            x,y = self.row_col_to_coordinates_conversion(self.last_move_to[0],self.last_move_to[1])
            to_square = pygame.Rect(x,y,self.SQUARE_DIMENSION,self.SQUARE_DIMENSION)
            pygame.draw.rect(self.screen, self.HIGHLIGHT_COLOUR_LAST_MOVE_TO, to_square)

    def draw_highlighted_legal_moves(self):
        if self.legal_moves_for_selected_piece[0] != (-1,-1):
            for legal_move in self.legal_moves_for_selected_piece:
                x,y = self.row_col_to_coordinates_conversion(legal_move[0],legal_move[1])
                if self.board[legal_move[0]][legal_move[1]] == 0:
                    x+= self.SQUARE_DIMENSION//2
                    y+= self.SQUARE_DIMENSION//2
                    pygame.draw.circle(self.screen, self.HIGHLIGHT_COLOUR_LEGAL_MOVE,(x,y),self.CIRCLE_RADIUS_LEGAL_MOVE)
                else:
                    higlighted_square = pygame.Rect(x,y,self.SQUARE_DIMENSION, self.SQUARE_DIMENSION)
                    pygame.draw.rect(self.screen, self.HIGHLIGHT_COLOUR_LEGAL_MOVE, higlighted_square,self.HIGHLIGHT_THICKNESS_LEGAL_MOVE)

    def draw_pieces(self):
        # squares = []
        
        for i in range(8):
            for j in range(8):
                square = self.board[i][j]
                if square != 0:
                    # if square.colour != self.current_colour_moving:
                    x,y = self.row_col_to_coordinates_conversion(i,j)
                    x += self.SQUARE_DIMENSION//2
                    y += self.SQUARE_DIMENSION//2
                    square.draw(x,y)
                    # else: 
                    #     squares.append([i,j])
        # for i,j in squares: 
        #     x,y = self.row_col_to_coordinates_conversion(i,j)
        #     x += self.SQUARE_DIMENSION//2
        #     y += self.SQUARE_DIMENSION//2
        #     self.board[i][j].draw(x,y)

        if (self.selected_moving_square != (-1,-1)):
            i,j = self.selected_moving_square
            x,y = self.row_col_to_coordinates_conversion(i,j)
            x += self.SQUARE_DIMENSION//2
            y += self.SQUARE_DIMENSION//2
            self.board[i][j].draw(x,y)



    def draw_highlighted_selected_square(self):
        if self.selected_moving_square != (-1,-1):
            x,y = self.row_col_to_coordinates_conversion(self.selected_moving_square[0], self.selected_moving_square[1])
            higlighted_square = pygame.Rect(x,y,self.SQUARE_DIMENSION, self.SQUARE_DIMENSION)
            pygame.draw.rect(self.screen, self.HIGHLIGHT_COLOUR_SELECTED_PIECE, higlighted_square)

    def blit_checkmate(self):
        self.screen.blit(self.CHECKMATE_TEXT, self.CHECKMATE_BOX)
        sleep(1)
        self.reset_board()

    def draw_if_in_checkmate(self):
        if self.in_checkmate:
            x = Thread(target=self.blit_checkmate)
            x.start()
            
    def reset_board(self):
        self.board = [[0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0]
        ]

        self.selected_moving_square = (-1,-1)
        self.legal_moves_for_selected_piece = [(-1,-1)]
        self.current_colour_moving = "white" # "black"
        self.currently_in_check = False
        self.check_pos = (-1,-1)
        self.last_move_from = (-1,-1)
        self.last_move_to = (-1,-1)
        self.in_checkmate = False 
        self.in_stalemate = False
        self.last_move_to_piece = 0
        
        if not self.is_inverted:

            for i in range(8): # pawns 
                self.board[6][i] =  Pawn(self.screen,"white")
                self.board[1][i] =  Pawn(self.screen,"black")
            
        
            self.board[7][0] = Rook(self.screen,"white")
            self.board[7][1] = Knight(self.screen,"white")
            self.board[7][2] = Bishop(self.screen,"white")
            self.board[7][3] = Queen(self.screen,"white")
            self.board[7][4] = King(self.screen,"white")
            self.board[7][5] = Bishop(self.screen,"white")
            self.board[7][6] = Knight(self.screen,"white")
            self.board[7][7] = Rook(self.screen,"white")

            self.board[0][0] = Rook(self.screen,"black")
            self.board[0][1] = Knight(self.screen,"black")
            self.board[0][2] = Bishop(self.screen,"black")
            self.board[0][3] = Queen(self.screen,"black")
            self.board[0][4] = King(self.screen,"black")
            self.board[0][5] = Bishop(self.screen,"black")
            self.board[0][6] = Knight(self.screen,"black")
            self.board[0][7] = Rook(self.screen,"black")

        else: 
            for i in range(8): # pawns 
                self.board[6][i] =  Pawn(self.screen,"black",True)
                self.board[1][i] =  Pawn(self.screen,"white",True)
            
        
            self.board[7][0] = Rook(self.screen,"black")
            self.board[7][1] = Knight(self.screen,"black")
            self.board[7][2] = Bishop(self.screen,"black")
            self.board[7][4] = Queen(self.screen,"black")
            self.board[7][3] = King(self.screen,"black",True)
            self.board[7][5] = Bishop(self.screen,"black")
            self.board[7][6] = Knight(self.screen,"black")
            self.board[7][7] = Rook(self.screen,"black")

            self.board[0][0] = Rook(self.screen,"white")
            self.board[0][1] = Knight(self.screen,"white")
            self.board[0][2] = Bishop(self.screen,"white")
            self.board[0][4] = Queen(self.screen,"white")
            self.board[0][3] = King(self.screen,"white",True)
            self.board[0][5] = Bishop(self.screen,"white")
            self.board[0][6] = Knight(self.screen,"white")
            self.board[0][7] = Rook(self.screen,"white")

    def move_selected_piece(self,row,col):
        # moves the currently selecting moving piece, to the square taken as a paramter, has already been checked for legality 
        # unhighlight piece. 
        # remove legal moves 
        if row != -1 and col != -1:
            if self.selected_moving_square != (-1,-1):
                self.last_move_to_piece = self.board[row][col] # here 
                self.board[row][col] = self.board[self.selected_moving_square[0]][self.selected_moving_square[1]]
                self.board[self.selected_moving_square[0]][self.selected_moving_square[1]] = 0
                self.last_move_from = self.selected_moving_square
                self.last_move_to = (row,col)
               
                self.legal_moves_for_selected_piece = [(-1,-1)]
                self.selected_moving_square = (-1,-1)

                self.check_if_castling(row,col) # moves rook 
                self.check_if_promotion(row,col)
                self.check_if_en_passant(row,col)
                self.alternate_move_color()
                self.set_pawns_just_moved_2_squares_false() # just_moved_2_squares = False
            
                if self.board[row][col].name == "pawn" or self.board[row][col].name=="rook" or self.board[row][col].name=="king":
                    self.board[row][col].moved = True
                
                if self.board[row][col].name == "pawn": # for en passant
                    squares_moved = abs(self.last_move_from[0]- self.last_move_to[0])
                    if squares_moved == 2:
                        self.board[row][col].just_moved_2_squares = True
    
    def check_if_en_passant(self,row,col):
        if self.current_colour_moving == "white":
            en_passant_to_rank = 2
            en_passant_from_rank = 3
            moving = 1
            if self.is_inverted: 
                en_passant_to_rank = 5
                en_passant_from_rank = 4
                moving = -1

        elif self.current_colour_moving == "black":
            en_passant_to_rank = 5
            en_passant_from_rank = 4
            moving = -1
            if self.is_inverted: 
                en_passant_to_rank = 2
                en_passant_from_rank = 3
                moving = 1

        if row == en_passant_to_rank:
            if self.last_move_from[0] == en_passant_from_rank:
                if abs(col-self.last_move_from[1]) == 1: # moved one column over

                    self.board[row+moving][col] = 0

    def set_pawns_just_moved_2_squares_false(self):
        for i in range(8):
            for j in range(8):
                if self.board[i][j] != 0:
                    if self.board[i][j].name == "pawn":
                        self.board[i][j].just_moved_2_squares = False

    def check_if_promotion(self,row,col):
    
        if self.current_colour_moving == "white":
            end_rank = 0
            if self.is_inverted: 
                end_rank = 7
        else: 
            end_rank = 7 
            if self.is_inverted:
                end_rank = 0 
        
        if row == end_rank and self.board[row][col].name == "pawn": 
            self.board[row][col] = Queen(self.screen, self.current_colour_moving)

    def check_if_castling(self,row,col):
        if self.current_colour_moving == "white":
            home = 7
            if self.is_inverted: 
                home = 0 
        else: # black 
            home = 0
            if self.is_inverted: 
                home = 7 
        
        
        king_starting_col = 4 
        kingside_dir = 1 
        queenside_dir = -1 
        king_rook_col = 7 
        queen_rook_col = 0 
        if self.is_inverted: 
            king_starting_col = 3
            kingside_dir = -1 
            queenside_dir = 1 
            king_rook_col = 0 
            queen_rook_col = 7

        if self.board[row][col].name == "king":
            if col == king_starting_col + (2*kingside_dir) and row == home: # kingside
                if self.board[home][king_rook_col] != 0:
                    if self.board[home][king_rook_col].name == "rook":
                        if self.board[home][king_rook_col].moved == False: # if rook hasnt' moved
                            if self.board[home][king_starting_col + (2*kingside_dir)].moved == False: # if king hasnt' moved
                                self.board[home][king_starting_col+kingside_dir] = self.board[home][king_rook_col]
                                self.board[home][king_rook_col] = 0
                                self.board[home][king_starting_col+kingside_dir].moved = True
                                self.board[row][col].castled = True
            
            if col == king_starting_col +(2*queenside_dir) and row == home: # queenside
                if self.board[home][queen_rook_col] != 0:
                    if self.board[home][queen_rook_col].name == "rook":
                        if self.board[home][queen_rook_col].moved == False:
                            if self.board[home][king_starting_col + (2*queenside_dir)].moved == False:
                                self.board[home][king_starting_col+queenside_dir] = self.board[home][queen_rook_col]
                                self.board[home][queen_rook_col] = 0
                                self.board[home][king_starting_col+queenside_dir].moved = True
                                self.board[row][col].castled = True

    def undo_last_move(self): 
        pass
        if self.last_move_from != (-1,-1) or self.last_move_to != (-1,-1):
            self.board[self.last_move_from[0]][self.last_move_from[1]] = self.board[self.last_move_to[0]][self.last_move_to[1]]
            self.board[self.last_move_to[0]][self.last_move_to[1]] = self.last_move_to_piece
            self.selected_moving_square = (-1,-1)
            self.legal_moves_for_selected_piece = [(-1,-1)]
            self.last_move_from = (-1,-1)
            self.last_move_to = (-1,-1)
            self.alternate_move_color() # reverts move colour back
    
    def clear_board(self): 
        for i in range(8):
            for j in range(8): 
                self.board[i][j] = 0 
    
    def convert_modified_fen_to_board(pos,move):
        # pos: rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1
        pass

    def alternate_move_color(self):
        if self.current_colour_moving == "white":
            self.current_colour_moving = "black"
        else:
            self.current_colour_moving = "white"

    def process_square_click(self,x,y,click_type):
        '''
        FIRST: convert, using coordinates_to_row_col_conversion()
        2 possible valid clicks 2) selecting a piece 1) moving an already selected piece.
        if we check moving a piece first, if that's not true, then we can simply highlight the square clicked 
        
        1) moving a piece 
            find the legal moves of the currently selected piece, using self.selecting_moving square and self.legal_moves
            if the square clicked is in legal moves, then move the piece
            move_selected_piece(col,row)
            make selected piece emptpty, and same with legal moves. 
            
        2) selecing a piece
            assuming click is in the board area, draw a rectangle around the box of click. 
            check the selected_Moving_square, and call the find legal moves for specific piece. 
        '''
        # row,col = coordinates_to_row_col_conversion(x,y)
        # if 0<=row<=7 and 0<=col<=7:
            # moved = false 
            # for legal move in piece_legal_moves
                # if legal move == row, col:
                    # move_selected_piece(row,col)
                    # moved = true 

            # if not moved: 
                # self.selected_moving_square = (row,col)
                # find_legal_moves_for_piece(row,col)
        is_processed = False 
        row,col,error = self.coordinates_to_row_col_conversion(x,y)

        if not is_processed:  # moves a piece
            for legal_move in self.legal_moves_for_selected_piece:
                if (row,col) == legal_move:

                    if self.board[self.selected_moving_square[0]][self.selected_moving_square[1]] != 0:
                        self.board[self.selected_moving_square[0]][self.selected_moving_square[1]].follow_mouse = False 
                    self.move_selected_piece(row,col)
                    if is_in_check(self.board, self.current_colour_moving):
                        self.check_pos = find_king_pos(self.board, self.current_colour_moving)
                        self.currently_in_check = True 
                        self.in_checkmate = is_in_checkmate(self.board, self.current_colour_moving)
                        
                    else:
                        self.currently_in_check = False
                        self.check_pos = (-1,-1)
                    is_processed = True

            
        
        if not is_processed: # puts piece back in place if not in moved square
            if (row,col) == self.selected_moving_square: 
                if self.board[row][col] != 0:
                    if self.board[row][col].colour == self.current_colour_moving:
                        if click_type == "up":
                            self.board[row][col].follow_mouse = False

                            is_processed = True
            else: 
                # legal moves have already been filtered out, so we know that this move has to be a none move
                if self.board[self.selected_moving_square[0]][self.selected_moving_square[1]] != 0:
                    self.board[self.selected_moving_square[0]][self.selected_moving_square[1]].follow_mouse = False 
                    self.selected_moving_square = (-1,-1)
                    self.legal_moves_for_selected_piece = [(-1,-1)]
                


        if not is_processed: # highlights a square also want the piece to follow the mouse 
            if not error: 
                if self.board[row][col] != 0:
                    self.selected_moving_square = (row,col)
                    if self.board[row][col] != 0:
                        self.legal_moves_for_selected_piece = self.board[row][col].legal_moves(self.board, row,col, self.current_colour_moving)
                        if click_type == "down":
                            if self.board[row][col].colour == self.current_colour_moving:
                                self.board[row][col].follow_mouse = True 
                    else:
                        self.legal_moves_for_selected_piece = [(-1,-1)]
            else: # clicked outside the range of the board
                self.selected_moving_square = (-1,-1)
                self.legal_moves_for_selected_piece = [(-1,-1)]

    def row_col_to_coordinates_conversion(self,row,col):
        x = self.LEFT_MARGIN + (col * self.SQUARE_DIMENSION)
        y = self.TOP_MARGIN + (row * self.SQUARE_DIMENSION)
        return (x,y)

    def is_click_in_board(self,x,y):
        if x >= self.LEFT_MARGIN and x <= self.RIGHT:
            if y >= self.TOP_MARGIN and y <= self.BOTTOM:
                return True
        return False

    def coordinates_to_row_col_conversion(self,x,y):
        error = True 
        row = -1 
        col = -1
        if self.is_click_in_board(x,y):
            col = (x - self.LEFT_MARGIN) // self.SQUARE_DIMENSION
            row = (y - self.TOP_MARGIN) // self.SQUARE_DIMENSION
            error = False 
        return (row,col, error )
    
    def simulate_bot(self):
        pygame.display.update()
        print(self.current_colour_moving)
        if self.current_colour_moving == "black" and not self.in_checkmate:
            # from_row, from_col, to_row, to_col = return_random_ai_move(self.board, "black")
            move, _ = self.minmax_bot.minimax(self.board, self.bot_depth, False)
            from_row = move[0]
            from_col = move[1]
            to_row = move[2]
            to_col = move[3]
            
            # from_row,from_col,to_row,to_col = 1,2,3,2
            print(from_row, from_col, to_row, to_col)
            print(f"Suggested move: ({self.board[from_row][from_col]}) --> ({to_row},{to_col})")
            # print(_)

            self.selected_moving_square = (from_row,from_col)
            self.move_selected_piece(to_row,to_col)
            if is_in_check(self.board, self.current_colour_moving):
                self.check_pos = find_king_pos(self.board, self.current_colour_moving)
                self.currently_in_check = True 
                self.in_checkmate = is_in_checkmate(self.board, self.current_colour_moving)
            else:
                self.currently_in_check = False
                self.check_pos = (-1,-1)



            self.selected_moving_square = (-1,-1)
            self.legal_moves_for_selected_piece = [(-1,-1)]
            
            self.currently_in_check = False
            self.currently_in_check = is_in_check(self.board, self.current_colour_moving)
    











from piece import Pawn, Knight, Bishop, King, Queen, Rook, is_in_check,find_king_pos, is_in_checkmate_or_stalemate
import pygame 
import threading
from bot import Search_Tree_bot


class Board: 
    def __init__(self, screen,is_inverted=False,is_bot_playing=False, ai_depth=0, ai_evaluatoin_level=0, user_colour="white"): 
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
        PEACH = (255,229,180)

        self.TOP_MARGIN = 100
        self.LEFT_MARGIN = 300
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


        self.STALEMATE_FONT_STYLE = 'freesansbold.ttf'
        self.STALEMATE_FONT_SIZE = 64 
        self.STALEMATE_FONT_COLOUR = GREEN
        self.STALEMATE_BG_COLOUR = GREY 

        self.STALEMATE_FONT = pygame.font.Font(self.STALEMATE_FONT_STYLE, self.STALEMATE_FONT_SIZE)
        self.STALEMATE_TEXT = self.STALEMATE_FONT.render('Stalemate!', True, self.STALEMATE_FONT_COLOUR,self.STALEMATE_BG_COLOUR)
        self.STALEMATE_BOX = self.STALEMATE_TEXT.get_rect()
        self.STALEMATE_BOX.center = (self.MIDPOINT_X, self.MIDPOINT_Y)

        x_buffer = self.LEFT_MARGIN//8
        box_width = 165
        box_height = 180
        self.CAPTURED_PIECE_BOX_BACKGROUND_COLOUR = self.SQUARE_COLOUR_1
        self.pieces_selected_top_box = pygame.Rect(x_buffer + self.RIGHT,self.TOP_MARGIN,box_width,box_height)
        self.pieces_selected_bottom_box = pygame.Rect(self.LEFT_MARGIN - x_buffer - box_width, self.BOTTOM - box_height, box_width,box_height)
        self.piece_captured_index = { 
            "pawn": 0, 
            "knight": 1, 
            "bishop": 2, 
            "rook": 3, 
            "queen": 4
        }
        self.number_of_identical_captured_pieces = {
            "pawn": {"white": 0, "black": 0},
            "knight": {"white": 0, "black": 0},
            "bishop": {"white": 0, "black": 0},
            "rook": {"white": 0, "black": 0},
            "queen": {"white": 0, "black": 0}
        }

        self.minmax_bot = Search_Tree_bot()
        self.bot_depth = 3
        self.is_inverted = is_inverted
        self.is_bot_playing = is_bot_playing
        self.ai_depth = ai_depth 
        self.ai_eval_level = ai_evaluatoin_level
        self.user_colour = user_colour
        
        self.thread_make_ai_think = self.return_new_ai_thread()
        self.screen = screen
        self.ints = ["0","1", "2", "3", "4", "5", "6", "7", "8", "9"]
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
        self.draw_if_in_stalemate()
        self.draw_captured_pieces()
    
    def draw_if_in_stalemate(self): 
        if self.in_stalemate:
            x = threading.Thread(target=self.blit_stalemate)
            x.start() 
    
    def blit_stalemate(self): 
        self.screen.blit(self.STALEMATE_TEXT, self.STALEMATE_BOX)
        t = threading.Timer(3.0, self.reset_board)
        t.start()

    def draw_last_move(self):
        if self.last_move_from != (-1,-1) and self.last_move_to != (-1,-1): 
            # last move from 
            x,y = self.row_col_to_coordinates_conversion(self.last_move_from[0],self.last_move_from[1])
            from_square = pygame.Rect(x,y,self.SQUARE_DIMENSION,self.SQUARE_DIMENSION)
            pygame.draw.rect(self.screen, self.HIGHLIGHT_COLOUR_LAST_MOVE_FROM, from_square)

            # last move to 
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
        
    def fen_to_board(self, fen, colour_moving): 
        
        self.board = []
        
        for row in fen.split('/'):
            brow = []
            for c in row:
                if c == ' ':
                    break
                elif c in '12345678':
                    brow.extend( [0] * int(c) )
                elif c == 'P': brow.append(Pawn(self.screen, "white"))
                elif c == 'p': brow.append(Pawn(self.screen, "black"))
                elif c == "R": brow.append(Rook(self.screen, "white"))
                elif c == "r": brow.append(Rook(self.screen, "black"))
                elif c == "B": brow.append(Bishop(self.screen, "white"))
                elif c == "b": brow.append(Bishop(self.screen, "black"))
                elif c == "Q": brow.append(Queen(self.screen, "white"))
                elif c == "q": brow.append(Queen(self.screen, "black"))
                elif c == "K": brow.append(King(self.screen, "white"))
                elif c == "k": brow.append(King(self.screen, "black"))
                elif c == "N": brow.append(Knight(self.screen, "white"))
                elif c == "n": brow.append(Knight(self.screen, "black"))
      
                
            self.board.append(brow)
        self.current_colour_moving = colour_moving
        self.board.remove([])

    def flip_fen_position(self, fen): 
        fen_rows = fen.split("/")
        string = f"{fen_rows[7][::-1]}/{fen_rows[6][::-1]}/{fen_rows[5][::-1]}/{fen_rows[4][::-1]}/{fen_rows[3][::-1]}/{fen_rows[2][::-1]}/{fen_rows[1][::-1]}/{fen_rows[0][::-1]}/"
        return string 

    def draw_highlighted_selected_square(self):
        if self.selected_moving_square != (-1,-1):
            x,y = self.row_col_to_coordinates_conversion(self.selected_moving_square[0], self.selected_moving_square[1])
            higlighted_square = pygame.Rect(x,y,self.SQUARE_DIMENSION, self.SQUARE_DIMENSION)
            pygame.draw.rect(self.screen, self.HIGHLIGHT_COLOUR_SELECTED_PIECE, higlighted_square)

    def blit_checkmate(self):
        self.screen.blit(self.CHECKMATE_TEXT, self.CHECKMATE_BOX)

        t = threading.Timer(3.0, self.reset_board)
        t.start()

    def draw_if_in_checkmate(self):
        if self.in_checkmate:
            x = threading.Thread(target=self.blit_checkmate)
            x.start()
    
    def draw_captured_pieces(self): 
        self.draw_captured_pieces_backgrounds()
      
        for piece in self.pieces_white_has_captured:
            piece.draw_icon(self.piece_captured_index[piece.name], self.number_of_identical_captured_pieces[piece.name][piece.colour], piece.colour, self.is_inverted)
        for piece in self.pieces_black_has_captured: 
            piece.draw_icon(self.piece_captured_index[piece.name], self.number_of_identical_captured_pieces[piece.name][piece.colour], piece.colour, self.is_inverted)

    def draw_captured_pieces_backgrounds(self): 
        pygame.draw.rect(self.screen, self.CAPTURED_PIECE_BOX_BACKGROUND_COLOUR, self.pieces_selected_top_box)
        pygame.draw.rect(self.screen, self.CAPTURED_PIECE_BOX_BACKGROUND_COLOUR, self.pieces_selected_bottom_box)
            
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
        self.pieces_white_has_captured = []
        self.pieces_black_has_captured = []
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

                # adds to captured piece 
                if self.board[row][col] != 0:
                    piece = self.board[row][col]
                    if piece.colour == "white": 
                        self.pieces_black_has_captured.append(piece)
                        
                    elif piece.colour == "black": 
                        self.pieces_white_has_captured.append(piece)
                    self.number_of_identical_captured_pieces[piece.name][piece.colour] += 1 

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
                        
        if self.is_bot_playing: 
            self.thread_make_ai_think = self.return_new_ai_thread().start()

    def return_new_ai_thread(self): 
        return threading.Thread(target=self.simulate_bot,daemon=False)
    
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
                    if self.board[row][col].name == "pawn":
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
        if not is_in_check(self.board, self.current_colour_moving):
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
    
    def flip_board(self): 
        self.is_inverted = not(self.is_inverted)
        temp_board = [
            self.board[7][::-1],
            self.board[6][::-1],
            self.board[5][::-1],
            self.board[4][::-1],
            self.board[3][::-1], 
            self.board[2][::-1], 
            self.board[1][::-1],
            self.board[0][::-1]
        ]
        self.board = temp_board
        for row in range(8): 
            for col in range(8): 
                if self.board[row][col] != 0:
                    if self.board[row][col].name == "pawn" or self.board[row][col].name == "king": 
                        self.board[row][col].is_inverted = not(self.board[row][col].is_inverted)

        
        self.selected_moving_square = (-1,-1)
        self.last_move_from = (-1,-1)
        self.last_move_to = (-1,-1)
        self.legal_moves_for_selected_piece = [(-1,-1)]

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
        
        is_processed = False 
        row,col,error = self.coordinates_to_row_col_conversion(x,y)

        if not is_processed:  # moves an already selected piece
            for legal_move in self.legal_moves_for_selected_piece:
                if (row,col) == legal_move:

                    if self.board[self.selected_moving_square[0]][self.selected_moving_square[1]] != 0:
                        self.board[self.selected_moving_square[0]][self.selected_moving_square[1]].follow_mouse = False 
                    self.move_selected_piece(row,col)
                    if is_in_check(self.board, self.current_colour_moving):
                        self.check_pos = find_king_pos(self.board, self.current_colour_moving)
                        self.currently_in_check = True 
                        self.in_checkmate = is_in_checkmate_or_stalemate(self.board, self.current_colour_moving)
                        
                    else:
                        self.in_stalemate = is_in_checkmate_or_stalemate(self.board, self.current_colour_moving)
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
                    if click_type == "down": 
                        self.selected_moving_square = (row,col)
                        if self.board[row][col] != 0:
                            self.legal_moves_for_selected_piece = self.board[row][col].legal_moves(self.board, row,col, self.current_colour_moving)
                            if self.is_bot_playing: 
                                if self.board[row][col].colour != self.user_colour: 
                                    self.legal_moves_for_selected_piece = [(-1,-1)]

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
        print('simulating bot..,')
        
        if self.current_colour_moving == "black" and not self.in_checkmate:
            # from_row, from_col, to_row, to_col = return_random_ai_move(self.board, "black")
            move, _ = self.minmax_bot.minimax(self.board, self.ai_depth , False, self.ai_eval_level)
            from_row = move[0]
            from_col = move[1]
            to_row = move[2]
            to_col = move[3]
            
            # from_row,from_col,to_row,to_col = 1,2,3,2
            # print(from_row, from_col, to_row, to_col)
            # print(f"Suggested move: ({self.board[from_row][from_col]}) --> ({to_row},{to_col})")
            # print(_)

            self.selected_moving_square = (from_row,from_col)
            self.move_selected_piece(to_row,to_col)
            if is_in_check(self.board, self.current_colour_moving):
                self.check_pos = find_king_pos(self.board, self.current_colour_moving)
                self.currently_in_check = True 
                self.in_checkmate = is_in_checkmate_or_stalemate(self.board, self.current_colour_moving)
            else:
                self.currently_in_check = False
                self.check_pos = (-1,-1)



            self.selected_moving_square = (-1,-1)
            self.legal_moves_for_selected_piece = [(-1,-1)]
            
            self.currently_in_check = False
            self.currently_in_check = is_in_check(self.board, self.current_colour_moving)
    










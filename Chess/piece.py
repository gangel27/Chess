import pygame

def is_square_empty(board, row,col,capture,piece_colour):
    if row >=8 or col >=8: 
        return False
    if board[row][col] == 0: # if empty 
        return True
    if capture:
        if board[row][col].colour != piece_colour:
            return True
    if board[row][col].colour == piece_colour: 
        return False
    return False 

def filter_legal_moves_for_check(local_board, row,col,legal_moves,colour_moving):
    removing = []# have to do it like htis, otherwise the for loop stops early
    # can't just remove srtaight away 
    # adds the moves to be removed to a list, then iterates through the list, and removes said moves. 
    for move in legal_moves: 
        
        editing_board = list(map(list, local_board)) # copy with a different place in memory 
        editing_board[move[0]][move[1]] = editing_board[row][col] 
        editing_board[row][col] = 0

        if is_in_check(editing_board, colour_moving):
            removing.append(move)

    for move in removing: 
        legal_moves.remove(move)

    return legal_moves

def find_king_pos(local_board, colour):
    for i in range(8):
        for j in range(8):
            if local_board[i][j] != 0:
                if local_board[i][j].name == "king":
                    if local_board[i][j].colour == colour:
                        return (i,j)
                        
def is_in_check(local_board, colour_moving): # edit this function when added pieces
    # lets' say we're checking for white

    in_check = False
    opposite_colour = 'white'
    if colour_moving == 'white':
        opposite_colour = 'black'

    
    king_pos = find_king_pos(local_board,colour_moving)


    for i in range(8):
        for j in range(8):
            if local_board[i][j] != 0:
                if local_board[i][j].colour == opposite_colour:
                    squares_piece_controls = local_board[i][j].controls(local_board, i,j, opposite_colour)

                    for move in squares_piece_controls:
                        if move != (-1,-1):
                            if move == king_pos:
                                in_check = True 

    return in_check


def is_in_checkmate_or_stalemate(board,colour_moving): # returns if the player doesn't have a legal move 
        possible_moves = []
        for i in range(8):
            for j in range(8):
                if board[i][j] != 0:
                    if board[i][j].colour == colour_moving:
                        moves_for_piece = board[i][j].legal_moves(board,i,j,colour_moving)

                        for move in moves_for_piece:
                            if move != (-1,-1):
                                possible_moves.append(move)

        if possible_moves == []:
            return True
        return False
        
class Piece: 
    def __init__(self,screen, colour): 
        self.screen = screen 

        self.colour = colour

        self.img_height = 60
        self.img_width = 60
        self.width_offset = 5
        self.height_offset = 5
        self.set = 'set-5'
        self.set = 'set-6'
        self.set = 'lichess-set'
        self.follow_mouse = False

        self.icon_width = 30
        self.icon_height = 35
        self.icon_gap_y = 35
        self.icon_gap_x = 15
        self.white_captured_pieces_box_x = 940
        self.white_captured_pieces_box_y = 100 
        self.black_captured_pieces_box_x = 100
        self.black_captured_pieces_box_y = 525


    def draw(self, x,y):
        if self.follow_mouse: 
            x,y = pygame.mouse.get_pos()
        if self.colour == "white":
            img = self.image_white
            rect = img.get_rect()
            rect.center = (x,y)
            self.screen.blit(self.image_white, rect)
            
        else:
            img = self.image_black
            rect = img.get_rect()
            rect.center = (x,y)
            self.screen.blit(self.image_black, rect)
    
    def draw_icon(self, index, number_of_identical_pieces_captured,  colour, inverted): 
        for i in range(number_of_identical_pieces_captured): 
            if not inverted: 
                if colour == "white": 
                    self.screen.blit(self.icon_image_white, ((self.white_captured_pieces_box_x + (i*self.icon_gap_x)), self.white_captured_pieces_box_y + (self.icon_gap_y* index)))
                else: 
                    self.screen.blit(self.icon_image_black, ((self.black_captured_pieces_box_x + (i*self.icon_gap_x)), self.black_captured_pieces_box_y + (self.icon_gap_y* index)))
            else: 
                if colour == "white": 
                    self.screen.blit(self.icon_image_white, ((self.black_captured_pieces_box_x + (i*self.icon_gap_x)), self.black_captured_pieces_box_y + (self.icon_gap_y* index)))
                else: 
                    self.screen.blit(self.icon_image_black, ((self.white_captured_pieces_box_x + (i*self.icon_gap_x)), self.white_captured_pieces_box_y + (self.icon_gap_y* index)))


      
class Pawn(Piece): 
    def __init__(self,screen, colour,is_inverted=False): 
        super(Pawn, self).__init__(screen, colour)
        self.image_white = pygame.transform.scale(pygame.image.load(f"./Images/{self.set}/white_pawn.png"), (self.img_width, self.img_height))
        self.image_black = pygame.transform.scale(pygame.image.load(f"./Images/{self.set}/black_pawn.png"), (self.img_width, self.img_height))
        self.icon_image_white = pygame.transform.scale(pygame.image.load(f"./Images/{self.set}/white_pawn.png"), (self.icon_width, self.icon_height))
        self.icon_image_black = pygame.transform.scale(pygame.image.load(f"./Images/{self.set}/black_pawn.png"), (self.icon_width, self.icon_height))
        self.moved = False
        self.name = "pawn"
        self.just_moved_2_squares = False # allows for en passant 
        self.value = 1 
        self.is_inverted= is_inverted
        self.colour = colour

    def legal_moves(self,board, row,col, colour_moving):
    
        # 2 forwards, 1 forwards, caputre left, caputre right
        
        moves = [] 
        if self.colour == "white":
            moving = -1 # moves up the 2D array 
        else: 
            moving = 1 # moves down the 2D array

        if self.is_inverted: 
            moving *= -1 

        if colour_moving == self.colour:
            # moves 1 forwards
            free = is_square_empty(board,row + moving, col, False, colour_moving)
            if free: moves.append((row +moving, col))


             # moves 2 forwards
            if not self.moved:
                free = is_square_empty(board, row + (2*moving),col, False,colour_moving)
                if free and(row+moving,col) in moves: moves.append((row+(2*moving),col))

            # capture right
            if col < 7:
                if board[row + moving][col + 1] != 0:
                    if board[row + moving][col + 1].colour != colour_moving: 
                        moves.append((row+moving, col+1))
            
            # capture left
            if col > 0:
                if board[row + moving][col - 1] != 0:
                    if board[row + moving][col - 1].colour != colour_moving: 
                        moves.append((row+moving, col-1))
            
            # en passant left
            if col > 0:
                if board[row][col-1] != 0:
                    if board[row][col-1].name == "pawn":
                        if board[row][col-1].just_moved_2_squares:
                            
                            moves.append((row+moving,col-1))

            # en passant right
            if col < 7:
                if board[row][col+1] != 0:
                    if board[row][col+1].name == "pawn":
                        if board[row][col+1].just_moved_2_squares:
                            moves.append((row+moving,col+1))

        moves = filter_legal_moves_for_check(board,row,col,moves,colour_moving)
        if moves == []:
            moves = [(-1,-1)]
        return moves
    
    def controls(self,board,row, col,colour_moving):
        # 2 forwards, 1 forwards, caputre left, caputre right
        # to do: en passant, promotion.
        moves = [] 
        if self.colour == "white":
            moving = -1 # moves up the 2D array 
        else: 
            moving = 1 # moves down the 2D array
        
        if self.is_inverted: 
            moving *= -1 

        if colour_moving == self.colour:
            # capture right
            if col < 7: moves.append((row+moving, col+1))
            
            # capture left
            if col > 0: moves.append((row+moving, col-1))

        if moves == []:
            moves = [(-1,-1)]
        return moves
  
class Knight(Piece): 
    def __init__(self,screen, colour): 
        super(Knight, self).__init__(screen, colour)
        self.image_white = pygame.transform.scale(pygame.image.load(f"./Images/{self.set}/white_knight.png"), (self.img_width, self.img_height))
        self.image_black = pygame.transform.scale(pygame.image.load(f"./Images/{self.set}/black_knight.png"), (self.img_width, self.img_height))
        self.icon_image_white = pygame.transform.scale(pygame.image.load(f"./Images/{self.set}/white_knight.png"), (self.icon_width, self.icon_height))
        self.icon_image_black = pygame.transform.scale(pygame.image.load(f"./Images/{self.set}/black_knight.png"), (self.icon_width, self.icon_height))
        self.name = "knight"
        self.value = 3
        

    def legal_moves(self,board, row,col,colour_moving): 
        moves = []
        if colour_moving == self.colour:

            # left 1 and up 2 
            if col > 0 and row > 1:
                free = is_square_empty(board, row-2, col-1, True, self.colour)
                if free: moves.append((row-2,col-1))

            # right 1 up 2
            if col < 7 and row > 1:
                free = is_square_empty(board, row-2, col+1, True, self.colour)
                if free: moves.append((row-2,col+1))

            # left 2 up 1 
            if col > 1 and row > 0:
                free = is_square_empty(board, row-1, col-2, True, self.colour)
                if free: moves.append((row-1,col-2))

            # right 2 up 1 
            if col < 6 and row > 0:
                free = is_square_empty(board, row-1, col+2, True, self.colour)
                if free: moves.append((row-1,col+2))

            # left 2 down 1
            if col > 1 and row < 7:
                free = is_square_empty(board, row+1, col-2, True, self.colour)
                if free: moves.append((row+1,col-2))

            # right 2 down 1 
            if col < 6 and row < 7:
                free = is_square_empty(board, row+1, col+2, True, self.colour)
                if free: moves.append((row+1,col+2))

            # left 1 down 2
            if col > 0 and row < 6:
                free = is_square_empty(board, row+2, col-1, True, self.colour)
                if free: moves.append((row+2,col-1))

            # right 1 down 2 
            if col < 7 and row < 6:
                free = is_square_empty(board, row+2, col+1, True, self.colour)
                if free: moves.append((row+2,col+1))
            


        moves = filter_legal_moves_for_check(board,row,col,moves,colour_moving)
        if moves == []:
            moves = [(-1,-1)]

        
        return moves
    
    def controls(self,board, row,col,colour_moving):
        moves = []
        if colour_moving == self.colour:

            # left 1 and up 2 
            if col > 0 and row > 1:
                free = is_square_empty(board, row-2, col-1, True, self.colour)
                if free: moves.append((row-2,col-1))

            # right 1 up 2
            if col < 7 and row > 1:
                free = is_square_empty(board, row-2, col+1, True, self.colour)
                if free: moves.append((row-2,col+1))

            # left 2 up 1 
            if col > 1 and row > 0:
                free = is_square_empty(board, row-1, col-2, True, self.colour)
                if free: moves.append((row-1,col-2))

            # right 2 up 1 
            if col < 6 and row > 0:
                free = is_square_empty(board, row-1, col+2, True, self.colour)
                if free: moves.append((row-1,col+2))

            # left 2 down 1
            if col > 1 and row < 7:
                free = is_square_empty(board, row+1, col-2, True, self.colour)
                if free: moves.append((row+1,col-2))

            # right 2 down 1 
            if col < 6 and row < 7:
                free = is_square_empty(board, row+1, col+2, True, self.colour)
                if free: moves.append((row+1,col+2))

            # left 1 down 2
            if col > 0 and row < 6:
                free = is_square_empty(board, row+2, col-1, True, self.colour)
                if free: moves.append((row+2,col-1))

            # right 1 down 2 
            if col < 7 and row < 6:
                free = is_square_empty(board, row+2, col+1, True, self.colour)
                if free: moves.append((row+2,col+1))

        if moves == []:
            moves = [(-1,-1)]
        return moves

class Bishop(Piece): 
    def __init__(self,screen=None, colour=None): 
        super(Bishop, self).__init__(screen, colour)
        self.image_white = pygame.transform.scale(pygame.image.load(f"./Images/{self.set}/white_bishop.png"), (self.img_width, self.img_height))
        self.image_black = pygame.transform.scale(pygame.image.load(f"./Images/{self.set}/black_bishop.png"), (self.img_width, self.img_height))
        self.icon_image_white = pygame.transform.scale(pygame.image.load(f"./Images/{self.set}/white_bishop.png"), (self.icon_width, self.icon_height))
        self.icon_image_black = pygame.transform.scale(pygame.image.load(f"./Images/{self.set}/black_bishop.png"), (self.icon_width, self.icon_height))
        self.name = "bishop"
        self.value = 3 

    def legal_moves(self,board, row,col,colour_moving): 
        moves = []
        if colour_moving == self.colour:
            
            # moving top right
            top_right_limit = False 
            moving = 1
            while not top_right_limit: 
                if row-moving < 0 or col+moving > 7: 
                    top_right_limit = True 
                    break 

                free = is_square_empty(board, row-moving, col+moving,False, self.colour)
                if free: moves.append((row-moving, col+moving))
                else: 
                    if board[row-moving][col+moving].colour != self.colour:
                        moves.append((row-moving, col+moving))
                    top_right_limit = True
                    break
                moving += 1 
            
            # moving top left
            top_left_limit = False 
            moving = 1
            while not top_left_limit: 
                if row-moving < 0 or col-moving < 0: 
                    top_left_limit = True 
                    break 

                free = is_square_empty(board, row-moving, col-moving,False, self.colour)
                if free: moves.append((row-moving, col-moving))
                else: 
                    if board[row-moving][col-moving].colour != self.colour:
                        moves.append((row-moving, col-moving))

                    top_left_limit = True
                    break
                moving += 1
            
            # moving bottom right
            bottom_right_limit = False 
            moving = 1
            while not bottom_right_limit: 
                if row+moving > 7 or col+moving >7 : 
                    bottom_right_limit = True 
                    break 

                free = is_square_empty(board, row+moving, col+moving,False, self.colour)
                if free: moves.append((row+moving, col+moving))
                else: 
                    if board[row+moving][col+moving].colour != self.colour:
                        moves.append((row+moving, col+moving))
                    bottom_right_limit = True
                    break
                moving += 1
            
            # moving bottom left
            bottom_left_limit = False 
            moving = 1
            while not bottom_left_limit: 
                if row+moving > 7 or col-moving < 0: 
                    bottom_left_limit = True 
                    break 

                free = is_square_empty(board, row+moving, col-moving,False, self.colour)
                if free: moves.append((row+moving, col-moving))
                else: 
                    if board[row+moving][col-moving].colour != self.colour:
                        moves.append((row+moving, col-moving))
                    bottom_left_limit = True
                    break
                moving += 1
        
        
        moves = filter_legal_moves_for_check(board,row,col,moves,colour_moving)
        if moves == []:
            moves = [(-1,-1)]
        return moves
    
    def controls(self,board, row,col,colour_moving): 
        moves = []
        if colour_moving == self.colour:
            # moving top right
            top_right_limit = False 
            moving = 1
            while not top_right_limit: 
                if row-moving < 0 or col+moving > 7: 
                    top_right_limit = True 
                    break 

                free = is_square_empty(board, row-moving, col+moving,False, self.colour)
                if free: moves.append((row-moving, col+moving))
                else: 
                    if board[row-moving][col+moving].colour != self.colour:
                        moves.append((row-moving, col+moving))
                    top_right_limit = True
                    break
                moving += 1 
            
            # moving top left
            top_left_limit = False 
            moving = 1
            while not top_left_limit: 
                if row-moving < 0 or col-moving < 0: 
                    top_left_limit = True 
                    break 

                free = is_square_empty(board, row-moving, col-moving,False, self.colour)
                if free: moves.append((row-moving, col-moving))
                else: 
                    if board[row-moving][col-moving].colour != self.colour:
                        moves.append((row-moving, col-moving))

                    top_left_limit = True
                    break
                moving += 1
            
            # moving bottom right
            bottom_right_limit = False 
            moving = 1
            while not bottom_right_limit: 
                if row+moving > 7 or col+moving >7 : 
                    bottom_right_limit = True 
                    break 

                free = is_square_empty(board, row+moving, col+moving,False, self.colour)
                if free: moves.append((row+moving, col+moving))
                else: 
                    if board[row+moving][col+moving].colour != self.colour:
                        moves.append((row+moving, col+moving))
                    bottom_right_limit = True
                    break
                moving += 1
            
            # moving bottom left
            bottom_left_limit = False 
            moving = 1
            while not bottom_left_limit: 
                if row+moving > 7 or col-moving < 0: 
                    bottom_left_limit = True 
                    break 

                free = is_square_empty(board, row+moving, col-moving,False, self.colour)
                if free: moves.append((row+moving, col-moving))
                else: 
                    if board[row+moving][col-moving].colour != self.colour:
                        moves.append((row+moving, col-moving))
                    bottom_left_limit = True
                    break
                moving += 1
        
        
        
        if moves == []:
            moves = [(-1,-1)]
        return moves

class King(Piece): 
    def __init__(self,screen, colour,is_inverted=False): 
        super(King, self).__init__(screen, colour)
        self.image_white = pygame.transform.scale(pygame.image.load(f"./Images/{self.set}/white_king.png"), (self.img_width, self.img_height))
        self.image_black = pygame.transform.scale(pygame.image.load(f"./Images/{self.set}/black_king.png"), (self.img_width, self.img_height))
        self.icon_image_white = pygame.transform.scale(pygame.image.load(f"./Images/{self.set}/white_king.png"), (self.icon_width, self.icon_height))
        self.icon_image_black = pygame.transform.scale(pygame.image.load(f"./Images/{self.set}/black_king.png"), (self.icon_width, self.icon_height))
        self.name = "king"
        self.moved = False 
        self.value = 10000 # infinite
        self.castled = False
        self.is_inverted = is_inverted
        self.colour = colour

    def legal_moves(self,board, row,col,colour_moving): 
        moves = []
        if colour_moving == "white":
    
            home = 7
            if self.is_inverted: 
                home = 0 
        else: 
            home = 0
            if self.is_inverted: 
                home = 7
        

        if colour_moving == self.colour:
            # up 1 
            if row > 0:
                free = is_square_empty(board,row-1,col,True,self.colour)
                if free: moves.append((row-1,col))
            
            # up 1 left 1 
            if row > 0 and col > 0:
                free = is_square_empty(board,row-1,col-1,True, self.colour)
                if free: moves.append((row-1,col-1))
            
            # up 1 right 1 
            if row > 0 and col < 7:
                free = is_square_empty(board,row-1,col+1,True,self.colour)
                if free: moves.append((row-1,col+1))
            
            # left 1
            if col > 0:
                free = is_square_empty(board,row,col-1,True,self.colour)
                if free: moves.append((row,col-1))
            
            # right 1 
            if col < 7: 
                free = is_square_empty(board,row,col+1, True, self.colour)
                if free: moves.append((row,col+1))
            
            # down 1 left 1 
            if row < 7 and col > 0: 
                free = is_square_empty(board,row+1, col-1,True, self.colour)
                if free: moves.append((row+1,col-1))
            
            # down 1 
            if row < 7: 
                free = is_square_empty(board,row+1,col, True,self.colour)
                if free: moves.append((row+1,col))
            
            # down 1 right 1 
            if row < 7 and col < 7:
                free = is_square_empty(board, row+1,col+1, True,self.colour)
                if free: moves.append((row+1,col+1))
        
        moves = filter_legal_moves_for_check(board,row,col,moves,colour_moving)
        # this is put before castling so that we can check if the king moves through check

        kingside_dir = 1
        king_starting_col = 4
        king_rook_col = 7
        queenside_dir = -1 
        queen_rook_col = 0
        if self.is_inverted: 
            kingside_dir = -1
            king_starting_col = 3 
            king_rook_col = 0
            queenside_dir = 1 
            queen_rook_col = 7

        print(is_in_check(board, colour_moving))

        # castling kingside
        if self.moved == False: # king hasn't moved
            if board[home][king_rook_col] != 0:
                if not is_in_check(board, colour_moving): 
                    if board[home][king_rook_col].name == "rook":
                        if board[home][king_rook_col].moved == False: # rook hasn't moved
                            if board[home][king_starting_col+kingside_dir] == 0 and board[home][king_starting_col+(2*kingside_dir)] == 0:# empty squares in between 
                                if (home,king_starting_col+kingside_dir) in moves: # makes sure the thing doesn't move thorugh check - already been checked.
                                    moves.append((home,king_starting_col+(2*kingside_dir)))

            
        # castling queenside
        if self.moved == False: # king hasn't moved
            if board[home][queen_rook_col] != 0:
                if not is_in_check(board, colour_moving): 

                    if board[home][queen_rook_col].name == "rook":
                        if board[home][queen_rook_col].moved == False: # if rook hasnt' move 
                            if board[home][king_starting_col+queenside_dir] == 0 and board[home][king_starting_col+(2*queenside_dir)] == 0 and board[home][king_starting_col+(3*queenside_dir)] == 0: # empty squares
                                if (home,king_starting_col+queenside_dir) in moves: # makes sure the thing doesn't move thorugh check - already been checked.
                                    moves.append((home,king_starting_col+(2*queenside_dir)))
            

        # so that you can't castle into check 
        moves = filter_legal_moves_for_check(board,row,col,moves,colour_moving)
                        
        if moves == []:
            moves = [(-1,-1)]
        return moves
    
    def controls(self,board, row,col,colour_moving): 
        moves = []
        if colour_moving == self.colour:
            # up 1 
            if row > 0: moves.append((row-1,col))
            
            # up 1 left 1 
            if row > 0 and col > 0: moves.append((row-1,col-1))
            
            # up 1 right 1 
            if row > 0 and col < 7: moves.append((row-1,col+1))
            
            # left 1
            if col > 0: moves.append((row,col-1))
            
            # right 1 
            if col < 7: moves.append((row,col+1))
            
            # down 1 left 1 
            if row < 7 and col > 0: moves.append((row+1,col-1))
            
            # down 1 
            if row < 7:  moves.append((row+1,col))
            
            # down 1 right 1 
            if row < 7 and col < 7: moves.append((row+1,col+1))

        if moves == []:
            moves = [(-1,-1)]
        return moves

class Queen(Piece): 
    def __init__(self,screen, colour): 
        super(Queen, self).__init__(screen, colour)
        self.image_white = pygame.transform.scale(pygame.image.load(f"./Images/{self.set}/white_queen.png"), (self.img_width, self.img_height))
        self.image_black = pygame.transform.scale(pygame.image.load(f"./Images/{self.set}/black_queen.png"), (self.img_width, self.img_height))
        self.icon_image_white = pygame.transform.scale(pygame.image.load(f"./Images/{self.set}/white_queen.png"), (self.icon_width, self.icon_height))
        self.icon_image_black = pygame.transform.scale(pygame.image.load(f"./Images/{self.set}/black_queen.png"), (self.icon_width, self.icon_height))
        self.name = "queen"
        self.value = 9 

    def legal_moves(self,board, row,col,colour_moving): 
        moves = []
        if colour_moving ==self.colour:
            rook_controls = Rook.controls
            bishop_controls = Bishop.controls
            bishop_moves = bishop_controls(self,board,row,col,colour_moving)
            rook_moves = rook_controls(self,board,row,col,colour_moving)


            for move in rook_moves: 
                if move != (-1,-1):
                    moves.append(move)
            
            for move in bishop_moves:
                if move != (-1,-1):
                    moves.append(move)
        moves = filter_legal_moves_for_check(board,row,col,moves,colour_moving)
        if moves == []:
            moves = [(-1,-1)]
        return moves
    
    def controls(self,board,row,col,colour_moving):
        moves = []
        rook_controls = Rook.controls
        bishop_controls = Bishop.controls
        bishop_moves = bishop_controls(self,board,row,col,colour_moving)
        rook_moves = rook_controls(self,board,row,col,colour_moving)


        for move in rook_moves: 
            if move != (-1,-1):
                moves.append(move)
        
        for move in bishop_moves:
            if move != (-1,-1):
                moves.append(move)
        
        if moves == []:
            moves = [(-1,-1)]
        return moves

class Rook(Piece): 
    def __init__(self,screen=None, colour=None): # so that we can decalre dummy verstions
        super(Rook, self).__init__(screen, colour)
        self.image_white = pygame.transform.scale(pygame.image.load(f"./Images/{self.set}/white_rook.png"), (self.img_width, self.img_height))
        self.image_black = pygame.transform.scale(pygame.image.load(f"./Images/{self.set}/black_rook.png"), (self.img_width, self.img_height))
        self.icon_image_white = pygame.transform.scale(pygame.image.load(f"./Images/{self.set}/white_rook.png"), (self.icon_width, self.icon_height))
        self.icon_image_black = pygame.transform.scale(pygame.image.load(f"./Images/{self.set}/black_rook.png"), (self.icon_width, self.icon_height))
        self.name = "rook"
        self.moved = False
        self.value = 5 

    def legal_moves(self,board, row,col,colour_moving): 
        moves = []

        if colour_moving == self.colour:
            # upwards
            up_limit = False
            moving = 1
            while not up_limit:
                if row-moving < 0:
                    up_limit = True
                    break 

                free = is_square_empty(board,row-moving,col,False,colour_moving)
                if free: moves.append((row-moving,col))
                else:
                    if board[row-moving][col].colour != self.colour:
                        moves.append((row-moving,col))
                    up_limit = True
                    break
                moving += 1
            
            # moving left
            left_limit = False 
            moving = 1
            while not left_limit:
                if col-moving < 0:
                    left_limit = True
                    break 

                free = is_square_empty(board,row,col-moving, False, colour_moving)
                if free: moves.append((row,col-moving))
                else:
                    if board[row][col-moving].colour != self.colour:
                        moves.append((row,col-moving))
                    left_limit = True
                    break 
                moving += 1
            
            # moving right
            right_limit = False
            moving = 1 
            while not right_limit:
                if col + moving > 7:
                    right_limit = True
                    break 
                
                free = is_square_empty(board,row,col+moving,False,colour_moving)
                if free: moves.append((row,col+moving))
                else: 
                    if board[row][col+moving].colour != self.colour:
                        moves.append((row,col+moving))
                    right_limit = True
                    break 
                moving += 1
              
            # moving down 
            down_limit = False 
            moving = 1 
            while not down_limit:
                if row + moving > 7:
                    down_limit = True
                    break 
                
                free = is_square_empty(board,row+moving,col,False,colour_moving)
                if free: moves.append((row+moving,col))
                else:
                    if board[row+moving][col].colour != self.colour:
                        moves.append((row+moving,col))
                    down_limit = True
                    break
                moving += 1
        moves = filter_legal_moves_for_check(board,row,col,moves,colour_moving)
        if moves == []:
            moves = [(-1,-1)]
        return moves
    
    def controls(self,board,row,col,colour_moving):
        moves = []

        if colour_moving == self.colour:
            # upwards
            up_limit = False
            moving = 1
            while not up_limit:
                if row-moving < 0:
                    up_limit = True
                    break 

                free = is_square_empty(board,row-moving,col,False,colour_moving)
                if free: moves.append((row-moving,col))
                else:
                    if board[row-moving][col].colour != self.colour:
                        moves.append((row-moving,col))
                    up_limit = True
                    break
                moving += 1
            
            # moving left
            left_limit = False 
            moving = 1
            while not left_limit:
                if col-moving < 0:
                    left_limit = True
                    break 

                free = is_square_empty(board,row,col-moving, False, colour_moving)
                if free: moves.append((row,col-moving))
                else:
                    if board[row][col-moving].colour != self.colour:
                        moves.append((row,col-moving))
                    left_limit = True
                    break 
                moving += 1
            
            # moving right
            right_limit = False
            moving = 1 
            while not right_limit:
                if col + moving > 7:
                    right_limit = True
                    break 
                
                free = is_square_empty(board,row,col+moving,False,colour_moving)
                if free: moves.append((row,col+moving))
                else: 
                    if board[row][col+moving].colour != self.colour:
                        moves.append((row,col+moving))
                    right_limit = True
                    break 
                moving += 1
              
            # moving down 
            down_limit = False 
            moving = 1 
            while not down_limit:
                if row + moving > 7:
                    down_limit = True
                    break 

                free = is_square_empty(board,row+moving,col,False,colour_moving)
                if free: moves.append((row+moving,col))
                else:
                    if board[row+moving][col].colour != self.colour:
                        moves.append((row+moving,col))
                    down_limit = True
                    break
                moving += 1
    
        if moves == []:
            moves = [(-1,-1)]
        return moves




from random import choice
from piece import Pawn, Knight, Bishop, King, Queen, Rook, is_in_check,find_king_pos, is_in_checkmate_or_stalemate
import pygame 

def return_all_legal_moves(board, colour="black"):
    
    valid = []
    for i in range(8):
        for j in range(8):
            piece = board[i][j]
            if piece != 0:
                if piece.colour == colour:
                    moves = piece.legal_moves(board,i,j,colour)
                    for move in moves:
                        if move != (-1,-1):
                            valid.append([i,j,move[0],move[1]])
    return valid 
            
def return_random_ai_move(board, colour="black"):
    valid = return_all_legal_moves(board, colour)

    if valid != []:
        move = choice(valid)
        return move[0],move[1],move[2],move[3]
    return -1,-1,-1,-1

def make_move(editing_board, from_row,from_col,to_row,to_col):
    editing_board[to_row][to_col] = editing_board[from_row][from_col]
    editing_board[from_row][from_col] = 0 
    return editing_board 
        
            
class Search_Tree_bot: 
    def return_position_value(self,board): 
        white_points = 0 
        black_points = 0 
        white_central_squares_controlled = 0 
        black_central_squares_controlled = 0 
        total_white_squares_controlled = 0 
        total_black_squares_controlled = 0 
        white_castled = 0 
        black_castled = 0 
        central_squares = [(3,3),(3,4),(4,3),(4,4)]


        for i in range(8): 
            for j in range(8): 
                if board[i][j] != 0: 
                    if board[i][j].name == "king": 
                        if board[i][j].castled: 
                            if board[i][j].colour == "white":
                                white_castled = 1 
                            else: 
                                black_castled = 1 
                        
                    controls = board[i][j].controls(board,i,j,board[i][j].colour)
                    for square in controls: 
                        if square in central_squares:
                            if board[i][j].colour == "white": 
                                white_central_squares_controlled += 1
                            else:
                                black_central_squares_controlled += 1
                        if board[i][j].colour == "white": 
                            total_white_squares_controlled += 1
                        else:
                            total_black_squares_controlled += 1
                            
                    if board[i][j].colour == "white": 
                        white_points += board[i][j].value 
                    else:
                        black_points += board[i][j].value 
        


                    
        
        direct_point_difference = white_points - black_points 
        central_squares_controlled_difference = white_central_squares_controlled - black_central_squares_controlled
        total_squares_controlled_difference = total_white_squares_controlled - total_black_squares_controlled
        castling_difference = white_castled - black_castled
        
        # print(f"castling difference:{castling_difference}") 
        

        total_evaluation = (1*direct_point_difference)  + (central_squares_controlled_difference*0.01) #+ (total_squares_controlled_difference*0.001)
        # total_evaluation -= black_castled*1000
        return round(total_evaluation,4)
    


    
    def minimax(self,board, depth, maximising_player, eval_strength):
        if depth == 0 or is_in_checkmate_or_stalemate(board, "white") or is_in_checkmate_or_stalemate(board, "black"): # base case 
            return None, self.return_position_value(board)

        
        
        if maximising_player: # for white moving 
            max_eval = -1000000
            whites_moves = return_all_legal_moves(board, "white")
            best_move = choice(whites_moves)
            for move in whites_moves: 
                editing_board = list(map(list, board))
                editing_board = make_move(editing_board, move[0], move[1], move[2], move[3])
                _, eval = self.minimax(editing_board, depth-1, False, eval_strength)
                if eval > max_eval: 
                    max_eval = eval 
                    best_move = move

            return best_move, max_eval 

        else: 
            min_eval = 1000000
            black_moves = return_all_legal_moves(board, "black")
            best_move = choice(black_moves)
            for move in black_moves: 
                editing_board = list(map(list, board))
                editing_board = make_move(editing_board, move[0], move[1], move[2], move[3])
                _, eval = self.minimax(editing_board,depth-1, True, eval_strength)
                if eval < min_eval: 
                    min_eval = eval 
                    best_move = move



            return best_move, min_eval
    
    def return_best_move(board): 
        pass


# x = Search_Tree_bot()
# x.is_known_position(1)
        

 # adds the total value of position after each move, chooses randomly between the moves that all have the highest value
# class Material_Bot: 
#     def return_position_value(self,board, colour="black"): 
#         white_points = 0 
#         black_points = 0 
#         for i in range(8): 
#             for j in range(8): 
#                 if board[i][j] != 0: 
#                     if board[i][j].colour == "white": 
#                         white_points += board[i][j].value 
#                     else:
#                         black_points += board[i][j].value 
        
#         return white_points - black_points
    
#     def return_best_move(self,board,colour="black",depth=1): 
#         legal_moves = return_all_legal_moves(board,colour)
#         # legal_moves = []
#         max_value = 1000
#         best_moves = []
#         for move in legal_moves: 
#             editing_board = list(map(list, board)) 
#             editing_board = make_move(editing_board, move[0], move[1], move[2], move[3])
#             value_after_one_move = self.return_position_value(editing_board)
            
            
#             if value_after_one_move < max_value: 
#                 best_moves = move
#                 max_value = value_after_one_move 
#             elif value_after_one_move == max_value: 
#                 best_moves.append(move)

#         if best_moves == []:
#             return -1,-1,-1,-1
#         if depth == 1:
#             best = choice(best_moves)
#             return best[0],best[1],best[2],best[3]



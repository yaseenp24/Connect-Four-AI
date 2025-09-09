import connectfour
 
def make_board(game_state):
    '''
    This function makes the board by inputting
    R's and Y's in places where a move has been 
    made, or .'s in a place that hasn't been made
    it allows the board to know whats been played
    '''
    for row in range(connectfour.rows(game_state)):
            row_str = ""
            for col in range(connectfour.columns(game_state)):
                cell = game_state.board[col][row]
                if cell == 1:
                    row_str += "R "
                elif cell == 2:
                    row_str += "Y "
                else:
                    row_str += ". "
            print(row_str)
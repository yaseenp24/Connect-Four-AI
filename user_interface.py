from shared import make_board
from connectfour import GameState, InvalidMoveError, GameOverError, new_game, columns, rows, drop, pop, winner, MIN_COLUMNS, MAX_COLUMNS, MIN_ROWS, MAX_ROWS

def check(game_state):
    '''
    This function receives the move from the user and determines
    whether its a drop or a pop command
    '''
    while True:
        column = input(f"Enter the column to make a move (1-{columns(game_state)}): ")
        if column[0] == 'P': 
            column = int(column[4:]) - 1 
            game_state = pop(game_state, column)
            break
        if column[0] == "D": 
            column = int(column[5:]) - 1 
            game_state = drop(game_state, column) 
            break
        else:
            continue
    return column, game_state 

def size():
    '''
    This function determines the size of the board
    by asking the user to enter the number of rows
    and columns
    '''
    while True:
        columns_input = int(input("Enter the number of columns (4-20): "))
        rows_input = int(input("Enter the number of rows (4-20): "))
        if columns_input < MIN_COLUMNS or columns_input > MAX_COLUMNS:
            print("Invalid") 
            continue
        if rows_input < MIN_ROWS or rows_input > MAX_ROWS:
            print("Invalid")
            continue
        else:
            break 
    return columns_input, rows_input

def main():
    '''
    This function is the first entry to start the game of 
    server/client interaction
    '''
    columns_input, rows_input = size()

    game_state = new_game(columns_input, rows_input)
    print("Connect Four Game Created!")

    while True: 
        try: 
            print(f"Current player: {'RED' if game_state.turn == 1 else 'YELLOW'}")
            print("Current game board:")           
            column_numbers = " ".join(str(i) for i in range(1, columns(game_state) + 1))
            print(column_numbers) 
            make_board(game_state)
            column, game_state = check(game_state)
            if not (0 <= column < columns(game_state)):
                print("Invalid column number. Please enter a valid column.")
                continue 
            if winner(game_state) != 0:
                print("Current game board:")
                column_numbers = " ".join(str(i) for i in range(1, columns(game_state) + 1))
                print(column_numbers) 
                make_board(game_state) 

                print(f"Player {'RED' if winner(game_state) == 1 else 'YELLOW'} wins!")
                break
        except (ValueError, InvalidMoveError):
            print("Invalid move. Try again.")
        except GameOverError:
            print("The game is over. It's a draw!")

if __name__ == "__main__":
    main()

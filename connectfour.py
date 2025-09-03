from collections import namedtuple
 
EMPTY = 0
RED = 1
YELLOW = 2

MIN_COLUMNS = 4
MAX_COLUMNS = 20

MIN_ROWS = 4
MAX_ROWS = 20

GameState = namedtuple('GameState', ['board', 'turn'])

class InvalidMoveError(Exception):
    '''Raised whenever an invalid move is made'''
    pass



class GameOverError(Exception):

    pass



def new_game(columns: int, rows: int) -> GameState:

    _require_valid_column_count(columns)
    _require_valid_row_count(rows)

    return GameState(board = _new_game_board(columns, rows), turn = RED)



def columns(game_state: GameState) -> int:

    return _board_columns(game_state.board)



def rows(game_state: GameState) -> int:

    return _board_rows(game_state.board)



def drop(game_state: GameState, column_number: int) -> GameState:

    _require_valid_column_number(column_number, game_state.board)
    _require_game_not_over(game_state)

    empty_row = _find_bottom_empty_row_in_column(game_state.board, column_number)

    if empty_row == -1:
        raise InvalidMoveError()

    else:
        new_board = _copy_game_board(game_state.board)
        new_board[column_number][empty_row] = game_state.turn
        new_turn = _opposite_turn(game_state.turn)
        return GameState(board = new_board, turn = new_turn)



def pop(game_state: GameState, column_number: int) -> GameState:

    _require_valid_column_number(column_number, game_state.board)
    _require_game_not_over(game_state)

    if game_state.turn == game_state.board[column_number][rows(game_state) - 1]:
        new_board = _copy_game_board(game_state.board)

        for row in range(rows(game_state) - 1, -1, -1):
            new_board[column_number][row] = new_board[column_number][row - 1]

        new_board[column_number][row] = EMPTY

        new_turn = _opposite_turn(game_state.turn)

        return GameState(board = new_board, turn = new_turn)

    else:
        raise InvalidMoveError()



def winner(game_state: GameState) -> int:

    winner = EMPTY
    
    for col in range(columns(game_state)):
        for row in range(rows(game_state)):
            if _winning_sequence_begins_at(game_state.board, col, row):
                if winner == EMPTY:
                    winner = game_state.board[col][row]
                elif winner != game_state.board[col][row]:
                    # This handles the rare case of popping a piece
                    # causing both players to have four in a row;
                    # in that case, the last player to make a move
                    # is the winner.
                    return _opposite_turn(game_state.turn)

    return winner
    
def _new_game_board(columns: int, rows: int) -> list[list[int]]:

    board = []

    for col in range(columns):
        board.append([])
        for row in range(rows):
            board[-1].append(EMPTY)

    return board



def _board_columns(board: list[list[int]]) -> int:
    return len(board)



def _board_rows(board: list[list[int]]) -> int:
    return len(board[0])



def _copy_game_board(board: list[list[int]]) -> list[list[int]]:
    board_copy = []

    for col in range(_board_columns(board)):
        board_copy.append([])
        for row in range(_board_rows(board)):
            board_copy[-1].append(board[col][row])

    return board_copy



def _find_bottom_empty_row_in_column(board: list[list[int]], column_number: int) -> int:

    for i in range(_board_rows(board) - 1, -1, -1):
        if board[column_number][i] == EMPTY:
            return i

    return -1



def _opposite_turn(turn: int) -> int:
    if turn == RED:
        return YELLOW
    else:
        return RED 



def _winning_sequence_begins_at(board: list[list[int]], col: int, row: int) -> bool:

    return _four_in_a_row(board, col, row, 0, 1) \
            or _four_in_a_row(board, col, row, 1, 1) \
            or _four_in_a_row(board, col, row, 1, 0) \
            or _four_in_a_row(board, col, row, 1, -1) \
            or _four_in_a_row(board, col, row, 0, -1) \
            or _four_in_a_row(board, col, row, -1, -1) \
            or _four_in_a_row(board, col, row, -1, 0) \
            or _four_in_a_row(board, col, row, -1, 1)
    


def _four_in_a_row(board: list[list[int]], col: int, row: int, coldelta: int, rowdelta: int) -> bool:

    start_cell = board[col][row]

    if start_cell == EMPTY:
        return False
    else:
        for i in range(1, 4):
            if not _is_valid_column_number(col + coldelta * i, board) \
                    or not _is_valid_row_number(row + rowdelta * i, board) \
                    or board[col + coldelta *i][row + rowdelta * i] != start_cell:
                return False
        return True
    


def _require_valid_column_number(column_number: int, board: list[list[int]]) -> None:
    if type(column_number) != int or not _is_valid_column_number(column_number, board):
        raise ValueError(f'column_number must be an int between 0 and {_board_columns(board) - 1}')



def _require_game_not_over(game_state: GameState) -> None:

    if winner(game_state) != EMPTY:
        raise GameOverError()



def _is_valid_column_number(column_number: int, board: list[list[int]]) -> bool:
    return 0 <= column_number < _board_columns(board)



def _is_valid_row_number(row_number: int, board: list[list[int]]) -> bool:
    return 0 <= row_number < _board_rows(board)


def _require_valid_column_count(columns: int) -> None:
    if not MIN_COLUMNS <= columns <= MAX_COLUMNS:
        raise ValueError(f'columns must be an int between {MIN_COLUMNS} and {MAX_COLUMNS}')


def _require_valid_row_count(rows: int) -> None:
    if not MIN_ROWS <= rows <= MAX_ROWS:
        raise ValueError(f'rows must be an intbetween {MIN_ROWS} and {MAX_ROWS}')

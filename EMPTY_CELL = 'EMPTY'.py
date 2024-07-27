EMPTY_CELL = 'EMPTY'
FALLER_MOVING_CELL = 'FALLER_MOVING'
FALLER_STOPPED_CELL = 'FALLER_STOPPED STATE'
OCCUPIED = 'OCCUPIED STATE'
MATCHED_CELL = 'MATCHED STATE'

LEFT = -1
RIGHT = 1
DOWN = 0
DOWN_LEFT = 2

NONE = 'NONE'
EMPTY = ' '
S = 'S'
T = 'T'
V = 'V'
W = 'W'
X = 'X'
Y = 'Y'
Z = 'Z'


def make_board(rows, cols):
    board_rows = []
    pieces = []
    for i in range(rows):
        row = []
        row_pieces = []
        for j in range(cols):
            row.append(EMPTY)
            row_pieces.append(EMPTY_CELL)
        board_rows.append(row)
        pieces.append(row_pieces)
    return board_rows, pieces


def init_board(board, contents):
    for row in range(len(contents)):
        for col in range(len(contents[row])):
            value = contents[row][col]
            if value is EMPTY:
                set_cell(board, row, col, EMPTY, EMPTY_CELL)
            else:
                set_cell(board, row, col, value, OCCUPIED)

    time_grav(board)
    matching(board)


def time(board):
    if board['faller']['active']:
        if board['faller']['is_moving']:
            check_faller(board)
        if not board['faller']['is_moving']:
            value = False
            if board['faller']['row'] - 2 < 0:
                value = True
            for i in range(3):
                set_cell(board, board['faller']['row'] - i, board['faller']['col'], board['faller']['contents'][i],
                         OCCUPIED)
            board['faller']['active'] = False
            matching(board)
            return value

        fall_down(board)
        check_faller(board)
    matching(board)
    return False


def spawn(board, column, faller):
    if board['faller']['active']:
        return

    board['faller']['active'] = True
    board['faller']['contents'] = faller
    board['faller']['row'] = 0
    board['faller']['col'] = column - 1
    set_cell(board, 0, board['faller']['col'], board['faller']['contents'][0], FALLER_MOVING_CELL)
    board['lastfallerposition'] = (board['faller']['row'], board['faller']['col'])
    check_faller(board)


def rotate(board):
    if not board['faller']['active']:
        return

    one = board['faller']['contents'][0]
    two = board['faller']['contents'][1]
    three = board['faller']['contents'][2]

    board['faller']['contents'] = [two, three, one]
    for i in range(3):
        set_cell_contents(board, board['faller']['row'] - i, board['faller']['col'], board['faller']['contents'][i])
    check_faller(board)


def move_hor(board, direction):
    if not board['faller']['active']:
        return

    if not direction == RIGHT and not direction == LEFT:
        return

    if (direction == LEFT and board['faller']['col'] == 0) or (
            direction == RIGHT and board['faller']['col'] == len(board['boardRows'][0]) - 1):
        return

    targetColumn = board['faller']['col'] + direction
    for i in range(3):
        if board['faller']['row'] - i < 0:
            break

        if board['pieces'][board['faller']['row'] - i][targetColumn] == OCCUPIED:
            return

    for i in range(3):
        if board['faller']['row'] - i < 0:
            break
        move(board, board['faller']['row'] - i, board['faller']['col'], direction)

    board['faller']['col'] = targetColumn
    check_faller(board)
    removelastfaller(board)
    board['lastfallerposition'] = (board['faller']['row'], board['faller']['col'])


def set_cell(board, row, col, contents, state):
    if row < 0:
        return
    set_cell_contents(board, row, col, contents)
    set_cell_state(board, row, col, state)


def set_cell_contents(board, row, col, contents):
    if row < 0:
        return
    board['boardRows'][row][col] = contents


def set_cell_state(board, row, col, state):
    if row < 0:
        return
    board['pieces'][row][col] = state


def time_grav(board):
    for col in range(len(board['boardRows'][0])):
        for row in range(len(board['boardRows']) - 1, -1, -1):
            state = board['pieces'][row][col]
            if state == FALLER_MOVING_CELL or state == FALLER_STOPPED_CELL:
                continue
            if state == OCCUPIED:
                i = 1
                while not ((row + i) >= len(board['boardRows']) or board['pieces'][row + i][col] == OCCUPIED):
                    move(board, row + i - 1, col, DOWN)
                    i += 1


def matching(board):
    for row in range(len(board['boardRows'])):
        for col in range(len(board['boardRows'][0])):
            if board['pieces'][row][col] == MATCHED_CELL:
                set_cell(board, row, col, EMPTY, EMPTY_CELL)
    time_grav(board)
    check_ver_ax(board)
    check_hor_ax(board)
    check_diag(board)


def check_ver_ax(board):
    for currentRow in range(len(board['boardRows']) - 1, -1, -1):
        matches = 0
        gem = NONE
        for col in range(0, len(board['boardRows'][0])):
            contents = board['boardRows'][currentRow][col]
            state = board['pieces'][currentRow][col]
            cellMatches = (contents == gem and (state == OCCUPIED or state == MATCHED_CELL))
            if cellMatches:
                matches += 1
            if col == len(board['boardRows'][0]) - 1:
                if matches >= 3:
                    if cellMatches:
                        match_pieces(board, currentRow, col, LEFT, matches)
                    else:
                        match_pieces(board, currentRow, col - 1, LEFT, matches)
            elif not cellMatches:
                if matches >= 3:
                    match_pieces(board, currentRow, col - 1, LEFT, matches)

                if state == OCCUPIED or state == MATCHED_CELL:
                    gem = contents
                    matches = 1
                else:
                    gem = NONE
                    matches = 1


def check_hor_ax(board):
    for currentCol in range(0, len(board['boardRows'][0])):
        matches = 0
        gem = NONE
        for row in range(len(board['boardRows']) - 1, -1, -1):
            contents = board['boardRows'][row][currentCol]
            state = board['pieces'][row][currentCol]
            cellMatches = (contents == gem and (state == OCCUPIED or state == MATCHED_CELL))
            if cellMatches:
                matches += 1

            if row == 0:
                if matches >= 3:
                    if cellMatches:
                        match_pieces(board, row, currentCol, DOWN, matches)
                    else:
                        match_pieces(board, row + 1, currentCol, DOWN, matches)
            elif not cellMatches:
                if matches >= 3:
                    match_pieces(board, row + 1, currentCol, DOWN, matches)

                if state == OCCUPIED or state == MATCHED_CELL:
                    gem = contents
                    matches = 1
                else:
                    gem = NONE
                    matches = 1


def check_diag(board):
    for currentRow in range(len(board['boardRows']) - 1, -1, -1):
        for currentCol in range(0, len(board['boardRows'][0])):
            matches = 0
            gem = NONE
            rowCounter = 0
            colCounter = 0
            while True:
                row = currentRow - rowCounter
                col = currentCol + colCounter

                contents = board['boardRows'][row][col]
                state = board['pieces'][row][col]
                cellMatches = (contents == gem and (state == OCCUPIED or state == MATCHED_CELL))

                if cellMatches:
                    matches += 1

                if col == len(board['boardRows'][0]) - 1 or row == 0:
                    if matches >= 3:
                        if cellMatches:
                            match_pieces(board, row, col, DOWN_LEFT, matches)
                        else:
                            match_pieces(board, row + 1, col - 1, DOWN_LEFT, matches)
                elif not cellMatches:
                    if matches >= 3:
                        match_pieces(board, row + 1, col - 1, DOWN_LEFT, matches)

                    if state == OCCUPIED or state == MATCHED_CELL:
                        gem = contents
                        matches = 1
                    else:
                        gem = NONE
                        matches = 1

                rowCounter += 1
                colCounter += 1

                if currentRow - rowCounter < 0 or currentCol + colCounter >= len(board['boardRows'][0]):
                    break


def match_pieces(board, row, col, direction, amount):
    if direction == LEFT:
        for targetCol in range(col, col - amount, -1):
            set_cell_state(board, row, targetCol, MATCHED_CELL)
    elif direction == DOWN:
        for targetRow in range(row, row + amount):
            set_cell_state(board, targetRow, col, MATCHED_CELL)
    elif direction == DOWN_LEFT:
        for i in range(amount):
            set_cell_state(board, row + i, col - i, MATCHED_CELL)


def check_faller(board):
    targetRow = board['faller']['row'] + 1
    if targetRow >= len(board['boardRows']) or board['pieces'][targetRow][board['faller']['col']] == OCCUPIED:
        state = FALLER_STOPPED_CELL
        board['faller']['is_moving'] = False
    else:
        state = FALLER_MOVING_CELL
        board['faller']['is_moving'] = True

    for i in range(3):
        row = board['faller']['row'] - i
        if row < 0:
            return
        set_cell(board, row, board['faller']['col'], board['faller']['contents'][i], state)


def fall_down(board):
    if board['faller']['row'] + 1 >= len(board['boardRows']) or \
            board['pieces'][board['faller']['row'] + 1][board['faller']['col']] == OCCUPIED:
        return

    move(board, board['faller']['row'], board['faller']['col'], DOWN)
    if board['faller']['row'] - 1 >= 0:
        move(board, board['faller']['row'] - 1, board['faller']['col'], DOWN)
        if board['faller']['row'] - 2 >= 0:
            move(board, board['faller']['row'] - 2, board['faller']['col'], DOWN)
        else:
            set_cell(board, board['faller']['row'] - 1, board['faller']['col'], board['faller']['contents'][2],
                     FALLER_MOVING_CELL)
    else:
        set_cell(board, board['faller']['row'], board['faller']['col'], board['faller']['contents'][1],
                 FALLER_MOVING_CELL)
    board['faller']['row'] = board['faller']['row'] + 1
    removelastfaller(board)
    board['lastfallerposition'] = (board['faller']['row'], board['faller']['col'])


def move(board, row, col, direction):
    old_val = board['boardRows'][row][col]
    old_status = board['pieces'][row][col]

    board['boardRows'][row][col] = EMPTY
    board['pieces'][row][col] = EMPTY_CELL

    if direction == DOWN:
        targetRow = row + 1
        board['boardRows'][targetRow][col] = old_val
        board['pieces'][targetRow][col] = old_status
    else:
        targetCol = col + direction
        board['boardRows'][row][targetCol] = old_val
        board['pieces'][row][targetCol] = old_status


def removelastfaller(board):
    row, col = board['lastfallerposition']
    resetcell(board, row, col)
    if row > 0:
        resetcell(board, row - 1, col)
    if row > 1:
        resetcell(board, row - 2, col)


def resetcell(board, row, col):
    set_cell(board, row, col, ' ', EMPTY_CELL)


if __name__ == '__main__':
    rows = int(input())
    cols = int(input())
    game_board = make_board(rows, cols)

    line = input().strip()
    if line == 'CONTENTS':
        row_list = []
        for i in range(rows):
            row = []
            line = input()
            for index in range(cols):
                row.append(line[index])
            row_list.append(row)
        init_board(game_board, row_list)

    while True:
        show(game_board)
        line = input().strip()
        if line == 'Q':
            break
        if line == '':
            if time(game_board):
                show(game_board)
                break
        else:
            get_input(line, game_board)

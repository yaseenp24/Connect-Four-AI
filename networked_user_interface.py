from connectfour import new_game, columns, rows, drop, pop, winner, GameState, InvalidMoveError, GameOverError
from network_handling import read_host, read_port, send_message, read_message, connect, receive_response, print_response, close
from shared import make_board

def check_move(message, game_state):
    '''
    This function receives the move from the user and determines
    whether its a drop or a pop command    
    '''
    if message[0] == "P":
        column = int(message[4:]) - 1
        game_state = pop(game_state, column)
    else:
        column = int(message[5:]) - 1
        game_state = drop(game_state, column)
    return column, game_state 

def receive_and_print_message(message, connection):
    '''
    This function receives messages from the user, sends it to 
    the server to receive a response
    '''
    send_message(connection, message)
    response = receive_response(connection)
    print_response(response)
    return response

def connect_to_server(host, port):
    '''
    This function takes in the host and port number and 
    determines whether it is the right host and port, if
    so, it connects to it
    '''
    print(f'Connecting to {host} (port {port}) ...')
    connection = connect(host, port)
    print('Connected!')
    return connection

def initialize_game(connection):
    '''
    This function initializes the game by checking if the
    first message is using the same protocol as the server
    '''
    while True:
        message = read_message()
        if message[0:13] == "I32CFSP_HELLO":
            response = receive_and_print_message(message, connection)
            if response == "ERROR":
                break
        else:
            print("Invalid")
            continue

        message = read_message()
        if message[0:7] == "AI_GAME":
            response = receive_and_print_message(message, connection)
            if response == "ERROR":
                break
            break
    
    row = int(message[8:10]) 
    column = int(message[10:])
    game_state = new_game(column, row)
    print("Connect Four Game Created!")
    return game_state

def main() -> None:
    '''
    This function is the first entry to start the game of 
    server/client interaction
    '''

    host = read_host()
    port = read_port()

    connection = connect_to_server(host, port)
    game_state = initialize_game(connection)

    while True:
        try:
            print(f"Current player: RED")
            print("Current game board:")
            column_numbers = " ".join(str(i) for i in range(1, columns(game_state) + 1))
            print(column_numbers)
            make_board(game_state)
            message = read_message()

            if message == '':
                break
            else:
                column, game_state = check_move(message, game_state)
                response = receive_and_print_message(message, connection)

                if response == "OKAY":
                    second_response = receive_response(connection)
                    print(second_response)
                    response = receive_response(connection)
                    print(response)

                    if second_response[0] == "P":
                        second_response = int(second_response[4:]) - 1
                        game_state = pop(game_state, second_response)
                    else:
                        second_response = int(second_response[5:]) - 1
                        game_state = drop(game_state, second_response)

                if response == "INVALID":
                    response = receive_response(connection)
                    print(response)
                    print("Y")
                    second_response = receive_response(connection)
                    print(second_response)
                    break

                if response in ("WINNER_RED", "WINNER_YELLOW", "ERROR"):
                    make_board(game_state)
                    break

        except (ValueError, InvalidMoveError):
            print("INVALID")
            break
        except GameOverError:
            print("The game is over.")
            break

    print('Closing connection...')
    close(connection)
    print('Closed!')

if __name__ == '__main__':
    main()

import socket
from typing import List
def read_host() -> str:
    '''
    This function reads the host connection  
    '''

    while True:
        host = input('Host: ').strip()

        if host == '':
            print('Please specify a host (either a name or an IP address)')
        else:
            return host
 
def read_port() -> int:
    '''
    This function reads the port number 
    '''
    while True:
        try:
            port = int(input('Port: ').strip())

            if 1 <= port <= 65535:
                return port

        except ValueError:
            pass
        
        print('Ports must be an integer between 1 and 65535')

def read_message() -> str:
    '''
    This function reads the message from the user
    '''
    return input('Message: ')

def print_response(response: str) -> None:
    '''
    This function prints the response from the server
    '''
    print('Response: ')
    print(response)

def connect(host: str, port: int) -> 'connection':
    '''
    This function connects to the host and port and determines 
    if they are valid entry points
    '''
    echo_socket = socket.socket()
    echo_socket.connect((host, port))
    echo_socket_input = echo_socket.makefile('r')
    echo_socket_output = echo_socket.makefile('w')

    return echo_socket, echo_socket_input, echo_socket_output

def close(connection: 'connection') -> None:
    '''
    This function closes the connection to the server
    once the program is complete
    '''
    echo_socket, echo_socket_input, echo_socket_output = connection
    echo_socket_input.close()
    echo_socket_output.close()
    echo_socket.close()

def send_message(connection: 'connection', message: str) -> None:
    '''
    This function sends a message from the user to the server
    '''
    echo_socket, echo_socket_input, echo_socket_output = connection
    echo_socket_output.write(message + '\r\n')
    echo_socket_output.flush()

def receive_response(connection: 'connection') -> None:
    '''
    This function receives the response from the server
    '''
    echo_socket, echo_socket_input, echo_socket_output = connection
    return echo_socket_input.readline()[:-1]


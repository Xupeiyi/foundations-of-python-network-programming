import socket
from argparse import ArgumentParser


def server(address):
    listening_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listening_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listening_socket.bind(address)
    listening_socket.listen(1)
    print('Run this script in another window with "-c" to connect')
    print(f'Listening at {listening_socket.getsockname()}')
    
    connected_socket, sockname = listening_socket.accept()
    print(f'Accepted connection from {sockname}')
    connected_socket.shutdown(socket.SHUT_WR)
    message = b''
    while True:
        more = connected_socket.recv(8192)  # arbitrary value of 8k
        if not more:  # socket has closed when recv returns ''
            print('Received zero bytes - end of file')
            break
        print(f'Received {len(more)} bytes')
        message += more
    print('Message:\n')
    print(message.decode('ascii'))
    connected_socket.close()
    
    listening_socket.close()


def client(address):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(address)
    client_socket.shutdown(socket.SHUT_RD)
    client_socket.sendall(b'Beautiful is better than ugly.\n')
    client_socket.sendall(b'Explicit is better than implicit.\n')
    client_socket.sendall(b'Simple is better than complex.\n')
    client_socket.close()


if __name__ == '__main__':
    parser = ArgumentParser(description="Transmit & receive a data stream")
    parser.add_argument('hostname', nargs='?', default='127.0.0.1', 
                        help='IP address or hostname (default: %(default)s)')
    parser.add_argument('-c', action='store_true', help='run as the client')
    parser.add_argument('-p', metavar='PORT', type=int, default=1060, 
                        help='TCP port number (default: %(default)s)')
    args = parser.parse_args()
    function = client if args.c else server
    function((args.hostname, args.p))

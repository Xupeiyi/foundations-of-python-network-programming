import socket, struct
from argparse import ArgumentParser

header_struct = struct.Struct("!I")  # big-endian unsigned int. 
                                     # messages up to 2**32 - 1 in length


def put_block(sock, message):
    block_length = len(message)
    sock.send(header_struct.pack(block_length))
    sock.send(message)


def recvall(sock, length):
    blocks = []
    while length:
        block = sock.recv(length)
        if not block:
            raise EOFError(f"Socket closed with {length} bytes left in this block")
        length -= len(block)
        blocks.append(block)
    return b"".join(blocks)


def get_block(sock):
    block_length_data = recvall(sock, header_struct.size)
    (block_length,) = header_struct.unpack(block_length_data)
    return recvall(sock, block_length)


def server(address):
    listening_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listening_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listening_socket.bind(address)
    listening_socket.listen(1)
    print("Run this script in another window with '-c' to connect")
    print(f'Listening at {listening_socket.getsockname()}')
    
    connected_socket, client_socket_name = listening_socket.accept()
    print(f'Accepted connection from {client_socket_name}')
    connected_socket.shutdown(socket.SHUT_WR)
    while True:
        block = get_block(connected_socket)
        if not block:
            break
        print(f"Block says: {repr(block)}")
    connected_socket.close()
    
    listening_socket.close()


def client(address):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(address)
    client_socket.shutdown(socket.SHUT_RD)

    put_block(client_socket, b"Beautiful is better than ugly.\n")
    put_block(client_socket, b"Explicit is better than implicit.\n")
    put_block(client_socket, b"Simple is better than complex.\n")
    put_block(client_socket, b"")
    client_socket.close()


if __name__ == "__main__":
    parser = ArgumentParser(description='Transmit & receive blocks over TCP')
    parser.add_argument('hostname', nargs='?', default='127.0.0.1',
                        help='IP address or hostname (default: %(default)s)')
    parser.add_argument('-c', action='store_true', help='run as the client')
    parser.add_argument('-p', type=int, metavar='port', default=1060,
                        help='TCP port number (default: %(default)s)')
    args = parser.parse_args()
    function = client if args.c else server
    function((args.hostname, args.p))
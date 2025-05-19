import argparse, socket


def recvall(sock, length):
    # recv() may return less than the requested number of bytes
    # so we need to loop until we have all the data.
    # The logic is similar to the sendall() method. 
    # But the standard library does not know the exact length of the data 
    # and does not provide a recvall() method
    data = b""
    while len(data) < length:
        more = sock.recv(length - len(data))
        if not more:
            raise EOFError(
                f"Socket was expecting to have {length} bytes, "
                f"but got {len(data)} before it closed"
            )
        data += more
    return data


def server(interface, port):
    listening_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listening_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listening_socket.bind((interface, port))

    # once listen() is called, the socket can only be used to receive connections 
    # and not to send or receive data
    listening_socket.listen(1)  # 1 means the maximum number of waiting connections
    print(f"Listening at {listening_socket.getsockname()}")
    
    while True:
        connected_socket, client_socket_name = listening_socket.accept()
        print(f"We have accepted a connection from {client_socket_name}")
        print(f"  Socket name: {connected_socket.getsockname()}")
        print(f"  Socket peer: {connected_socket.getpeername()}")  # this is equivalent to client_sockname

        message = recvall(connected_socket, 16)
        print(f"  Incoming sixteen-octet message: {repr(message)}")
        connected_socket.sendall(b"Farewell, client")  # exactly 16 letters
        connected_socket.close()
        print("  Reply sent, socket closed")
    

def client(host, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # In TCP, the connect() method can fail 
    # because it needs to handshake with the server
    client_socket.connect((host, port))  
    print(f"Client has been assigned socket name {client_socket.getsockname()}")
    
    # data might be split across multiple packets and not sent all at once
    # so we need to make sure all data is sent
    client_socket.sendall(b"Hi there, server")  # exactly 16 letters
    
    reply = recvall(client_socket, 16)
    print(f"The server said {repr(reply)}")
    client_socket.close()


if __name__ == "__main__":
    choies = {"client": client, "server": server}
    parser = argparse.ArgumentParser(description="Send and receive over TCP")
    parser.add_argument("role", choices=choies, help="Choose 'client' or 'server'")
    parser.add_argument("host", help="Network the server listens at and the client sends to")
    parser.add_argument(
        "-p", metavar="PORT", type=int, default=1060, help="TCP port (default 1060)"
    )
    args = parser.parse_args()
    function = choies[args.role]
    function(args.host, args.p)
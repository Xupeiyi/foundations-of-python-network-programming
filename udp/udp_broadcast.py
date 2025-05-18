import socket, argparse

BUFSIZE = 65535


def server(interface, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((interface, port))
    print(f"Listening at {sock.getsockname()}")

    while True:
        client_data, client_address = sock.recvfrom(BUFSIZE)
        print(f"The client at {client_address} says {client_data.decode('ascii')}")
        

def client(network, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    text = "Broadcast datagram!"
    sock.sendto(text.encode("ascii"), (network, port))


if __name__ == '__main__':
    choices = {'client': client, 'server': server}
    parser = argparse.ArgumentParser(description="Send and receive UDP broadcast")
    parser.add_argument('role', choices=choices, help="Choose 'client' or 'server'")
    parser.add_argument('host', help="Network the server listens at and the client sends to")
    parser.add_argument('-p', metavar='PORT', type=int, default=1060, help='UDP port (default 1060)')
    args = parser.parse_args()
    function = choices[args.role]
    function(args.host, args.p)
import argparse, socket
from datetime import datetime


MAX_BYTES = 65535


def server(port):
    sock = socket.socket(
        socket.AF_INET,    # internet family of protocols
        socket.SOCK_DGRAM  # datagram socket (UDP)
    )
    sock.bind(("127.0.0.1", port))  # request a UDP network address
    print(f"Listening at {sock.getsockname()}")

    while True:
        client_data, client_address = sock.recvfrom(MAX_BYTES)
        client_text = client_data.decode('ascii')
        print(f"The client at {client_address} says {client_text}")

        server_text = f"Your data was {len(client_data)} bytes long"
        server_data = server_text.encode('ascii')
        sock.sendto(server_data, client_address)


def client(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    text = f"The time is {datetime.now()}"
    data = text.encode('ascii')
    sock.sendto(data, ("127.0.0.1", port))
    print(f"The OS assigned me the address {sock.getsockname()}")

    data, address = sock.recvfrom(MAX_BYTES)  # danger - the code did not check if data comes from the server
    text = data.decode("ascii")
    print(f"The server {address} replied: {text}")


if __name__ == "__main__":
    choices = {'client': client, 'server': server}
    parser = argparse.ArgumentParser(description="Send and receive UDP locally")
    parser.add_argument('role', choices=choices, help="Choose 'client' or 'server'")
    parser.add_argument('-p', metavar='PORT', type=int, default=1060, help='UDP port (default 1060)')
    args = parser.parse_args()
    function = choices[args.role]
    function(args.p)

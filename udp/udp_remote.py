import argparse, random, socket

MAX_BYTES = 65535


def server(interface, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((interface, port))
    print(f"Listening at {sock.getsockname()}")

    while True:
        client_data, client_address = sock.recvfrom(MAX_BYTES)

        if random.random() < 0.5:
            print(f"Pretending to drop packet from {client_address}")
            continue

        print(f"The client at {client_address} says {client_data.decode('ascii')}")
        server_text = f"Your data was {len(client_data)} bytes long"
        sock.sendto(server_text.encode("ascii"), client_address)


def client(hostname, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.connect((hostname, port))  # connect to the remote address
    print(f"Client socket name is {sock.getsockname()}")

    client_data = "This is another message".encode("ascii")

    delay = 0.1  # 0.1 seconds might be too short for a response to come back
    while True:
        sock.send(client_data)
        print(f"Waiting up to {delay} seconds for a reply")
        sock.settimeout(delay)

        try:
            server_data = sock.recv(MAX_BYTES)
        except socket.timeout:
            # exponential backoff
            delay *= 2
            if delay > 2.0:
                raise RuntimeError("I think the server is down")
        else:
            break

    print(f"The server says: {server_data.decode('ascii')}")


if __name__ == "__main__":
    choices = {"client": client, "server": server}
    parser = argparse.ArgumentParser(description="Send and receive UDP, pretending packets are often lost")
    parser.add_argument('role', choices=choices, help="Choose 'client' or 'server'")
    parser.add_argument("host", help="interface the server listens at; host the client sends to")
    parser.add_argument("-p", metavar="PORT", type=int, default=1060, help="UDP port (default 1060)")
    args = parser.parse_args()
    function = choices[args.role]
    function(args.host, args.p)

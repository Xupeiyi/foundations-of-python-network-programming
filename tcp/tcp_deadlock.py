import argparse, socket, sys


def server(host, port, bytecount):
    listening_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listening_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listening_socket.bind((host, port))
    listening_socket.listen(1)
    print(f"Listening at {listening_socket.getsockname()}")

    while True:
        connected_socket, client_socket_name = listening_socket.accept()
        print(f"Processing up to 1024 bytes at a time from {client_socket_name}")
        n = 0
        while True:
            data = connected_socket.recv(1024)  # will return 16 bytes if that's all there is
            if not data:
                break
            output = data.decode("ascii").upper().encode("ascii")
            # 2. the server can block here when the client's buffer is full
            # and it will not receive the data sent by the client
            # so gradually the client will stop sending data, creating a deadlock
            connected_socket.sendall(output)
            n += len(data)
            print(f"\r{n} bytes so far", end=" ")
            sys.stdout.flush()
        print()
        connected_socket.close()
        print("  Socket closed")


def client(host, port, bytecount):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    bytecount = (bytecount + 15) // 16 * 16  # round up to a multiple of 16
    message = b"capitalize this!"

    print(f"Sending {bytecount} bytes of data, in chunks of 16 bytes")
    client_socket.connect((host, port))

    sent = 0
    while sent < bytecount:
        # 1. the client sends the data but never receives it in this while loop
        # the client's TCP buffer can be full at some point, and the server will stop sending
        client_socket.sendall(message)
        sent += len(message)
        print(f"\r {sent} bytes sent", end=" ")
        sys.stdout.flush()

    print()
    client_socket.shutdown(socket.SHUT_WR)

    print("Receiving all the data the server sends back")

    received = 0
    while True:
        data = client_socket.recv(42)
        if not received:
            print(f"  The first data received says {repr(data)}")
        if not data:
            break
        received += len(data)
        print(f"\r   {received} bytes received", end=" ")

    print()
    client_socket.close()


if __name__ == "__main__":
    choices = {"client": client, "server": None}
    parser = argparse.ArgumentParser(description="Send deadlock over TCP")
    parser.add_argument("role", choices=choices, help="Choose 'client' or 'server'")
    parser.add_argument("host", help="Network the server listens at and the client sends to")
    parser.add_argument(
        "bytecount", type=int, nargs="?", default=16,
        help="Number of bytes for client to send (default 16)"
    )
    parser.add_argument(
        "-p", metavar="PORT", type=int, default=1060,
        help="TCP port (default 1060)"
    )
    args = parser.parse_args()
    function = choices[args.role]
    function(args.host, args.p, args.bytecount)
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
            data = connected_socket.recv(1024)
            if not data:
                break
            output = data.decode("ascii").upper().encode("ascii")
            connected_socket.sendall(output)
            n += len(data)
            print(f"\r{n} bytes so far", end=" ")
            sys.stdout.flush()
        print()
        connected_socket.close()
        print("  Socket closed")



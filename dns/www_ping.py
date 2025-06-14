import argparse, socket, sys
from pprint import pprint


def connect_to(hostname_or_ip):
    try:
        infolist = socket.getaddrinfo(
            hostname_or_ip, 'www', 0, socket.SOCK_STREAM, 0,
            socket.AI_ADDRCONFIG | socket.AI_CANONNAME | socket.AI_V4MAPPED 
        )
    except socket.gaierror as e:
        print(f"Name service failure: {e.args[1]}")
        sys.exit(1)

    info = infolist[0]  # try the first address as recommended
    print(info)

    socket_args = info[0:3]
    address = info[4]
    s = socket.socket(*socket_args)
    try:
        s.connect(address)
    except socket.error as e:
        print(f"Network failure: {e.args[1]}")
    else:
        print(f"Success: host {info[3]} is listening on port 80")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Try connecting to port 80")
    parser.add_argument("hostname", help="hostname that you want to contact")
    connect_to(parser.parse_args().hostname)
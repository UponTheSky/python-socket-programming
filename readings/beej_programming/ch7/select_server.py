import socket
import select
import sys

from ._utils import get_listener_socket


PORT = 9034
BACKLOG = 10
TIMEOUT = 2.5


def main() -> None:
    read_socks: list[socket.socket] = []

    listener = get_listener_socket(port=PORT, backlog=BACKLOG)
    listener.setblocking(False)

    read_socks.append(listener)

    while True:
        try:
            rlist, _, _ = select.select(read_socks, [], [], TIMEOUT)

            for read_sock in rlist:
                try:
                    if read_sock.fileno() == listener.fileno():
                        conn, addr = listener.accept()

                        conn.setblocking(False)
                        read_socks.append(conn)
                        print(f"select server: new connection from {addr} on socket {conn}")

                    else:
                        response = read_sock.recv(4096)

                        if not response:
                            print(f"connection on {read_sock} closed - EOF")
                            read_socks.remove(read_sock)

                        else:
                            for other_read_sock in rlist:
                                if other_read_sock.fileno() not in (read_sock.fileno(), listener.fileno()):
                                    other_read_sock.send(response)

                except OSError as error:
                    print(f"error while handling reading sockets: {error}")

        except OSError as error:
            print(f"error while select: {error}")
            sys.exit(1)
    

if __name__ == "__main__":
    main()

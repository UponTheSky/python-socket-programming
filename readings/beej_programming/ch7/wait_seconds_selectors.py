"""
Additional reference: https://docs.python.org/3/library/selectors.html
"""

import selectors
import socket


TIMEOUT_SECONDS = 3

selector = selectors.DefaultSelector()


def read(conn: socket.socket, mast: int) -> None:
    data = conn.recv(4096)

    if data:
        print("received: ", data)

    else:
        print("closing the current connection", conn)
        selector.unregister(conn)
        conn.close()


def accept(sock: socket.socket, mask: int) -> None:
    conn, addr = sock.accept()
    print("accepted", conn, "from", addr)

    conn.setblocking(False)
    # this registers newly created connection to the selector, and 
    # this selector polls the connection socket to check whether there 
    # is something to be received from the remote client
    selector.register(conn, selectors.EVENT_READ, read)


def run() -> None:
    # prepare a non blocking server
    listener_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener_sock.bind(("localhost", 8080))
    listener_sock.listen(100)
    listener_sock.setblocking(False)

    # register events to the selector
    # this listener socket mainly deals with creating new sockets whenever there is an incoming request
    selector.register(listener_sock, selectors.EVENT_READ, accept)

    while True:
        events = selector.select(TIMEOUT_SECONDS)




if __name__ == "__main__":
    run()
import socket
import select
import sys
from typing import Mapping

from ._utils import get_listener_socket


PORT = 9034
BACK_LOG = 20
POLL_TIMEOUT = 3000


def _add_to_pfds(
    *, poll: select.poll, sock: socket.socket, sock_table: Mapping[int, socket.socket]
) -> None:
    new_fd = sock.fileno()

    if new_fd in sock_table:
        raise RuntimeError(f"the socket with fd {new_fd} is already registered")

    poll.register(new_fd, select.POLLIN)
    sock_table[new_fd] = sock


def _del_from_pfds(
    *, poll: select.poll, sock: socket.socket, sock_table: Mapping[int, socket.socket]
) -> None:
    fd = sock.fileno()

    if fd in sock_table:
        del sock_table[fd]

    poll.unregister(fd)


def main() -> None:
    poll = select.poll()
    sock_table: dict[str, socket.socket] = {}

    listener: socket.socket = get_listener_socket(port=PORT, backlog=BACK_LOG)
    listener.setblocking(False)

    _add_to_pfds(poll=poll, sock=listener, sock_table=sock_table)

    while True:
        try:
            events = poll.poll(POLL_TIMEOUT)

            if not events:
                print(f"poll timeout of {POLL_TIMEOUT} millisecs")
                continue

            for fd, event in events:
                if not (event & select.POLLIN):
                    print(f"unexpected event {event} for registered fd {fd}")
                    continue

                if fd == listener.fileno():
                    conn, addr = listener.accept()
                    print(f"new connection from address: {addr}")

                    conn.setblocking(False)
                    _add_to_pfds(poll=poll, sock=conn, sock_table=sock_table)

                else:
                    conn = sock_table[fd]
                    response = conn.recv(4096)

                    if not response:
                        print(f"connection of fd {fd} has been closed")
                        conn = sock_table[fd]

                        _del_from_pfds(poll=poll, sock=conn, sock_table=sock_table)
                        conn.close()

                    else:
                        print("get response: ", response)
                        for other_conn in sock_table.values():
                            if other_conn not in (conn, listener):
                                # other_conn.send(response)
                                other_conn.sendall(response)

        except OSError as error:
            print(f"error while polling the sockets: {error}")
            sys.exit(1)

        except Exception as error:
            print(f"unexpected error: {error}")
            sys.exit(1)


if __name__ == "__main__":
    main()

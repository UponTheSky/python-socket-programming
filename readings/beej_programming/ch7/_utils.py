import socket
import sys

def get_listener_socket(*, port: int, backlog: int) -> socket.socket:
    try:
        addrinfos = socket.getaddrinfo(
            None,
            port,
            socket.AF_UNSPEC,
            socket.SOCK_STREAM,
            socket.IPPROTO_TCP,
            socket.AI_PASSIVE,
        )

        if not addrinfos:
            raise OSError("no address info has been fetched")

        for addrinfo in addrinfos:
            family, type_, proto, _, sockaddr = addrinfo
            try:
                sock = socket.socket(family, type_, proto)
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                sock.bind(sockaddr)
                sock.listen(backlog)

                return sock

            except OSError as error:
                print(f"socket creation error: {error}")
                sys.exit(1)

            except Exception as error:
                print(f"unexpected error {error}")
                sys.exit(1)

    except socket.gaierror as error:
        print(f"address error: {error}")
        sys.exit(1)

    except Exception as error:
        print(f"unexpected error {error}")
        sys.exit(1)

    else:
        raise OSError(f"failed to bind to the port {port}")
    
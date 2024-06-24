import sys
import socket


def client_tcp(*, host: str, port: int) -> None:
    """
    Makes a simple and primitive client request to the server of given (host, port)
    """
    try:
        # step 1: get address information of the remote server
        remote_addrinfo = socket.getaddrinfo(
            host=host, port=port, family=socket.AF_UNSPEC, type=socket.SOCK_STREAM
        )

        for remote_addr in remote_addrinfo:
            family, socket_type, proto, _, (remote_host, remote_port) = remote_addr
            print(
                f"family={family}, socket_type={socket_type}, prototype={proto}, remote_host={remote_host}, remote_port={remote_port}"
            )

            # step 2: create a socket fd and simply connect
            try:
                with socket.socket(family, socket_type, proto) as sock:
                    sock.connect((remote_host, remote_port))
                    print(f"client has been connected to {remote_host}:{remote_port}")

                    request = b"hello from the python tcp client!"
                    sock.send(request)

                    response = sock.recv(4096)
                    print(f"response: {response}")

            except OSError | TimeoutError as error:
                print(
                    f"error while connecting to the (host:port): ({host}:{port}) - {error}",
                    file=sys.stderr,
                )
                continue

            break

    except socket.gaierror as addr_error:
        print(f"address error: {addr_error}", file=sys.stderr)
        exit(1)

    except Exception as error:
        print(f"unexpected error: {error}", file=sys.stderr)
        exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise ValueError("provide (host, port) pair")

    host, port = sys.argv[1], sys.argv[2]

    if not port.isdigit():
        raise ValueError("a given port should be an integer")

    client_tcp(host=host, port=port)

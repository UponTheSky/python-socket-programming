import sys
import socket
import multiprocessing as mp


def handle_incoming_connection(sock: socket.socket, response_message: bytes) -> None:
    sent_len = sock.send(response_message)
    print(f"length of {sent_len} bytes has been sent")

    response = sock.recv(4096) 
    
    if len(response) == 0:
        print("end of connection")

    print(str(response))


def server_tcp(*, port: int) -> None:
    """Serves simple TCP stream requests"""
    try:
        # step 1: get address information of the current host server
        host_addrinfo = socket.getaddrinfo(
            host=None,
            port=port,
            family=socket.AF_INET,
            type=socket.SOCK_STREAM,
            flags=socket.AI_PASSIVE,
        )

        for host_addr in host_addrinfo:
            family, socket_type, proto, _, (host_host, host_port) = host_addr
            print(
                f"family={family}, socket_type={socket_type}, prototype={proto}, host={host_host}, port={host_port}"
            )
            
            try:
                # step 2: create a socket and setup socket options
                with socket.socket(family, socket_type, proto) as sock:
                    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

                    # step 3: bind the socket to the host machine's host and port, and listen
                    sock.bind((host_host, host_port))
                    sock.listen(10)
                    print(f"server has been binded to, and is listening to {host_host}:{host_port}")

                    # step 3: accept incoming connections
                    while True:
                        new_sock, (incoming_host, incoming_port) = sock.accept()
                        print(f"incoming_host={incoming_host}, incoming_port={incoming_port}")

                        # create a new process to handle the new socket fd
                        subprocess = mp.Process(target=handle_incoming_connection, args=(new_sock, b"hello, this is server!"))

                        subprocess.start()
                        subprocess.join()

            except OSError as error:
                print(
                    f"error while serving the (host:port): ({host_host}:{host_port}) - {error}",
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
    if len(sys.argv) != 2:
        raise ValueError("provide port")

    port = sys.argv[1]

    if not port.isdigit():
        raise ValueError("a given port should be an integer")

    server_tcp(port=port)

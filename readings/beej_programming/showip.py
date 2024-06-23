import socket
import sys

def showip(hostname: str) -> None:
    """
    Show IP adddresses for a host given on the command line    
    """
    family = socket.AF_UNSPEC # either v4 or v6
    socket_type = socket.SOCK_STREAM # TCP

    try:
        addrinfo = socket.getaddrinfo(host=hostname, port=0, family=family, type=socket_type)

        for addr in addrinfo:
            addr_family, addr_socket_type, addr_proto, _, (address, port) = addr
            print(addr_family, addr_socket_type, addr_proto, address, port)

            # ip_str = socket.inet_ntop(addr_family, address) # required in the C code, not here
            print(address)

    except socket.gaierror as error:
        print(error)
        sys.exit(1)

    except Exception as error:
        print(f"unexpected error: {error}")

if __name__ == "__main__":
    hostname = sys.argv[1]
    showip(hostname)
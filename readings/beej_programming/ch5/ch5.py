from socket import *

# 5.1 - getaddrinfo
# in C, we have a linkedlist as a result
# instead of not having to prepare for the struct addrinfo,
# we can provide the options - family, type, proto, flags
# see:
host_address = "www.example.net"  # either domain name or ip address
port = 443  # actual port number or service name such as http
family = AF_INET
sock_type = SOCK_STREAM
protocol = getprotobyname("tcp")

assert protocol == IPPROTO_TCP

try:
    # when making a client request
    addrinfo_client = getaddrinfo(
        host=host_address, port=port, family=family, type=sock_type, proto=protocol
    )
    # when making a server hosting, passing the AI_PASSIVE flag so that the function
    # automatically fills the IP address of the host
    addrinfo_server = getaddrinfo(
        host=None,
        port=80,
        family=family,
        type=sock_type,
        proto=protocol,
        flags=AI_PASSIVE,
    )

    # print(addrinfo_client)
except gaierror as error:
    print(error)


# the data to be used below
addrinfo_client = getaddrinfo(
    host="www.example.com", port="http", family=AF_INET, type=SOCK_STREAM, proto=0
)
addrinfo_server = getaddrinfo(
    host=None, port="http", family=AF_INET, type=SOCK_STREAM, proto=0, flags=AI_PASSIVE
)

# need to check whether addrinfo is empty first
assert len(addrinfo_client) > 0
assert len(addrinfo_server) > 0

# assuming the first node is okay
addr_client = addrinfo_client[0]
addr_server = addrinfo_server[0]

# 5.2 - socket
# in C, this is for getting the corresponding file descriptor
# but in Python, we have a high-level abstraction object `socket`.
# usually the fields are fed by the result of the call to getaddrinfo
# REMARK: in the Python docs, the family is AF_* family, whereas in the book it says PF_* family.
# use `with ... as sock:` statement in production

client_family, client_sock_type, client_proto, _, (client_address, client_port) = (
    addr_client
)
sock_client = socket(family=client_family, type=client_sock_type, proto=client_proto)

server_family, server_sock_type, server_proto, _, (server_address, server_port) = (
    addr_server
)
sock_server = socket(family=server_family, type=server_sock_type, proto=server_proto)

# 5.3 - bind
# since we haven't related the socket fd to the address and port, we need to do so.
# this is necessary for the server part.
# for the client connection, the kernel will assign an unused local port to the socket fd if necessary
try:
    sock_server.bind((server_address, server_port))

except OSError as error:
    print(error)

# 5.4 - connect
# the client asks connection to a remote server
try:
    sock_client.connect((client_address, client_port))
    print("getpeername:", sock_client.getpeername())  # get the remote server's name

except OSError as error:
    print(error)

except TimeoutError | InterruptedError as error:
    print(error)

# 5.5 listen
# only for the server
# wait for the incoming connections
sock_server.listen(10)  # backlog: the length of the waiting queue

# 5.6 accept
# only for the server
# it will create a new socket fd, and you can send and receive messages through that new socket

IS_SERVER_RUN = False

if IS_SERVER_RUN:
    sock_req, req_addr = sock_server.accept()
    print(req_addr)

    # 5.7 send() and recv()
    # use socket fd as a medium to communicate with remote clients/servers
    server_recv_message = sock_req.recv(4096)  # 4096 - buffer size
    print(server_recv_message)  # if the message is 0 byte, the connection is over
    sock_req.send(b"HTTP/1.1 200 OK\r\nContent-Length: 9\r\n\r\nHi there!")

    sock_req.close()

IS_CLIENT_RUN = False

if IS_CLIENT_RUN:
    sock_client.send(b"GET / HTTP/1.1\r\n\r\n")
    print(sock_client.recv(4096))

# 5.8 sendto() and recvfrom()
# if you use datagram socket(`SOCK_DGRAM`), we don't have to connect to a specific client / server.
# instead, we directly send / recv data using sendto() and recvfrom()

IS_UDP_RUN = False

if IS_UDP_RUN:
    sock_udp_client = socket(
        AF_INET, SOCK_DGRAM
    )  # should not be connected to a remote server
    sock_udp_client.sendto(b"GET / HTTP/1.1\r\n\r\n", ("www.example.com", 80))
    print(sock_udp_client.recvfrom(4096))
    sock_udp_client.close()

# 5.9 close() and shutdown()
# shutdown() simply disable further send() and recv()
# in any cases, we need to call close() to retrieve the resources from the socket
sock_client.close()

GRACEFULL_SHUTDOWN = False

if GRACEFULL_SHUTDOWN:
    sock_server.shutdown(SHUT_RD)  # further read is disallowed
    import time

    time.sleep(300)  # close after 5 minutes

sock_server.close()

# 5.10 getpeername() / 5.11 gethostname()
# getpeername() is tied to the client socket
# gethostname() can be useful on the server side
# gethostname() is not tied to a certain socket
print("gethostname", gethostname())

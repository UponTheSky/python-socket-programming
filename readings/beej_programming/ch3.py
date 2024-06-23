import sys
from socket import *

# 3.1
# IP v4 and v6
# subnet(masks), port numbers

# 3.2
# big vs little endian
# htons, htonl, ntohs, ntohl
# 42 -> 42 * (1 << 4)
host_number = 127
assert htons(host_number) == host_number * (1 << 8)
assert ntohs(htons(host_number)) == host_number

# 3.3, 3.4
# C struct used by the network syscalls
# here we don't need such struct
# inet_pton is required for translating human readable ip address strings 
# into bytes that is to be used in the low level functions

ip_address = "127.0.0.1" 

try:
   packed_ip = inet_pton(AF_INET, ip_address)
   assert ip_address == inet_ntop(AF_INET, packed_ip)
except OSError as error:
    print(f"error: {error}", file=sys.stderr)

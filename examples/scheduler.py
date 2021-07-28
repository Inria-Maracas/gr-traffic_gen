import socket
import time
import numpy as np

# addressing information of target
IPADDR = '127.0.0.1'
PORTNUM = 7000
ip_base = 'mnode'

# enter the data content of the UDP packet as hex
PACKETDATA = np.ones(1, dtype=np.uint8)*0

# initialize a socket, think of it as a cable
# SOCK_DGRAM specifies that this is UDP
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)


PACKETDATA = np.array([10, 0.34, 0.001], dtype=np.float64).tobytes()
# IPADDR = ip_base+str(node)

try:
    # send the command
    s.sendto(PACKETDATA, (IPADDR, PORTNUM))
except:
    pass

    #Let's do it again


# close the socket
s.close()

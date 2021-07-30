import socket
import time
import numpy as np
from gnuradio.eng_arg import eng_float, intx
from argparse import ArgumentParser


def argument_parser():
    parser = ArgumentParser()
    parser.add_argument(
        "-p", "--port", dest="port", type=int, default=7000,
        help="Set base port [default=%(default)r]")
    parser.add_argument(
        "-t", "--tx_node", dest="tx", type=int, default=3,
        help="Set TX node number [default=%(default)r]")
    parser.add_argument(
        "-r", "--rn_node", dest="rx", type=int, default=9,
        help="Set RX node number [default=%(default)r]")
    parser.add_argument(
        "-w", "--wait_time", dest="time", type=float, default=0.01,
        help="Set wait time between transmissions [default=%(default)r]")
    return parser


def main():

    options = argument_parser().parse_args()

    # addressing information of target
    IPADDR = '127.0.0.1'
    PORTNUM = options.port
    ip_base = 'mnode'
    tx_node = options.tx
    rx_node = options.rx
    SLEEP_TIME=options.time
    possible_bw = np.array([0.01,0.05,0.1,0.2,0.5])
    # initialize a socket, think of it as a cable
    # SOCK_DGRAM specifies that this is UDP
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)


    time.sleep(1)
    while(True):
        #Wait a bit to sent next order
        time.sleep(SLEEP_TIME)


        modulation = 0
        pack_len = 100
        bw_ratio = possible_bw[4]#[np.random.randint(5)]
        freq_shift = 0

        # Send to transmitter
        PACKETDATA = np.array([pack_len, bw_ratio, freq_shift], dtype=np.float64).tobytes()
        IPADDR = IPADDR#ip_base+str(tx_node)
        try:
            # send the command
            s.sendto(PACKETDATA, (IPADDR, PORTNUM+modulation))
        except:
            pass

        # # Send to reciever
        # PACKETDATA = np.array([modulation, pack_len, bw_ratio, freq_shift], dtype=np.float64).tobytes()
        # IPADDR = ip_base+str(rx_node)
        # try:
        #     # send the command
        #     s.sendto(PACKETDATA, (IPADDR, PORTNUM))
        # except:
        #     pass

            #Let's do it again


    # close the socket
    s.close()

if __name__ == '__main__':
    main()

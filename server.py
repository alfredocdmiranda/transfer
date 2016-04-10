#!/usr/bin/python3

import os
import sys
import socket
import struct
import argparse


def loadbar(total, current, tiles=10):
    sys.stdout.write("\033[K")
    print("[", end="")
    tile_value = int(total)/tiles
    for i in range(1, tiles+1):
        if current >= i*tile_value:
            print("#", end="")
        else:
            print(" ", end="")

    print("]", end="")
    print("\t{}/{}".format(current,total),end="\r")

def arguments():
    global args

    parser = argparse.ArgumentParser(description='File Receiver.', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('filename', help="Filename to be saved.")
    parser.add_argument('-p', '--port', help="Port where the sender will connect.", default=8000, type=int)
    parser.add_argument('-o', '--overwrite', help="Overwrite existing file.", action='store_true')
    #parser.add_argument('-s', '--size', help="Blocks' size in bytes to be received.", default=256, type=int)
    args = parser.parse_args()

if __name__ == '__main__':
    arguments()
    
    if not args.overwrite and os.path.exists(args.filename):
        print("File already exists.")
        exit(1)
        

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR, 1)
    s.bind(('', args.port))
    s.listen(1)

    print("Waiting connection...")
    conn, addr = s.accept()
    print('Connected by {a[0]}:{a[1]}'.format(a=addr))
    print("")

    block_size = struct.unpack('i',conn.recv(4))[0]
    print("Blocks' size: {}".format(block_size))
    file_size = struct.unpack('i',conn.recv(4))[0]
    print("File size: {}".format(file_size))

    with open(args.file, "wb") as f:
        recv = 0
        while recv < file_size:
            aux = conn.recv(block_size)
            recv += len(aux)
            f.write(aux)
            loadbar(file_size, recv)
        print("")

    conn.close()

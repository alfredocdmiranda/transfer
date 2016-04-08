#!/usr/bin/python3

import sys
import socket
import struct
import argparse

import time


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
    
    parser = argparse.ArgumentParser(description='File Sender.', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('host', help="Host that will receive the file.")
    parser.add_argument('file', help="File to be sent.")
    parser.add_argument('-p', '--port', help="Port where the receiver is listening.", default=8000, type=int)
    parser.add_argument('-s', '--size', help="Blocks' size in bytes to be sent.", default=256, type=int)
    args = parser.parse_args()

if __name__ == '__main__':
    arguments()
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        #Load the file
        with open(args.file, "rb") as f:
            data = f.read()
    except IOError as e:
      print(e)
      exit(e.errno)
    
    print("Trying to connect on {a.host}:{a.port}".format(a=args))
    try:
        s.connect((args.host, args.port))
        print("Successful connected!")
    except socket.error as e:
        print(e)
        exit(e.errno)
    
    #Sending block size
    s.send(struct.pack("i", args.size))
    #Sending file's size
    f_size = len(data)
    s.send(struct.pack("i", f_size))
    
    sent = 0
    while sent < f_size:
        start = sent
        end = sent + args.size
        if end > f_size:
            end = f_size
        s.send(data[start:end])
        sent += args.size
        #time.sleep(1)
        loadbar(f_size, sent)
    print("")

    s.close()

    
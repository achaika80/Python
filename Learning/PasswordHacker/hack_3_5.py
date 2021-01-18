# write your code here
import argparse
import sys
import socket
import itertools

#parser = argparse.ArgumentParser(description="hacking website passwords")

#parser.add_argument("addrress")
#parser.add_argument("port")
#parser.add_argument("password")

args = sys.argv

ipaddress = args[1]
port = int(args[2])

def make_connection(ipaddress, port):
    strpass = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    #ch = itertools.chain.from_iterable(itertools.combinations_with_replacement(strpass, r) for r in range(len(strpass)+1))
    # with socket.socket() as c_socket:
    #     c_socket.connect((ipaddress, port))
    #     password = 'az'
    #     print(password)
    #     e_password = password.encode()
    #     c_socket.send(e_password)
    #     e_response = c_socket.recv(1024)
    #     response = e_response.decode()
    #     print(response)
    #     return password

    with socket.socket() as c_socket:
        response = ''
        ch = itertools.chain.from_iterable(itertools.combinations_with_replacement(strpass, r) for r in range(len(strpass)+1))
        next(ch)
        c_socket.connect((ipaddress, port))
        for c in ch:
            #print(c)
            password = ''.join(c)
            #print(f'password is {password}')
            e_password = password.encode()
            c_socket.send(e_password)
            e_response = c_socket.recv(1024)
            response = e_response.decode()
            #print(response)
            if response == 'Connection success!':
                break
    return password


        # while response != 'Connection success!':
        #     password = ''.join(next(ch))
        #     print(password)
        #     e_password = password.encode()
        #     c_socket.send(e_password)
        #     e_response = c_socket.recv(1024)
        #     response = e_response.decode()
        #     print(response)
        # return password

#ipaddress = '127.0.0.1'
#port = 9090

response = make_connection(ipaddress, port)
print(response)



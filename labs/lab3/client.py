import zmq
import sys
import threading

context = zmq.Context()

sock_req = context.socket(zmq.REQ)
sock_req.connect("tcp://127.0.0.1:5678")

sock_sub = context.socket(zmq.SUB)
sock_sub.setsockopt_string(zmq.SUBSCRIBE, '')
sock_sub.connect("tcp://127.0.0.1:5679")

def recv():
    while True:
        name, message = sock_sub.recv_pyobj()
        if user != name:
            print('\r', end="")
            print('[{}]: {}\n[{}]> '.format(name, message, user), end="")
            
user = sys.argv[1]
print('User[' + user + '] Connected to the chat server.')
thread = threading.Thread(target = recv, args=())
thread.start()

while True:
    msg = input('[{}]> '.format(user))
    sock_req.send_pyobj((user, msg))
    sock_req.recv_string()

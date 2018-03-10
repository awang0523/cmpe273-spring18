import zmq

# ZeroMQ Context
context = zmq.Context()

# Define the socket using the "Context"
sock_rep = context.socket(zmq.REP)
sock_rep.bind("tcp://127.0.0.1:5678")
sock_pub = context.socket(zmq.PUB)
sock_pub.bind("tcp://127.0.0.1:5679")

print("Server started.")

while True:
    user, message = sock_rep.recv_pyobj()
    sock_rep.send_string('')
    sock_pub.send_pyobj((user, message))

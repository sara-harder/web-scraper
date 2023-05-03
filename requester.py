import zmq

context = zmq.Context()

#  Socket to talk to server
print("Connecting to server…")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:2007")

request = "https://en.wikipedia.org/wiki/Uncompahgre_Peak"

print(f"Sending request {request} …")
socket.send(bytes(request, "utf-8"))

#  Get the reply.
message = socket.recv()
message = message.decode("utf-8")
print(f"Received reply: {message}")

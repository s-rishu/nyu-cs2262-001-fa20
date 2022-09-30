from flask import Flask, request, Response
from flask_api import status

import socket

app = Flask(__name__)
@app.route('/')
def hello_world():
    return 'Hello, this is fibonacci server!'

@app.route('/register', methods=['PUT'], strict_slashes=False)
def register():
    body = request.get_json(force=True)
    message = "TYPE={}\nNAME={}\nVALUE={}\nTTL={}".format('A', body["hostname"], body["ip"], 10) #type=A and ttl=10
    as_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    as_socket.sendto(message.encode(), (body["as_ip"], int(body["as_port"])))
    message, server_add = as_socket.recvfrom(2048)
    as_socket.close()
    if message.decode()=="Success":
        return Response(status=201)
    else:
        return Response(status=400)

@app.route('/fibonacci', methods=['GET'], strict_slashes=False)
def fibonacci():
    args = request.args
    try:
        number = int(args.get("number"))
        assert number!=None
    except:
        return "Parameters are in wrong format.", status.HTTP_400_BAD_REQUEST

    return str(fib_calc(number))

def fib_calc(number):

    if number<0:
        return("Please enter a positive number.")
    if number==0:
        return 0
    if number==1 or number==2:
        return 1
    return fib_calc(number-1) + fib_calc(number-2)

app.run(host='0.0.0.0',
        port=9090,
        debug=True)

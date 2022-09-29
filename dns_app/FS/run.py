from flask import Flask, request
from flask_api import status

import socket

app = Flask(__name__)
@app.route('/')
def hello_world():
    return 'Hello, this is fibonacci server!'

@app.route('/register', methods=['PUT'])
def register():
    body = request.get_json(force=True)
    message = "TYPE={}\nNAME={}\nVALUE={}\nTTL={}\n".format('A', body["hostname"], body["ip"], 10)
    as_socket = socket(socket.AF_INET, socket.SOCK_DGRAM)
    as_socket.sendto(message.encode(), (body["as_ip"], body["as_port"]))
    message, server_add = as_socket.recvfrom(2048)
    as_socket.close()
    if message=="Success":
        return status.HTTP_201_CREATED
    else:
        return status.HTTP_400_BAD_REQUEST

@app.route('/fibonacci', methods=['GET'])
def fibonacci():
    print("hi")
    args = request.args
    try:
        number = int(args.get("number"))
        assert number!=None
    except:
        return "Parameters are in wrong format.", status.HTTP_400_BAD_REQUEST
    print(number)
    return str(fib_calc(number))

def fib_calc(number):
    print("calculating")
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

from flask import Flask, request
from flask_api import status
import requests

import socket

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, this is user server!'

@app.route('/fibonacci', methods=['GET'], strict_slashes=False)
def fibonacci():
    #get arguments
    args = request.args
    try:
        hostname = args.get("hostname")
        fs_port = int(args.get("fs_port"))
        number = args.get("number")
        as_ip = args.get("as_ip")
        as_port = int(args.get("as_port"))
        assert hostname!=None
        assert fs_port!=None
        assert number!=None
        assert as_ip!=None
        assert as_port!=None
    except:
        return "Parameters are missing", status.HTTP_400_BAD_REQUEST

    #get hostname ip
    message = "TYPE={}\nNAME={}".format('A', hostname)
    as_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    as_socket.sendto(message.encode(), (as_ip, as_port))
    response, server_add = as_socket.recvfrom(2048)
    as_socket.close()
    response = response.decode()
    response = response.split('\n')
    for data in response:
        data = data.split('=')
        if data[0] == "VALUE":
            hostname_ip = data[1]

    #get request to FS server
    url = 'http://%s:%s/fibonacci?number=%s'%(hostname_ip,fs_port, number)
    fib = requests.get(url).content.decode()
    return str(fib)


app.run(host='0.0.0.0',
        port=8080,
        debug=True)
